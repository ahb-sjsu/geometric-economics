#!/usr/bin/env python3
"""Forward-prediction registry -- hashed, timestamped sign-predictions that later
history can verify.

Each prediction records where the geometry and scalar economics DIVERGE on a
non-monetary coordinate, before the event resolves. The `frozen` part of every
entry is sha256-hashed (same scheme as llmpanel.prereg); the hash + registration
timestamp prove the prediction was not back-fit after the outcome. Resolutions are
appended later WITHOUT changing the frozen prediction or its hash.

    python registry.py            # (re)compute registry.lock.json + summary
    python registry.py --verify   # verify every frozen prediction hash still matches

Scope: sign-level only; mechanism-level; no grand macro forecasts (see LEDGER scope).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRED = os.path.join(HERE, "predictions.json")
LOCK = os.path.join(HERE, "registry.lock.json")


def _canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def sha256(obj) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()


def load() -> dict:
    with open(PRED, encoding="utf-8") as f:
        return json.load(f)


def build_lock(data: dict) -> dict:
    per = {}
    for p in data["predictions"]:
        per[p["id"]] = sha256(p["frozen"])
    return {
        "registry": "projection-gap forward predictions v1",
        "n_predictions": len(data["predictions"]),
        "open": sum(1 for p in data["predictions"] if p.get("status") == "open"),
        "resolved": sum(1 for p in data["predictions"] if p.get("status") == "resolved"),
        "per_prediction_sha256": per,
        "combined_sha256": sha256(per),
    }


def verify(data: dict, lock: dict) -> bool:
    ok = True
    for p in data["predictions"]:
        h = sha256(p["frozen"])
        stored = lock["per_prediction_sha256"].get(p["id"])
        if h != stored:
            print(f"  MISMATCH {p['id']}: frozen prediction changed since registration!")
            ok = False
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    data = load()

    if a.verify:
        if not os.path.exists(LOCK):
            print("no lock yet; run without --verify first"); return 1
        lock = json.load(open(LOCK, encoding="utf-8"))
        good = verify(data, lock)
        print("all frozen predictions intact" if good else "REGISTRY TAMPERED")
        return 0 if good else 2

    lock = build_lock(data)
    with open(LOCK, "w", encoding="utf-8") as f:
        json.dump(lock, f, indent=2)
    print(f"{lock['n_predictions']} predictions "
          f"({lock['open']} open, {lock['resolved']} resolved)")
    for p in data["predictions"]:
        fr = p["frozen"]
        print(f"\n[{p['id']}] {p['status']}  (registered {fr['registered']})")
        print(f"  claim:   {fr['claim']}")
        print(f"  scalar:  {fr['scalar_prediction']}")
        print(f"  geom:    {fr['geometry_prediction']}  (coord d{fr['coordinate']})")
        print(f"  resolve: {fr['resolution_criterion']}")
        print(f"  sha256:  {lock['per_prediction_sha256'][p['id']][:16]}...")
    print(f"\ncombined sha256: {lock['combined_sha256']}")
    print(f"wrote {LOCK}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
