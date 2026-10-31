#!/usr/bin/env python3
"""Grade prereg-psych101-v1. Every bar lives here and nowhere else.

    python grade_psych101.py results_real.json      # the registered grade
    python grade_psych101.py results_sim_gdt.json   # rehearsal
    python grade_psych101.py results_sim_cpt.json   # rehearsal
"""
from __future__ import annotations

import json
import sys

GRADED_NATIVE = ("EV", "GDT")   # native fits a graded prediction depends on (H1, H4)


def grade(res: dict) -> dict:
    void = [f"V2 native {k} did not converge" for k in GRADED_NATIVE if not res["converged"][k]]
    c, m, a = res["test_comparisons"], res["margin"], res["angle"]
    dd = res["loss_domain"]["GDT-CPT_with_loss_minus_gains_only"]
    h = {
        "H1 frozen GDT beats expected value refit on this corpus":
            c["GDT_transfer-EV_native"]["ci_high"] < -m,
        "H2 frozen GDT beats frozen linear random utility":
            c["GDT_transfer-RUM_transfer"]["ci_high"] < -m,
        "H3 frozen CPT beats frozen GDT (Part II's ordering replicates)":
            c["CPT_transfer-GDT_transfer"]["ci_high"] < -m,
        "H4 the CPC18 aversion angle lies inside this corpus's 95% interval":
            a["native_ci_low"] <= a["frozen_ratio"] <= a["native_ci_high"],
        "H5 GDT's deficit to CPT is larger on problems with a loss":
            dd["ci_low"] > m,
    }
    return {"void": void, "verdict": "VOID" if void else "GRADED",
            "predictions": {k: ("PASS" if v else "FAIL") for k, v in h.items()},
            "numbers": {"margin": m, "test_nll": res["test_nll"], "comparisons": c,
                        "angle": a, "loss_domain_dd": dd, "kappa": res["kappa"],
                        "transfer_efficiency": res["transfer_efficiency"]}}


def rehearsal_check(res: dict, out: dict) -> str:
    """The chain must not hand CPT a win it did not earn, nor deny it one it did."""
    p = {k.split()[0]: v for k, v in out["predictions"].items()}
    if res["simulation"]["truth"] == "gdt":
        ok = p["H3"] == "FAIL" and p["H4"] == "PASS" and p["H1"] == "PASS"
        return "OK" if ok else "FAILED: under a GDT truth the chain must find GDT's angle and not prefer CPT"
    ok = p["H3"] == "PASS"
    return "OK" if ok else "FAILED: under a CPT truth the chain must prefer CPT"


def main() -> None:
    res = json.load(open(sys.argv[1]))
    out = grade(res)
    if res["simulation"]:
        out["rehearsal"] = rehearsal_check(res, out)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
