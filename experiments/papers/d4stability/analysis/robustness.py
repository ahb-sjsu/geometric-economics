#!/usr/bin/env python3
"""EXPLORATORY. Held-out validation, model form, and individual heterogeneity.

**Not part of any registration and it changes no verdict.**

Three checks that a claimed structure has to survive, and that nothing so far has
put it through.

    A  HELD OUT. Regime separation buys 195.8 log-likelihood units in sample.
       In-sample gain on 6 extra parameters is not evidence; a term that is real
       should PAY out of sample. Splits are by PROBLEM, never by trial, because
       trials inside a problem are not independent and a trial-level split leaks
       the answer across the fold boundary.

    B  MODEL FORM. Does the conclusion depend on having chosen the standard
       deviation as the risk measure and the logit as the link? A structure that
       evaporates under variance, range or semi-deviation was a property of the
       summary statistic. Five risk measures, two links.

    C  INDIVIDUAL HETEROGENEITY. Aggregation can manufacture curvature no person
       has. Participants are split at random into halves and the fit repeated, so
       a structure that exists only in the aggregate shows up as disagreement
       between halves.

Every standard error here is problem-clustered by the factor measured in
`cluster_bootstrap.py`, 1.76 on this corpus, because the coordinate is a property
of the problem and not of the trial.

    python robustness.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.abspath(os.path.join(HERE, "..", "..", "d4interior", "analysis"))
sys.path.insert(0, HERE)
sys.path.insert(0, V3)

from kappa_mle import TERM_NAMES, _nll_grad_hess, fit  # noqa: E402
from stability_rows_v2 import load_covariates, load_outcome  # noqa: E402

CLUSTER_INFL = 1.76        # measured in cluster_bootstrap.py on this corpus
SEED = 20260913
N_SPLITS = 20
IDQ = TERM_NAMES.index("d*q")
ID2 = TERM_NAMES.index("d2-q2")


def _z(x):
    s = x.std()
    return (x - x.mean()) / (s if s > 1e-12 else 1.0)


def terms(d, q):
    return np.vstack([np.ones_like(d), d ** 2 + q ** 2, d * q,
                      d, q, d ** 2 - q ** 2])


def logistic(lin):
    return np.where(lin >= 0, 1.0 / (1.0 + np.exp(-np.clip(lin, -700, 700))),
                    np.exp(np.clip(lin, -700, 0)) / (1.0 + np.exp(np.clip(lin, -700, 0))))


def fit_se(X, y):
    th, info = fit(X, y)
    _n, _g, H = _nll_grad_hess(X, y, th)
    try:
        se = np.sqrt(np.diag(np.linalg.inv(H)))
    except np.linalg.LinAlgError:
        se = np.full(len(th), np.nan)
    return th, se, info


def heldout_ll(Xtr, ytr, Xte, yte):
    th, _i = fit(Xtr, ytr)
    p = np.clip(logistic(Xte @ th), 1e-12, 1 - 1e-12)
    return float(np.sum(yte * np.log(p) + (1 - yte) * np.log(1 - p)) / len(yte))


def designs(d, q, eZ, sZ, regime):
    ev_only = np.vstack([eZ]).T
    pooled = np.vstack([eZ, terms(d, q) * sZ]).T
    cols = [eZ]
    for r in ("mixed", "gain_only", "loss_only"):
        m = (regime == r).astype(float)
        basis = ([terms(d, q)[i] for i in range(6)] if r == "mixed"
                 else [np.ones_like(q), q, q ** 2])
        for col in basis:
            cols.append(col * sZ * m)
    return {"EV only": ev_only, "pooled six-term": pooled,
            "regime-separated": np.vstack(cols).T}


def main():
    dEV, dSD, d, q, pid, fold, scale, part = load_covariates()
    y = load_outcome()
    z = np.load(os.path.join(HERE, "seam_covariates.npz"))
    rH, rp, rL = z["risky_H"], z["risky_p"], z["risky_L"]
    sH, sp, sL = z["safe_H"], z["safe_p"], z["safe_L"]
    has_loss = np.minimum(rH, rL) < 0
    has_gain = np.maximum(rH, rL) > 0
    regime = np.where(~has_loss, "gain_only",
                      np.where(~has_gain, "loss_only", "mixed"))
    eZ, sZ = _z(dEV), _z(dSD)
    out = {"note": "EXPLORATORY, changes no registered verdict",
           "cluster_inflation": CLUSTER_INFL}

    # ---------------- A. held out, split by PROBLEM ------------------------
    print("=" * 76)
    print("A. HELD-OUT PREDICTION, splits by PROBLEM not by trial")
    print("=" * 76)
    rng = np.random.default_rng(SEED)
    uids = np.unique(pid)
    D = designs(d, q, eZ, sZ, regime)
    acc = {k: [] for k in D}
    for s in range(N_SPLITS):
        perm = rng.permutation(uids)
        tr_ids = set(perm[:len(perm) // 2].tolist())
        tr = np.array([p in tr_ids for p in pid])
        for k, X in D.items():
            acc[k].append(heldout_ll(X[tr], y[tr], X[~tr], y[~tr]))
    print("  mean held-out log-likelihood per trial over %d problem splits" % N_SPLITS)
    base = None
    for k in D:
        m = float(np.mean(acc[k]))
        se = float(np.std(acc[k], ddof=1) / np.sqrt(N_SPLITS))
        if base is None:
            base = m
        print("    %-20s %+.6f +/- %.6f    gain over EV only %+.6f"
              % (k, m, se, m - base))
    d_pool = np.array(acc["pooled six-term"]) - np.array(acc["EV only"])
    d_reg = np.array(acc["regime-separated"]) - np.array(acc["pooled six-term"])
    print()
    print("    paired across splits:")
    print("      six-term over EV only        %+.6f +/- %.6f  (%d of %d splits positive)"
          % (d_pool.mean(), d_pool.std(ddof=1) / np.sqrt(N_SPLITS),
             int((d_pool > 0).sum()), N_SPLITS))
    print("      regime-separated over pooled %+.6f +/- %.6f  (%d of %d splits positive)"
          % (d_reg.mean(), d_reg.std(ddof=1) / np.sqrt(N_SPLITS),
             int((d_reg > 0).sum()), N_SPLITS))
    out["heldout"] = {k: {"mean": float(np.mean(v)),
                          "se": float(np.std(v, ddof=1) / np.sqrt(N_SPLITS))}
                      for k, v in acc.items()}
    out["heldout_paired"] = {
        "six_term_over_ev": {"mean": float(d_pool.mean()),
                             "n_positive": int((d_pool > 0).sum())},
        "regime_over_pooled": {"mean": float(d_reg.mean()),
                               "n_positive": int((d_reg > 0).sum())}}

    # ---------------- B. model form ----------------------------------------
    print()
    print("=" * 76)
    print("B. MODEL FORM: five risk measures, two links")
    print("=" * 76)

    def risk(H, p, L, kind):
        ev = p * H + (1 - p) * L
        var = p * (H - ev) ** 2 + (1 - p) * (L - ev) ** 2
        if kind == "sd":
            return np.sqrt(np.maximum(var, 0))
        if kind == "variance":
            return var
        if kind == "range":
            return np.abs(H - L)
        if kind == "semideviation":
            dn = p * np.minimum(H - ev, 0) ** 2 + (1 - p) * np.minimum(L - ev, 0) ** 2
            return np.sqrt(np.maximum(dn, 0))
        if kind == "gini":
            return 2 * p * (1 - p) * np.abs(H - L)
        raise ValueError(kind)

    mixed = regime == "mixed"
    print("  chirality and d2-q2 INSIDE MIXED GAMBLES, se x %.2f for clustering"
          % CLUSTER_INFL)
    print("    risk measure     link      d*q                d2-q2")
    rows = {}
    for kind in ("sd", "variance", "range", "semideviation", "gini"):
        dr = risk(rH, rp, rL, kind) - risk(sH, sp, sL, kind)
        if not np.all(dr[mixed] != 0):
            print("    %-15s skipped, zero risk difference on some rows" % kind)
            continue
        for link in ("logit",):
            X = np.vstack([_z(dEV[mixed]),
                           terms(d[mixed], q[mixed]) * _z(dr[mixed])]).T
            th, se, info = fit_se(X, y[mixed])
            a, b = th[1 + IDQ], th[1 + ID2]
            sa, sb = se[1 + IDQ] * CLUSTER_INFL, se[1 + ID2] * CLUSTER_INFL
            print("    %-15s  %-7s %+.4f +/- %.4f   %+.4f +/- %.4f"
                  % (kind, link, a, sa, b, sb))
            rows["%s_%s" % (kind, link)] = {
                "dq": float(a), "dq_se": float(sa),
                "d2q2": float(b), "d2q2_se": float(sb)}
    # probit on the standard measure, via a scaled logit approximation is not
    # honest, so fit the probit likelihood directly with a simple Newton
    from scipy.optimize import minimize
    from scipy.stats import norm
    Xp = np.vstack([_z(dEV[mixed]), terms(d[mixed], q[mixed]) * _z(dSD[mixed])]).T
    ym = y[mixed]

    def nll(th):
        lin = np.clip(Xp @ th, -8, 8)
        p = np.clip(norm.cdf(lin), 1e-12, 1 - 1e-12)
        return -np.sum(ym * np.log(p) + (1 - ym) * np.log(1 - p))

    r = minimize(nll, np.zeros(Xp.shape[1]), method="L-BFGS-B")
    print("    %-15s  %-7s %+.4f              %+.4f   (scaled to logit: %+.4f)"
          % ("sd", "probit", r.x[1 + IDQ], r.x[1 + ID2], r.x[1 + IDQ] * 1.6))
    rows["sd_probit"] = {"dq": float(r.x[1 + IDQ]), "d2q2": float(r.x[1 + ID2]),
                         "dq_logit_scaled": float(r.x[1 + IDQ] * 1.6)}
    out["model_form"] = rows

    # ---------------- C. individual heterogeneity --------------------------
    print()
    print("=" * 76)
    print("C. INDIVIDUAL HETEROGENEITY: random halves of PARTICIPANTS")
    print("=" * 76)
    rng2 = np.random.default_rng(SEED + 1)
    parts = np.unique(part)
    halves = []
    for s in range(6):
        pm = rng2.permutation(parts)
        a_ids = set(pm[:len(pm) // 2].tolist())
        sel = np.array([p in a_ids for p in part])
        for which, mm in (("A", sel & mixed), ("B", (~sel) & mixed)):
            X = np.vstack([_z(dEV[mm]), terms(d[mm], q[mm]) * _z(dSD[mm])]).T
            th, se, info = fit_se(X, y[mm])
            halves.append({"split": s, "half": which, "n": int(mm.sum()),
                           "dq": float(th[1 + IDQ]),
                           "dq_se": float(se[1 + IDQ] * CLUSTER_INFL),
                           "d2q2": float(th[1 + ID2]),
                           "d2q2_se": float(se[1 + ID2] * CLUSTER_INFL)})
    print("  d*q and d2-q2 inside mixed gambles, per participant half")
    for h in halves:
        print("    split %d half %s  n %6d   d*q %+.4f +/- %.4f   d2-q2 %+.4f +/- %.4f"
              % (h["split"], h["half"], h["n"], h["dq"], h["dq_se"],
                 h["d2q2"], h["d2q2_se"]))
    dq = np.array([h["dq"] for h in halves])
    d2 = np.array([h["d2q2"] for h in halves])
    print()
    print("    d*q   across 12 halves: mean %+.4f  sd %.4f  range [%+.4f, %+.4f]"
          % (dq.mean(), dq.std(ddof=1), dq.min(), dq.max()))
    print("    d2-q2 across 12 halves: mean %+.4f  sd %.4f  range [%+.4f, %+.4f]"
          % (d2.mean(), d2.std(ddof=1), d2.min(), d2.max()))
    out["participant_halves"] = halves

    with open(os.path.join(HERE, "robustness.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written robustness.json")


if __name__ == "__main__":
    main()
