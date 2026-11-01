#!/usr/bin/env python3
"""Grader for prereg-boundary-v1. Written BEFORE any fit was run.

Reads results.json produced by boundary_fit.py and reports each of the six
registered predictions as PASS or FAIL against the frozen thresholds. The
thresholds live here and nowhere else, so the fitting code cannot see them.

Registered predictions, transcribed from prereg-boundary-v1.md Section 5,
frozen 2026-09-10, combined sha256
175bad98ac871fc4e6b8e7869ad1edca7cbe48876aa83ee17343cfbe968de2c0.

  P1  In M1, g > 0, and M1 improves on M0 by a likelihood-ratio test at
      alpha = 0.01.
  P2  M1s does not improve on M1: the LR test of g_SR = g_C = g_IN (2 df) is
      NOT rejected at alpha = 0.05. The ratio of largest to smallest g_s is
      reported with a bootstrap 95% CI and carries NO pass/fail threshold.
  P3  In M2, h is not significant at alpha = 0.05 and |h| < 0.25 per log10
      unit.
  P4  Leave-one-study-out: held-out log-loss of M1 is within 0.02 nats per
      decision of M1s fitted on the held-out study itself, for each of the
      three folds.
  P5  Model G attains held-out log-loss within 0.03 nats per decision of M1
      on every fold, with sigma_1^2 finite (upper bound 1e4).
  P6  Proposer slopes on log10(pie_days): IN slope < -3 pp per decade
      (prior, not a test); SR and C slopes within +/-1.5 pp per decade
      (95% CI excludes +/-3).
"""
from __future__ import annotations

import json
import math
import os
import sys

ALPHA_P1 = 0.01
ALPHA_P2 = 0.05
ALPHA_P3 = 0.05
H_BOUND_PER_LOG10 = 0.25
P4_MARGIN_NATS = 0.02
P5_MARGIN_NATS = 0.03
SIGMA1_UPPER_BOUND = 1e4
P6_POINT_BOUND_PP = 1.5
P6_CI_MARGIN_PP = 3.0
P6_PRIOR_IN_SLOPE_MAX = -3.0

HERE = os.path.dirname(os.path.abspath(__file__))


def grade(r: dict) -> dict:
    out = {}

    # ---- P1 -----------------------------------------------------------------
    g = r["M1"]["g"]
    p = r["lr_M0_vs_M1"]["p"]
    out["P1"] = {
        "verdict": "PASS" if (g > 0 and p < ALPHA_P1) else "FAIL",
        "g": g, "lr_p": p, "alpha": ALPHA_P1,
        "conditions": {"g_positive": g > 0, "lr_rejects": p < ALPHA_P1},
        "statement": "money enters acceptance through the responder's income units",
    }

    # ---- P2 -----------------------------------------------------------------
    p2 = r["lr_M1_vs_M1s"]["p"]
    out["P2"] = {
        "verdict": "PASS" if p2 >= ALPHA_P2 else "FAIL",
        "lr_p": p2, "alpha": ALPHA_P2, "df": r["lr_M1_vs_M1s"]["df"],
        "note": "PASS is NON-rejection. The registered simulation establishes "
                "size, not power against heterogeneity, so a pass is evidence "
                "consistent with one shared coordinate, not a demonstration.",
        "ratio_descriptive_no_threshold": r["M1s"].get("g_ratio"),
        "ratio_ci95_descriptive": r["M1s"].get("g_ratio_ci95"),
        "statement": "one monetary coordinate, not three",
    }

    # ---- P3 -----------------------------------------------------------------
    h = r["M2"]["h"]
    hp = r["M2"]["h_p"]
    h_log10 = h * math.log(10.0)  # M2 uses natural log; bound is per log10 unit
    ok3 = (hp >= ALPHA_P3) and (abs(h_log10) < H_BOUND_PER_LOG10)
    out["P3"] = {
        "verdict": "PASS" if ok3 else "FAIL",
        "h_natural_log": h, "h_per_log10": h_log10, "h_p": hp,
        "alpha": ALPHA_P3, "bound_per_log10": H_BOUND_PER_LOG10,
        "conditions": {"not_significant": hp >= ALPHA_P3,
                       "magnitude_under_bound": abs(h_log10) < H_BOUND_PER_LOG10},
        "statement": "nominal stake adds nothing given the offered amount and share",
    }

    # ---- P4 -----------------------------------------------------------------
    folds4, ok4 = [], True
    for f in r["cv"]:
        d = f["m1_heldout_logloss"] - f["m1s_own_logloss"]
        passed = d <= P4_MARGIN_NATS
        ok4 &= passed
        folds4.append({"held_out": f["held_out"], "m1": f["m1_heldout_logloss"],
                       "own": f["m1s_own_logloss"], "signed_diff": d,
                       "abs_diff": abs(d), "pass": passed})
    out["P4"] = {
        "verdict": "PASS" if ok4 else "FAIL",
        "margin_nats": P4_MARGIN_NATS, "folds": folds4,
        "reading": "'within 0.02 nats' is applied as 'not worse by more than "
                   "0.02', i.e. signed difference M1 minus own-fit <= 0.02. The "
                   "absolute difference is reported alongside; if the two "
                   "readings ever disagree, both are reported and the "
                   "disagreement disclosed.",
        "abs_reading_pass": all(abs(f["signed_diff"]) <= P4_MARGIN_NATS
                                for f in folds4),
        "statement": "the shared coordinate transfers across countries",
    }

    # ---- P5 -----------------------------------------------------------------
    folds5, ok5 = [], True
    for f in r["cv"]:
        d = f["g_heldout_logloss"] - f["m1_heldout_logloss"]
        passed = d <= P5_MARGIN_NATS
        ok5 &= passed
        folds5.append({"held_out": f["held_out"], "modelG": f["g_heldout_logloss"],
                       "m1": f["m1_heldout_logloss"], "signed_diff": d,
                       "pass": passed})
    s1 = r["modelG"]["sigma1_sq"]
    finite = s1 < SIGMA1_UPPER_BOUND
    out["P5"] = {
        "verdict": "PASS" if (ok5 and finite) else "FAIL",
        "margin_nats": P5_MARGIN_NATS, "folds": folds5,
        "sigma1_sq": s1, "sigma1_upper_bound": SIGMA1_UPPER_BOUND,
        "sigma1_finite": finite,
        "note": "sigma_1^2 at its bound means the income rescaling did no work "
                "and Model G has collapsed to Part I's responder; that is a "
                "failure on its own regardless of log-loss.",
        "statement": "the geometric responder matches the logit",
    }

    # ---- P6 -----------------------------------------------------------------
    prop, ok6 = {}, True
    for s in ("SR", "C"):
        e = r["proposer"][s]
        point_ok = abs(e["slope_pp_per_decade"]) <= P6_POINT_BOUND_PP
        ci_ok = (e["ci95_low"] > -P6_CI_MARGIN_PP) and (e["ci95_high"] < P6_CI_MARGIN_PP)
        ok6 &= point_ok and ci_ok
        prop[s] = {"slope_pp_per_decade": e["slope_pp_per_decade"],
                   "ci95": [e["ci95_low"], e["ci95_high"]],
                   "point_within_1p5": point_ok, "ci_excludes_3": ci_ok,
                   "pass": point_ok and ci_ok}
    inn = r["proposer"]["IN"]
    prop["IN"] = {"slope_pp_per_decade": inn["slope_pp_per_decade"],
                  "ci95": [inn["ci95_low"], inn["ci95_high"]],
                  "prior_holds": inn["slope_pp_per_decade"] < P6_PRIOR_IN_SLOPE_MAX,
                  "note": "registered as prior knowledge, NOT a test; reported only"}
    out["P6"] = {
        "verdict": "PASS" if ok6 else "FAIL",
        "point_bound_pp": P6_POINT_BOUND_PP, "ci_margin_pp": P6_CI_MARGIN_PP,
        "studies": prop,
        "statement": "the boundary is on the responder side",
    }

    return out


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results.json")
    r = json.load(open(path, encoding="utf-8"))
    g = grade(r)

    print("prereg-boundary-v1  ---  graded verdicts")
    print("frozen bundle sha256 "
          "175bad98ac871fc4e6b8e7869ad1edca7cbe48876aa83ee17343cfbe968de2c0")
    print()
    for k in ("P1", "P2", "P3", "P4", "P5", "P6"):
        print(f"  {k}  {g[k]['verdict']:4}  {g[k]['statement']}")
    print()
    n_pass = sum(1 for k in g if g[k]["verdict"] == "PASS")
    print(f"{n_pass} of 6 predictions pass. No composite verdict is registered; "
          f"each stands alone with its own falsifier.")

    outp = os.path.join(os.path.dirname(os.path.abspath(path)), "grade.json")
    json.dump(g, open(outp, "w", encoding="utf-8"), indent=2)
    print(f"\nwritten {outp}")


if __name__ == "__main__":
    main()
