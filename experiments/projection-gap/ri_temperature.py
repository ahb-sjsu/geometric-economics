#!/usr/bin/env python3
"""Rational-inattention temperature model — rigorous test vs the two alternatives.

The program's recurring nemesis is the temperature/magnitude architecture. Three
falsifiers all point at it: (1) the cost-dependent T predicted a PEAKED dose curve
(observed monotone); (2) the geometric magnitudes were ~5x over-predicted; (3) the
risk weight sign-flips with stakes (fourfold pattern; a separate lottery result).

Rational inattention (Sims; Matejka-McKay): the information-optimal choice rule is a
logit whose temperature is the price of a bit lambda, plus a prior/default anchor.
Crucially lambda is FIXED (not cost-dependent) and the prior anchors the baseline.
We test three temperature architectures on the projection-gap panel, each mapping a
temperature-free cost-gap g = c_B - c_A to a choice probability P(A) = sigma(g/T):

  fixed-T (naive):    P = sigma(g / T)                         [1 param]
  cost-dependent (orig): P = sigma(g / max(T0, c*|g|^p))       [3 params]  <- the falsifier
  rational inattention:  P = sigma(g / lambda + b)             [2 params]  fixed price + prior

Data: llm_full.jsonl (16,848 choices). Fit by binomial NLL over every (contrast,pole)
cell, weighted by n. Compare BIC; then the dose-shape and magnitude diagnostics.

    python ri_temperature.py
"""
from __future__ import annotations

import json
import os
from collections import defaultdict

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit  # logistic sigma

import contrasts as K
import geometric_model as M

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "human_pilot", "llm_full.jsonl")


def load_cells():
    """Per (contrast, pole): observed (kA, n) and the temperature-free cost-gap g."""
    obs = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for line in open(DATA, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("status") != "ok" or r.get("choice") not in ("A", "B"):
            continue
        obs[r["contrast"]][r.get("pole")][0] += int(r["choice"] == "A")
        obs[r["contrast"]][r.get("pole")][1] += 1
    cells = []
    by = {c.id: c for c in K.ALL_CONTRASTS}
    for cid, poles in obs.items():
        c = by.get(cid)
        if not c:
            continue
        for pole in ("lo", "hi"):
            if pole not in poles or poles[pole][1] == 0:
                continue
            a = c.a_hi if pole == "hi" else c.a_lo
            b = c.b_hi if pole == "hi" else c.b_lo
            g = M.cost(b) - M.cost(a)                      # temperature-free cost-gap, +g favors A
            kA, n = poles[pole]
            cells.append({"cid": cid, "pole": pole, "kind": c.kind, "g": g, "kA": kA, "n": n})
    return cells


# ---- temperature architectures: P(A) as a function of cost-gap g -------------
def p_fixed(g, th):        # T
    return expit(g / (abs(th[0]) + 1e-6))


def p_costdep(g, th):      # T0, c, p
    T0, c, p = abs(th[0]) + 1e-6, abs(th[1]), abs(th[2])
    T = np.maximum(T0, c * np.abs(g) ** p)
    return expit(g / T)


def p_ri(g, th):           # lambda, b (prior log-odds)
    return expit(g / (abs(th[0]) + 1e-6) + th[1])


MODELS = {
    "fixed-T":            (p_fixed, [0.5], 1),
    "cost-dependent":     (p_costdep, [0.5, 0.24, 2.13], 3),
    "rational-inatt.":    (p_ri, [1.0, 0.0], 2),
}


def nll(pfun, th, cells):
    tot = 0.0
    for c in cells:
        p = np.clip(pfun(c["g"], th), 1e-6, 1 - 1e-6)
        tot += -(c["kA"] * np.log(p) + (c["n"] - c["kA"]) * np.log(1 - p))
    return tot


def fit(pfun, x0, cells):
    best = None
    for s in range(6):
        rng = np.random.default_rng(s)
        start = np.array(x0) * rng.uniform(0.5, 1.5, len(x0)) + rng.normal(0, 0.1, len(x0))
        r = minimize(lambda th: nll(pfun, th, cells), start, method="Nelder-Mead",
                     options={"maxiter": 8000, "xatol": 1e-5, "fatol": 1e-5})
        if best is None or r.fun < best.fun:
            best = r
    return best


def main():
    cells = load_cells()
    N = sum(c["n"] for c in cells)
    print(f"projection-gap panel: {len(cells)} (contrast,pole) cells, {N} choices\n")

    print(f"{'model':18} {'#p':>3} {'NLL':>10} {'BIC':>10}")
    fits = {}
    for name, (pfun, x0, k) in MODELS.items():
        r = fit(pfun, x0, cells)
        bic = 2 * r.fun + k * np.log(N)
        fits[name] = (pfun, r.x, r.fun, bic)
        print(f"{name:18} {k:>3} {r.fun:>10.1f} {bic:>10.1f}")
    best = min(fits, key=lambda m: fits[m][3])
    print(f"\nbest by BIC: {best}")

    # ---- dose diagnostic: monotone (data) vs peaked (cost-dependent) ----
    print("\n== Dose diagnostic (D9.1-4; observed is MONOTONE) ==")
    dose = sorted([c for c in cells if c["kind"] == "dose" and c["pole"] == "hi"],
                  key=lambda c: c["cid"])
    dlo = {c["cid"]: c for c in cells if c["kind"] == "dose" and c["pole"] == "lo"}
    print(f"{'level':6} {'g_hi':>7} {'obs gap':>9} " +
          " ".join(f"{m[:8]:>10}" for m in MODELS))
    obs_gaps, pred_gaps = [], {m: [] for m in MODELS}
    for c in dose:
        og = c["kA"] / c["n"] - dlo[c["cid"]]["kA"] / dlo[c["cid"]]["n"]
        obs_gaps.append(og)
        row = f"{c['cid']:6} {c['g']:>7.2f} {og:>+9.3f} "
        for m, (pfun, th, *_ ) in fits.items():
            pg = pfun(c["g"], th) - pfun(dlo[c["cid"]]["g"], th)
            pred_gaps[m].append(pg)
            row += f"{pg:>+10.3f}"
        print(row)
    # monotonicity + peak location
    from scipy.stats import spearmanr
    print("\n  Spearman(predicted dose gaps, level) and peak level:")
    lvl = list(range(1, len(dose) + 1))
    print(f"  {'observed':16}: rho={spearmanr(obs_gaps, lvl)[0]:+.2f}  peak@level {int(np.argmax(obs_gaps))+1}")
    for m in MODELS:
        pg = pred_gaps[m]
        print(f"  {m:16}: rho={spearmanr(pg, lvl)[0]:+.2f}  peak@level {int(np.argmax(pg))+1}")

    # ---- magnitude diagnostic: implied vs observed on the real contrasts ----
    print("\n== Magnitude diagnostic (real contrasts: mean |predicted gap| / |observed gap|) ==")
    reals_hi = [c for c in cells if c["kind"] == "real" and c["pole"] == "hi"]
    rlo = {c["cid"]: c for c in cells if c["kind"] == "real" and c["pole"] == "lo"}
    for m, (pfun, th, *_ ) in fits.items():
        ratios = []
        for c in reals_hi:
            if c["cid"] not in rlo:
                continue
            og = c["kA"] / c["n"] - rlo[c["cid"]]["kA"] / rlo[c["cid"]]["n"]
            pg = pfun(c["g"], th) - pfun(rlo[c["cid"]]["g"], th)
            if abs(og) > 1e-3:
                ratios.append(abs(pg) / abs(og))
        print(f"  {m:16}: mean |pred|/|obs| = {np.mean(ratios):.2f} "
              f"(1.0 = calibrated; >>1 = over-predicts magnitude)")

    print("\n== Verdict ==")
    lam, b = fits["rational-inatt."][1]
    print(f"rational inattention: info price lambda={abs(lam):.2f}, prior log-odds b={b:+.2f} "
          f"(prior P(A)={expit(b):.2f}); ONE fixed price + prior across all contrasts.")
    print("HONEST: RI reduces to a logit-with-prior for one decision; the test is whether a FIXED "
          "price beats the cost-dependent T (dose shape + BIC) and whether the prior fixes the "
          "baseline. It does NOT by itself explain the fourfold sign-flip (a utility-curvature effect).")


if __name__ == "__main__":
    main()
