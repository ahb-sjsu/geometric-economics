#!/usr/bin/env python3
"""Summarise power_study / power_tree cells: pass rates by sample size, true rho and sigma.

    python aggregate_power.py LADDER_DIR TREE_DIR OUT.json

Rates are averaged over the six corpora that supply the true parameters; the lowest corpus is shown
beside the mean. Chi-square(1) 5% critical value 3.84 for the ladder's quasi-LR tests.

The registered rho tests (DEVELOPMENT.md, "The estimand"): rho = 1 and rho = 0 are rejected by a 95%
interval (person-clustered); the frozen 0.725 is checked against a band of +-TOL, because rho here
is a population-level quantity and differences between people move the pooled estimate a little.
  * reject_band0725: the 95% interval lies wholly outside 0.725 +- TOL (the frozen value fails).
  * within_band0725: the 90% interval lies wholly inside the band (equivalence, two one-sided tests).
"""
import glob
import json
import os
import sys

import numpy as np

CRIT = 3.84
RHO, TOL = 0.725, 0.05


def band_tests(est, se):
    return {"reject_band0725": bool(abs(est - RHO) - TOL > 1.96 * se),
            "within_band0725": bool(abs(est - RHO) + 1.645 * se < TOL)}


def ladder_tests(s):
    out = {"h1_alone": s["h1_est"] - 1.96 * s["h1_se"] > 0, "h1_pooled": s["h1_pooled_pass"],
           "qlr_reject_rho1": s["lr"]["1.0"] > CRIT, "qlr_reject_rho0": s["lr"]["0.0"] > CRIT,
           "qlr_reject_rho0725": s["lr"]["0.725"] > CRIT}
    if "reject_cluster" in s:                          # the registered, person-clustered tests
        out.update({"reject_rho1": s["reject_cluster"]["1.0"], "reject_rho0": s["reject_cluster"]["0.0"],
                    "reject_rho0725": s["reject_cluster"]["0.725"], **band_tests(s["rho_hat"], s["se_rho_cluster"])})
    return out


def tree_tests(s):
    return {"reject_wilcox_e0": s["reject_wilcox_e0"], "reject_rho1": s["reject_rho_1.0"],
            "reject_rho0": s["reject_rho_0.0"], "reject_rho0725": s["reject_rho_0.725"],
            **band_tests(s["rho_mean"], s["se_rho_mean"])}


def summarise(d, prefix, tests):
    cells = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(d, f"{prefix}_*.json")))]
    out = {}
    for c in cells:
        for N, sims in c["sims"].items():
            key = f"rho{c['rho_true']}_sigma{c['sigma']}_N{N}"
            rates = {t: float(np.mean([tests(s)[t] for s in sims])) for t in tests(sims[0])}
            out.setdefault(key, {})[c["corpus"]] = rates
    table = {}
    for key, per in out.items():
        tests_ = next(iter(per.values()))
        table[key] = {t: {"mean": round(float(np.mean([p[t] for p in per.values()])), 3),
                          "min": round(float(min(p[t] for p in per.values())), 3)} for t in tests_}
        table[key]["corpora"] = len(per)
    return table, cells


def main(ladder, tree, out):
    res = {}
    res["ladder"], lc = summarise(ladder, "power_study", ladder_tests)
    res["tree"], tc = summarise(tree, "power_tree", tree_tests)
    # tree: fitted curvature against the true one, as a bias check
    res["tree_curvature"] = {}
    for c in tc:
        for N, sims in c["sims"].items():
            res["tree_curvature"].setdefault(f"rho{c['rho_true']}_sigma{c['sigma']}_N{N}", []).append(
                {"corpus": c["corpus"], "alpha": round(c["alpha"], 3), "a_gain": round(float(np.median([s["d0"]["a"] for s in sims])), 3),
                 "beta": round(c["beta"], 3), "a_loss": round(float(np.median([s["d1"]["a"] for s in sims])), 3),
                 "rho_median": round(float(np.median([s["rho_mean"] for s in sims])), 3)})
    json.dump(res, open(out, "w"), indent=1)
    for part in ("ladder", "tree"):
        print(part.upper())
        for key in sorted(res[part], key=lambda k: (k.split("_N")[0], int(k.split("_N")[1]))):
            v = res[part][key]
            print(f"  {key:<26} n={v['corpora']}  " + "  ".join(f"{t} {x['mean']:.2f} (min {x['min']:.2f})"
                                                           for t, x in v.items() if t != "corpora"))


if __name__ == "__main__":
    main(*sys.argv[1:])
