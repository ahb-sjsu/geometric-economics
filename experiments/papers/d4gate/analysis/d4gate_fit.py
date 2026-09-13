#!/usr/bin/env python3
"""Fits the gated chirality registered in prereg-d4gate-v1 and writes results.json.

This file contains NO thresholds and makes NO pass/fail judgement. Grading is
`d4gate_grade.py`, which was written first and holds every bar.

Analysis set. The CPC18 interior only. The Kahneman and Tversky corners are
excluded, because Prediction G is a claim about the interior and Part A of the
original rotation test already covers the corners.

The gate. Fixed by the stimulus. A choice set is CERTAIN when one of its two
options has zero standard deviation, that is when a sure outcome is on the menu.
No outcome enters the gate.

The model. One fit over all interior rows, with only the chirality allowed to
differ by gate,

    kappa(d, q) = c0 + c1 (d^2+q^2) + c2 (d*q) + c3 d + c4 q + c5 (d^2-q^2)
                     + gamma * 1[certain] * (d*q)

so c2 is the chirality where the gate does not fire, gamma is the increment where
it does, and c2 + gamma is the chirality where it does. Fitting the two cells
separately is not possible on this data. The chirality is an interaction needing
both signs of d and the uncertain cell holds four pure-loss rows, so the
coefficient is not identified there.

Usage:
  python d4gate_fit.py [--raw <cpc18_raw.csv>] [--out results.json]

Specification is prereg-d4gate-v1.md Sections 3 and 4, frozen 2026-09-12.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
sys.path.insert(0, DATASETS)

TERM_NAMES = ["const", "d2+q2", "d*q", "d", "q", "d2-q2", "gate*d*q"]


def _feats(H, p, L):
    ev = p * H + (1 - p) * L
    var = p * (H - ev) ** 2 + (1 - p) * (L - ev) ** 2
    return ev, float(np.sqrt(max(var, 0.0)))


def _opt_coords(H, p, L):
    dom = 1.0 if (H <= 0 and L <= 0) else (-1.0 if (H >= 0 and L >= 0) else 0.0)
    return dom, 2.0 * p - 1.0


def build(raw_path):
    import cpc18
    raw = (pd.read_csv(raw_path, usecols=["GameID", "Ha", "pHa", "La", "Hb", "pHb", "Lb"])
           .groupby("GameID").first())
    d = cpc18.load_description().merge(raw.reset_index(), on="GameID")
    rows = []
    for r in d.itertuples():
        brate = getattr(r, "brate", None)
        if brate is None or (isinstance(brate, float) and np.isnan(brate)):
            continue
        evA, sdA = _feats(r.Ha, r.pHa, r.La)
        evB, sdB = _feats(r.Hb, r.pHb, r.Lb)
        H, p, L = (r.Ha, r.pHa, r.La) if sdA >= sdB else (r.Hb, r.pHb, r.Lb)
        dc, qc = _opt_coords(H, p, L)
        certain = bool(min(sdA, sdB) <= 0.0)
        rows.append((evA - evB, sdA - sdB, dc, qc, 1.0 - brate, certain))
    return rows


def terms(d, q, cert):
    return np.vstack([np.ones_like(d), d ** 2 + q ** 2, d * q, d, q, d ** 2 - q ** 2,
                      cert.astype(float) * d * q])


def fit(dEV, dSD, d, q, cert, pA):
    T = terms(d, q, cert)

    def nll(theta):
        lin = theta[0] * dEV + (theta[1:] @ T) * dSD
        p = np.clip(1.0 / (1.0 + np.exp(-lin)), 1e-9, 1 - 1e-9)
        return -np.sum(pA * np.log(p) + (1 - pA) * np.log(1 - p))

    best = None
    for s in (0.0, 0.1):
        r = minimize(nll, np.full(8, s), method="Powell", options={"maxiter": 40000})
        if best is None or r.fun < best.fun:
            best = r
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=None)
    ap.add_argument("--out", default=os.path.join(HERE, "results.json"))
    a = ap.parse_args()

    import cpc18
    rows = build(a.raw or cpc18.RAW)
    dEV = np.array([r[0] for r in rows]); dSD = np.array([r[1] for r in rows])
    dc = np.array([r[2] for r in rows]);  qc = np.array([r[3] for r in rows])
    pA = np.array([r[4] for r in rows])
    cert = np.array([r[5] for r in rows], dtype=bool)
    z = lambda x: (x - x.mean()) / (x.std() + 1e-9)
    dEVz, dSDz = z(dEV), z(dSD)

    r = fit(dEVz, dSDz, dc, qc, cert, pA)
    coef = {n: float(v) for n, v in zip(TERM_NAMES, r.x[1:])}
    c2, gamma = coef["d*q"], coef["gate*d*q"]

    dq = dc * qc
    res = {
        "n_total": int(len(rows)),
        "n_certain": int(cert.sum()),
        "n_uncertain": int((~cert).sum()),
        "n_nonzero_dq_certain": int(((dq != 0) & cert).sum()),
        "n_nonzero_dq_uncertain": int(((dq != 0) & ~cert).sum()),
        "n_pure_loss_certain": int(((dc > 0) & cert).sum()),
        "n_pure_loss_uncertain": int(((dc > 0) & ~cert).sum()),
        "bEV": float(r.x[0]),
        "coefficients": coef,
        "chirality_uncertain_c2": c2,
        "gate_increment_gamma": gamma,
        "chirality_certain_c2_plus_gamma": c2 + gamma,
        "nll": float(r.fun),
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2)
    print("n = %d  certain = %d  uncertain = %d"
          % (res["n_total"], res["n_certain"], res["n_uncertain"]))
    print("written", a.out)


if __name__ == "__main__":
    main()
