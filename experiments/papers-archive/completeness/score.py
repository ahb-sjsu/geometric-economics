#!/usr/bin/env python3
"""Completeness and restrictiveness of one corpus. Design in DEVELOPMENT.md, written before any score.

    python score.py DATA_DIR NAME OUT.json [--folds F] [--draws M]

Needs strata_models.py beside it (a copy of ../strata/strata_models.py). Prints the result JSON
between RESULT markers as well, so a Job log carries it.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import strata_models as M  # noqa: E402

FOLD_SEED, DRAW_SEED = 20261101, 20261102
N_STARTS_CV, N_STARTS_R = 5, 3
N_BOOT = 2000
MODELS = {"EV": M.logit_ev, "RUM": M.logit_rum, "GDT2": M.logit_gdt2, "GDTS": M.logit_gdts,
          "CPT_unit": M.make_cpt("unit"), "CPT_share": M.make_cpt("share")}


def sig(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))


def nll(z, k, n):
    return float(-(k * -np.logaddexp(0, -z) + (n - k) * -np.logaddexp(0, z)).sum() / n.sum())


def fit(loss, x0, starts, rng):
    best = None
    for s in [np.array(x0, float)] + [np.array(x0, float) + rng.normal(0, 0.7, len(x0))
                                       for _ in range(starts - 1)]:
        try:
            r = minimize(loss, s, method="L-BFGS-B")
        except (FloatingPointError, ValueError):
            continue
        if np.isfinite(r.fun) and (best is None or r.fun < best.fun):
            best = r
    return best.x


def features(pr):
    cols = []
    for coding in ("unit", "share"):
        XA, PA, XB, PB = pr.coded(coding)
        for X, P in ((XA, PA), (XB, PB)):
            live = P > 0
            cols += [M.ev(X, P), M.sd(X, P), np.where(live, X, np.inf).min(1), np.where(live, X, -np.inf).max(1),
                     (P * (X < 0)).sum(1)]
        cols += [M.ev(XB, PB) - M.ev(XA, PA), M.sd(XB, PB) - M.sd(XA, PA)]
    XA, PA, XB, PB = pr.coded("share")
    for X, P in ((XA, PA), (XB, PB)):
        best = X.argmax(1)
        cols += [P[np.arange(len(P)), best], (P > 0).sum(1)]
    return np.column_stack(cols)


def dominates(Xa, Pa, Xb, Pb):
    """True if lottery a first-order stochastically dominates b."""
    t = np.unique(np.r_[Xa[Pa > 0], Xb[Pb > 0]])
    Fa = np.array([Pa[Xa <= v].sum() for v in t])
    Fb = np.array([Pb[Xb <= v].sum() for v in t])
    return bool(np.all(Fa <= Fb + 1e-12) and np.any(Fa < Fb - 1e-12))


def err_rate(pred, k, n):
    """Noise-corrected squared error on rates, per problem."""
    ph = k / n
    return (ph - pred) ** 2 - ph * (1 - ph) / (n - 1)


def logloss(pred, k, n):
    p = np.clip(pred, 1e-9, 1 - 1e-9)
    return -(k * np.log(p) + (n - k) * np.log1p(-p))


def completeness(pr, k, n, folds):
    rng = np.random.default_rng(FOLD_SEED)
    fold = rng.permutation(len(pr)) % folds
    feats = features(pr)
    pred = {m: np.zeros(len(pr)) for m in list(MODELS) + ["naive", "GB", "RF"]}
    theta = {m: [] for m in MODELS}
    for f in range(folds):
        tr, te = fold != f, fold == f
        ptr, pte = pr.subset(tr), pr.subset(te)
        pred["naive"][te] = k[tr].sum() / n[tr].sum()
        for m, fn in MODELS.items():
            th = fit(lambda t: nll(fn(t, ptr), k[tr], n[tr]), M.X0[m], N_STARTS_CV,
                     np.random.default_rng(FOLD_SEED + f))
            theta[m].append([float(x) for x in th])
            pred[m][te] = sig(fn(th, pte))
        y, w = k[tr] / n[tr], n[tr]
        gb = GradientBoostingRegressor(n_estimators=300, max_depth=2, learning_rate=0.05, subsample=0.8,
                                       random_state=f).fit(feats[tr], y, sample_weight=w)
        rf = RandomForestRegressor(n_estimators=500, min_samples_leaf=3, random_state=f).fit(
            feats[tr], y, sample_weight=w)
        pred["GB"][te] = np.clip(gb.predict(feats[te]), 1e-4, 1 - 1e-4)
        pred["RF"][te] = np.clip(rf.predict(feats[te]), 1e-4, 1 - 1e-4)
    e = {m: err_rate(p, k, n) for m, p in pred.items()}
    ll = {m: logloss(p, k, n) for m, p in pred.items()}
    ml = "GB" if e["GB"].mean() <= e["RF"].mean() else "RF"

    def scores(idx):
        en, eml = e["naive"][idx].mean(), e[ml][idx].mean()
        ln, lml = ll["naive"][idx].sum() / n[idx].sum(), ll[ml][idx].sum() / n[idx].sum()
        out = {}
        for m in MODELS:
            em, lm = e[m][idx].mean(), ll[m][idx].sum() / n[idx].sum()
            out[m] = {"vs_ml": (en - em) / (en - eml), "vs_ceiling": (en - em) / en,
                      "logloss_vs_ml": (ln - lm) / (ln - lml)}
        out[ml] = {"vs_ceiling": (en - eml) / en}
        return out

    point = scores(np.arange(len(pr)))
    brng = np.random.default_rng(FOLD_SEED + 99)
    boot = [scores(brng.integers(0, len(pr), len(pr))) for _ in range(N_BOOT)]
    ci = {m: {s: [float(np.percentile([b[m][s] for b in boot], q)) for q in (2.5, 97.5)] for s in point[m]}
          for m in point}
    return {"folds": folds, "ml_predictor": ml,
            "error_rate": {m: float(v.mean()) for m, v in e.items()},
            "logloss": {m: float(v.sum() / n.sum()) for m, v in ll.items()},
            "completeness": {m: {s: float(v) for s, v in d.items()} for m, d in point.items()}, "ci95": ci,
            "theta_per_fold": theta,
            "boot": {m: {s: [round(float(b[m][s]), 5) for b in boot] for s in point[m]} for m in point}}


def restrictiveness(pr, draws):
    rng = np.random.default_rng(DRAW_SEED)
    dom = np.zeros(len(pr))                                    # +1: B dominates A, -1: A dominates B
    for j in range(len(pr)):
        if dominates(pr.XB[j], pr.PB[j], pr.XA[j], pr.PA[j]):
            dom[j] = 1
        elif dominates(pr.XA[j], pr.PA[j], pr.XB[j], pr.PB[j]):
            dom[j] = -1
    ratios = {m: [] for m in MODELS}
    for d in range(draws):
        u = rng.random(len(pr))
        f = np.where(dom > 0, 0.5 + u / 2, np.where(dom < 0, u / 2, u))
        base = f.var()
        for m, fn in MODELS.items():
            th = fit(lambda t: float(((sig(fn(t, pr)) - f) ** 2).mean()), M.X0[m], N_STARTS_R,
                     np.random.default_rng(DRAW_SEED + 1000 * d + len(m)))
            ratios[m].append(float(((sig(fn(th, pr)) - f) ** 2).mean() / base))
    return {"draws": draws, "dominated_problems": int((dom != 0).sum()),
            "restrictiveness": {m: float(np.mean(v)) for m, v in ratios.items()},
            "se": {m: float(np.std(v, ddof=1) / np.sqrt(len(v))) for m, v in ratios.items()},
            "ratios": ratios}


def main(data_dir, name, out, *opts):
    o = dict(zip(opts[::2], opts[1::2]))
    folds, draws = int(o.get("--folds", 10)), int(o.get("--draws", 100))
    np.seterr(all="ignore")
    z = np.load(os.path.join(data_dir, f"problems_{name}.npz"))
    pr = M.Problems(z["XA"], z["PA"], z["XB"], z["PB"], unit=float(z["unit"]))
    k, n = z["k"], z["n"]
    t0 = time.time()
    comp = completeness(pr, k, n, folds)
    t1 = time.time()
    res = {"corpus": name, "problems": len(pr), "choices": float(n.sum()), "completeness": comp,
           "restrictiveness": restrictiveness(pr, draws), "seconds": {"completeness": t1 - t0,
                                                                     "restrictiveness": time.time() - t1}}
    json.dump(res, open(out, "w"), indent=1)
    print("RESULT-BEGIN")
    print(json.dumps(res))
    print("RESULT-END", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
