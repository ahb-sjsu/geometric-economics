#!/usr/bin/env python3
"""Grade prereg-menus-v1. Every bar lives here and nowhere else.

    python grade_menus.py results_menus_real.json
    python grade_menus.py results_menus_sim_RNG.json      # rehearsal (also ADD, RNG1, DN)
"""
from __future__ import annotations

import json
import sys

MOLTER_IQR = (0.3812, 0.7455)      # per-participant rho, Molter et al. 2022 (explore_molter3.json)
H4_CI_BOUNDS = (0.10, 0.90)        # the median's interval must exclude both pure absolute and full scaling
MAX_NONCONVERGED = 0.10


def grade(res):
    m = res["margin"]
    C = res["comparisons"]
    beats = lambda k: C[k]["ci_high"] < -m
    n_fits = res["participants"] * 5
    void = len(res["nonconverged_fits"]) > MAX_NONCONVERGED * n_fits
    r = res["rho_free"]
    h = {
        "H1 range scaling at Molter's exponent beats additive value on distractor trials": beats("RNG minus ADD"),
        "H2 it beats divisive normalisation": beats("RNG minus DN"),
        "H3 it beats full range normalisation (rho = 1)": beats("RNG minus RNG1"),
        "H4 universality: Gluth's median rho lies in Molter's interquartile range, interval inside (0.1, 0.9)":
            MOLTER_IQR[0] <= r["median"] <= MOLTER_IQR[1] and r["ci_low"] > H4_CI_BOUNDS[0] and r["ci_high"] < H4_CI_BOUNDS[1],
        "H5 square-root-to-Weber crossover": None,      # declared not assessable: menu ranges span a factor 5-6
    }
    show = lambda v: "NOT ASSESSABLE" if v is None else ("PASS" if v else "FAIL")
    return {"verdict": "VOID" if void else "GRADED", "nonconverged": len(res["nonconverged_fits"]),
            "predictions": {k: show(v) for k, v in h.items()},
            "numbers": {"margin": m, "test_nll": res["test_nll"], "comparisons": C, "rho_free": r}}


def rehearsal_check(res, out):
    p = {k.split()[0]: v for k, v in out["predictions"].items()}
    need = {"ADD": {"H1": ["FAIL"], "H4": ["FAIL"]},
            "RNG": {"H1": ["PASS"], "H2": ["PASS"], "H3": ["PASS"], "H4": ["PASS"]},
            "RNG1": {"H3": ["FAIL"]},
            "DN": {"H2": ["FAIL"]}}[res["simulation"]]
    bad = {k: p[k] for k, v in need.items() if p[k] not in v}
    if out["verdict"] == "VOID":
        bad["verdict"] = "VOID"
    return "OK" if not bad else f"FAILED under truth {res['simulation']}: {bad}"


if __name__ == "__main__":
    res = json.load(open(sys.argv[1]))
    out = grade(res)
    if res["simulation"]:
        out["rehearsal"] = rehearsal_check(res, out)
    print(json.dumps(out, indent=1))
