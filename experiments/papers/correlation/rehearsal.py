#!/usr/bin/env python3
"""Rehearsal of the correlation-attitude design (DESIGN.md, "Stages", step 1).

    python rehearsal.py TRUTH OUT.json

TRUTH is one of GEO1, GEO2, EARLY, RDU, CAG, ADD. Each simulated study draws people from that model,
runs them through the exact stimulus set (stimuli.py), fits every candidate model per person on the
calibration trials, and scores held-out log-loss on the test trials with no refit. Needs models.py and
stimuli.py beside it. REHEARSAL_QUICK=1 for a smoke test.

Truths (shape drawn per person; scale set so that the median |logit| over block R is ~1.5, a
moderately noisy chooser; a left bias drawn per person):
  GEO1   late contraction, full metric, kappa = 1. Shape: sqrt(P22/P11) ~ U(0.25, 1), the metric's
         correlation P12/sqrt(P11 P22) ~ U(-0.6, 0.6).
  GEO2   the same with kappa = 2 (expected squared distance).
  EARLY  the metric on the mean bundle, kappa ~ U(1, 2).
  RDU    additive value per outcome, eta ~ U(0.8, 1.6), charity weight ~ U(0.25, 1), weight on the
         better outcome ~ U(0.30, 0.48).
  CAG    concave aggregator, rho ~ U(1.5, 3), charity weight ~ U(0.25, 1).
  ADD    linear additive value, no risk attitude.

Tests, on the first n people of each simulated study (n in NS), intervals over people:
  H_vs_EARLY  (H1)  GEO's held-out log-loss below EARLY's: the interval's upper end below -margin.
  H_vs_RDU    (H2)  the same against RDU.
  H_vs_CAG    (H3)  the same against CAG.
  H4                Spearman correlation, across people, between the correlated-option preference GEO
                    predicts from calibration and the one observed in block X; lower end above 0.
  MF1               model-free: the block X choice rate of the correlated option differs from 0.5.
  MF2               model-free: lottery choice rate on one attribute changes when the other attribute
                    leaves its ideal (S test cells against S calibration cells).
Recovery (GEO truths): fitted against true metric correlation, ratio and kappa, and the person-level
predicted correlated-option preference against its true value.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import models as M  # noqa: E402
import stimuli  # noqa: E402

TRUTHS = ["GEO1", "GEO2", "EARLY", "RDU", "CAG", "ADD"]
FIT = ["GEO", "EARLY", "RDU", "CAG"]
NS = [60, 120, 200]
SIMS = 60
MARGINS = [0.0, 0.002, 0.005, 0.01]
SEED = 20261102
if os.environ.get("REHEARSAL_QUICK"):
    NS, SIMS = [30], 2

TRIALS = stimuli.build()
ALL = M.arrays(TRIALS)
IDX = {k: np.array([t["id"] for t in TRIALS if cond(t)]) for k, cond in {
    "R": lambda t: t["block"] == "R",
    "calib": lambda t: t["role"] == "calib",
    "test": lambda t: t["role"] == "test",
    "S_test": lambda t: t["block"] == "S" and t["role"] == "test",
    "X": lambda t: t["block"] == "X",
}.items()}
SUB = {k: tuple(arr[v] for arr in ALL) for k, v in IDX.items()}
CORR = np.array([TRIALS[i]["corr_option"] for i in IDX["X"]])
S_ALL = [t for t in TRIALS if t["block"] == "S"]


def diff(m, th, data):
    v = m.value(th, *data)
    return v[:, 0] - v[:, 1]


def draw(truth, rng):
    target = float(np.exp(rng.normal(np.log(1.5), 0.35)))
    bias = float(rng.normal(0.0, 0.3))
    if truth in ("GEO1", "GEO2", "EARLY"):
        kappa = {"GEO1": 1.0, "GEO2": 2.0}.get(truth) or float(rng.uniform(1.0, 2.0))
        ratio, r = float(rng.uniform(0.25, 1.0)), float(rng.uniform(-0.6, 0.6))
        L = np.linalg.cholesky(np.array([[1.0, r * ratio], [r * ratio, ratio * ratio]]))
        th = np.array([np.log(L[0, 0]), L[1, 0], np.log(L[1, 1]), kappa, 0.0])
        m = M.MODELS["EARLY" if truth == "EARLY" else "GEO"]
        s = (target / np.median(np.abs(diff(m, th, SUB["R"])))) ** (1.0 / kappa)
        th[0] += np.log(s)
        th[1] *= s
        th[2] += np.log(s)
        th[4] = bias
        return m, th, {"r": r, "ratio": ratio, "kappa": kappa}
    if truth in ("RDU", "ADD"):
        eta = 1.0 if truth == "ADD" else float(rng.uniform(0.8, 1.6))
        pi = 0.5 if truth == "ADD" else float(rng.uniform(0.30, 0.48))
        th = np.array([0.0, np.log(eta), np.log(rng.uniform(0.25, 1.0)), np.log(pi / (1 - pi)), 0.0])
        m = M.MODELS["RDU"]
    else:
        th = np.array([0.0, np.log(rng.uniform(0.25, 1.0)), rng.uniform(1.5, 3.0), 0.0])
        m = M.MODELS["CAG"]
    th[0] = np.log(target / np.median(np.abs(diff(m, th, SUB["R"]))))
    th[-1] = bias
    return m, th, {}


def corr_pref(p_left):
    return float(np.where(CORR == 0, p_left, 1 - p_left).mean() - 0.5)


def lottery_rates(y, side, base_level):
    at, off = [], []
    for t in S_ALL:
        if t["side"] != side:
            continue
        took = y[t["id"]] if t["lot_option"] == 0 else 1 - y[t["id"]]
        (at if t["level"] == base_level else off).append(took)
    return float(np.mean(off) - np.mean(at))


def person(truth, rng):
    m, th, shape = draw(truth, rng)
    pl = M.p_left(m, th, ALL)
    y = (rng.random(len(TRIALS)) < pl).astype(float)
    fits = {k: M.fit(M.MODELS[k], SUB["calib"], y[IDX["calib"]], rng) for k in FIT}
    out = {"ll": {k: M.log_loss(M.MODELS[k], fits[k], SUB["test"], y[IDX["test"]]) for k in FIT},
           "ll_S": {k: M.log_loss(M.MODELS[k], fits[k], SUB["S_test"], y[IDX["S_test"]]) for k in FIT},
           "ll_X": {k: M.log_loss(M.MODELS[k], fits[k], SUB["X"], y[IDX["X"]]) for k in FIT},
           "obs_corr": float(np.where(CORR == 0, y[IDX["X"]], 1 - y[IDX["X"]]).mean() - 0.5),
           "pred_corr": corr_pref(M.p_left(M.MODELS["GEO"], fits["GEO"], SUB["X"])),
           "true_corr": corr_pref(pl[IDX["X"]]),
           "bg": 0.5 * (lottery_rates(y, "self", 0) + lottery_rates(y, "charity", 0))}
    if shape:
        P11, P12, P22 = M.metric(fits["GEO"])
        out["rec"] = {**shape, "r_hat": float(P12 / np.sqrt(P11 * P22)), "ratio_hat": float(np.sqrt(P22 / P11)),
                      "kappa_hat": float(fits["GEO"][3])}
    return out


def ci(x):
    x = np.asarray(x, float)
    m, se = x.mean(), x.std(ddof=1) / np.sqrt(len(x))
    return float(m), float(m - 1.96 * se), float(m + 1.96 * se)


def tests(ps):
    n, res = len(ps), {}
    for k in ("EARLY", "RDU", "CAG"):
        d = [p["ll"]["GEO"] - p["ll"][k] for p in ps]
        est, lo, hi = ci(d)
        res[f"H_vs_{k}"] = {"est": est, "lo": lo, "hi": hi, "pass": [bool(hi < -mg) for mg in MARGINS],
                            "est_S": ci([p["ll_S"]["GEO"] - p["ll_S"][k] for p in ps])[0],
                            "est_X": ci([p["ll_X"]["GEO"] - p["ll_X"][k] for p in ps])[0]}
    rho = spearmanr([p["pred_corr"] for p in ps], [p["obs_corr"] for p in ps]).statistic
    if np.isfinite(rho):
        z, se = np.arctanh(np.clip(rho, -0.999, 0.999)), np.sqrt(1.06 / (n - 3))
        res["H4"] = {"rho": float(rho), "lo": float(np.tanh(z - 1.96 * se)), "pass": bool(np.tanh(z - 1.96 * se) > 0)}
    else:
        res["H4"] = {"rho": None, "lo": None, "pass": False}
    for key, name in (("obs_corr", "MF1"), ("bg", "MF2")):
        est, lo, hi = ci([p[key] for p in ps])
        res[name] = {"est": est, "lo": lo, "hi": hi, "pass": bool(lo > 0 or hi < 0)}
    res["mean_ll"] = {k: float(np.mean([p["ll"][k] for p in ps])) for k in FIT}
    return res


def recovery(ps):
    rec = [p["rec"] for p in ps if "rec" in p]
    if not rec:
        return {}
    g = lambda k: np.array([r[k] for r in rec])  # noqa: E731
    out = {"r_corr": float(np.corrcoef(g("r"), g("r_hat"))[0, 1]),
           "r_mae": float(np.median(np.abs(g("r_hat") - g("r")))),
           "logratio_corr": float(np.corrcoef(np.log(g("ratio")), np.log(g("ratio_hat")))[0, 1]),
           "kappa_hat_mean": float(g("kappa_hat").mean()), "kappa_hat_sd": float(g("kappa_hat").std()),
           "effect_corr": float(np.corrcoef([p["true_corr"] for p in ps], [p["pred_corr"] for p in ps])[0, 1])}
    if g("kappa").std() > 0:
        out["kappa_corr"] = float(np.corrcoef(g("kappa"), g("kappa_hat"))[0, 1])
    return out


def main(truth, out, *_):
    np.seterr(all="ignore")
    t0, sims = time.time(), []
    for sim in range(SIMS):
        rng = np.random.default_rng([SEED, TRUTHS.index(truth), sim])
        ps = [person(truth, rng) for _ in range(max(NS))]
        sims.append({**{f"n{n}": tests(ps[:n]) for n in NS}, "recovery": recovery(ps)})
        print(sim, f"{time.time() - t0:.0f}s", flush=True)
    res = {"truth": truth, "ns": NS, "sims_n": SIMS, "margins": MARGINS, "sims": sims, "seconds": time.time() - t0}
    json.dump(res, open(out, "w"))
    print("RESULT-BEGIN")
    print(json.dumps({k: v for k, v in res.items() if k != "sims"}))
    print("RESULT-END", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
