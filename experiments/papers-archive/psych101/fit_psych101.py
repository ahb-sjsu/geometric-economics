#!/usr/bin/env python3
"""prereg-psych101-v1. Carry Part II's CPC18 models, frozen, to wulff2018description.

    python fit_psych101.py                      # the registered run (opens rows_outcome.npz)
    python fit_psych101.py --simulate gdt       # rehearsal, choices drawn from frozen GDT
    python fit_psych101.py --simulate cpt       # rehearsal, choices drawn from frozen CPT

Models and fitter are imported from `experiments/datasets/fit_transfer.py`. Frozen
parameters come from `frozen_cpc18.json`. Problems are split in half at random
(SEED). On the calibration half each model refits ONE scalar, a multiplier `kappa`
on its frozen logit, because a metric's scale is not identified across contexts and
its shape is (theory paper, Proposition 2). Each model is also refit in full on the
calibration half (`native`). Everything is scored on the test half, per choice, in
nats, with a paired bootstrap over test problems, the unit the covariates live on.

Payoffs are divided by the standard deviation of option expected values over this
corpus's problems (stimuli only), the unit `freeze_cpc18.py` applies to CPC18, so a
frozen parameter means the same thing in both corpora. Under `--simulate`, the real
outcome file is never opened and the frozen model draws the choices in that unit.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "datasets"))
import cpc18  # noqa: E402
import fit_transfer  # noqa: E402
from fit_transfer import MODELS, fit, pred_cpt, _nll, _sig  # noqa: E402

SEED = 20261031
CAL_FRAC = 0.5
MARGIN_FRAC = 0.01          # margin = 1% of EV's calibration gain over the constant
N_BOOT = 2000               # paired bootstrap over test problems
N_BOOT_ANGLE = 500          # refits of native GDT on resampled calibration problems
CONV_TOL = 1e-6             # relative NLL change on a restart from the solution
EPS = 1e-6
FAMILY = {"EV": "EV", "RUM": "RUM", "GDT": "Geometric", "CPT": "CPT", "CPT_TK92": "CPT_TK92"}


def payoff_unit(A, B, prob):
    """SD of option EVs over distinct problems, the corpus's own stimulus-defined unit."""
    _, first = np.unique(prob, return_index=True)
    ev = lambda O: cpc18._opt_stats(O[first, 0], O[first, 1], O[first, 2])[0]
    return float(np.std(np.r_[ev(A), ev(B)]))


def frame(A, B, y):
    evA, sdA = cpc18._opt_stats(A[:, 0], A[:, 1], A[:, 2])
    evB, sdB = cpc18._opt_stats(B[:, 0], B[:, 1], B[:, 2])
    return pd.DataFrame({
        "evA": evA, "sdA": sdA, "evB": evB, "sdB": sdB, "amb": 0.0,
        "d_ev": evB - evA, "d_sd": sdB - sdA,
        "_Ha": A[:, 0], "_pHa": A[:, 1], "_La": A[:, 2],
        "_Hb": B[:, 0], "_pHb": B[:, 1], "_Lb": B[:, 2],
        "brate": y.astype(float), "n": 1.0})


def fn_of(name):
    return pred_cpt if name == "CPT_TK92" else MODELS[FAMILY[name]][0]


def raw_logit(fn, theta, d):
    """The model's logit, read from Part II's code with its sigmoid swapped for the identity.

    Inverting a predicted probability saturates where the frozen model is sharp (the
    first rehearsal failed on exactly that), so the logit is taken before the sigmoid.
    """
    sig = fit_transfer._sig
    fit_transfer._sig = lambda x: x
    try:
        return np.asarray(fn(theta, d), dtype=float)
    finally:
        fit_transfer._sig = sig


def row_loss(p, y):
    p = np.clip(p, EPS, 1 - EPS)
    return -(y * np.log(p) + (1 - y) * np.log1p(-p))


def fit_kappa(z, y):
    r = minimize_scalar(lambda lk: row_loss(_sig(10 ** lk * z), y).mean(), bounds=(-4, 4), method="bounded")
    return float(10 ** r.x)


def fit_native(fn, x0, d):
    """Full refit with Part II's fitter, then a restart from the solution as the convergence check."""
    y, n = d["brate"].to_numpy(), d["n"].to_numpy()
    th = fit(fn, list(x0), d)
    a = _nll(fn(th, d), y, n)
    th2 = fit(fn, list(th), d)
    b = _nll(fn(th2, d), y, n)
    return [float(t) for t in th2], abs(a - b) / max(abs(b), EPS) <= CONV_TOL


def ratio(theta):
    return abs(theta[0]) / (abs(theta[1]) + 1e-9)    # s_ev / s_sd, as cross_domain._ratio


def boot_diff(la, lb, prob, rng, n_boot=N_BOOT):
    """Paired bootstrap over problems of mean(la) - mean(lb) per choice."""
    u, inv = np.unique(prob, return_inverse=True)
    sa = np.bincount(inv, la); sb = np.bincount(inv, lb); cnt = np.bincount(inv)
    idx = rng.integers(0, len(u), size=(n_boot, len(u)))
    d = (sa[idx].sum(1) - sb[idx].sum(1)) / cnt[idx].sum(1)
    mean = float((la - lb).mean())
    return {"mean": mean, "ci_low": float(np.percentile(d, 2.5)),
            "ci_high": float(np.percentile(d, 97.5)), "se": float(d.std())}


def boot_dd(la, lb, prob, grp, rng):
    """(mean la-lb in grp 1) - (mean la-lb in grp 0), problems resampled within group."""
    out = []
    parts = []
    for g in (1, 0):
        m = grp == g
        u, inv = np.unique(prob[m], return_inverse=True)
        parts.append((np.bincount(inv, la[m] - lb[m]), np.bincount(inv), len(u)))
    for _ in range(N_BOOT):
        v = []
        for s, c, k in parts:
            i = rng.integers(0, k, size=k)
            v.append(s[i].sum() / c[i].sum())
        out.append(v[0] - v[1])
    m1, m0 = grp == 1, grp == 0
    mean = float((la[m1] - lb[m1]).mean() - (la[m0] - lb[m0]).mean())
    return {"mean": mean, "ci_low": float(np.percentile(out, 2.5)),
            "ci_high": float(np.percentile(out, 97.5))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--simulate", choices=["gdt", "cpt"])
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    frozen = json.load(open(os.path.join(HERE, "frozen_cpc18.json")))["models"]
    th0 = {k: frozen[FAMILY[k]]["theta"] for k in FAMILY}
    cov = np.load(os.path.join(HERE, "rows_covariates.npz"))
    A, B, prob, part = cov["A"], cov["B"], cov["problem"], cov["participant"]
    rng = np.random.default_rng(SEED)

    unit = payoff_unit(A, B, prob)
    A, B = A / [unit, 1, unit], B / [unit, 1, unit]     # the common unit, as freeze_cpc18
    sim = None
    if args.simulate:
        name = {"gdt": "GDT", "cpt": "CPT"}[args.simulate]
        p = fn_of(name)(th0[name], frame(A, B, np.zeros(len(A))))
        y = (np.random.default_rng(SEED + 1).random(len(p)) < p).astype(int)
        sim = {"truth": args.simulate}
    else:
        y = np.load(os.path.join(HERE, "rows_outcome.npz"))["chose_B"].astype(int)

    probs = np.unique(prob)
    perm = rng.permutation(probs)
    cal_set = set(perm[: int(len(perm) * CAL_FRAC)].tolist())
    cal = np.array([q in cal_set for q in prob])
    d = frame(A, B, y)
    dc, dt = d[cal].reset_index(drop=True), d[~cal].reset_index(drop=True)
    yc, yt = y[cal], y[~cal]

    res = {"prereg": "prereg-psych101-v1", "simulation": sim, "seed": SEED,
           "n": {"rows": int(len(y)), "problems": int(len(probs)), "participants": int(len(np.unique(part))),
                 "cal_rows": int(cal.sum()), "test_rows": int((~cal).sum()),
                 "cal_problems": len(cal_set), "test_problems": int(len(probs) - len(cal_set))},
           "payoff_unit": unit, "frozen_theta": th0, "kappa": {}, "native_theta": {}, "converged": {}}

    loss = {}
    base = yc.mean()
    loss["M0"] = row_loss(np.full(len(yt), base), yt)
    cal_m0 = row_loss(np.full(len(yc), base), yc).mean()
    for name in FAMILY:
        fn = fn_of(name)
        zc, zt = raw_logit(fn, th0[name], dc), raw_logit(fn, th0[name], dt)
        k = fit_kappa(zc, yc)
        res["kappa"][name] = k
        loss[f"{name}_transfer"] = row_loss(_sig(k * zt), yt)
        loss[f"{name}_zerofit"] = row_loss(_sig(zt), yt)
        if name != "CPT_TK92":
            th, ok = fit_native(fn, th0[name], dc)
            res["native_theta"][name], res["converged"][name] = th, bool(ok)
            loss[f"{name}_native"] = row_loss(fn(th, dt), yt)
    cal_ev = row_loss(fn_of("EV")(res["native_theta"]["EV"], dc), yc).mean()
    margin = MARGIN_FRAC * float(cal_m0 - cal_ev)
    res["margin"] = margin
    res["test_nll"] = {k: float(v.mean()) for k, v in loss.items()}

    pt = prob[~cal]
    comp = {
        "GDT_transfer-EV_native": ("GDT_transfer", "EV_native"),
        "GDT_transfer-RUM_transfer": ("GDT_transfer", "RUM_transfer"),
        "CPT_transfer-GDT_transfer": ("CPT_transfer", "GDT_transfer"),
        "GDT_transfer-CPT_TK92_transfer": ("GDT_transfer", "CPT_TK92_transfer"),
        "GDT_native-GDT_transfer": ("GDT_native", "GDT_transfer"),
        "CPT_native-CPT_transfer": ("CPT_native", "CPT_transfer"),
        "GDT_zerofit-CPT_zerofit": ("GDT_zerofit", "CPT_zerofit"),
    }
    brng = np.random.default_rng(SEED + 2)
    res["test_comparisons"] = {k: boot_diff(loss[a], loss[b], pt, brng) for k, (a, b) in comp.items()}

    At, Bt = A[~cal], B[~cal]
    has_loss = ((At[:, [0, 2]] < 0).any(1) | (Bt[:, [0, 2]] < 0).any(1)).astype(int)
    res["loss_domain"] = {
        "test_rows_with_a_loss": int(has_loss.sum()), "test_rows_gains_only": int((1 - has_loss).sum()),
        "GDT-CPT_with_loss_minus_gains_only": boot_dd(loss["GDT_transfer"], loss["CPT_transfer"], pt, has_loss, brng),
        "per_group_nll": {g: {k: float(loss[k][has_loss == gi].mean()) for k in loss}
                          for g, gi in (("with_loss", 1), ("gains_only", 0))}}

    nat = res["native_theta"]["GDT"]
    up = np.unique(prob[cal])
    arng = np.random.default_rng(SEED + 3)
    rs = []
    for _ in range(N_BOOT_ANGLE):
        pick = arng.choice(up, size=len(up), replace=True)
        cnt = np.bincount(np.searchsorted(up, pick), minlength=len(up))
        w = cnt[np.searchsorted(up, prob[cal])]
        db = dc.assign(n=w.astype(float))
        db = db[db["n"] > 0].reset_index(drop=True)
        rs.append(ratio(fit(MODELS["Geometric"][0], list(nat), db)))
    lr = np.log(rs)
    res["angle"] = {"frozen_ratio": ratio(th0["GDT"]), "native_ratio": ratio(nat),
                    "native_ci_low": float(np.exp(np.percentile(lr, 2.5))),
                    "native_ci_high": float(np.exp(np.percentile(lr, 97.5)))}

    chance = float(np.log(2))
    res["transfer_efficiency"] = {
        m: float((chance - res["test_nll"][f"{m}_transfer"]) / (chance - res["test_nll"][f"{m}_native"]))
        for m in ("GDT", "CPT", "RUM")}

    tag = f"sim_{args.simulate}" if args.simulate else "real"
    path = args.out or os.path.join(HERE, f"results_{tag}.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print("WROTE", path, json.dumps({"test_nll": res["test_nll"], "angle": res["angle"]}))


if __name__ == "__main__":
    main()
