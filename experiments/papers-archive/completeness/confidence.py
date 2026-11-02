#!/usr/bin/env python3
"""Confidence on the spent data, before any sealed test of diameter scaling. Design in DEVELOPMENT.md,
"Building confidence on the spent data".

    python confidence.py DATA_DIR NAME OUT.json

NAME is a risky corpus (problems_<NAME>.npz; needs score.py, explore_rho.py, explore_cu.py and
strata_models.py beside it) or menus_molter / menus_gluth (needs menus_models.py beside it).
Prints the result between RESULT markers.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PROFILE = [round(0.025 * i, 3) for i in range(61)]          # 0 .. 1.5
FROZEN = [round(0.40 + 0.025 * i, 3) for i in range(29)]    # 0.40 .. 1.10
SEED = 20261105
if os.environ.get("CONF_QUICK"):                           # smoke test only
    PROFILE, FROZEN = [0.5, 1.0], [0.75, 1.0]


def warm_fit(loss, x0, prev, rng, starts):
    """Best of the previous solution and a few jittered starts."""
    best = None
    cands = ([np.array(prev, float)] if prev is not None else []) + [np.array(x0, float)] + \
            [np.array(x0, float) + rng.normal(0, 0.7, len(x0)) for _ in range(starts - 1)]
    for s in cands:
        try:
            r = minimize(loss, s, method="L-BFGS-B")
        except (FloatingPointError, ValueError):
            continue
        if np.isfinite(r.fun) and (best is None or r.fun < best.fun):
            best = r
    return best.x, float(best.fun)


# ---------------------------------------------------------------- risky
def risky(data_dir, name):
    import explore_cu as C
    import explore_rho as E
    import score as S
    import strata_models as M
    z = np.load(os.path.join(data_dir, f"problems_{name}.npz"))
    pr = M.Problems(z["XA"], z["PA"], z["XB"], z["PB"], unit=float(z["unit"]))
    k, n = z["k"], z["n"]
    rng = np.random.default_rng(SEED)
    prof, prev = {}, None
    for rho in PROFILE:
        fn = C.cpt_cu_fixed(rho)
        prev, f = warm_fit(lambda t: S.nll(fn(t, pr), k, n), E.CPT0, prev, rng, 3)
        prof[str(rho)] = f * float(n.sum())                    # total nats
    fold = np.random.default_rng(S.FOLD_SEED).permutation(len(pr)) % 10
    preds = {str(r): np.zeros(len(pr)) for r in FROZEN}
    naive = np.zeros(len(pr))
    for f in range(10):
        tr, te = fold != f, fold == f
        ptr, pte = pr.subset(tr), pr.subset(te)
        naive[te] = k[tr].sum() / n[tr].sum()
        prev = None
        for rho in FROZEN:
            fn = C.cpt_cu_fixed(rho)
            prev, _ = warm_fit(lambda t: S.nll(fn(t, ptr), k[tr], n[tr]), E.CPT0, prev, rng, 3)
            preds[str(rho)][te] = S.sig(fn(prev, pte))
    # the ML predictor exactly as in score.py: same folds and settings, the better of the two kept
    from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
    feats = S.features(pr)
    gb, rf = np.zeros(len(pr)), np.zeros(len(pr))
    for f in range(10):
        tr, te = fold != f, fold == f
        y, w = k[tr] / n[tr], n[tr]
        gb[te] = np.clip(GradientBoostingRegressor(n_estimators=300, max_depth=2, learning_rate=0.05, subsample=0.8,
                                                   random_state=f).fit(feats[tr], y, sample_weight=w).predict(feats[te]),
                         1e-4, 1 - 1e-4)
        rf[te] = np.clip(RandomForestRegressor(n_estimators=500, min_samples_leaf=3, random_state=f).fit(
            feats[tr], y, sample_weight=w).predict(feats[te]), 1e-4, 1 - 1e-4)
    ml = "GB" if S.err_rate(gb, k, n).mean() <= S.err_rate(rf, k, n).mean() else "RF"
    mlp = gb if ml == "GB" else rf
    err = lambda p: S.err_rate(p, k, n).round(7).tolist()    # noqa: E731
    return {"kind": "risky", "choices": float(n.sum()), "profile_total_nats": prof, "ml_predictor": ml,
            "err": {"naive": err(naive), "ML": err(mlp), **{r: err(p) for r, p in preds.items()}}}


# ---------------------------------------------------------------- menus
def menus(data_dir, name):
    import menus_models as MM
    z = np.load(os.path.join(data_dir, f"problems_{name}.npz"))
    P, Mg, shown, avail, y, subj = (z[x] for x in ("P", "M", "shown", "avail", "y", "subj"))

    def logp(th, rho, idx):
        p, m, sh, av = P[idx], Mg[idx], shown[idx], avail[idx]
        p = np.where(sh, p, 0.5); m = np.where(sh, m, 1.0)
        xp, xm = MM.coords(th, p, m)
        gp, gm = MM._mx(xp, sh) - xp, MM._mx(xm, sh) - xm
        gp = gp / (MM._mx(xp, sh) - MM._mn(xp, sh) + 1e-6) ** rho
        gm = gm / (MM._mx(xm, sh) - MM._mn(xm, sh) + 1e-6) ** rho
        c = np.exp(np.clip(th[3], -20, 20)) * gp + np.exp(np.clip(th[4], -20, 20)) * gm
        zz = np.where(av, -c, -np.inf)
        zz = zz - zz.max(1, keepdims=True)
        lp = zz - np.log(np.exp(zz).sum(1, keepdims=True))
        return lp[np.arange(len(idx)), y[idx]]

    rng = np.random.default_rng(SEED)
    allidx = np.arange(len(y))
    prof, prev = {}, None
    for rho in PROFILE:
        prev, f = warm_fit(lambda t: -logp(t, rho, allidx).mean(), MM.X0, prev, rng, 2)
        prof[str(rho)] = f * len(y)
    people = np.unique(subj)
    pf = np.random.default_rng(SEED + 1).permutation(len(people)) % 5
    fold = pf[np.searchsorted(people, subj)]
    grid = ([0.0] if FROZEN and FROZEN[0] == 0.40 else []) + FROZEN
    loss = {str(r): np.zeros(len(y)) for r in grid}
    for f in range(5):
        tr, te = np.where(fold != f)[0], np.where(fold == f)[0]
        prev = None
        for rho in grid:
            prev, _ = warm_fit(lambda t: -logp(t, rho, tr).mean(), MM.X0, prev, rng, 2)
            loss[str(rho)][te] = -logp(prev, rho, te)
    per_person = {r: [float(v[subj == s].mean()) for s in people] for r, v in loss.items()}
    return {"kind": "menus", "trials": int(len(y)), "participants": int(len(people)),
            "profile_total_nats": prof, "cv_loss_per_participant": per_person,
            "trials_per_participant": [int((subj == s).sum()) for s in people]}


def main(data_dir, name, out, *_):
    """NAME may carry a part, e.g. menus_gluth.p2of6: that job fits every 6th rho value from the 3rd."""
    global PROFILE, FROZEN
    np.seterr(all="ignore")
    base, part = (name.split(".p") + [None])[:2]
    if part:
        i, n_parts = (int(x) for x in part.split("of"))
        PROFILE, FROZEN = PROFILE[i::n_parts], FROZEN[i::n_parts]
    t0 = time.time()
    res = menus(data_dir, base) if base.startswith("menus_") else risky(data_dir, base)
    res.update({"name": base, "part": part, "seconds": time.time() - t0})
    json.dump(res, open(out, "w"))
    print("RESULT-BEGIN")
    print(json.dumps(res))
    print("RESULT-END", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
