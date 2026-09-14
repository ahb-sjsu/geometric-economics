#!/usr/bin/env python3
"""Grader for the transition study. Every bar lives here and nowhere else.

Written before any data exists. The analysis script computes numbers and decides
nothing. This file decides, and it can decide that the run is void.

HOW THE BARS ARE SET, GIVEN THAT THE NOISE SCALE IS NOT YET KNOWN

The design specifies bars as multiples of the between-family noise, because a bar
in absolute units measures its own tolerance. That mistake has been made twice in
this programme, once with a convergence threshold of `1e-6` that excluded
converged draws and once with a recovery tolerance of `0.06` against a standard
error of `0.101`.

So the registered quantity is the **multiplier**, fixed in this file now, before
any data. The **scale** is the between-family standard deviation measured by the
pilot, a sealed input and not a decision. Neither can be changed after the other
is known.

ARM B IS NOT REGISTERED IN v1, AND THIS FILE DOES NOT GRADE IT

The registration covers Arm A only. Arm B is built, from stimuli through task to
analysis, and collecting it is a separate decision that would need its own scale
and roughly doubles the sample. **P3 was a registered prediction in the draft and
has been removed**, before any data, rather than carried as a bar nobody intended
to test.

Arm B numbers are therefore NOT GRADED here. If a result carries them they are
reported back untouched and labelled unregistered, because silently dropping them
would hide a measurement and grading them would register a prediction after the
fact. Either would be worse than saying which it is.

The scale is still read per arm. Arm A prices in multiples of a gamble's spread
and Arm B in multiples of a permission's gain, so a scale file declares its arm
and this file refuses one that does not match. That guard is kept even with P3
gone, because a later registration may add the arm back and the file it would
read is the one being written now.

SIGN CONVENTION, DECLARED SO IT CANNOT BE CHOSEN LATER

`forward` is the direction that **acquires** a loss branch, moving from the state
with no loss branch to the mixed state. A positive excess therefore means a
participant requires more to acquire loss exposure than the control pairs
explain. That is the direction loss aversion predicts, and P2 tests it.

    python grade_transition.py results.json
"""
from __future__ import annotations

import json
import os
import sys

# ---------------------------------------------------------------------------
# REGISTERED BARS. Multipliers of the pilot's between-family standard deviation.
# ---------------------------------------------------------------------------
P1_MULTIPLIER = 2.5      # excess must exceed this many pilot sigmas
P2_DIRECTION = +1        # acquiring a loss branch costs more, not less
# P3 was here. It required arm B to exceed arm A, each standardised by its own
# between-family spread. REMOVED BEFORE ANY DATA, with arm B left out of this
# registration. Nothing in this file grades arm B.

# ---------------------------------------------------------------------------
# VOID CONDITIONS. Not predictions. A run failing any of these reports nothing.
# ---------------------------------------------------------------------------
V1_MIN_PRICE_SLOPE_Z = 3.0    # price must move choice, in the expected direction
V3_MAX_NONCONVERGED = 0.15    # share of staircases allowed to fail their rule
V4_EV_TOL = 0.02              # delivered stimuli, from build_stimuli.py
V4_SD_TOL = 0.02
V5_MAX_CONTROL_GAP = 3.0      # the two controls may not differ by more than
                              # this many pilot sigmas, or their mean is not
                              # a single quantity and subtracting it is unjustified
V6_MIN_FAMILIES = 40
V6_MIN_SHAPES = 20
V7_MAX_SINGLE_FAMILY_SHARE = 0.25   # no one family may carry this much of the
                                    # estimate, checked by leave-one-family-out

HERE = os.path.dirname(os.path.abspath(__file__))


def scale_path(arm):
    return os.path.join(HERE, "pilot_scale_arm_%s.json" % arm)


def pilot_sigma(arm, required=True):
    """The measured noise scale FOR ONE ARM. A sealed input, not a decision.

    Refuses a scale that did not come from human responses, that reports itself
    unusable, or that belongs to the other arm. Every bar in this file is a
    multiple of one of these numbers, so a scale computed from a simulation, or
    the wrong arm's scale, would set the study silently. `pilot_analysis.py`
    writes simulated runs to a rehearsal filename instead, and this is the other
    half of that guard.

    Returns None when `required` is false and the file is absent, which is how
    an unrun arm B reaches the grader.
    """
    # a file from before the split would be read as whichever arm asked for it
    stale = os.path.join(HERE, "pilot_scale.json")
    if os.path.exists(stale):
        raise AssertionError(
            "pilot_scale.json exists, from before the scale was split per arm. "
            "The arms do not share a unit. Rename it to pilot_scale_arm_A.json "
            "or pilot_scale_arm_B.json so it cannot be read as either.")
    p = scale_path(arm)
    if not os.path.exists(p):
        if required:
            raise AssertionError(
                "%s is missing. Arm %s cannot be graded without its own scale."
                % (os.path.basename(p), arm))
        return None
    with open(p, encoding="utf-8") as fh:
        doc = json.load(fh)
    prov = doc.get("provenance")
    if prov != "human":
        raise AssertionError(
            "%s has provenance %r and must be 'human'. Every bar is a multiple "
            "of this scale, so a simulated one would set the study without "
            "anyone choosing it." % (os.path.basename(p), prov))
    if not doc.get("usable", False):
        raise AssertionError(
            "%s reports usable false. Fix the instrument and repeat the pilot "
            "before sizing anything." % os.path.basename(p))
    got = doc.get("arm")
    if got != arm:
        raise AssertionError(
            "%s reports arm %r but was read as arm %r. Barring one arm with the "
            "other's noise is the error this split exists to prevent."
            % (os.path.basename(p), got, arm))
    return float(doc["between_family_sd"])


def grade(r, sigma):
    """Returns the verdict dict. `r` is the analysis output.

    `sigma` is arm A's between-family spread and sets P1, P2 and V5. There is no
    arm B bar: arm B is not registered in v1.
    """
    voids = []

    # V1, the instrument must respond to price in the expected direction
    z = r.get("price_slope_z")
    if z is None or z < V1_MIN_PRICE_SLOPE_Z:
        voids.append(
            "V1, price does not move choice in the expected direction. "
            "slope z is %s against a minimum of %.1f. A price that does not "
            "move acceptance, or moves it the wrong way, means the instrument "
            "is inverted and nothing downstream means anything."
            % (z, V1_MIN_PRICE_SLOPE_Z))

    # V2, the analysis invariance suite must have passed, self-test included
    inv = r.get("invariants", {})
    if not inv.get("all_pass"):
        voids.append("V2, the analysis invariance suite did not pass: %s"
                     % inv.get("checks"))
    elif not inv.get("checks", {}).get("I0_self_test"):
        voids.append("V2, the invariance suite passed but its self-test did "
                     "not, so it has never been shown to reject anything")

    # V3, staircase convergence
    nc = r.get("nonconverged_share")
    if nc is None or nc > V3_MAX_NONCONVERGED:
        voids.append("V3, %s of staircases failed their stopping rule against "
                     "a maximum of %.2f" % (nc, V3_MAX_NONCONVERGED))

    # V4, the delivered stimuli must satisfy their matching tolerances
    st = r.get("stimuli", {})
    if st.get("worst_ev_mismatch", 9e9) > V4_EV_TOL:
        voids.append("V4, delivered stimuli break the expected-value match, "
                     "worst %s against %.3f" % (st.get("worst_ev_mismatch"), V4_EV_TOL))
    if st.get("worst_sd_mismatch", 9e9) > V4_SD_TOL:
        voids.append("V4, delivered stimuli break the spread match, worst %s "
                     "against %.3f" % (st.get("worst_sd_mismatch"), V4_SD_TOL))

    # V5, the two controls must be one quantity
    gap = r.get("control_gap")
    if gap is None or abs(gap) > V5_MAX_CONTROL_GAP * sigma:
        voids.append(
            "V5, the two control pairs differ by %s, more than %.1f pilot "
            "sigmas. Their mean is then not a single quantity and subtracting "
            "it is unjustified." % (gap, V5_MAX_CONTROL_GAP))

    # V6, enough independent stimulus units
    nf, ns = r.get("n_families", 0), r.get("n_shapes", 0)
    if nf < V6_MIN_FAMILIES or ns < V6_MIN_SHAPES:
        voids.append("V6, %s families on %s shapes, below the minimum of %d and "
                     "%d. The effective sample is the stimulus unit, not the "
                     "trial count." % (nf, ns, V6_MIN_FAMILIES, V6_MIN_SHAPES))

    # V7, no single family may carry the estimate
    share = r.get("max_single_family_share")
    if share is None or share > V7_MAX_SINGLE_FAMILY_SHARE:
        voids.append("V7, one family moves the estimate by %s of itself when "
                     "removed, above %.2f" % (share, V7_MAX_SINGLE_FAMILY_SHARE))

    out = {
        "study": "transition study, arm A. arm B is built and not registered.",
        "pilot_between_family_sd": sigma,
        "bars": {"P1_multiplier": P1_MULTIPLIER, "P2_direction": P2_DIRECTION},
        "void": bool(voids),
        "void_reasons": voids,
    }
    if voids:
        out["verdict"] = "VOID"
        return out

    exA = r["arm_a"]["excess"]
    seA = r["arm_a"]["se"]
    exB = r.get("arm_b", {}).get("excess")

    p1 = exA > P1_MULTIPLIER * sigma
    p2 = (exA * P2_DIRECTION) > 0 and abs(exA) > 2.0 * seA

    out.update({
        "P1_penalty_exists": {
            "bar": "arm A excess > %.2f x %.4f = %.4f"
                   % (P1_MULTIPLIER, sigma, P1_MULTIPLIER * sigma),
            "value": exA, "pass": bool(p1)},
        "P2_direction": {
            "bar": "excess positive, meaning acquiring a loss branch costs "
                   "more, and beyond two of its own standard errors",
            "value": exA, "se": seA, "pass": bool(p2)},
        "arm_b": {
            "registered": False,
            "present": exB is not None,
            "excess": exB,
            "note": ("Arm B is not part of this registration. Its numbers are "
                     "reported unchanged and are NOT GRADED. Grading them would "
                     "register a prediction after the data, and omitting them "
                     "would hide a measurement.")
            if exB is not None else
                    ("Arm B is not part of this registration and was not "
                     "supplied.")},
        "verdict": "P1 %s, P2 %s" % (
            "PASS" if p1 else "FAIL",
            "PASS" if p2 else "FAIL"),
    })
    if not p1:
        out["F1"] = ("P1 failed. This design found no boundary-specific "
                     "component beyond what the control pairs explain. The "
                     "correct report is that it measured a switching cost and "
                     "nothing more, and that Chapter 6's asymmetry is not "
                     "detectable by this route.")
    if p1 and not p2:
        out["F2"] = ("P1 passed and P2 failed. An excess in the unexpected "
                     "direction is a finding about the sign of the penalty and "
                     "must be reported as one, not folded into P1.")
    return out


# ---------------------------------------------------------------------------
def _base_result():
    return {
        "price_slope_z": 8.4,
        "invariants": {"all_pass": True,
                       "checks": {"I0_self_test": True, "I1_direction_swap": True,
                                  "I4_switching_bias": True, "I6_clustering": True}},
        "nonconverged_share": 0.06,
        "stimuli": {"worst_ev_mismatch": 0.009, "worst_sd_mismatch": 0.0074},
        "control_gap": 0.10,
        "n_families": 160, "n_shapes": 35,
        "max_single_family_share": 0.04,
        "arm_a": {"excess": 0.52, "se": 0.05},
        "arm_b": {"excess": 0.95, "se": 0.07},
    }


def self_test():
    """The grader must VOID when it should. Each case breaks one condition."""
    import copy
    sigma = 0.12          # arm A's between-family spread
    print("SELF-TEST, the grader must void on each broken result")
    ok = True

    good = grade(_base_result(), sigma)
    if good["void"]:
        print("  FAIL, a clean result was voided: %s" % good["void_reasons"])
        ok = False
    else:
        print("  a clean result grades: %s" % good["verdict"])

    cases = [
        ("V1 price slope inverted", {"price_slope_z": -6.0}, "V1"),
        ("V1 price does not move choice", {"price_slope_z": 0.4}, "V1"),
        ("V2 invariants failed", {"invariants": {"all_pass": False, "checks": {}}}, "V2"),
        ("V2 suite passed but self-test did not",
         {"invariants": {"all_pass": True, "checks": {"I0_self_test": False}}}, "V2"),
        ("V3 too many staircases failed", {"nonconverged_share": 0.40}, "V3"),
        ("V4 stimuli break the match",
         {"stimuli": {"worst_ev_mismatch": 0.9, "worst_sd_mismatch": 0.0074}}, "V4"),
        ("V5 controls disagree", {"control_gap": 2.0}, "V5"),
        ("V6 too few stimulus units", {"n_families": 12, "n_shapes": 4}, "V6"),
        ("V7 one family carries it", {"max_single_family_share": 0.6}, "V7"),
    ]
    for label, patch, expect in cases:
        r = copy.deepcopy(_base_result())
        r.update(patch)
        v = grade(r, sigma)
        hit = v["void"] and any(x.startswith(expect) for x in v["void_reasons"])
        print("  %-38s -> %s" % (label, "VOIDED" if hit else "NOT VOIDED"))
        if not hit:
            print("       expected %s, got %s" % (expect, v.get("void_reasons")))
            ok = False

    # and the predictions must be able to fail on a clean run
    r = _base_result()
    r["arm_a"] = {"excess": 0.02, "se": 0.05}
    v = grade(r, sigma)
    f1 = (not v["void"]) and (not v["P1_penalty_exists"]["pass"]) and "F1" in v
    print("  %-38s -> %s" % ("a clean run with no penalty",
                             "F1 fires" if f1 else "F1 DID NOT FIRE"))
    ok = ok and f1

    # ARM B IS NOT REGISTERED. Its numbers must be neither graded nor hidden.
    v = grade(_base_result(), sigma)
    ab = v["arm_b"]
    shown = (ab["registered"] is False and ab["present"] is True
             and ab["excess"] == 0.95 and "NOT GRADED" in ab["note"]
             and "P3" not in v["verdict"])
    print("  %-38s -> %s" % ("arm B supplied, not registered",
                             "reported, not graded" if shown else "MISHANDLED"))
    ok = ok and shown

    r = _base_result()
    del r["arm_b"]
    v = grade(r, sigma)
    absent = v["arm_b"]["present"] is False and "P3" not in v["verdict"]
    print("  %-38s -> %s" % ("arm B absent",
                             "no bar, no verdict slot" if absent else "MISHANDLED"))
    ok = ok and absent

    r = _base_result()
    r["arm_a"] = {"excess": -0.60, "se": 0.05}
    v = grade(r, sigma)
    f2 = (not v["void"]) and ("F2" in v or not v["P2_direction"]["pass"])
    print("  %-38s -> %s" % ("a penalty in the wrong direction",
                             "reported as such" if f2 else "NOT REPORTED"))
    ok = ok and f2

    print("  SELF-TEST %s" % ("PASSED" if ok else "FAILED"))
    return ok


def main():
    if "--self-test" in sys.argv or len(sys.argv) == 1:
        ok = self_test()
        if len(sys.argv) == 1:
            print()
            print("no results file given, self-test only")
            return 0 if ok else 1
        if not ok:
            return 1
    path = sys.argv[1]
    with open(path, encoding="utf-8") as fh:
        r = json.load(fh)
    out = grade(r, pilot_sigma("A"))
    print(json.dumps(out, indent=2))
    with open(os.path.join(HERE, "grade_transition.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
