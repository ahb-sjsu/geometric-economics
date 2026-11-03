#!/usr/bin/env python3
"""Rehearsal of the correlation-attitude design (DESIGN.md, "Stages", step 1).

    python rehearsal.py TRUTH OUT.json

TRUTH is one of GEO1, GEO2, EARLY, RDU, CAG, ADD, IA, or IA02, IA05, IA10, IA20 (inequality aversion at a
fixed gamma of 0.02 to 0.20). Each simulated study draws people from that model,
runs them through the exact stimulus set (stimuli.py), fits every candidate model per person on the
calibration trials, and scores held-out log-loss on the test trials with no refit. Needs models.py and
stimuli.py beside it. REHEARSAL_QUICK=1 for a smoke test.

Version 4 (2026-11-02). The stimulus set adds the crossing set (stimuli.py: 8 XC pairs and 12 SC straddle
lotteries, role "secondary"), the truths add IA (inequality aversion between self and charity, gamma ~
U(0.1, 0.6)), and the fitted models add IA. The main tests are unchanged and never see the crossing set.
Secondary tests, on the crossing set, intervals over people:
  SH1   IA predicts the crossing set better than GEO (held-out log-loss, margin 0.005); SH1r the reverse.
  SH2   lottery choice at the straddling lotteries falls below GEO's zero-fit prediction (the kink).
  SH3   the correlated, equal-split option in XC is chosen above GEO's zero-fit prediction; SH3_did the
        same minus the person's residual on the main X pairs (GEO's calibration bias cancels).

Version 3 (2026-11-02). The stimulus set has 12 calibration lotteries per attribute at the ideal
(stimuli.py version 3), and the first HIER_SIMS studies of each truth also get the hierarchical
population kappa (hier.py) from their first HIER_N people, to check that it recovers the truth.

Version 2 (2026-11-02). Simulated people lapse at a rate drawn from U(0, 0.06); every model chooses
with a fixed 4% lapse; each model is fit twice, first with fixed weak priors, then with an empirical-
Bayes prior (median and MAD of the first-pass estimates over the first NS[0] people). Version 1 had
neither: its fitted models were overconfident on test trials far from the calibration region, and
held-out log-loss was worse than chance even for the true model (REHEARSAL.md).

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
  H4                comparative: across people, the Spearman correlation between the correlated-option
                    preference GEO predicts from calibration and the one observed in block X, minus
                    the larger of RDU's and CAG's; bootstrap lower end above 0. (Version 1 used GEO's
                    correlation alone, which also passed under RDU, because pessimism and kappa > 1
                    both show as risk aversion at the ideal.)
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

# IA02 .. IA20: inequality aversion at a fixed gamma of 0.02, 0.05, 0.10 and 0.20, for the power of the
# secondary claim against weaker aversion than IA's U(0.1, 0.6). Appended, so earlier truths keep their seeds.
TRUTHS = ["GEO1", "GEO2", "EARLY", "RDU", "CAG", "ADD", "IA", "IA02", "IA05", "IA10", "IA20"]
FIT = ["GEO", "EARLY", "RDU", "CAG", "IA"]
NS = [60, 120, 200]
SIMS = 50
MARGINS = [0.0, 0.002, 0.005, 0.01]
SEED = 20261102
# Version 3: the hierarchical population kappa (hier.py, NumPyro) on the first HIER_N people of the first
# HIER_SIMS studies. Needs jax and numpyro; REHEARSAL_HIER_SIMS=0 skips it.
HIER_SIMS = int(os.environ.get("REHEARSAL_HIER_SIMS", "10"))
HIER_N = 120
# the population median kappa of the GEO truths; None elsewhere. EARLY is not GEO: its kappa (drawn from
# U(1, 2)) shapes only riskless choices, its lotteries are risk-neutral, and GEO's fitted kappa has no
# reason to equal it. Version 3 ran with EARLY set to 1.5, which made a coverage figure for EARLY that
# means nothing (REHEARSAL.md); aggregate_rehearsal.py reports coverage for GEO truths only.
TRUE_KAPPA = {"GEO1": 1.0, "GEO2": 2.0, "EARLY": None, "RDU": None, "CAG": None, "ADD": None, "IA": None}
SEC_MARGIN = 0.005      # the registered margin, applied to the secondary comparison too
if os.environ.get("REHEARSAL_QUICK"):
    NS, SIMS = [30], 2
    HIER_SIMS, HIER_N = min(HIER_SIMS, 1), 30

TRIALS = stimuli.build()
ALL = M.arrays(TRIALS)
IDX = {k: np.array([t["id"] for t in TRIALS if cond(t)]) for k, cond in {
    "R": lambda t: t["block"] == "R",
    "calib": lambda t: t["role"] == "calib",
    "test": lambda t: t["role"] == "test",
    "S_test": lambda t: t["block"] == "S" and t["role"] == "test",
    "X": lambda t: t["block"] == "X",
    "secondary": lambda t: t["role"] == "secondary",
    "XC": lambda t: t["block"] == "XC",
}.items()}
SUB = {k: tuple(arr[v] for arr in ALL) for k, v in IDX.items()}
CORR = np.array([TRIALS[i]["corr_option"] for i in IDX["X"]])
CORR_XC = np.array([TRIALS[i]["corr_option"] for i in IDX["XC"]])
S_ALL = [t for t in TRIALS if t["block"] == "S"]
SC_ALL = [t for t in TRIALS if t["block"] == "SC"]


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
    elif truth == "CAG":
        th = np.array([0.0, np.log(rng.uniform(0.25, 1.0)), rng.uniform(1.5, 3.0), 0.0])
        m = M.MODELS["CAG"]
    else:  # IA: inequality aversion between self and charity, gamma ~ U(0.1, 0.6); IAxx: gamma fixed at xx/100
        lam = rng.uniform(0.25, 1.0)
        gamma = rng.uniform(0.1, 0.6) if truth == "IA" else int(truth[2:]) / 100
        th = np.array([0.0, np.log(lam), gamma, 0.0])
        m = M.MODELS["IA"]
    th[0] = np.log(target / np.median(np.abs(diff(m, th, SUB["R"]))))
    th[-1] = bias
    return m, th, {}


def corr_pref(p_left):
    return float(np.where(CORR == 0, p_left, 1 - p_left).mean() - 0.5)


def lottery_rates(y, side, base_level, matched_only=True):
    """Lottery-choice rate off the ideal minus at the ideal, on one attribute. Only the lotteries offered
    at every level enter (`matched`); the version 3 rehearsal ran with matched_only=False in effect,
    which compares different gambles and gave false positives under RDU (REHEARSAL.md)."""
    at, off = [], []
    for t in S_ALL:
        if t["side"] != side or (matched_only and not t.get("matched", True)):
            continue
        took = y[t["id"]] if t["lot_option"] == 0 else 1 - y[t["id"]]
        (at if t["level"] == base_level else off).append(took)
    return float(np.mean(off) - np.mean(at))


def straddle(p):
    """Lottery-choice probability (or rate) at the straddling lotteries minus the mean of the two
    non-straddling controls with the same spread, averaged over attribute and spread. Negative = more
    risk-averse exactly where the outcomes cross self = charity, the kink inequality aversion predicts."""
    took = {(t["side"], t["level"], t["spread"]): (p[t["id"]] if t["lot_option"] == 0 else 1 - p[t["id"]])
            for t in SC_ALL}
    return float(np.mean([took[(s, 50, d)] - 0.5 * (took[(s, 25, d)] + took[(s, 75, d)])
                          for s in ("self", "charity") for d in (10, 20)]))


def xc_pref(p):
    return float(np.where(CORR_XC == 0, p[IDX["XC"]], 1 - p[IDX["XC"]]).mean() - 0.5)


def simulate(truth, rng):
    """One simulated person: true model, choices on every trial, with a lapse drawn U(0, 0.06)."""
    m, th, shape = draw(truth, rng)
    pl = M.p_choice(m.logit(th, *ALL), lapse=float(rng.uniform(0.0, 0.06)))
    return {"y": (rng.random(len(TRIALS)) < pl).astype(float), "pl": pl, "shape": shape}


def evaluate(sim, fits, fits1):
    y, pl, shape = sim["y"], sim["pl"], sim["shape"]
    out = {"ll1": {k: M.log_loss(M.MODELS[k], fits1[k], SUB["test"], y[IDX["test"]]) for k in FIT},
           "ll": {k: M.log_loss(M.MODELS[k], fits[k], SUB["test"], y[IDX["test"]]) for k in FIT},
           "ll_S": {k: M.log_loss(M.MODELS[k], fits[k], SUB["S_test"], y[IDX["S_test"]]) for k in FIT},
           "ll_X": {k: M.log_loss(M.MODELS[k], fits[k], SUB["X"], y[IDX["X"]]) for k in FIT},
           "obs_corr": float(np.where(CORR == 0, y[IDX["X"]], 1 - y[IDX["X"]]).mean() - 0.5),
           "pred_corr": corr_pref(M.p_left(M.MODELS["GEO"], fits["GEO"], SUB["X"])),
           "pred_corr_RDU": corr_pref(M.p_left(M.MODELS["RDU"], fits["RDU"], SUB["X"])),
           "pred_corr_CAG": corr_pref(M.p_left(M.MODELS["CAG"], fits["CAG"], SUB["X"])),
           "true_corr": corr_pref(pl[IDX["X"]]),
           "bg": 0.5 * (lottery_rates(y, "self", 0) + lottery_rates(y, "charity", 0))}
    # version 4: the crossing set, never used by H1 to H4. GEO's and IA's zero-fit predictions there.
    p_geo = M.p_left(M.MODELS["GEO"], fits["GEO"], ALL)
    out["sec"] = {"ll": {k: M.log_loss(M.MODELS[k], fits[k], SUB["secondary"], y[IDX["secondary"]])
                         for k in ("GEO", "IA")},
                  "straddle_obs": straddle(y), "straddle_geo": straddle(p_geo),
                  "xc_obs": xc_pref(y), "xc_geo": xc_pref(p_geo)}
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
    # H4, comparative: GEO's person-level predictions of the correlated-option preference track the
    # observed ones better than RDU's and CAG's do. Bootstrap over people.
    obs = np.array([p["obs_corr"] for p in ps])
    pred = {k: np.array([p[f"pred_corr{s}"] for p in ps]) for k, s in (("GEO", ""), ("RDU", "_RDU"), ("CAG", "_CAG"))}

    def rho(k, i):
        r = spearmanr(pred[k][i], obs[i]).statistic
        return r if np.isfinite(r) else 0.0

    def gap(i):
        return rho("GEO", i) - max(rho("RDU", i), rho("CAG", i))

    allp = np.arange(n)
    brng = np.random.default_rng([SEED, n])
    boots = np.array([gap(brng.integers(0, n, n)) for _ in range(300)])
    lo = float(np.quantile(boots, 0.025))
    res["H4"] = {"rho": float(rho("GEO", allp)), "rho_RDU": float(rho("RDU", allp)),
                 "rho_CAG": float(rho("CAG", allp)), "gap": float(gap(allp)), "lo": lo, "pass": bool(lo > 0)}
    for key, name in (("obs_corr", "MF1"), ("bg", "MF2")):
        est, lo, hi = ci([p[key] for p in ps])
        res[name] = {"est": est, "lo": lo, "hi": hi, "pass": bool(lo > 0 or hi < 0)}
    res["mean_ll"] = {k: float(np.mean([p["ll"][k] for p in ps])) for k in FIT}
    res["mean_ll_pass1"] = {k: float(np.mean([p["ll1"][k] for p in ps])) for k in FIT}
    # version 4, the crossing set (secondary). Intervals over people; margin as registered.
    sec = {}
    est, lo, hi = ci([p["sec"]["ll"]["IA"] - p["sec"]["ll"]["GEO"] for p in ps])
    sec["SH1_IA_beats_GEO"] = {"est": est, "hi": hi, "pass": bool(hi < -SEC_MARGIN)}
    sec["SH1r_GEO_beats_IA"] = {"est": -est, "hi": -lo, "pass": bool(-lo < -SEC_MARGIN)}
    est, lo, hi = ci([p["sec"]["straddle_obs"] - p["sec"]["straddle_geo"] for p in ps])
    sec["SH2_straddle_beyond_GEO"] = {"est": est, "lo": lo, "hi": hi, "pass": bool(hi < 0)}
    est, lo, hi = ci([p["sec"]["straddle_obs"] for p in ps])
    sec["straddle_raw"] = {"est": est, "lo": lo, "hi": hi, "pass": bool(hi < 0)}
    est, lo, hi = ci([p["sec"]["xc_obs"] - p["sec"]["xc_geo"] for p in ps])
    sec["SH3_equal_splits_beyond_GEO"] = {"est": est, "lo": lo, "hi": hi, "pass": bool(lo > 0)}
    # SH3 as a difference in differences: the XC residual minus the same person's residual on the main X
    # pairs, which never cross. GEO's calibration bias (kappa, REHEARSAL.md) enters both; an equal-split
    # preference enters only XC. In the smoke test the plain SH3 passed under GEO1.
    est, lo, hi = ci([(p["sec"]["xc_obs"] - p["sec"]["xc_geo"]) - (p["obs_corr"] - p["pred_corr"]) for p in ps])
    sec["SH3_did"] = {"est": est, "lo": lo, "hi": hi, "pass": bool(lo > 0)}
    res["secondary"] = sec
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
        people = [simulate(truth, rng) for _ in range(max(NS))]
        calib = [(SUB["calib"], p["y"][IDX["calib"]]) for p in people]
        f1 = [{k: M.fit(M.MODELS[k], d, y, rng) for k in FIT} for d, y in calib]
        # empirical-Bayes prior from the first NS[0] people, used for everyone in the study
        priors = {k: M.eb_prior(M.MODELS[k], [f[k] for f in f1[:NS[0]]]) for k in FIT}
        f2 = [{k: M.fit(M.MODELS[k], d, y, rng, starts=1, prior=priors[k], x0=f[k]) for k in FIT}
              for (d, y), f in zip(calib, f1)]
        ps = [evaluate(p, b, a) for p, a, b in zip(people, f1, f2)]
        record = {**{f"n{n}": tests(ps[:n]) for n in NS}, "recovery": recovery(ps)}
        if sim < HIER_SIMS:
            import hier  # noqa: PLC0415  (jax is needed only here)
            Y = np.stack([p["y"][IDX["calib"]] for p in people[:HIER_N]])
            record["hier"] = {**hier.fit(SUB["calib"], Y, seed=sim), "n": HIER_N}
        sims.append(record)
        print(sim, f"{time.time() - t0:.0f}s", flush=True)
    res = {"truth": truth, "version": 4, "ns": NS, "sims_n": SIMS, "margins": MARGINS, "lapse": M.LAPSE,
           "hier_sims": HIER_SIMS, "hier_n": HIER_N, "true_kappa": TRUE_KAPPA.get(truth),
           "sims": sims, "seconds": time.time() - t0}
    json.dump(res, open(out, "w"))
    print("RESULT-BEGIN")
    print(json.dumps({k: v for k, v in res.items() if k != "sims"}))
    print("RESULT-END", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
