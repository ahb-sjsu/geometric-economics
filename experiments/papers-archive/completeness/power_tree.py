#!/usr/bin/env python3
"""Power of the proposed study's tree section (DEVELOPMENT.md, "Power of the proposed study").

    python power_tree.py DATA_DIR CELL OUT.json

CELL as in power_study.py (<corpus>.p<rho>s<sigma>): simulated people follow CPT_CUr with rho fixed
at <rho> and the other parameters fitted to that spent corpus, with sensitivity multiplied by
exp(N(0, sigma)) per person. Needs power_study.py and its dependencies beside it.

The tree: six families, interleaved (gain: 50% of 20k points or 0, against a sure c; loss: the
mirror), k = 1, 4, 16, each an 8-trial Psi staircase (Kontsevich and Tyler 1999) on a logistic in
c/k. The unit coding is the ladder's, from a ladder drawn alongside.

Analysis per domain d (gain, loss): P(lottery) = sig(s_d k^e_d (|c/k|^a_d - A_d)) (sign flipped for
losses), which is exact under CPT_CUr: e_d = curvature x (1 - rho). Fitted by maximum likelihood on
all trials, covariance clustered by person. Tests at the 5% level:
  * Wilcox: mean e = (e_gain + e_loss)/2 differs from 0.
  * rho: rho_d = 1 - e_d / a_d, averaged; interval against 1, 0.725 and 0.
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explore_cu as C  # noqa: E402
import explore_rho as E  # noqa: E402
import power_study as P  # noqa: E402
import score as S  # noqa: E402
import strata_models as M  # noqa: E402

NS = [60, 120, 180, 240]
SIMS = 60
SCALES = [1, 4, 16]
TRIALS = 8
SEED = 20261109
T_GRID = np.arange(1.0, 19.01, 0.5)                    # indifference point, in c/k
S_GRID = np.exp(np.linspace(np.log(0.1), np.log(10), 25))
C_GRID = np.arange(0.5, 19.51, 0.5)                    # sure amounts offered, in c/k
if os.environ.get("POWER_QUICK"):
    NS, SIMS = [120], 2


def problems(c, k, sign, unit):
    """Sure c (A) against the 50/50 lottery of sign*20k or 0 (B), as Problems."""
    n = len(c)
    XA = np.c_[c, np.zeros(n), np.zeros(n)]
    PA = np.c_[np.ones(n), np.zeros(n), np.zeros(n)]
    XB = np.c_[sign * 20.0 * k, np.zeros(n), np.zeros(n)]
    PB = np.c_[np.full(n, 0.5), np.full(n, 0.5), np.zeros(n)]
    return M.Problems(XA, PA, XB, PB, unit=unit)


class Psi:
    """Psi method on P(lottery) = sig(s (t - x)), x = |c|/k, posterior over (t, s) grids."""

    def __init__(self):
        self.logpost = np.zeros((len(T_GRID), len(S_GRID)))
        self.p = S.sig(S_GRID[None, :, None] * (T_GRID[:, None, None] - C_GRID[None, None, :]))  # t, s, x

    def next_x(self):
        post = np.exp(self.logpost - self.logpost.max()); post /= post.sum()
        p1 = (post[:, :, None] * self.p).sum((0, 1))                     # P(lottery) per x
        best, arg = np.inf, 0
        for j in range(len(C_GRID)):
            h = 0.0
            for y, py in ((1, p1[j]), (0, 1 - p1[j])):
                q = post * (self.p[:, :, j] if y else 1 - self.p[:, :, j]); q = q / max(q.sum(), 1e-300)
                h += py * -(q[q > 0] * np.log(q[q > 0])).sum()
            if h < best:
                best, arg = h, j
        return arg

    def update(self, j, y):
        self.logpost += np.log(np.clip(self.p[:, :, j] if y else 1 - self.p[:, :, j], 1e-300, 1))


def run_people(rng, truth, rho, sigma, n_people, unit):
    rows = []                                              # person, domain(0 gain/1 loss), k, x, y
    for person in range(n_people):
        m = np.exp(sigma * rng.normal())
        fams = [(d, k) for d in (0, 1) for k in SCALES]
        psi = {f: Psi() for f in fams}
        order = rng.permutation(np.repeat(np.arange(len(fams)), TRIALS))
        for i in order:
            d, k = fams[i]
            j = psi[(d, k)].next_x()
            sign = 1.0 if d == 0 else -1.0
            pr = problems(np.array([sign * C_GRID[j] * k]), k, sign, unit)
            y = int(rng.random() < S.sig(m * C.cu_logit(truth, rho, pr)[0]))
            psi[(d, k)].update(j, y)
            rows.append((person, d, k, C_GRID[j], y))
    return np.array(rows, float)


def loglik_trials(th, k, x, y, sign):
    s, e, a, A = np.exp(th[0]), th[1], np.exp(th[2]), th[3]
    # gains: lottery preferred when the sure amount is small, z = s k^e (A - x^a)
    # losses: lottery preferred when the sure loss is large, z = s k^e (x^a - A)
    z = -sign * s * k ** e * (x ** a - A)
    return y * -np.logaddexp(0, -z) + (1 - y) * -np.logaddexp(0, z)


def fit_domain(rows, d, rng):
    r = rows[rows[:, 1] == d]
    person, k, x, y = r[:, 0].astype(int), r[:, 2], r[:, 3], r[:, 4]
    sign = 1.0 if d == 0 else -1.0
    f = lambda th: -loglik_trials(th, k, x, y, sign).sum()  # noqa: E731
    th = S.fit(f, [0.0, 0.2, np.log(0.8), 5.0], 4, rng)
    # cluster-robust covariance: per-person scores by central differences
    h, npar = 1e-4, len(th)
    grads = np.zeros((len(r), npar))
    for i in range(npar):
        dp = np.zeros(npar); dp[i] = h
        grads[:, i] = (loglik_trials(th + dp, k, x, y, sign) - loglik_trials(th - dp, k, x, y, sign)) / (2 * h)
    people = np.unique(person)
    score = np.array([grads[person == p].sum(0) for p in people])
    H = np.zeros((npar, npar))
    for i in range(npar):
        dp = np.zeros(npar); dp[i] = h
        gp = np.array([(loglik_trials(th + dp + dq, k, x, y, sign).sum() - loglik_trials(th + dp - dq, k, x, y, sign).sum())
                       / (2 * h) for dq in np.eye(npar) * h])
        gm = np.array([(loglik_trials(th - dp + dq, k, x, y, sign).sum() - loglik_trials(th - dp - dq, k, x, y, sign).sum())
                       / (2 * h) for dq in np.eye(npar) * h])
        H[i] = (gp - gm) / (2 * h)
    Hinv = np.linalg.pinv(-H)
    V = Hinv @ (score.T @ score) @ Hinv
    return th, V


def analyse(rows, rng):
    out, es, ves, rhos, grads = {}, [], [], [], []
    Vs = []
    for d in (0, 1):
        th, V = fit_domain(rows, d, rng)
        e, a = th[1], np.exp(th[2])
        es.append(e); ves.append(V[1, 1])
        rho_d = 1 - e / a
        g = np.array([0, -1 / a, e / a, 0])                    # d rho / d (log s, e, log a, A)
        rhos.append(rho_d); grads.append(g); Vs.append(V)
        out[f"d{d}"] = {"e": float(e), "a": float(a), "rho": float(rho_d), "se_e": float(np.sqrt(V[1, 1])),
                        "se_rho": float(np.sqrt(max(g @ V @ g, 0)))}
    e_mean, se_e = np.mean(es), np.sqrt(np.sum(ves)) / 2
    rho_mean = float(np.mean(rhos))
    se_rho = float(np.sqrt(sum(g @ V @ g for g, V in zip(grads, Vs))) / 2)
    out.update({"e_mean": float(e_mean), "se_e_mean": float(se_e), "rho_mean": rho_mean, "se_rho_mean": se_rho,
                "reject_wilcox_e0": bool(abs(e_mean) > 1.96 * se_e),
                **{f"reject_rho_{r}": bool(abs(rho_mean - r) > 1.96 * se_rho) for r in (0.0, 0.725, 1.0)}})
    return out


def main(data_dir, cell, out, *_):
    np.seterr(all="ignore")
    corpus, spec = cell.split(".p")
    rho, sigma = (float(x) for x in spec.split("s"))
    z = np.load(os.path.join(data_dir, f"problems_{corpus}.npz"))
    spent = M.Problems(z["XA"], z["PA"], z["XB"], z["PB"], unit=float(z["unit"]))
    truth = E.fit_nll(C.cpt_cu_fixed(rho), E.CPT0, spent, z["k"], z["n"], 5, P.SEED)
    t0 = time.time()
    res = {"cell": cell, "corpus": corpus, "rho_true": rho, "sigma": sigma, "truth": truth.tolist(),
           "alpha": float(np.exp(truth[0])), "beta": float(np.exp(truth[1])), "sims": {}}
    for N in NS:
        rows_out = []
        for sim in range(SIMS):
            rng = np.random.default_rng([SEED, N, sim, int(1000 * rho), int(100 * sigma)])
            unit = P.study(rng)[0].unit
            rows = run_people(rng, truth, rho, sigma, N, unit)
            rows_out.append(analyse(rows, rng))
        res["sims"][str(N)] = rows_out
        print(N, f"{time.time() - t0:.0f}s", flush=True)
    res["seconds"] = time.time() - t0
    json.dump(res, open(out, "w"))
    print("RESULT-BEGIN")
    print(json.dumps({k: v for k, v in res.items() if k != "sims"}))
    print("RESULT-END", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
