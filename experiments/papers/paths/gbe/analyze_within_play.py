"""Development: the effect of the last gamble's outcome, compared within a play.

    python analyze_within_play.py dev.pkl out.json

analyze_last.py compared within a participant, across that participant's
plays. Its lead-1 check came out at -0.0044 and not zero, and diag_check.py
found the share of gambles won rising from 50.2% on a first play to 51.2% on
fourth and later plays. So the chance of winning is not the same across a
person's plays, and a comparison across plays can pick up whatever else changes
with practice.

Here each play is its own block. Within a play, among trials whose reference
trial was a taken gamble, let w be 1 if that gamble was won and g be 1 if the
player gambled on the present trial. The estimate is

    sum over plays of sum (g - mean g)(w - mean w)
    ----------------------------------------------
    sum over plays of sum (w - mean w)^2

with the means taken within the play. It is the difference in the rate of
gambling after a win and after a loss, using only contrasts inside one play.
The interval is from 2,000 resamples of participants.

The same is computed for lag 2 and for lead 1 and lead 2, which must be zero.
Splits of lag 1 by the kind of the present trial and of the reference trial.
"""
import json
import pickle
import sys
from collections import defaultdict

import numpy as np

from analyze_last import KIND, SEED, plays


def main(src, out):
    recs = pickle.load(open(src, "rb"))["subjData"]
    rng = np.random.default_rng(SEED)
    acc = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))     # name -> participant -> [numerator, denominator]
    for rec in recs:
        pid = int(rec["id"])
        for p in plays(rec):
            gam = (p[:, 6] == 1)
            won = gam & (p[:, 7] == p[:, 3])
            kind = [KIND[int(np.sign(x))] for x in p[:, 2]]
            n = len(p)
            cells = defaultdict(lambda: ([], []))
            for t in range(n):
                for name, r in (("lag1", t - 1), ("lag2", t - 2), ("lead1", t + 1), ("lead2", t + 2)):
                    if not 0 <= r < n or not gam[r]:
                        continue
                    keys = [name]
                    if name == "lag1":
                        keys += ["lag1_now_" + kind[t], "lag1_after_" + kind[r]]
                    for k in keys:
                        cells[k][0].append(float(gam[t]))
                        cells[k][1].append(float(won[r]))
            for k, (g, w) in cells.items():
                g, w = np.array(g), np.array(w)
                dw = w - w.mean()
                a = acc[k][pid]
                a[0] += float(((g - g.mean()) * dw).sum())
                a[1] += float((dw * dw).sum())
    res = {}
    for k in sorted(acc):
        v = np.array(list(acc[k].values()))
        est = v[:, 0].sum() / v[:, 1].sum()
        boots = []
        for _ in range(2000):
            b = v[rng.integers(0, len(v), len(v))]
            boots.append(b[:, 0].sum() / b[:, 1].sum())
        res[k] = {"participants": int(len(v)), "difference": float(est),
                  "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}
    json.dump(res, open(out, "w"), indent=1)
    for k, v in res.items():
        print("%-18s %+.4f (%+.4f to %+.4f) participants %d" % (k, v["difference"], v["ci95"][0], v["ci95"][1], v["participants"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
