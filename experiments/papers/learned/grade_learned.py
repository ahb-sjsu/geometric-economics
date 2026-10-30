#!/usr/bin/env python3
"""Grade prereg-learned-v1. Every bar lives here and nowhere else.

    python grade_learned.py results_labse.json            # the registered grade
    python grade_learned.py results_sim_gdt2_labse.json   # rehearsal
    python grade_learned.py results_sim_lin_labse.json    # rehearsal

Only the LaBSE run is graded. The BGE-M3 run is reported beside it, ungraded.
"""
from __future__ import annotations

import json
import sys

REGISTERED_ENCODER = "sentence-transformers/LaBSE"
REGISTERED_SNAPSHOT = "836121a0533e5664b21c7aacc5d22951f2b8b25b"
K_MAX_LOW_RANK = 8
TRANSFER_TARGETS = ["A1.1", "A1.2", "A2.1", "A3.1", "B1.1"]  # placebo-corrected significant, all observed +
TRANSFER_MIN = 4


def grade(res: dict) -> dict:
    void = []
    if res["simulation"] is None:
        if res["encoder"]["model"] != REGISTERED_ENCODER:
            return {"verdict": "NOT GRADED", "why": "only the registered encoder is graded"}
        if res["encoder"]["snapshot"] != REGISTERED_SNAPSHOT:
            void.append("V1 encoder snapshot differs from the registered one")
    for name, g in res["selected"].items():
        if name != "M0" and not g["converged"]:
            void.append(f"V2 selected {name} did not converge")

    c = res["test_comparisons"]
    m = res["margin"]  # 1% of LIN's dev gain over M0, fixed before test
    h = {
        "H1 learned coordinates beat the codebook coordinates":
            c["GDT-ANCHOR"]["ci_high"] < -m,
        "H2 a learned metric beats a learned linear scalar":
            c["GDT-LIN"]["ci_high"] < -m,
        "H3 the learned metric is low rank (k* <= 8)":
            res["k_star"] is not None and res["k_star"] <= K_MAX_LOW_RANK,
        "H4 the learned span contains the codebook axes beyond chance":
            res["alignment"]["stat"] > res["alignment"]["null_p99"],
    }
    preds = {r["id"]: r["pred"] for r in res["panel_transfer"]["GDT"]}
    hits = sum(1 for t in TRANSFER_TARGETS if preds[t] > 0)
    h[f"H5 zero-fit sign transfer to the panel ({hits}/5, need {TRANSFER_MIN})"] = hits >= TRANSFER_MIN
    return {"void": void, "verdict": "VOID" if void else "GRADED",
            "predictions": {k: ("PASS" if v else "FAIL") for k, v in h.items()},
            "numbers": {"k_star": res["k_star"], "margin": m, "test_nll": res["test_nll"],
                        "comparisons": c, "alignment": {k: res["alignment"][k] for k in ("stat", "null_p99")},
                        "panel_pred": preds}}


def main() -> None:
    res = json.load(open(sys.argv[1]))
    out = grade(res)
    if res["simulation"]:
        out["rehearsal"] = rehearsal_check(res, out)
    print(json.dumps(out, indent=1))


def rehearsal_check(res: dict, out: dict) -> str:
    """The chain must find structure when it is there and not invent it when it is not."""
    p = out["predictions"]
    h2 = next(v for k, v in p.items() if k.startswith("H2"))
    if res["simulation"]["truth"] == "gdt2":
        ok = h2 == "PASS" and res["k_star"] in (1, 2, 4)
        return "OK" if ok else "FAILED: chain missed a rank-2 metric that is there"
    ok = h2 == "FAIL"
    return "OK" if ok else "FAILED: chain preferred a metric when the truth is linear"


if __name__ == "__main__":
    main()
