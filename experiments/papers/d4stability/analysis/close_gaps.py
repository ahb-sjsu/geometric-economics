#!/usr/bin/env python3
"""EXPLORATORY. The three gaps named at the end of paper_04.

**Not part of any registration and it changes no verdict.**

    G1  THE LOSS STRATUM IS THIN. How thin, exactly, and what is the best
        estimate its data can support? Pooling every corpus that has pure-loss
        gambles, with problem-clustered uncertainty, and stating the detection
        limit rather than a bare confidence interval.

        Note the trap. The experience arm holds four times the trials but on the
        SAME problems, and the effective sample for a coordinate coefficient is
        the number of problems. Extra trials on the same gambles cannot close
        this gap, and reporting them as if they could would be the error this
        programme has already made once.

    G2  THE FREE SURFACE IS COARSE, and its R^2 against the quadratic is
        ATTENUATED BY CELL NOISE. A weighted R^2 of 0.306 does not mean the
        quadratic misses 69 percent of the structure, because some of the cell to
        cell variation is estimation error. The honest quantity is the R^2 the
        quadratic would score IF IT WERE TRUE, obtained by simulating from the
        fitted quadratic and re-running the whole free-surface estimate. That
        calibrates the number.

    G3  SEPARABILITY HAS NEVER BEEN TESTED. The model assumes the expected-value
        coefficient does not depend on position, `b_EV * dEV + kappa(d,q) * dSD`.
        If it does, part of what has been read as kappa structure is really
        b_EV structure. Fitted against the full model in which BOTH coefficients
        vary over the plane, compared in sample and out of sample by problem.

    python close_gaps.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
V3 = os.path.abspath(os.path.join(HERE, "..", "..", "d4interior", "analysis"))
sys.path.insert(0, DATASETS)
sys.path.insert(0, V3)
sys.path.insert(0, HERE)

from d4_rotation import _opt_coords  # noqa: E402
from kappa_mle import TERM_NAMES, _nll_grad_hess, fit  # noqa: E402
from stability_rows_v2 import load_covariates, load_outcome  # noqa: E402

B_BOOT = 400
SEED = 20260913
IDQ = TERM_NAMES.index("d*q")
ID2 = TERM_NAMES.index("d2-q2")


def _z(x):
    s = x.std()
    return (x - x.mean()) / (s if s > 1e-12 else 1.0)


def terms(d, q):
    return np.vstack([np.ones_like(d), d ** 2 + q ** 2, d * q,
                      d, q, d ** 2 - q ** 2])


def fit_se(X, y):
    th, info = fit(X, y)
    _n, _g, H = _nll_grad_hess(X, y, th)
    try:
        se = np.sqrt(np.diag(np.linalg.inv(H)))
    except np.linalg.LinAlgError:
        se = np.full(len(th), np.nan)
    return th, se, info


def logistic(v):
    return np.where(v >= 0, 1.0 / (1.0 + np.exp(-np.clip(v, -700, 700))),
                    np.exp(np.clip(v, -700, 0)) / (1.0 + np.exp(np.clip(v, -700, 0))))


def free_surface(d, q, eZ, sZ, y, nbin, min_problems, pid):
    """One free kappa per cell, keeping cells with enough distinct PROBLEMS."""
    de = np.quantile(d, np.linspace(0, 1, nbin + 1))
    qe = np.quantile(q, np.linspace(0, 1, nbin + 1))
    de[0] -= 1e-9
    qe[0] -= 1e-9
    cell = (np.clip(np.digitize(d, de[1:-1]), 0, nbin - 1) * nbin
            + np.clip(np.digitize(q, qe[1:-1]), 0, nbin - 1))
    keep = [c for c in range(nbin * nbin)
            if len(np.unique(pid[cell == c])) >= min_problems]
    if len(keep) < 8:
        return None
    cols = [eZ] + [np.where(cell == c, sZ, 0.0) for c in keep]
    th, se, info = fit_se(np.vstack(cols).T, y)
    kap, ks = th[1:], se[1:]
    cd = np.array([d[cell == c].mean() for c in keep])
    cq = np.array([q[cell == c].mean() for c in keep])
    T = terms(cd, cq).T
    W = np.diag(1.0 / np.maximum(ks, 1e-9) ** 2)
    beta = np.linalg.solve(T.T @ W @ T, T.T @ W @ kap)
    resid = kap - T @ beta
    wm = np.average(kap, weights=np.diag(W))
    sst = float((((kap - wm) ** 2) * np.diag(W)).sum())
    ssr = float(((resid ** 2) * np.diag(W)).sum())
    return {"cells": len(keep), "r2": float(1 - ssr / sst) if sst > 0 else np.nan,
            "max_resid": float(np.max(np.abs(resid / np.maximum(ks, 1e-9)))),
            "beta": beta, "kappa": kap, "se": ks, "cd": cd, "cq": cq}


def main():
    out = {"note": "EXPLORATORY, changes no registered verdict"}
    dEV, dSD, d, q, pid, fold, scale, part = load_covariates()
    y = load_outcome()
    eZ, sZ = _z(dEV), _z(dSD)
    z = np.load(os.path.join(HERE, "seam_covariates.npz"))
    rH, rL = z["risky_H"], z["risky_L"]
    has_loss = np.minimum(rH, rL) < 0
    has_gain = np.maximum(rH, rL) > 0
    mixed = has_loss & has_gain
    loss_only = ~has_gain
    rng = np.random.default_rng(SEED)

    # ================= G1, the loss stratum ==============================
    print("=" * 78)
    print("G1. THE LOSS STRATUM, AND WHAT ITS DATA CAN SUPPORT")
    print("=" * 78)
    n_lp = len(np.unique(pid[loss_only]))
    print("  peterson description   %6d trials over %4d distinct problems"
          % (loss_only.sum(), n_lp))

    # the trap, stated with numbers
    from peterson_parse import PRESS_REPEAT, feats, trials as ptrials  # noqa: E402
    exp_path = os.path.join(HERE, "experience_rows.npz")
    if os.path.exists(exp_path):
        ez = np.load(exp_path)
        eloss = np.maximum(ez["risky_H"], ez["risky_L"]) <= 0
        key = np.round(np.c_[ez["risky_H"], ez["risky_L"], ez["d"], ez["q"]], 4)
        uniq_exp = len({tuple(r) for r in key[eloss]})
        print("  peterson experience    %6d trials over %4d distinct gambles"
              % (int(eloss.sum()), uniq_exp))
        print("  ** the experience arm adds trials on the SAME gambles, so it")
        print("     cannot raise the effective sample for a coordinate term **")
        out["G1_experience_trap"] = {"trials": int(eloss.sum()),
                                     "distinct_gambles": int(uniq_exp)}

    # best estimate the description data supports, problem-clustered
    def loss_q_slope(rows):
        m = rows
        X = np.vstack([eZ[m], sZ[m], q[m] * sZ[m]]).T
        th, _se, info = fit_se(X, y[m])
        return float(th[2]), bool(info["converged"])

    point, _ok = loss_q_slope(loss_only)
    uids = np.unique(pid[loss_only])
    idx = {u: np.where((pid == u) & loss_only)[0] for u in uids}
    est = []
    for _ in range(B_BOOT):
        pick = rng.choice(uids, size=len(uids), replace=True)
        rows = np.concatenate([idx[u] for u in pick])
        m = np.zeros(len(y), bool)
        m[rows] = True
        try:
            v, ok = loss_q_slope(m)
            if ok and np.isfinite(v):
                est.append(v)
        except np.linalg.LinAlgError:
            continue
    est = np.array(est)
    lo, hi = np.percentile(est, [2.5, 97.5])
    print()
    print("  q slope on pure-loss gambles   %+.4f" % point)
    print("  problem-clustered bootstrap    sd %.4f   95%% CI [%+.4f, %+.4f]"
          % (est.std(ddof=1), lo, hi))
    print("  contains zero: %s" % ("YES" if lo <= 0 <= hi else "NO"))
    print()
    print("  DETECTION LIMIT. with %d problems the clustered sd is %.3f, so a"
          % (n_lp, est.std(ddof=1)))
    print("  two-sided test at the conventional level can only detect a slope")
    print("  of about %.2f or larger. The gain-side slope is +0.34." % (2.8 * est.std(ddof=1)))
    print("  ** the mirror-image slope could be anything from zero to the size")
    print("     of the gain-side slope and this corpus could not tell **")
    out["G1_loss_stratum"] = {
        "n_trials": int(loss_only.sum()), "n_problems": int(n_lp),
        "q_slope": point, "boot_sd": float(est.std(ddof=1)),
        "ci": [float(lo), float(hi)], "contains_zero": bool(lo <= 0 <= hi),
        "detectable_slope": float(2.8 * est.std(ddof=1))}

    # ================= G2, the surface, noise-calibrated =================
    print()
    print("=" * 78)
    print("G2. THE FREE SURFACE, FINER, AND CALIBRATED AGAINST CELL NOISE")
    print("=" * 78)
    md, mq, my = d[mixed], q[mixed], y[mixed]
    me, ms, mp = _z(dEV[mixed]), _z(dSD[mixed]), pid[mixed]
    print("  mixed gambles %d trials over %d problems"
          % (mixed.sum(), len(np.unique(mp))))
    print()
    print("    grid   cells   weighted R^2   max resid")
    grids = []
    for nbin, minp in ((5, 25), (6, 20), (8, 12), (10, 8)):
        r = free_surface(md, mq, me, ms, my, nbin, minp, mp)
        if r:
            print("    %2dx%-2d  %5d   %12.3f   %9.2f"
                  % (nbin, nbin, r["cells"], r["r2"], r["max_resid"]))
            grids.append({"grid": nbin, "min_problems": minp,
                          "cells": r["cells"], "r2": r["r2"],
                          "max_resid": r["max_resid"]})
    out["G2_grids"] = grids

    # calibration: what R^2 would the quadratic score if it were TRUE?
    print()
    print("  CALIBRATION. simulate from the FITTED QUADRATIC, re-estimate the")
    print("  free surface, and project. If the quadratic were true this is the")
    print("  R^2 it would score, and the deficit is cell noise rather than")
    print("  missing structure.")
    Xq = np.vstack([me, terms(md, mq) * ms]).T
    thq, _s, _i = fit_se(Xq, my)
    pr = logistic(Xq @ thq)
    sim_r2 = []
    for _ in range(12):
        ysim = (rng.random(len(pr)) < pr).astype(float)
        r = free_surface(md, mq, me, ms, ysim, 5, 25, mp)
        if r:
            sim_r2.append(r["r2"])
    obs = [g for g in grids if g["grid"] == 5][0]["r2"]
    print()
    print("    observed R^2 at 5x5                 %.3f" % obs)
    print("    R^2 if the quadratic were TRUE      %.3f  (mean of %d simulations,"
          % (float(np.mean(sim_r2)), len(sim_r2)))
    print("                                              sd %.3f)" % float(np.std(sim_r2, ddof=1)))
    gap = float(np.mean(sim_r2)) - obs
    print("    deficit attributable to real missing structure   %.3f" % gap)
    print()
    if gap > 3 * float(np.std(sim_r2, ddof=1)):
        print("    ** the quadratic misses real structure, not just noise **")
    else:
        print("    ** the deficit is within simulation noise, so the low R^2 is")
        print("       largely cell estimation error and the quadratic is a")
        print("       better description than the raw number suggested **")
    out["G2_calibration"] = {"observed_r2": obs,
                             "r2_if_quadratic_true": float(np.mean(sim_r2)),
                             "sim_sd": float(np.std(sim_r2, ddof=1)),
                             "deficit": gap,
                             "misses_real_structure": bool(gap > 3 * float(np.std(sim_r2, ddof=1)))}

    # ================= G3, separability ==================================
    print()
    print("=" * 78)
    print("G3. IS THE MODEL SEPARABLE? DOES b_EV DEPEND ON POSITION?")
    print("=" * 78)
    T = terms(md, mq)
    X_sep = np.vstack([me, T * ms]).T                      # b_EV constant
    X_full = np.vstack([T * me, T * ms]).T                 # both vary
    th_s, se_s, _i = fit_se(X_sep, my)
    th_f, se_f, _i = fit_se(X_full, my)
    nll_s = _nll_grad_hess(X_sep, my, th_s)[0]
    nll_f = _nll_grad_hess(X_full, my, th_f)[0]
    print("  separable   parameters %2d   nll %.1f" % (X_sep.shape[1], nll_s))
    print("  full        parameters %2d   nll %.1f" % (X_full.shape[1], nll_f))
    print("  in-sample gain %.1f on %d extra parameters"
          % (nll_s - nll_f, X_full.shape[1] - X_sep.shape[1]))
    print()
    print("  b_EV surface in the full model")
    for i, t in enumerate(TERM_NAMES):
        print("    bEV:%-6s %+.4f +/- %.4f" % (t, th_f[i], se_f[i] * 1.76))
    print()
    print("  do the kappa terms move when b_EV is allowed to vary?")
    print("    term      separable        full")
    for i, t in enumerate(TERM_NAMES):
        print("    %-8s %+.4f         %+.4f" % (t, th_s[1 + i], th_f[6 + i]))

    # held out by problem
    uids = np.unique(mp)
    hs, hf = [], []
    for _ in range(20):
        perm = rng.permutation(uids)
        tr_ids = set(perm[:len(perm) // 2].tolist())
        tr = np.array([p in tr_ids for p in mp])
        for X, acc in ((X_sep, hs), (X_full, hf)):
            th, _i2 = fit(X[tr], my[tr])
            p2 = np.clip(logistic(X[~tr] @ th), 1e-12, 1 - 1e-12)
            acc.append(float(np.sum(my[~tr] * np.log(p2)
                                    + (1 - my[~tr]) * np.log(1 - p2)) / (~tr).sum()))
    hs, hf = np.array(hs), np.array(hf)
    dd = hf - hs
    print()
    print("  HELD OUT by problem, 20 splits")
    print("    separable  %+.6f" % hs.mean())
    print("    full       %+.6f" % hf.mean())
    print("    difference %+.6f +/- %.6f   (%d of 20 splits favour the full model)"
          % (dd.mean(), dd.std(ddof=1) / np.sqrt(20), int((dd > 0).sum())))
    verdict = ("separability is REJECTED, b_EV varies with position"
               if dd.mean() > 2 * dd.std(ddof=1) / np.sqrt(20)
               else "separability SURVIVES out of sample")
    print("    %s" % verdict)
    out["G3_separability"] = {
        "nll_separable": float(nll_s), "nll_full": float(nll_f),
        "insample_gain": float(nll_s - nll_f),
        "bEV_surface": {t: float(th_f[i]) for i, t in enumerate(TERM_NAMES)},
        "bEV_surface_se": {t: float(se_f[i] * 1.76) for i, t in enumerate(TERM_NAMES)},
        "kappa_separable": {t: float(th_s[1 + i]) for i, t in enumerate(TERM_NAMES)},
        "kappa_full": {t: float(th_f[6 + i]) for i, t in enumerate(TERM_NAMES)},
        "heldout_separable": float(hs.mean()), "heldout_full": float(hf.mean()),
        "heldout_diff": float(dd.mean()),
        "splits_favouring_full": int((dd > 0).sum()), "verdict": verdict}

    with open(os.path.join(HERE, "close_gaps.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written close_gaps.json")


if __name__ == "__main__":
    main()
