#!/usr/bin/env python3
"""DEVELOPMENT on Molter et al. 2022 (PLoS Comp Biol 18(7): e1010283), the development set for menu
geometry. Chau et al. 2014 / Gluth et al. 2018 are held back for a sealed test and are not read here.

Each trial: three all-or-nothing gambles (p to win m, else 0). A and B are near-indifferent; C is a
decoy, either asymmetrically dominated by the target (attraction) or an extreme that makes the target
the middle option (compromise); filler trials otherwise. 40 participants x 225 trials.

Every model maps an option to attribute coordinates x = (W(p), m^alpha / 20^alpha), W linear in
log-odds (gamma, delta), then a cost; choice probabilities are softmax(-cost / 1) with the scale
absorbed in the attribute weights a_p, a_m. The menu reference r is the attribute-wise best over the
three options.

    ADD      cost = a_p (r_p - x_p) + a_m (r_m - x_m)        additive; the reference cancels: context-free
    L2       cost = sqrt(a_p^2 (r_p - x_p)^2 + a_m^2 (r_m - x_m)^2)   GDT menu geometry
    Lq       Minkowski exponent q free in (0.5, 4.5)
    ADD-rng  ADD with each gap divided by the menu's range on that attribute (range normalisation)
    L2-rng   L2 on range-normalised gaps

Fit pooled over participants; scored by 5-fold cross-validation over participants (log-loss per
trial), and by each model's predicted relative choice share of the target, RST = P(target) /
(P(target) + P(competitor)), against the observed, for attraction and compromise trials.

    python explore_molter.py TRIALS.csv OUT.json
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize

SEED = 20261031
FOLDS = 5
STARTS = 4
MODELS = ["ADD", "L2", "Lq", "ADD-rng", "L2-rng"]


def load(path):
    t = pd.read_csv(path)
    t = t[t["choice"].isin(["A", "B", "C"])].reset_index(drop=True)
    P = t[["pA", "pB", "pC"]].to_numpy(float)
    M = t[["mA", "mB", "mC"]].to_numpy(float)
    y = t["choice"].map({"A": 0, "B": 1, "C": 2}).to_numpy()
    return t, P, M, y


def coords(th, P, M):
    g, d, al = np.exp(th[0]), th[1], np.exp(th[2])
    Pc = np.clip(P, 1e-6, 1 - 1e-6)
    W = 1 / (1 + np.exp(-(g * (np.log(Pc) - np.log1p(-Pc)) + d)))
    return W, (M / 20.0) ** al


def costs(model, th, P, M):
    xp, xm = coords(th, P, M)
    ap, am = np.exp(th[3]), np.exp(th[4])
    gp = xp.max(1, keepdims=True) - xp
    gm = xm.max(1, keepdims=True) - xm
    if model.endswith("-rng"):
        gp = gp / (np.ptp(xp, 1, keepdims=True) + 1e-6)
        gm = gm / (np.ptp(xm, 1, keepdims=True) + 1e-6)
    gp, gm = ap * gp, am * gm
    if model.startswith("ADD"):
        return gp + gm
    if model.startswith("L2"):
        return np.sqrt(gp ** 2 + gm ** 2 + 1e-12)
    q = 0.5 + 4 / (1 + np.exp(-th[5]))
    return (gp ** q + gm ** q + 1e-12) ** (1 / q)


def probs(model, th, P, M):
    z = -costs(model, th, P, M)
    z -= z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


def nll(model, th, P, M, y):
    p = probs(model, th, P, M)[np.arange(len(y)), y]
    return float(-np.log(np.clip(p, 1e-12, 1)).mean())


def fit(model, P, M, y, rng):
    x0 = np.array([np.log(0.7), 0.0, np.log(0.9), np.log(8.0), np.log(8.0)] + ([0.0] if model == "Lq" else []))
    best = None
    for i in range(STARTS):
        s = x0 if i == 0 else x0 + rng.normal(0, 0.5, len(x0))
        r = minimize(lambda th: nll(model, th, P, M, y), s, method="L-BFGS-B")
        if best is None or r.fun < best.fun:
            best = r
    return best.x, float(best.fun)


def rst(t, p, effect):
    """Mean relative share of the target over participants' trials of one effect."""
    sel = (t["effect"] == effect).to_numpy()
    tgt = np.where(t["target"] == "A", 0, 1)
    pt = p[np.arange(len(t)), tgt][sel]
    pc = p[np.arange(len(t)), 1 - tgt][sel]
    return float(np.mean(pt / (pt + pc)))


def observed_rst(t, effect):
    s = t[t["effect"] == effect]
    tg = (s["choice"] == s["target"]).sum()
    co = ((s["choice"] != s["target"]) & (s["choice"] != "C")).sum()
    return float(tg / (tg + co))


def main(path, out):
    t, P, M, y = load(path)
    subj = t["subject"].to_numpy()
    rng = np.random.default_rng(SEED)
    us = rng.permutation(np.unique(subj))
    fold_of = {s: i % FOLDS for i, s in enumerate(us)}
    f = np.array([fold_of[s] for s in subj])
    res = {"note": "development on Molter et al. 2022", "trials": int(len(y)), "participants": int(len(us)),
           "observed_rst": {e: observed_rst(t, e) for e in ("attraction", "compromise")},
           "choice_share": {k: float(np.mean(y == i)) for i, k in enumerate("ABC")}, "models": {}}
    for model in MODELS:
        cv = np.zeros(len(y)); pr = np.zeros((len(y), 3))
        for k in range(FOLDS):
            tr, te = f != k, f == k
            th, _ = fit(model, P[tr], M[tr], y[tr], rng)
            p = probs(model, th, P[te], M[te])
            pr[te] = p
            cv[te] = -np.log(np.clip(p[np.arange(te.sum()), y[te]], 1e-12, 1))
        th_all, l_all = fit(model, P, M, y, rng)
        row = {"cv_nll": float(cv.mean()), "in_sample_nll": l_all, "theta": th_all.tolist(),
               "cv_rst": {e: rst(t, pr, e) for e in ("attraction", "compromise")},
               "cv_choice_share_C": float(pr[:, 2].mean()), "_cv": cv}
        if model == "Lq":
            row["q"] = float(0.5 + 4 / (1 + np.exp(-th_all[5])))
        res["models"][model] = row
        print(model, json.dumps({k: v for k, v in row.items() if k != "_cv"}), flush=True)
    base = res["models"]["ADD"]["_cv"]
    by_s = pd.Series(subj)
    for model in MODELS:
        d = res["models"][model]["_cv"] - base
        per = pd.Series(d).groupby(by_s).mean().to_numpy()            # bootstrap over participants
        bs = [per[rng.integers(0, len(per), len(per))].mean() for _ in range(2000)]
        res["models"][model]["minus_ADD"] = {"mean": float(per.mean()), "ci_low": float(np.percentile(bs, 2.5)),
                                             "ci_high": float(np.percentile(bs, 97.5))}
    for m in MODELS:
        res["models"][m].pop("_cv")
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({m: {"cv": round(v["cv_nll"], 4), "vsADD": v["minus_ADD"], "rst": v["cv_rst"]}
                      for m, v in res["models"].items()}, indent=1))
    print("observed", res["observed_rst"], res["choice_share"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
