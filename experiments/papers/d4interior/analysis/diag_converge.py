#!/usr/bin/env python3
"""Why does the solver fail on some synthetic draws? Covariates only.

Reports, over a handful of draws, the gradient norm reached, the smallest
Hessian eigenvalue, the coefficient magnitude, and how many target rows sit at
exactly 0 or 1. Perfect or near-perfect separation drives the logistic maximum
likelihood estimate to infinity, in which case no optimizer converges and the
estimator needs a penalty rather than a better search.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from c13k_rows import build  # noqa: E402
import kappa_mle as K  # noqa: E402

DIAG = os.path.abspath(os.path.join(HERE, "..", "..", "d4gate",
                                    "analysis", "diagnostic_pooling.json"))
TERMS = ["const", "d2+q2", "d*q", "d", "q", "d2-q2"]


def main():
    dEV, dSD, d, q, _, nsub = build(with_outcome=False)
    X = K.design(dEV, dSD, d, q)
    with open(DIAG, encoding="utf-8") as fh:
        B = json.load(fh)["fits"]["B_corners_dropped"]["coefficients"]
    true = np.array([1.0] + [B[t] for t in TERMS])
    p = 1.0 / (1.0 + np.exp(-(X @ true)))
    rng = np.random.default_rng(20260913)

    print("n rows %d   median subjects/problem %d" % (len(d), int(np.median(nsub))))
    print("%4s %8s %10s %12s %10s %8s" %
          ("rep", "|grad|", "minEig", "max|theta|", "y in {0,1}", "conv"))
    bad = 0
    for i in range(12):
        y = rng.binomial(nsub, p) / nsub
        th, info = K.fit(X, y)
        extreme = int(((y <= 0.0) | (y >= 1.0)).sum())
        print("%4d %8.1e %10.4f %12.2f %10d %8s"
              % (i, info["grad_inf_norm"], info["hessian_min_eig"],
                 float(np.max(np.abs(th))), extreme, info["converged"]))
        if not info["converged"]:
            bad += 1
    print()
    print("non-converged: %d of 12" % bad)


if __name__ == "__main__":
    main()
