#!/usr/bin/env python3
"""Pilot analysis. Emits variance components and structurally cannot emit the mean.

`PILOT.md` Section 1 says the pilot measures one number, the scale that every bar
in `grade_transition.py` is a multiple of, and tests no hypothesis. The estimand
of the study is the mean excess, so **the pilot must not report it**.

THE REFUSAL IS STRUCTURAL AND IS TESTED

Three separate things enforce it.

1. `variance_components` returns the three variances only. The grand mean exists
   inside it as a centring constant and goes out of scope with the function.
2. `build_output` is given the variances and nothing else, so the mean is not in
   scope where the output is assembled.
3. `_guard` asserts the emitted keys are exactly the permitted set, so a later
   edit that adds the mean fails loudly rather than silently.

And the self-test checks the property those three are for. **Shifting the excess
table by a constant changes the mean and must leave the components identical.**
If the mean leaked anywhere into the output, that test fails.

The first version of that test shifted the TRUE mean rather than the excess table
and failed, which looked like a leak and was not. A shift of ten pushes every
price list outside its range, so every list is censored and the components
collapse to zero. That is the instrument, not a disclosure defect, and the two
had to be separated before either could be checked. The censoring itself is now
tested on its own, and it exposed a worse problem described in `excess_table`.

THE ESTIMATOR

Per participant and family the excess is

    D(pair)   = mean forward price - mean backward price
    excess_pf = D(CROSS) - 0.5 ( D(CTRL_G) + D(CTRL_M) )

and it is modelled as a grand mean plus a family effect, a participant effect and
a residual. The components come from a moment estimator rather than an optimiser,
because it is transparent and needs no dependency.

    sigma^2_family       = average covariance between two participants in one family
    sigma^2_participant  = average covariance between two families for one participant
    sigma^2_residual     = total variance minus the other two

THE QUANTITY THE CONFIRMATORY STUDY ACTUALLY NEEDS

Not the raw spread of per-family excess, which depends on how many participants
contributed to each family, but the components, from which the spread at any
design follows.

    sd(k) = sqrt( sigma^2_family + ( sigma^2_participant + sigma^2_residual ) / k )

for `k` participants per family. `PILOT.md` Section 6 is why this matters. A pilot
at six per family and a confirmatory study at twelve do not share a raw scale.

    python pilot_analysis.py                 # self-test only
    python pilot_analysis.py responses.json  # analyse and write pilot_scale.json
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = ("CROSS", "CTRL_G", "CTRL_M")

# the only keys the pilot may emit
PERMITTED = {
    "study", "design", "n_participants", "n_families", "n_observations",
    "between_family_sd", "participant_sd", "residual_sd",
    "between_family_var", "participant_var", "residual_var",
    "implied_sd_by_k", "price_slope_z", "nonmonotone_share",
    "floor_ceiling_share", "floor_ceiling_by_cell",
    "worst_cell_floor_ceiling", "checks", "usable",
}
FORBIDDEN_SUBSTRINGS = ("mean_excess", "excess_mean", "grand_mean", "estimate",
                        "point", "effect_size", "beta")


def _guard(out):
    """Refuse to emit anything outside the permitted set."""
    bad = set(out) - PERMITTED
    if bad:
        raise AssertionError(
            "pilot output contains keys outside the permitted set: %s. The "
            "pilot reports a scale and must not report the estimand." % sorted(bad))
    for k in out:
        for f in FORBIDDEN_SUBSTRINGS:
            if f in k.lower():
                raise AssertionError("pilot output key %r looks like the estimand" % k)
    return out


# ----------------------------------------------------------------------------
# price lists
# ----------------------------------------------------------------------------
def read_list(prices, accepts):
    """Indifference price, and flags. Accepts should run 1 then 0 as price rises.

    Returns (indifference, monotone, at_edge). `indifference` is the midpoint of
    the interval containing the single switch.
    """
    a = [bool(x) for x in accepts]
    switches = [i for i in range(len(a) - 1) if a[i] != a[i + 1]]
    monotone = len(switches) == 1 and a[0] and not a[-1]
    if all(a):
        return prices[-1], len(switches) == 0, True      # never declined
    if not any(a):
        return prices[0], len(switches) == 0, True       # never accepted
    if not monotone:
        return float("nan"), False, False
    i = switches[0]
    return 0.5 * (prices[i] + prices[i + 1]), True, False


def price_slope_z(records):
    """Logistic of accept on price, pooled. Positive z means the expected
    direction, that raising the charge lowers acceptance."""
    xs, ys = [], []
    for r in records:
        for p, a in zip(r["prices"], r["accepts"]):
            xs.append(float(p))
            ys.append(1.0 if a else 0.0)
    x = np.array(xs)
    y = np.array(ys)
    x = (x - x.mean()) / (x.std() + 1e-12)
    b = np.zeros(2)
    X = np.vstack([np.ones_like(x), x]).T
    for _ in range(60):
        eta = np.clip(X @ b, -30, 30)
        p = 1.0 / (1.0 + np.exp(-eta))
        W = np.maximum(p * (1 - p), 1e-9)
        g = X.T @ (y - p)
        H = X.T @ (X * W[:, None])
        try:
            step = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            return 0.0
        b = b + step
        if np.max(np.abs(step)) < 1e-10:
            break
    eta = np.clip(X @ b, -30, 30)
    p = 1.0 / (1.0 + np.exp(-eta))
    W = np.maximum(p * (1 - p), 1e-9)
    cov = np.linalg.inv(X.T @ (X * W[:, None]))
    se = math.sqrt(max(cov[1, 1], 1e-30))
    # expected sign is negative, so a correct instrument gives a positive z here
    return float(-b[1] / se)


# ----------------------------------------------------------------------------
# the excess, and the variance components
# ----------------------------------------------------------------------------
def excess_table(records):
    """(participant, family) -> excess, from the price lists.

    Edge hits are counted PER CELL TYPE and not only pooled. A pooled share
    hides censoring on the one cell the study depends on. In a self-test the
    pooled share was 3.1 percent, inside any reasonable budget, while the
    crossing pair's forward cell was censored 19 percent of the time and the
    variance components came out 24 percent low. Four of the six cells are
    controls sitting safely inside the price range, and they diluted the
    statistic that was supposed to catch exactly this.
    """
    cell = {}
    flags = {"nonmonotone": 0, "edge": 0, "total": 0}
    by_cell = {}
    for r in records:
        v, mono, edge = read_list(r["prices"], r["accepts"])
        key = "%s_%s" % (r["pair"], r["direction"])
        c = by_cell.setdefault(key, {"edge": 0, "total": 0})
        c["total"] += 1
        flags["total"] += 1
        if not mono:
            flags["nonmonotone"] += 1
        if edge:
            flags["edge"] += 1
            c["edge"] += 1
        cell[(r["participant"], r["family"], r["pair"], r["direction"])] = v
    flags["by_cell"] = {k: v["edge"] / max(v["total"], 1)
                        for k, v in by_cell.items()}
    out = {}
    keys = {(p, f) for (p, f, _pa, _d) in cell}
    for (p, f) in keys:
        D = {}
        for pair in PAIRS:
            fwd = cell.get((p, f, pair, "forward"))
            bwd = cell.get((p, f, pair, "backward"))
            if fwd is None or bwd is None or not np.isfinite(fwd) or not np.isfinite(bwd):
                D = None
                break
            D[pair] = fwd - bwd
        if D is not None:
            out[(p, f)] = D["CROSS"] - 0.5 * (D["CTRL_G"] + D["CTRL_M"])
    return out, flags


def variance_components(excess):
    """The three variances. The grand mean is local and is not returned.

    Moment estimator. The covariance between two observations sharing a family
    and not a participant estimates the family variance, and symmetrically.
    """
    vals = np.array(list(excess.values()), float)
    mu = float(vals.mean())                      # centring only, not returned
    cen = {k: v - mu for k, v in excess.items()}
    total = float(np.var(vals, ddof=1))

    def shared_cov(index):
        prods = []
        groups = {}
        for (p, f), v in cen.items():
            groups.setdefault((p if index == 0 else f), []).append(
                ((f if index == 0 else p), v))
        for _g, items in groups.items():
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    if items[i][0] != items[j][0]:
                        prods.append(items[i][1] * items[j][1])
        return float(np.mean(prods)) if prods else 0.0

    var_part = max(shared_cov(0), 0.0)       # same participant, different family
    var_fam = max(shared_cov(1), 0.0)        # same family, different participant
    var_res = max(total - var_fam - var_part, 0.0)
    del mu, cen
    return var_fam, var_part, var_res, total


def build_output(var_fam, var_part, var_res, n_part, n_fam, n_obs,
                 slope_z, nonmono, edge, edge_by_cell):
    """Assembled from the components only. The mean is not in scope here."""
    sd_fam = math.sqrt(var_fam)
    checks = {
        "price_slope_ok": bool(slope_z >= 3.0),
        "nonmonotone_ok": bool(nonmono <= 0.25),
        "between_family_positive": bool(var_fam > 0.0),
        # the WORST cell, not the pooled share, for the reason in excess_table
        "floor_ceiling_ok": bool(max(edge_by_cell.values(), default=0.0) <= 0.15),
    }
    out = {
        "study": "transition study pilot",
        "design": {"participants": n_part, "families": n_fam,
                   "observations": n_obs},
        "n_participants": n_part, "n_families": n_fam, "n_observations": n_obs,
        "between_family_var": var_fam, "participant_var": var_part,
        "residual_var": var_res,
        "between_family_sd": sd_fam,
        "participant_sd": math.sqrt(var_part),
        "residual_sd": math.sqrt(var_res),
        "implied_sd_by_k": {
            str(k): math.sqrt(var_fam + (var_part + var_res) / k)
            for k in (4, 6, 8, 12, 16, 24)},
        "price_slope_z": slope_z,
        "nonmonotone_share": nonmono,
        "floor_ceiling_share": edge,
        "floor_ceiling_by_cell": edge_by_cell,
        "worst_cell_floor_ceiling": max(edge_by_cell.values(), default=0.0),
        "checks": checks,
        "usable": bool(all(checks.values())),
    }
    return _guard(out)


def analyse(records):
    excess, flags = excess_table(records)
    vf, vp, vr, _total = variance_components(excess)
    n_part = len({p for (p, _f) in excess})
    n_fam = len({f for (_p, f) in excess})
    return build_output(
        vf, vp, vr, n_part, n_fam, len(excess),
        price_slope_z(records),
        flags["nonmonotone"] / max(flags["total"], 1),
        flags["edge"] / max(flags["total"], 1),
        flags["by_cell"])


# ----------------------------------------------------------------------------
# synthetic pilot data, for the self-test only
# ----------------------------------------------------------------------------
def simulate(n_fam=30, n_part=60, fam_per_part=3, mean_excess=0.0,
             sd_fam=0.30, sd_part=0.40, sd_res=0.50, switch_bias=0.3,
             price_rows=(-1.0, -0.7, -0.5, -0.3, -0.15, 0.0,
                         0.15, 0.3, 0.5, 0.7, 1.0), seed=11):
    rng = np.random.default_rng(seed)
    fam_eff = rng.normal(0, sd_fam, n_fam)
    part_eff = rng.normal(0, sd_part, n_part)
    recs = []
    for p in range(n_part):
        fams = rng.choice(n_fam, size=fam_per_part, replace=False)
        for f in fams:
            # the excess this participant and family would show
            e = mean_excess + fam_eff[f] + part_eff[p] + rng.normal(0, sd_res)
            for pair in PAIRS:
                # put the whole excess on CROSS, none on the controls
                add = e if pair == "CROSS" else 0.0
                for direction in ("forward", "backward"):
                    s = switch_bias if direction == "forward" else -switch_bias
                    centre = s + (add if direction == "forward" else 0.0)
                    accepts = [1 if pr < centre else 0 for pr in price_rows]
                    recs.append({"participant": "p%03d" % p,
                                 "family": "f%03d" % f, "pair": pair,
                                 "direction": direction,
                                 "prices": list(price_rows),
                                 "accepts": accepts})
    return recs


def self_test():
    print("SELF-TEST")
    ok = True

    # 1, THE DISCLOSURE PROPERTY, isolated from the instrument.
    # Shifting the excess table by a constant changes the estimand and must
    # leave the components untouched. An earlier version of this test shifted
    # the TRUE mean instead and failed, because a shift of ten pushes every
    # price list outside its range and censors it. That was the instrument, not
    # a leak, and conflating the two would have sent us looking in the wrong
    # place.
    recs = simulate(mean_excess=0.0, seed=5)
    ex, _f = excess_table(recs)
    a = variance_components(ex)
    b = variance_components({k: v + 10.0 for k, v in ex.items()})
    same = all(abs(x - y) < 1e-9 for x, y in zip(a, b))
    print("  shifting the excess table by 10 leaves the components identical")
    print("    -> %s" % ("PASS" if same else "FAIL, the estimand leaked"))
    ok = ok and same

    # 2, the guard must reject a forbidden key
    try:
        _guard({"study": "x", "mean_excess": 1.0})
        print("  the guard rejects a forbidden key -> FAIL, it did not")
        ok = False
    except AssertionError:
        print("  the guard rejects a forbidden key -> PASS")

    # 3, an out-of-range excess must be CAUGHT, not silently absorbed
    r10 = analyse(simulate(mean_excess=10.0, seed=5))
    caught = not r10["usable"]
    print("  an excess far outside the price range is caught")
    print("    worst cell at an edge %.3f, family sd %.4f, usable %s -> %s"
          % (r10["worst_cell_floor_ceiling"], r10["between_family_sd"],
             r10["usable"], "PASS" if caught else "FAIL"))
    ok = ok and caught

    # 4, components recovered when the range brackets the excess
    wide = tuple(x * 4.0 for x in (-1.0, -0.7, -0.5, -0.3, -0.15, 0.0,
                                   0.15, 0.3, 0.5, 0.7, 1.0))
    truth = (0.30, 0.40, 0.50)
    r = analyse(simulate(sd_fam=truth[0], sd_part=truth[1], sd_res=truth[2],
                         n_fam=40, n_part=120, seed=9, price_rows=wide))
    got = (r["between_family_sd"], r["participant_sd"], r["residual_sd"])
    print("  recovering planted components with a range that brackets them")
    for nm, t, g in zip(("family", "participant", "residual"), truth, got):
        print("    %-12s planted %.3f  recovered %.3f" % (nm, t, g))
    print("    worst cell at an edge %.3f" % r["worst_cell_floor_ceiling"])
    rec_ok = all(abs(g - t) < 0.35 * t + 0.05 for g, t in zip(got, truth))
    print("    -> %s" % ("PASS" if rec_ok else "FAIL"))
    ok = ok and rec_ok

    # 5, the narrow range that hid censoring in a pooled statistic
    rn = analyse(simulate(sd_fam=truth[0], sd_part=truth[1], sd_res=truth[2],
                          n_fam=40, n_part=120, seed=9))
    print("  the same data on a range that does NOT bracket it")
    print("    pooled edge share %.3f, which looks fine"
          % rn["floor_ceiling_share"])
    print("    worst cell %.3f on %s"
          % (rn["worst_cell_floor_ceiling"],
             max(rn["floor_ceiling_by_cell"], key=rn["floor_ceiling_by_cell"].get)))
    print("    family sd %.3f against a planted %.3f"
          % (rn["between_family_sd"], truth[0]))
    hidden = (rn["floor_ceiling_share"] < 0.15
              and rn["worst_cell_floor_ceiling"] > 0.15)
    print("    the per-cell check catches what the pooled one misses -> %s"
          % ("PASS" if hidden else "not triggered on this seed"))

    # 6, a participant who never declines must trip a check
    flat = simulate(seed=3)
    for rec in flat:
        rec["accepts"] = [1] * len(rec["prices"])
    r2 = analyse(flat)
    fired = not r2["usable"]
    print("  a participant who never declines trips a pilot check -> %s"
          % ("PASS" if fired else "FAIL"))
    ok = ok and fired

    print("  SELF-TEST %s" % ("PASSED" if ok else "FAILED"))
    return ok


def main():
    if len(sys.argv) == 1:
        return 0 if self_test() else 1
    if not self_test():
        print()
        print("self-test failed, refusing to analyse")
        return 1
    with open(sys.argv[1], encoding="utf-8") as fh:
        records = json.load(fh)
    out = analyse(records)
    print()
    print(json.dumps(out, indent=2))
    with open(os.path.join(HERE, "pilot_scale.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written pilot_scale.json")
    if not out["usable"]:
        print("PILOT NOT USABLE. See checks. Fix the instrument and repeat.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
