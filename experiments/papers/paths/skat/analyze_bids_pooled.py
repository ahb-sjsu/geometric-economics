"""Development: the comparisons of analyze_bids.py with cells pooled over all players.

    python analyze_bids_pooled.py dev_rows.tsv.gz out.json

`analyze_bids.py` gives every player one value and averages the values, so a
player with twenty usable decisions counts as much as one with twenty thousand.
For people the intervals came out about 0.045 wide, too wide to see an effect
of the size found in poker (0.010).

Here the cells are the same (unit, number of jacks, aces plus tens in three
bins) and so are the two sides of each comparison. Inside a cell the rate of
bidding on side a minus the rate on side b. Cells are then weighted by
n_a * n_b / (n_a + n_b) and pooled over all units, as in the Great Brain
Experiment matched comparison. The interval is from 2,000 resamples of units,
each unit carrying all of its cells.

The output has the layout of analyze_bids.py so the same summary scripts read
it. Whether this estimator is free of the bias found in pass 2 is not assumed.
It is to be measured on the shuffled games of null_perm.py.
"""
import json
import sys
from collections import Counter, defaultdict

import numpy as np

from analyze_bids import LAGS, PROGRAMS, SEED, decisions, read


def contrast(cells, a, b, rng):
    num = defaultdict(float)
    den = defaultdict(float)
    for (unit, _), c in cells.items():
        x, y = c.get(a), c.get(b)
        if not x or not y:
            continue
        w = x[1] * y[1] / (x[1] + y[1])
        num[unit] += w * (x[0] / x[1] - y[0] / y[1])
        den[unit] += w
    if len(den) < 30:
        return {"units": len(den)}
    units = list(den)
    n = np.array([num[u] for u in units])
    d = np.array([den[u] for u in units])
    boots = []
    for _ in range(2000):
        i = rng.integers(0, len(units), len(units))
        boots.append(n[i].sum() / d[i].sum())
    return {"units": len(units), "difference": float(n.sum() / d.sum()), "effective_pairs": float(d.sum()),
            "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}


def main(rows, out):
    dec = list(decisions(read(rows)))
    n_by = Counter(d[0] for d in dec if d[0] not in PROGRAMS and d[1] == "0")
    busiest = {w for w, _ in n_by.most_common(10)}
    groups = {"people": lambda d: d[0] not in PROGRAMS and d[1] == "0",
              "people_without_ten_busiest": lambda d: d[0] not in PROGRAMS and d[1] == "0" and d[0] not in busiest}
    for p in PROGRAMS:
        groups[p] = lambda d, p=p: d[0] == p
    res = {"decisions": len(dec), "people": len(n_by), "estimator": "cells pooled, weights n_a*n_b/(n_a+n_b)", "groups": {}}
    for name, keep in groups.items():
        rng = np.random.default_rng(SEED)
        last = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        lag = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        n = 0
        for who, suf, series, jacks, high, bid, h in dec:
            if not keep((who, suf)):
                continue
            n += 1
            unit = series if name in PROGRAMS else who
            key = (unit, (jacks, high))
            if h and h[0] in "LWN":
                c = last[key][h[0]]
                c[0] += bid
                c[1] += 1
            if len(h) == LAGS and "O" not in h and sum(x != "N" for x in h) == 1:
                j = [i for i, x in enumerate(h) if x != "N"][0] + 1
                for e in (h[j - 1], "A"):
                    c = lag[key][(e, j)]
                    c[0] += bid
                    c[1] += 1
        g = {"decisions": n,
             "by_last_outcome": {"L_minus_N": contrast(last, "L", "N", rng), "W_minus_N": contrast(last, "W", "N", rng),
                                 "L_minus_W": contrast(last, "L", "W", rng)},
             "by_lag": {}}
        for e, label in (("A", "any"), ("L", "loss"), ("W", "win")):
            for j in range(1, LAGS):
                g["by_lag"]["%s_lag%d_minus_lag%d" % (label, j, j + 1)] = contrast(lag, (e, j), (e, j + 1), rng)
        res["groups"][name] = g
        print(name, json.dumps({s: {k: [round(v.get("difference", 9), 4)] + [round(x, 4) for x in v.get("ci95", [])]
                                    for k, v in g[s].items()} for s in ("by_last_outcome", "by_lag")}), flush=True)
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
