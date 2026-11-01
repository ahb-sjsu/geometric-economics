#!/usr/bin/env python3
"""Summarise explore_cu_<corpus>.json against the conditions in DEVELOPMENT.md, "Diameter scaling".

    python aggregate_cu.py DIR OUT.json
"""
import glob
import json
import os
import sys

import numpy as np

MENUS = (0.31, 0.53)
LR = 1.92


def interval(grid, total):
    best = int(np.argmin(total))
    ok = [g for g, t in zip(grid, total) if t - total[best] <= LR]
    return grid[best], [min(ok), max(ok)]


def main(d, out):
    R = {}
    for f in sorted(glob.glob(os.path.join(d, "explore_cu_*.json"))):
        r = json.load(open(f))
        R[r["corpus"]] = r
    grid = sorted(float(g) for g in next(iter(R.values()))["profile"])
    per, pooled_tot = {}, np.zeros(len(grid))
    for c, r in R.items():
        tot = np.array([r["profile"][str(g) if str(g) in r["profile"] else repr(g)]["nll"] for g in grid]) * r["choices"]
        pooled_tot += tot
        best, ci = interval(grid, tot)
        rec = {}
        for x in r["recovery"]:
            rec.setdefault(x["true"], []).append(round(x["recovered"], 3))
        comp = r["completeness"]
        per[c] = {"rho_best": best, "rho_ci": ci, "rho_all": r["all_data_fit"]["rho_cpt_cur"],
                  "rho_gdts_d": r["all_data_fit"]["rho_gdts_d"],
                  "rho_folds": [round(x, 3) for x in comp["rho_per_fold"]["CPT_CUr"]],
                  "recovery": rec, "recovery_ok": all(abs(v - t) <= 0.15 for t, vs in rec.items() for v in vs),
                  "completeness": {k: round(v, 3) for k, v in comp["completeness_vs_ml"].items()},
                  "restrictiveness": r["restrictiveness"]}
    pbest, pci = interval(grid, pooled_tot)
    keys = list(next(iter(R.values()))["completeness"]["completeness_vs_ml"])
    pooled = {}
    for k in keys:
        draws = np.mean([np.array(r["completeness"]["boot"][k]) for r in R.values()], axis=0)
        pooled[k] = {"point": float(np.mean([r["completeness"]["completeness_vs_ml"][k] for r in R.values()])),
                     "ci95": [float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))]}
    lo = max(p["rho_ci"][0] for p in per.values())
    hi = min(p["rho_ci"][1] for p in per.values())
    cond = {"1_recovery": all(p["recovery_ok"] for p in per.values()),
            "2_common_rho": bool(lo <= hi), "2_common_range": [lo, hi],
            "3_cur_at_least_cu": bool(pooled["CPT_CUr-CPT_CU"]["ci95"][1] >= 0),
            "4_overlaps_menus": bool(pci[0] <= MENUS[1] and pci[1] >= MENUS[0])}
    res = {"per_corpus": per, "pooled_rho": {"best": pbest, "ci": pci, "profile_total_nats":
                                             dict(zip(map(str, grid), (pooled_tot - pooled_tot.min()).round(2).tolist()))},
           "pooled_completeness": pooled, "conditions": cond}
    json.dump(res, open(out, "w"), indent=1)
    for c, p in per.items():
        print(c, "rho", p["rho_best"], p["rho_ci"], "all", round(p["rho_all"], 3), "gdts_d", round(p["rho_gdts_d"], 3),
              "folds", p["rho_folds"], "recovery", p["recovery"])
        print("   ", p["completeness"], {m: round(v["mean"], 3) for m, v in p["restrictiveness"].items()})
    print("POOLED rho", pbest, pci, res["pooled_rho"]["profile_total_nats"])
    for k, v in pooled.items():
        print(f"POOLED {k:<20} {v['point']:7.3f} [{v['ci95'][0]:.3f}, {v['ci95'][1]:.3f}]")
    print("CONDITIONS", cond)


if __name__ == "__main__":
    main(*sys.argv[1:])
