#!/usr/bin/env python3
"""Docket-lineage eval pairs = (district opinion body, appellate opinion body) linked by matching
normalized docket numbers (search_originatingcourtinformation), NOT by citations.

This is an INDEPENDENT downstream test for LeBSE-v2: the model trained on the citation graph; docket
lineage is a different, structural relation (same case, district decision + its appeal). The district
opinions are 1990-2015 (id < 10M), below the id>10M training floor, so they were never seen in training.

Uses the pre-built d_norm / c_norm normalized-docket tables. Output JSONL {"a": district, "b": appellate}.
"""
import argparse
import json
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PY_CAPTION_SKIP = 400   # drop the caption/party-name prefix in Python (after HTML strip) so the eval
                        # tests body semantics, not string-matching of shared party names
MIN_SNIP = 400
SEP = "\x01"
SET = ("SET jit=off; SET max_parallel_workers_per_gather=8; "
       "SET effective_cache_size='200GB'; SET work_mem='512MB'; ")


def psql(sql, timeout=2400):
    r = subprocess.run(
        ["sudo", "-u", "postgres", "psql", "-d", "courtlistener", "-v", "ON_ERROR_STOP=1",
         "-tAF", SEP, "-f", "-"],
        input=SET + sql, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:800])
    return [ln for ln in r.stdout.split("\n") if SEP in ln]


def snippet_expr():
    # Recover old-opinion text: fall back to HTML (tags stripped) when plain_text is empty.
    # substr first (partial detoast), strip tags, collapse whitespace.
    src = "coalesce(nullif(plain_text,''), nullif(html_with_citations,''), '')"
    return (r"regexp_replace(regexp_replace(substr(%s, 1, 6000), '<[^>]+>', ' ', 'g'), '\s+', ' ', 'g')"
            % src)


def lineage_pairs(limit):
    # district opinion <-> appellate opinion, same normalized docket, different court.
    sql = ("SELECT d.district_opinion_id, c.circuit_opinion_id "
           "FROM d_norm d JOIN c_norm c ON c.dn = d.dn "
           "WHERE d.dn IS NOT NULL AND c.circuit_court <> d.district_court "
           f"LIMIT {limit};")
    out = []
    for ln in psql(sql):
        p = ln.split(SEP)
        if len(p) == 2:
            out.append((int(p[0]), int(p[1])))
    return out


def fetch_snippets(ids, chunk=20000):
    out = {}
    ids = sorted(set(ids))
    for i in range(0, len(ids), chunk):
        arr = "{" + ",".join(str(x) for x in ids[i:i + chunk]) + "}"
        sql = f"SELECT id, {snippet_expr()} FROM search_opinion WHERE id = ANY('{arr}'::int[]);"
        for ln in psql(sql):
            k, _, v = ln.partition(SEP)
            body = v[PY_CAPTION_SKIP:]          # drop caption/party prefix -> body semantics only
            if len(body) >= MIN_SNIP:
                out[int(k)] = body[:2600]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=50000)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    pairs = lineage_pairs(a.limit)
    print(f"[docket] {len(pairs)} lineage pairs; fetching body snippets ...", flush=True)
    snips = fetch_snippets({x for p in pairs for x in p})
    n = 0
    with open(a.out, "w", encoding="utf-8") as f:
        for d_id, c_id in pairs:
            sd, sc = snips.get(d_id), snips.get(c_id)
            if sd and sc:
                f.write(json.dumps({"a": sd, "b": sc}) + "\n")
                n += 1
    print(f"[docket] wrote {n} pairs (both sides have body text) -> {a.out}", flush=True)


if __name__ == "__main__":
    main()
