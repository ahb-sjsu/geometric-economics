#!/usr/bin/env python3
"""DEVELOPMENT on Molter et al. 2022, round 2. Same data and coordinates as explore_molter.py.

Round 1 found range-scaled attributes beat additive value but overshoot the attraction effect.
Round 2 asks how much scaling the data want, by what statistic of the menu, and against the standard
context model of neuroeconomics:

    ADD        additive, context-free (round 1)
    RNG        gaps divided by the menu range on each attribute (round 1 ADD-rng)
    RNGrho     gaps divided by range^rho, rho in (0, 1.5) free: rho = 0 is ADD, rho = 1 is RNG
    SD         gaps divided by the menu's standard deviation on each attribute
    L2rho      Euclidean cost on range^rho-scaled gaps
    DN         divisive normalisation (Louie, Khaw and Glimcher 2013): V_i = W(p_i) (m_i/20)^alpha,
               u_i = V_i / (sigma + sum_j V_j), choice softmax(beta u)

Two protocols:
    pooled     one parameter set; 5-fold CV over participants (round 1's protocol)
    personal   one parameter set per participant; 5-fold CV over each participant's trials

    python explore_molter2.py TRIALS.csv OUT.json
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
MODELS = ["ADD", "RNG", "RNGrho", "SD", "L2rho", "DN"]
X0 = {"ADD": [], "RNG": [], "RNGrho": [0.0], "SD": [], "L2rho": [0.0], "DN": [0.0]}


def rho(t):
    return 1.5 / (1 + np.exp(-t))


def costs(model, th, P, M):
    xp, xm = E.coords(th, P, M)
    ap, am = np.exp(th[3]), np.exp(th[4])
    if model == "DN":
        V = xp * xm
        u = V / (np.exp(th[5]) + V.sum(1, keepdims=True))
        return -ap * u                                  # a_p plays beta; a_m unused
    gp = xp.max(1, keepdims=True) - xp
    gm = xm.max(1, keepdims=True) - xm
    if model in ("RNG", "RNGrho", "L2rho"):
        r = 1.0 if model == "RNG" else rho(th[5])
        gp = gp / (np.ptp(xp, 1, keepdims=True) + 1e-6) ** r
        gm = gm / (np.ptp(xm, 1, keepdims=True) + 1e-6) ** r
    elif model == "SD":
        gp = gp / (xp.std(1, keepdims=True) + 1e-6)
        gm = gm / (xm.std(1, keepdims=True) + 1e-6)
    gp, gm = ap * gp, am * gm
    if model == "L2rho":
        return np.sqrt(gp ** 2 + gm ** 2 + 1e-12)
    return gp + gm


def probs(model, th, P, M):
    z = -costs(model, th, P, M)
    z -= z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


def nll(model, th, P, M, y):
    p = probs(model, th, P, M)[np.arange(len(y)), y]
    return float(-np.log(np.clip(p, 1e-12, 1)).mean())


def fit(model, P, M, y, rng, x0=None):
    base = [np.log(0.7), 0.0, np.log(0.9), np.log(8.0), np.log(8.0)]
    if model == "DN":
        base = [np.log(0.7), 0.0, np.log(0.9), np.log(5.0), 0.0]
    x0 = np.array(base + X0[model]) if x0 is None else x0
    best = None
    for i in range(STARTS):
        s = x0 if i == 0 else x0 + rng.normal(0, 0.5, len(x0))
        r = minimize(lambda th: nll(model, th, P, M, y), s, method="L-BFGS-B")
        if best is None or r.fun < best.fun:
            best = r
    return best.x


def run(protocol, t, P, M, y, rng):
    subj = t["subject"].to_numpy()
    out = {}
    if protocol == "pooled":
        us = rng.permutation(np.unique(subj))
        fold_of = {s: i % FOLDS for i, s in enumerate(us)}
        f = np.array([fold_of[s] for s in subj])
        groups = [(None, f)]
    else:
        f = np.zeros(len(y), int)
        for s in np.unique(subj):
            idx = np.where(subj == s)[0]
            f[idx] = rng.permutation(len(idx)) % FOLDS
        groups = [(s, f) for s in np.unique(subj)]
    for model in MODELS:
        pr = np.zeros((len(y), 3))
        extra = []
        for s, ff in groups:
            sel = np.ones(len(y), bool) if s is None else subj == s
            for k in range(FOLDS):
                tr, te = sel & (ff != k), sel & (ff == k)
                th = fit(model, P[tr], M[tr], y[tr], rng)
                pr[te] = probs(model, th, P[te], M[te])
                if model in ("RNGrho", "L2rho"):
                    extra.append(float(rho(th[5])))
        cv = -np.log(np.clip(pr[np.arange(len(y)), y], 1e-12, 1))
        out[model] = {"cv_nll": float(cv.mean()), "_cv": cv,
                      "rst": {e: E.rst(t, pr, e) for e in ("attraction", "compromise")},
                      "P_C": float(pr[:, 2].mean())}
        if extra:
            out[model]["rho_median"] = float(np.median(extra))
            out[model]["rho_quartiles"] = [float(np.percentile(extra, 25)), float(np.percentile(extra, 75))]
        print(protocol, model, json.dumps({k: v for k, v in out[model].items() if k != "_cv"}), flush=True)
    per = {model: out[model].pop("_cv") for model in MODELS}
    for model in MODELS:
        d = pd.Series(per[model] - per["ADD"]).groupby(subj).mean().to_numpy()
        bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(2000)]
        out[model]["minus_ADD"] = {"mean": float(d.mean()), "ci_low": float(np.percentile(bs, 2.5)),
                                   "ci_high": float(np.percentile(bs, 97.5))}
    for a, b in [("RNGrho", "DN"), ("RNG", "DN"), ("L2rho", "RNGrho")]:
        d = pd.Series(per[a] - per[b]).groupby(subj).mean().to_numpy()
        bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(2000)]
        out[f"{a} minus {b}"] = {"mean": float(d.mean()), "ci_low": float(np.percentile(bs, 2.5)),
                                 "ci_high": float(np.percentile(bs, 97.5))}
    return out


def main(path, out):
    t, P, M, y = E.load(path)
    rng = np.random.default_rng(E.SEED + 1)
    res = {"note": "development on Molter et al. 2022, round 2",
           "observed_rst": {e: E.observed_rst(t, e) for e in ("attraction", "compromise")},
           "observed_P_C": float(np.mean(y == 2))}
    for protocol in ("pooled", "personal"):
        res[protocol] = run(protocol, t, P, M, y, rng)
        json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({p: {m: (round(v["cv_nll"], 4), v["minus_ADD"]["mean"], v["rst"]) for m, v in res[p].items()
                          if isinstance(v, dict) and "cv_nll" in v} for p in ("pooled", "personal")}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
