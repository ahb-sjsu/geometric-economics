#!/usr/bin/env python3
"""prereg-strata-v1: freeze on CPC18, check identification, transfer to the test corpora, grade inputs.

    python fit_strata.py freeze                 # fit every model on CPC18 -> frozen_strata.json
    python fit_strata.py recover                # V4: can GDT-C's budget be recovered on CPC18?
    python fit_strata.py run ROWS               # the registered run (opens the outcome files)
    python fit_strata.py run ROWS --simulate T  # rehearsal, T in {GDTC, GDTS, GDT2, CPT_unit}

Every corpus is reduced to problems: identical rows pooled into (choices of B, choices). All
losses are binomial log-loss per choice in nats. The bootstrap resamples problems within each
corpus; pooled numbers weight corpora equally.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "datasets"))
import strata_models as M  # noqa: E402

SEED = 20261101
CAL_FRAC = 0.5
MARGIN_FRAC = 0.01
N_BOOT = 2000
N_STARTS = 5
CONV_TOL = 1e-6
H7_MIN_SHIFT = 0.05          # a predicted gamma shift counts only if larger than this
H7_MIN_CORPORA = 3
V4_FACTOR = 2.0
V5_MIN_DP = 0.005            # H6 needs GDT-C and GDT-S to predict differently on the test stimuli
CORPORA = ["gp2012", "pachur2017", "pachur2018", "zilker2020", "babula2018"]
FROZEN = os.path.join(HERE, "frozen_strata.json")
GRADED = ["EV", "RUM", "GDT2", "GDTS", "GDTC", "CPT_unit", "CPT_share"]


# ---------------------------------------------------------------- data
def cpc18_problems():
    raw = pd.read_csv(os.path.join(HERE, "..", "..", "datasets", "raw", "cpc18_raw.csv"),
                      usecols=["GameID", "Ha", "pHa", "La", "Hb", "pHb", "Lb", "Amb", "Trial", "B"])
    d = raw[(raw["Trial"] == 1) & (raw["Amb"] == 0)]
    g = d.groupby("GameID").agg(k=("B", "sum"), n=("B", "size"))
    f = d.groupby("GameID").first().loc[g.index]
    XA = np.c_[f["Ha"], f["La"]]; PA = np.c_[f["pHa"], 1 - f["pHa"]]
    XB = np.c_[f["Hb"], f["Lb"]]; PB = np.c_[f["pHb"], 1 - f["pHb"]]
    return M.Problems(XA, PA, XB, PB), g["k"].to_numpy(float), g["n"].to_numpy(float)


def corpus_rows(rows_dir, name):
    c = np.load(os.path.join(rows_dir, f"{name}_covariates.npz"))
    keep = ~np.load(os.path.join(rows_dir, f"{name}_overlap_mask.npy"))
    return {k: c[k][keep] for k in ("XA", "PA", "XB", "PB", "participant")}


def to_problems(r, y=None):
    """Pool identical rows. Returns Problems, k (B choices), n, and the row -> problem index."""
    key = np.round(np.c_[r["XA"], r["PA"], r["XB"], r["PB"]], 6)
    u, first, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
    inv = inv.ravel()
    n = np.bincount(inv).astype(float)
    k = np.bincount(inv, weights=y).astype(float) if y is not None else None
    pr = M.Problems(r["XA"][first], r["PA"][first], r["XB"][first], r["PB"][first])
    return pr, k, n, inv


# ---------------------------------------------------------------- fitting
def nll(z, k, n):
    """Mean binomial log-loss per choice for logits z."""
    lp = -np.logaddexp(0, -z); lq = -np.logaddexp(0, z)
    return float(-(k * lp + (n - k) * lq).sum() / n.sum())


def fit(fn, x0, pr, k, n, rng):
    best = None
    starts = [np.array(x0, float)] + [np.array(x0, float) + rng.normal(0, 0.7, len(x0)) for _ in range(N_STARTS - 1)]
    for s in starts:
        r = minimize(lambda th: nll(fn(th, pr), k, n), s, method="L-BFGS-B")
        if best is None or r.fun < best.fun:
            best = r
    a = best.fun
    r2 = minimize(lambda th: nll(fn(th, pr), k, n), best.x, method="L-BFGS-B")
    th = r2.x if r2.fun <= a else best.x
    return [float(t) for t in th], abs(a - min(a, r2.fun)) / max(a, 1e-12) <= CONV_TOL, float(min(a, r2.fun))


def models(env):
    return {"EV": M.logit_ev, "RUM": M.logit_rum, "GDT2": M.logit_gdt2, "GDTS": M.logit_gdts,
            "GDTC": M.make_gdtc(env), "CPT_unit": M.make_cpt("unit"), "CPT_share": M.make_cpt("share")}


def freeze():
    pr, k, n = cpc18_problems()
    env = M.Environment(pr)
    rng = np.random.default_rng(SEED)
    out = {"source": "CPC18 description choices (Trial 1), games without ambiguity",
           "n_games": len(pr), "n_choices": float(n.sum()), "unit": pr.unit, "models": {}}
    for name, fn in models(env).items():
        th, ok, loss = fit(fn, M.X0[name], pr, k, n, rng)
        out["models"][name] = {"theta": th, "converged": bool(ok), "in_sample_nll": loss}
        print(name, round(loss, 5), ok, flush=True)
    json.dump(out, open(FROZEN, "w"), indent=1)


def gdtc_summary(th):
    w = np.exp(th[:5])
    s_mag, s_prob = M.allocate(np.exp(th[6]), w[0] + w[1], w[2] + w[3])
    return {"budget_bits": float(np.exp(th[6])), "sigma_mag": float(s_mag), "sigma_prob": float(s_prob)}


def recover():
    """V4. Simulate frozen GDT-C on CPC18 stimuli with CPC18's counts, refit, compare."""
    fr = json.load(open(FROZEN))["models"]["GDTC"]["theta"]
    pr, _, n = cpc18_problems()
    env = M.Environment(pr)
    fn = M.make_gdtc(env)
    p = 1 / (1 + np.exp(-fn(fr, pr)))
    out = {"truth": gdtc_summary(fr), "refits": []}
    for rep in range(3):
        k = np.random.default_rng(SEED + 10 + rep).binomial(n.astype(int), p).astype(float)
        th, ok, _ = fit(fn, M.X0["GDTC"], pr, k, n, np.random.default_rng(SEED + 20 + rep))
        out["refits"].append({**gdtc_summary(th), "converged": bool(ok)})
    t = out["truth"]
    order = np.sign(t["sigma_mag"] - t["sigma_prob"])
    ok = all(abs(np.log(r["budget_bits"] / t["budget_bits"])) <= np.log(V4_FACTOR)
             and np.sign(r["sigma_mag"] - r["sigma_prob"]) == order for r in out["refits"])
    out["V4_void"] = not ok
    json.dump(out, open(os.path.join(HERE, "recovery_v4.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


# ---------------------------------------------------------------- transfer
def kappa(z, k, n):
    r = minimize_scalar(lambda lk: nll(10 ** lk * z, k, n), bounds=(-4, 4), method="bounded")
    return float(10 ** r.x)


def per_problem_loss(z, k, n):
    lp = -np.logaddexp(0, -z); lq = -np.logaddexp(0, z)
    return -(k * lp + (n - k) * lq)


def cpt_gamma(th):
    return float(0.28 + 1.72 / (1 + np.exp(-th[3])))


def run(rows_dir, simulate=None):
    frozen = json.load(open(FROZEN))
    th0 = {m: frozen["models"][m]["theta"] for m in GRADED}
    rng = np.random.default_rng(SEED)
    cpc, _, _ = cpc18_problems()
    cpc_env = M.Environment(cpc)
    res = {"prereg": "prereg-strata-v1", "simulation": simulate, "corpora": {}}
    for name in CORPORA:
        r = corpus_rows(rows_dir, name)
        pr_all, _, n_all, inv = to_problems(r)
        env = M.Environment(pr_all)
        fns = models(env)
        if simulate:
            p_true = 1 / (1 + np.exp(-fns[simulate](th0[simulate], pr_all)))
            y = (np.random.default_rng(SEED + 1).random(len(inv)) < p_true[inv]).astype(float)
        else:
            y = np.load(os.path.join(rows_dir, f"{name}_outcome.npz"))["chose_B"][
                ~np.load(os.path.join(rows_dir, f"{name}_overlap_mask.npy"))].astype(float)
        k_all = np.bincount(inv, weights=y, minlength=len(pr_all)).astype(float)
        perm = rng.permutation(len(pr_all))
        cal = np.zeros(len(pr_all), bool); cal[perm[: int(len(pr_all) * CAL_FRAC)]] = True
        pc, pt = pr_all.subset(cal), pr_all.subset(~cal)
        kc, nc, kt, nt = k_all[cal], n_all[cal], k_all[~cal], n_all[~cal]
        out = {"rows": int(len(inv)), "problems": int(len(pr_all)), "participants": int(len(set(r["participant"]))),
               "cal_problems": int(cal.sum()), "test_problems": int((~cal).sum()), "kappa": {}, "test_nll": {}}
        loss = {}
        base = kc.sum() / nc.sum()
        z0 = np.full(int((~cal).sum()), np.log(base / (1 - base)))
        loss["M0"] = per_problem_loss(z0, kt, nt)
        cal_m0 = nll(np.full(int(cal.sum()), np.log(base / (1 - base))), kc, nc)
        cal_loss = {}
        for m in GRADED:
            zc, zt = fns[m](th0[m], pc), fns[m](th0[m], pt)
            kk = kappa(zc, kc, nc)
            out["kappa"][m] = kk
            cal_loss[m] = nll(kk * zc, kc, nc)
            loss[m] = per_problem_loss(kk * zt, kt, nt)
        out["cpt_coding"] = "CPT_unit" if cal_loss["CPT_unit"] <= cal_loss["CPT_share"] else "CPT_share"
        loss["CPT"] = loss[out["cpt_coding"]]
        out["margin"] = MARGIN_FRAC * (cal_m0 - cal_loss["EV"])
        out["test_nll"] = {m: float(v.sum() / nt.sum()) for m, v in loss.items()}
        # H7: observed gamma = CPT (share coding) refit natively on the calibration half
        th_n, ok_n, _ = fit(fns["CPT_share"], th0["CPT_share"], pc, kc, nc, np.random.default_rng(SEED + 5))
        p_gdtc = 1 / (1 + np.exp(-fns["GDTC"](th0["GDTC"], pr_all)))
        th_p, ok_p, _ = fit(fns["CPT_share"], th0["CPT_share"], pr_all, p_gdtc, np.ones(len(pr_all)),
                            np.random.default_rng(SEED + 6))
        out["gamma"] = {"observed": cpt_gamma(th_n), "observed_converged": bool(ok_n),
                        "predicted": cpt_gamma(th_p), "predicted_converged": bool(ok_p)}
        pS = 1 / (1 + np.exp(-fns["GDTS"](th0["GDTS"], pr_all)))
        out["consumer_vs_stratified_mean_abs_dp"] = float(np.mean(np.abs(p_gdtc - pS)))
        out["stake_groups"] = stake_groups(pr_all, k_all, n_all, out["kappa"]["GDT2"] * fns["GDT2"](th0["GDT2"], pr_all))
        out["_loss"] = {m: v.tolist() for m, v in loss.items()}
        out["_n"] = nt.tolist()
        res["corpora"][name] = out
        print(name, json.dumps(out["test_nll"]), flush=True)

    # CPC18 references for H7
    cpt = M.make_cpt("share")
    p_cpc = 1 / (1 + np.exp(-M.make_gdtc(cpc_env)(th0["GDTC"], cpc)))
    th_cp, _, _ = fit(cpt, th0["CPT_share"], cpc, p_cpc, np.ones(len(cpc)), np.random.default_rng(SEED + 7))
    res["gamma_cpc18"] = {"observed": cpt_gamma(th0["CPT_share"]), "predicted": cpt_gamma(th_cp)}
    res["pooled"] = pooled(res)
    res["stake_invariance"] = h4(res)
    res["effects"] = effects(th0, cpc_env, frozen["unit"])
    for c in res["corpora"].values():
        c.pop("_loss"); c.pop("_n")
    tag = f"sim_{simulate}" if simulate else "real"
    json.dump(res, open(os.path.join(HERE, f"results_strata_{tag}.json"), "w"), indent=1)
    print("WROTE", tag)


def stake_groups(pr, k, n, z2):
    """Problems identical in share coding but at different stakes: lowest vs highest stake."""
    S = pr.stake[:, None]
    key = np.round(np.c_[pr.XA / S, pr.PA, pr.XB / S, pr.PB], 4)
    u, inv = np.unique(key, axis=0, return_inverse=True)
    inv = inv.ravel()
    out = []
    p2 = 1 / (1 + np.exp(-z2))
    for g in range(len(u)):
        idx = np.where(inv == g)[0]
        if len(np.unique(np.round(pr.stake[idx], 4))) < 2:
            continue
        lo, hi = idx[np.argmin(pr.stake[idx])], idx[np.argmax(pr.stake[idx])]
        out.append({"pred_shift_gdt2": float(p2[hi] - p2[lo]), "obs_hi": [float(k[hi]), float(n[hi])],
                    "obs_lo": [float(k[lo]), float(n[lo])]})
    return out


H4_MIN_GROUPS = 5


def h4(res):
    """Per group: |predicted GDT-2 shift| minus the observed shift in GDT-2's direction. Positive
    means people moved less with stake than GDT-2 predicts. Bootstrap over groups and choices."""
    G = [g for c in res["corpora"].values() for g in c["stake_groups"]]
    if len(G) < H4_MIN_GROUPS:
        return {"groups": len(G), "assessable": False}
    rng = np.random.default_rng(SEED + 4)
    def stat(gs, draw):
        v = []
        for g in gs:
            (kh, nh), (kl, nl) = g["obs_hi"], g["obs_lo"]
            rh = rng.binomial(int(nh), kh / nh) / nh if draw else kh / nh
            rl = rng.binomial(int(nl), kl / nl) / nl if draw else kl / nl
            d = g["pred_shift_gdt2"]
            v.append(abs(d) - np.sign(d) * (rh - rl))
        return float(np.mean(v))
    boots = [stat([G[i] for i in rng.integers(0, len(G), len(G))], True) for _ in range(N_BOOT)]
    return {"groups": len(G), "assessable": True, "mean": stat(G, False),
            "ci_low": float(np.percentile(boots, 2.5)), "ci_high": float(np.percentile(boots, 97.5))}


def selfcheck():
    """On gains-only two-branch CPC18 problems, GDT2 and CPT match fit_transfer exactly."""
    import fit_transfer as ft
    import cpc18
    pr, _, _ = cpc18_problems()
    gains = (pr.XA.min(1) >= 0) & (pr.XB.min(1) >= 0)
    q = pr.subset(gains)
    q.unit = 1.0
    d = pd.DataFrame({"evA": M.ev(q.XA, q.PA), "evB": M.ev(q.XB, q.PB), "sdA": M.sd(q.XA, q.PA),
                      "sdB": M.sd(q.XB, q.PB), "amb": 0.0, "_Ha": q.XA[:, 0], "_pHa": q.PA[:, 0],
                      "_La": q.XA[:, 1], "_Hb": q.XB[:, 0], "_pHb": q.PB[:, 0], "_Lb": q.XB[:, 1]})
    s_ev, s_sd, T = 2.0, 5.0, 1.5
    zg = np.log(ft.pred_geom([s_ev, s_sd, 1.0, T], d)) - np.log1p(-ft.pred_geom([s_ev, s_sd, 1.0, T], d))
    mine = M.logit_gdt2([np.log(1 / (s_ev * T)), np.log(1 / (s_sd * T))], q)
    a, b, lam, g, T2 = 0.8, 0.9, 2.0, 0.7, 3.0
    zc = np.log(ft.pred_cpt([a, b, lam, g, T2], d)) - np.log1p(-ft.pred_cpt([a, b, lam, g, T2], d))
    gi = np.log((g - 0.28) / 1.72 / (1 - (g - 0.28) / 1.72))
    mc = M.make_cpt("unit")([np.log(a), np.log(b), np.log(lam), gi, np.log(1 / T2)], q)
    out = {"gains_only_problems": int(gains.sum()), "gdt2_max_abs_diff": float(np.abs(zg - mine).max()),
           "cpt_max_abs_diff": float(np.abs(zc - mc).max())}
    print(json.dumps(out))
    # fit_transfer adds 1e-6 to every parameter, which moves its logits by about 1e-5
    assert out["gdt2_max_abs_diff"] < 1e-4 and out["cpt_max_abs_diff"] < 1e-4, out


def pooled(res):
    rng = np.random.default_rng(SEED + 3)
    C = list(res["corpora"].values())
    pairs = {"GDTS-GDT2": ("GDTS", "GDT2"), "GDTS-CPT": ("GDTS", "CPT"), "GDTC-GDTS": ("GDTC", "GDTS"),
             "CPT-GDT2": ("CPT", "GDT2"), "GDTC-CPT": ("GDTC", "CPT"), "GDT2-EV": ("GDT2", "EV")}
    L = [{m: np.array(v) for m, v in c["_loss"].items()} for c in C]
    N = [np.array(c["_n"]) for c in C]
    margin = float(np.mean([c["margin"] for c in C]))
    draws = {p: [] for p in pairs}
    ratio = []
    for _ in range(N_BOOT):
        per = {p: [] for p in pairs}
        r_num, r_den = [], []
        for l, n in zip(L, N):
            i = rng.integers(0, len(n), len(n))
            tot = n[i].sum()
            mean = {m: l[m][i].sum() / tot for m in ("GDT2", "GDTS", "GDTC", "CPT", "EV")}
            for p, (a, b) in pairs.items():
                per[p].append(mean[a] - mean[b])
            r_num.append(mean["GDT2"] - mean["GDTS"]); r_den.append(mean["GDT2"] - mean["CPT"])
        for p in pairs:
            draws[p].append(np.mean(per[p]))
        ratio.append(np.mean(r_num) / np.mean(r_den) if np.mean(r_den) != 0 else np.nan)
    out = {"margin": margin}
    for p, (a, b) in pairs.items():
        point = float(np.mean([l[a].sum() / n.sum() - l[b].sum() / n.sum() for l, n in zip(L, N)]))
        out[p] = {"mean": point, "ci_low": float(np.percentile(draws[p], 2.5)),
                  "ci_high": float(np.percentile(draws[p], 97.5))}
        per_c = []
        for l, n, c in zip(L, N, C):
            dd = []
            for _ in range(500):
                i = rng.integers(0, len(n), len(n))
                dd.append((l[a][i].sum() - l[b][i].sum()) / n[i].sum())
            per_c.append(bool(np.percentile(dd, 97.5) < -c["margin"]))
        out[p]["corpora_won"] = int(sum(per_c))
    num = np.mean([l["GDT2"].sum() / n.sum() - l["GDTS"].sum() / n.sum() for l, n in zip(L, N)])
    den = np.mean([l["GDT2"].sum() / n.sum() - l["CPT"].sum() / n.sum() for l, n in zip(L, N)])
    out["gap_closed"] = {"point": float(num / den) if den != 0 else None,
                         "ci_low": float(np.nanpercentile(ratio, 2.5)), "ci_high": float(np.nanpercentile(ratio, 97.5))}
    return out


# ---------------------------------------------------------------- Section 7 effects
def L(*branches):
    X = [b[0] for b in branches]; P = [b[1] for b in branches]
    return X, P


EFFECTS = {
    # name: list of (option A, option B, documented side: "A" means A preferred)
    "reflection": [(L((3000, 1.0)), L((4000, 0.8), (0, 0.2)), "A"),
                   (L((-3000, 1.0)), L((-4000, 0.8), (0, 0.2)), "B")],
    "common_ratio": [(L((3000, 1.0)), L((4000, 0.8), (0, 0.2)), "A"),
                     (L((3000, 0.25), (0, 0.75)), L((4000, 0.2), (0, 0.8)), "B")],
    "loss_aversion": [(L((0, 1.0)), L((x, 0.5), (-x, 0.5)), "A") for x in (10, 100, 1000)],
    "possibility_gains": [(L((5, 1.0)), L((5000, 0.001), (0, 0.999)), "B")],
    "insurance_losses": [(L((-5, 1.0)), L((-5000, 0.001), (0, 0.999)), "A")],
    "stake_invariance": [(L((3000 * s, 1.0)), L((4000 * s, 0.8), (0, 0.2)), "A") for s in (0.01, 1, 100)],
}


def effect_problems(items):
    def arr(opts):
        k = 2
        X = np.zeros((len(opts), k)); P = np.zeros((len(opts), k))
        for i, (x, p) in enumerate(opts):
            X[i, :len(x)] = x; P[i, :len(p)] = p
        return X, P
    XA, PA = arr([a for a, _, _ in items]); XB, PB = arr([b for _, b, _ in items])
    return XA, PA, XB, PB


def effects(th0, cpc_env, unit):
    out = {}
    fns = models(cpc_env)
    for m in ("GDT2", "GDTS", "GDTC", "CPT_unit"):
        hits = {}
        for e, items in EFFECTS.items():
            XA, PA, XB, PB = effect_problems(items)
            pr = M.Problems(XA, PA, XB, PB, unit=unit)
            z = fns[m](th0[m], pr)
            if e == "stake_invariance":          # same side at every stake, whichever side it is
                ok = bool(np.all(z < 0) or np.all(z > 0))
            else:
                ok = all((zi < 0) == (side == "A") for zi, (_, _, side) in zip(z, items))
            hits[e] = {"reproduced": bool(ok), "p_B": [float(1 / (1 + np.exp(-zi))) for zi in z]}
        out[m] = hits
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "selfcheck":
        selfcheck()
    elif cmd == "freeze":
        freeze()
    elif cmd == "recover":
        recover()
    elif cmd == "run":
        sim = sys.argv[sys.argv.index("--simulate") + 1] if "--simulate" in sys.argv else None
        run(sys.argv[2], sim)
