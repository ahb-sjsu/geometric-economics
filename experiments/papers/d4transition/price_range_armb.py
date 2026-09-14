#!/usr/bin/env python3
"""Arm B's price rows, chosen by measuring rather than by arguing.

WHERE THE ROWS HAVE TO SIT

Arm A's pairs are matched in expected value and spread, so a participant who
cares only about value prices every switch at zero, and the rows sit either side
of zero. Arm B's pairs are all worth exactly `v`, so the same participant prices
the forward switch at `v` and the backward switch at minus `v`. The rule is one
rule and arm A is the case where it is invisible.

    price row = (value difference) + (multiple) x (unit)

The value difference is `best(to) - best(from)`, which is `+v` forward and `-v`
backward. **It cancels out of the estimand.** The excess is one crossing
direction difference minus the mean of two control direction differences, and all
three pairs in a family carry the same `v`, so `2v - 2v = 0`. Where the rows sit
is a decision about where to spend rows, not a thing that can move the answer.

WHICH ROWS ARE DOMINATED, AND THE ONE I FIRST GOT BACKWARDS

A row is dominated when every participant gives the same answer whatever they
think of permissions.

    forward,  price below zero     paid to take the better state. everyone accepts.
    backward, price above zero     pay to take the worse state. everyone declines.

The first version of this file treated the rule as symmetric and capped the
multiples at plus and minus one, giving forward rows from zero to `2v`. That is
wrong at the far end. **A forward price above `v` is not dominated. It is the
whole measurement.** Paying more than the money is worth is exactly what a
premium on the permission looks like, and capping the rows at `2v` caps the
premium the instrument can see at one times the gain. The round trip found it:
fourteen percent of one cell hit an edge under a synthetic participant with a
direction effect of `0.4v`.

So the rows are asymmetric by direction, and each direction is the mirror of the
other.

    forward     from zero upward, with room above v for a premium
    backward    from zero downward, with room below -v for the same premium

A mirrored grid means the forward and backward lists quantise differently, so a
direction difference carries a grid bias. That bias is the same for all three
pairs in a family, and the estimand subtracts a control mean from the crossing
pair, so it cancels for the same reason the value does.

WHAT IS SWEPT

The direction effect is the thing being measured, so its size cannot be assumed
when choosing the range. It is swept alongside the noise, and a candidate is
usable only if it survives every combination. Rows in multiples of `v` also
assume the spread of prices scales with the stake, which the pilot can check
because a spread that does not scale shows up in the per-cell edge shares that
Section 7 of `PILOT.md` already computes.

    python price_range_armb.py
"""
from __future__ import annotations

import json
import os

import numpy as np

import pilot_analysis as P

HERE = os.path.dirname(os.path.abspath(__file__))

PAIRS = ("CROSS", "CTRL_LO", "CTRL_HI")

# component ratio carried over from arm A's sweep, rescaled to each assumed total
RATIO = np.array([0.30, 0.40, 0.50])
NOISE_LEVELS = (0.10, 0.25, 0.40)       # per-observation sd, in units of v
BIAS_LEVELS = (0.10, 0.40, 0.80)        # direction effect, in units of v
N_SEEDS = 5
EDGE_BUDGET = 0.15
BIAS_BUDGET = 12.0


def mirror(fwd):
    """The backward rows are the forward rows reflected through the centre."""
    return tuple(sorted((-x if x else 0.0) for x in fwd))


def rows(core, tail):
    """A symmetric fine core, plus a tail above the value difference only.

    The tail is where a premium on the permission would show up. It has no
    mirror image below, because a forward row below zero pays the participant to
    take the better state and has one sensible answer.
    """
    out = [0.0] + [x for c in core for x in (-c, c)] + list(tail)
    return tuple(sorted(out))


FINE = (0.12, 0.25, 0.45, 0.70, 1.00)
COARSE = (0.15, 0.35, 0.65, 1.00)

CANDIDATES = {
    # symmetric, the first attempt. kept so the table shows why it fails.
    "S1 symmetric +/-1.0v":  rows(FINE, ()),
    "S2 symmetric +/-1.5v":  rows(tuple(1.5 * x for x in FINE), ()),
    # asymmetric, room above v for a premium and none below zero
    "P1 fine, tail to 1.5v": rows(FINE, (1.5,)),
    "P2 fine, tail to 2.2v": rows(FINE, (1.5, 2.2)),
    "P3 fine, tail to 3.0v": rows(FINE, (1.5, 2.2, 3.0)),
    "P4 coarse, tail to 2.2v": rows(COARSE, (1.5, 2.2)),
}


# A price list can only measure a spread it can straddle. When the step where the
# switch lands is wide compared with the spread, the switch falls in the same
# interval whatever the family effect was, and THE SCALE COMES OUT LOW WITH
# NOTHING HITTING AN EDGE. That is the dangerous direction, because every bar in
# the confirmatory study is a multiple of the scale. The rule and its constant
# live in `pilot_analysis`, measured there rather than chosen, and this sweep
# asks the analysis itself whether it could resolve each combination rather than
# keeping a second copy of the rule.


def central_step(fwd):
    """The gap between adjacent rows at the centre of the grid, for reporting.

    The step that matters is the one where the switch lands, which is a fact
    about the participants and not about the design, so it is read from the
    analysis output. This is only the best case.
    """
    xs = sorted(fwd)
    i = xs.index(0.0)
    return min(xs[i + 1] - xs[i], xs[i] - xs[i - 1])


def dominated_share(fwd):
    """Rows with only one sensible answer, over both directions."""
    bwd = mirror(fwd)
    n = sum(1 for m in fwd if m < -1.0 - 1e-9) + sum(1 for m in bwd if m > 1.0 + 1e-9)
    return n / (len(fwd) + len(bwd))


def evaluate(fwd, total_sd, bias, seeds=N_SEEDS):
    """Worst-cell censoring and family-sd recovery, at one noise and one bias.

    The simulation works in DEVIATION FROM THE VALUE DIFFERENCE, which is the
    delivered prices shifted by a constant per cell. `read_list` is translation
    equivariant and the estimand is a difference of differences, so the shift
    changes nothing here. It is checked on the delivered prices in
    `roundtrip_check.py`.
    """
    comp = RATIO * (total_sd / float(np.sqrt((RATIO ** 2).sum())))
    sf, sp, sr = (float(x) for x in comp)
    rows = {"forward": list(fwd), "backward": list(mirror(fwd))}
    edge, fam_err, step, res = [], [], [], []
    for s in range(seeds):
        recs = P.simulate(n_fam=40, n_part=120, pairs=PAIRS,
                          sd_fam=sf, sd_part=sp, sd_res=sr,
                          switch_bias=bias, price_rows=rows, seed=300 + s)
        out = P.analyse(recs)
        edge.append(out["worst_cell_floor_ceiling"])
        fam_err.append(out["between_family_sd"] - sf)
        step.append(out["grid_step_median"])
        res.append(1.0 if out["checks"]["resolution_ok"] else 0.0)
    return {"rows": len(fwd),
            "worst_edge": float(np.mean(edge)),
            "family_bias_pct": float(100 * np.mean(fam_err) / sf),
            "grid_step": float(np.mean(step)),
            "resolution_ok": bool(np.mean(res) >= 0.5)}


def main():
    print("=" * 80)
    print("ARM B PRICE ROWS")
    print("=" * 80)
    print("rows are multiples of the family gain v, added to the value difference.")
    print("backward rows are the forward rows mirrored. a forward row below -1.0")
    print("and a backward row above +1.0 are DOMINATED and buy nothing.")
    print("%d seeds, 40 families and 120 participants each" % N_SEEDS)

    results = {}
    for bias in BIAS_LEVELS:
        for sd in NOISE_LEVELS:
            print()
            print("DIRECTION EFFECT %.2f v, PER-OBSERVATION SPREAD %.2f v" % (bias, sd))
            print("  candidate                          rows   dominated   worst edge   family bias")
            for name, fwd in CANDIDATES.items():
                r = evaluate(fwd, sd, bias)
                results["%s @b%.2f n%.2f" % (name, bias, sd)] = r
                flag = ""
                if not r["resolution_ok"]:
                    flag = "  CANNOT RESOLVE"
                elif r["worst_edge"] > EDGE_BUDGET:
                    flag = "  CENSORED"
                elif abs(r["family_bias_pct"]) > BIAS_BUDGET:
                    flag = "  biased"
                print("  %-33s %4d   %8.2f   %10.3f   %+10.1f%%%s"
                      % (name, r["rows"], dominated_share(fwd),
                         r["worst_edge"], r["family_bias_pct"], flag))

    print()
    print("=" * 80)
    print("READING THE TABLE")
    print("=" * 80)
    print("  a candidate is usable only if it holds at EVERY combination, because")
    print("  the direction effect is the estimand and its size is what is unknown.")
    ok, resolved = [], {}
    n_combos = len(BIAS_LEVELS) * len(NOISE_LEVELS)
    for name in CANDIDATES:
        all_rs = [results["%s @b%.2f n%.2f" % (name, b, n)]
                  for b in BIAS_LEVELS for n in NOISE_LEVELS]
        rs = [r for r in all_rs if r["resolution_ok"]]
        resolved[name] = len(rs)
        if rs and all(r["worst_edge"] <= EDGE_BUDGET
                      and abs(r["family_bias_pct"]) <= BIAS_BUDGET for r in rs):
            ok.append(name)
    print("  A combination the ANALYSIS ITSELF reports it cannot resolve is left")
    print("  out of that rule and counted instead, because a spread finer than")
    print("  the step where the switch lands cannot be measured by any short")
    print("  list. The pilot refuses such a scale rather than reporting it.")
    print()
    print("  candidate                          best-case step   resolved")
    for name, fwd in CANDIDATES.items():
        print("  %-33s %12.2f v %8d of %d"
              % (name, central_step(fwd), resolved[name], n_combos))
    print()
    chosen = None
    if not ok:
        print("  NO CANDIDATE SURVIVES EVERY COMBINATION.")
        def worst(n):
            return max(results["%s @b%.2f n%.2f" % (n, b, s)]["worst_edge"]
                       for b in BIAS_LEVELS for s in NOISE_LEVELS)
        for n in sorted(CANDIDATES, key=worst)[:3]:
            print("    %-33s worst edge anywhere %.3f" % (n, worst(n)))
    else:
        print("  usable everywhere: %s" % ", ".join(sorted(ok)))
        # the two failure modes first, then cost, as in arm A's sweep. the
        # resolution floor comes before the row count because attenuation is
        # the failure that reports nothing.
        # the two failure modes first, then cost, as in arm A's sweep. what a
        # row set can resolve comes before its length, because attenuation is
        # the failure that reports nothing.
        best = min(ok, key=lambda n: (dominated_share(CANDIDATES[n]),
                                      -resolved[n], len(CANDIDATES[n])))
        print("  no dominated rows, then most combinations resolved, then")
        print("  fewest rows: %s" % best)
        fwd = CANDIDATES[best]
        print()
        print("  adopted forward multiples of v")
        print("    %s" % ", ".join("%+.2f" % x for x in fwd))
        print("  adopted backward multiples of v")
        print("    %s" % ", ".join("%+.2f" % x for x in mirror(fwd)))
        print("  forward prices run %.2fv to %.2fv, backward %.2fv to %.2fv"
              % (1 + fwd[0], 1 + fwd[-1], -1 + mirror(fwd)[0], -1 + mirror(fwd)[-1]))
        print("  headroom above the money value: %.1f times the gain" % fwd[-1])
        worst_edge = max(results["%s @b%.2f n%.2f" % (best, b, s)]["worst_edge"]
                         for b in BIAS_LEVELS for s in NOISE_LEVELS)
        print("  worst cell at an edge, anywhere in the sweep: %.3f" % worst_edge)
        print("  combinations the analysis could resolve: %d of %d"
              % (resolved[best], n_combos))
        chosen = {"name": best, "forward_multiples_of_v": list(fwd),
                  "centre_step_in_v": central_step(fwd),
                  "combinations_resolved": resolved[best],
                  "backward_multiples_of_v": list(mirror(fwd)),
                  "dominated_share": dominated_share(fwd),
                  "worst_edge_anywhere": worst_edge,
                  "cells": {k: v for k, v in results.items() if k.startswith(best)}}

    with open(os.path.join(HERE, "price_range_armb.json"), "w",
              encoding="utf-8") as fh:
        json.dump({"noise_levels_in_v": list(NOISE_LEVELS),
                   "bias_levels_in_v": list(BIAS_LEVELS),
                   "component_ratio": list(RATIO), "n_seeds": N_SEEDS,
                   "edge_budget": EDGE_BUDGET, "bias_budget_pct": BIAS_BUDGET,
                   "candidates": {k: list(v) for k, v in CANDIDATES.items()},
                   "results": results, "chosen": chosen}, fh, indent=2)
    print()
    print("written price_range_armb.json")
    return 0 if chosen else 1


if __name__ == "__main__":
    raise SystemExit(main())
