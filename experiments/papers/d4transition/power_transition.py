#!/usr/bin/env python3
"""Power and size for the transition study, WITHOUT needing the pilot first.

Section 11 of the registration read PENDING THE PILOT, and the document called it
the only thing between the draft and a seal. It does not have to be.

THE SCALE CANCELS

P1's bar is `excess > P1_MULTIPLIER x sigma_fam`, where `sigma_fam` is the
between-family standard deviation of the excess, so the bar is stated in the same
units as the quantity and the absolute scale never enters. Write the excess for
participant `j` in family `i` as

    excess_ij = d * sigma_fam + a_i + b_j + e_ij

with variances `var_fam`, `var_part`, `var_res`, and `d` the true effect in units
of `sigma_fam`. The estimator averages within family then across families and
resamples FAMILIES, so with `r = (var_part + var_res) / var_fam`,

    SE = sigma_fam * sqrt(1 + r/k) / sqrt(n_fam)

**`sigma_fam` is in the bar and in the estimate alike and divides out.** Only the
RATIO `r` and the design numbers are needed, so Section 11 is answerable now,
before any data, which is the safer order: the multipliers are frozen before
anything about the scale is known. The pilot measures `r`, which says which column
of the table the study is in, and checks whether the instrument works at all. It
cannot move a multiplier and it cannot move a sample size, because the sizes are
tabulated across `r` in advance.

WHAT THIS CALCULATION FOUND, WHICH IS THE REASON TO DO IT

**P1's bar is an EFFECT-SIZE bar, and sample size very nearly cannot buy it.**
Power to clear it is `Phi((d - P1_MULTIPLIER) * sqrt(n_fam) / sqrt(1 + r/k))`, so
it goes to one when `d > 2.5` and to zero when `d < 2.5`, and `n_fam` only
sharpens the step, it does not move it. Adding families to reach P1 is not an
option the design has. Either the true excess is more than two and a half
between-family spreads or P1 fails, and no sample makes that false.

So **the study is sized on P2**, whose bar is the ordinary one, the estimate
beyond two of its own standard errors. P2's power does rise with `n_fam` in the
usual way, and it is what a modest true effect can actually clear.

This is worth stating in the registration rather than buried here, because a
reader who sees P1 fail should know the sample was never what stood in its way.

THE ALGEBRA IS CHECKED, NOT TRUSTED

Closed forms in this programme have been wrong before. Both are verified against
Monte Carlo using the estimator the study actually uses, a mean of family means
with a family-clustered bootstrap, and they must agree.

    python power_transition.py
"""
from __future__ import annotations

import json
import math
import os

import numpy as np

import grade_transition as G

HERE = os.path.dirname(os.path.abspath(__file__))

FAM_PER_PARTICIPANT = 3            # PILOT.md Section 4
R_GRID = (1.0, 3.0, 6.0, 10.0)     # (var_part + var_res) / var_fam
K = 6                              # participants per family
TARGETS = (0.80, 0.90)
B_BOOT = 300
N_SIM = 800

P1_D_GRID = (2.0, 2.4, 2.6, 3.0, 3.5)      # around the bar, to show the step
P2_D_GRID = (0.20, 0.35, 0.50, 1.00)       # what P2 can actually reach


def _phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def se_units(r, k, n_fam):
    """SE of the estimate, in units of sigma_fam."""
    return math.sqrt(1.0 + r / k) / math.sqrt(n_fam)


def power_p1(d, r, k, n_fam):
    return _phi((d - G.P1_MULTIPLIER) / se_units(r, k, n_fam))


def power_p2(d, r, k, n_fam):
    """P(estimate beyond two of its own standard errors, correct sign).

    Normal approximation with the SE treated as known, which the bootstrap with
    this many families is close to. The Monte Carlo check uses the bootstrap SE
    itself, so any optimism in that assumption shows up there.
    """
    nc = d / se_units(r, k, n_fam)
    return _phi(nc - 2.0) - _phi(-nc - 2.0)


def n_needed(fn, d, r, k, target, cap=100000):
    lo, hi = 4, 64
    while hi < cap and fn(d, r, k, hi) < target:
        hi *= 2
    if fn(d, r, k, hi) < target:
        return None
    while lo < hi:
        mid = (lo + hi) // 2
        if fn(d, r, k, mid) >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo


def simulate_once(d, r, k, n_fam, sigma_fam, rng):
    var_fam = sigma_fam ** 2
    rest = r * var_fam
    w = np.array([0.40, 0.50]) ** 2          # split as arm A's sweep assumed
    var_part, var_res = rest * w / w.sum()
    a = rng.normal(0, math.sqrt(var_fam), n_fam)
    b = rng.normal(0, math.sqrt(var_part), (n_fam, k))
    e = rng.normal(0, math.sqrt(var_res), (n_fam, k))
    fam_means = d * sigma_fam + a + (b + e).mean(axis=1)
    point = float(fam_means.mean())
    idx = rng.integers(0, n_fam, size=(B_BOOT, n_fam))
    return point, float(fam_means[idx].mean(axis=1).std(ddof=1))


def power_mc(d, r, k, n_fam, sigma_fam, seed, n_sim=N_SIM):
    rng = np.random.default_rng(seed)
    bar = G.P1_MULTIPLIER * sigma_fam
    p1 = p2 = 0
    for _ in range(n_sim):
        point, se = simulate_once(d, r, k, n_fam, sigma_fam, rng)
        if point > bar:
            p1 += 1
        if point * G.P2_DIRECTION > 0 and abs(point) > 2.0 * se:
            p2 += 1
    return p1 / n_sim, p2 / n_sim


def main():
    print("=" * 78)
    print("POWER AND SIZE")
    print("=" * 78)
    print("bars: P1 excess > %.2f sigma_fam, P2 correct sign beyond two of its"
          % G.P1_MULTIPLIER)
    print("own standard errors. d is the true excess in units of sigma_fam.")
    print("r = (var_part + var_res) / var_fam. sigma_fam CANCELS throughout.")

    print()
    print("CHECK, closed forms against Monte Carlo with the real estimator")
    print("     d     r  n_fam   P1 closed     MC    P2 closed     MC   sigma_fam")
    worst, rows = 0.0, []
    for (d, r, n_fam, sig) in ((2.6, 3.0, 40, 0.30), (2.4, 6.0, 80, 1.00),
                               (0.35, 3.0, 60, 0.05), (0.50, 10.0, 120, 2.50)):
        c1, c2 = power_p1(d, r, K, n_fam), power_p2(d, r, K, n_fam)
        m1, m2 = power_mc(d, r, K, n_fam, sig, seed=11 + n_fam)
        worst = max(worst, abs(c1 - m1), abs(c2 - m2))
        rows.append({"d": d, "r": r, "n_fam": n_fam, "sigma_fam": sig,
                     "p1_closed": c1, "p1_mc": m1,
                     "p2_closed": c2, "p2_mc": m2})
        print("  %5.2f %5.1f  %5d      %6.3f %6.3f       %6.3f %6.3f      %.2f"
              % (d, r, n_fam, c1, m1, c2, m2, sig))
    ok = worst < 0.05
    print("  worst disagreement %.3f against a bar of 0.05 -> %s"
          % (worst, "AGREE" if ok else "DISAGREE, the algebra is wrong"))
    print("  sigma_fam runs 0.05 to 2.50 above and the closed forms do not take")
    print("  it as an argument. That is the cancellation, shown rather than said.")
    if not ok:
        return 1

    print()
    print("P1 IS AN EFFECT-SIZE BAR. n_fam SHARPENS THE STEP, IT DOES NOT MOVE IT.")
    print("  power to clear P1, at r = 6")
    print("      d      n=40    n=80   n=160   n=640")
    p1_tab = {}
    for d in P1_D_GRID:
        cells = [power_p1(d, 6.0, K, n) for n in (40, 80, 160, 640)]
        p1_tab["d%.1f" % d] = cells
        print("    %.1f   %7.3f %7.3f %7.3f %7.3f" % (d, *cells))
    print("  Below the bar more families make P1 LESS likely to pass, not more.")
    print("  There is no sample size that rescues a true effect under %.2f."
          % G.P1_MULTIPLIER)

    print()
    print("SO THE STUDY IS SIZED ON P2. Families needed, %d participants each." % K)
    p2_tab = {}
    for target in TARGETS:
        print()
        print("  power %.0f%%" % (100 * target))
        print("      d        r=1     r=3     r=6    r=10")
        for d in P2_D_GRID:
            cells = [n_needed(power_p2, d, r, K, target) for r in R_GRID]
            for r, c in zip(R_GRID, cells):
                p2_tab["d%.2f_r%.0f_p%.0f" % (d, r, 100 * target)] = c
            print("    %.2f  %8s%8s%8s%8s"
                  % (d, *["%d" % c if c else "   -" for c in cells]))

    print()
    print("=" * 78)
    print("THE REGISTERED SAMPLE")
    print("=" * 78)
    with open(os.path.join(HERE, "stimuli.json"), encoding="utf-8") as fh:
        stim = json.load(fh)
    available = stim["n_families"]

    # SIZE FOR THE WORST r IN THE TABLE, not the middle one. The pilot measures
    # r, and a sample sized at the middle would have to be revised upward if the
    # pilot came back high. Revising a sample after a measurement is how a
    # design starts negotiating with its data, so the number is chosen now
    # against the least favourable case the table covers.
    d_reg, r_worst, target = 0.50, max(R_GRID), 0.90
    n_reg = max(n_needed(power_p2, d_reg, r_worst, K, target), G.V6_MIN_FAMILIES)
    feasible = n_reg <= available
    participants = math.ceil(n_reg * K / FAM_PER_PARTICIPANT)

    print("  Sized on P2, at d = %.2f sigma_fam and the WORST r in the table,"
          % d_reg)
    print("  r = %.0f, so that whatever the pilot finds the sample stands."
          % r_worst)
    print("    families needed        %d" % n_reg)
    print("    V6 floor               %d" % G.V6_MIN_FAMILIES)
    print("    families available     %d  -> %s"
          % (available, "fits" if feasible else "DOES NOT FIT"))
    print("    REGISTERED: %d families, %d participants per family, %d participants"
          % (n_reg, K, participants))
    print()
    print("  What that sample reaches at 90% power, by what the pilot finds:")
    print("      r      smallest d detectable")
    reach = {}
    for r in R_GRID:
        lo, hi = 0.0, 5.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if power_p2(mid, r, K, n_reg) >= target:
                hi = mid
            else:
                lo = mid
        reach["r%.0f" % r] = hi
        print("    %5.1f      %.3f sigma_fam" % (r, hi))
    print()
    print("  P1 is not sized, because it cannot be. It passes if the true excess")
    print("  exceeds %.2f sigma_fam and fails otherwise, and this sample only"
          % G.P1_MULTIPLIER)
    print("  makes that verdict sharp. A reader seeing P1 fail should know the")
    print("  sample was never what stood in its way.")
    if not feasible:
        print()
        print("  THE DESIGN CANNOT SUPPLY THIS SAMPLE. Report that, do not lower")
        print("  a bar. The multipliers are registered.")

    out = {"note": "power for the transition study, arm A. sigma_fam cancels.",
           "bars": {"P1_multiplier": G.P1_MULTIPLIER,
                    "P2_direction": G.P2_DIRECTION},
           "k_participants_per_family": K,
           "fam_per_participant": FAM_PER_PARTICIPANT,
           "r_grid": list(R_GRID),
           "closed_form_vs_monte_carlo": rows,
           "worst_disagreement": worst,
           "p1_is_effect_size_bar": p1_tab,
           "p2_families_needed": p2_tab,
           "registered_n_families": n_reg,
           "registered_participants": participants,
           "registered_target": {"d": d_reg, "r": r_worst, "power": target},
           "families_available": available,
           "feasible": feasible,
           "smallest_d_detectable_at_90pct": reach}
    with open(os.path.join(HERE, "power_transition.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written power_transition.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
