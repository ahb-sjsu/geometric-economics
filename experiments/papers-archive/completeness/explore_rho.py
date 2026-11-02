#!/usr/bin/env python3
"""Partial stake scaling, exploration. Design in DEVELOPMENT.md, "Partial stake scaling", written first.

    python explore_rho.py DATA_DIR NAME OUT.json [--folds F] [--draws M]

Needs score.py and strata_models.py beside it. Prints the result between RESULT markers.
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score as S  # noqa: E402
import strata_models as M  # noqa: E402

RHO_GRID = [-0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
RECOVER_RHO = [0.0, 0.5, 1.0]
RECOVER_REPS = 3
SEED = 20261103
CPT0 = [np.log(0.88), np.log(0.88), np.log(2.25), 0.0, 1.0]


def scaled(pr, rho):
    s = (pr.unit ** (1 - rho) * pr.stake ** rho)[:, None]
    return pr.XA / s, pr.PA, pr.XB / s, pr.PB


def cpt_logit(th, XA, PA, XB, PB):
    a, b, lam = np.exp(th[0]), np.exp(th[1]), np.exp(th[2])
    g = 0.28 + 1.72 / (1 + np.exp(-th[3]))
    return (M.cpt_value(XB, PB, a, b, lam, g) - M.cpt_value(XA, PA, a, b, lam, g)) * np.exp(th[4])


def cpt_rho(th, pr):
    return cpt_logit(th[:5], *scaled(pr, th[5]))


def cpt_fixed_rho(rho):
    return lambda th, pr: cpt_logit(th, *scaled(pr, rho))


def cpt_cu(th, pr):
    """Wilcox (2011) contextual utility on CPT values: dV over the range of v across the problem's outcomes."""
    a, b, lam = np.exp(th[0]), np.exp(th[1]), np.exp(th[2])
    g = 0.28 + 1.72 / (1 + np.exp(-th[3]))
    XA, PA, XB, PB = pr.coded("unit")
    X, P = np.c_[XA, XB], np.c_[PA, PB]
    v = np.where(X >= 0, np.abs(X) ** a, -lam * np.abs(X) ** b)
    rng = np.where(P > 0, v, -np.inf).max(1) - np.where(P > 0, v, np.inf).min(1)
    dv = M.cpt_value(XB, PB, a, b, lam, g) - M.cpt_value(XA, PA, a, b, lam, g)
    return np.exp(th[4]) * dv / np.maximum(rng, 1e-9)


def gdts_rho(th, pr):
    XA, PA, XB, PB = scaled(pr, th[6])
    cA, cB = M.gdts_cost_pair(th[:6], M.strata_coords(XA, PA), M.strata_coords(XB, PB))
    return cA - cB


MODELS = {"CPT_unit": (M.make_cpt("unit"), M.X0["CPT_unit"]), "CPT_share": (M.make_cpt("share"), M.X0["CPT_share"]),
          "CPT_rho": (cpt_rho, CPT0 + [0.5]), "CPT_CU": (cpt_cu, CPT0),
          "GDTS_rho": (gdts_rho, M.X0["GDTS"] + [0.5])}
RHO_FOLD = ["CPT_rho", "GDTS_rho"]
PAIRS = [("CPT_rho", "CPT_share"), ("CPT_rho", "CPT_CU"), ("CPT_share", "CPT_CU"), ("GDTS_rho", "CPT_rho"),
         ("CPT_rho", "CPT_unit")]


def fit_nll(fn, x0, pr, k, n, starts, seed):
    return S.fit(lambda t: S.nll(fn(t, pr), k, n), x0, starts, np.random.default_rng(seed))


def completeness(pr, k, n, folds):
    fold = np.random.default_rng(S.FOLD_SEED).permutation(len(pr)) % folds
    feats = S.features(pr)
    pred = {m: np.zeros(len(pr)) for m in list(MODELS) + ["naive", "ML"]}
    rho_fold = {m: [] for m in RHO_FOLD}
    ml_kind = None
    for f in range(folds):
        tr, te = fold != f, fold == f
        ptr, pte = pr.subset(tr), pr.subset(te)
        pred["naive"][te] = k[tr].sum() / n[tr].sum()
        for m, (fn, x0) in MODELS.items():
            th = fit_nll(fn, x0, ptr, k[tr], n[tr], S.N_STARTS_CV, S.FOLD_SEED + f)
            pred[m][te] = S.sig(fn(th, pte))
            if m in rho_fold:
                rho_fold[m].append(float(th[-1]))
    # the ML predictor exactly as in score.py (same folds, same settings, same choice rule)
    gb, rf = np.zeros(len(pr)), np.zeros(len(pr))
    from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
    for f in range(folds):
        tr, te = fold != f, fold == f
        y, w = k[tr] / n[tr], n[tr]
        gb[te] = np.clip(GradientBoostingRegressor(n_estimators=300, max_depth=2, learning_rate=0.05, subsample=0.8,
                                                   random_state=f).fit(feats[tr], y, sample_weight=w).predict(feats[te]),
                         1e-4, 1 - 1e-4)
        rf[te] = np.clip(RandomForestRegressor(n_estimators=500, min_samples_leaf=3, random_state=f).fit(
            feats[tr], y, sample_weight=w).predict(feats[te]), 1e-4, 1 - 1e-4)
    ml_kind = "GB" if S.err_rate(gb, k, n).mean() <= S.err_rate(rf, k, n).mean() else "RF"
    pred["ML"] = gb if ml_kind == "GB" else rf
    e = {m: S.err_rate(p, k, n) for m, p in pred.items()}

    def scores(idx):
        en, eml = e["naive"][idx].mean(), e["ML"][idx].mean()
        c = {m: (en - e[m][idx].mean()) / (en - eml) for m in MODELS}
        return {**c, **{f"{a}-{b}": c[a] - c[b] for a, b in PAIRS}}

    point = scores(np.arange(len(pr)))
    brng = np.random.default_rng(S.FOLD_SEED + 99)
    boot = [scores(brng.integers(0, len(pr), len(pr))) for _ in range(S.N_BOOT)]
    ci = {s: [float(np.percentile([b[s] for b in boot], q)) for q in (2.5, 97.5)] for s in point}
    return {"ml_predictor": ml_kind, "completeness_vs_ml": {s: float(v) for s, v in point.items()}, "ci95": ci,
            "rho_per_fold": rho_fold, "boot": {s: [round(float(b[s]), 5) for b in boot] for s in point}}


def profile(pr, k, n):
    out = {}
    for rho in RHO_GRID:
        fn = cpt_fixed_rho(rho)
        th = fit_nll(fn, CPT0, pr, k, n, S.N_STARTS_CV, SEED)
        out[str(rho)] = {"nll": S.nll(fn(th, pr), k, n), "alpha": float(np.exp(th[0])), "beta": float(np.exp(th[1]))}
    return out


def recovery(pr, n, th_all):
    out = []
    for rho in RECOVER_RHO:
        p = S.sig(cpt_rho(np.r_[th_all[:5], rho], pr))
        for rep in range(RECOVER_REPS):
            k = np.random.default_rng(SEED + 100 * rep + int(10 * rho)).binomial(n.astype(int), p).astype(float)
            th = fit_nll(cpt_rho, CPT0 + [0.5], pr, k, n, S.N_STARTS_CV, SEED + rep)
            out.append({"true": rho, "rep": rep, "recovered": float(th[5]), "alpha": float(np.exp(th[0]))})
    return out


def restrictiveness(pr, draws):
    rng = np.random.default_rng(S.DRAW_SEED)
    dom = np.zeros(len(pr))
    for j in range(len(pr)):
        if S.dominates(pr.XB[j], pr.PB[j], pr.XA[j], pr.PA[j]):
            dom[j] = 1
        elif S.dominates(pr.XA[j], pr.PA[j], pr.XB[j], pr.PB[j]):
            dom[j] = -1
    ratios = {"CPT_rho": [], "CPT_CU": []}
    for d in range(draws):
        u = rng.random(len(pr))
        f = np.where(dom > 0, 0.5 + u / 2, np.where(dom < 0, u / 2, u))
        for m in ratios:
            fn, x0 = MODELS[m]
            th = S.fit(lambda t: float(((S.sig(fn(t, pr)) - f) ** 2).mean()), x0, S.N_STARTS_R,
                       np.random.default_rng(S.DRAW_SEED + 1000 * d + len(m)))
            ratios[m].append(float(((S.sig(fn(th, pr)) - f) ** 2).mean() / f.var()))
    return {m: {"mean": float(np.mean(v)), "se": float(np.std(v, ddof=1) / np.sqrt(len(v)))} for m, v in ratios.items()}


def main(data_dir, name, out, *opts):
    o = dict(zip(opts[::2], opts[1::2]))
    folds, draws = int(o.get("--folds", 10)), int(o.get("--draws", 100))
    np.seterr(all="ignore")
    z = np.load(os.path.join(data_dir, f"problems_{name}.npz"))
    pr = M.Problems(z["XA"], z["PA"], z["XB"], z["PB"], unit=float(z["unit"]))
    k, n = z["k"], z["n"]
    t = {"start": time.time()}
    th_all = fit_nll(cpt_rho, CPT0 + [0.5], pr, k, n, S.N_STARTS_CV, SEED)
    res = {"corpus": name, "problems": len(pr),
           "stake": {"min": float(pr.stake.min()), "max": float(pr.stake.max()),
                     "ratio": float(pr.stake.max() / pr.stake.min()), "unit": pr.unit,
                     "log_sd": float(np.log(pr.stake).std())},
           "all_data_fit": {"rho": float(th_all[5]), "alpha": float(np.exp(th_all[0])),
                            "beta": float(np.exp(th_all[1])), "nll": S.nll(cpt_rho(th_all, pr), k, n)}}
    res["profile"] = profile(pr, k, n)
    t["profile"] = time.time()
    res["completeness"] = completeness(pr, k, n, folds)
    t["completeness"] = time.time()
    res["recovery"] = recovery(pr, n, th_all)
    t["recovery"] = time.time()
    res["restrictiveness"] = restrictiveness(pr, draws)
    t["end"] = time.time()
    res["seconds"] = {s: t[s] - t["start"] for s in t if s != "start"}
    json.dump(res, open(out, "w"), indent=1)
    print("RESULT-BEGIN")
    print(json.dumps(res))
    print("RESULT-END", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
