#!/usr/bin/env python3
"""Stage-3 labeler rewired to the LOCAL CourtListener Postgres replica (on Atlas).

Replaces the API-based build_labels.py: reverse-citation, docket lineage, and opinion text are now
fast local SQL joins instead of rate-limited/timing-out API calls. `--demo` validates the mechanics
(reverse-citation speed, docket-lineage linkage, disposition/gate detection) on a small sample. It
computes NO study labels over the corpus and NO pathology score S -- the labeled dataset is built only
AFTER the freeze (prereg-legal-reversal-v1). Run ON ATLAS.

    python3 cl_labels_sql.py --demo
"""
from __future__ import annotations

import argparse
import re
import subprocess
import time

# disposition + ground->deontic-gate detection (same as the API version)
REVERSE = re.compile(r"\b(revers|vacate|vacat|set aside|overrul)", re.I)
AFFIRM = re.compile(r"\baffirm", re.I)
GATE = {
    "legitimate_authority": re.compile(r"jurisdic|standing|ultra vires|lacked (?:the )?authority", re.I),
    "valid_consent": re.compile(r"due process|waiver|voluntar|coerc|without consent", re.I),
    "universalizability": re.compile(r"equal protection|similarly situated|disparate treatment", re.I),
    "mere_means": re.compile(r"cruel and unusual|human dignity|instrumentaliz", re.I),
}


def q(sql, timeout=60):
    """Run a query against the local replica; return list of rows (each a list of column strings)."""
    r = subprocess.run(
        ["sudo", "-u", "postgres", "psql", "-d", "courtlistener", "-tAF", "\t", "-c", sql],
        capture_output=True, text=True, timeout=timeout,
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split("\t") for ln in r.stdout.strip().split("\n") if ln]


def disposition(text):
    disp = "reverse" if REVERSE.search(text) else ("affirm" if AFFIRM.search(text) else "unclear")
    gates = [g for g, pat in GATE.items() if pat.search(text)]
    return disp, gates


def demo():
    print("== Stage-3 labeler on LOCAL Postgres replica (mechanics only; NO labels/S) ==\n")

    # 0. corpus reachable
    t = time.time()
    n_op = q("SELECT count(*) FROM search_opinion")[0][0]
    n_cite = q("SELECT count(*) FROM search_opinionscited")[0][0]
    n_oci = q("SELECT count(*) FROM search_originatingcourtinformation WHERE docket_number <> ''")[0][0]
    print(f"corpus: {int(n_op):,} opinions, {int(n_cite):,} citation edges, "
          f"{int(n_oci):,} originating-court-info rows with a docket# ({time.time()-t:.2f}s)")

    # 1. reverse-citation, instant (this is what timed out on the API)
    t = time.time()
    row = q("SELECT cited_opinion_id, count(*) c FROM search_opinionscited "
            "GROUP BY cited_opinion_id ORDER BY c DESC LIMIT 1")[0]
    oid, c = row[0], row[1]
    print(f"\nreverse-citation: most-cited opinion {oid} has {int(c):,} citing opinions "
          f"(indexed lookup, {time.time()-t:.2f}s)")

    # 2. docket-lineage linkage: appellate originating-docket -> the lower opinion it reviewed
    t = time.time()
    pairs = q(
        "SELECT oci.docket_number, low.id, low_c.case_name "
        "FROM search_docket ad "
        "JOIN search_originatingcourtinformation oci ON oci.id = ad.originating_court_information_id "
        "JOIN search_docket low ON low.docket_number = oci.docket_number AND low.court_id <> ad.court_id "
        "JOIN search_opinioncluster low_c ON low_c.docket_id = low.id "
        "WHERE ad.originating_court_information_id IS NOT NULL AND oci.docket_number <> '' LIMIT 3",
        timeout=120)
    print(f"\ndocket-lineage join (appellate originating-docket -> reviewed lower case), "
          f"{time.time()-t:.2f}s:")
    for p in pairs:
        print(f"  originating docket# {p[0]!r} -> lower docket {p[1]}  {str(p[2])[:45]!r}")
    if not pairs:
        print("  (no direct docket-number matches in the sampled rows; lineage also derivable via "
              "the citation graph -- both are now local joins)")

    # 3. disposition + gate detection on real opinion text (fast text pull from the replica)
    t = time.time()
    txt = q("SELECT coalesce(nullif(plain_text,''), html_with_citations) FROM search_opinion "
            "WHERE plain_text ~* 'we reverse' AND length(plain_text) BETWEEN 2000 AND 8000 LIMIT 1")
    if txt and txt[0][0]:
        disp, gates = disposition(txt[0][0][:6000])
        print(f"\ndisposition detection on a real opinion ({time.time()-t:.2f}s): "
              f"disp={disp}, gate(s)={gates}")

    print("\nAll lineage/citation/text ops are now local SQL -- the API rate-limit/timeout wall is gone. "
          "Building the full labeled dataset (link every decision -> reviewer -> disposition/ground -> "
          "KeyCite-validate) is Stage 3 PROPER and runs only AFTER the freeze.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        demo()
    else:
        print("use --demo (pre-freeze mechanics). Full label build is post-freeze.")


if __name__ == "__main__":
    main()
