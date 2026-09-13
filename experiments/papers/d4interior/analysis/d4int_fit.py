#!/usr/bin/env python3
"""Fits the interior chirality registered in prereg-d4interior-v2 on choices13k.

This file contains NO thresholds and makes NO pass/fail judgement. Grading is
`d4int_grade.py`, which was written first and holds every bar.

Rows, coordinate and model come from `c13k_rows.py`, which imports `_opt_coords`
from `d4_rotation` and asserts at import that it has the real one. Nothing here
restates a definition it inherits, which is the condition prereg-d4gate-v1 failed.

    python d4int_fit.py [--out results.json]

Specification is prereg-d4interior-v2.md Sections 3 and 4.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from c13k_rows import build, fit_kappa, TERM_NAMES  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "results.json"))
    a = ap.parse_args()

    dEV, dSD, d, q, pA, nsub = build(with_outcome=True)

    # F3 of the registration: both starts must agree in the objective.
    r0 = fit_kappa(dEV, dSD, d, q, pA, starts=(0.0,))
    r1 = fit_kappa(dEV, dSD, d, q, pA, starts=(0.1,))
    best = r0 if r0.fun <= r1.fun else r1

    coef = {n: float(v) for n, v in zip(TERM_NAMES, best.x[1:])}
    dq = d * q
    res = {
        "corpus": "choices13k, Block==1 and Feedback==0",
        "n_rows": int(len(d)),
        "n_nonzero_dq": int((dq != 0).sum()),
        "n_d_negative": int((d < 0).sum()),
        "n_d_positive": int((d > 0).sum()),
        "distinct_d_values": int(len(np.unique(np.round(d, 6)))),
        "subjects_per_problem_median": int(np.median(nsub)),
        "bEV": float(best.x[0]),
        "coefficients": coef,
        "chirality_dq": coef["d*q"],
        "nll": float(best.fun),
        "convergence": {
            "nll_start_0.0": float(r0.fun),
            "nll_start_0.1": float(r1.fun),
            "abs_difference": float(abs(r0.fun - r1.fun)),
            "dq_start_0.0": float(r0.x[3]),
            "dq_start_0.1": float(r1.x[3]),
        },
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2)
    print("n = %d rows, chirality d*q = %+.4f" % (res["n_rows"], res["chirality_dq"]))
    print("written", a.out)


if __name__ == "__main__":
    main()
