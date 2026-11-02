#!/usr/bin/env python3
"""Power of the proposed scale-ladder study (DEVELOPMENT.md, "Power of the proposed study").

    python power_study.py DATA_DIR CELL OUT.json

CELL is <corpus>.p<rho>s<sigma>, e.g. cpc18.p0.725s0.5: the true model is CPT_CUr with rho fixed at
<rho> and the other parameters fitted to that spent corpus; each simulated person's sensitivity is
multiplied by exp(N(0, sigma)). Needs score.py, strata_models.py, explore_rho.py, explore_cu.py,
standins.json and problems_<corpus>.npz beside it. POWER_QUICK=1 for a smoke test.

Per simulated study (fresh stimuli each time):
  * 60 base pairs (20 gain, 20 loss, 20 mixed; 1-3 outcomes per option, probabilities in steps of
    0.05, outcomes 1..20 in size, no dominance), each at scales 1, 4, 16; three Latin-square lists of
    60 choices, N/3 people per list.
  * H1 alone: completeness of rho=0.725 minus rho=1, 10-fold CV by base pair, ML = gradient boosting,
    delta-method 95% interval above 0.
  * H1 pooled: the same difference averaged with three stand-in public corpora, each a spent corpus
    drawn at random and resampled at its own size (power.py's method), interval above 0.
  * H2: rho fitted freely on all data; Wald tests of rho = 1, 0.725 and 0 at the 5% level with a
    person-clustered sandwich SE. The quasi-likelihood-ratio tests (Pearson dispersion) are kept
    for comparison: they ignore that each person makes 60 choices.
    The registered H2 rejects rho = 1 and rho = 0 by the clustered interval and checks 0.725
    against a band of +-0.05 (scored in aggregate_power.py from rho_hat and se_rho_cluster).
    The band is there because the fitted rho is population-level: when people differ in
    sensitivity (sigma > 0), pooling flattens the high-stakes problems most and the pooled rho
    sits about 0.03 above every individual's (0.757 for 0.725 at sigma = 0.5). The frozen 0.725
    was itself fitted to pooled choice rates, so it is the same kind of number.
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explore_cu as C  # noqa: E402
import explore_rho as E  # noqa: E402
import score as S  # noqa: E402
import strata_models as M  # noqa: E402

NS = [60, 120, 180, 240]
SIMS = 60
SCALES = [1, 4, 16]
RHO_TEST = 0.725
SEED = 20261108
if os.environ.get("POWER_QUICK"):
    NS, SIMS = [120], 2


def diff_ci(d, g):
    n = len(d)
    est = d.sum() / g.sum()
    z = (d - est * g) / g.mean()
    se = z.std(ddof=1) / np.sqrt(n)
    return est, se


# ---------------------------------------------------------------- stimuli
def option(rng, domain, n_out):
    if n_out == 1:
        p = np.array([1.0])
    else:
        cuts = np.sort(rng.choice(np.arange(1, 20), n_out - 1, replace=False))
        p = np.diff(np.r_[0, cuts, 20]) / 20
    mag = rng.choice(np.arange(1, 21), n_out, replace=False).astype(float)
    if domain == "gain":
        x = mag
    elif domain == "loss":
        x = -mag
    else:
        sign = rng.permutation(np.r_[1, -1, rng.choice([1, -1], n_out - 2)]) if n_out >= 2 else np.array([1])
        x = mag * sign
    return x, p


def base_pairs(rng):
    out = []
    for domain in ["gain"] * 20 + ["loss"] * 20 + ["mixed"] * 20:
        while True:
            lo = 2 if domain == "mixed" else 1
            na, nb = rng.integers(lo, 4), rng.integers(lo, 4)
            if na == 1 and nb == 1:
                continue
            xa, pa = option(rng, domain, na)
            xb, pb = option(rng, domain, nb)
            pad = lambda x, p: (np.r_[x, np.zeros(3 - len(x))], np.r_[p, np.zeros(3 - len(p))])  # noqa: E731
            xa, pa = pad(xa, pa)
            xb, pb = pad(xb, pb)
            if S.dominates(xa, pa, xb, pb) or S.dominates(xb, pb, xa, pa):
                continue
            out.append((xa, pa, xb, pb))
            break
    return out


def study(rng):
    bp = base_pairs(rng)
    XA, PA, XB, PB, base, scale = [], [], [], [], [], []
    for j, (xa, pa, xb, pb) in enumerate(bp):
        for s, k in enumerate(SCALES):
            XA.append(xa * k); PA.append(pa); XB.append(xb * k); PB.append(pb); base.append(j); scale.append(s)
    pr = M.Problems(np.array(XA), np.array(PA), np.array(XB), np.array(PB))
    return pr, np.array(base), np.array(scale)


# ---------------------------------------------------------------- one simulated study
def simulate(rng, pr, base, scale, truth, rho, sigma, n_people):
    """Choice counts per problem, and the trials as (person, problem, chose B)."""
    z_true = C.cu_logit(truth, rho, pr)
    k, n = np.zeros(len(pr)), np.zeros(len(pr))
    trials = []
    for person in range(n_people):
        lst = person % 3
        shown = scale == (base + lst) % 3              # each base pair once, at the list's scale
        m = np.exp(sigma * rng.normal())
        y = rng.random(shown.sum()) < S.sig(m * z_true[shown])
        k[shown] += y
        n[shown] += 1
        trials.append(np.c_[np.full(shown.sum(), person), np.where(shown)[0], y])
    return k, n, np.vstack(trials).astype(int)


def rho_cluster_se(th, pr, trials):
    """Sandwich SE of rho in CPT_CUr at th, clustered by person: Fisher information as the bread,
    per-person score sums as the meat."""
    h, npar = 1e-5, len(th)
    J = np.zeros((len(pr), npar))                      # d logit / d theta, per problem
    for i in range(npar):
        dp = np.zeros(npar); dp[i] = h
        J[:, i] = (C.cpt_cur(th + dp, pr) - C.cpt_cur(th - dp, pr)) / (2 * h)
    p = S.sig(C.cpt_cur(th, pr))
    person, prob, y = trials[:, 0], trials[:, 1], trials[:, 2]
    s_trial = (y - p[prob])[:, None] * J[prob]
    meat = np.zeros((npar, npar))
    for q in np.unique(person):
        s = s_trial[person == q].sum(0)
        meat += np.outer(s, s)
    w = np.bincount(prob, minlength=len(pr)) * p * (1 - p)
    bread = np.linalg.pinv((J * w[:, None]).T @ J)
    V = bread @ meat @ bread
    return float(np.sqrt(max(V[5, 5], 0)))


def fit_fixed(rho, pr, k, n, x0, rng):
    fn = C.cpt_cu_fixed(rho)
    th = S.fit(lambda t: S.nll(fn(t, pr), k, n), x0, 3, rng)
    return th, S.nll(fn(th, pr), k, n) * n.sum()


def analyse(pr, base, k, n, trials, truth, rng):
    from sklearn.ensemble import GradientBoostingRegressor
    fold = np.random.default_rng(S.FOLD_SEED).permutation(base.max() + 1)[base] % 10
    pred = {RHO_TEST: np.zeros(len(pr)), 1.0: np.zeros(len(pr))}
    naive, ml = np.zeros(len(pr)), np.zeros(len(pr))
    feats = S.features(pr)
    for f in range(10):
        tr, te = fold != f, fold == f
        ptr, pte = pr.subset(tr), pr.subset(te)
        naive[te] = k[tr].sum() / n[tr].sum()
        for rho in pred:
            th, _ = fit_fixed(rho, ptr, k[tr], n[tr], truth, rng)
            pred[rho][te] = S.sig(C.cu_logit(th, rho, pte))
        ml[te] = np.clip(GradientBoostingRegressor(n_estimators=300, max_depth=2, learning_rate=0.05, subsample=0.8,
                                                   random_state=f).fit(feats[tr], k[tr] / n[tr], sample_weight=n[tr])
                         .predict(feats[te]), 1e-4, 1 - 1e-4)
    d = S.err_rate(pred[1.0], k, n) - S.err_rate(pred[RHO_TEST], k, n)
    g = S.err_rate(naive, k, n) - S.err_rate(ml, k, n)
    est, se = diff_ci(d, g)
    # H2: rho free, quasi-LR against fixed values
    fixed = {r: fit_fixed(r, pr, k, n, truth, rng) for r in (0.0, RHO_TEST, 1.0)}
    best = min(fixed, key=lambda r: fixed[r][1])
    th_free = S.fit(lambda t: S.nll(C.cpt_cur(t, pr), k, n), np.r_[fixed[best][0], best], 3, rng)
    nll_free = min(S.nll(C.cpt_cur(th_free, pr), k, n) * n.sum(), fixed[best][1])
    p = S.sig(C.cpt_cur(th_free, pr))
    phi = max(float((((k - n * p) ** 2) / (n * p * (1 - p))).sum() / (len(pr) - 6)), 1.0)
    lr = {str(r): float(2 * (fixed[r][1] - nll_free) / phi) for r in fixed}
    se_rho = rho_cluster_se(th_free, pr, trials)
    wald = {str(r): bool(abs(th_free[5] - r) > 1.96 * se_rho) for r in fixed}
    return {"h1_est": float(est), "h1_se": float(se), "rho_hat": float(th_free[5]), "phi": phi, "lr": lr,
            "se_rho_cluster": se_rho, "reject_cluster": wald}


def pooled_pass(est, se, standins, rng):
    names = list(standins)
    es, vs = [est], [se ** 2]
    for c in rng.choice(names, 3):
        d, g = (np.array(standins[c][x]) for x in ("d", "g"))
        idx = rng.integers(0, len(d), len(d))
        e, s = diff_ci(d[idx], g[idx])
        es.append(e); vs.append(s ** 2)
    pe, pse = np.mean(es), np.sqrt(np.sum(vs)) / len(es)
    return bool(pe - 1.96 * pse > 0)


def main(data_dir, cell, out, *_):
    np.seterr(all="ignore")
    corpus, spec = cell.split(".p")
    rho, sigma = (float(x) for x in spec.split("s"))
    z = np.load(os.path.join(data_dir, f"problems_{corpus}.npz"))
    spent = M.Problems(z["XA"], z["PA"], z["XB"], z["PB"], unit=float(z["unit"]))
    truth = E.fit_nll(C.cpt_cu_fixed(rho), E.CPT0, spent, z["k"], z["n"], 5, SEED)
    standins = json.load(open(os.path.join(data_dir, "standins.json")))
    t0 = time.time()
    res = {"cell": cell, "corpus": corpus, "rho_true": rho, "sigma": sigma, "truth": truth.tolist(),
           "alpha": float(np.exp(truth[0])), "beta": float(np.exp(truth[1])), "sims": {}}
    for N in NS:
        rows = []
        for sim in range(SIMS):
            rng = np.random.default_rng([SEED, N, sim, int(1000 * rho), int(100 * sigma)])
            pr, base, scale = study(rng)
            k, n, trials = simulate(rng, pr, base, scale, truth, rho, sigma, N)
            r = analyse(pr, base, k, n, trials, truth, rng)
            r["h1_pooled_pass"] = pooled_pass(r["h1_est"], r["h1_se"], standins, rng)
            rows.append(r)
        res["sims"][str(N)] = rows
        print(N, f"{time.time() - t0:.0f}s", flush=True)
    res["seconds"] = time.time() - t0
    json.dump(res, open(out, "w"))
    print("RESULT-BEGIN")
    print(json.dumps({k: v for k, v in res.items() if k != "sims"}))
    print("RESULT-END", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
