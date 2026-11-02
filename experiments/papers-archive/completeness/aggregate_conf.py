#!/usr/bin/env python3
"""Score the confidence runs against DEVELOPMENT.md, "Building confidence on the spent data".

    python aggregate_conf.py DIR OUT.json
"""
import glob
import json
import os
import sys

import numpy as np

RISKY = ["cpc18", "gp2012", "pachur2017", "pachur2018", "zilker2020", "babula2018"]
MENUS = ["menus_molter", "menus_gluth"]
LR, B, SEED = 1.92, 2000, 20261106


def load(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, "confidence_*.json"))):
        r = json.load(open(f))
        cur = out.setdefault(r["name"], {**r, "profile_total_nats": {}, "cv_loss_per_participant": {}, "err": {}})
        cur["profile_total_nats"].update(r["profile_total_nats"])
        cur["cv_loss_per_participant"].update(r.get("cv_loss_per_participant", {}))
        cur["err"].update(r.get("err", {}))
    return out


def profile(rs):
    grid = sorted({float(g) for r in rs for g in r["profile_total_nats"]})
    tot = np.array([sum(r["profile_total_nats"][str(g)] for r in rs) for g in grid])
    best = int(np.argmin(tot))
    ok = [g for g, t in zip(grid, tot) if t - tot[best] <= LR]
    return grid[best], [min(ok), max(ok)]


def frozen_key(rho):
    return str(round(min(max(round(rho / 0.025) * 0.025, 0.40), 1.10), 3))


def comp_diff_draws(r, ra, rb, rng):
    e = {k: np.array(v) for k, v in r["err"].items()}
    def c(idx, key):
        en = e["naive"][idx].mean()
        return (en - e[key][idx].mean()) / (en - e["ML"][idx].mean())
    n = len(e["naive"])
    point = (c(np.arange(n), ra) - c(np.arange(n), rb), c(np.arange(n), ra), c(np.arange(n), rb))
    draws = np.array([c(i, ra) - c(i, rb) for i in (rng.integers(0, n, n) for _ in range(B))])
    return point, draws


def menus_diff(r, ra, rb, rng):
    a, b = np.array(r["cv_loss_per_participant"][ra]), np.array(r["cv_loss_per_participant"][rb])
    d = a - b
    bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(B)]
    return {"mean": float(d.mean()), "ci95": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
            "loss_a": float(a.mean()), "loss_b": float(b.mean())}


def main(d, out):
    R = load(d)
    rng = np.random.default_rng(SEED)
    res = {"datasets": {k: {"parts_profile_points": len(v["profile_total_nats"])} for k, v in R.items()}}
    risky = [c for c in RISKY if c in R]
    # A: leave one corpus out
    A, pooled_draws = {}, []
    for h in risky:
        rho_h, _ = profile([R[c] for c in risky if c != h])
        key = frozen_key(rho_h)
        (diff, c_fr, c_one), draws = comp_diff_draws(R[h], key, "1.0", rng)
        pooled_draws.append(draws)
        A[h] = {"rho_frozen": rho_h, "grid_key": key, "completeness_frozen": c_fr, "completeness_rho1": c_one,
                "diff": diff, "diff_ci95": [float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))]}
    pd_ = np.mean(pooled_draws, axis=0)
    pooled = float(np.mean([A[h]["diff"] for h in risky]))
    wins = int(sum(A[h]["diff"] > 0 for h in risky))
    res["A"] = {"per_corpus": A, "pooled_diff": pooled,
                "pooled_ci95": [float(np.percentile(pd_, 2.5)), float(np.percentile(pd_, 97.5))],
                "wins": wins, "pass": bool(np.percentile(pd_, 2.5) > 0 and wins >= 4)}
    # B: menus, pooled over participants
    rho_r, ci_r = profile([R[c] for c in risky])
    res["risky_pooled_rho"] = {"rho": rho_r, "ci": ci_r}
    Bres = {}
    for m in MENUS:
        if m not in R:
            continue
        rho_m, ci_m = profile([R[m]])
        key = frozen_key(rho_r)
        Bres[m] = {"own_rho": rho_m, "own_ci": ci_m, "overlaps_risky": bool(ci_m[0] <= ci_r[1] and ci_m[1] >= ci_r[0]),
                   "frozen_key": key, "vs_rho0": menus_diff(R[m], key, "0.0", rng),
                   "vs_rho1": menus_diff(R[m], key, "1.0", rng)}
        Bres[m]["beats_both"] = bool(Bres[m]["vs_rho0"]["ci95"][1] < 0 and Bres[m]["vs_rho1"]["ci95"][1] < 0)
    res["B"] = {"per_dataset": Bres, "pass": bool(len(Bres) == 2 and all(v["beats_both"] for v in Bres.values()))}
    # reverse transfer, reported only
    ms = [R[m] for m in MENUS if m in R]
    if ms:
        rho_m, ci_m = profile(ms)
        key = frozen_key(rho_m)
        rev = {h: comp_diff_draws(R[h], key, "1.0", rng)[0][0] for h in risky}
        res["reverse"] = {"menus_pooled_rho": rho_m, "ci": ci_m, "grid_key": key,
                          "risky_completeness_diff_vs_wilcox": rev, "mean": float(np.mean(list(rev.values())))}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:])
