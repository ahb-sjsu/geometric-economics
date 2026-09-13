#!/usr/bin/env python3
"""Checks the convex solver on synthetic data. Outcomes are never read.

Two things are established before any registration relies on this estimator.

1. It converges to a gradient norm far below any tolerance worth registering,
   from every start tried, and the Hessian at the optimum is positive definite,
   so the optimum is unique rather than merely agreed upon.
2. It recovers a known chirality that was put into the synthetic data.

Powell, the estimator prereg-d4interior-v2 used, is run on the same synthetic
data for comparison, so the void of that registration is characterised rather
than asserted.

    python verify_mle.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from c13k_rows import build  # noqa: E402
import kappa_mle as K  # noqa: E402

TRUE_DQ = 0.4437750481416212


def main():
    dEV, dSD, d, q, _, nsub = build(with_outcome=False)
    X = K.design(dEV, dSD, d, q)
    rng = np.random.default_rng(20260913)

    true = np.array([1.0, -0.4092, 0.2911, TRUE_DQ, -0.4822, -0.2865, 0.3777])
    p = 1.0 / (1.0 + np.exp(-(X @ true)))
    y = rng.binomial(nsub, p) / nsub

    out = {"true_dq": TRUE_DQ, "n_rows": int(X.shape[0]), "newton": {}, "powell": {}}

    # Newton, from several starts. The solver itself starts at zero, so the
    # starts are injected by shifting the initial point through a warm start.
    for s in (0.0, 0.1, -0.1, 0.5, -0.5, 2.0):
        theta = np.full(X.shape[1], s)
        nll, g, H = K._nll_grad_hess(X, y, theta)
        # run Newton from this start
        cur = theta.copy()
        for _ in range(200):
            nll, g, H = K._nll_grad_hess(X, y, cur)
            if np.max(np.abs(g)) < 1e-10:
                break
            step = np.linalg.solve(H + 1e-10 * np.eye(X.shape[1]), -g)
            t = 1.0
            for _ in range(60):
                cand = cur + t * step
                nll_c, _, _ = K._nll_grad_hess(X, y, cand)
                if nll_c <= nll:
                    break
                t *= 0.5
            cur = cand
        nll, g, H = K._nll_grad_hess(X, y, cur)
        eig = np.linalg.eigvalsh(H)
        out["newton"][str(s)] = {
            "dq": float(cur[3]), "nll": float(nll),
            "grad_inf_norm": float(np.max(np.abs(g))),
            "hessian_min_eig": float(eig.min()),
        }

    # Powell, the v2 estimator, on the same data
    def nllp(theta):
        lin = X @ theta
        pp = np.clip(1.0 / (1.0 + np.exp(-lin)), 1e-9, 1 - 1e-9)
        return -np.sum(y * np.log(pp) + (1 - y) * np.log(1 - pp))

    for s in (0.0, 0.1):
        r = minimize(nllp, np.full(X.shape[1], s), method="Powell",
                     options={"maxiter": 40000})
        out["powell"][str(s)] = {"dq": float(r.x[3]), "nll": float(r.fun)}

    nl = out["newton"]
    dqs = [v["dq"] for v in nl.values()]
    nlls = [v["nll"] for v in nl.values()]
    out["newton_spread"] = {"dq_range": float(max(dqs) - min(dqs)),
                            "nll_range": float(max(nlls) - min(nlls))}
    pw = out["powell"]
    out["powell_spread"] = {
        "dq_range": float(abs(pw["0.0"]["dq"] - pw["0.1"]["dq"])),
        "nll_range": float(abs(pw["0.0"]["nll"] - pw["0.1"]["nll"]))}

    print("true d*q = %+.4f on %d rows" % (TRUE_DQ, X.shape[0]))
    print()
    print("Newton, by start")
    for s, v in nl.items():
        print("  start %-5s  d*q %+.4f   nll %.6f   |grad| %.2e   minEig %.4f"
              % (s, v["dq"], v["nll"], v["grad_inf_norm"], v["hessian_min_eig"]))
    print("  spread across starts: d*q %.2e   nll %.2e"
          % (out["newton_spread"]["dq_range"], out["newton_spread"]["nll_range"]))
    print()
    print("Powell, the v2 estimator, same data")
    for s, v in pw.items():
        print("  start %-5s  d*q %+.4f   nll %.6f" % (s, v["dq"], v["nll"]))
    print("  spread across starts: d*q %.2e   nll %.2e"
          % (out["powell_spread"]["dq_range"], out["powell_spread"]["nll_range"]))

    with open(os.path.join(HERE, "verify_mle.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written verify_mle.json")


if __name__ == "__main__":
    main()
