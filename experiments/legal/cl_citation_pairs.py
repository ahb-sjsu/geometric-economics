#!/usr/bin/env python3
"""Extract SPECTER-style citation training pairs for LeBSE v2 from the CourtListener replica (Atlas).

Positive pair = (citing opinion body snippet, cited opinion body snippet). A citing opinion and the
opinion it cites share legal topic, so this is real relatedness supervision (unlike v1 SimCSE dropout).
MultipleNegativesRankingLoss then uses the rest of the batch as negatives.

Clean OPINION-LEVEL split (no leakage): eval = id %% 10 == EVAL_MOD (~10%), train = the rest. BOTH
endpoints of a pair must be in the same split, so a training pair never touches an eval opinion.

Body snippet SKIPS the caption (substr from CAPTION_SKIP) so we embed legal substance, not the
standardized "UNITED STATES COURT OF APPEALS ..." header that made v1's eval sit near chance.

Two-phase (fast): pull edge id pairs (int-only), dedup opinion ids, batch-fetch snippets (partial
TOAST detoast via substr, parallel workers), emit JSONL {"a": citing_snip, "b": cited_snip}.

  python3 cl_citation_pairs.py --split train --pairs 200000 --out /archive/courtlistener/pairs_train.jsonl
"""
import argparse
import json
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EVAL_MOD = 7
FLOOR = 10_000_000   # id>10M opinions are ~90-97% populated plain_text (electronic era); older ids
                     # are mostly empty (text lives in html_with_citations). Sample here for real body.
CAPTION_SKIP = 800
BODY = 2600
MIN_SNIP = 400
SEP = "\x01"
SET = ("SET jit=off; SET max_parallel_workers_per_gather=8; "
       "SET effective_cache_size='200GB'; SET work_mem='512MB'; ")


def psql(sql, timeout=2400):
    # SQL via stdin (-f -), NOT -c: a big `id = ANY('{...}')` array literal blows past Linux's
    # 128KB per-argument limit (MAX_ARG_STRLEN). stdin has no such cap.
    r = subprocess.run(
        ["sudo", "-u", "postgres", "psql", "-d", "courtlistener", "-v", "ON_ERROR_STOP=1",
         "-tAF", SEP, "-f", "-"],
        input=SET + sql, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:800])
    return [ln for ln in r.stdout.split("\n") if SEP in ln]  # SET echoes have no SEP -> dropped


def snippet_expr(col):
    return r"regexp_replace(substr(%s, %d, %d), '\s+', ' ', 'g')" % (col, CAPTION_SKIP, BODY)


def edge_ids(split, limit):
    op = "=" if split == "eval" else "<>"
    sql = (f"SELECT citing_opinion_id, cited_opinion_id FROM search_opinionscited "
           f"WHERE citing_opinion_id > {FLOOR} AND cited_opinion_id > {FLOOR} "
           f"AND citing_opinion_id % 10 {op} {EVAL_MOD} AND cited_opinion_id % 10 {op} {EVAL_MOD} "
           f"LIMIT {limit};")
    edges = []
    for ln in psql(sql):
        p = ln.split(SEP)
        if len(p) == 2:
            edges.append((int(p[0]), int(p[1])))
    return edges


def fetch_snippets(ids, chunk=20000):
    out = {}
    ids = sorted(set(ids))
    for i in range(0, len(ids), chunk):
        arr = "{" + ",".join(str(x) for x in ids[i:i + chunk]) + "}"
        sql = f"SELECT id, {snippet_expr('plain_text')} FROM search_opinion WHERE id = ANY('{arr}'::int[]);"
        for ln in psql(sql):
            k, _, v = ln.partition(SEP)
            if len(v) >= MIN_SNIP:
                out[int(k)] = v
        print(f"   fetched snippets {min(i + chunk, len(ids))}/{len(ids)} (kept {len(out)})", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["train", "eval"], default="train")
    ap.add_argument("--pairs", type=int, default=200000, help="edge candidates (before snippet filter)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    print(f"[pairs] split={a.split} pulling up to {a.pairs} citation edges ...", flush=True)
    edges = edge_ids(a.split, a.pairs)
    print(f"[pairs] {len(edges)} edges; fetching unique opinion snippets ...", flush=True)
    snips = fetch_snippets({x for e in edges for x in e})
    n = 0
    with open(a.out, "w", encoding="utf-8") as f:
        for a_id, b_id in edges:
            sa, sb = snips.get(a_id), snips.get(b_id)
            if sa and sb:
                f.write(json.dumps({"a": sa, "b": sb}) + "\n")
                n += 1
    print(f"[pairs] wrote {n} pairs -> {a.out}", flush=True)


if __name__ == "__main__":
    main()
