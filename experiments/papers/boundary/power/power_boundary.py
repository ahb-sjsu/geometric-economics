"""Power simulation for prereg-boundary-v1, Section 8.

Uses only the covariates of the bundled openICPSR file (offer share x, offered
amount in days of wages m, study) and the pre-freeze descriptive acceptance
rates of Section 3.  The observed accept/reject outcomes are never read.
Outcomes are simulated under model M1 of Section 4,

    logit P(accept) = a_s + b * x + g * log(1 + m),

with b fixed at 10 (acceptance rising from about 0.1 to 0.95 over shares
0.1 to 0.5) and a_s solved per study so that simulated acceptance at the
study's lowest stake matches the Section 3 descriptive at that stake.  For
each g in {0, 0.5, 1, 2} and each replicate: fit M0, M1, M1s by maximum
likelihood, record the likelihood-ratio p-value for P1 (M1 vs M0, alpha
0.01), the P2 homogeneity test (M1s vs M1, alpha 0.05) and the factor-of-2
spread of the three g_s, and the P3 test (M2 vs M1).

Run:  python power_boundary.py --data <path to 112485-V1.zip> --reps 500
"""

from __future__ import annotations

import argparse
import io
import json
import warnings
import zipfile

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.optimize import brentq
from scipy.stats import chi2

STUDIES = ("SR", "C", "IN")
LOWEST_STAKE_ACCEPT = {"SR": 0.829, "C": 0.783, "IN": 0.637}  # Section 3, lowest stake
B_SHARE = 10.0
G_GRID = (0.0, 0.5, 1.0, 2.0)


def load_covariates(path: str) -> pd.DataFrame:
    with zipfile.ZipFile(path) as z:
        d = pd.read_stata(io.BytesIO(z.read("data/20100982_DATA.dta")))
    d["study"] = d[["SR", "C", "IN"]].idxmax(axis=1)
    out = pd.DataFrame(
        {
            "study": d["study"].values,
            "x": d["percent_offer"].astype(float).values,
            "m": d["DaysW"].astype(float).values,
            "stakes": d["stakes"].astype(float).values,
        }
    )
    return out  # no outcome column on purpose


def design(df: pd.DataFrame, money: str) -> np.ndarray:
    cols = []
    for s in STUDIES:
        ind = (df["study"] == s).astype(float).values
        cols.append(ind)
        cols.append(ind * df["x"].values)
    lm = np.log1p(df["m"].values)
    if money == "shared":
        cols.append(lm)
    elif money == "study":
        for s in STUDIES:
            cols.append((df["study"] == s).astype(float).values * lm)
    elif money == "shared+pie":
        cols.append(lm)
        cols.append(np.log10(df["pie_days"].values))
    return np.column_stack(cols)


def fit_llf(y: np.ndarray, X: np.ndarray):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = sm.Logit(y, X).fit(disp=0, maxiter=200, method="newton")
    return res.llf, res.params


def solve_intercepts(df: pd.DataFrame, g: float) -> dict:
    a = {}
    for s in STUDIES:
        sub = df[df["study"] == s]
        low = sub[sub["stakes"] == sub["stakes"].min()]
        eta = B_SHARE * low["x"].values + g * np.log1p(low["m"].values)
        target = LOWEST_STAKE_ACCEPT[s]
        f = lambda a0: np.mean(1 / (1 + np.exp(-(a0 + eta)))) - target  # noqa: E731
        a[s] = brentq(f, -30, 30)
    return a


def simulate(df: pd.DataFrame, g: float, rng: np.random.Generator) -> np.ndarray:
    a = solve_intercepts(df, g)
    eta = np.array([a[s] for s in df["study"]]) + B_SHARE * df["x"].values + g * np.log1p(df["m"].values)
    return (rng.random(len(df)) < 1 / (1 + np.exp(-eta))).astype(float)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--reps", type=int, default=500)
    ap.add_argument("--seed", type=int, default=20260910)
    args = ap.parse_args()

    df = load_covariates(args.data)
    wage = {"IN": 100.0, "C": 1 / 0.000375, "SR": 240.0}
    df["pie_days"] = df["stakes"] / df["study"].map(wage)
    X0, X1, X1s, X2 = (design(df, k) for k in ("none", "shared", "study", "shared+pie"))
    rng = np.random.default_rng(args.seed)
    results = {}
    for g in G_GRID:
        p1 = p2 = spread = p3 = 0
        n_ok = 0
        for _ in range(args.reps):
            y = simulate(df, g, rng)
            try:
                l0, _ = fit_llf(y, X0)
                l1, b1 = fit_llf(y, X1)
                l1s, b1s = fit_llf(y, X1s)
                l2, b2 = fit_llf(y, X2)
            except Exception:
                continue
            n_ok += 1
            p1 += chi2.sf(2 * (l1 - l0), 1) < 0.01
            p2 += chi2.sf(2 * (l1s - l1), 2) < 0.05
            gs = np.abs(b1s[-3:])
            spread += (gs.max() / max(gs.min(), 1e-9)) <= 2.0 if g > 0 else 0
            p3 += chi2.sf(2 * (l2 - l1), 1) < 0.05
        results[g] = {
            "replicates": n_ok,
            "P1_reject_rate_alpha_0.01": p1 / n_ok,
            "P2_homogeneity_reject_rate_alpha_0.05": p2 / n_ok,
            "P2_factor_of_2_pass_rate": spread / n_ok if g > 0 else None,
            "P3_pie_term_reject_rate_alpha_0.05": p3 / n_ok,
        }
        print(f"g={g}: " + json.dumps(results[g]))
    print(json.dumps({"b_share": B_SHARE, "n": int(len(df)), "seed": args.seed, "results": {str(k): v for k, v in results.items()}}, indent=1))


if __name__ == "__main__":
    main()
