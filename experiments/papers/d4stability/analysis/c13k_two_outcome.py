#!/usr/bin/env python3
"""EXPLORATORY. Does the multi-branch collapse explain the choices13k sign?

**Not part of any registration and it changes no verdict.** `prereg-d4interior-v3`
is sealed, it ran, and its `-0.1216` stands as what it measured.

The puzzle. Three estimates of the same quantity:

    CPC18 interior, corners dropped          +0.4438
    choices13k aggregate, prereg-d4interior-v3   -0.1216
    peterson2021using, individual choices    +0.2506

The first and third agree in sign and the second does not, which is awkward
because **peterson2021using is the choices13k stimulus family measured at the
individual level.** The same problems, largely the same people, opposite sign.

One difference is concrete enough to test. `c13k_rows.py` reads `Ha, pHa, La` and
`Hb, pHb, Lb` for every row, but choices13k option B may be a lottery of up to
ten branches, described by `LotShapeB` and `LotNumB`. **1,095 of the 2,380 rows
the v3 fit used have `LotNumB > 1`**, so for nearly half the corpus those three
columns describe the extremes of a lottery rather than the lottery. The peterson
corpus excludes multi-branch problems outright, because extending a two-outcome
coordinate to a ten-branch lottery would mean writing a new coordinate and
calling it the old one.

So: refit v3's corpus restricted to `LotNumB == 1`, where the three columns are
the whole option and the coordinate means what it says. If the sign flips, the
disagreement is an artifact of collapsing multi-branch lotteries and not a fact
about the two corpora.

The estimator, the design and the orientation are v3's own, taken by importing
its modules, so the only thing that changes is which rows are included.

    python c13k_two_outcome.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.abspath(os.path.join(HERE, "..", "..", "d4interior", "analysis"))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
sys.path.insert(0, V3)
sys.path.insert(0, DATASETS)

from d4_rotation import _opt_coords  # noqa: E402  IMPORTED, never restated
from kappa_mle import TERM_NAMES, _nll_grad_hess, design, fit  # noqa: E402

C13K = os.path.join(DATASETS, "raw", "choices13k", "c13k_selections.csv")

_d, _q = _opt_coords(10.0, 1.0, 10.0)
assert abs(_d - 1.0) < 1e-9, "imported _opt_coords is not the expected coordinate"


def feats(H, p, L):
    ev = p * H + (1 - p) * L
    var = p * (H - ev) ** 2 + (1 - p) * (L - ev) ** 2
    return float(ev), float(np.sqrt(max(var, 0.0)))


def build(df):
    """v3's row construction: y = P(chose A), regressors A - B. Consistent, and
    not the orientation that voided prereg-d4stability-v1."""
    rows = []
    for r in df.itertuples():
        evA, sdA = feats(r.Ha, r.pHa, r.La)
        evB, sdB = feats(r.Hb, r.pHb, r.Lb)
        H, p, L = (r.Ha, r.pHa, r.La) if sdA >= sdB else (r.Hb, r.pHb, r.Lb)
        dc, qc = _opt_coords(H, p, L)
        rows.append((evA - evB, sdA - sdB, dc, qc, 1.0 - float(r.bRate)))
    A = lambda j: np.array([x[j] for x in rows])
    z = lambda x: (x - x.mean()) / (x.std() + 1e-9)
    return z(A(0)), z(A(1)), A(2), A(3), A(4)


def run(tag, df):
    dEV, dSD, d, q, pA = build(df)
    X = design(dEV, dSD, d, q)
    theta, info = fit(X, pA)
    _n, _g, H = _nll_grad_hess(X, pA, theta)
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    print()
    print("%s   n = %d" % (tag, len(pA)))
    print("   bEV    %+.4f" % theta[0])
    for i, t in enumerate(TERM_NAMES):
        star = "   <-- chirality" if t == "d*q" else ""
        print("   %-6s %+.4f +/- %.4f%s" % (t, theta[1 + i], se[1 + i], star))
    print("   grad %.2e   converged %s" % (info["grad_inf_norm"], info["converged"]))
    return {"n": int(len(pA)), "bEV": float(theta[0]),
            "coefficients": {t: float(theta[1 + i]) for i, t in enumerate(TERM_NAMES)},
            "se": {t: float(se[1 + i]) for i, t in enumerate(TERM_NAMES)},
            "chirality": float(theta[1 + TERM_NAMES.index("d*q")])}


def main():
    c = pd.read_csv(C13K)
    sub = c[(c["Block"] == 1) & (c["Feedback"] == 0)].dropna(
        subset=["Ha", "pHa", "La", "Hb", "pHb", "Lb", "bRate"])
    print("choices13k Block 1, Feedback 0: %d rows" % len(sub))
    print("  with LotNumB > 1 (multi-branch B): %d" % int((sub["LotNumB"] > 1).sum()))
    print("  with LotNumB == 1 (two-outcome) : %d" % int((sub["LotNumB"] == 1).sum()))
    print("  ambiguous (Amb True)            : %d" % int(sub["Amb"].sum()))

    out = {"note": "EXPLORATORY, changes no registered verdict",
           "v3_published_chirality": -0.12158348968635554}
    out["all_rows"] = run("ALL ROWS, reproducing the v3 corpus", sub)
    out["two_outcome"] = run("TWO-OUTCOME ONLY, LotNumB == 1",
                             sub[sub["LotNumB"] == 1])
    out["multi_branch"] = run("MULTI-BRANCH ONLY, LotNumB > 1",
                              sub[sub["LotNumB"] > 1])
    out["two_outcome_unambiguous"] = run(
        "TWO-OUTCOME AND UNAMBIGUOUS", sub[(sub["LotNumB"] == 1) & (~sub["Amb"])])

    print()
    print("=" * 70)
    print("v3 published chirality on all rows      %+.4f" % out["v3_published_chirality"])
    print("reproduced here on all rows             %+.4f" % out["all_rows"]["chirality"])
    print("restricted to two-outcome problems      %+.4f" % out["two_outcome"]["chirality"])
    print("multi-branch problems alone             %+.4f" % out["multi_branch"]["chirality"])
    print("peterson2021using, individual, 2-outcome    +0.2506")
    print("CPC18 interior, corners dropped             +0.4438")
    print("=" * 70)

    with open(os.path.join(HERE, "c13k_two_outcome.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("written c13k_two_outcome.json")


if __name__ == "__main__":
    main()
