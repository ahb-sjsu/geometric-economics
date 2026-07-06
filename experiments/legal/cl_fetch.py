#!/usr/bin/env python3
"""Stage 2 (corpus) of the legal-reversal study: fetch opinions from CourtListener.

Corpus acquisition ONLY -- pulls opinion text + citation edges + metadata for a fixed court/window.
It does NOT construct reversal labels and does NOT compute the pathology score S: those are Stages 3-5
and must follow the freeze (see RUNBOOK_legal_reversal.md, FREEZE_PROTOCOL.md). Running this fetcher is
engineering plumbing, not the confirmatory data pull.

Token: read from experiments/legal/.cl_token (gitignored) or env CL_TOKEN. Never hard-code it.
Output: one JSON per case under experiments/legal/raw/ (gitignored; CourtListener terms).

    python cl_fetch.py --court ca9 --after 2005-01-01 --before 2015-12-31 --limit 3   # plumbing test
"""
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
API = "https://www.courtlistener.com/api/rest/v4"


def token():
    t = os.environ.get("CL_TOKEN")
    if not t:
        p = os.path.join(HERE, ".cl_token")
        if os.path.exists(p):
            t = open(p).read().strip()
    if not t:
        raise SystemExit("No CourtListener token: set CL_TOKEN or write experiments/legal/.cl_token")
    return t


def get(url, tok, params=None):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        req = urllib.request.Request(url, headers={"Authorization": f"Token {tok}"})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:              # rate limited: back off (honor Retry-After if present)
                wait = int(e.headers.get("Retry-After", 0) or 0) or (2 ** attempt)
                time.sleep(min(wait, 30))
                continue
            raise
    raise RuntimeError("repeated rate-limit / failure on " + url)   # catchable by callers


def opinion_text(op):
    for k in ("plain_text", "html_with_citations", "html", "html_lawbox", "xml_harvard"):
        if op.get(k):
            return k, op[k]
    return None, ""


def fetch(court, after, before, limit, tok):
    """Discovery via the fast search API (court/date filters), then fetch text by opinion id."""
    os.makedirs(RAW, exist_ok=True)
    hits = get(f"{API}/search/", tok, {
        "type": "o", "court": court, "filed_after": after, "filed_before": before,
        "order_by": "dateFiled asc", "page_size": min(limit, 20),
    })
    rows = []
    for res in hits.get("results", [])[:limit]:
        ops = res.get("opinions") or []
        op_id = (ops[0].get("id") if ops and isinstance(ops[0], dict) else None)
        text_field, text, cites_out = None, "", 0
        if op_id:
            op = get(f"{API}/opinions/{op_id}/", tok)
            text_field, text = opinion_text(op)
            cites_out = len(op.get("opinions_cited") or [])
        rec = {
            "cluster_id": res.get("cluster_id"),
            "opinion_id": op_id,
            "court": court,
            "case_name": res.get("caseName"),
            "date_filed": res.get("dateFiled"),
            "docket_number": res.get("docketNumber"),
            "status": res.get("status"),
            "citation": res.get("citation"),
            "cite_count": res.get("citeCount"),
            "text_field": text_field,
            "text_len": len(text or ""),
            "cites_out": cites_out,
        }
        with open(os.path.join(RAW, f"{rec['cluster_id']}.json"), "w", encoding="utf-8") as f:
            json.dump({**rec, "text": text}, f)
        rows.append(rec)
        time.sleep(0.3)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--court", default="ca9")
    ap.add_argument("--after", default="2005-01-01")
    ap.add_argument("--before", default="2015-12-31")
    ap.add_argument("--limit", type=int, default=3)
    a = ap.parse_args()
    rows = fetch(a.court, a.after, a.before, a.limit, token())

    print(f"== cl_fetch plumbing: {len(rows)} {a.court} opinions [{a.after}..{a.before}] ==")
    for r in rows:
        print(f"  cluster {r['cluster_id']}  {r['date_filed']}  text={r['text_len']:>7} chars "
              f"({r['text_field']})  cites_out={r['cites_out']}  cites_in={r['cite_count']}  "
              f"{str(r['case_name'])[:40]!r}")
    ok = sum(r["text_len"] > 500 for r in rows)
    cg = sum(r["cites_out"] > 0 for r in rows)
    print(f"-- coverage: full-text {ok}/{len(rows)}, citation-graph {cg}/{len(rows)}. "
          f"NO labels/S computed (Stages 3-5 are post-freeze).")


if __name__ == "__main__":
    main()
