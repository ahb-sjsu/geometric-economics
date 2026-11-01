#!/usr/bin/env python3
"""Summarise explore_rho_<corpus>.json: per-corpus rho, profile, recovery, completeness, and pooled paired
differences (equal weight over corpora, bootstrap draws averaged draw by draw).

    python aggregate_rho.py DIR OUT.json
"""
import glob
import json
import os
import sys

import numpy as np


def main(d, out):
    R = {json.load(open(f))["corpus"]: json.load(open(f)) for f in sorted(glob.glob(os.path.join(d, "explore_rho_*.json")))}
    per = {}
    for c, r in R.items():
        prof = {float(k): v["nll"] for k, v in r["profile"].items()}
        best = min(prof, key=prof.get)
        rec = {}
        for x in r["recovery"]:
            rec.setdefault(x["true"], []).append(round(x["recovered"], 3))
        comp = r["completeness"]
        per[c] = {"stake_ratio": r["stake"]["ratio"], "log_stake_sd": r["stake"]["log_sd"],
                  "rho_all": r["all_data_fit"]["rho"], "alpha_all": r["all_data_fit"]["alpha"],
                  "profile_best": best,
                  "profile_dnll_vs_best": {k: round((v - prof[best]) * 1e3, 3) for k, v in prof.items()},
                  "rho_folds": [round(x, 3) for x in comp["rho_per_fold"]["CPT_rho"]],
                  "gdts_rho_folds_median": float(np.median(comp["rho_per_fold"]["GDTS_rho"])),
                  "recovery": rec, "completeness": {k: round(v, 3) for k, v in comp["completeness_vs_ml"].items()},
                  "ci95": {k: [round(x, 3) for x in v] for k, v in comp["ci95"].items()},
                  "restrictiveness": r["restrictiveness"]}
    keys = list(next(iter(R.values()))["completeness"]["completeness_vs_ml"])
    pooled = {}
    for k in keys:
        draws = np.mean([np.array(r["completeness"]["boot"][k]) for r in R.values()], axis=0)
        pooled[k] = {"point": float(np.mean([r["completeness"]["completeness_vs_ml"][k] for r in R.values()])),
                     "ci95": [float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))]}
    res = {"per_corpus": per, "pooled": pooled}
    json.dump(res, open(out, "w"), indent=1)
    for c, p in per.items():
        print(c, "stake ratio", round(p["stake_ratio"], 1), "rho_all", round(p["rho_all"], 3), "alpha", round(p["alpha_all"], 3),
              "profile best", p["profile_best"], "folds", p["rho_folds"], "recovery", p["recovery"])
        print("   profile dNLL (milli-nats)", p["profile_dnll_vs_best"])
        print("   completeness", p["completeness"], "restr", {m: round(v["mean"], 3) for m, v in p["restrictiveness"].items()})
    for k, v in pooled.items():
        print(f"POOLED {k:<22} {v['point']:7.3f} [{v['ci95'][0]:.3f}, {v['ci95'][1]:.3f}]")


if __name__ == "__main__":
    main(*sys.argv[1:])
