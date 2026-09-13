#!/usr/bin/env python3
"""EXPLORATORY. Characterising the seam at |d| = 1.

**Not part of any registration and it changes no verdict.**

`refine_structure.py` found the six-term quadratic explains a weighted
`R^2 = 0.361` of a freely estimated kappa surface, with the dominant failure a
jump of `1.29` in kappa across `delta-d = 0.038` at the `|d| = 1` boundary. This
asks what that boundary is and whether the jump is real.

**What `|d| = 1` is.** From `_opt_coords`, `d = (pos - neg) / (pos + neg)` with
`pos` and `neg` the probability-weighted positive and negative parts. So `d = +1`
exactly when `neg = 0`, meaning the option has no loss branch at all, and
`d = -1` exactly when `pos = 0`. **The endpoints of `d` are not a region of the
coordinate, they are a different class of gamble**, and `seam_covariates.py`
checks that correspondence on every row rather than assuming it.

That matters because a coordinate whose endpoint coincides with a categorical
change in the stimulus will show a discontinuity there for reasons that have
nothing to do with geometry, and a smooth model fitted across it will be wrong on
both sides.

Five questions:

    Q1  Is the jump real, or a binning artifact? Estimate kappa in fine strata of
        `1 - |d|` approaching zero and see whether the limit from inside the
        mixed gambles meets the value at the boundary.
    Q2  How big is it, with an interval rather than a point?
    Q3  Is it one seam or two? The gain boundary and the loss boundary are
        different stimuli and need not behave alike.
    Q4  Does the quadratic work INSIDE the regimes? If the free surface is well
        described by six terms once the seam is removed, the seam is the whole
        misspecification. If not, there is more wrong than the seam.
    Q5  Does a regime-separated model beat the pooled one, and by how much?

Standard errors carry the design-effect inflation measured in the confirmatory
run, `sqrt(null_Q_mean / 3)`, because trials are clustered about seventeen to a
problem.

    python seam_analysis.py
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

RESULTS = os.path.join(HERE, "results_stability_v2.json")
MIN_CELL = 300


def _z(x):
    s = x.std()
    return (x - x.mean()) / (s if s > 1e-12 else 1.0)


def fit_design(X, y):
    theta, info = fit(X, y)
    assert info["converged"], "fit did not converge"
    _n, _g, H = _nll_grad_hess(X, y, theta)
    return theta, np.sqrt(np.diag(np.linalg.inv(H))), info


def terms(d, q):
    return np.vstack([np.ones_like(d), d ** 2 + q ** 2, d * q,
                      d, q, d ** 2 - q ** 2])


def kappa_by_group(eZ, sZ, y, group, labels):
    """One free kappa per group, sharing a single bEV. No form imposed."""
    cols = [eZ] + [np.where(group == g, sZ, 0.0) for g in labels]
    th, se, info = fit_design(np.vstack(cols).T, y)
    return th[1:], se[1:], th[0], info


def main():
    with open(RESULTS, encoding="utf-8") as fh:
        infl = float(np.sqrt(json.load(fh)["null_Q_mean"] / 3.0))
    dEV, dSD, d, q, pid, fold, scale, part = load_covariates()
    y = load_outcome()
    eZ, sZ = _z(dEV), _z(dSD)
    z = np.load(os.path.join(HERE, "seam_covariates.npz"))
    rH, rL = z["risky_H"], z["risky_L"]

    has_loss = np.minimum(rH, rL) < 0
    has_gain = np.maximum(rH, rL) > 0
    regime = np.where(~has_loss, "gain_only",
                      np.where(~has_gain, "loss_only", "mixed"))
    print("design-effect inflation on every standard error: %.3f" % infl)
    print("rows %d" % len(y))
    for r in ("gain_only", "mixed", "loss_only"):
        m = regime == r
        print("  %-10s %7d rows, %5d problems, d in [%+.3f, %+.3f]"
              % (r, m.sum(), len(set(pid[m].tolist())),
                 d[m].min() if m.any() else 0, d[m].max() if m.any() else 0))

    out = {"note": "EXPLORATORY, changes no registered verdict",
           "design_effect_inflation": infl}

    # ---- Q1/Q2/Q3: the limit from inside, on each side separately ---------
    print()
    print("Q1-Q3. APPROACHING THE BOUNDARY FROM INSIDE THE MIXED GAMBLES")
    print("  strata of 1 - |d| among mixed gambles, plus the boundary itself")
    edges = [0.0, 0.005, 0.02, 0.05, 0.10, 0.20, 0.40, 1.01]
    for side, sel, bname in (("GAIN side, d > 0", d > 0, "gain_only"),
                             ("LOSS side, d < 0", d < 0, "loss_only")):
        gap = 1.0 - np.abs(d)
        lab, grp = [], np.full(len(y), "none", dtype=object)
        bm = sel & (regime == "mixed")
        for i in range(len(edges) - 1):
            m = bm & (gap > edges[i]) & (gap <= edges[i + 1])
            if m.sum() >= MIN_CELL:
                nm = "mix_%.3f_%.3f" % (edges[i], edges[i + 1])
                grp[m] = nm
                lab.append(nm)
        bd = regime == bname
        if bd.sum() >= MIN_CELL:
            grp[bd] = bname
            lab.append(bname)
        if len(lab) < 2:
            print("  %s: too few rows to stratify" % side)
            continue
        kap, se, bev, info = kappa_by_group(eZ, sZ, y, grp, lab)
        print()
        print("  %s   (bEV %+.4f)" % (side, bev))
        print("    stratum                 n      kappa        se")
        rec = []
        for j, nm in enumerate(lab):
            n = int((grp == nm).sum())
            mark = "   <-- BOUNDARY" if nm == bname else ""
            print("    %-20s %6d   %+8.4f  %7.4f%s"
                  % (nm, n, kap[j], se[j] * infl, mark))
            rec.append({"stratum": nm, "n": n, "kappa": float(kap[j]),
                        "se": float(se[j] * infl)})
        # the jump: nearest mixed stratum against the boundary
        if bname in lab and len(lab) >= 2:
            ib = lab.index(bname)
            near = 0 if ib != 0 else 1
            jump = float(kap[ib] - kap[near])
            sej = float(np.hypot(se[ib], se[near]) * infl)
            print("    jump at the boundary: %+.4f +/- %.4f   (%.1f se)"
                  % (jump, sej, abs(jump) / sej if sej > 0 else float("nan")))
            out[side.split(",")[0].strip().lower().replace(" ", "_")] = {
                "strata": rec, "jump": jump, "jump_se": sej,
                "jump_in_se": float(abs(jump) / sej) if sej > 0 else None}

    # ---- Q4: does the quadratic work inside the regimes? ------------------
    print()
    print("Q4. IS THE QUADRATIC ADEQUATE ONCE THE SEAM IS REMOVED?")
    for tag, m in (("MIXED gambles only", regime == "mixed"),
                   ("ALL rows, for comparison", np.ones(len(y), bool))):
        dm, qm, ym = d[m], q[m], y[m]
        em, sm = _z(dEV[m]), _z(dSD[m])
        de = np.quantile(dm, np.linspace(0, 1, 6))
        qe = np.quantile(qm, np.linspace(0, 1, 6))
        de[0] -= 1e-9; qe[0] -= 1e-9
        cell = (np.clip(np.digitize(dm, de[1:-1]), 0, 4) * 5
                + np.clip(np.digitize(qm, qe[1:-1]), 0, 4))
        keep = [c for c in range(25) if (cell == c).sum() >= MIN_CELL]
        kap, se, bev, _i = kappa_by_group(em, sm, ym, cell, keep)
        se = se * infl
        cd = np.array([dm[cell == c].mean() for c in keep])
        cq = np.array([qm[cell == c].mean() for c in keep])
        T = terms(cd, cq).T
        W = np.diag(1.0 / np.maximum(se, 1e-9) ** 2)
        beta = np.linalg.solve(T.T @ W @ T, T.T @ W @ kap)
        resid = kap - T @ beta
        wm = np.average(kap, weights=np.diag(W))
        ss_tot = float((((kap - wm) ** 2) * np.diag(W)).sum())
        ss_res = float(((resid ** 2) * np.diag(W)).sum())
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        print()
        print("  %s: %d cells, weighted R^2 of the quadratic = %.3f"
              % (tag, len(keep), r2))
        print("    largest standardised residual %.2f"
              % float(np.max(np.abs(resid / np.maximum(se, 1e-9)))))
        print("    projected d*q %+.4f    d %+.4f    d2-q2 %+.4f"
              % (beta[TERM_NAMES.index("d*q")], beta[TERM_NAMES.index("d")],
                 beta[TERM_NAMES.index("d2-q2")]))
        out["quadratic_" + ("mixed" if "MIXED" in tag else "all")] = {
            "cells": len(keep), "weighted_r2": float(r2),
            "max_abs_std_resid": float(np.max(np.abs(resid / np.maximum(se, 1e-9)))),
            "projection": {t: float(beta[i]) for i, t in enumerate(TERM_NAMES)}}

    # ---- Q5: regime-separated model against the pooled one ----------------
    #
    # Inside an unmixed regime `d` is identically +/-1, so all six symmetry terms
    # collapse onto the span {1, q, q^2}: `d` becomes a constant, `d*q` becomes
    # +/-q, `d^2+q^2` becomes 1+q^2 and `d^2-q^2` becomes 1-q^2. Handing the full
    # basis to those rows gives a singular Hessian, which is what a first version
    # of this script did. The reduced basis is the identified one and using it is
    # not a simplification, it is the only thing the regime can support.
    print()
    print("Q5. A REGIME-SEPARATED MODEL AGAINST THE POOLED ONE")
    Xp = np.vstack([eZ, terms(d, q) * sZ]).T
    tp, sep, _ = fit_design(Xp, y)
    nll_p = _nll_grad_hess(Xp, y, tp)[0]

    cols, names = [eZ], ["bEV"]
    for r in ("mixed", "gain_only", "loss_only"):
        m = (regime == r).astype(float)
        if m.sum() < MIN_CELL:
            continue
        if r == "mixed":
            basis = [(t, terms(d, q)[i]) for i, t in enumerate(TERM_NAMES)]
        else:
            basis = [("1", np.ones_like(q)), ("q", q), ("q2", q ** 2)]
        for nm, col in basis:
            cols.append(col * sZ * m)
            names.append("%s:%s" % (r, nm))
    Xr = np.vstack(cols).T
    tr, ser, _ = fit_design(Xr, y)
    nll_r = _nll_grad_hess(Xr, y, tr)[0]
    dfree = Xr.shape[1] - Xp.shape[1]
    print("  pooled six-term      parameters %2d   nll %.1f" % (Xp.shape[1], nll_p))
    print("  regime-separated     parameters %2d   nll %.1f" % (Xr.shape[1], nll_r))
    print("  log-likelihood gain %.1f on %d extra parameters"
          % (nll_p - nll_r, dfree))
    print()
    print("  regime-separated coefficients")
    for j2, nm in enumerate(names):
        if nm == "bEV":
            continue
        print("    %-22s %+.4f +/- %.4f" % (nm, tr[j2], ser[j2] * infl))

    # what kappa looks like inside each unmixed regime, freely in q
    print()
    print("  kappa inside each regime, free in q, no form imposed")
    for r in ("gain_only", "loss_only"):
        m = regime == r
        if m.sum() < MIN_CELL:
            continue
        qe = np.quantile(q[m], np.linspace(0, 1, 6))
        qe[0] -= 1e-9
        bins = np.clip(np.digitize(q, qe[1:-1]), 0, 4)
        grp = np.where(m, np.array(["%s_q%d" % (r, b) for b in bins]), "none")
        lab = [g for g in sorted(set(grp.tolist())) if g != "none"
               and (grp == g).sum() >= MIN_CELL]
        kap, se2, bev2, _i = kappa_by_group(eZ, sZ, y, grp, lab)
        for j3, nm in enumerate(lab):
            mm = grp == nm
            print("    %-16s n %6d   mean q %+.3f   kappa %+.4f +/- %.4f"
                  % (nm, mm.sum(), q[mm].mean(), kap[j3], se2[j3] * infl))
        out["kappa_in_" + r] = [
            {"stratum": nm, "n": int((grp == nm).sum()),
             "mean_q": float(q[grp == nm].mean()),
             "kappa": float(kap[j3]), "se": float(se2[j3] * infl)}
            for j3, nm in enumerate(lab)]

    out["model_comparison"] = {
        "pooled_params": int(Xp.shape[1]), "pooled_nll": float(nll_p),
        "regime_params": int(Xr.shape[1]), "regime_nll": float(nll_r),
        "loglik_gain": float(nll_p - nll_r), "extra_params": int(dfree),
        "regime_coefficients": {names[k]: float(tr[k]) for k in range(1, len(names))},
        "regime_se_inflated": {names[k]: float(ser[k] * infl)
                               for k in range(1, len(names))}}

    with open(os.path.join(HERE, "seam_analysis.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written seam_analysis.json")


if __name__ == "__main__":
    main()
