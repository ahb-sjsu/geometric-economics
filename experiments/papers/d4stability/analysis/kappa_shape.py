#!/usr/bin/env python3
"""EXPLORATORY. What shape is the kappa surface, without assuming a group first?

**This is not part of `prereg-d4stability-v1` and changes no verdict in it.** The
registration tested one coefficient, the `d*q` chirality, because that is what
the D4 question is about. The prior question is what the surface actually looks
like, and nobody had measured that.

The risk sensitivity modifier is

    kappa(d, q) = c0 + c1 (d^2 + q^2) + c2 (d q) + c3 d + c4 q + c5 (d^2 - q^2)

whose terms are the symmetry-adapted pieces a square's symmetry group supplies:
an isotropic part, a chirality that a ninety degree rotation sign-flips, a linear
pair that no rotation preserves, and a term that tells the two axes apart.
Reporting a coefficient tells you little, because the terms are not on a common
scale and the data does not cover the plane evenly.

So the surface is decomposed **over the empirical distribution of (d, q) in the
corpus**. Each term's share is the variance it contributes to the fitted kappa at
the points the data actually occupies, with the terms orthogonalised in that
measure by Gram-Schmidt so the shares sum to the whole and none is double
counted. A term that is large where there is no data counts for nothing, which is
the correct behaviour and is not what a table of coefficients gives you.

Corners and interior are reported separately because that is the distinction the
whole line has been arguing about.

**Standard errors are inflated by the measured design effect.** The trials are
clustered about seventeen to a problem and a trial-level logistic likelihood
cannot see that. `prereg-d4stability-v1` measured the resulting inflation: its
random-split null on Cochran's Q had a mean of 13.015 where a correctly specified
model gives 3, so the standard errors are understated by about sqrt(13.015/3).
Every interval here is widened by that factor and it is printed.

    python kappa_shape.py
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

from kappa_mle import TERM_NAMES, _nll_grad_hess, design, fit  # noqa: E402
from stability_rows import load_covariates, load_outcome  # noqa: E402

NULL_Q_MEAN = 13.014963  # from results_stability_v1.json, measured not assumed
DF = 3.0


def _z(x):
    s = x.std()
    return (x - x.mean()) / (s if s > 1e-12 else 1.0)


def terms(d, q):
    return np.vstack([np.ones_like(d), d ** 2 + q ** 2, d * q,
                      d, q, d ** 2 - q ** 2])


def fit_all(dEV, dSD, d, q, y):
    X = design(_z(dEV), _z(dSD), d, q)
    theta, info = fit(X, y)
    _n, _g, H = _nll_grad_hess(X, y, theta)
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    return theta, se, info


def shares(theta, d, q, mask=None):
    """Variance share of each kappa term over the empirical (d, q) measure.

    The six term columns are correlated on real data, so raw variances would sum
    to more than the whole. They are orthogonalised in the data measure, in the
    listed order, and the constant is removed first because a constant carries no
    variance and would otherwise absorb the mean.
    """
    T = terms(d, q)
    if mask is not None:
        T = T[:, mask]
    coef = theta[1:]
    contrib = T * coef[:, None]              # 6 by n
    total = (contrib.sum(axis=0)).var()

    basis, out = [], {}
    for i in range(1, 6):                    # skip the constant, index 0
        v = contrib[i] - contrib[i].mean()
        for b in basis:
            v = v - (v @ b) * b
        n = np.linalg.norm(v)
        if n > 1e-12:
            basis.append(v / n)
        out[TERM_NAMES[i]] = float((v.var()) / total) if total > 0 else 0.0
    out["_total_var"] = float(total)
    return out


def describe(tag, theta, se, d, q, infl):
    print()
    print("=" * 78)
    print(tag)
    print("=" * 78)
    print("  bEV  %+.4f" % theta[0])
    print()
    print("  term       coefficient    se (inflated)    range over [-1,1]^2")
    for i, t in enumerate(TERM_NAMES):
        c = theta[1 + i]
        s = se[1 + i] * infl
        rng = {"const": 0.0, "d2+q2": 2.0, "d*q": 2.0,
               "d": 2.0, "q": 2.0, "d2-q2": 2.0}[t] * abs(c)
        star = "  <-- chirality" if t == "d*q" else ""
        print("  %-9s  %+9.4f     +/- %.4f        %6.3f%s" % (t, c, s, rng, star))

    for name, m in (("ALL", None),
                    ("interior |d| < 0.9", np.abs(d) < 0.9),
                    ("corners  |d| >= 0.9", np.abs(d) >= 0.9)):
        sh = shares(theta, d, q, m)
        n = len(d) if m is None else int(m.sum())
        print()
        print("  variance share of kappa over the data, %s (n=%d)" % (name, n))
        items = [(k, v) for k, v in sh.items() if not k.startswith("_")]
        for k, v in sorted(items, key=lambda kv: -kv[1]):
            bar = "#" * int(round(v * 50))
            print("    %-8s %6.1f%%  %s" % (k, 100 * v, bar))


def main():
    infl = float(np.sqrt(NULL_Q_MEAN / DF))
    print("design-effect inflation applied to every standard error: %.3f" % infl)
    print("(from the measured random-split null mean Q of %.3f against %g)"
          % (NULL_Q_MEAN, DF))

    dEV, dSD, d, q, pid, fold_of_problem, scale, part = load_covariates()
    y = load_outcome()
    theta, se, info = fit_all(dEV, dSD, d, q, y)
    assert info["converged"], "fit did not converge"
    describe("peterson2021using, 95,748 individual description choices",
             theta, se, d, q, infl)

    out = {
        "source": "EXPLORATORY, not part of prereg-d4stability-v1",
        "design_effect_inflation": infl,
        "bEV": float(theta[0]),
        "coefficients": {t: float(theta[1 + i]) for i, t in enumerate(TERM_NAMES)},
        "se_inflated": {t: float(se[1 + i] * infl) for i, t in enumerate(TERM_NAMES)},
        "shares_all": shares(theta, d, q, None),
        "shares_interior": shares(theta, d, q, np.abs(d) < 0.9),
        "shares_corners": shares(theta, d, q, np.abs(d) >= 0.9),
        "n_trials": int(len(y)),
    }
    with open(os.path.join(HERE, "kappa_shape.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written kappa_shape.json")


if __name__ == "__main__":
    main()
