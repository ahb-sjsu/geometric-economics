#!/usr/bin/env python3
"""Stimulus construction for the transition study, with every match verified.

Builds families of four two-outcome states such that all four have **exactly** the
same expected value and **exactly** the same standard deviation, and differ only
in the probability of the high outcome. Three pairs are drawn from each family,
one that crosses the loss-branch boundary and two that do not, and all three have
the **same probability separation**, so the crossing pair differs from the
controls in the crossing and in nothing else the construction can control.

THE ALGEBRA, WHICH IS WHY THE MATCHING IS EXACT RATHER THAN APPROXIMATE

For a two-outcome state `(H, p, L)` with `H >= L`,

    EV = p H + (1 - p) L
    SD = sqrt(p (1 - p)) (H - L)

so for a target mean `mu` and spread `sigma`, every probability gives exactly one
state,

    R = sigma / sqrt(p (1 - p))
    L = mu - p R
    H = mu + (1 - p) R

and the stratum is decided by the sign of `L`,

    L >= 0   <=>   mu / sigma >= sqrt(p / (1 - p))   <=>   p <= p_star

with `p_star = mu^2 / (mu^2 + sigma^2)`. **At fixed mean and spread the
probability alone decides whether a loss branch exists.** So a family is specified
by `p_star`, a spacing, and a scale, and the four states sit at

    p_star - 3d,  p_star - d,  p_star + d,  p_star + 3d

the first two with no loss branch and the last two mixed. The three pairs are

    CROSS    (p_star - d, p_star + d)    crosses the boundary
    CTRL_G   (p_star - 3d, p_star - d)   both unmixed
    CTRL_M   (p_star + d, p_star + 3d)   both mixed

and each has a probability separation of exactly `2d`.

THE CONFOUND THIS FIXES, which the design document did not have

Because the stratum is decided by probability at fixed mean and spread, a crossing
pair necessarily differs in probability. Without matched controls that difference
is confounded with the crossing. Matching the separation across all three pair
types is what makes the subtraction in the design's Section 5 remove it.

WHAT ROUNDING DOES, AND WHY IT IS CHECKED AFTER

Participants are shown rounded numbers. Rounding breaks exact matching, so every
match is re-verified **on the delivered rounded values** and the worst residual is
reported rather than assumed small. A construction that verifies only the
unrounded values is checking something the participant never sees.

    python build_stimuli.py
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

DECIMALS = 2          # what the participant is shown
EV_TOL = 0.02         # after rounding, per pair
SD_TOL = 0.02         # after rounding, per pair
MIN_ABS_OUTCOME = 0.5     # no outcome smaller than this in magnitude
MIN_SEAM_LOG_RATIO = 0.10  # keep |H| / |L| away from 1, the q discontinuity
P_MIN, P_MAX = 0.08, 0.92  # keep probabilities off the extremes


def state(mu, sigma, p):
    """The unique two-outcome state with this mean, spread and probability."""
    R = sigma / math.sqrt(p * (1.0 - p))
    return {"H": mu + (1.0 - p) * R, "p": p, "L": mu - p * R}


def ev_sd(H, p, L):
    ev = p * H + (1.0 - p) * L
    var = p * (1 - p) * (H - L) ** 2
    return ev, math.sqrt(max(var, 0.0))


def rounded(s):
    return {"H": round(s["H"], DECIMALS), "p": round(s["p"], 4),
            "L": round(s["L"], DECIMALS)}


def has_loss(s):
    return min(s["H"], s["L"]) < 0


def has_gain(s):
    return max(s["H"], s["L"]) > 0


def build_family(p_star, d, sigma, name):
    """Four states, exact in EV and SD, straddling the boundary at p_star."""
    mu = sigma * math.sqrt(p_star / (1.0 - p_star))
    ps = [p_star - 3 * d, p_star - d, p_star + d, p_star + 3 * d]
    if not all(P_MIN <= p <= P_MAX for p in ps):
        return None, "probability outside the usable range"
    raw = [state(mu, sigma, p) for p in ps]
    out = [rounded(s) for s in raw]
    fam = {"name": name, "p_star": p_star, "d": d, "sigma": sigma, "mu": mu,
           "states": {"G2": out[0], "G1": out[1], "M1": out[2], "M2": out[3]},
           "states_exact": {"G2": raw[0], "G1": raw[1], "M1": raw[2],
                            "M2": raw[3]}}
    fam["pairs"] = {
        "CROSS": ["G1", "M1"],
        "CTRL_G": ["G2", "G1"],
        "CTRL_M": ["M1", "M2"],
    }
    return fam, None


def check_family(fam):
    """Every requirement, verified on the DELIVERED rounded values.

    Returns a list of failures. An empty list is the only acceptable result.
    """
    fails = []
    S = fam["states"]

    # 1 and 2, EV and SD matched within every pair, after rounding
    stats = {k: ev_sd(v["H"], v["p"], v["L"]) for k, v in S.items()}
    for pname, (a, b) in fam["pairs"].items():
        dev = abs(stats[a][0] - stats[b][0])
        dsd = abs(stats[a][1] - stats[b][1])
        if dev > EV_TOL:
            fails.append("%s EV mismatch %.4f exceeds %.4f" % (pname, dev, EV_TOL))
        if dsd > SD_TOL:
            fails.append("%s SD mismatch %.4f exceeds %.4f" % (pname, dsd, SD_TOL))

    # 3, the crossing pair crosses, exactly one side has a loss branch
    a, b = fam["pairs"]["CROSS"]
    if has_loss(S[a]) == has_loss(S[b]):
        fails.append("CROSS does not cross, both states on the same side")
    if not has_gain(S[a]) or not has_gain(S[b]):
        fails.append("CROSS contains a state with no gain branch")

    # 4, the controls do not cross
    for pname in ("CTRL_G", "CTRL_M"):
        a, b = fam["pairs"][pname]
        if has_loss(S[a]) != has_loss(S[b]):
            fails.append("%s crosses the boundary and must not" % pname)

    # 5, probability separation identical across pair types
    seps = {k: abs(S[a]["p"] - S[b]["p"]) for k, (a, b) in fam["pairs"].items()}
    if max(seps.values()) - min(seps.values()) > 1e-6:
        fails.append("probability separations differ across pairs %s" % seps)

    # 6 and 7, degenerate states
    for k, v in S.items():
        if abs(v["H"] - v["L"]) < 1e-9:
            fails.append("%s has zero spread" % k)
        if abs(v["H"]) < MIN_ABS_OUTCOME or abs(v["L"]) < MIN_ABS_OUTCOME:
            fails.append("%s has an outcome below the minimum magnitude" % k)

    # 8, keep away from the |H| = |L| seam, where the salience coordinate jumps
    for k, v in S.items():
        if abs(v["L"]) > 1e-12:
            lr = abs(math.log10(abs(v["H"]) / abs(v["L"])))
            if lr < MIN_SEAM_LOG_RATIO:
                fails.append("%s sits within %.3f of the |H| = |L| seam" % (k, lr))

    # 9, probabilities usable
    for k, v in S.items():
        if not (P_MIN <= v["p"] <= P_MAX):
            fails.append("%s probability %.3f outside the usable range"
                         % (k, v["p"]))
    return fails


def self_test():
    """The constructor must REJECT families that are deliberately broken.

    A check that has never been shown to fail is not a check. Each case below
    breaks exactly one requirement and the corresponding failure must appear.
    """
    print("SELF-TEST, the checker must reject deliberately broken families")
    ok = True
    good, err = build_family(0.50, 0.08, 20.0, "selftest")
    assert good is not None, err
    if check_family(good):
        print("  FAIL, a valid family was rejected: %s" % check_family(good))
        ok = False
    else:
        print("  a valid family passes")

    import copy
    cases = [
        ("EV broken", lambda f: f["states"]["M1"].update({"H": f["states"]["M1"]["H"] + 5.0}),
         "EV mismatch"),
        ("control made to cross", lambda f: f["states"]["G2"].update({"L": -abs(f["states"]["G2"]["L"]) - 1.0}),
         "crosses the boundary"),
        ("separation broken", lambda f: f["states"]["M2"].update({"p": f["states"]["M2"]["p"] + 0.05}),
         "probability separations differ"),
        ("crossing pair made not to cross",
         lambda f: f["states"]["M1"].update({"L": abs(f["states"]["M1"]["L"])}),
         "does not cross"),
        ("pushed onto the |H| = |L| seam",
         lambda f: f["states"]["M1"].update({"L": -abs(f["states"]["M1"]["H"])}),
         "seam"),
    ]
    for label, break_it, expect in cases:
        f = copy.deepcopy(good)
        break_it(f)
        fails = check_family(f)
        hit = any(expect in x for x in fails)
        print("  %-34s -> %s" % (label, "rejected" if hit else "NOT REJECTED"))
        if not hit:
            print("       expected a failure containing %r, got %s" % (expect, fails))
            ok = False
    print("  SELF-TEST %s" % ("PASSED" if ok else "FAILED"))
    return ok


def main():
    if not self_test():
        print()
        print("the checker does not reject known-bad families, so it licenses")
        print("nothing. no stimuli written.")
        return 1

    print()
    print("=" * 74)
    print("BUILDING FAMILIES")
    print("=" * 74)
    fams, rejected = [], []
    # p_star sets where the boundary sits, d the separation, sigma the scale
    for p_star in (0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70,
                   0.75, 0.80):
        for d in (0.03, 0.05, 0.07, 0.09, 0.11, 0.13):
            for sigma in (5.0, 10.0, 20.0, 40.0, 80.0):
                name = "f_p%02d_d%02d_s%02d" % (p_star * 100, d * 100, sigma)
                fam, err = build_family(p_star, d, sigma, name)
                if fam is None:
                    rejected.append((name, err))
                    continue
                fails = check_family(fam)
                if fails:
                    rejected.append((name, "; ".join(fails)))
                    continue
                fams.append(fam)

    print("  constructed %d families, rejected %d" % (len(fams), len(rejected)))
    if rejected:
        print("  rejection reasons, first six")
        for n, r in rejected[:6]:
            print("    %-20s %s" % (n, r[:70]))

    if not fams:
        print("  no families survived the checks")
        return 1

    # worst residual after rounding, reported rather than assumed
    worst_ev = worst_sd = 0.0
    for f in fams:
        st = {k: ev_sd(v["H"], v["p"], v["L"]) for k, v in f["states"].items()}
        for a, b in f["pairs"].values():
            worst_ev = max(worst_ev, abs(st[a][0] - st[b][0]))
            worst_sd = max(worst_sd, abs(st[a][1] - st[b][1]))
    print()
    print("  worst EV mismatch after rounding  %.4f   tolerance %.4f"
          % (worst_ev, EV_TOL))
    print("  worst SD mismatch after rounding  %.4f   tolerance %.4f"
          % (worst_sd, SD_TOL))

    print()
    print("  example family")
    f = fams[len(fams) // 2]
    print("    %s   p_star %.2f   separation %.2f   sigma %.1f   mu %.2f"
          % (f["name"], f["p_star"], 2 * f["d"], f["sigma"], f["mu"]))
    print("    state      H        p        L       EV       SD    loss branch")
    for k in ("G2", "G1", "M1", "M2"):
        v = f["states"][k]
        e, s = ev_sd(v["H"], v["p"], v["L"])
        print("    %-5s %8.2f  %6.3f %8.2f %8.2f %8.2f    %s"
              % (k, v["H"], v["p"], v["L"], e, s,
                 "yes" if has_loss(v) else "no"))
    print("    pairs   CROSS %s   CTRL_G %s   CTRL_M %s"
          % (f["pairs"]["CROSS"], f["pairs"]["CTRL_G"], f["pairs"]["CTRL_M"]))

    # the clustering unit, stated here because the power section depends on it
    shapes = sorted({(f["p_star"], f["d"]) for f in fams})
    print()
    print("  CLUSTERING UNIT. The three pairs of a family share states, so they")
    print("  are not independent. Every interval must resample FAMILIES, of")
    print("  which there are %d, and not pairs or trials." % len(fams))
    print()
    print("  AND A CAUTION ABOUT WHAT IS INDEPENDENT. Families sharing a shape")
    print("  and differing only in scale are the same design in different units,")
    print("  so they are more alike than two independently drawn families.")
    print("  %d families rest on %d distinct shapes. Treat the shape count as"
          % (len(fams), len(shapes)))
    print("  the conservative effective sample and report both.")

    out = {"note": "stimulus set for the transition study, not yet registered",
           "decimals": DECIMALS, "ev_tolerance": EV_TOL, "sd_tolerance": SD_TOL,
           "worst_ev_mismatch": worst_ev, "worst_sd_mismatch": worst_sd,
           "n_families": len(fams), "n_rejected": len(rejected),
           "n_distinct_shapes": len(shapes),
           "shapes": [[a, b] for a, b in shapes],
           "clustering_unit": "family",
           "families": fams}
    with open(os.path.join(HERE, "stimuli.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written stimuli.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
