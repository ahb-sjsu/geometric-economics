#!/usr/bin/env python3
"""Grade prereg-strata-v1. Every bar lives here and nowhere else.

    python grade_strata.py results_strata_real.json
    python grade_strata.py results_strata_sim_GDTS.json     # rehearsal (also GDT2, CPT_unit, GDTC)
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAJORITY = 3                 # of the five test corpora
H2_POINT, H2_FLOOR = 0.5, 0.25
H5_MIN = 4
H7_MIN_SHIFT, H7_MIN_CORPORA = 0.05, 3
V5_MIN_DP = 0.005            # mean |p_GDTC - p_GDTS| over test stimuli, frozen parameters


def grade(res):
    frozen = json.load(open(os.path.join(HERE, "frozen_strata.json")))
    rec = json.load(open(os.path.join(HERE, "recovery_v4.json")))
    void = [f"V2 frozen {m} did not converge" for m, v in frozen["models"].items() if not v["converged"]]
    consumer_void = bool(rec["V4_void"])
    P, m = res["pooled"], res["pooled"]["margin"]
    beats = lambda k: P[k]["ci_high"] < -m
    h = {}
    h["H1 stratified beats two-number, pooled and in a majority"] = beats("GDTS-GDT2") and P["GDTS-GDT2"]["corpora_won"] >= MAJORITY
    if beats("CPT-GDT2"):
        g = P["gap_closed"]
        h["H2 at least half the gap to CPT closes"] = g["point"] is not None and g["point"] >= H2_POINT and g["ci_low"] > H2_FLOOR
    else:
        h["H2 at least half the gap to CPT closes"] = None
    h["H3 stratified beats CPT, pooled"] = beats("GDTS-CPT")
    s = res["stake_invariance"]
    h["H4 people move with stake less than the two-number model predicts"] = (s["ci_low"] > 0) if s["assessable"] else None
    eff = res["effects"]
    nS = sum(v["reproduced"] for v in eff["GDTS"].values())
    n2 = sum(v["reproduced"] for v in eff["GDT2"].values())
    h[f"H5 stratified reproduces >= {H5_MIN} of 6 effects and more than two-number ({nS} vs {n2})"] = nS >= H5_MIN and nS > n2
    if consumer_void:
        h["H6 consumer beats stratified"] = h["H7 distortions move as predicted from stimuli"] = h["H8 consumer reproduces the rare-event effects"] = "VOID (V4)"
    else:
        dp = sum(c["consumer_vs_stratified_mean_abs_dp"] for c in res["corpora"].values()) / len(res["corpora"])
        h["H6 consumer beats stratified"] = ((beats("GDTC-GDTS") and P["GDTC-GDTS"]["corpora_won"] >= MAJORITY)
                                             if dp >= V5_MIN_DP else None)
        g0 = res["gamma_cpc18"]
        rows = []
        for name, c in res["corpora"].items():
            pred = c["gamma"]["predicted"] - g0["predicted"]
            obs = c["gamma"]["observed"] - g0["observed"]
            if abs(pred) > H7_MIN_SHIFT:
                rows.append((name, pred, obs))
        h["H7 distortions shift between corpora as the frozen geometric model predicts from stimuli"] = (all((p > 0) == (o > 0) for _, p, o in rows)
                                                              if len(rows) >= H7_MIN_CORPORA else None)
        h["H8 consumer reproduces the rare-event effects"] = (eff["GDTC"]["possibility_gains"]["reproduced"]
                                                             and eff["GDTC"]["insurance_losses"]["reproduced"])
    show = lambda v: v if isinstance(v, str) else ("NOT ASSESSABLE" if v is None else ("PASS" if v else "FAIL"))
    return {"void": void, "verdict": "VOID" if void else "GRADED", "consumer_arm_void": consumer_void,
            "predictions": {k: show(v) for k, v in h.items()},
            "numbers": {"pooled": P, "stake_invariance": s,
                        "effects_reproduced": {mm: [e for e, v in vv.items() if v["reproduced"]] for mm, vv in eff.items()},
                        "gamma": {"cpc18": res["gamma_cpc18"], **{n: c["gamma"] for n, c in res["corpora"].items()}},
                        "test_nll": {n: c["test_nll"] for n, c in res["corpora"].items()},
                        "cpt_coding": {n: c["cpt_coding"] for n, c in res["corpora"].items()}}}


def rehearsal_check(res, out):
    p = {k.split()[0]: v for k, v in out["predictions"].items()}
    t = res["simulation"]
    need = {"GDTS": {"H1": ["PASS"], "H3": ["PASS"], "H6": ["FAIL", "NOT ASSESSABLE"]},
            "GDT2": {"H1": ["FAIL"]},
            "CPT_unit": {"H3": ["FAIL"], "H7": ["FAIL", "NOT ASSESSABLE"]},
            "GDTC": {"H6": ["PASS", "NOT ASSESSABLE"]}}[t]
    bad = {k: p[k] for k, v in need.items() if p[k] not in v}
    return "OK" if not bad else f"FAILED under truth {t}: {bad}"


if __name__ == "__main__":
    res = json.load(open(sys.argv[1]))
    out = grade(res)
    if res["simulation"]:
        out["rehearsal"] = rehearsal_check(res, out)
    print(json.dumps(out, indent=1))
