#!/usr/bin/env python3
"""Structural fuzzing over the CHOICE RULE (redesign the caught culprit).

The projection-gap panel + CPC18 magnitudes convicted the cost-dependent
temperature T(Delta)=max(Tf, Tb*Delta^alpha), alpha=2.13. Because alpha>1, the
effective signal Delta/T ~ Delta^(1-alpha) DECREASES for large cost gaps -> the
model predicts washout (a dose peak) and tiny magnitudes, while data are monotone
and large.

We fuzz over response-function FAMILIES mapping the geometric cost gap to choice
probability, fit each on CPC18 (individual, held-out CV), and require MONOTONICITY
(the property the panel showed and the old rule broke). Winner = best held-out fit
that is also monotone.

Families (each on cost c(option)=sqrt(((EVmax-EV)/s_ev)^2+(SD/s_sd)^2)):
  logit_fixed   P(B)=sigmoid((cA-cB)/T)                    fixed temperature (monotone)
  temp_power    P(B)=sigmoid((cA-cB)/max(Tf,Tb|cA-cB|^a))  the CURRENT family, a free
  probit        P(B)=Phi((cA-cB)/s)                        Gaussian noise (monotone)
  luce          P(B)=cA^b/(cA^b+cB^b)                      power-law / Luce (monotone)
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

import cpc18


def _sig(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def _costs(d, s_ev, s_sd):
    evA, evB = d["evA"].to_numpy(), d["evB"].to_numpy()
    sdA, sdB = d["sdA"].to_numpy(), d["sdB"].to_numpy()
    evmax = np.maximum(evA, evB)
    cA = np.sqrt(((evmax - evA) / s_ev) ** 2 + (sdA / s_sd) ** 2)
    cB = np.sqrt(((evmax - evB) / s_ev) ** 2 + (sdB / s_sd) ** 2)
    return cA, cB


def _pred(name, theta, d):
    s_ev, s_sd = np.abs(theta[0]) + 1e-6, np.abs(theta[1]) + 1e-6
    cA, cB = _costs(d, s_ev, s_sd)
    dc = cA - cB
    if name == "logit_fixed":
        T = np.abs(theta[2]) + 1e-6
        return _sig(dc / T)
    if name == "temp_power":
        Tb, a, Tf = np.abs(theta[2]) + 1e-6, abs(theta[3]), np.abs(theta[4]) + 1e-6
        T = np.maximum(Tf, Tb * np.abs(dc) ** a)
        return _sig(dc / T)
    if name == "temp_power_OLD":  # alpha FROZEN at the TCSS-aggregate value 2.13
        Tb, Tf = np.abs(theta[2]) + 1e-6, np.abs(theta[3]) + 1e-6
        T = np.maximum(Tf, Tb * np.abs(dc) ** 2.13)
        return _sig(dc / T)
    if name == "probit":
        s = np.abs(theta[2]) + 1e-6
        return norm.cdf(dc / s)
    if name == "luce":
        b = np.abs(theta[2]) + 1e-6
        cA2, cB2 = cA + 1e-6, cB + 1e-6
        return cA2**b / (cA2**b + cB2**b)
    raise ValueError(name)


FAMILIES = {
    "temp_power_OLD": [3.0, 5.0, 0.24, 0.5],       # alpha frozen at 2.13 (the culprit)
    "logit_fixed":   [3.0, 5.0, 1.0],              # fixed temperature (the proposed redesign)
    "temp_power":    [3.0, 5.0, 0.24, 2.13, 0.5],  # cost-dep temp, alpha FREE
    "probit":        [3.0, 5.0, 1.0],
    "luce":          [3.0, 5.0, 2.0],
}


def _nll(name, theta, d):
    p = np.clip(_pred(name, theta, d), 1e-6, 1 - 1e-6)
    br, n = d["brate"].to_numpy(), d["n"].to_numpy()
    k = br * n
    return -np.sum(k * np.log(p) + (n - k) * np.log(1 - p)) / np.sum(n)


def _fit(name, train, x0):
    r = minimize(lambda th: _nll(name, th, train), x0, method="Nelder-Mead",
                 options={"maxiter": 8000, "xatol": 1e-5, "fatol": 1e-7})
    return r.x


def _mae(name, theta, d):
    p = np.clip(_pred(name, theta, d), 1e-6, 1 - 1e-6)
    return float(np.mean(np.abs(p - d["brate"].to_numpy())))


def _monotone(name, theta):
    """Does P(B) increase monotonically as B gets better (cost gap cA-cB rises)?
    Evaluate the response over a grid of cost gaps at fixed small SD."""
    import pandas as pd
    gaps = np.linspace(0.0, 6.0, 60)
    # synth: A fixed at (ev=0, sd=0); B improves (ev grows) -> cA-cB rises
    d = pd.DataFrame({"evA": np.zeros_like(gaps), "sdA": np.zeros_like(gaps),
                      "evB": gaps, "sdB": np.zeros_like(gaps)})
    p = _pred(name, theta, d)
    return bool(np.all(np.diff(p) >= -1e-9))


def main():
    df = cpc18.load_description()
    n_splits = 15
    print(f"choice-rule fuzzing on CPC18: {len(df)} games, {n_splits}-split held-out CV\n")
    print(f"{'family':13} {'#p':>3} {'TEST MAE':>10} {'TEST NLL':>10} {'monotone':>9}")
    rows = []
    for name, x0 in FAMILIES.items():
        maes, nlls = [], []
        theta_last = None
        for seed in range(n_splits):
            tr, te = cpc18.split_by_game(df, 0.3, seed)
            th = _fit(name, tr, x0)
            theta_last = th
            maes.append(_mae(name, th, te)); nlls.append(_nll(name, th, te))
        th_full = _fit(name, df, x0)
        mono = _monotone(name, th_full)
        extra = f"  alpha={abs(th_full[3]):.2f}" if name == "temp_power" else ""
        rows.append((name, np.mean(maes), np.mean(nlls), mono))
        print(f"{name:15} {len(x0):>3} {np.mean(maes):>10.4f} {np.mean(nlls):>10.4f} "
              f"{('yes' if mono else 'NO'):>9}{extra}")
    good = [r for r in rows if r[3]]
    best = min(good or rows, key=lambda r: r[2])
    print(f"\nBEST monotone choice rule: {best[0]} (held-out NLL {best[2]:.4f}, MAE {best[1]:.4f})")
    print("The old temp_power (alpha~2) family should show washout / worse fit; a fixed-temperature "
          "or probit/Luce rule should be monotone and fit at least as well -> the redesign.")


if __name__ == "__main__":
    main()
