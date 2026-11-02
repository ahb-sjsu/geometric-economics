#!/usr/bin/env python3
"""Power of a sealed risky-only test: CPT_CUr with rho frozen at 0.725 against Wilcox (rho = 1) on a
fresh corpus. Design in DEVELOPMENT.md, "Power of the risky-only sealed test".

    python power.py CONF_DIR OUT.json

A fresh corpus of N problems is simulated by drawing N problems, with replacement, from one spent
corpus's held-out per-problem errors (results_conf). The test passes when the 95% interval on the
completeness difference is above 0. The interval is the delta-method interval for the ratio
sum(d) / sum(g), d = err(rho=1) - err(rho), g = err(naive) - err(ML); it is checked against the
bootstrap intervals of aggregate_conf.py on the real corpora first.
"""
import json
import os
import sys

import numpy as np

RISKY = ["cpc18", "gp2012", "pachur2017", "pachur2018", "zilker2020", "babula2018"]
RHO, NS, SIMS, SEED = "0.725", [50, 100, 150, 200, 300, 500, 800, 1200], 4000, 20261107


def diff_ci(d, g, axis=-1):
    """Completeness difference and its delta-method 95% interval, along axis."""
    n = d.shape[axis]
    est = d.sum(axis) / g.sum(axis)
    z = (d - np.expand_dims(est, axis) * g) / np.expand_dims(g.mean(axis), axis)
    se = z.std(axis, ddof=1) / np.sqrt(n)
    return est, est - 1.96 * se, est + 1.96 * se


def main(conf_dir, out):
    rng = np.random.default_rng(SEED)
    summ = json.load(open(os.path.join(conf_dir, "conf_summary.json")))["A"]["per_corpus"]
    res = {"rho": RHO, "sims": SIMS, "check": {}, "power": {}}
    data = {}
    for c in RISKY:
        e = {k: np.array(v) for k, v in json.load(open(os.path.join(conf_dir, f"confidence_{c}.json")))["err"].items()}
        d, g = e["1.0"] - e[RHO], e["naive"] - e["ML"]
        data[c] = (d, g)
        est, lo, hi = diff_ci(d, g)
        res["check"][c] = {"problems": len(d), "delta": [round(float(x), 4) for x in (est, lo, hi)],
                           "bootstrap_at_own_frozen_rho": [round(summ[c]["diff"], 4)] +
                                                          [round(x, 4) for x in summ[c]["diff_ci95"]],
                           "own_frozen_rho": summ[c]["rho_frozen"]}
    for N in NS:
        row = {}
        for c, (d, g) in data.items():
            idx = rng.integers(0, len(d), (SIMS, N))
            _, lo, _ = diff_ci(d[idx], g[idx], axis=1)
            row[c] = float((lo > 0).mean())
        row["mean_over_corpora"] = float(np.mean([row[c] for c in RISKY]))
        res["power"][str(N)] = row
    # several fresh corpora pooled as in part A: k corpora drawn from the six, each at its own size;
    # pooled difference = mean of the k differences, interval from their delta-method SEs
    res["pooled"] = {}
    for k in [1, 2, 3, 4, 6, 8]:
        pick = rng.integers(0, len(RISKY), (SIMS, k))
        est, var = np.zeros((SIMS, k)), np.zeros((SIMS, k))
        for j, c in enumerate(RISKY):
            d, g = data[c]
            m = pick == j
            if not m.any():
                continue
            idx = rng.integers(0, len(d), (int(m.sum()), len(d)))
            e_, lo_, _ = diff_ci(d[idx], g[idx], axis=1)
            est[m], var[m] = e_, ((e_ - lo_) / 1.96) ** 2
        pe, pse = est.mean(1), np.sqrt(var.sum(1)) / k
        res["pooled"][str(k)] = {"power": float((pe - 1.96 * pse > 0).mean()),
                                 "median_halfwidth": float(np.median(1.96 * pse))}
    json.dump(res, open(out, "w"), indent=1)
    print("pooled: k fresh corpora like randomly drawn spent ones, each at its own size")
    for k, v in res["pooled"].items():
        print(f"  k={k}: power {v['power']:.2f}, median 95% half-width {v['median_halfwidth']:.4f}")
    print("check: delta-method vs bootstrap (point, lo, hi)")
    for c, v in res["check"].items():
        print(f"  {c:<11} n={v['problems']:<4} delta {v['delta']}  bootstrap {v['bootstrap_at_own_frozen_rho']}"
              f" (rho {v['own_frozen_rho']})")
    print("power: P(95% interval above 0) for a fresh corpus of N problems like each spent corpus")
    print("N     " + " ".join(f"{c[:10]:>10}" for c in RISKY) + "       mean")
    for N, row in res["power"].items():
        print(f"{N:<5} " + " ".join(f"{row[c]:10.2f}" for c in RISKY) + f" {row['mean_over_corpora']:10.2f}")


if __name__ == "__main__":
    main(*sys.argv[1:])
