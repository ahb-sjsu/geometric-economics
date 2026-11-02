#!/usr/bin/env python3
"""MF2, the model-free background check, with and without matched lotteries (REHEARSAL.md, version 3).

    python mf2_check.py OUT.json [STUDIES]

MF2 needs only simulated choices, no model fits, so this re-runs it on fresh simulated studies from
every truth in rehearsal.py (default 200 studies per truth, 200 people each) and reports how often its
interval excludes zero at n = 60, 120 and 200: with only the lotteries offered at every level
(matched, the corrected check) and with every lottery at the ideal (unmatched, as version 3 ran it).
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rehearsal as R  # noqa: E402


def mf2_pass(bg):
    est, lo, hi = R.ci(bg)
    return bool(lo > 0 or hi < 0), est


def main(out, studies=200):
    res = {}
    for ti, truth in enumerate(R.TRUTHS):
        rows = {n: {"matched": [], "unmatched": []} for n in R.NS}
        for s in range(studies):
            rng = np.random.default_rng([20261104, ti, s])
            people = [R.simulate(truth, rng) for _ in range(max(R.NS))]
            for kind, matched in (("matched", True), ("unmatched", False)):
                bg = [0.5 * (R.lottery_rates(p["y"], "self", 0, matched) + R.lottery_rates(p["y"], "charity", 0, matched))
                      for p in people]
                for n in R.NS:
                    rows[n][kind].append(mf2_pass(bg[:n]))
        res[truth] = {f"n{n}": {k: {"pass": float(np.mean([x[0] for x in v])), "est": float(np.median([x[1] for x in v]))}
                                for k, v in rows[n].items()} for n in R.NS}
        print(truth, {n: (round(res[truth][f'n{n}']['matched']['pass'], 2), round(res[truth][f'n{n}']['unmatched']['pass'], 2))
                      for n in R.NS}, "(matched, unmatched) pass rates", flush=True)
    json.dump({"studies": studies, "results": res}, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 200)
