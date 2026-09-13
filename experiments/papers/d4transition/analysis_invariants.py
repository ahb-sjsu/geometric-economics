#!/usr/bin/env python3
"""Invariance suite for the transition study analysis, with a self-test.

Written **before any data exists**, which is the only time it can be written
honestly. It tests the analysis pipeline rather than its inputs.

`prereg-d4stability-v1` was void because its design matrix was oriented against
its outcome, and every check that registration carried passed, because each tested
a component and the defect was in a relationship between two components. The
lesson is that wiring errors are caught by transformations whose effect on the
answer is known in advance, and by nothing else.

The pipeline under test is short. For each participant, family, pair and
direction there is an indifference price. From those,

    D(pair)  = price(forward) - price(backward)
    excess   = D(CROSS) - mean( D(CTRL_G), D(CTRL_M) )

and the interval on `excess` comes from resampling FAMILIES.

THE INVARIANTS

    I1  DIRECTION SWAP. Relabel which direction is forward, everywhere. Every
        direction difference must NEGATE exactly and so must the excess. A
        pipeline that does not is not measuring direction.

    I2  PARTICIPANT PERMUTATION. Permute participant identifiers. Every estimate
        must be bit-identical. Catches any accidental dependence on order.

    I3  PRICE RESCALING. Multiply every price by a positive constant. The excess
        must scale by that constant and the ratio of excess to its own standard
        error must be UNCHANGED. Catches unit errors.

    I4  SWITCHING BIAS. Add an asymmetric switching cost to every pair, which is
        the confound the design exists to defeat. Every raw direction difference
        must move and **the excess must not**. This is the formal statement that
        the controls do their job, and it is the most important invariant here.

    I5  PLANT. Generate responses from a known penalty on the crossing pair and
        nothing elsewhere, push them through the whole pipeline, recover it.
        Judged in standard errors, because a bar in absolute units measures its
        own tolerance.

    I6  CLUSTERING. Duplicate every observation within its family, leaving the
        number of families unchanged. The family-resampled interval must be
        essentially unchanged. A trial-level interval would shrink by about the
        square root of two, and the test reports both so the difference is
        visible.

    I0  SELF-TEST. Three deliberately broken pipelines, each caught by a
        different invariant. A suite never shown to reject anything licenses
        nothing, and three distinct failures show the invariants are not
        redundant.

    python analysis_invariants.py
"""
from __future__ import annotations

import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20260913
B_BOOT = 400
PAIRS = ("CROSS", "CTRL_G", "CTRL_M")


# ----------------------------------------------------------------------------
# the reference pipeline
# ----------------------------------------------------------------------------
def direction_differences(rec):
    """D(family, pair) = mean forward price minus mean backward price."""
    out = {}
    for (fam, pair), v in rec.items():
        fwd = np.mean(v["forward"]) if len(v["forward"]) else np.nan
        bwd = np.mean(v["backward"]) if len(v["backward"]) else np.nan
        out[(fam, pair)] = fwd - bwd
    return out


def excess_by_family(rec):
    """Per family, the crossing pair's direction difference minus the mean of the
    two controls'. The control subtraction is here and nowhere else."""
    D = direction_differences(rec)
    fams = sorted({f for (f, _p) in rec})
    out = {}
    for f in fams:
        c = D.get((f, "CROSS"), np.nan)
        g = D.get((f, "CTRL_G"), np.nan)
        m = D.get((f, "CTRL_M"), np.nan)
        out[f] = c - 0.5 * (g + m)
    return out


def estimate(rec, b=B_BOOT, seed=SEED, cluster="family"):
    """Point estimate and interval. `cluster` is exposed ONLY so the self-test
    can demonstrate what the wrong choice does."""
    per_fam = excess_by_family(rec)
    fams = sorted(per_fam)
    vals = np.array([per_fam[f] for f in fams])
    point = float(np.nanmean(vals))
    rng = np.random.default_rng(seed)
    draws = []
    if cluster == "family":
        for _ in range(b):
            pick = rng.choice(len(fams), size=len(fams), replace=True)
            draws.append(float(np.nanmean(vals[pick])))
    else:  # trial-level, which is the error this suite exists to make visible
        flat = []
        for (f, p), v in rec.items():
            if p == "CROSS":
                flat += [x for x in v["forward"]] + [-x for x in v["backward"]]
        flat = np.array(flat)
        for _ in range(b):
            pick = rng.choice(len(flat), size=len(flat), replace=True)
            draws.append(float(np.nanmean(flat[pick])))
    draws = np.array(draws)
    return {"point": point, "se": float(draws.std(ddof=1)),
            "lo": float(np.percentile(draws, 2.5)),
            "hi": float(np.percentile(draws, 97.5)),
            "n_families": len(fams)}


# ----------------------------------------------------------------------------
# synthetic data, generated in the study's own terms
# ----------------------------------------------------------------------------
def simulate(n_families=60, n_participants=40, n_reps=2, beta=0.0,
             switch_bias=0.0, sd_family=0.30, sd_part=0.40, sd_noise=0.60,
             seed=SEED):
    """Prices for every family, pair and direction.

    `beta` is a penalty that applies ONLY to the crossing pair and ONLY in the
    forward direction, which is what the study is trying to recover.
    `switch_bias` is an asymmetric cost applied to EVERY pair in both directions,
    which is the confound the controls are meant to remove.
    """
    rng = np.random.default_rng(seed)
    fam_eff = rng.normal(0, sd_family, n_families)
    part_eff = rng.normal(0, sd_part, n_participants)
    rec = {}
    for fi in range(n_families):
        for pair in PAIRS:
            key = ("fam%03d" % fi, pair)
            rec[key] = {"forward": [], "backward": []}
            for pi in range(n_participants):
                for _ in range(n_reps):
                    base = fam_eff[fi] + part_eff[pi]
                    f = base + switch_bias + rng.normal(0, sd_noise)
                    b_ = base - switch_bias + rng.normal(0, sd_noise)
                    if pair == "CROSS":
                        f += beta
                    rec[key]["forward"].append(f)
                    rec[key]["backward"].append(b_)
    return rec


def relabel_directions(rec):
    return {k: {"forward": v["backward"], "backward": v["forward"]}
            for k, v in rec.items()}


def rescale(rec, lam):
    return {k: {"forward": [x * lam for x in v["forward"]],
                "backward": [x * lam for x in v["backward"]]}
            for k, v in rec.items()}


def duplicate_within_family(rec):
    return {k: {"forward": v["forward"] * 2, "backward": v["backward"] * 2}
            for k, v in rec.items()}


# ----------------------------------------------------------------------------
# broken pipelines, for the self-test
# ----------------------------------------------------------------------------
def broken_sum_instead_of_difference(rec):
    """Adds the two directions instead of differencing them. I1 must catch it."""
    D = {}
    for (fam, pair), v in rec.items():
        D[(fam, pair)] = np.mean(v["forward"]) + np.mean(v["backward"])
    fams = sorted({f for (f, _p) in rec})
    return {f: D[(f, "CROSS")] - 0.5 * (D[(f, "CTRL_G")] + D[(f, "CTRL_M")])
            for f in fams}


def broken_no_control_subtraction(rec):
    """Reports the crossing pair's raw direction difference. I4 must catch it."""
    D = direction_differences(rec)
    return {f: D[(f, "CROSS")] for f in sorted({x for (x, _p) in rec})}


def main():
    out = {"note": "invariance suite for the transition study, no data exists yet"}
    print("=" * 76)
    print("INVARIANCE SUITE FOR THE TRANSITION ANALYSIS")
    print("=" * 76)

    BETA, BIAS = 0.50, 0.35
    rec = simulate(beta=BETA, switch_bias=BIAS)
    base = estimate(rec)
    print("  reference run, planted penalty %.2f, planted switching bias %.2f"
          % (BETA, BIAS))
    print("    excess %+.4f  se %.4f  95%% CI [%+.4f, %+.4f]  families %d"
          % (base["point"], base["se"], base["lo"], base["hi"],
             base["n_families"]))

    checks = {}

    # ---- I1 direction swap -------------------------------------------------
    sw = estimate(relabel_directions(rec))
    d1 = abs(sw["point"] + base["point"])
    checks["I1_direction_swap"] = bool(d1 < 1e-12)
    print()
    print("I1 DIRECTION SWAP   excess must negate exactly")
    print("    %+.4f against %+.4f, residual %.2e  -> %s"
          % (sw["point"], base["point"], d1, "PASS" if checks["I1_direction_swap"] else "FAIL"))

    # ---- I2 participant permutation ---------------------------------------
    rng = np.random.default_rng(7)
    perm = {k: {"forward": list(rng.permutation(v["forward"])),
                "backward": list(rng.permutation(v["backward"]))}
            for k, v in rec.items()}
    pm = estimate(perm)
    d2 = abs(pm["point"] - base["point"])
    checks["I2_participant_permutation"] = bool(d2 < 1e-12)
    print()
    print("I2 PARTICIPANT PERMUTATION   estimate must be unchanged")
    print("    residual %.2e  -> %s"
          % (d2, "PASS" if checks["I2_participant_permutation"] else "FAIL"))

    # ---- I3 rescaling ------------------------------------------------------
    lam = 7.5
    rs = estimate(rescale(rec, lam))
    scaled_ok = abs(rs["point"] - lam * base["point"]) < 1e-9
    ratio_ok = abs(rs["point"] / rs["se"] - base["point"] / base["se"]) < 1e-6
    checks["I3_rescaling"] = bool(scaled_ok and ratio_ok)
    print()
    print("I3 PRICE RESCALING by %.1f   excess scales, ratio to its se does not" % lam)
    print("    excess %+.4f against %+.4f expected" % (rs["point"], lam * base["point"]))
    print("    ratio  %+.4f against %+.4f  -> %s"
          % (rs["point"] / rs["se"], base["point"] / base["se"],
             "PASS" if checks["I3_rescaling"] else "FAIL"))

    # ---- I4 switching bias -------------------------------------------------
    no_bias = simulate(beta=BETA, switch_bias=0.0)
    big_bias = simulate(beta=BETA, switch_bias=2.0)
    e0, e2 = estimate(no_bias), estimate(big_bias)
    raw0 = np.mean([v for (f, p), v in direction_differences(no_bias).items()
                    if p == "CTRL_G"])
    raw2 = np.mean([v for (f, p), v in direction_differences(big_bias).items()
                    if p == "CTRL_G"])
    moved = abs(raw2 - raw0) > 1.0
    steady = abs(e2["point"] - e0["point"]) < 4 * e0["se"]
    checks["I4_switching_bias"] = bool(moved and steady)
    print()
    print("I4 SWITCHING BIAS   raw differences must move, the excess must not")
    print("    control raw difference  %+.4f with no bias, %+.4f with bias 2.0"
          % (raw0, raw2))
    print("    excess                  %+.4f with no bias, %+.4f with bias 2.0"
          % (e0["point"], e2["point"]))
    print("    -> %s" % ("PASS" if checks["I4_switching_bias"] else "FAIL"))

    # ---- I5 plant ----------------------------------------------------------
    zs = []
    for i, planted in enumerate((0.0, 0.25, 0.50, 1.00)):
        r = simulate(beta=planted, switch_bias=0.4, seed=SEED + 100 + i)
        e = estimate(r, seed=SEED + 200 + i)
        z = (e["point"] - planted) / e["se"]
        zs.append(z)
        print() if i == 0 else None
        if i == 0:
            print("I5 PLANT   recover a known penalty through the whole pipeline")
            print("    planted   recovered        se     err/se")
        print("    %+.3f     %+.4f    %.4f    %+6.2f"
              % (planted, e["point"], e["se"], z))
    checks["I5_plant"] = bool(max(abs(z) for z in zs) < 3.0)
    print("    worst |err/se| %.2f against a bar of 3.0  -> %s"
          % (max(abs(z) for z in zs), "PASS" if checks["I5_plant"] else "FAIL"))

    # ---- I6 clustering -----------------------------------------------------
    dup = duplicate_within_family(rec)
    fam_dup = estimate(dup)
    tri_base = estimate(rec, cluster="trial")
    tri_dup = estimate(dup, cluster="trial")
    fam_ratio = fam_dup["se"] / base["se"]
    tri_ratio = tri_dup["se"] / tri_base["se"]
    checks["I6_clustering"] = bool(abs(fam_ratio - 1.0) < 0.05 and tri_ratio < 0.85)
    print()
    print("I6 CLUSTERING   duplicating observations within families must not")
    print("   narrow a family-resampled interval, and would narrow a trial one")
    print("    family-resampled se ratio after duplication  %.3f  (target 1.00)"
          % fam_ratio)
    print("    trial-level    se ratio after duplication  %.3f  (about 0.71)"
          % tri_ratio)
    print("    -> %s" % ("PASS" if checks["I6_clustering"] else "FAIL"))

    # ---- I0 self-test ------------------------------------------------------
    print()
    print("I0 SELF-TEST   three broken pipelines, each caught by a different")
    print("   invariant. A suite never shown to reject anything licenses nothing.")

    def excess_from(per_fam):
        v = np.array([per_fam[f] for f in sorted(per_fam)])
        return float(np.nanmean(v))

    a = excess_from(broken_sum_instead_of_difference(rec))
    b_ = excess_from(broken_sum_instead_of_difference(relabel_directions(rec)))
    i1_catches = abs(a + b_) > 1e-6
    print("    sums the directions instead of differencing")
    print("      I1 residual %.4f  -> %s"
          % (abs(a + b_), "REJECTED" if i1_catches else "NOT REJECTED"))

    n0 = excess_from(broken_no_control_subtraction(no_bias))
    n2 = excess_from(broken_no_control_subtraction(big_bias))
    i4_catches = abs(n2 - n0) > 1.0
    print("    omits the control subtraction")
    print("      excess moves %.4f under a switching bias  -> %s"
          % (abs(n2 - n0), "REJECTED" if i4_catches else "NOT REJECTED"))

    i6_catches = tri_ratio < 0.85
    print("    clusters by trial instead of by family")
    print("      interval shrinks to %.3f on duplicated data  -> %s"
          % (tri_ratio, "REJECTED" if i6_catches else "NOT REJECTED"))

    checks["I0_self_test"] = bool(i1_catches and i4_catches and i6_catches)
    print("    -> %s" % ("PASS" if checks["I0_self_test"] else "FAIL"))

    ok = all(checks.values())
    print()
    print("=" * 76)
    print("INVARIANCE SUITE: %s" % ("ALL PASS" if ok else "FAILURE"))
    print("=" * 76)
    out["checks"] = {k: bool(v) for k, v in checks.items()}
    out["all_pass"] = bool(ok)
    out["reference"] = base
    out["planted_beta"] = BETA
    out["planted_switch_bias"] = BIAS
    with open(os.path.join(HERE, "analysis_invariants.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("written analysis_invariants.json")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
