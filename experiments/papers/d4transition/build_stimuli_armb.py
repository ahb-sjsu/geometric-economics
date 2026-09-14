#!/usr/bin/env python3
"""Arm B stimuli. Permission boundaries, matched on value to Arm A's logic.

`DESIGN.md` Section 4 describes the arm and does not say what its controls are.
Working that out is most of the design, and the answer decides whether the arm
measures anything.

WHAT THE CONTROL HAS TO BE

Arm A's controls hold expected value and spread fixed and differ only in whether
a loss branch exists. The analogue here is not "a permission change that does not
change permissions", which is not a thing. It is **the same value gain delivered
without the permitted set changing**.

So a participant faces actions with known payoffs and takes the best one they are
permitted to take. Let `a < b` be two permitted payoffs and `v` the gain under
test.

    L0   permits {A, B}      payoffs (a, b)          best b
    L1   permits {A, B}      payoffs (a, b+v)        best b+v     B improved
    H1   permits {A, B, C}   payoffs (a, b, b+v)     best b+v     C newly permitted
    H2   permits {A, B, C}   payoffs (a, b, b+2v)    best b+2v    C improved

    CROSS     (L0, H1)   gains v BY GAINING A PERMISSION
    CTRL_LO   (L0, L1)   gains v by improving an action already permitted
    CTRL_HI   (H1, H2)   gains v by improving an action already permitted

**All three are worth exactly `v`. Only the first changes the permitted set.** The
excess over the two controls is therefore the part of the price that attaches to
the permission rather than to the money.

WHY THE PAYOFFS ARE CERTAIN RATHER THAN RISKY

An earlier sketch gave the actions uncertain payoffs so a permission would carry
option value. That introduces a confound the design cannot remove. Valuing an
option is harder than valuing a bonus, so a difference between the crossing pair
and the controls could be a difference in arithmetic rather than in permissions.
With certain payoffs every pair is the same sum, "the best I may take goes from
`X` to `X + v`", and the only thing that differs is how it got there.

A CLOSED ACTION HAS TO BE VISIBLE

If action `C` simply did not appear in `L0`, then moving to `H1` would look like
a new option arriving, which is what `CTRL_LO` already does when `B` improves.
There would be no boundary on the screen to cross. So every state shows every
action with its payoff, and marks which of them the participant may take.

That makes the contrast exact.

    CROSS     opens `C`. **Not one number on the board changes.**
    CTRL_LO   raises `B` by `v`. `C` stays closed at the same number.
    CTRL_HI   raises `C` by `v`. Nothing opens or closes.

The cost of showing a closed action is that some of what it measures may be a
response to being refused rather than to the permission itself. That is the
construct, not a confound. What would be a confound is a participant who never
saw the boundary.

**Arm B reuses Arm A's analysis unchanged.** The pair names are the same three,
the excess is the same subtraction, and the clustering unit is still the family.
Nothing in `pilot_analysis.py`, `analysis_invariants.py` or `grade_transition.py`
needs to know which arm produced a record.

    python build_stimuli_armb.py
"""
from __future__ import annotations

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

ACTIONS = ("A", "B", "C")

MIN_GAP = 2.0        # permitted payoffs must be legibly apart
MIN_V = 1.0          # the gain under test must be legible
MAX_PAYOFF = 200.0
DECIMALS = 2


def build_family(a, b, v, name):
    """Four states with the structure above, or a reason it is not usable."""
    if b - a < MIN_GAP:
        return None, "the two base payoffs are less than %.1f apart" % MIN_GAP
    if v < MIN_V:
        return None, "the gain is below %.1f" % MIN_V
    if b + 2 * v > MAX_PAYOFF:
        return None, "payoffs exceed %.0f" % MAX_PAYOFF
    # C must beat B once permitted, or the elevation is nominal
    if v <= 0:
        return None, "the newly permitted action is not better"
    r = lambda x: round(x, DECIMALS)
    # Every state carries a payoff for every action. `permits` says which of them
    # the participant may take. A closed action is SHOWN with its payoff and
    # marked closed, for the reason in the module docstring.
    states = {
        "L0": {"permits": ["A", "B"],
               "payoffs": {"A": r(a), "B": r(b), "C": r(b + v)}},
        "L1": {"permits": ["A", "B"],
               "payoffs": {"A": r(a), "B": r(b + v), "C": r(b + v)}},
        "H1": {"permits": ["A", "B", "C"],
               "payoffs": {"A": r(a), "B": r(b), "C": r(b + v)}},
        "H2": {"permits": ["A", "B", "C"],
               "payoffs": {"A": r(a), "B": r(b), "C": r(b + 2 * v)}},
    }
    return {"name": name, "a": a, "b": b, "v": v, "arm": "B",
            "actions": ACTIONS,
            "states": states,
            "pairs": {"CROSS": ["L0", "H1"],
                      "CTRL_LO": ["L0", "L1"],
                      "CTRL_HI": ["H1", "H2"]}}, None


def best(state):
    """The payoff of the best action the participant is permitted to take.

    Tolerant of a malformed state, because `check_family` must be able to REPORT
    that a state permits an action with no payoff rather than crash on it. A
    checker that raises where it should reject tells you nothing about the
    stimulus.
    """
    vals = [state["payoffs"][k] for k in state["permits"] if k in state["payoffs"]]
    return max(vals) if vals else float("nan")


def best_action(state):
    vals = {k: state["payoffs"][k] for k in state["permits"]
            if k in state["payoffs"]}
    if not vals:
        return []
    top = max(vals.values())
    winners = [k for k, x in vals.items() if abs(x - top) < 1e-9]
    return winners


def check_family(fam):
    """Every requirement, on the delivered rounded values."""
    fails = []
    S = fam["states"]
    v = fam["v"]

    # 0, structural validity. every permitted action must have a payoff, or
    # nothing below can be computed and the state is meaningless.
    for k, st in S.items():
        missing = [x for x in st["permits"] if x not in st["payoffs"]]
        if missing:
            fails.append("%s permits %s with no payoff" % (k, ", ".join(missing)))

    # 0b, the board must be complete. an action with no payoff cannot be shown,
    # and an action that is not shown is not a boundary the participant can see.
    for k, st in S.items():
        absent = [x for x in fam["actions"] if x not in st["payoffs"]]
        if absent:
            fails.append("%s does not display %s" % (k, ", ".join(absent)))

    # a structurally broken board makes every check below meaningless, and a
    # checker that raises where it should report tells you nothing.
    if fails:
        return fails

    # 1, every pair is worth exactly v
    for pname, (x, y) in fam["pairs"].items():
        gain = best(S[y]) - best(S[x])
        if abs(gain - v) > 10 ** (-DECIMALS) * 1.01:
            fails.append("%s is worth %.4f, not the family's %.4f"
                         % (pname, gain, v))

    # 2, the crossing pair changes the permitted set and the controls do not
    x, y = fam["pairs"]["CROSS"]
    if set(S[x]["permits"]) == set(S[y]["permits"]):
        fails.append("CROSS does not change the permitted set")
    for pname in ("CTRL_LO", "CTRL_HI"):
        x, y = fam["pairs"][pname]
        if set(S[x]["permits"]) != set(S[y]["permits"]):
            fails.append("%s changes the permitted set and must not" % pname)

    # 3, the elevation must not be nominal. the newly permitted action has to be
    # the one the participant would actually take.
    lo, hi = fam["pairs"]["CROSS"]
    new = set(S[hi]["permits"]) - set(S[lo]["permits"])
    if not new:
        fails.append("CROSS adds no action")
    elif not (set(best_action(S[hi])) & new):
        fails.append("the newly permitted action is not the best one, so the "
                     "elevation is nominal")

    # 4, no ties, which would make the best action ambiguous
    for k, st in S.items():
        if len(best_action(st)) > 1:
            fails.append("%s has a tie for the best permitted action" % k)

    # 5, the crossing pair changes the PERMITTED SET AND NOTHING ELSE. if a
    # payoff moved as well, the price would be paid for money and permission
    # together and the two could not be told apart.
    lo, hi = fam["pairs"]["CROSS"]
    if S[lo]["payoffs"] != S[hi]["payoffs"]:
        diff = [x for x in fam["actions"]
                if S[lo]["payoffs"].get(x) != S[hi]["payoffs"].get(x)]
        fails.append("CROSS also changes the payoff of %s, so the price would "
                     "buy money and permission at once" % ", ".join(diff))

    # 6, the closed action must be worth having before it opens, or the
    # participant is being offered a permission with nothing behind it
    closed = [x for x in fam["actions"] if x not in S[lo]["permits"]]
    for x in closed:
        if S[lo]["payoffs"][x] <= best(S[lo]):
            fails.append("%s is closed in %s and pays no more than what is "
                         "already open" % (x, lo))

    # 7, payoffs legible and in range
    for k, st in S.items():
        for act, val in st["payoffs"].items():
            if val <= 0 or val > MAX_PAYOFF:
                fails.append("%s action %s pays %.2f, outside the usable range"
                             % (k, act, val))
    return fails


def self_test():
    print("SELF-TEST, the checker must reject deliberately broken families")
    ok = True
    good, err = build_family(8.0, 20.0, 5.0, "selftest")
    assert good is not None, err
    f = check_family(good)
    if f:
        print("  FAIL, a valid family was rejected: %s" % f)
        ok = False
    else:
        print("  a valid family passes")

    import copy
    cases = [
        ("a control given a different permitted set",
         lambda x: x["states"]["L1"]["permits"].append("C"),
         "must not"),
        ("a state permitting an action with no payoff",
         lambda x: x["states"]["L0"]["permits"].append("D"),
         "with no payoff"),
        ("a state not displaying one of the actions",
         lambda x: x["states"]["L0"]["payoffs"].pop("C"),
         "does not display"),
        ("the crossing pair moving a payoff as well",
         lambda x: x["states"]["H1"]["payoffs"].__setitem__("B", 9.5),
         "buy money and permission at once"),
        ("the closed action worth no more than what is open",
         lambda x: (x["states"]["L0"]["payoffs"].__setitem__("C", 3.0),
                    x["states"]["H1"]["payoffs"].__setitem__("C", 3.0)),
         "pays no more than what is already open"),
        ("the crossing pair made not to cross",
         lambda x: x["states"]["H1"].__setitem__("permits", ["A", "B"]),
         "does not change the permitted set"),
        ("the elevation made nominal",
         lambda x: x["states"]["H1"]["payoffs"].__setitem__("C", 1.0),
         "nominal"),
        ("a pair worth the wrong amount",
         lambda x: x["states"]["L1"]["payoffs"].__setitem__("B", 99.0),
         "is worth"),
        ("a tie for the best action",
         lambda x: x["states"]["L0"]["payoffs"].__setitem__("A", x["states"]["L0"]["payoffs"]["B"]),
         "tie"),
    ]
    for label, break_it, expect in cases:
        fam = copy.deepcopy(good)
        break_it(fam)
        fails = check_family(fam)
        hit = any(expect in s for s in fails)
        print("  %-42s -> %s" % (label, "rejected" if hit else "NOT REJECTED"))
        if not hit:
            print("       expected %r, got %s" % (expect, fails))
            ok = False
    print("  SELF-TEST %s" % ("PASSED" if ok else "FAILED"))
    return ok


def main():
    if not self_test():
        return 1
    print()
    print("=" * 74)
    print("BUILDING ARM B FAMILIES")
    print("=" * 74)
    fams, rejected = [], []
    for a in (5.0, 8.0, 12.0):
        for b in (18.0, 25.0, 35.0, 50.0):
            for v in (2.0, 4.0, 7.0, 12.0, 20.0):
                name = "b_a%02d_b%02d_v%02d" % (a, b, v)
                fam, err = build_family(a, b, v, name)
                if fam is None:
                    rejected.append((name, err))
                    continue
                f = check_family(fam)
                if f:
                    rejected.append((name, "; ".join(f)))
                    continue
                fams.append(fam)
    print("  constructed %d families, rejected %d" % (len(fams), len(rejected)))

    # v relative to the base is what a participant plausibly responds to
    ratios = sorted({round(f["v"] / f["b"], 3) for f in fams})
    print("  gain as a fraction of the base payoff spans %.3f to %.3f over %d values"
          % (min(ratios), max(ratios), len(ratios)))

    f = fams[len(fams) // 2]
    print()
    print("  example family %s, gain %.2f" % (f["name"], f["v"]))
    print("    state  permits      payoffs                     best")
    for k in ("L0", "L1", "H1", "H2"):
        st = f["states"][k]
        pays = ", ".join("%s %.2f" % (x, st["payoffs"][x])
                         for x in sorted(st["payoffs"]))
        print("    %-5s  %-11s  %-26s  %.2f"
              % (k, "".join(st["permits"]), pays, best(st)))
    print("    pairs, each worth exactly %.2f" % f["v"])
    for pn, (x, y) in f["pairs"].items():
        print("      %-8s %s to %s   %s"
              % (pn, x, y,
                 "PERMISSION GAIN" if pn == "CROSS" else "payoff improvement"))

    out = {"note": "arm B stimuli, permission boundaries, not yet registered",
           "arm": "B", "n_families": len(fams), "n_rejected": len(rejected),
           "clustering_unit": "family", "families": fams}
    with open(os.path.join(HERE, "stimuli_armb.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("  CLUSTERING UNIT is the family, as in arm A, because the three")
    print("  pairs share states.")
    print()
    print("written stimuli_armb.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
