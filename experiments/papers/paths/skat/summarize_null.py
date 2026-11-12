"""Set a real result of analyze_bids.py or analyze_bids_pooled.py beside the same analysis on shuffled games.

    python summarize_null.py real.json shuffled_1.json shuffled_2.json ...
"""
import json
import sys

import numpy as np

real = json.load(open(sys.argv[1]))
nulls = [json.load(open(p)) for p in sys.argv[2:]]
print("shuffles", len(nulls))
for name in real["groups"]:
    print(name)
    for sec in ("by_last_outcome", "by_lag"):
        for k, c in real["groups"][name][sec].items():
            v = np.array([n["groups"][name][sec][k].get("difference", np.nan) for n in nulls])
            out = sum(1 for n in nulls if "ci95" in n["groups"][name][sec][k] and
                      (n["groups"][name][sec][k]["ci95"][0] > 0 or n["groups"][name][sec][k]["ci95"][1] < 0))
            r = c.get("difference", float("nan"))
            ci = c.get("ci95", [float("nan")] * 2)
            print("  %-22s real %+.4f (%+.4f to %+.4f)  shuffled mean %+.4f sd %.4f min %+.4f max %+.4f  intervals excluding zero %d of %d"
                  % (k, r, ci[0], ci[1], np.nanmean(v), np.nanstd(v, ddof=1), np.nanmin(v), np.nanmax(v), out, len(v)))
