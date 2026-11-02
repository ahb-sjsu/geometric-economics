#!/usr/bin/env python3
"""Diagnose the upward bias of fitted kappa under the GEO1 truth (REHEARSAL.md, "Open before sealing").

    python diag_kappa.py OUT.json [PEOPLE] [CONFIG ...]

The truth is GEO1 (kappa = 1) as in rehearsal.py, unless a configuration changes one ingredient. Each
configuration simulates PEOPLE people (default 300), fits GEO by first-pass MAP on the calibration
trials, and reports the mean, median and spread of fitted kappa. One factor changes at a time:

  base             as in the rehearsal: prior kappa ~ N(1.5, 1.5), calibration = R + the 8 S cells at
                   the ideal, simulated lapse U(0, 0.06), model lapse 0.04
  prior_1          prior mean for kappa 1.0 instead of 1.5
  prior_flat       no prior on kappa (sd 1000)
  no_lapse         the simulated people never lapse
  sharp            simulated people three times as sensitive (median |logit| over R about 4.5)
  r_only           calibration on the 40 riskless pairs only
  shape_round      truth with an untilted, equal-weight metric (P proportional to I)
  s_x3             the 8 S cells at the ideal answered three times each
  eb               the rehearsal's second pass, empirical-Bayes prior from the first-pass estimates
  all_x5           every calibration trial answered five times (240 choices)
  all_x5_lapse04   the same, with the simulated lapse fixed at the model's 0.04
  all_x5_flat      all_x5 with no prior on kappa
  kappa_only       kappa alone fitted on the 8 S cells, P and bias fixed at the truth (no prior)
  kappa_only_x5    the same with each S cell answered 5 times (40 choices)
  kappa_only_x20   the same with each S cell answered 20 times (160 choices)
  eb_pooled        the second pass with its kappa prior centred on a pooled kappa (option 1)
  eb_sharp, eb_pooled_sharp   the plain and pooled second pass for three-times-sharper choosers
  eb_s_x3, eb_pooled_s_x3     the same with the 8 S cells answered three times each (option 2)
  eb_laplace, eb_laplace_sharp, eb_laplace_s_x3   option 1 with the pooled kappa from the summed
                   Laplace-approximated marginal likelihood (nuisance parameters integrated out)
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy.optimize import minimize_scalar

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import models as M  # noqa: E402
import rehearsal as R  # noqa: E402

GEO = M.MODELS["GEO"]
S_CAL = np.array([t["id"] for t in R.TRIALS if t["block"] == "S" and t["role"] == "calib"])
SPEC = {"base": {}, "prior_1": {"kmu": 1.0}, "prior_flat": {"ksd": 1000.0}, "no_lapse": {"lapse": 0.0},
        "sharp": {"sharp": 3.0}, "r_only": {"calib": "R"}, "shape_round": {"round": True},
        "s_x3": {"s_rep": 3}, "eb": {"eb": True}, "all_x5": {"rep": 5},
        "all_x5_lapse04": {"rep": 5, "lapse": 0.04}, "all_x5_flat": {"rep": 5, "ksd": 1000.0},
        "kappa_only": {"kappa_only": True}, "kappa_only_x5": {"kappa_only": True, "s_rep": 5},
        "kappa_only_x20": {"kappa_only": True, "s_rep": 20},
        # option 1: second-pass prior centred on a pooled kappa (models.pooled_center); option 2: more
        # lottery choices at the ideal (s_rep). Compared with the plain second pass (eb).
        "eb_pooled": {"eb": True, "pooled": True}, "eb_sharp": {"eb": True, "sharp": 3.0},
        "eb_pooled_sharp": {"eb": True, "pooled": True, "sharp": 3.0},
        "eb_s_x3": {"eb": True, "s_rep": 3}, "eb_pooled_s_x3": {"eb": True, "pooled": True, "s_rep": 3},
        # option 1 with the nuisance parameters integrated out (Laplace) instead of maximized over
        "eb_laplace": {"eb": True, "pooled": "laplace"},
        "eb_laplace_sharp": {"eb": True, "pooled": "laplace", "sharp": 3.0},
        "eb_laplace_s_x3": {"eb": True, "pooled": "laplace", "s_rep": 3}}
CONFIGS = list(SPEC)


def truth(rng, sharp=1.0, round_shape=False):
    target = sharp * float(np.exp(rng.normal(np.log(1.5), 0.35)))
    ratio, r = (1.0, 0.0) if round_shape else (float(rng.uniform(0.25, 1.0)), float(rng.uniform(-0.6, 0.6)))
    L = np.linalg.cholesky(np.array([[1.0, r * ratio], [r * ratio, ratio * ratio]]))
    th = np.array([np.log(L[0, 0]), L[1, 0], np.log(L[1, 1]), 1.0, 0.0])
    s = target / np.median(np.abs(R.diff(GEO, th, R.SUB["R"])))
    th[0] += np.log(s)
    th[1] *= s
    th[2] += np.log(s)
    th[4] = float(rng.normal(0.0, 0.3))
    return th


def answer(th, idx, rng, lapse):
    data = tuple(arr[idx] for arr in R.ALL)
    return (rng.random(len(idx)) < M.p_choice(GEO.logit(th, *data), lapse=lapse)).astype(float)


def kappa_only(th_true, idx, y):
    data = tuple(arr[idx] for arr in R.ALL)

    def nll(k):
        th = th_true.copy()
        th[3] = k
        p = M.p_choice(GEO.logit(th, *data))
        return -(y * np.log(p) + (1 - y) * np.log(1 - p)).sum()

    return minimize_scalar(nll, bounds=(0.5, 4.0), method="bounded").x


def run(config, people, seed):
    sp = SPEC[config]
    rng = np.random.default_rng([seed, CONFIGS.index(config)])
    mu, sd = GEO.mu.copy(), GEO.sd.copy()
    mu[3] = sp.get("kmu", mu[3])
    sd[3] = sp.get("ksd", sd[3])
    calib = R.IDX["R"] if sp.get("calib") == "R" else R.IDX["calib"]
    est, firsts = [], []
    for _ in range(people):
        th = truth(rng, sharp=sp.get("sharp", 1.0), round_shape=sp.get("round", False))
        lapse = sp["lapse"] if "lapse" in sp else float(rng.uniform(0.0, 0.06))
        if sp.get("kappa_only"):
            idx = np.tile(S_CAL, sp.get("s_rep", 1))
            est.append(kappa_only(th, idx, answer(th, idx, rng, lapse)))
            continue
        idx = np.concatenate([np.tile(calib, sp.get("rep", 1))] + [S_CAL] * (sp.get("s_rep", 1) - 1))
        y = answer(th, idx, rng, lapse)
        data = tuple(arr[idx] for arr in R.ALL)
        f = M.fit(GEO, data, y, rng, prior=(mu, sd))
        firsts.append((f, data, y))
        est.append(f[3])
    extra = {}
    if sp.get("eb"):
        prior = M.eb_prior(GEO, [f for f, _, _ in firsts[:60]])
        if sp.get("pooled"):
            ref = firsts[:60]
            prior[0][3] = extra["pooled_center"] = M.pooled_center(GEO, 3, [(d, y) for _, d, y in ref],
                                                                   [f for f, _, _ in ref],
                                                                   laplace=sp["pooled"] == "laplace")
        est = [M.fit(GEO, d, y, rng, starts=1, prior=prior, x0=f)[3] for f, d, y in firsts]
    k = np.array(est)
    return {"mean": float(k.mean()), "median": float(np.median(k)), "sd": float(k.std()),
            "q10": float(np.quantile(k, 0.1)), "q90": float(np.quantile(k, 0.9)),
            "at_upper_bound": float(np.mean(k > 3.99)), "at_lower_bound": float(np.mean(k < 0.51)), **extra}


if __name__ == "__main__":
    np.seterr(over="ignore")
    out = sys.argv[1]
    people = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    todo = sys.argv[3:] or CONFIGS
    res = {}
    for c in todo:
        res[c] = run(c, people, 20261103)
        print(f"{c:<15} mean {res[c]['mean']:.3f}  median {res[c]['median']:.3f}  sd {res[c]['sd']:.3f}  "
              f"q10-q90 {res[c]['q10']:.2f}-{res[c]['q90']:.2f}  bounds lo {res[c]['at_lower_bound']:.2f} "
              f"hi {res[c]['at_upper_bound']:.2f}" +
              (f"  pooled centre {res[c]['pooled_center']:.3f}" if "pooled_center" in res[c] else ""), flush=True)
    json.dump({"people": people, "true_kappa": 1.0, "configs": res}, open(out, "w"), indent=1)
