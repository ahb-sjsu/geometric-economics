#!/usr/bin/env python3
"""The power table (PILOT.md) from rehearsal.py's version 6 rehearsal_<CELL>.json files.

    python power_table.py DIR OUT.json [V5_TABLE.json]

For each cell and n, the main claim's pass rate (H1, H2 and H3 at margin 0.005) over the cell's simulated
studies, with a 95% Wilson interval, in two populations: every simulated person (`power`, the claim as DESIGN.md
registers it), and the people the main study's self-only flag does not catch, recruited until there are n of
them (`power_unflagged`). Checks, as PILOT.md defines them:
  rank one     A share s of rank-one people should act like a sample of n(1 - s). Each rank-one cell's power
               at n = 120 to 240 is compared with its base cell's at n(1 - s), interpolated linearly (with power
               0 at n = 0). Version 5 found misses of more than two standard errors, so s is now a dimension of
               the table; the check is kept as a record.
  specificity  Under each non-GEO cell the claim may pass in at most 1 of 50 studies at every n, in both
               populations.
  version 5    With V5_TABLE.json, each version 5 cell's passes against its rerun. Version 6 changed no simulated
               choice the claim reads, but floating point can differ between NRP nodes, so the check reports how
               far each cell moved rather than requiring none to.
pilot_analysis.py reads `cells`, `kappas`, `targets`, `shares` and `ns`.
"""
import glob
import hashlib
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rehearsal as R  # noqa: E402

FORMAT = "correlation-power-table/2"
MARGIN = 0.005
CHECK_NS = (120, 160, 200, 240)
HS = ("H_vs_EARLY", "H_vs_RDU", "H_vs_CAG")


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


def name(kappa, target, share=0.0):
    return f"G{round(kappa * 100):03d}T{round(target * 10):02d}" + (f"S{round(share * 100):02d}" if share else "")


def rate(k, n):
    return k / n if n else None


def main(d, out, v5_path=None):
    cells, inputs = {}, {}
    for f in sorted(glob.glob(os.path.join(d, "rehearsal_*.json"))):
        with open(f) as fh:
            r = json.load(fh)
        if r.get("version") != 6 or not (r.get("spec") or {}).get("v5"):
            continue
        mi, m, ns, sims = r["margins"].index(MARGIN), len(r["sims"]), r["ns"], r["sims"]
        claim = lambda rec, n: all(rec[f"n{n}"][h]["pass"][mi] for h in HS)  # noqa: E731
        sec = lambda rec, n: (rec[f"n{n}"]["secondary"]["SH1_IA_beats_GEO"]["pass"]  # noqa: E731
                              and rec[f"n{n}"]["secondary"]["SH2_straddle_beyond_GEO"]["pass"])
        c = {"spec": r["spec"], "studies": m, "seconds": r["seconds"]}
        for suffix, get in (("", lambda s: s), ("_unflagged", lambda s: s["unflagged"])):
            k = {str(n): int(sum(claim(get(s), n) for s in sims)) for n in ns}
            c.update({f"passes{suffix}": k, f"power{suffix}": {n: v / m for n, v in k.items()},
                      f"ci95{suffix}": {n: wilson(v, m) for n, v in k.items()},
                      f"single{suffix}": {h: {str(n): float(np.mean([get(s)[f"n{n}"][h]["pass"][mi] for s in sims]))
                                              for n in ns} for h in HS},
                      f"secondary_claim{suffix}": {str(n): float(np.mean([sec(get(s), n) for s in sims])) for n in ns}})
        fl = {g: [sum(s["flags"][g][i] for s in sims) for i in (0, 1)] for g in ("rank_one", "trader")}
        c["main_flag"] = {"tpr": rate(*fl["rank_one"]), "fpr": rate(*fl["trader"]), "counts": fl}
        c["extras_mean"] = float(np.mean([s["unflagged"]["extras"] for s in sims]))
        c["residual_rank_one"] = float(np.mean([s["unflagged"]["residual_rank_one"] for s in sims]))
        cells[r["truth"]] = c
        inputs[os.path.basename(f)] = sha256(f)
    geo = {c: v for c, v in cells.items() if v["spec"]["base"] == "GEO" and v["spec"]["lapse"] == 0.06}
    rows = {c: v for c, v in geo.items() if not v["spec"]["share"]}
    ns = sorted({int(n) for v in cells.values() for n in v["power"]})
    res = {"format": FORMAT, "source": "rehearsal.py version 6, simulated studies", "margin": MARGIN, "ns": ns,
           "kappas": sorted({v["spec"]["kappa"] for v in rows.values()}),
           "targets": sorted({v["spec"]["target"] for v in rows.values()}),
           "shares": sorted({v["spec"]["share"] for v in geo.values()}),
           "missing": [c for c in R.TABLE_V6 if c not in cells], "cells": cells, "rank_one": {}, "specificity": {},
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
            res["specificity"][c] = {"passes": v["passes"], "passes_unflagged": v["passes_unflagged"],
                                     "max": max(max(v["passes"].values()), max(v["passes_unflagged"].values()))}
            res["specificity"][c]["ok"] = res["specificity"][c]["max"] <= 1
    res["specificity_ok"] = all(x["ok"] for x in res["specificity"].values()) if res["specificity"] else None
    if v5_path:
        with open(v5_path) as fh:
            v5 = json.load(fh)
        rep = {c: cells[c]["passes"] == old["passes"] for c, old in v5["cells"].items() if c in cells}
        # the largest change in passes at any n. Version 5 and 6 ran on different NRP nodes, and floating point can
        # differ between machines: on Atlas the two versions' records were identical, and on NRP they differed by
        # about 1e-6 in a typical H estimate, enough to move a study near the margin.
        gap = {c: max(abs(cells[c]["passes"][n] - old["passes"][n]) for n in old["passes"])
               for c, old in v5["cells"].items() if c in cells}
        res["v5_reproduced"] = {"table_sha256": sha256(v5_path), "cells": rep, "max_pass_change": gap,
                                "all": bool(rep) and all(rep.values()) and len(rep) == len(v5["cells"])}
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)

    def line(c, key):
        return "/".join(f"{100 * cells[c][key][str(n)]:.0f}" for n in ns) if c in cells else "(missing)"

    print(f"main claim (H1, H2, H3 at margin {MARGIN}), percent of studies at n = " + " / ".join(map(str, ns)))
    for s in res["shares"]:
        print(f"share of rank-one people {s}: every person | unflagged people")
        for k in res["kappas"]:
            rs = [name(k, t, s) for t in res["targets"] if name(k, t, s) in cells]
            if rs:
                print(f"  kappa {k:<5}" + "   ".join(f"T{cells[c]['spec']['target']}: {line(c, 'power')} | "
                                                     f"{line(c, 'power_unflagged')}" for c in rs))
    for c, x in res["rank_one"].items():
        print(f"rank one {c}: " + "; ".join(f"n {ch['n']}: {100 * ch['power']:.0f} vs {100 * ch['predicted']:.0f}"
                                            for ch in x["checks"]) + ("  MISS" if x["misses"] else ""))
    for c, x in res["specificity"].items():
        print(f"specificity {c}: {x['passes']} | unflagged {x['passes_unflagged']} {'ok' if x['ok'] else 'TOO MANY'}")
    print("main flag tpr/fpr by cell:", {c: (round(v["main_flag"]["tpr"], 3) if v["main_flag"]["tpr"] is not None
                                            else None, round(v["main_flag"]["fpr"], 4)) for c, v in cells.items()})
    if "v5_reproduced" in res:
        bad = {c: res["v5_reproduced"]["max_pass_change"][c] for c, ok in res["v5_reproduced"]["cells"].items() if not ok}
        print("version 5 reproduced exactly:", res["v5_reproduced"]["all"], "| cells that moved (largest change in passes "
              "of 50):", bad or "none")
    print("missing cells:", res["missing"] or "none")


if __name__ == "__main__":
    main(*sys.argv[1:4])
