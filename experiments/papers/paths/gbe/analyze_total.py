"""Development: does the last outcome still matter once the running total is held fixed.

    python analyze_total.py dev.pkl out.json

Pass 3 found that a player gambles about one point in a hundred less after
winning a gamble than after losing one. Winning also leaves the player with
more points. This file asks whether the last outcome says anything beyond
what the total says.

Rows are the trials whose reference trial was a taken gamble, as in
analyze_within_play.py. For each row: g is 1 if the player gambled now, w is 1
if the reference gamble was won, total is the points held in this play before
the present choice, ev_gap is the mean of the present gamble minus the present
safe value, and two flags give the kind of the present trial. Every column has
its mean within the play removed, so only contrasts inside one play are used.
Least squares of g on

    A   w
    B   w, total
    C   w, total, ev_gap, mixed, loss
    D   the same and the position of the trial in the play
    E   D without total

The total before the present choice equals the total before the reference
trial plus what the reference trial paid. So w and total are separated only by
the size of the reference gamble and by what happened earlier in the play. If
the last outcome acted only through the total, the coefficient on w would go
to zero in B and C.

The coefficient on total is given per one standard deviation of the total
within a play. The same three fits are run with the next trial as reference
(lead 1), where the coefficient on w must be zero. Intervals are from 2,000
resamples of participants.
"""
import json
import pickle
import sys
from collections import defaultdict

import numpy as np

from analyze_last import SEED, plays

COLS = ["w", "total", "ev_gap", "mixed", "loss", "trial"]
SPECS = {"A": [0], "B": [0, 1], "C": [0, 1, 2, 3, 4], "D": [0, 1, 2, 3, 4, 5], "E": [0, 2, 3, 4, 5]}


def main(src, out):
    recs = pickle.load(open(src, "rb"))["subjData"]
    rng = np.random.default_rng(SEED)
    k = len(COLS)
    acc = {name: defaultdict(lambda: [np.zeros((k, k)), np.zeros(k), 0]) for name in ("lag1", "lead1")}
    for rec in recs:
        pid = int(rec["id"])
        for p in plays(rec):
            safe, win, lose = p[:, 2], p[:, 3], p[:, 4]
            gam = p[:, 6] == 1
            won = gam & (p[:, 7] == win)
            got = np.where(gam, p[:, 7], safe)
            total = np.concatenate(([0.0], np.cumsum(got)[:-1]))
            n = len(p)
            Z = np.c_[np.zeros(n), total, (win + lose) / 2 - safe, safe == 0, safe < 0, np.arange(n)].astype(float)
            for name, step in (("lag1", -1), ("lead1", 1)):
                t = np.arange(n)
                r = t + step
                ok = (r >= 0) & (r < n)
                t, r = t[ok], r[ok]
                keep = gam[r]
                t, r = t[keep], r[keep]
                if len(t) < 2:
                    continue
                z = Z[t].copy()
                z[:, 0] = won[r]
                z -= z.mean(0)
                y = gam[t].astype(float)
                y -= y.mean()
                a = acc[name][pid]
                a[0] += z.T @ z
                a[1] += z.T @ y
                a[2] += len(t)
    res = {}
    for name, d in acc.items():
        ZZ = np.array([v[0] for v in d.values()])
        Zy = np.array([v[1] for v in d.values()])
        rows = sum(v[2] for v in d.values())
        sd_total = float(np.sqrt(ZZ[:, 1, 1].sum() / rows))
        scale = np.array([1.0, sd_total, 1.0, 1.0, 1.0, 1.0])
        draws = [np.arange(len(ZZ))] + [rng.integers(0, len(ZZ), len(ZZ)) for _ in range(2000)]
        sums = [(ZZ[i].sum(0), Zy[i].sum(0)) for i in draws]
        res[name] = {"participants": len(ZZ), "rows": int(rows), "sd_total_within_play": sd_total}
        for spec, idx in SPECS.items():
            fits = np.array([np.linalg.solve(A[np.ix_(idx, idx)], b[idx]) * scale[idx] for A, b in sums])
            res[name][spec] = {COLS[j]: {"coef": float(fits[0, c]),
                                         "ci95": [float(np.percentile(fits[1:, c], 2.5)), float(np.percentile(fits[1:, c], 97.5))]}
                               for c, j in enumerate(idx)}
            print(name, spec, " ".join("%s %+.4f (%+.4f to %+.4f)" % (c, v["coef"], v["ci95"][0], v["ci95"][1])
                                       for c, v in res[name][spec].items()), flush=True)
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
