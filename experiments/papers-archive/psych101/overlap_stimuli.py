#!/usr/bin/env python3
"""Do the candidate Psych-101 problems repeat CPC18 problems? Stimuli only.

Reads only the lines that describe options. Choice tokens are never parsed. Each
problem is keyed by the unordered pair of its options' expected values and minimum
outcomes, rounded to 0.01. CPC18 keys use EV = pH*H + (1-pH)*L (exact, H is the
mean of the high part) and the minimum is L or, if lower, the sub-lottery floor is
ignored, so the CPC18 minimum is approximate for multi-outcome shapes and the
match count is a lower bound for those.
"""
import re
import sys
import collections

import pandas as pd
from datasets import load_dataset

OPT_PL = re.compile(r"Option ([A-Z]) delivers (.*?)\.\s*$")
OUT = re.compile(r"(-?[\d.]+) points with ([\d.]+)% chance")
LOT_W = re.compile(r"Lottery ([A-Z]) offers (.*?)\.\s*$")
OUT_W = re.compile(r"(-?[\d.]+) points with ([\d.]+)% probability")


def opt_key(pairs):
    ev = sum(x * p for x, p in pairs)
    return (round(ev, 2), round(min(x for x, _ in pairs), 2))


def problems(text, opt_re, out_re):
    cur, out = {}, []
    for ln in text.split("\n"):
        m = opt_re.search(ln.strip())
        if m:
            pairs = [(float(x), float(p) / 100) for x, p in out_re.findall(m.group(2))]
            cur[m.group(1)] = pairs
            if len(cur) == 2:
                if not all(cur.values()):        # unknown probabilities: not keyed
                    out.append("unparsed")
                    cur = {}
                    continue
                a, b = cur.values()
                out.append(tuple(sorted([opt_key(a), opt_key(b)])))
                cur = {}
    return out


def cpc18_keys(path):
    df = pd.read_csv(path, usecols=["GameID", "Ha", "pHa", "La", "Hb", "pHb", "Lb", "Amb"])
    g = df.groupby("GameID").first()
    keys = {}
    for gid, r in g.iterrows():
        ka = (round(r.pHa * r.Ha + (1 - r.pHa) * r.La, 2), round(min(r.Ha, r.La) if r.pHa < 1 else r.Ha, 2))
        kb = (round(r.pHb * r.Hb + (1 - r.pHb) * r.Lb, 2), round(min(r.Hb, r.Lb) if r.pHb < 1 else r.Hb, 2))
        keys[tuple(sorted([ka, kb]))] = gid
    return keys


def main():
    ck = cpc18_keys(sys.argv[1])
    ds = load_dataset("marcelbinz/Psych-101", split="train")
    for exp, opt_re, out_re in [("plonsky2018when/exp1.csv", OPT_PL, OUT),
                                ("wulff2018description/exp1.csv", LOT_W, OUT_W)]:
        rows = ds.filter(lambda r: r["experiment"] == exp)
        probs = collections.Counter()
        for r in rows:
            probs.update(set(problems(r["text"], opt_re, out_re)))
        unparsed = probs.pop("unparsed", 0)
        hit = [p for p in probs if p in ck]
        print("  participants with an option lacking stated probabilities:", unparsed)
        print(exp, "participants", len(rows), "distinct problems", len(probs),
              "matching a CPC18 problem", len(hit))
        print("  example problems:", list(probs)[:3])


if __name__ == "__main__":
    main()
