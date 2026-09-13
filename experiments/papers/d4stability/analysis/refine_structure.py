#!/usr/bin/env python3
"""EXPLORATORY. Is the kappa surface real, and is the quadratic basis inventing it?

**Not part of any registration and it changes no verdict.** `prereg-d4stability-v2`
tested one thing, whether the chirality holds still across a scale split, and it
does not: `+0.228, -0.261, -0.422, -0.500` from the smallest stakes to the
largest, Cochran's Q of 103 against a null mean of 9.9, permutation `p = 0.0005`.

That result is what motivates everything here. The coordinate `(d, q)` is exactly
invariant under positive scaling of both outcomes, checked 191,496 times in the
sealed row builder. **A chirality that moves monotonically with stake size is
therefore moving with a variable the coordinate cannot represent, which is
misspecification and not instability.** Three questions follow.

**A. Is the structure an artifact of the basis?** Everything so far assumes
kappa is a quadratic in `(d, q)`. That basis could be manufacturing the
chirality. Here kappa is estimated **freely, one coefficient per cell of the
(d, q) plane**, with no functional form imposed, and the resulting surface is
then projected onto the six symmetry terms. If the chirality survives without
having been written into the model, it is a property of the data. The residual of
that projection says how much of the free surface the quadratic misses.

**B. Are the two small terms actually absent?** `q` and `d^2-q^2` came out near
zero, and "not significant" is not "absent". They are tested here against a
negligibility band, so the claim can fail.

**The band is anchored outside this corpus**, because the point estimates have
already been seen and a band chosen after the fact would be worthless. CPC18's
published interior coefficients, quoted in `prereg-d4gate-v1`, are `q = +0.144`
and `d^2-q^2 = +0.340`. The band is one third of the smaller of those, so
`|c| < 0.048` counts as negligible. A term is declared absent only if its whole
confidence interval lies inside that band, which is an equivalence test and not a
failed significance test.

**C. Does absolute scale belong in the model?** If the chirality depends on stake
size then `kappa` needs a scale term, and the right question is whether adding one
absorbs the fold heterogeneity that `prereg-d4stability-v2` found. That is the
model refinement the result demands.

Standard errors are inflated by the design effect measured in the confirmatory
run, `sqrt(null_Q_mean / 3)`, because trials are clustered about seventeen to a
problem and a trial-level logistic likelihood cannot see that.

    python refine_structure.py
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
BAND = 0.048          # externally anchored, see the docstring
MIN_CELL = 400        # trials required before a cell gets its own coefficient


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


def main():
    with open(RESULTS, encoding="utf-8") as fh:
        res = json.load(fh)
    infl = float(np.sqrt(res["null_Q_mean"] / 3.0))
    print("design-effect inflation on every standard error: %.3f" % infl)
    print("(measured null mean Q %.3f against the 3 of chi-square on 3 df)"
          % res["null_Q_mean"])

    dEV, dSD, d, q, pid, fold_of_problem, scale, part = load_covariates()
    y = load_outcome()
    eZ, sZ = _z(dEV), _z(dSD)
    print("rows %d, problems %d" % (len(y), len(fold_of_problem)))

    # ---------------- the parametric fit, for reference --------------------
    Xp = np.vstack([eZ, terms(d, q) * sZ]).T
    tp, sep, _ = fit_design(Xp, y)
    print()
    print("PARAMETRIC, the model the registration used")
    print("  bEV    %+.4f +/- %.4f" % (tp[0], sep[0] * infl))
    for i, t in enumerate(TERM_NAMES):
        print("  %-6s %+.4f +/- %.4f" % (t, tp[1 + i], sep[1 + i] * infl))

    # ---------------- A. free surface, no functional form ------------------
    de = np.quantile(d, np.linspace(0, 1, 6))
    qe = np.quantile(q, np.linspace(0, 1, 6))
    de[0] -= 1e-9; qe[0] -= 1e-9
    di = np.clip(np.digitize(d, de[1:-1]), 0, 4)
    qi = np.clip(np.digitize(q, qe[1:-1]), 0, 4)
    cell = di * 5 + qi
    keep = [c for c in range(25) if (cell == c).sum() >= MIN_CELL]
    cols = [eZ] + [np.where(cell == c, sZ, 0.0) for c in keep]
    Xf = np.vstack(cols).T
    tf, sef, _ = fit_design(Xf, y)
    kap = tf[1:]
    kse = sef[1:] * infl
    cd = np.array([d[cell == c].mean() for c in keep])
    cq = np.array([q[cell == c].mean() for c in keep])
    cn = np.array([int((cell == c).sum()) for c in keep])

    print()
    print("A. FREE SURFACE, one kappa per cell, no functional form imposed")
    print("   %d cells of 25 kept at n >= %d" % (len(keep), MIN_CELL))
    print("   cell   mean d   mean q        n     kappa       se")
    for j, c in enumerate(keep):
        print("   %4d   %+6.3f   %+6.3f  %7d  %+8.4f  %7.4f"
              % (c, cd[j], cq[j], cn[j], kap[j], kse[j]))

    # project the free surface onto the six symmetry terms, weighted by
    # precision, and see what the quadratic form misses
    T = terms(cd, cq).T
    W = np.diag(1.0 / np.maximum(kse, 1e-9) ** 2)
    beta = np.linalg.solve(T.T @ W @ T, T.T @ W @ kap)
    resid = kap - T @ beta
    ss_tot = float(((kap - np.average(kap, weights=np.diag(W))) ** 2 * np.diag(W)).sum())
    ss_res = float((resid ** 2 * np.diag(W)).sum())
    print()
    print("   projection of the FREE surface onto the six symmetry terms")
    for i, t in enumerate(TERM_NAMES):
        flag = "   <-- chirality" if t == "d*q" else ""
        print("     %-6s %+.4f   (parametric %+.4f)%s"
              % (t, beta[i], tp[1 + i], flag))
    print("     weighted R^2 of the quadratic against the free surface: %.3f"
          % (1 - ss_res / ss_tot if ss_tot > 0 else float("nan")))
    print("     largest standardised residual cell: %.2f"
          % float(np.max(np.abs(resid / np.maximum(kse, 1e-9)))))

    # ---------------- B. equivalence on the two small terms ----------------
    print()
    print("B. EQUIVALENCE against a band of |c| < %.3f, anchored on CPC18" % BAND)
    eq = {}
    for t in ("q", "d2-q2", "d2+q2", "d*q", "d"):
        i = TERM_NAMES.index(t)
        c, s = tp[1 + i], sep[1 + i] * infl
        lo, hi = c - 1.96 * s, c + 1.96 * s
        inside = (lo > -BAND) and (hi < BAND)
        eq[t] = {"coef": float(c), "se": float(s), "ci": [float(lo), float(hi)],
                 "absent": bool(inside)}
        print("   %-6s %+.4f  CI [%+.4f, %+.4f]  -> %s"
              % (t, c, lo, hi,
                 "ABSENT, whole interval inside the band" if inside
                 else "NOT SHOWN ABSENT, interval leaves the band"))

    # ---------------- C. does absolute scale belong in kappa? --------------
    ls = _z(np.log10(scale))
    Xs = np.vstack([eZ, terms(d, q) * sZ, ls * sZ, (d * q) * ls * sZ]).T
    ts, ses, _ = fit_design(Xs, y)
    print()
    print("C. ADDING ABSOLUTE SCALE TO KAPPA")
    print("   the coordinate (d, q) is scale-invariant by construction, so a")
    print("   scale term is testing for structure the coordinate cannot carry")
    print("   scale            %+.4f +/- %.4f" % (ts[7], ses[7] * infl))
    print("   (d*q) x scale    %+.4f +/- %.4f   <-- does the chirality depend on stakes?"
          % (ts[8], ses[8] * infl))
    print("   d*q  base        %+.4f +/- %.4f  (was %+.4f without the scale terms)"
          % (ts[3], ses[3] * infl, tp[3]))
    ll_gain = float(_nll_grad_hess(Xp, y, tp)[0] - _nll_grad_hess(Xs, y, ts)[0])
    print("   log-likelihood gain from the two scale terms: %.1f on 2 df" % ll_gain)

    out = {
        "note": "EXPLORATORY, not part of prereg-d4stability-v2",
        "design_effect_inflation": infl,
        "parametric": {t: float(tp[1 + i]) for i, t in enumerate(TERM_NAMES)},
        "parametric_se_inflated": {t: float(sep[1 + i] * infl)
                                   for i, t in enumerate(TERM_NAMES)},
        "bEV": float(tp[0]),
        "free_surface": {"cells_kept": len(keep), "min_cell": MIN_CELL,
                         "kappa": [float(x) for x in kap],
                         "se": [float(x) for x in kse],
                         "mean_d": [float(x) for x in cd],
                         "mean_q": [float(x) for x in cq],
                         "n": [int(x) for x in cn]},
        "projection_of_free_surface": {t: float(beta[i])
                                       for i, t in enumerate(TERM_NAMES)},
        "quadratic_weighted_r2": float(1 - ss_res / ss_tot) if ss_tot > 0 else None,
        "equivalence_band": BAND,
        "equivalence": eq,
        "scale_terms": {"scale": float(ts[7]), "dq_x_scale": float(ts[8]),
                        "se_scale": float(ses[7] * infl),
                        "se_dq_x_scale": float(ses[8] * infl),
                        "loglik_gain_2df": ll_gain},
    }
    with open(os.path.join(HERE, "refine_structure.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written refine_structure.json")


if __name__ == "__main__":
    main()
