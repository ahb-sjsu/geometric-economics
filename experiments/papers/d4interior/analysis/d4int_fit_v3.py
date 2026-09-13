#!/usr/bin/env python3
"""Fits the interior chirality registered in prereg-d4interior-v3 on choices13k.

NO thresholds here and no pass/fail judgement. Grading is `d4int_grade_v3.py`,
written first, which holds every bar.

Rows and the coordinate come from `c13k_rows.py`, which imports `_opt_coords`
from `d4_rotation` and asserts on it at import. The estimator is the convex
Newton solver of `kappa_mle.py`. Nothing here restates a definition it inherits.

    python d4int_fit_v3.py [--out results_v3.json]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from c13k_rows import build  # noqa: E402
import kappa_mle as K  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "results_v3.json"))
    a = ap.parse_args()

    dEV, dSD, d, q, pA, nsub = build(with_outcome=True)
    X = K.design(dEV, dSD, d, q)

    # The problem is convex, so the optimum does not depend on the start. Several
    # starts are run anyway and reported, because a disagreement would mean the
    # convexity argument does not apply to this data and that is worth seeing.
    runs = {}
    for s in (0.0, 0.1, -0.1, 0.5):
        th, info = K.fit(X, pA, start=s)
        runs[str(s)] = {"dq": float(th[3]), "nll": info["nll"],
                        "grad_inf_norm": info["grad_inf_norm"],
                        "converged": info["converged"]}
    th, info = K.fit(X, pA, start=0.0)

    dq = d * q
    res = {
        "corpus": "choices13k, Block==1 and Feedback==0",
        "estimator": "convex Newton, kappa_mle.fit",
        "n_rows": int(len(d)),
        "n_nonzero_dq": int((dq != 0).sum()),
        "n_d_negative": int((d < 0).sum()),
        "n_d_positive": int((d > 0).sum()),
        "subjects_per_problem_median": int(np.median(nsub)),
        "bEV": float(th[0]),
        "coefficients": {n: float(v) for n, v in zip(K.TERM_NAMES, th[1:])},
        "chirality_dq": float(th[3]),
        "nll": info["nll"],
        "grad_inf_norm": info["grad_inf_norm"],
        "hessian_min_eig": info["hessian_min_eig"],
        "iterations": info["iterations"],
        "converged": info["converged"],
        "starts": runs,
        "dq_spread_across_starts": float(
            max(r["dq"] for r in runs.values()) - min(r["dq"] for r in runs.values())),
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2)
    print("n = %d   d*q = %+.4f   |grad| = %.2e   minEig = %.3f"
          % (res["n_rows"], res["chirality_dq"], res["grad_inf_norm"],
             res["hessian_min_eig"]))
    print("spread across 4 starts: %.2e" % res["dq_spread_across_starts"])
    print("written", a.out)


if __name__ == "__main__":
    main()
