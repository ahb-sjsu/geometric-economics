#!/usr/bin/env python3
"""Re-derive projection-gap predictions under the v2 fixed-temperature rule.

Same contrasts (`contrasts.py`), same active metric Σ (panel-confirmed), new
choice rule. Writes predictions_v2.json. Key differences from v1: the dose-
response is now MONOTONE (v1 predicted a peaked inverted-U that the panel
rejected), and magnitudes are not throttled by a super-linear temperature. Signs
are unchanged (T-invariant), carrying over the panel's confirmed result.
"""
from __future__ import annotations

import json
import os

import contrasts as K
import geometric_model_v2 as G

HERE = os.path.dirname(os.path.abspath(__file__))


def build():
    rows = []
    for c in K.ALL_CONTRASTS:
        pr = G.predict_delta(c.a_lo, c.b_lo, c.a_hi, c.b_hi)
        rows.append({"id": c.id, "family": c.family, "domain": c.domain,
                     "coord": c.coord, "coord_name": G.DIM_NAMES.get(c.coord, "?"),
                     "kind": c.kind, "p_a_lo": round(pr["p_a_lo"], 6),
                     "p_a_hi": round(pr["p_a_hi"], 6),
                     "delta_pred": round(pr["delta"], 6), "sign_pred": pr["sign"]})
    dose = sorted((r for r in rows if r["kind"] == "dose"), key=lambda r: r["id"])
    dmeans = [r["delta_pred"] for r in dose]
    structural = {
        "scalar_null": "every scalar theory predicts delta=0 for all real contrasts",
        "placebos_zero": all(r["sign_pred"] == 0 for r in rows if r["kind"] == "placebo"),
        "dose_monotone_increasing": all(b >= a for a, b in zip(dmeans, dmeans[1:])),
        "dose_is_peaked": False,   # v2 explicitly predicts NO interior peak (contra v1)
        "all_real_signs_nonzero": all(r["sign_pred"] != 0 for r in rows if r["kind"] == "real"),
        "loss_domain_d9_reversal_retained": (
            next(r["sign_pred"] for r in rows if r["family"] == "B1_epistemic_gain") == 1
            and next(r["sign_pred"] for r in rows if r["family"] == "B1L_epistemic_loss") == -1
        ),
    }
    return {"model": {"sigma2": G.SIGMA2, "T_fixed": G.T_FIXED, "rule": "fixed-temperature logit",
                      "source": "v2 redesign (choice-rule fuzzing); Sigma frozen+panel-confirmed"},
            "m_unit": K.M_UNIT, "n_contrasts": len(rows), "predictions": rows,
            "structural": structural,
            "changes_from_v1": [
                "cost-dependent temperature (alpha=2.13) -> fixed temperature",
                "dose-response: peaked inverted-U -> MONOTONE increasing (fixes the falsified prediction)",
                "magnitude: single per-population scale T, not throttled",
                "signs unchanged (T-invariant): the panel-confirmed 5/7 carry over",
                "loss-domain d9 reversal RETAINED as a human-testable prediction "
                "(the LLM panel did not show it; flagged for the human study)",
            ]}


def main():
    pred = build()
    out = os.path.join(HERE, "predictions_v2.json")
    json.dump(pred, open(out, "w"), indent=2)
    print(f"{pred['n_contrasts']} contrasts (v2 fixed-T)\n")
    print(f"{'id':7} {'coord':16} {'kind':8} {'Delta':>8} sign")
    for r in pred["predictions"]:
        print(f"{r['id']:7} {r['coord_name']:16} {r['kind']:8} {r['delta_pred']:+8.3f} {r['sign_pred']:+d}")
    print("\nStructural (v2):")
    for k, v in pred["structural"].items():
        print(f"  {k}: {v}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
