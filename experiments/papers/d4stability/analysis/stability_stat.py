#!/usr/bin/env python3
"""The stability statistic and its random-split null.

The question is whether the interior chirality `c2` is a stable quantity inside
one corpus, or whether it moves with stimulus composition by as much as it moved
between CPC18 (`+0.4438`) and choices13k (`−0.1216`).

**Why a null is required.** Any split produces some spread in `c2`, because each
fold is smaller and therefore noisier than the whole. A raw spread is not
evidence of anything. Only spread in excess of what an uninformative split of the
same fold sizes would give is evidence that composition matters. So the statistic
is compared against random partitions of the problems into folds of exactly the
observed sizes, refitting every fold every time.

**Why the statistic is studentised, which a first version was not.** The first
version of this module used the plain standard deviation of the four fold
estimates. Its power simulation put the size of the test at **0.110 against a
nominal 0.05**, and the reason is structural rather than accidental. The scale
folds differ in composition, so they differ in how precisely `c2` can be
estimated in them, while a random fold always has average composition and so
average precision. Under a perfectly constant `c2` the real split therefore
spreads further than the null does, and a test built on the raw spread rejects
more than twice as often as it should.

Dividing each fold's deviation by its own standard error removes exactly that
asymmetry. The statistic is Cochran's Q,

    Q = sum_f (c2_f - c2_bar)^2 / se_f^2 ,  c2_bar the precision-weighted mean,

which is a chi-square on three degrees of freedom under a constant `c2` when the
standard errors are right. The permutation null is kept rather than leaning on
that asymptotic form, because the trials are clustered inside problems and the
logistic standard errors understate the clustering. Clustering inflates Q for the
observed split and for every permutation alike, since problems are assigned to
folds whole, so the permutation p-value stays calibrated while the studentisation
does the job of removing the precision differences.

**Why folds are z-scored separately, which is not a convenience.** In a logistic
model the linear predictor is `b0*dEV + kappa(d,q)*dSD`. Multiplying `dSD` by any
positive constant divides every kappa coefficient by that same constant, so the
kappa coefficients are identified only up to the scale of `dSD`. Folds built from
gambles of different stake sizes have `dSD` on different scales, and comparing
their raw coefficients would be comparing units, not chiralities. Standardising
`dEV` and `dSD` within each fold fixes that scale at unity in every fold and is
the normalisation that makes fold coefficients comparable at all. The same
standardisation is applied inside the null, so the comparison is exact.

`c2` is `theta[3]` in the design of `kappa_mle.design`, whose columns are
`dEV` then the six kappa terms times `dSD` in the order of `TERM_NAMES`.
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.abspath(os.path.join(HERE, "..", "..", "d4interior", "analysis"))
sys.path.insert(0, V3)

from kappa_mle import TERM_NAMES, _nll_grad_hess, design, fit  # noqa: E402

C2_INDEX = 1 + TERM_NAMES.index("d*q")
assert C2_INDEX == 3, "coefficient layout is not what this module assumes"


def _z(x):
    s = x.std()
    return (x - x.mean()) / (s if s > 1e-12 else 1.0)


def fit_fold(dEV, dSD, d, q, y, tol=1e-9):
    """Standardise within the fold, solve the convex problem, return
    `(c2, se, info)`.

    The standardisation is inside this function so that no caller can compare
    coefficients fitted on differently scaled columns. The standard error comes
    from the inverse of the Hessian at the optimum, which is the observed
    information for this model, and it is what makes the fold estimates
    comparable when the folds differ in precision.
    """
    X = design(_z(dEV), _z(dSD), d, q)
    theta, info = fit(X, y, tol=tol)
    _nll, _g, H = _nll_grad_hess(X, y, theta)
    cov = np.linalg.inv(H)
    var = float(cov[C2_INDEX, C2_INDEX])
    info["se_c2"] = float(np.sqrt(var)) if var > 0 else float("inf")
    return float(theta[C2_INDEX]), info["se_c2"], info


def fold_estimates(rows, fold_of_problem, n_folds):
    """`c2` and its standard error in each fold. `rows` is
    (dEV, dSD, d, q, y, pid)."""
    dEV, dSD, d, q, y, pid = rows
    fold = fold_of_problem[pid]
    c2s, ses, infos = [], [], []
    for f in range(n_folds):
        m = fold == f
        c2, se, info = fit_fold(dEV[m], dSD[m], d[m], q[m], y[m])
        c2s.append(c2)
        ses.append(se)
        infos.append(info)
    return np.array(c2s), np.array(ses), infos


def heterogeneity(c2s, ses):
    """Cochran's Q, the registered statistic.

    Each fold's deviation from the precision-weighted mean is measured in units
    of that fold's own standard error, so a fold in which `c2` is poorly
    determined cannot contribute spread merely by being poorly determined.
    """
    w = 1.0 / np.maximum(np.asarray(ses, float) ** 2, 1e-300)
    mean = float((w * c2s).sum() / w.sum())
    return float((w * (np.asarray(c2s, float) - mean) ** 2).sum())


def spread(c2s):
    """The plain standard deviation of the fold estimates. **Reported, not
    tested.** It is in the units of the chirality and so is readable, but its
    null distribution depends on how precision varies across folds, which is why
    `heterogeneity` is the statistic the verdict rests on."""
    return float(np.std(c2s, ddof=1))


def random_fold_map(sizes, n_problems, rng):
    """A partition of the problems into folds of exactly the given sizes."""
    perm = rng.permutation(n_problems)
    out = np.empty(n_problems, dtype=int)
    at = 0
    for f, s in enumerate(sizes):
        out[perm[at:at + s]] = f
        at += s
    assert at == n_problems, "fold sizes do not cover the problems"
    return out


def null_stats(rows, sizes, n_problems, b, seed, n_jobs=1):
    """The distribution of `heterogeneity` under uninformative splits of the
    same sizes. Every fold is refitted, so this carries the same estimation
    noise the observed statistic carries. Returns `(q, spreads, converged)`."""
    def one(i):
        rng = np.random.default_rng([seed, i])
        fm = random_fold_map(sizes, n_problems, rng)
        c2s, ses, infos = fold_estimates(rows, fm, len(sizes))
        ok = all(inf["converged"] for inf in infos)
        return heterogeneity(c2s, ses), spread(c2s), ok

    if n_jobs == 1:
        res = [one(i) for i in range(b)]
    else:
        from joblib import Parallel, delayed
        res = Parallel(n_jobs=n_jobs)(delayed(one)(i) for i in range(b))
    return (np.array([r[0] for r in res]),
            np.array([r[1] for r in res]),
            np.array([r[2] for r in res]))


def p_value(observed, null):
    """One-sided, with the observed value included, so it can never be zero."""
    return float((1 + int(np.sum(null >= observed))) / (len(null) + 1))
