#!/usr/bin/env python3
"""DEVELOPMENT, not a registered test. The five prereg-strata-v1 corpora are spent: their outcomes
have been read. This script asks which probability reader would fix GDT-S, using leave-one-corpus-out
so each corpus is scored by a model that never saw it:

    for each held-out corpus h:
        fit shared parameters jointly on CPC18 + the other four corpora (all problems),
        with a free logit scale per training set (CPC18's fixed at 1), corpora weighted equally;
        on h: refit one scale kappa on the registered calibration half, score the registered test half.

The registered splits are reproduced exactly (same seed, same order). CPT gets the same protocol, and
on h chooses its coding (money unit or stake share) on the calibration half, as registered.

    python explore_readers.py ROWS          # on Atlas; writes explore_readers.json
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "strata"))
import fit_strata as F  # noqa: E402
import readers as R  # noqa: E402
import strata_models as M  # noqa: E402

N_GRID = [2, 4, 8, 16, 32, 64, 128, 256]
MODELS = ["GDTS-lin", "GDTS-fr", "GDTS-llo", "GDTS-eff", "GDTS-lin-pow", "GDTS-llo-pow", "CPT_unit", "CPT_share"]
N_STARTS = 4
N_BOOT = 2000


def load(rows_dir):
    rng = np.random.default_rng(F.SEED)
    data = {}
    for name in F.CORPORA:
        r = F.corpus_rows(rows_dir, name)
        pr, _, n, inv = F.to_problems(r)
        y = np.load(os.path.join(rows_dir, f"{name}_outcome.npz"))["chose_B"][
            ~np.load(os.path.join(rows_dir, f"{name}_overlap_mask.npy"))].astype(float)
        k = np.bincount(inv, weights=y, minlength=len(pr)).astype(float)
        perm = rng.permutation(len(pr))
        cal = np.zeros(len(pr), bool); cal[perm[: int(len(pr) * F.CAL_FRAC)]] = True
        data[name] = {"pr": pr, "k": k, "n": n, "cal": cal, "prior": R.Prior(pr)}
    pr, k, n = F.cpc18_problems()
    data["cpc18"] = {"pr": pr, "k": k, "n": n, "cal": None, "prior": R.Prior(pr)}
    return data


def spec(model):
    """(logit(th, d, n_cap) for a dataset dict d, number of shared parameters, x0)."""
    if model.startswith("GDTS"):
        tok = model.split("-")
        reader = tok[1]
        curved = 2 if "pow2" in tok else (1 if "pow" in tok else 0)
        norm = "L1" if "L1" in tok else ("Lq" if "Lq" in tok else "L2")
        # ablations switch coordinates off: w_s (index 4), beta (5), or everything but w_g, w_l
        off = {"nos": [4], "nobeta": [5], "core": [2, 3, 4, 5]}
        dead = [i for t in tok for i in off.get(t, [])]
        fns = {}
        def logit(th, d, ncap=None):
            key = id(d["prior"])
            if key not in fns:
                fns[key] = R.make_gdts(reader, d["prior"], curved, norm)
            if dead:
                th = np.array(th, float); th[dead] = -60.0
            return fns[key](th, d["pr"], ncap)
        x0 = (list(M.X0["GDTS"]) + ([0.0, 0.0] if reader == "llo" else []) + [np.log(0.88)] * curved
              + ([np.log(1.5)] if norm == "Lq" else []))
        return logit, len(x0), x0
    coding = model.split("_")[1]
    f = M.make_cpt(coding)
    return (lambda th, d, ncap=None: f(th, d["pr"])), 5, list(M.X0[f"CPT_{coding}"])


def joint_fit(model, train, ncap=None, seed=0):
    logit, p, x0 = spec(model)
    names = list(train)
    scale_idx = {nm: i for i, nm in enumerate([nm for nm in names if nm != "cpc18"])}

    def loss(x):
        th = x[:p]
        tot = 0.0
        for nm in names:
            d = train[nm]
            s = 1.0 if nm == "cpc18" else np.exp(x[p + scale_idx[nm]])
            tot += F.nll(s * logit(th, d, ncap), d["k"], d["n"])
        return tot / len(names)

    rng = np.random.default_rng(seed)
    start = np.r_[x0, np.zeros(len(scale_idx))]
    best = None
    for i in range(N_STARTS):
        s = start if i == 0 else start + rng.normal(0, 0.5, len(start))
        r = minimize(loss, s, method="L-BFGS-B")
        if best is None or r.fun < best.fun:
            best = r
    return best.x[:p], float(best.fun)


def score(model, th, d, ncap=None):
    logit, _, _ = spec(model)
    z = logit(th, d, ncap)
    cal = d["cal"]
    kk = F.kappa(z[cal], d["k"][cal], d["n"][cal])
    cal_loss = F.nll(kk * z[cal], d["k"][cal], d["n"][cal])
    return F.per_problem_loss(kk * z[~cal], d["k"][~cal], d["n"][~cal]), cal_loss, kk


def reader_curve(model, th, d, ncap):
    c = np.array([0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
    if model.startswith("GDTS-fr"):
        w = R.w_fr(c)
    elif model.startswith("GDTS-llo"):
        w = R.w_llo(c, th[6:8])
    elif model.startswith("GDTS-eff"):
        w = d["prior"].w(c, ncap)
    else:
        w = c
    return dict(zip([str(x) for x in c], [round(float(v), 4) for v in w]))


def domain(pr):
    """gains (no negative outcome), losses (no positive outcome) or mixed, per problem."""
    X = np.c_[pr.XA, pr.XB]
    return np.where((X >= 0).all(1), "gains", np.where((X <= 0).all(1), "losses", "mixed"))


def by_domain(losses, data, models):
    out = {}
    for dom in ("gains", "losses", "mixed"):
        row = {"choices": 0.0}
        for m in models:
            num = den = 0.0
            for h in F.CORPORA:
                d = data[h]
                sel = domain(d["pr"].subset(~d["cal"])) == dom
                num += losses[(h, m)][sel].sum(); den += d["n"][~d["cal"]][sel].sum()
            row[m] = float(num / den) if den else None
            row["choices"] = den
        out[dom] = row
    return out


def main(rows_dir, models=None, tag=""):
    global MODELS
    MODELS = models or MODELS
    data = load(rows_dir)
    out = {"protocol": "leave-one-corpus-out, development only", "folds": {}}
    losses = {}
    for h in F.CORPORA:
        train = {nm: d for nm, d in data.items() if nm != h}
        fold = {"models": {}}
        for model in MODELS:
            if model == "GDTS-eff":
                fits = {n: joint_fit(model, train, n) for n in N_GRID}
                ncap = min(fits, key=lambda n: fits[n][1])
                th, tl = fits[ncap]
                extra = {"capacity_n": ncap, "train_loss_by_n": {str(n): v[1] for n, v in fits.items()}}
            else:
                ncap = None
                th, tl = joint_fit(model, train)
                extra = {}
            pl, cal_loss, kk = score(model, th, data[h], ncap)
            losses[(h, model)] = pl
            fold["models"][model] = {"train_loss": tl, "theta": [float(t) for t in th], "kappa": kk,
                                     "cal_loss": cal_loss, "test_nll": float(pl.sum() / data[h]["n"][~data[h]["cal"]].sum()),
                                     "reader_on_heldout": reader_curve(model, th, data[h], ncap), **extra}
            print(h, model, round(fold["models"][model]["test_nll"], 5), extra.get("capacity_n", ""), flush=True)
        cu, cs = fold["models"]["CPT_unit"]["cal_loss"], fold["models"]["CPT_share"]["cal_loss"]
        fold["cpt_coding"] = "CPT_unit" if cu <= cs else "CPT_share"
        losses[(h, "CPT")] = losses[(h, fold["cpt_coding"])]
        out["folds"][h] = fold

    rng = np.random.default_rng(F.SEED + 30)
    gd = [m for m in MODELS if m.startswith("GDTS")]
    comps = [(m, "CPT") for m in gd] + [(m, gd[0]) for m in gd[1:]]
    out["by_domain"] = by_domain(losses, data, gd + ["CPT"])
    out["pooled"] = {}
    for a, b in comps:
        point = np.mean([(losses[(h, a)].sum() - losses[(h, b)].sum()) / data[h]["n"][~data[h]["cal"]].sum()
                         for h in F.CORPORA])
        draws = []
        for _ in range(N_BOOT):
            v = []
            for h in F.CORPORA:
                nt = data[h]["n"][~data[h]["cal"]]
                i = rng.integers(0, len(nt), len(nt))
                v.append((losses[(h, a)][i].sum() - losses[(h, b)][i].sum()) / nt[i].sum())
            draws.append(np.mean(v))
        out["pooled"][f"{a} minus {b}"] = {"mean": float(point), "ci_low": float(np.percentile(draws, 2.5)),
                                           "ci_high": float(np.percentile(draws, 97.5))}
    json.dump(out, open(os.path.join(HERE, f"explore_readers{tag}.json"), "w"), indent=1)
    print(json.dumps({"pooled": out["pooled"], "by_domain": out["by_domain"]}, indent=1))


if __name__ == "__main__":
    ms = sys.argv[sys.argv.index("--models") + 1].split(",") if "--models" in sys.argv else None
    tg = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else ""
    main(sys.argv[1], ms, tg)
