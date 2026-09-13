#!/usr/bin/env python3
"""Conditioning of the kappa design, on covariates only. Diagnostic, not a registration.

prereg-d4interior-v2 was void because two optimizer starts did not agree. The
question this answers is whether a better optimizer would have helped, or whether
the six kappa terms are close to collinear on the corpus, in which case the term
set is the problem and no optimizer fixes it.

The regressors that actually enter the likelihood are not the kappa terms
themselves. The linear predictor is

    bEV * dEV  +  kappa(d, q) * dSD

so the effective design is `dEV` beside each kappa term multiplied by `dSD`.
That is what is examined here.

Outcomes are never read. Both corpora are built through the shared row builders
that import `_opt_coords` from `d4_rotation`.

    python conditioning_check.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
sys.path.insert(0, HERE)
sys.path.insert(0, DATASETS)

from c13k_rows import build as build_c13k, kappa_terms, TERM_NAMES  # noqa: E402

COLS = ["dEV"] + ["%s*dSD" % t for t in TERM_NAMES]


def report(name, dEV, dSD, d, q):
    T = kappa_terms(d, q)                      # 6 by n
    X = np.vstack([dEV, T * dSD]).T            # n by 7
    # scale each column to unit norm so the condition number reflects geometry
    # rather than the arbitrary units of each term
    norms = np.linalg.norm(X, axis=0)
    norms[norms < 1e-12] = 1.0
    Xs = X / norms
    s = np.linalg.svd(Xs, compute_uv=False)
    cond = float(s[0] / s[-1])

    # the direction that is least determined
    _, _, Vt = np.linalg.svd(Xs, full_matrices=False)
    weak = Vt[-1]

    # variance inflation for the chirality column, index 3 in X
    def vif(j):
        y = Xs[:, j]
        A = np.delete(Xs, j, axis=1)
        beta, *_ = np.linalg.lstsq(A, y, rcond=None)
        resid = y - A @ beta
        ss_tot = float(((y - y.mean()) ** 2).sum())
        ss_res = float((resid ** 2).sum())
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
        return float(1.0 / (1.0 - r2)) if r2 < 1 - 1e-12 else float("inf")

    out = {
        "corpus": name,
        "n_rows": int(X.shape[0]),
        "singular_values": [float(v) for v in s],
        "condition_number": cond,
        "weakest_direction": {c: float(w) for c, w in zip(COLS, weak)},
        "vif": {COLS[j]: vif(j) for j in range(X.shape[1])},
    }
    print("=" * 68)
    print("%s   n = %d" % (name, X.shape[0]))
    print("=" * 68)
    print("  condition number (unit-scaled columns): %.1f" % cond)
    print("  singular values: " + "  ".join("%.4f" % v for v in s))
    print()
    print("  variance inflation by column")
    for c in COLS:
        print("    %-16s %10.1f" % (c, out["vif"][c]))
    print()
    print("  least determined direction, largest loadings")
    for c, w in sorted(out["weakest_direction"].items(),
                       key=lambda kv: -abs(kv[1]))[:4]:
        print("    %-16s %+.3f" % (c, w))
    print()
    return out


def main():
    res = {}

    dEV, dSD, d, q, _, _ = build_c13k(with_outcome=False)
    res["choices13k"] = report("choices13k", dEV, dSD, d, q)

    # CPC18 interior for comparison, built by d4_rotation's own builder with the
    # corner rows dropped, which is fit B of the pooling diagnostic.
    import d4_rotation as D
    rows = D.build_continuous()
    n_corner = len(D.R.KT)
    keep = slice(0, len(rows) - n_corner)
    a = {k: np.array([r[i] for r in rows])[keep]
         for i, k in enumerate(["dEV", "dSD", "d", "q", "pA", "w"])}
    z = lambda x: (x - x.mean()) / (x.std() + 1e-9)
    res["cpc18_interior"] = report("CPC18 interior, corners dropped",
                                   z(a["dEV"]), z(a["dSD"]), a["d"], a["q"])

    with open(os.path.join(HERE, "conditioning_check.json"), "w",
              encoding="utf-8") as fh:
        json.dump(res, fh, indent=2)
    print("written conditioning_check.json")


if __name__ == "__main__":
    main()
