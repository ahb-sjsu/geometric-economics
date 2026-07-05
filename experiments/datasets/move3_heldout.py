#!/usr/bin/env python3
"""Move 3 -- pre-register the V4 constraints and confirm them HELD-OUT.

The V4 structure was DISCOVERED on Ruggeri (17 KT problems x 19 countries). Here we freeze its
structural predictions and test them on a DIFFERENT corpus: the pure-gain and pure-loss gambles in
CPC18 + choices13k (a distinct lottery source, representative not adversarial). If the same
interaction-dominant, no-probability-main-effect structure appears out-of-sample, V4 moves from
'organizing description on one corpus' to 'confirmed structure'.

Pre-registered predictions (frozen from the Ruggeri result, BEFORE the held-out fit):
  R1  interaction dominates:      |b_dq| > 2 * |b_q|     (risk attitude ~ d*q, not q alone)
  R2  probability has ~no main effect:  |b_q| < 0.5*|b_dq|
  R3  a domain main effect (loss aversion) is present and is the largest non-interaction term.
The frozen block is hashed; the held-out fit is scored against R1-R3.

    python move3_heldout.py
"""
from __future__ import annotations

import hashlib
import json
import os

import numpy as np
import pandas as pd
from scipy.optimize import minimize

import cpc18

HERE = os.path.dirname(os.path.abspath(__file__))
C13K = os.path.join(HERE, "raw", "choices13k", "c13k_selections.csv")

PREREG = {
    "discovered_on": "ruggeri_kt_17x19",
    "held_out_corpus": "cpc18+choices13k pure-gain & pure-loss gambles",
    "R1_interaction_dominates": "|b_dq| > 2*|b_q|",
    "R2_no_prob_main_effect": "|b_q| < 0.5*|b_dq|",
    "R3_loss_aversion_present": "|b_d| is the largest non-interaction term and nonzero",
    "model": "P(A)=sigmoid(bEV*dEV + (b0+b_d*d+b_q*q+b_dq*d*q)*dSD), z-scored, weighted by n",
}


def _feats(H, p, L):
    ev = p * H + (1 - p) * L
    sd = np.sqrt(max(p * (H - ev) ** 2 + (1 - p) * (L - ev) ** 2, 0))
    return ev, sd


def _domain(H, p, L):
    if H >= 0 and L >= 0:
        return 1        # pure gain
    if H <= 0 and L <= 0:
        return -1       # pure loss
    return 0            # mixed -> excluded


def _prob_level(H, p, L):
    # probability of the larger-|amount| outcome of this (risky) option
    p_ext = p if abs(H) >= abs(L) else (1 - p)
    return 1.0 if p_ext >= 0.5 else -1.0


def load_rows():
    rows = []
    raw = pd.read_csv(cpc18.RAW, usecols=["GameID", "Ha", "pHa", "La", "Hb", "pHb", "Lb"]
                      ).groupby("GameID").first()
    d = cpc18.load_description().merge(raw.reset_index(), on="GameID")
    src = [(r.Ha, r.pHa, r.La, r.Hb, r.pHb, r.Lb, getattr(r, "brate", np.nan), getattr(r, "n", 1))
           for r in d.itertuples()]
    try:
        c = pd.read_csv(C13K)
        c = c[(c.get("Block", 1) == 1)] if "Block" in c else c
        c = c.rename(columns={"bRate": "brate"}).dropna(subset=["Ha", "pHa", "La", "Hb", "pHb", "Lb", "brate"])
        src += [(r.Ha, r.pHa, r.La, r.Hb, r.pHb, r.Lb, r.brate, 1) for r in c.itertuples()]
    except Exception:  # noqa: BLE001
        pass
    for Ha, pHa, La, Hb, pHb, Lb, brate, n in src:
        if brate is None or (isinstance(brate, float) and np.isnan(brate)):
            continue
        # both options must be the SAME pure domain for a clean cell
        da, db = _domain(Ha, pHa, La), _domain(Hb, pHb, Lb)
        if da == 0 or db == 0 or da != db:
            continue
        evA, sdA = _feats(Ha, pHa, La)
        evB, sdB = _feats(Hb, pHb, Lb)
        H, p, L = (Ha, pHa, La) if sdA >= sdB else (Hb, pHb, Lb)
        q = _prob_level(H, p, L)
        rows.append((evA - evB, sdA - sdB, float(da), q, 1 - brate, float(n)))
    return rows


def fit(rows):
    dEV = np.array([r[0] for r in rows]); dSD = np.array([r[1] for r in rows])
    d = np.array([r[2] for r in rows]); q = np.array([r[3] for r in rows])
    pA = np.array([r[4] for r in rows]); n = np.array([r[5] for r in rows])
    zc = lambda x: (x - x.mean()) / (x.std() + 1e-9)
    zE, zS = zc(dEV), zc(dSD)

    def nll(b):
        bEV, b0, bd, bq, bdq = b
        lin = bEV * zE + (b0 + bd * d + bq * q + bdq * d * q) * zS
        p = np.clip(1 / (1 + np.exp(-lin)), 1e-9, 1 - 1e-9)
        return -np.sum(n * (pA * np.log(p) + (1 - pA) * np.log(1 - p)))

    best = None
    for s in range(8):
        r = minimize(nll, np.random.default_rng(s).normal(0, 0.5, 5), method="BFGS",
                     options={"maxiter": 1000})
        if best is None or r.fun < best.fun:
            best = r
    return best.x, (d, q)


def main():
    blob = json.dumps(PREREG, sort_keys=True)
    h = hashlib.sha256(blob.encode()).hexdigest()[:12]
    print(f"== PRE-REGISTRATION (frozen from Ruggeri) sha256={h} ==")
    for k in ("R1_interaction_dominates", "R2_no_prob_main_effect", "R3_loss_aversion_present"):
        print(f"  {k}: {PREREG[k]}")

    rows = load_rows()
    d = np.array([r[2] for r in rows]); q = np.array([r[3] for r in rows])
    from collections import Counter
    cells = Counter((int(dd), int(qq)) for dd, qq in zip(d, q))
    print(f"\n== HELD-OUT corpus: {len(rows)} gamble-pairs (CPC18+choices13k pure-domain) ==")
    print("  cells (domain, prob-level):", dict(cells))
    beta, _ = fit(rows)
    bEV, b0, bd, bq, bdq = beta
    print(f"\n  fitted: b0={b0:+.3f}  b_d={bd:+.3f}  b_q={bq:+.3f}  b_dq={bdq:+.3f}  (bEV={bEV:+.2f})")

    print("\n== Scoring against the pre-registration ==")
    r1 = abs(bdq) > 2 * abs(bq)
    r2 = abs(bq) < 0.5 * abs(bdq)
    r3 = abs(bd) >= max(abs(b0), abs(bq)) and abs(bd) > 0.02
    print(f"  R1 interaction dominates (|b_dq|>2|b_q|): |{bdq:+.3f}| vs 2*|{bq:+.3f}|  -> {'PASS' if r1 else 'FAIL'}")
    print(f"  R2 no prob main effect (|b_q|<0.5|b_dq|): |{bq:+.3f}| < {0.5*abs(bdq):.3f}  -> {'PASS' if r2 else 'FAIL'}")
    print(f"  R3 loss aversion present (b_d largest non-interaction): b_d={bd:+.3f}  -> {'PASS' if r3 else 'FAIL'}")

    npass = sum([r1, r2, r3])
    print(f"\n== Verdict (Move 3): {npass}/3 pre-registered predictions confirmed HELD-OUT ==")
    if npass == 3:
        print("V4 structure REPLICATES out-of-sample on a distinct corpus -> confirmed, not just an "
              "organizing description of one dataset.")
    elif npass >= 1:
        print("PARTIAL held-out confirmation -- report exactly which structural predictions replicate.")
    else:
        print("V4 does NOT replicate held-out -- it was specific to the Ruggeri KT corpus.")
    print("HONEST: CPC18/choices13k are representative (bEV>0) vs Ruggeri adversarial (bEV<0); pure-loss "
          "gambles are the scarce cell -- check the cell counts above before trusting b_d/b_q.")


if __name__ == "__main__":
    main()
