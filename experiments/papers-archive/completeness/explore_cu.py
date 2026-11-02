#!/usr/bin/env python3
"""Diameter scaling, exploration: logit = theta * dC / D^rho. Design in DEVELOPMENT.md, "Diameter scaling".

    python explore_cu.py DATA_DIR NAME OUT.json [--folds F] [--draws M]

Needs score.py, explore_rho.py and strata_models.py beside it. Prints the result between RESULT markers.
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explore_rho as E  # noqa: E402
import score as S  # noqa: E402
import strata_models as M  # noqa: E402

RHO_GRID = [round(0.125 * i, 3) for i in range(13)]
SEED = 20261104


def _live_range(X, P):
    return np.where(P > 0, X, -np.inf).max(1) - np.where(P > 0, X, np.inf).min(1)


def cu_logit(th, rho, pr):
    """CPT values on the one-unit coding, difference over the range of v across the problem's outcomes, to rho."""
    a, b, lam = np.exp(th[0]), np.exp(th[1]), np.exp(th[2])
    g = 0.28 + 1.72 / (1 + np.exp(-th[3]))
    XA, PA, XB, PB = pr.coded("unit")
    X, P = np.c_[XA, XB], np.c_[PA, PB]
    v = np.where(X >= 0, np.abs(X) ** a, -lam * np.abs(X) ** b)
    D = np.maximum(_live_range(v, P), 1e-9)
    dv = M.cpt_value(XB, PB, a, b, lam, g) - M.cpt_value(XA, PA, a, b, lam, g)
    return np.exp(th[4]) * dv / D ** rho


def cpt_cur(th, pr):
    return cu_logit(th[:5], th[5], pr)


def cpt_cu_fixed(rho):
    return lambda th, pr: cu_logit(th, rho, pr)


def gdts_d(th, pr):
    XA, PA, XB, PB = pr.coded("unit")
    cA, cB = M.gdts_cost_pair(th[:6], M.strata_coords(XA, PA), M.strata_coords(XB, PB))
    D = np.maximum(_live_range(np.c_[XA, XB], np.c_[PA, PB]), 1e-9)
    return (cA - cB) / D ** th[6]


MODELS = {"CPT_unit": (M.make_cpt("unit"), M.X0["CPT_unit"]), "CPT_share": (M.make_cpt("share"), M.X0["CPT_share"]),
          "CPT_CU": (E.cpt_cu, E.CPT0), "CPT_CUr": (cpt_cur, E.CPT0 + [0.5]),
          "GDTS": (M.logit_gdts, M.X0["GDTS"]), "GDTS_D": (gdts_d, M.X0["GDTS"] + [0.5])}
PAIRS = [("CPT_CUr", "CPT_CU"), ("CPT_CUr", "CPT_share"), ("CPT_CU", "CPT_share"), ("GDTS_D", "GDTS"),
         ("GDTS_D", "CPT_CUr")]
RHO_MODELS = ["CPT_CUr", "GDTS_D"]


def main(data_dir, name, out, *opts):
    o = dict(zip(opts[::2], opts[1::2]))
    folds, draws = int(o.get("--folds", 10)), int(o.get("--draws", 100))
    np.seterr(all="ignore")
    z = np.load(os.path.join(data_dir, f"problems_{name}.npz"))
    pr = M.Problems(z["XA"], z["PA"], z["XB"], z["PB"], unit=float(z["unit"]))
    k, n = z["k"], z["n"]
    # reuse explore_rho's machinery with this file's models
    E.MODELS, E.PAIRS, E.RHO_FOLD = MODELS, PAIRS, RHO_MODELS
    t0 = time.time()
    th_all = E.fit_nll(cpt_cur, E.CPT0 + [0.5], pr, k, n, S.N_STARTS_CV, SEED)
    th_g = E.fit_nll(gdts_d, M.X0["GDTS"] + [0.5], pr, k, n, S.N_STARTS_CV, SEED)
    res = {"corpus": name, "problems": len(pr), "choices": float(n.sum()),
           "all_data_fit": {"rho_cpt_cur": float(th_all[5]), "alpha": float(np.exp(th_all[0])),
                            "rho_gdts_d": float(th_g[6]), "nll_cpt_cur": S.nll(cpt_cur(th_all, pr), k, n)}}
    prof = {}
    for rho in RHO_GRID:
        fn = cpt_cu_fixed(rho)
        th = E.fit_nll(fn, E.CPT0, pr, k, n, S.N_STARTS_CV, SEED)
        prof[str(rho)] = {"nll": S.nll(fn(th, pr), k, n), "alpha": float(np.exp(th[0]))}
    res["profile"] = prof
    comp = E.completeness(pr, k, n, folds)
    res["completeness"] = comp
    rec = []
    for rho in E.RECOVER_RHO:
        p = S.sig(cu_logit(th_all[:5], rho, pr))
        for rep in range(E.RECOVER_REPS):
            kk = np.random.default_rng(SEED + 100 * rep + int(10 * rho)).binomial(n.astype(int), p).astype(float)
            th = E.fit_nll(cpt_cur, E.CPT0 + [0.5], pr, kk, n, S.N_STARTS_CV, SEED + rep)
            rec.append({"true": rho, "rep": rep, "recovered": float(th[5]), "alpha": float(np.exp(th[0]))})
    res["recovery"] = rec
    E.MODELS = {m: MODELS[m] for m in RHO_MODELS}
    res["restrictiveness"] = restrictiveness(pr, draws)
    res["seconds"] = time.time() - t0
    json.dump(res, open(out, "w"), indent=1)
    print("RESULT-BEGIN")
    print(json.dumps(res))
    print("RESULT-END", flush=True)


def restrictiveness(pr, draws):
    rng = np.random.default_rng(S.DRAW_SEED)
    dom = np.zeros(len(pr))
    for j in range(len(pr)):
        if S.dominates(pr.XB[j], pr.PB[j], pr.XA[j], pr.PA[j]):
            dom[j] = 1
        elif S.dominates(pr.XA[j], pr.PA[j], pr.XB[j], pr.PB[j]):
            dom[j] = -1
    ratios = {m: [] for m in RHO_MODELS}
    for d in range(draws):
        u = rng.random(len(pr))
        f = np.where(dom > 0, 0.5 + u / 2, np.where(dom < 0, u / 2, u))
        for m in ratios:
            fn, x0 = MODELS[m]
            th = S.fit(lambda t: float(((S.sig(fn(t, pr)) - f) ** 2).mean()), x0, S.N_STARTS_R,
                       np.random.default_rng(S.DRAW_SEED + 1000 * d + len(m)))
            ratios[m].append(float(((S.sig(fn(th, pr)) - f) ** 2).mean() / f.var()))
    return {m: {"mean": float(np.mean(v)), "se": float(np.std(v, ddof=1) / np.sqrt(len(v)))} for m, v in ratios.items()}


if __name__ == "__main__":
    main(*sys.argv[1:])
