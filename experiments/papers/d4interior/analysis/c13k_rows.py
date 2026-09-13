#!/usr/bin/env python3
"""Row builder for prereg-d4interior-v2. Shared by the power simulation and the fit.

The coordinate is IMPORTED from `d4_rotation`, never restated. prereg-d4gate-v1
was voided because its analysis code reimplemented `_opt_coords` from assumption
and got both its form and its sign convention wrong, so this module asserts at
import time that it is using the real one.

Corpus: choices13k, description regime, Block == 1 and Feedback == 0, which is
the decision-from-description condition that matches CPC18's Trial == 1.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
sys.path.insert(0, DATASETS)

from d4_rotation import _opt_coords  # noqa: E402  IMPORTED, never restated

C13K = os.path.join(DATASETS, "raw", "choices13k", "c13k_selections.csv")

# A pure-gain, certain, two-outcome option must give d = +1. If this fails the
# imported coordinate is not the one this registration assumes and nothing below
# is valid.
_d, _q = _opt_coords(10.0, 1.0, 10.0)
assert abs(_d - 1.0) < 1e-9, "imported _opt_coords is not the expected coordinate"

TERM_NAMES = ["const", "d2+q2", "d*q", "d", "q", "d2-q2"]


def _feats(H, p, L):
    ev = p * H + (1 - p) * L
    var = p * (H - ev) ** 2 + (1 - p) * (L - ev) ** 2
    return ev, float(np.sqrt(max(var, 0.0)))


def build(with_outcome: bool):
    """Interior rows. With `with_outcome=False` the choice column is never read,
    which is what the power simulation uses."""
    cols = ["Problem", "Block", "Feedback", "n",
            "Ha", "pHa", "La", "Hb", "pHb", "Lb"]
    if with_outcome:
        cols.append("bRate")
    d = pd.read_csv(C13K, usecols=cols)
    d = d[(d["Block"] == 1) & (d["Feedback"] == 0)]
    sub = ["Ha", "pHa", "La", "Hb", "pHb", "Lb"] + (["bRate"] if with_outcome else [])
    d = d.dropna(subset=sub)

    rows = []
    for r in d.itertuples():
        evA, sdA = _feats(r.Ha, r.pHa, r.La)
        evB, sdB = _feats(r.Hb, r.pHb, r.Lb)
        H, p, L = (r.Ha, r.pHa, r.La) if sdA >= sdB else (r.Hb, r.pHb, r.Lb)
        dc, qc = _opt_coords(H, p, L)
        pA = (1.0 - float(r.bRate)) if with_outcome else np.nan
        rows.append((evA - evB, sdA - sdB, dc, qc, pA, int(r.n)))

    z = lambda x: (x - x.mean()) / (x.std() + 1e-9)
    return (z(np.array([r[0] for r in rows])),
            z(np.array([r[1] for r in rows])),
            np.array([r[2] for r in rows]),
            np.array([r[3] for r in rows]),
            np.array([r[4] for r in rows]),
            np.array([r[5] for r in rows], dtype=int))


def kappa_terms(d, q):
    """The six terms of d4_rotation part_b, allowed then breaking."""
    return np.vstack([np.ones_like(d), d ** 2 + q ** 2, d * q,
                      d, q, d ** 2 - q ** 2])


def fit_kappa(dEV, dSD, d, q, pA, starts=(0.0, 0.1)):
    from scipy.optimize import minimize
    T = kappa_terms(d, q)

    def nll(theta):
        lin = theta[0] * dEV + (theta[1:] @ T) * dSD
        p = np.clip(1.0 / (1.0 + np.exp(-lin)), 1e-9, 1 - 1e-9)
        return -np.sum(pA * np.log(p) + (1 - pA) * np.log(1 - p))

    best = None
    for s in starts:
        r = minimize(nll, np.full(7, s), method="Powell",
                     options={"maxiter": 40000})
        if best is None or r.fun < best.fun:
            best = r
    return best
