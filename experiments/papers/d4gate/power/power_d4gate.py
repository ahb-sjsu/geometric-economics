#!/usr/bin/env python3
"""Power and size simulation for prereg-d4gate-v1. Outcomes are never read.

Design note, 2026-09-12. The first version of this simulation fitted the six-term
kappa separately in each gate cell. A covariates-only cross-tabulation showed why
that cannot work. The chirality d*q is an interaction needing both signs of the
domain coordinate d, and the uncertain cell holds only four pure-loss rows, so
the coefficient is not identified there. The design below fits ONE model to all
interior rows and lets ONLY the chirality differ by gate:

    kappa(d, q) = c0 + c1 (d^2+q^2) + c2 (d*q) + c3 d + c4 q + c5 (d^2-q^2)
                     + gamma * 1[certain] * (d*q)

so c2 is the chirality where the gate does not fire, gamma is the increment where
it does, and c2 + gamma is the chirality where it does. Eight parameters on 270
rows rather than fourteen on a split, and the gating is one coefficient rather
than a difference of two noisy fits.

The script reads the CPC18 stimulus columns and the per-game subject count only.
The choice column B and the derived rate `brate` are never read, so running this
cannot inform any threshold with an outcome. Synthetic outcomes are generated
from the pooled Part B coefficients already published in
`experiments/datasets/RESULTS_d4_rotation.md`, which are a published result of
the earlier test and not a new measurement:

    const -0.265, d^2+q^2 -0.058, d*q +0.003, d -0.194, q +0.144, d^2-q^2 +0.340

  NULL       no chirality anywhere: c2 = 0 and gamma = 0.
  ALT(x)     gated chirality: c2 = 0 and gamma = x.

The null fixes the bars at a 5 percent size. The alternative gives the power the
registration reports. Nothing here decides the verdict.

    python power_d4gate.py --reps 400 --seed 20260912
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
import pandas as pd
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
RAW = os.path.join(DATASETS, "raw", "cpc18_raw.csv")

TERM_NAMES = ["const", "d2+q2", "d*q", "d", "q", "d2-q2"]
POOLED = np.array([-0.265, -0.058, 0.003, -0.194, 0.144, 0.340])
POOLED_BEV = 1.0  # not reported in the record; fixed for simulation only


def _feats(H, p, L):
    ev = p * H + (1 - p) * L
    var = p * (H - ev) ** 2 + (1 - p) * (L - ev) ** 2
    return ev, float(np.sqrt(max(var, 0.0)))


def _opt_coords(H, p, L):
    dom = 1.0 if (H <= 0 and L <= 0) else (-1.0 if (H >= 0 and L >= 0) else 0.0)
    return dom, 2.0 * p - 1.0


def design():
    """Stimulus columns and per-game subject counts only. `B` is never read."""
    raw = (pd.read_csv(RAW, usecols=["GameID", "Ha", "pHa", "La", "Hb", "pHb", "Lb"])
           .groupby("GameID").first().reset_index())
    tri = pd.read_csv(RAW, usecols=["GameID", "Trial"])
    nsub = tri[tri["Trial"] == 1].groupby("GameID").size()
    rows = []
    for r in raw.itertuples():
        evA, sdA = _feats(r.Ha, r.pHa, r.La)
        evB, sdB = _feats(r.Hb, r.pHb, r.Lb)
        H, p, L = (r.Ha, r.pHa, r.La) if sdA >= sdB else (r.Hb, r.pHb, r.Lb)
        dc, qc = _opt_coords(H, p, L)
        certain = (min(sdA, sdB) <= 0.0)   # THE GATE, fixed by the stimulus
        rows.append((evA - evB, sdA - sdB, dc, qc, certain,
                     int(nsub.get(r.GameID, 1))))
    z = lambda x: (x - x.mean()) / (x.std() + 1e-9)
    return (z(np.array([r[0] for r in rows])),
            z(np.array([r[1] for r in rows])),
            np.array([r[2] for r in rows]),
            np.array([r[3] for r in rows]),
            np.array([r[4] for r in rows], dtype=bool),
            np.array([r[5] for r in rows], dtype=int))


def terms(d, q, cert):
    """Six kappa terms plus the gate-by-chirality interaction."""
    return np.vstack([np.ones_like(d), d ** 2 + q ** 2, d * q, d, q, d ** 2 - q ** 2,
                      cert.astype(float) * d * q])


def fit(dEV, dSD, d, q, cert, y):
    T = terms(d, q, cert)

    def nll(theta):
        lin = theta[0] * dEV + (theta[1:] @ T) * dSD
        p = np.clip(1.0 / (1.0 + np.exp(-lin)), 1e-9, 1 - 1e-9)
        return -np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))

    best = None
    for s in (0.0, 0.1):
        r = minimize(nll, np.full(8, s), method="Powell", options={"maxiter": 40000})
        if best is None or r.fun < best.fun:
            best = r
    c2, gamma = float(best.x[3]), float(best.x[7])
    return c2, gamma


def simulate(dEV, dSD, d, q, cert, nsub, c2, gamma, rng):
    T = terms(d, q, cert)
    coef = np.concatenate([POOLED.copy(), [0.0]])
    coef[2] = c2
    coef[6] = gamma
    lin = POOLED_BEV * dEV + (coef @ T) * dSD
    ptrue = 1.0 / (1.0 + np.exp(-lin))
    return rng.binomial(nsub, ptrue) / nsub   # the target is a rate over nsub


def run(reps, seed, alts):
    dEV, dSD, d, q, cert, nsub = design()
    rng = np.random.default_rng(seed)
    dq = d * q
    out = {
        "n_total": int(len(d)),
        "n_certain": int(cert.sum()),
        "n_uncertain": int((~cert).sum()),
        "n_nonzero_dq_certain": int(((dq != 0) & cert).sum()),
        "n_nonzero_dq_uncertain": int(((dq != 0) & ~cert).sum()),
        "n_pure_loss_certain": int(((d > 0) & cert).sum()),
        "n_pure_loss_uncertain": int(((d > 0) & ~cert).sum()),
        "subjects_per_game_median": int(np.median(nsub)),
        "reps": reps, "seed": seed,
        "note": "outcomes never read; synthetic draws only",
    }

    def stats(c2, gamma):
        g, pres = [], []
        for _ in range(reps):
            y = simulate(dEV, dSD, d, q, cert, nsub, c2, gamma, rng)
            c2h, gh = fit(dEV, dSD, d, q, cert, y)
            g.append(abs(gh))
            pres.append(abs(c2h + gh))
        return np.array(g), np.array(pres)

    g0, p0 = stats(0.0, 0.0)
    T_gamma = float(np.quantile(g0, 0.95))
    T_pres = float(np.quantile(p0, 0.95))
    out["null"] = {"T_gamma_95pct": T_gamma, "T_presence_95pct": T_pres}

    out["power"] = {}
    for x in alts:
        g, pres = stats(0.0, float(x))
        out["power"][str(x)] = {
            "G1_gating_power": float(np.mean(g >= T_gamma)),
            "G2_presence_power": float(np.mean(pres >= T_pres)),
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=400)
    ap.add_argument("--seed", type=int, default=20260912)
    ap.add_argument("--alts", default="0.10,0.25,0.50,1.00")
    ap.add_argument("--out", default=os.path.join(HERE, "power_d4gate.json"))
    a = ap.parse_args()
    res = run(a.reps, a.seed, [float(x) for x in a.alts.split(",")])
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
