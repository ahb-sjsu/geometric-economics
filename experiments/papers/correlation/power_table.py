#!/usr/bin/env python3
"""The version 5 power table (PILOT.md) from rehearsal.py's rehearsal_<CELL>.json files.

    python power_table.py DIR OUT.json

For each cell and n, the main claim's pass rate (H1, H2 and H3 at margin 0.005) over the cell's simulated
studies, with a 95% Wilson interval. Two checks, as PILOT.md defines them:
  rank one     A share s of rank-one people should act like a sample of n(1 - s). Each rank-one cell's power
               at n = 120 to 240 is compared with its base cell's at n(1 - s), interpolated linearly (with power
               0 at n = 0). A miss of more than two standard errors makes s a dimension of the table before
               the seal.
  specificity  Under each non-GEO cell the claim may pass in at most 1 of 50 studies at every n.
pilot_analysis.py reads `cells`, `kappas`, `targets` and `ns`.
"""
import glob
import hashlib
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rehearsal as R  # noqa: E402

FORMAT = "correlation-power-table/1"
MARGIN = 0.005
CHECK_NS = (120, 160, 200, 240)


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def wilson(k, n, z=1.959963984540054):
    p, d = k / n, 1 + z * z / n
    c, h = p + z * z / (2 * n), z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [float(max(0.0, (c - h) / d)), float(min(1.0, (c + h) / d))]


def var(k, m):
    p = (k + 1) / (m + 2)       # never zero, so a cell at 0 or 50 of 50 still has a standard error
    return p * (1 - p) / m


def name(kappa, target):
    return f"G{round(kappa * 100):03d}T{round(target * 10):02d}"


def main(d, out):
    cells, inputs = {}, {}
    for f in sorted(glob.glob(os.path.join(d, "rehearsal_*.json"))):
        with open(f) as fh:
            r = json.load(fh)
        if r.get("version") != 5 or not (r.get("spec") or {}).get("v5"):
            continue
        mi, m, ns = r["margins"].index(MARGIN), len(r["sims"]), r["ns"]
        claim = lambda s, n: all(s[f"n{n}"][h]["pass"][mi] for h in ("H_vs_EARLY", "H_vs_RDU", "H_vs_CAG"))  # noqa: E731
        k = {str(n): int(sum(claim(s, n) for s in r["sims"])) for n in ns}
        sec = lambda s, n: (s[f"n{n}"]["secondary"]["SH1_IA_beats_GEO"]["pass"]  # noqa: E731
                            and s[f"n{n}"]["secondary"]["SH2_straddle_beyond_GEO"]["pass"])
        cells[r["truth"]] = {
            "spec": r["spec"], "studies": m, "passes": k, "power": {n: v / m for n, v in k.items()},
            "ci95": {n: wilson(v, m) for n, v in k.items()},
            "single": {h: {str(n): float(np.mean([s[f"n{n}"][h]["pass"][mi] for s in r["sims"]])) for n in ns}
                       for h in ("H_vs_EARLY", "H_vs_RDU", "H_vs_CAG")},
            "secondary_claim": {str(n): float(np.mean([sec(s, n) for s in r["sims"]])) for n in ns},
            "seconds": r["seconds"]}
        inputs[os.path.basename(f)] = sha256(f)
    rows = {c: v for c, v in cells.items() if v["spec"]["base"] == "GEO" and not v["spec"]["share"]
            and v["spec"]["lapse"] == 0.06}
    ns = sorted({int(n) for v in cells.values() for n in v["power"]})
    res = {"format": FORMAT, "source": "rehearsal.py version 5, simulated studies", "margin": MARGIN, "ns": ns,
           "kappas": sorted({v["spec"]["kappa"] for v in rows.values()}),
           "targets": sorted({v["spec"]["target"] for v in rows.values()}),
           "missing": [c for c in R.TABLE_V5 if c not in cells], "cells": cells, "rank_one": {}, "specificity": {},
           "inputs_sha256": inputs, "code_sha256": {f: sha256(os.path.join(os.path.dirname(os.path.abspath(__file__)), f))
                                                    for f in ("rehearsal.py", "models.py", "stimuli.py", "power_table.py")}}
    for c, v in cells.items():
        sp = v["spec"]
        if sp["base"] == "GEO" and sp["share"]:
            base = rows.get(name(sp["kappa"], sp["target"]))
            if base is None:
                continue
            xs = [0] + ns
            checks = []
            for n in CHECK_NS:
                x = n * (1 - sp["share"])
                j = int(np.searchsorted(xs, x))
                w = 1.0 if xs[j] == x else (xs[j] - x) / (xs[j] - xs[j - 1])
                pts = [(j, 1.0)] if w == 1.0 else [(j - 1, w), (j, 1 - w)]
                pw = lambda i: 0.0 if i == 0 else base["power"][str(xs[i])]  # noqa: E731
                vr = lambda i: 0.0 if i == 0 else var(base["passes"][str(xs[i])], base["studies"])  # noqa: E731
                pred = sum(wt * pw(i) for i, wt in pts)
                se = float(np.sqrt(var(v["passes"][str(n)], v["studies"]) + sum(wt * wt * vr(i) for i, wt in pts)))
                obs = v["power"][str(n)]
                checks.append({"n": n, "n_effective": x, "power": obs, "predicted": float(pred), "se": se,
                               "z": float((obs - pred) / se), "miss": bool(abs(obs - pred) > 2 * se)})
            res["rank_one"][c] = {"base": name(sp["kappa"], sp["target"]), "share": sp["share"], "checks": checks,
                                  "misses": any(ch["miss"] for ch in checks)}
        elif sp["base"] != "GEO":
            res["specificity"][c] = {"passes": v["passes"], "max": max(v["passes"].values()),
                                     "ok": max(v["passes"].values()) <= 1}
    res["s_becomes_a_dimension"] = any(x["misses"] for x in res["rank_one"].values())
    res["specificity_ok"] = all(x["ok"] for x in res["specificity"].values()) if res["specificity"] else None
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)
    print(f"power of the main claim (H1, H2, H3 at margin {MARGIN}), percent of studies, n = " + " / ".join(map(str, ns)))
    for k in res["kappas"]:
        print(f"  kappa {k:<5}" + "   ".join(
            f"T{t}: " + "/".join(f"{100 * rows[name(k, t)]['power'][str(n)]:.0f}" for n in ns) if name(k, t) in rows
            else f"T{t}: (missing)" for t in res["targets"]))
    for c, x in res["rank_one"].items():
        print(f"rank one {c} (s = {x['share']}, base {x['base']}): " + "; ".join(
            f"n {ch['n']}: {100 * ch['power']:.0f} vs {100 * ch['predicted']:.0f} predicted (z {ch['z']:+.1f})"
            for ch in x["checks"]) + ("  MISS" if x["misses"] else ""))
    for c, x in res["specificity"].items():
        print(f"specificity {c}: passes {x['passes']} {'ok' if x['ok'] else 'TOO MANY'}")
    print("missing cells:", res["missing"] or "none")


if __name__ == "__main__":
    main(*sys.argv[1:3])
