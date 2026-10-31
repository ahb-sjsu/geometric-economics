#!/usr/bin/env python3
"""prereg-menus-v1: does the menu's range set the scale of evaluation, with Molter's exponent?

Data: Gluth, Spektor and Rieskamp 2018, all four experiments (rows from gluth_rows.py). On each trial
HV and LV can be chosen; on distractor trials a third option D is shown but cannot be chosen.

Per participant:
    1. fit each model on that participant's binary trials (no D)            -- calibration
    2. score the HV-vs-LV choices on that participant's distractor trials     -- test
       (trials where D was pressed are not scored; D cannot be chosen)
    3. fit RNGfree (rho free) on all of that participant's trials            -- H4 only
Comparisons average participants equally; intervals bootstrap over participants.

    python fit_menus.py run ROWS                 # the registered run (opens the outcome file)
    python fit_menus.py run ROWS --simulate T    # rehearsal, T in {ADD, RNG, RNG1, DN}
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import menus_models as MM  # noqa: E402

SEED = 20261031
STARTS = 4
N_BOOT = 2000
MARGIN_FRAC = 0.01
# rehearsal truths: person parameters drawn around these, lognormal jitter on the weights
SIM_THETA = {"ADD": [np.log(0.7), 0.0, np.log(0.9), np.log(5.0), np.log(5.0)],
             "RNG": [np.log(0.7), 0.0, np.log(0.9), np.log(3.0), np.log(3.0)],
             "RNG1": [np.log(0.7), 0.0, np.log(0.9), np.log(1.5), np.log(1.5)],
             "DN": [np.log(0.7), 0.0, np.log(0.9), np.log(12.0), 0.0, np.log(0.1)]}


def load(rows, simulate=None):
    c = np.load(os.path.join(rows, "gluth_covariates.npz"))
    has_d = ~np.isnan(c["d_mag"])
    P = np.c_[c["hv_prob"], c["lv_prob"], np.where(has_d, c["d_prob"], 0.5)]
    M = np.c_[c["hv_mag"], c["lv_mag"], np.where(has_d, c["d_mag"], 1.0)]
    shown = np.c_[np.ones_like(has_d), np.ones_like(has_d), has_d]
    avail = np.c_[np.ones_like(has_d), np.ones_like(has_d), np.zeros_like(has_d)]
    subj = c["subject"]
    if simulate:
        y = simulate_choices(simulate, P, M, shown, avail, subj)
    else:
        ch = np.load(os.path.join(rows, "gluth_outcome.npz"))["choice"]
        y = np.select([ch == "HV", ch == "LV"], [0, 1], default=2)
    return {"P": P, "M": M, "shown": shown, "avail": avail, "has_d": has_d, "subj": subj, "y": y,
            "exp": c["exp"]}


def simulate_choices(truth, P, M, shown, avail, subj):
    rng = np.random.default_rng(SEED + 100)
    y = np.zeros(len(subj), int)
    for s in np.unique(subj):
        m = subj == s
        th = np.array(SIM_THETA[truth], float)
        th[3:5] += rng.normal(0, 0.3, 2)
        lp = MM.log_probs(truth, th, P[m], M[m], shown[m], avail[m])
        u = rng.random(m.sum())
        y[m] = (u > np.exp(lp[:, 0])).astype(int)          # 0 = HV, 1 = LV
    return y


def nll(model, th, d, m):
    lp = MM.log_probs(model, th, d["P"][m], d["M"][m], d["shown"][m], d["avail"][m])
    return float(-lp[np.arange(m.sum()), d["y"][m]].mean())


def fit(model, d, m, rng):
    x0 = np.array(MM.x0(model))
    best = None
    for i in range(STARTS):
        s = x0 if i == 0 else x0 + rng.normal(0, 0.5, len(x0))
        r = minimize(lambda th: nll(model, th, d, m), s, method="L-BFGS-B")
        if best is None or r.fun < best.fun:
            best = r
    return best.x, float(best.fun), bool(best.success)


def boot(v, rng):
    b = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(N_BOOT)]
    return {"mean": float(v.mean()), "ci_low": float(np.percentile(b, 2.5)), "ci_high": float(np.percentile(b, 97.5))}


def boot_median(v, rng):
    b = [np.median(v[rng.integers(0, len(v), len(v))]) for _ in range(N_BOOT)]
    return {"median": float(np.median(v)), "ci_low": float(np.percentile(b, 2.5)), "ci_high": float(np.percentile(b, 97.5))}


def run(rows, simulate=None):
    d = load(rows, simulate)
    rng = np.random.default_rng(SEED)
    scored = d["y"] < 2
    per = {m: [] for m in MM.MODELS}
    rho_free, cal_add, conv_fail, n_test, exps = [], [], [], [], []
    for s in np.unique(d["subj"]):
        ms = d["subj"] == s
        cal = ms & ~d["has_d"] & scored
        test = ms & d["has_d"] & scored
        for model in MM.MODELS:
            th, loss, ok = fit(model, d, cal, rng)
            if not ok:
                conv_fail.append(f"{s}:{model}")
            if model == "ADD":
                cal_add.append(loss)
            per[model].append(nll(model, th, d, test))
        th, _, ok = fit("RNGfree", d, ms & scored, rng)
        rho_free.append(MM.rho_of(th))
        n_test.append(int(test.sum()))
        exps.append(str(d["exp"][ms][0]))
    per = {m: np.array(v) for m, v in per.items()}
    margin = MARGIN_FRAC * (np.log(2) - float(np.mean(cal_add)))
    res = {"prereg": "prereg-menus-v1", "simulation": simulate, "participants": len(n_test),
           "scored_test_choices": int(sum(n_test)), "excluded_D_presses": int((~scored).sum()),
           "rho_star": MM.RHO_STAR, "margin": margin, "nonconverged_fits": conv_fail,
           "test_nll": {m: float(v.mean()) for m, v in per.items()}, "comparisons": {}}
    for a, b in [("RNG", "ADD"), ("RNG", "DN"), ("RNG", "RNG1"), ("DN", "ADD"), ("RNG1", "ADD")]:
        res["comparisons"][f"{a} minus {b}"] = boot(per[a] - per[b], rng)
    res["comparisons"]["per_experiment_RNG_minus_ADD"] = {
        e: float(np.mean((per["RNG"] - per["ADD"])[np.array(exps) == e])) for e in sorted(set(exps))}
    res["rho_free"] = boot_median(np.array(rho_free), rng)
    tag = f"sim_{simulate}" if simulate else "real"
    json.dump(res, open(os.path.join(HERE, f"results_menus_{tag}.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    if sys.argv[1] == "run":
        sim = sys.argv[sys.argv.index("--simulate") + 1] if "--simulate" in sys.argv else None
        run(sys.argv[2], sim)
