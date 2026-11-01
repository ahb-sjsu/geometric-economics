#!/usr/bin/env python3
"""Pool score_<corpus>.json files: per-corpus table and the equal-weight mean over corpora, with
95% intervals from the per-corpus bootstrap draws averaged draw by draw.

    python aggregate.py NRP_OUT_DIR OUT.json
"""
import glob
import json
import os
import sys

import numpy as np

MODELS = ["EV", "RUM", "GDT2", "GDTS", "CPT_unit", "CPT_share"]
STATS = ["vs_ml", "vs_ceiling", "logloss_vs_ml"]


def main(d, out):
    runs = {}
    for f in sorted(glob.glob(os.path.join(d, "score_*.json"))):
        r = json.load(open(f))
        runs[r["corpus"]] = r
    table = {}
    for c, r in runs.items():
        comp, rest = r["completeness"], r["restrictiveness"]
        table[c] = {"problems": r["problems"], "ml_predictor": comp["ml_predictor"],
                    "ml_vs_ceiling": comp["completeness"][comp["ml_predictor"]]["vs_ceiling"],
                    "models": {m: {**{s: comp["completeness"][m][s] for s in STATS},
                                   **{f"{s}_ci": comp["ci95"][m][s] for s in STATS},
                                   "restrictiveness": rest["restrictiveness"][m], "restr_se": rest["se"][m]}
                               for m in MODELS}}
    pooled = {}
    for m in MODELS:
        p = {}
        for s in STATS:
            draws = np.mean([np.array(runs[c]["completeness"]["boot"][m][s]) for c in runs], axis=0)
            p[s] = float(np.mean([table[c]["models"][m][s] for c in runs]))
            p[f"{s}_ci"] = [float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))]
        p["restrictiveness"] = float(np.mean([table[c]["models"][m]["restrictiveness"] for c in runs]))
        p["restr_se"] = float(np.sqrt(np.sum([table[c]["models"][m]["restr_se"] ** 2 for c in runs])) / len(runs))
        pooled[m] = p
    res = {"corpora": list(runs), "per_corpus": table, "pooled": pooled,
           "ml_vs_ceiling_mean": float(np.mean([table[c]["ml_vs_ceiling"] for c in runs]))}
    json.dump(res, open(out, "w"), indent=1)
    print(f"{'model':<10} {'compl_vs_ML':>22} {'compl_vs_ceiling':>22} {'restrictiveness':>16}")
    for m, p in pooled.items():
        print(f"{m:<10} {p['vs_ml']:6.3f} [{p['vs_ml_ci'][0]:.3f},{p['vs_ml_ci'][1]:.3f}]   "
              f"{p['vs_ceiling']:6.3f} [{p['vs_ceiling_ci'][0]:.3f},{p['vs_ceiling_ci'][1]:.3f}]   "
              f"{p['restrictiveness']:.3f} ({p['restr_se']:.3f})")
    for c, t in table.items():
        print(c, t["ml_predictor"], round(t["ml_vs_ceiling"], 3),
              {m: (round(v["vs_ml"], 2), round(v["vs_ceiling"], 2), round(v["restrictiveness"], 3))
               for m, v in t["models"].items()})


if __name__ == "__main__":
    main(*sys.argv[1:])
