#!/usr/bin/env python3
"""Diagnostic, not a registration. Why does the interior chirality differ?

`RESULTS_d4_rotation.md` Part B reports the chirality `d*q` at +0.003. The
prereg-d4gate-v1 run, on the CPC18 interior alone, puts it near -0.73. This
script decomposes the difference, using `d4_rotation.py`'s own row builder so
that nothing is re-implemented and no coordinate is redefined.

Four fits, all with the same six terms and the same optimizer settings that
`d4_rotation.py` used, one Powell start at zero with 20000 iterations:

  A  AS PUBLISHED      all rows, standardised over all rows.
  B  CORNERS DROPPED   CPC18 rows only, standardised over CPC18 rows.
  C  CORNERS IN LIKELIHOOD ONLY   all rows, but standardised over CPC18 rows,
                       so the corner rows contribute to the fit and do not
                       rescale the interior.
  D  CORNERS IN SCALING ONLY      CPC18 rows only, standardised over all rows,
                       so the corner rows rescale the interior and do not
                       contribute to the fit.

A against B is the whole difference. C and D split it into the part carried by
the corner rows' own likelihood contribution and the part carried by their
effect on the standardisation of every other row.

This is exploratory. The registration it follows is spent, and nothing here
grades anything.

    python diagnostic_pooling.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
sys.path.insert(0, DATASETS)

import d4_rotation as D  # noqa: E402

TERMS = ["const", "d2+q2", "d*q", "d", "q", "d2-q2"]


def kappa_terms(d, q):
    return np.vstack([np.ones_like(d), d ** 2 + q ** 2, d * q, d, q, d ** 2 - q ** 2])


def fit(dEV, dSD, d, q, pA, w):
    """Six-term kappa, d4_rotation.py's own optimizer settings."""
    T = kappa_terms(d, q)

    def nll(theta):
        lin = theta[0] * dEV + (theta[1:] @ T) * dSD
        p = np.clip(1.0 / (1.0 + np.exp(-lin)), 1e-9, 1 - 1e-9)
        return -np.sum(w * (pA * np.log(p) + (1 - pA) * np.log(1 - p)))

    r = minimize(nll, np.zeros(1 + len(TERMS)), method="Powell",
                 options={"maxiter": 20000})
    return r


def main():
    rows = D.build_continuous()
    arr = {k: np.array([r[i] for r in rows])
           for i, k in enumerate(["dEV", "dSD", "d", "q", "pA", "w"])}
    n = len(rows)
    # d4_rotation.py appends the KT corner rows last, one per KT problem.
    n_corner = len(D.R.KT)
    is_cpc = np.arange(n) < (n - n_corner)

    def z_with(x, mask):
        m, s = x[mask].mean(), x[mask].std()
        return (x - m) / (s + 1e-9)

    all_mask = np.ones(n, dtype=bool)
    out = {"n_rows": int(n), "n_corner_rows": int(n_corner),
           "n_cpc18_rows": int(is_cpc.sum()), "fits": {}}

    specs = [
        ("A_as_published", all_mask, all_mask),
        ("B_corners_dropped", is_cpc, is_cpc),
        ("C_corners_in_likelihood_only", all_mask, is_cpc),
        ("D_corners_in_scaling_only", is_cpc, all_mask),
    ]
    for name, fit_mask, scale_mask in specs:
        dEVz = z_with(arr["dEV"], scale_mask)
        dSDz = z_with(arr["dSD"], scale_mask)
        r = fit(dEVz[fit_mask], dSDz[fit_mask], arr["d"][fit_mask],
                arr["q"][fit_mask], arr["pA"][fit_mask], arr["w"][fit_mask])
        out["fits"][name] = {
            "n_fitted": int(fit_mask.sum()),
            "coefficients": {t: float(v) for t, v in zip(TERMS, r.x[1:])},
            "d*q": float(r.x[3]),
            "nll": float(r.fun),
        }

    print("rows %d = %d CPC18 interior + %d KT corners"
          % (n, is_cpc.sum(), n_corner))
    print()
    print("%-32s %10s %10s" % ("fit", "d*q", "nll"))
    for name in [s[0] for s in specs]:
        f = out["fits"][name]
        print("%-32s %+10.4f %10.4f" % (name, f["d*q"], f["nll"]))
    with open(os.path.join(HERE, "diagnostic_pooling.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written diagnostic_pooling.json")


if __name__ == "__main__":
    main()
