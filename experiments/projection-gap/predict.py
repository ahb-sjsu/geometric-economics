#!/usr/bin/env python3
"""Compute the frozen, no-refit projection-gap predictions -> predictions.json.

For each pre-registered contrast, apply the FROZEN geometric model to the
option displacements and record the signed gap Delta = P(A|hi) - P(A|lo), which
every scalar theory is forced to predict as 0. Primary pre-registered claim is
sign(Delta); magnitude is secondary. Nothing here is fit to data.
"""
from __future__ import annotations

import json
import os

import contrasts as K
import geometric_model as G

HERE = os.path.dirname(os.path.abspath(__file__))


def build_predictions() -> dict:
    rows = []
    for c in K.ALL_CONTRASTS:
        pred = G.predict_delta(c.a_lo, c.b_lo, c.a_hi, c.b_hi)
        rows.append({
            "id": c.id, "family": c.family, "domain": c.domain,
            "coord": c.coord, "coord_name": G.DIM_NAMES.get(c.coord, "?"),
            "kind": c.kind,
            "p_a_lo": round(pred["p_a_lo"], 6),
            "p_a_hi": round(pred["p_a_hi"], 6),
            "delta_pred": round(pred["delta"], 6),
            "sign_pred": pred["sign"],
        })
    # Structural predictions (H4): family-level expectations the model commits to.
    structural = {
        "scalar_null": "every scalar theory (EU/Nash/Fehr-Schmidt/CPT) predicts delta=0 for all real contrasts",
        "placebos_zero": all(r["sign_pred"] == 0 for r in rows if r["kind"] == "placebo"),
        "loss_domain_d9_reversal": (
            _sign(rows, "B1_epistemic_gain") == 1 and _sign(rows, "B1L_epistemic_loss") == -1
        ),
        "dose_peaked_at_level": _dose_peak_level(rows),
        "dose_is_nonmonotone": not _dose_monotone(rows),
        "all_real_signs_nonzero": all(r["sign_pred"] != 0 for r in rows if r["kind"] == "real"),
    }
    return {
        "model": {
            "sigma2": G.SIGMA2, "T_base": G.T_BASE, "T_alpha": G.T_ALPHA,
            "T_floor": G.T_FLOOR, "source": "TCSS revised_manuscript_v2 (frozen, no refit)",
        },
        "m_unit": K.M_UNIT,
        "n_contrasts": len(rows),
        "predictions": rows,
        "structural": structural,
    }


def _sign(rows, family):
    xs = [r["sign_pred"] for r in rows if r["family"] == family]
    return xs[0] if xs else 0


def _fam_absdelta(rows, family):
    xs = [abs(r["delta_pred"]) for r in rows if r["family"] == family]
    return sum(xs) / len(xs) if xs else 0.0


def _dose_rows(rows):
    return sorted((r for r in rows if r["kind"] == "dose"), key=lambda r: r["id"])


def _dose_monotone(rows):
    deltas = [r["delta_pred"] for r in _dose_rows(rows)]
    return all(b >= a for a, b in zip(deltas, deltas[1:])) and len(deltas) >= 2


def _dose_peak_level(rows):
    dose = _dose_rows(rows)
    if not dose:
        return 0
    deltas = [r["delta_pred"] for r in dose]
    return deltas.index(max(deltas)) + 1  # 1-indexed level of maximum effect


def main():
    pred = build_predictions()
    out = os.path.join(HERE, "predictions.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(pred, f, indent=2)
    # human-readable summary
    print(f"{pred['n_contrasts']} contrasts predicted (frozen model, no refit)\n")
    print(f"{'id':7} {'coord':16} {'kind':8} {'P(A|lo)':>8} {'P(A|hi)':>8} {'Delta':>8} sign")
    for r in pred["predictions"]:
        print(f"{r['id']:7} {r['coord_name']:16} {r['kind']:8} "
              f"{r['p_a_lo']:8.3f} {r['p_a_hi']:8.3f} {r['delta_pred']:+8.3f} {r['sign_pred']:+d}")
    print("\nStructural predictions (H4):")
    for k, v in pred["structural"].items():
        print(f"  {k}: {v}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
