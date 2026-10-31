#!/usr/bin/env python3
"""DEVELOPMENT on Molter et al. 2022, round 3: physics-style tests of the menu scale exponent.

Round 2 (personal fits) found gaps scaled by range^rho with rho ~ 0.55 per person: partial scale
invariance. Two techniques from mathematical physics make sharp claims about such an exponent:

  Universality. A broken scale symmetry is described by an exponent that does not depend on details.
      RHO2   separate exponents for probability and amount (rho_p, rho_m). Universality: rho_p = rho_m.
  Crossover. Between a noise-limited fixed point (square-root law, as DeVries-Rose in vision) and the
      scale-invariant one (Weber, rho = 1), with one crossover scale R0:
      CROSS  gap / sqrt(R (R0 + R)), both exponents fixed (1/2 below R0, 1 above), one R0 per attribute,
             so it has as many free parameters as RHO2.
  Baselines from round 2: ADD (no scaling) and RNGrho (one free exponent).

Protocol: one parameter set per participant, 5-fold CV over each participant's trials (round 2's
"personal" protocol). Per-participant parameters are reported so rho_p against rho_m can be compared.

    python explore_molter3.py TRIALS.csv OUT.json
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explore_molter as E  # noqa: E402

FOLDS = 5
STARTS = 3
MODELS = ["ADD", "RNGrho", "RHO2", "CROSS"]
EXTRA = {"ADD": [], "RNGrho": [0.0], "RHO2": [0.0, 0.0], "CROSS": [np.log(0.1), np.log(0.1)]}


def rho(t):
    return 1.5 / (1 + np.exp(-t))


def costs(model, th, P, M):
    xp, xm = E.coords(th, P, M)
    ap, am = np.exp(th[3]), np.exp(th[4])
    gp = xp.max(1, keepdims=True) - xp
    gm = xm.max(1, keepdims=True) - xm
    Rp = np.ptp(xp, 1, keepdims=True) + 1e-6
    Rm = np.ptp(xm, 1, keepdims=True) + 1e-6
    if model == "RNGrho":
        gp, gm = gp / Rp ** rho(th[5]), gm / Rm ** rho(th[5])
    elif model == "RHO2":
        gp, gm = gp / Rp ** rho(th[5]), gm / Rm ** rho(th[6])
    elif model == "CROSS":
        # one crossover scale per attribute, in that attribute's coordinate units
        R0p, R0m = np.exp(th[5]), np.exp(th[6])
        gp, gm = gp / np.sqrt(Rp * (R0p + Rp)), gm / np.sqrt(Rm * (R0m + Rm))
    return ap * gp + am * gm


def probs(model, th, P, M):
    z = -costs(model, th, P, M)
    z -= z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


def nll(model, th, P, M, y):
    p = probs(model, th, P, M)[np.arange(len(y)), y]
    return float(-np.log(np.clip(p, 1e-12, 1)).mean())


def fit(model, P, M, y, rng):
    x0 = np.array([np.log(0.7), 0.0, np.log(0.9), np.log(8.0), np.log(8.0)] + EXTRA[model])
    best = None
    for i in range(STARTS):
        s = x0 if i == 0 else x0 + rng.normal(0, 0.5, len(x0))
        r = minimize(lambda th: nll(model, th, P, M, y), s, method="L-BFGS-B")
        if best is None or r.fun < best.fun:
            best = r
    return best.x


def main(path, out):
    t, P, M, y = E.load(path)
    rng = np.random.default_rng(E.SEED + 2)
    subj = t["subject"].to_numpy()
    f = np.zeros(len(y), int)
    for s in np.unique(subj):
        idx = np.where(subj == s)[0]
        f[idx] = rng.permutation(len(idx)) % FOLDS
    res = {"note": "development on Molter et al. 2022, round 3 (personal fits)",
           "observed_rst": {e: E.observed_rst(t, e) for e in ("attraction", "compromise")}, "models": {}}
    per = {}
    for model in MODELS:
        pr = np.zeros((len(y), 3))
        params = {}
        for s in np.unique(subj):
            sel = subj == s
            for k in range(FOLDS):
                tr, te = sel & (f != k), sel & (f == k)
                th = fit(model, P[tr], M[tr], y[tr], rng)
                pr[te] = probs(model, th, P[te], M[te])
            th_all = fit(model, P[sel], M[sel], y[sel], rng)
            if model in ("RNGrho", "RHO2"):
                params[str(s)] = [float(rho(x)) for x in th_all[5:]]
            elif model == "CROSS":
                params[str(s)] = [float(np.exp(x)) for x in th_all[5:7]]
        cv = -np.log(np.clip(pr[np.arange(len(y)), y], 1e-12, 1))
        per[model] = cv
        res["models"][model] = {"cv_nll": float(cv.mean()),
                                "rst": {e: E.rst(t, pr, e) for e in ("attraction", "compromise")},
                                "P_C": float(pr[:, 2].mean()), "per_participant": params}
        print(model, json.dumps({k: v for k, v in res["models"][model].items() if k != "per_participant"}), flush=True)
    for a, b in [("RNGrho", "ADD"), ("RHO2", "RNGrho"), ("CROSS", "RNGrho"), ("CROSS", "RHO2"), ("CROSS", "ADD")]:
        d = pd.Series(per[a] - per[b]).groupby(subj).mean().to_numpy()
        bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(2000)]
        res[f"{a} minus {b}"] = {"mean": float(d.mean()), "ci_low": float(np.percentile(bs, 2.5)),
                                 "ci_high": float(np.percentile(bs, 97.5))}
    r2 = np.array(list(res["models"]["RHO2"]["per_participant"].values()))
    diff = r2[:, 0] - r2[:, 1]
    bs = [diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(2000)]
    res["universality_rho_p_minus_rho_m"] = {
        "median_rho_p": float(np.median(r2[:, 0])), "median_rho_m": float(np.median(r2[:, 1])),
        "mean_diff": float(diff.mean()), "ci_low": float(np.percentile(bs, 2.5)), "ci_high": float(np.percentile(bs, 97.5)),
        "spearman_across_people": float(pd.Series(r2[:, 0]).corr(pd.Series(r2[:, 1]), method="spearman"))}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k not in ("models",)}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
