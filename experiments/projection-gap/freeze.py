#!/usr/bin/env python3
"""Freeze the pre-registration: hash the frozen model + contrasts + predictions.

Writes prereg.lock.json with a sha256 over the canonical serialization of every
input that could bias the result if changed after seeing data:
  - the frozen geometric-model constants (Sigma, temperature),
  - the full contrast set (prompts + option displacements),
  - the computed no-refit predictions (signs + magnitudes + structural claims).

After running this, commit and tag `prereg-v1`. Any later change to the model,
contrasts, or predictions changes the hash and voids the pre-registration --
exactly the CHSH `_selftest` discipline, applied to a confirmatory economics run.

Usage:
    python predict.py            # (re)generate predictions.json
    python freeze.py --stamp 2026-07-04T00:00:00Z
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os

import contrasts as K
import geometric_model as G

HERE = os.path.dirname(os.path.abspath(__file__))


def _canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def _sha256(obj) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stamp", required=True, help="ISO-8601 UTC timestamp (frozen externally)")
    a = ap.parse_args()

    pred_path = os.path.join(HERE, "predictions.json")
    if not os.path.exists(pred_path):
        print("run predict.py first"); return 1
    predictions = json.load(open(pred_path, encoding="utf-8"))

    model = {"SIGMA2": G.SIGMA2, "T_BASE": G.T_BASE, "T_ALPHA": G.T_ALPHA,
             "T_FLOOR": G.T_FLOOR, "ACTIVE": list(G.ACTIVE)}
    contrast_records = K.as_records()

    components = {
        "model": _sha256(model),
        "contrasts": _sha256(contrast_records),
        "predictions": _sha256(predictions),
    }
    combined = _sha256(components)

    lock = {
        "prereg": "projection-gap v1",
        "frozen_at": a.stamp,
        "combined_sha256": combined,
        "component_sha256": components,
        "counts": {
            "contrasts": len(contrast_records),
            "real": sum(1 for c in contrast_records if c["kind"] == "real"),
            "placebo": sum(1 for c in contrast_records if c["kind"] == "placebo"),
            "dose": sum(1 for c in contrast_records if c["kind"] == "dose"),
        },
        "primary_hypothesis": "sign(Delta_obs)=sign(Delta_pred) for all real contrasts; scalar null Delta=0",
        "sharp_predictions": [
            "loss-domain d9 sign reversal (B1 vs B1L)",
            "non-monotone PEAKED dose-response, max at level 2 (cost-gap ~1.4)",
            "placebos Delta=0",
        ],
        "note": "Commit this file and tag prereg-v1 BEFORE running any LLM-panel subject.",
    }
    out = os.path.join(HERE, "prereg.lock.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(lock, f, indent=2)
    print(f"combined sha256: {combined}")
    print(f"  model:       {components['model']}")
    print(f"  contrasts:   {components['contrasts']}")
    print(f"  predictions: {components['predictions']}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
