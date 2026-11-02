#!/usr/bin/env python3
"""Summarise rehearsal_<TRUTH>.json files: pass rates by truth and n, and recovery.

    python aggregate_rehearsal.py DIR OUT.json

A pass rate is the share of simulated studies in which the test passed. For the H tests it is given
at margin 0 and at 0.005 nats per trial. EXPECT marks the truths under which a test should pass.
"""
import glob
import json
import os
import sys

import numpy as np

EXPECT = {"H_vs_EARLY": {"GEO1", "GEO2", "RDU", "CAG"}, "H_vs_RDU": {"GEO1", "GEO2"},
          "H_vs_CAG": {"GEO1", "GEO2"}, "H4": {"GEO1", "GEO2"}}
ORDER = ["GEO1", "GEO2", "EARLY", "RDU", "CAG", "ADD"]


def main(d, out):
    res, table = {}, {}
    files = {json.load(open(f))["truth"]: json.load(open(f)) for f in glob.glob(os.path.join(d, "rehearsal_*.json"))}
    for truth in [t for t in ORDER if t in files]:
        r = files[truth]
        margins = r["margins"]
        mi = margins.index(0.005)
        for n in r["ns"]:
            rows = [s[f"n{n}"] for s in r["sims"]]
            row = {}
            for h in ("H_vs_EARLY", "H_vs_RDU", "H_vs_CAG"):
                row[h] = {"pass0": float(np.mean([x[h]["pass"][0] for x in rows])),
                          "pass005": float(np.mean([x[h]["pass"][mi] for x in rows])),
                          "est": float(np.median([x[h]["est"] for x in rows])),
                          "est_S": float(np.median([x[h]["est_S"] for x in rows])),
                          "est_X": float(np.median([x[h]["est_X"] for x in rows]))}
            row["H4"] = {"pass": float(np.mean([x["H4"]["pass"] for x in rows])),
                         "rho": float(np.median([x["H4"]["rho"] for x in rows if x["H4"]["rho"] is not None] or [np.nan]))}
            for mf in ("MF1", "MF2"):
                row[mf] = {"pass": float(np.mean([x[mf]["pass"] for x in rows])),
                           "est": float(np.median([x[mf]["est"] for x in rows]))}
            table[f"{truth}_n{n}"] = row
        rec = [s["recovery"] for s in r["sims"] if s["recovery"]]
        if rec:
            res[f"recovery_{truth}"] = {k: float(np.median([x[k] for x in rec if k in x])) for k in rec[0]}
    res["table"] = table
    json.dump(res, open(out, "w"), indent=1)
    print(f"{'truth/n':<12} {'H1 vs EARLY':>14} {'H2 vs RDU':>14} {'H3 vs CAG':>14} {'H4':>11} {'MF1 corr':>15} {'MF2 bg':>15}")
    for key, row in table.items():
        truth = key.split("_n")[0]
        cell = lambda h: (f"{row[h]['pass0']:.2f}/{row[h]['pass005']:.2f}" +  # noqa: E731
                          ("*" if truth in EXPECT[h] else " "))
        print(f"{key:<12} {cell('H_vs_EARLY'):>14} {cell('H_vs_RDU'):>14} {cell('H_vs_CAG'):>14} "
              f"{row['H4']['pass']:>6.2f}{'*' if truth in EXPECT['H4'] else ' '} rho{row['H4']['rho']:+.2f} "
              f"{row['MF1']['pass']:>5.2f} ({row['MF1']['est']:+.3f}) {row['MF2']['pass']:>5.2f} ({row['MF2']['est']:+.3f})")
    print("pass rates at margin 0 / 0.005; * = the test should pass under this truth")
    for k, v in res.items():
        if k.startswith("recovery_"):
            print(k, {kk: round(vv, 3) for kk, vv in v.items()})


if __name__ == "__main__":
    main(*sys.argv[1:])
