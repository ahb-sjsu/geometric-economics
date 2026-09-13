#!/usr/bin/env python3
"""Fits every model registered in prereg-boundary-v1 and writes results.json.

This file contains NO thresholds and makes NO pass/fail judgement. Grading is
`boundary_grade.py`, which was written first.

Usage:
  python boundary_fit.py --data <path to 112485-V1.zip>
  python boundary_fit.py --smoke          # synthetic data, pipeline check only

Specification is prereg-boundary-v1.md Sections 2 and 4, frozen 2026-09-10.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import zipfile

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIES = ("SR", "C", "IN")
DAILY_WAGE = {"IN": 100.0, "C": 2666.666666666667, "SR": 240.0}

# Part I coordinates, prereg Section 4. Order d1..d9.
REF = np.array([0.5, 1.0, 0.8, 1.0, 0.5, 0.0, 0.6, 0.5, 0.5])
SIGMA_SQ_BASE = np.array([np.nan, 1e6, 1e6, 1e6, 1e6, 1e6, 32.28, 1e6, 1e6])


# ----------------------------------------------------------------- data ------
def load(path: str) -> pd.DataFrame:
    with zipfile.ZipFile(path) as z:
        # The archive was packaged on macOS and carries an AppleDouble resource
        # fork, "data/._20100982_DATA.dta", whose name also ends with the data
        # file's name. Skip anything whose basename starts with "._".
        names = [n for n in z.namelist()
                 if n.endswith("20100982_DATA.dta")
                 and not os.path.basename(n).startswith("._")]
        if len(names) != 1:
            raise SystemExit("expected one data member, found %r" % names)
        raw = pd.read_stata(io.BytesIO(z.read(names[0])))
    return prepare(raw)


def prepare(raw: pd.DataFrame) -> pd.DataFrame:
    study = np.where(raw["SR"] == 1, "SR",
                     np.where(raw["C"] == 1, "C", "IN"))
    d = pd.DataFrame({
        "study": study,
        "accept": raw["accept"].astype(float),
        "x": raw["percent_offer"].astype(float) / 100.0,
        "stakes": raw["stakes"].astype(float),
        "m": raw["DaysW"].astype(float),
    })
    d["pie_days"] = d["stakes"] / d["study"].map(DAILY_WAGE)
    d["logm"] = np.log1p(d["m"])
    d["log_pie"] = np.log(d["pie_days"])
    d["log10_pie"] = np.log10(d["pie_days"])
    d["percent_offer"] = raw["percent_offer"].astype(float)
    if "wealth" in raw:
        d["wealth"] = raw["wealth"]
    return d


# ------------------------------------------------------------ logit core -----
def _design(d: pd.DataFrame, studies, money=None, per_study_money=False,
            pie=False) -> tuple[np.ndarray, list[str]]:
    cols, names = [], []
    for s in studies:
        ind = (d["study"] == s).to_numpy(float)
        cols += [ind, ind * d["x"].to_numpy()]
        names += [f"a_{s}", f"b_{s}"]
    if money is not None:
        mv = d[money].to_numpy()
        if per_study_money:
            for s in studies:
                cols.append((d["study"] == s).to_numpy(float) * mv)
                names.append(f"g_{s}")
        else:
            cols.append(mv)
            names.append("g")
    if pie:
        cols.append(d["log_pie"].to_numpy())
        names.append("h")
    return np.column_stack(cols), names


def _nll(beta, X, y):
    z = np.clip(X @ beta, -35, 35)
    return float(np.sum(np.logaddexp(0, z) - y * z))


def fit_logit(X, y):
    b0 = np.zeros(X.shape[1])
    res = minimize(_nll, b0, args=(X, y), method="BFGS",
                   options={"maxiter": 5000, "gtol": 1e-10})
    beta = res.x
    z = np.clip(X @ beta, -35, 35)
    p = 1 / (1 + np.exp(-z))
    W = p * (1 - p)
    cov = np.linalg.pinv((X * W[:, None]).T @ X)
    return beta, -_nll(beta, X, y), np.sqrt(np.diag(cov))


def logloss(beta, X, y):
    z = np.clip(X @ beta, -35, 35)
    p = np.clip(1 / (1 + np.exp(-z)), 1e-12, 1 - 1e-12)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def lr_test(ll_r, ll_f, df):
    stat = 2.0 * (ll_f - ll_r)
    return {"stat": stat, "df": df, "p": float(stats.chi2.sf(max(stat, 0.0), df))}


# ---------------------------------------------------------------- Model G ----
def g_costs(x, pie_days, sigma1_sq):
    """Cost of accepting and of rejecting, per prereg Section 4."""
    scale = pie_days / 200.0
    sig = SIGMA_SQ_BASE.copy()
    sig[0] = sigma1_sq
    n = len(x)
    ref = np.tile(REF, (n, 1))
    ref[:, 0] = 0.5 * scale

    acc = ref.copy()
    sat = np.minimum(2 * x, 1.0)
    acc[:, 0] = x * scale
    acc[:, 2] = 0.1 + 0.8 * sat
    acc[:, 6] = 0.3 + 0.3 * sat

    rej = ref.copy()
    rej[:, 0] = 0.0
    rej[:, 2] = 0.8
    rej[:, 6] = 0.7

    c_acc = np.sqrt(np.sum((acc - ref) ** 2 / sig, axis=1))
    c_rej = np.sqrt(np.sum((rej - ref) ** 2 / sig, axis=1))
    return c_acc, c_rej


def fit_modelG(d, studies, sigma1_upper=1e4):
    x = d["x"].to_numpy()
    pd_ = d["pie_days"].to_numpy()
    y = d["accept"].to_numpy()
    ind = {s: (d["study"] == s).to_numpy(float) for s in studies}

    def unpack(th):
        s1 = float(sigma1_upper / (1.0 + np.exp(-th[0])))  # in (0, upper)
        T = float(np.exp(np.clip(th[1], -20, 20)))
        return s1, T, th[2:]

    def nll(th):
        s1, T, alpha = unpack(th)
        ca, cr = g_costs(x, pd_, s1)
        z = (cr - ca) / T
        for a, s in zip(alpha, studies):
            z = z + a * ind[s]
        z = np.clip(z, -35, 35)
        return float(np.sum(np.logaddexp(0, z) - y * z))

    best = None
    for seed in range(6):
        rng = np.random.default_rng(20260910 + seed)
        th0 = np.concatenate([[rng.uniform(-3, 3), rng.uniform(-3, 1)],
                              rng.normal(0, 0.5, len(studies))])
        r = minimize(nll, th0, method="Nelder-Mead",
                     options={"maxiter": 20000, "xatol": 1e-9, "fatol": 1e-11})
        if best is None or r.fun < best.fun:
            best = r
    s1, T, alpha = unpack(best.x)
    return {"sigma1_sq": s1, "T": T,
            "alpha": {s: float(a) for s, a in zip(studies, alpha)},
            "loglik": -best.fun, "theta": best.x.tolist()}


def modelG_logloss(params, d, studies):
    x = d["x"].to_numpy(); pd_ = d["pie_days"].to_numpy(); y = d["accept"].to_numpy()
    ca, cr = g_costs(x, pd_, params["sigma1_sq"])
    z = (cr - ca) / params["T"]
    for s in studies:
        z = z + params["alpha"].get(s, 0.0) * (d["study"] == s).to_numpy(float)
    p = np.clip(1 / (1 + np.exp(-np.clip(z, -35, 35))), 1e-12, 1 - 1e-12)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


# ----------------------------------------------------------------- main ------
def run(d: pd.DataFrame) -> dict:
    y = d["accept"].to_numpy()
    out = {"n_total": int(len(d)),
           "n_by_study": {s: int((d["study"] == s).sum()) for s in STUDIES}}

    X0, n0 = _design(d, STUDIES)
    X1, n1 = _design(d, STUDIES, money="logm")
    X1s, n1s = _design(d, STUDIES, money="logm", per_study_money=True)
    X2, n2 = _design(d, STUDIES, money="logm", pie=True)

    fits = {}
    for tag, X, names in (("M0", X0, n0), ("M1", X1, n1),
                          ("M1s", X1s, n1s), ("M2", X2, n2)):
        b, ll, se = fit_logit(X, y)
        k = len(b)
        fits[tag] = {"coef": dict(zip(names, map(float, b))),
                     "se": dict(zip(names, map(float, se))),
                     "loglik": ll, "k": k,
                     "aic": 2 * k - 2 * ll, "bic": k * np.log(len(y)) - 2 * ll}
        out[tag] = fits[tag]

    out["M1"]["g"] = fits["M1"]["coef"]["g"]
    out["M2"]["h"] = fits["M2"]["coef"]["h"]
    zsc = fits["M2"]["coef"]["h"] / fits["M2"]["se"]["h"]
    out["M2"]["h_p"] = float(2 * stats.norm.sf(abs(zsc)))

    gs = [fits["M1s"]["coef"][f"g_{s}"] for s in STUDIES]
    out["M1s"]["g_by_study"] = dict(zip(STUDIES, map(float, gs)))
    if min(gs) != 0:
        out["M1s"]["g_ratio"] = float(max(gs) / min(gs))
    rng = np.random.default_rng(20260910)
    boots = []
    for _ in range(2000):
        idx = rng.integers(0, len(d), len(d))
        try:
            bb, _, _ = fit_logit(X1s[idx], y[idx])
            v = [bb[n1s.index(f"g_{s}")] for s in STUDIES]
            if min(v) != 0:
                boots.append(max(v) / min(v))
        except Exception:
            pass
    if boots:
        out["M1s"]["g_ratio_ci95"] = [float(np.percentile(boots, 2.5)),
                                      float(np.percentile(boots, 97.5))]

    out["lr_M0_vs_M1"] = lr_test(fits["M0"]["loglik"], fits["M1"]["loglik"], 1)
    out["lr_M1_vs_M1s"] = lr_test(fits["M1"]["loglik"], fits["M1s"]["loglik"], 2)
    out["lr_M1_vs_M2"] = lr_test(fits["M1"]["loglik"], fits["M2"]["loglik"], 1)

    # ---- leave-one-study-out -------------------------------------------------
    out["cv"] = []
    for s in STUDIES:
        tr = d[d["study"] != s].reset_index(drop=True)
        te = d[d["study"] == s].reset_index(drop=True)
        others = [t for t in STUDIES if t != s]

        Xtr, ntr = _design(tr, others, money="logm")
        btr, _, _ = fit_logit(Xtr, tr["accept"].to_numpy())
        g_hat = btr[ntr.index("g")]

        # primary reading: g transfers; the held-out study's own intercept and
        # share slope are nuisance parameters and are estimated on it.
        Xh, nh = _design(te, [s])
        off = g_hat * te["logm"].to_numpy()

        def nll_off(beta):
            z = np.clip(Xh @ beta + off, -35, 35)
            return float(np.sum(np.logaddexp(0, z) - te["accept"].to_numpy() * z))

        r = minimize(nll_off, np.zeros(Xh.shape[1]), method="BFGS",
                     options={"maxiter": 5000})
        zt = np.clip(Xh @ r.x + off, -35, 35)
        p = np.clip(1 / (1 + np.exp(-zt)), 1e-12, 1 - 1e-12)
        ya = te["accept"].to_numpy()
        m1_ll = float(-np.mean(ya * np.log(p) + (1 - ya) * np.log(1 - p)))

        # alternative reading: pooled intercept and slope from training too
        mean_a = np.mean([btr[ntr.index(f"a_{t}")] for t in others])
        mean_b = np.mean([btr[ntr.index(f"b_{t}")] for t in others])
        zp = np.clip(mean_a + mean_b * te["x"].to_numpy() + off, -35, 35)
        pp = np.clip(1 / (1 + np.exp(-zp)), 1e-12, 1 - 1e-12)
        m1_ll_pooled = float(-np.mean(ya * np.log(pp) + (1 - ya) * np.log(1 - pp)))

        Xo, _ = _design(te, [s], money="logm")
        bo, _, _ = fit_logit(Xo, ya)
        own_ll = logloss(bo, Xo, ya)

        gpar = fit_modelG(tr, others)
        gp = dict(gpar)
        gp["alpha"] = {s: float(np.mean(list(gpar["alpha"].values())))}
        g_ll = modelG_logloss(gp, te, [s])

        out["cv"].append({
            "held_out": s, "n_train": int(len(tr)), "n_test": int(len(te)),
            "g_train": float(g_hat),
            "m1_heldout_logloss": m1_ll,
            "m1_heldout_logloss_pooled_alt": m1_ll_pooled,
            "m1s_own_logloss": own_ll,
            "g_heldout_logloss": g_ll,
        })

    out["modelG"] = fit_modelG(d, STUDIES)

    # ---- proposer ------------------------------------------------------------
    out["proposer"] = {}
    for s in STUDIES:
        sub = d[d["study"] == s]
        X = np.column_stack([np.ones(len(sub)), sub["log10_pie"].to_numpy()])
        yy = sub["percent_offer"].to_numpy()
        XtXi = np.linalg.pinv(X.T @ X)
        beta = XtXi @ X.T @ yy
        resid = yy - X @ beta
        meat = (X * (resid ** 2)[:, None]).T @ X          # HC0
        V = XtXi @ meat @ XtXi
        se = float(np.sqrt(V[1, 1]))
        out["proposer"][s] = {
            "n": int(len(sub)), "slope_pp_per_decade": float(beta[1]),
            "se": se, "ci95_low": float(beta[1] - 1.96 * se),
            "ci95_high": float(beta[1] + 1.96 * se),
            "intercept": float(beta[0]),
        }
    return out


def smoke() -> pd.DataFrame:
    rng = np.random.default_rng(20260910)
    rows = []
    spec = {"SR": (820, [60, 300, 1500]), "C": (178, [5000, 40000, 200000]),
            "IN": (458, [20, 200, 2000, 20000])}
    for s, (n, stakes) in spec.items():
        st = rng.choice(stakes, n)
        x = np.clip(rng.normal(0.42, 0.12, n), 0.0, 1.0)
        pied = st / DAILY_WAGE[s]
        m = x * pied
        p = 1 / (1 + np.exp(-(-0.5 + 4.0 * x + 0.3 * np.log1p(m))))
        rows.append(pd.DataFrame({"SR": int(s == "SR"), "C": int(s == "C"),
                                  "IN": int(s == "IN"),
                                  "accept": rng.binomial(1, p),
                                  "percent_offer": x * 100, "stakes": st,
                                  "DaysW": m}))
    return prepare(pd.concat(rows, ignore_index=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--out", default=os.path.join(HERE, "results.json"))
    a = ap.parse_args()
    if a.smoke:
        d = smoke()
        a.out = os.path.join(HERE, "results_smoke.json")
        print("SMOKE RUN on synthetic data. Not a result.")
    else:
        if not a.data:
            ap.error("--data is required unless --smoke")
        d = load(a.data)
    res = run(d)
    res["smoke"] = bool(a.smoke)
    json.dump(res, open(a.out, "w", encoding="utf-8"), indent=2)
    print(f"n = {res['n_total']}  by study {res['n_by_study']}")
    print(f"written {a.out}")


if __name__ == "__main__":
    main()
