#!/usr/bin/env python3
"""Rehearsal of the correlation-attitude design (DESIGN.md, "Stages", step 1).

    python rehearsal.py TRUTH OUT.json

TRUTH is one of GEO1, GEO2, EARLY, RDU, CAG, ADD, IA, or IA02, IA05, IA10, IA20 (inequality aversion at a
fixed gamma of 0.02 to 0.20), or a version 5 cell (below). Each simulated study draws people from that model,
runs them through the exact stimulus set (stimuli.py), fits every candidate model per person on the
calibration trials, and scores held-out log-loss on the test trials with no refit. Needs models.py and
stimuli.py beside it. REHEARSAL_QUICK=1 for a smoke test.

Version 6 (2026-11-03), the table the pilot's rules now need (PILOT.md, decisions of 2026-11-03). TABLE_V6 adds
rows at kappa 0.5 and 0.75 (G050, G075) and the rank-one share as a dimension: S20, S40 and S60 at every row
that reached 0.80 by n = 240 in version 5, and at the new rows. After the first pilot rehearsals it also has a
noisier row, target 0.7, at every kappa (NOISY_ROWS), with shares at kappa up to 1: 79 cells in all. Every study also scores the main claim over
the people the main study's self-only flag does not catch (`flagged`: the self-favouring option in at least
MAIN_FLAG_MIN of block R's 20 pairs at ratios 2 and 3), recruited until there are max(ns) of them. Those extra
people come from their own stream, so every version 5 number reproduces; the version 5 cells are rerun for this
alone. The stimulus set is version 5, whose attention checks moved, and no simulated choice the claim reads
changed with them (stimuli.py).

Version 5 (2026-11-03), the power table the pilot reads (PILOT.md). A cell is named by its base model, then
T and the centre of the noise target (the median |logit| over block R) times ten, then optionally S and the
share of rank-one people in percent, and L and the lapse ceiling in percent:
  G125T15     GEO with kappa 1.25 for everyone (the digits after G are kappa times 100), target around 1.5
  G150T15S40  the same at kappa 1.5, with 40% of people of rank one, who weigh only their own points
  RDUT20L15   RDU drawn as in version 4, target around 2.0, lapses drawn from U(0, 0.15)
Cells run 50 studies of 240 people, with tests on the first 60, 120, 160, 200 and 240 (NS5). TABLE_V5 lists
the table's 22 cells. A cell is seeded by a checksum of its name; the version 4 truths keep their seeds,
their n and their draws, so their results reproduce. `simulate` takes another trial set (`data`), which
pilot_analysis.py uses to run simulated pilots through the pilot-only trials.

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
import re
import sys
import time
import zlib

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import models as M  # noqa: E402
import stimuli  # noqa: E402

# IA02 .. IA20: inequality aversion at a fixed gamma of 0.02, 0.05, 0.10 and 0.20, for the power of the
# secondary claim against weaker aversion than IA's U(0.1, 0.6). Appended, so earlier truths keep their seeds.
TRUTHS = ["GEO1", "GEO2", "EARLY", "RDU", "CAG", "ADD", "IA", "IA02", "IA05", "IA10", "IA20"]
# version 5, the power table (PILOT.md): 15 GEO cells (kappa by noise target), 2 rank-one cells and 5
# specificity cells (the non-GEO truths, sharp choosers, lapses up to 0.15)
TABLE_V5 = ([f"G{k}T{t}" for k in (100, 125, 150, 175, 200) for t in (10, 15, 20)] + ["G100T15S40", "G150T15S40"]
            + [f"{b}T20L15" for b in ("EARLY", "RDU", "CAG", "ADD", "IA")])
# version 6: rows at kappa 0.5 and 0.75, and shares of 20, 40 and 60% of rank-one people at the rows that reached
# 0.80 by n = 240 in version 5 and at the new rows. The version 5 cells come first and are rerun.
POWERED_V5 = ["G100T10", "G100T15", "G100T20", "G125T15", "G125T20", "G200T20"]
LOW_ROWS = [f"G{k:03d}T{t}" for k in (50, 75) for t in (10, 15, 20)]
# Added after the first two pilot rehearsals (2026-11-03): a noisier row, target 0.7, at every kappa, with shares at
# kappa <= 1. A pilot's pessimistic agreement fell below every target-1.0 row in up to 17% of simulated pilots, and
# the rule then had no noise position. These 16 cells ran with this file before the list grew; nothing else differs.
NOISY_ROWS = [f"G{k:03d}T07" for k in (50, 75, 100, 125, 150, 175, 200)]
TABLE_V6 = (TABLE_V5 + LOW_ROWS + [f"{r}S{s}" for r in POWERED_V5 + LOW_ROWS for s in (20, 40, 60) if f"{r}S{s}" not in TABLE_V5]
            + NOISY_ROWS + [f"{r}S{s}" for r in NOISY_ROWS[:3] for s in (20, 40, 60)])
CELL = re.compile(r"(?:G(\d{3})|(EARLY|RDU|CAG|ADD|IA))T(\d{2})(?:S(\d{2}))?(?:L(\d{2}))?")
MAIN_FLAG_MIN = 15          # of block R's 20 pairs at ratios 2 and 3 (version 6)
FIT = ["GEO", "EARLY", "RDU", "CAG", "IA"]
NS = [60, 120, 200]
NS5 = [60, 120, 160, 200, 240]
SIMS = 50
MARGINS = [0.0, 0.002, 0.005, 0.01]
SEED = 20261102
# Version 3: the hierarchical population kappa (hier.py, NumPyro) on the first HIER_N people of the first
# HIER_SIMS studies. Needs jax and numpyro; REHEARSAL_HIER_SIMS=0 skips it.
HIER_SIMS = int(os.environ.get("REHEARSAL_HIER_SIMS", "10"))
HIER_N = 120
SEC_MARGIN = 0.005      # the registered margin, applied to the secondary comparison too
if os.environ.get("REHEARSAL_QUICK"):
    NS, NS5, SIMS = [30], [30], 2
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
HI_R = np.array([t["id"] for t in TRIALS if t["cell"] in ("R_ratio2", "R_ratio3")])
SELF_HI_R = np.array([stimuli.self_option(TRIALS[i]) for i in HI_R])
CORR = np.array([TRIALS[i]["corr_option"] for i in IDX["X"]])
CORR_XC = np.array([TRIALS[i]["corr_option"] for i in IDX["XC"]])
S_ALL = [t for t in TRIALS if t["block"] == "S"]
SC_ALL = [t for t in TRIALS if t["block"] == "SC"]


def diff(m, th, data):
    v = m.value(th, *data)
    return v[:, 0] - v[:, 1]


def spec(truth):
    """The truth's parameters: base model, kappa (GEO, the same for everyone), gamma (IA, fixed), the
    centre of the noise target, the share of rank-one people and the lapse ceiling."""
    sp = {"base": truth, "kappa": None, "gamma": None, "target": 1.5, "share": 0.0, "lapse": 0.06, "v5": False}
    if truth in ("GEO1", "GEO2"):
        sp.update(base="GEO", kappa=float(truth[3]))
    elif truth in TRUTHS and truth.startswith("IA") and truth != "IA":
        sp.update(base="IA", gamma=int(truth[2:]) / 100)
    elif truth not in TRUTHS:
        m = CELL.fullmatch(truth)
        if m is None:
            raise ValueError(f"unknown truth {truth!r}")
        k, base, t, s, lapse = m.groups()
        if s and not k:
            raise ValueError(f"{truth}: a rank-one share is defined for GEO cells only")
        sp.update(base=base or "GEO", kappa=int(k) / 100 if k else None, target=int(t) / 10,
                  share=int(s) / 100 if s else 0.0, lapse=int(lapse) / 100 if lapse else 0.06, v5=True)
    return sp


def draw(truth, rng):
    sp = spec(truth)
    target = float(np.exp(rng.normal(np.log(sp["target"]), 0.35)))
    bias = float(rng.normal(0.0, 0.3))
    if sp["base"] in ("GEO", "EARLY"):
        kappa = sp["kappa"] or float(rng.uniform(1.0, 2.0))
        ratio, r = float(rng.uniform(0.25, 1.0)), float(rng.uniform(-0.6, 0.6))
        L = np.linalg.cholesky(np.array([[1.0, r * ratio], [r * ratio, ratio * ratio]]))
        th = np.array([np.log(L[0, 0]), L[1, 0], np.log(L[1, 1]), kappa, 0.0])
        m = M.MODELS[sp["base"]]
        s = (target / np.median(np.abs(diff(m, th, SUB["R"])))) ** (1.0 / kappa)
        th[0] += np.log(s)
        th[1] *= s
        th[2] += np.log(s)
        th[4] = bias
        if sp["share"] and rng.random() < sp["share"]:
            # version 5: rank one, the same person with no weight on the charity. Their sensitivity to
            # their own points is kept, not rescaled to the noise target, so they choose consistently in
            # block R, as someone who ignores the charity would.
            th[1], th[2] = 0.0, -30.0
            return m, th, {"rank_one": True, "kappa": kappa}
        return m, th, {"r": r, "ratio": ratio, "kappa": kappa}
    if sp["base"] in ("RDU", "ADD"):
        eta = 1.0 if sp["base"] == "ADD" else float(rng.uniform(0.8, 1.6))
        pi = 0.5 if sp["base"] == "ADD" else float(rng.uniform(0.30, 0.48))
        th = np.array([0.0, np.log(eta), np.log(rng.uniform(0.25, 1.0)), np.log(pi / (1 - pi)), 0.0])
        m = M.MODELS["RDU"]
    elif sp["base"] == "CAG":
        th = np.array([0.0, np.log(rng.uniform(0.25, 1.0)), rng.uniform(1.5, 3.0), 0.0])
        m = M.MODELS["CAG"]
    else:  # IA: inequality aversion between self and charity, gamma ~ U(0.1, 0.6); IAxx: gamma fixed at xx/100
        lam = rng.uniform(0.25, 1.0)
        gamma = rng.uniform(0.1, 0.6) if sp["gamma"] is None else sp["gamma"]
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


def simulate(truth, rng, data=None):
    """One simulated person: true model, choices on every trial of the main set (or of `data`), with a
    lapse drawn from U(0, the truth's ceiling), 0.06 unless the truth says otherwise."""
    m, th, shape = draw(truth, rng)
    pl = M.p_choice(m.logit(th, *(ALL if data is None else data)), lapse=float(rng.uniform(0.0, spec(truth)["lapse"])))
    return {"y": (rng.random(len(pl)) < pl).astype(float), "pl": pl, "shape": shape}


def flagged(y):
    """The main study's self-only flag (version 6): the self-favouring option in at least MAIN_FLAG_MIN of block R's
    20 pairs at ratios 2 and 3. y is 1 where the left option (option 0) was chosen."""
    return bool(np.sum(1 - y[HI_R] == SELF_HI_R) >= MAIN_FLAG_MIN)


def evaluate(sim, fits, fits1):
    y, pl, shape = sim["y"], sim["pl"], sim["shape"]
    out = {"rank_one": bool(shape.get("rank_one")),
           "ll1": {k: M.log_loss(M.MODELS[k], fits1[k], SUB["test"], y[IDX["test"]]) for k in FIT},
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
    if "ratio" in shape:        # GEO and EARLY people who trade the two off; not the rank-one ones
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
    sp = spec(truth)
    ns = NS5 if sp["v5"] else NS
    t0, sims = time.time(), []
    for sim in range(SIMS):
        key = [SEED, TRUTHS.index(truth), sim] if truth in TRUTHS else [SEED, 5, zlib.crc32(truth.encode()), sim]
        rng = np.random.default_rng(key)
        people = [simulate(truth, rng) for _ in range(max(ns))]
        calib = [(SUB["calib"], p["y"][IDX["calib"]]) for p in people]
        f1 = [{k: M.fit(M.MODELS[k], d, y, rng) for k in FIT} for d, y in calib]
        # empirical-Bayes prior from the first ns[0] people, used for everyone in the study
        priors = {k: M.eb_prior(M.MODELS[k], [f[k] for f in f1[:ns[0]]]) for k in FIT}
        f2 = [{k: M.fit(M.MODELS[k], d, y, rng, starts=1, prior=priors[k], x0=f[k]) for k in FIT}
              for (d, y), f in zip(calib, f1)]
        ps = [evaluate(p, b, a) for p, a, b in zip(people, f1, f2)]
        record = {**{f"n{n}": tests(ps[:n]) for n in ns}, "recovery": recovery(ps)}
        # version 6: the claim over the people the self-only flag does not catch, recruited until there are max(ns)
        # of them. Extra people come from their own stream and use the study's prior, so nothing above changes.
        flags = [flagged(p["y"]) for p in people]
        kept = [q for q, f in zip(ps, flags) if not f]
        xrng, extras = np.random.default_rng([*key, 6]), 0
        while len(kept) < max(ns):
            p = simulate(truth, xrng)
            extras += 1
            if flagged(p["y"]):
                continue
            d, y = SUB["calib"], p["y"][IDX["calib"]]
            a = {k: M.fit(M.MODELS[k], d, y, xrng) for k in FIT}
            b = {k: M.fit(M.MODELS[k], d, y, xrng, starts=1, prior=priors[k], x0=a[k]) for k in FIT}
            kept.append(evaluate(p, b, a))
        r1 = [q["rank_one"] for q in ps]
        record["unflagged"] = {**{f"n{n}": tests(kept[:n]) for n in ns}, "extras": extras,
                               "residual_rank_one": float(np.mean([q["rank_one"] for q in kept[:max(ns)]]))}
        record["flags"] = {"rank_one": [sum(f for f, r in zip(flags, r1) if r), sum(r1)],
                           "trader": [sum(f for f, r in zip(flags, r1) if not r), len(r1) - sum(r1)]}
        if sim < HIER_SIMS:
            import hier  # noqa: PLC0415  (jax is needed only here)
            Y = np.stack([p["y"][IDX["calib"]] for p in people[:HIER_N]])
            record["hier"] = {**hier.fit(SUB["calib"], Y, seed=sim), "n": HIER_N}
        sims.append(record)
        print(sim, f"{time.time() - t0:.0f}s", flush=True)
    # true_kappa: the population median kappa of the GEO truths; None elsewhere. EARLY is not GEO: its kappa
    # (drawn from U(1, 2)) shapes only riskless choices, its lotteries are risk-neutral, and GEO's fitted
    # kappa has no reason to equal it. Version 3 ran with EARLY set to 1.5, which made a coverage figure
    # for EARLY that means nothing (REHEARSAL.md); aggregate_rehearsal.py reports coverage for GEO only.
    res = {"truth": truth, "version": 6, "spec": sp, "ns": ns, "sims_n": SIMS, "margins": MARGINS,
           "lapse": M.LAPSE, "hier_sims": HIER_SIMS, "hier_n": HIER_N, "main_flag_min": MAIN_FLAG_MIN,
           "true_kappa": sp["kappa"] if sp["base"] == "GEO" else None, "sims": sims, "seconds": time.time() - t0}
    json.dump(res, open(out, "w"))
    print("RESULT-BEGIN")
    print(json.dumps({k: v for k, v in res.items() if k != "sims"}))
    print("RESULT-END", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
