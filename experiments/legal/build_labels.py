#!/usr/bin/env python3
"""Stage 3 (label construction) of the legal-reversal study -- LINKAGE MECHANICS ONLY.

Given a decision, find the opinion that later REVIEWED it (via the citation graph), and detect the
disposition (reverse/vacate vs affirm) + the GROUND, mapped to the ErisML deontic gates. This file is
the plumbing for the reversal label; run as `--demo` it exercises the mechanics on one opinion and
reports what the pipeline can/can't do. It computes NO study labels over a corpus and NO pathology
score, and it must only be used to BUILD the labeler -- the labeled corpus is generated AFTER the
freeze (RUNBOOK_legal_reversal.md, FREEZE_PROTOCOL.md).

The hard, unsolved part is disambiguating "reviewed by" from "merely cited by": most citing opinions
cite for precedent, not because they reviewed the case. Real Stage 3 needs docket/subsequent-history
lineage + Westlaw KeyCite validation; this demo shows the ingredients, not a solved labeler.

    python build_labels.py --demo 8504381
"""
from __future__ import annotations

import argparse
import re
import time
import cl_fetch as clf   # reuse get(), token(), API, opinion_text() -- same dir

# disposition + ground -> deontic-gate mapping (regex ingredients, not a validated classifier)
REVERSE = re.compile(r"\b(revers|vacate|vacat|set aside|overrul)", re.I)
AFFIRM = re.compile(r"\baffirm", re.I)
GROUND_GATES = {
    "legitimate_authority": re.compile(r"jurisdic|standing|ultra vires|lacked (?:the )?authority|want of authority", re.I),
    "valid_consent": re.compile(r"due process|waiver|voluntar|coerc|without consent|notice and", re.I),
    "universalizability": re.compile(r"equal protection|similarly situated|disparate treatment", re.I),
    "mere_means": re.compile(r"cruel and unusual|human dignity|instrumentaliz", re.I),
}


def cited_by(opinion_id, tok, limit=8):
    """Opinions that CITE this one (candidate reviewers live here)."""
    d = clf.get(f"{clf.API}/opinions-cited/", tok, {"cited_opinion": opinion_id, "page_size": limit})
    ids = []
    for r in d.get("results", [])[:limit]:
        u = r.get("citing_opinion") or ""
        m = re.search(r"/opinions/(\d+)/", u)
        if m:
            ids.append((int(m.group(1)), r.get("depth")))
    return ids


def opinion_ctx(opinion_id, tok):
    """(case_name, date_filed, text) for an opinion via its cluster."""
    op = clf.get(f"{clf.API}/opinions/{opinion_id}/", tok)
    _, text = clf.opinion_text(op)
    cl_url = op.get("cluster") or ""
    m = re.search(r"/clusters/(\d+)/", cl_url)
    name, date = None, None
    if m:
        cl = clf.get(f"{clf.API}/clusters/{m.group(1)}/", tok)
        name, date = cl.get("case_name"), cl.get("date_filed")
    return name, date, (text or "")


def name_overlap(a, b):
    if not a or not b:
        return 0.0
    ta = set(re.findall(r"[A-Za-z]{4,}", a.lower())) - {"united", "states", "county"}
    tb = set(re.findall(r"[A-Za-z]{4,}", b.lower())) - {"united", "states", "county"}
    return len(ta & tb) / max(1, len(ta | tb))


def disposition(text):
    disp = "reverse" if REVERSE.search(text) else ("affirm" if AFFIRM.search(text) else "unclear")
    gates = [g for g, pat in GROUND_GATES.items() if pat.search(text)]
    return disp, gates


def demo(opinion_id, tok):
    print(f"== Stage-3 linkage demo for opinion {opinion_id} (mechanics only; NO labels/S) ==")
    subj_name, subj_date, _ = opinion_ctx(opinion_id, tok)
    print(f"  subject: {subj_name!r}  filed {subj_date}")
    citers = cited_by(opinion_id, tok, limit=4)
    print(f"  cited-by: {len(citers)} citing opinions retrieved")
    if not citers:
        print("  (no citing opinions -> no reviewer candidate; expected for minor/recent cases)")
        return
    best = None
    for cid, depth in citers:
        try:
            name, date, text = opinion_ctx(cid, tok)
        except Exception as e:                       # rate-limit / fetch error: degrade, don't crash
            print(f"    citing {cid}: [skipped: {type(e).__name__}]")
            time.sleep(2.0)
            continue
        ov = name_overlap(subj_name, name)
        later = (date or "") > (subj_date or "")
        disp, gates = disposition(text)
        cand = later and ov >= 0.25          # heuristic: later + shares party names
        flag = "  <-- candidate reviewer" if cand else ""
        print(f"    citing {cid}: {str(name)[:38]!r} {date}  name_overlap={ov:.2f} later={later} "
              f"disp={disp} gates={gates}{flag}")
        if cand and best is None:
            best = (cid, name, disp, gates)
        time.sleep(1.0)                               # gentle pacing under the rate limit
    print("  --")
    if best:
        print(f"  best candidate reviewer: {best[0]} {best[1]!r} -> disposition={best[2]}, gate(s)={best[3]}")
    else:
        print("  no citing opinion passed the later+name-overlap heuristic "
              "(this is the review-vs-citation disambiguation problem, unsolved by plumbing).")
    print("  HONEST: retrieval + disposition-regex ingredients work; reliable review-vs-citation "
          "linkage needs docket/subsequent-history lineage + KeyCite validation (real Stage 3).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", type=int, required=True, help="opinion id to exercise linkage on")
    a = ap.parse_args()
    demo(a.demo, clf.token())


if __name__ == "__main__":
    main()
