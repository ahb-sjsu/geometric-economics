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
ORDER = ["GEO1", "GEO2", "EARLY", "RDU", "CAG", "ADD", "IA"]
# version 4, the crossing set: the truths under which each secondary test should pass
SEC_EXPECT = {"SH1_IA_beats_GEO": {"IA"}, "SH1r_GEO_beats_IA": {"GEO1", "GEO2"},
              "SH2_straddle_beyond_GEO": {"IA"}, "SH3_equal_splits_beyond_GEO": {"IA"}, "straddle_raw": {"IA"},
              "SH3_did": {"IA"}}


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
            if "gap" in rows[0]["H4"]:
                row["H4"]["gap"] = float(np.median([x["H4"]["gap"] for x in rows]))
            for mf in ("MF1", "MF2"):
                row[mf] = {"pass": float(np.mean([x[mf]["pass"] for x in rows])),
                           "est": float(np.median([x[mf]["est"] for x in rows]))}
            for key in ("mean_ll", "mean_ll_pass1"):
                if key in rows[0]:
                    row[key] = {k: float(np.median([x[key][k] for x in rows])) for k in rows[0][key]}
            if "secondary" in rows[0]:
                row["secondary"] = {k: {"pass": float(np.mean([x["secondary"][k]["pass"] for x in rows])),
                                        "est": float(np.median([x["secondary"][k]["est"] for x in rows]))}
                                    for k in rows[0]["secondary"]}
            table[f"{truth}_n{n}"] = row
        rec = [s["recovery"] for s in r["sims"] if s["recovery"]]
        if rec:
            res[f"recovery_{truth}"] = {k: float(np.median([x[k] for x in rec if k in x])) for k in rec[0]}
        hs = [s["hier"] for s in r["sims"] if "hier" in s]
        if hs:          # version 3: the hierarchical population median kappa
            # coverage is defined only for the GEO truths; version 3's EARLY file carries 1.5, which is
            # not a GEO kappa (rehearsal.py, TRUE_KAPPA)
            tk = r.get("true_kappa") if truth in ("GEO1", "GEO2") else None
            h = {"studies": len(hs), "kappa_median": float(np.median([x["kappa_median"] for x in hs])),
                 "width": float(np.median([x["hi"] - x["lo"] for x in hs])),
                 "excludes_1": float(np.mean([x["lo"] > 1 or x["hi"] < 1 for x in hs])),
                 "excludes_2": float(np.mean([x["lo"] > 2 or x["hi"] < 2 for x in hs])),
                 "divergences": float(np.mean([x["divergences"] for x in hs]))}
            if tk is not None:
                h["true"] = tk
                h["covers_truth"] = float(np.mean([x["lo"] <= tk <= x["hi"] for x in hs]))
            res[f"hier_{truth}"] = h
    res["table"] = table
    json.dump(res, open(out, "w"), indent=1)
    print(f"{'truth/n':<12} {'H1 vs EARLY':>14} {'H2 vs RDU':>14} {'H3 vs CAG':>14} {'H4':>11} {'MF1 corr':>15} {'MF2 bg':>15}")
    for key, row in table.items():
        truth = key.split("_n")[0]
        cell = lambda h: (f"{row[h]['pass0']:.2f}/{row[h]['pass005']:.2f}" +  # noqa: E731
                          ("*" if truth in EXPECT[h] else " "))
        print(f"{key:<12} {cell('H_vs_EARLY'):>14} {cell('H_vs_RDU'):>14} {cell('H_vs_CAG'):>14} "
              f"{row['H4']['pass']:>6.2f}{'*' if truth in EXPECT['H4'] else ' '} "
              f"{'gap' if 'gap' in row['H4'] else 'rho'}{row['H4'].get('gap', row['H4']['rho']):+.2f} "
              f"{row['MF1']['pass']:>5.2f} ({row['MF1']['est']:+.3f}) {row['MF2']['pass']:>5.2f} ({row['MF2']['est']:+.3f})")
    print("pass rates at margin 0 / 0.005; * = the test should pass under this truth")
    print("held-out log-loss per test trial at the largest n (chance = 0.693), median over studies:")
    for key, row in table.items():
        if key.endswith(f"_n{max(int(k.split('_n')[1]) for k in table)}"):
            print(f"  {key:<12} " + "  ".join(f"{k} {v:.3f}" for k, v in row["mean_ll"].items()) +
                  ("   first pass: " + "  ".join(f"{k} {v:.3f}" for k, v in row["mean_ll_pass1"].items())
                   if "mean_ll_pass1" in row else ""))
    for k, v in res.items():
        if k.startswith("recovery_") or k.startswith("hier_"):
            print(k, {kk: round(vv, 3) for kk, vv in v.items()})
    sec_rows = {k: v["secondary"] for k, v in table.items() if "secondary" in v}
    if sec_rows:
        names = list(next(iter(sec_rows.values())))
        print("crossing set (secondary): pass rate (median estimate); * = should pass under this truth")
        print(f"{'truth/n':<12} " + " ".join(f"{s[:24]:>27}" for s in names))
        for key, sec in sec_rows.items():
            truth = key.split("_n")[0]
            print(f"{key:<12} " + " ".join(
                f"{sec[s]['pass']:>8.2f}{'*' if truth in SEC_EXPECT.get(s, ()) else ' '} ({sec[s]['est']:+.3f})".rjust(27)
                for s in names))


if __name__ == "__main__":
    main(*sys.argv[1:])
