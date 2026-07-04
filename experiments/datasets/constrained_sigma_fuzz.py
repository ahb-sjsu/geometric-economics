#!/usr/bin/env python3
"""Structural fuzz over the Sigma STRUCTURE, scored on held-out cross-domain transfer.

The ensemble test showed the free-DIAGONAL Sigma does not win on parsimony. This
searches for a CONSTRAINED Sigma^-1 structure that might: it fits the precision
matrix at several complexity levels and asks which maximizes held-out CROSS-DOMAIN
transfer at the fewest parameters (BIC). Discipline (against meta-overfitting):
the score is held-out TRANSFER, not in-sample fit, and the winner is a HYPOTHESIS
to be pre-registered and re-tested -- not a result.

Richer feature space (so Sigma has structure to exploit): each option ->
[EV, SD, skew, worst, p_favorable], z-scored per dataset. Cost = Mahalanobis
distance from the choice-set ideal under Sigma^-1 = L L^T; choice = softmax(-cost/T).

Sigma^-1 structures (via the Cholesky-like factor L):
  isotropic  L = a*I                     (1 param)
  diagonal   L = diag(d)                  (k params)
  rank1      L = outer(u)                 (k params, rank-1 precision)
  rank2      L = [u1 u2]                  (2k params)
  full       L = lower-triangular         (k(k+1)/2 params)

Datasets: CPC18 + choices13k (lotteries), bogota (games). Transfer = fit lotteries,
predict games (and reverse), with a per-domain temperature/scale recalibration
(the polar lesson: transfer structure, recalibrate scale).
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
from scipy.optimize import minimize

import bogota_games
import cpc18

HERE = os.path.dirname(os.path.abspath(__file__))
C13K = os.path.join(HERE, "raw", "choices13k", "c13k_selections.csv")
K = 5  # features


def _feats_two_outcome(H, p, L):
    H, p, L = np.asarray(H, float), np.asarray(p, float), np.asarray(L, float)
    ev = p * H + (1 - p) * L
    sd = np.sqrt(np.maximum(p * (H - ev) ** 2 + (1 - p) * (L - ev) ** 2, 0))
    # 2-point standardized skew, signed toward the upside
    sk = np.where((p > 0) & (p < 1), (1 - 2 * p) / np.sqrt(np.maximum(p * (1 - p), 1e-9)), 0.0)
    sk = sk * np.sign(H - L)
    worst = np.minimum(H, L)
    pfav = np.where(H >= L, p, 1 - p)
    return np.stack([ev, sd, sk, worst, pfav], axis=1)


def lottery_problems(df):
    """df with Ha,pHa,La,Hb,pHb,Lb,brate,n -> list of (X[2,K], obs[2], n)."""
    A = _feats_two_outcome(df["Ha"], df["pHa"], df["La"])
    B = _feats_two_outcome(df["Hb"], df["pHb"], df["Lb"])
    out = []
    for i in range(len(df)):
        obs = np.array([1 - df["brate"].iloc[i], df["brate"].iloc[i]])
        out.append((np.stack([A[i], B[i]]), obs, float(df["n"].iloc[i])))
    return out


def load_cpc18():
    d = cpc18.load_description().rename(columns={})
    raw = pd.read_csv(cpc18.RAW, usecols=["GameID", "Ha", "pHa", "La", "Hb", "pHb", "Lb"]).groupby("GameID").first()
    d = d.merge(raw.reset_index(), on="GameID")
    return lottery_problems(d)


def load_c13k(cap=1500):
    d = pd.read_csv(C13K)
    d = d[(d["Block"] == 1) & (d["Feedback"] == 0)] if "Block" in d else d
    d = d.rename(columns={"bRate": "brate"}).dropna(subset=["Ha", "pHa", "La", "Hb", "pHb", "Lb", "brate"])
    if len(d) > cap:
        d = d.sample(cap, random_state=0)
    return lottery_problems(d.reset_index(drop=True))


def load_games():
    games = bogota_games.load_games()
    out = []
    for g in games:
        M = g["M"]
        ev = M.mean(axis=1); sd = M.std(axis=1)
        n0 = M.shape[0]
        sk = np.array([_skew(M[i]) for i in range(n0)])
        worst = M.min(axis=1)
        pfav = np.array([(M[i] >= ev[i]).mean() for i in range(n0)])
        X = np.stack([ev, sd, sk, worst, pfav], axis=1)
        out.append((X, g["freqs"], float(g["N"])))
    return out


def _skew(x):
    x = np.asarray(x, float); m = x.mean(); s = x.std()
    return float(((x - m) ** 3).mean() / s ** 3) if s > 1e-9 else 0.0


def _zscale(problems):
    allX = np.vstack([X for X, _, _ in problems])
    mu, sd = allX.mean(0), allX.std(0) + 1e-9
    return [((X - mu) / sd, obs, n) for X, obs, n in problems], (mu, sd)


# ---- Sigma^-1 = L L^T structures ---------------------------------------------
def make_L(struct, theta):
    if struct == "isotropic":
        return np.abs(theta[0]) * np.eye(K), 1
    if struct == "diagonal":
        return np.diag(np.abs(theta[:K])), K
    if struct == "rank1":
        return np.outer(theta[:K], theta[:K]) + 1e-3 * np.eye(K), K
    if struct == "rank2":
        u1, u2 = theta[:K], theta[K:2 * K]
        return u1[:, None] * u1[None, :] + u2[:, None] * u2[None, :] + 1e-3 * np.eye(K), 2 * K
    if struct == "full":
        L = np.zeros((K, K)); idx = np.tril_indices(K)
        L[idx] = theta[:len(idx[0])]
        return L @ L.T + 1e-3 * np.eye(K), K * (K + 1) // 2
    if struct == "lowrank_diag":     # robust-PCA / GoDec: diagonal + rank-2
        d = np.abs(theta[:K]); U = theta[K:3 * K].reshape(K, 2)
        return np.diag(d) + U @ U.T + 1e-3 * np.eye(K), 3 * K
    if struct == "banded":           # local (adjacent-feature) interactions
        L = np.zeros((K, K))
        for i in range(K):
            L[i, i] = theta[i]
        for i in range(1, K):
            L[i, i - 1] = theta[K + i - 1]
        return L @ L.T + 1e-3 * np.eye(K), 2 * K - 1
    if struct == "block":            # group structure: {EV,worst,pfav} value | {SD,skew} risk
        v, r = [0, 3, 4], [1, 2]
        L = np.zeros((K, K)); t = 0
        for blk in (v, r):
            for a in range(len(blk)):
                for b in range(a + 1):
                    L[blk[a], blk[b]] = theta[t]; t += 1
        return L @ L.T + 1e-3 * np.eye(K), 9
    raise ValueError(struct)


STRUCTS = {"isotropic": 1, "diagonal": K, "rank1": K, "rank2": 2 * K,
           "banded": 2 * K - 1, "block": 9, "lowrank_diag": 3 * K, "full": K * (K + 1) // 2}


def cost_choice(P, T):
    """P[k,K] displacement-from-ideal already; return softmax choice over -||.||_P."""
    pass


def _group(problems):
    """Group problems by #options and pre-stack (vectorization; cached on the list id)."""
    key = id(problems)
    if key in _GROUP_CACHE:
        return _GROUP_CACHE[key]
    from collections import defaultdict
    g = defaultdict(list)
    for X, obs, n in problems:
        g[X.shape[0]].append((X, obs, n))
    out = []
    for kopt, items in g.items():
        Xs = np.stack([X for X, _, _ in items])          # (m, kopt, K)
        obss = np.stack([o for _, o, _ in items])         # (m, kopt)
        ns = np.array([n for *_, n in items])             # (m,)
        ideal = Xs.max(1); ideal[:, 1] = Xs[:, :, 1].min(1)  # feature 1 (SD): lower is ideal
        out.append((Xs, obss, ns, ideal))
    _GROUP_CACHE[key] = out
    return out


_GROUP_CACHE: dict = {}


def nll(struct, theta, problems):
    nparam = STRUCTS[struct]
    Pinv, _ = make_L(struct, theta[:nparam])
    T = np.abs(theta[nparam]) + 1e-6
    tot = w = 0.0
    for Xs, obss, ns, ideal in _group(problems):
        d = ideal[:, None, :] - Xs                         # (m, kopt, K)
        c = np.sqrt(np.maximum(np.einsum("mpi,ij,mpj->mp", d, Pinv, d), 0))
        z = -c / T; z -= z.max(1, keepdims=True)
        e = np.exp(z); p = np.clip(e / e.sum(1, keepdims=True), 1e-6, 1)
        tot += -np.sum(ns * np.sum(obss * np.log(p), axis=1)); w += ns.sum()
    return tot / w


def fit(struct, problems, seed=0):
    np1 = STRUCTS[struct]
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(3):
        x0 = np.r_[rng.uniform(0.3, 1.0, np1), [1.0]]
        r = minimize(lambda th: nll(struct, th, problems), x0, method="Nelder-Mead",
                     options={"maxiter": 6000, "xatol": 1e-4, "fatol": 1e-6})
        if best is None or r.fun < best.fun:
            best = r
    return best.x


def refit_T(struct, theta, problems):
    """Recalibrate ONLY the temperature on the target domain (transfer the structure)."""
    np1 = STRUCTS[struct]
    r = minimize(lambda t: nll(struct, np.r_[theta[:np1], np.abs(t)], problems), [abs(theta[np1])],
                 method="Nelder-Mead", options={"maxiter": 2000})
    return np.r_[theta[:np1], np.abs(r.x)]


def uniform_nll(problems):
    tot = w = 0.0
    for _, obs, n in problems:
        tot += -n * np.sum(obs * np.log(1.0 / len(obs))); w += n
    return tot / w


def _fit_task(s, lot, gam):
    """One structure: fit both domains (restarts inside). Returns fitted thetas."""
    return s, fit(s, lot), fit(s, gam)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=20)  # Atlas thermal cap (<=20)
    a = ap.parse_args()

    lot = _zscale(load_cpc18() + load_c13k())[0]
    gam = _zscale(load_games())[0]
    ch_l, ch_g = uniform_nll(lot), uniform_nll(gam)
    n_l = sum(int(n) for *_, n in lot); n_g = sum(int(n) for *_, n in gam)
    print(f"lotteries: {len(lot)} problems (CPC18+choices13k)  games: {len(gam)} (bogota)  K={K} features")
    print(f"fuzzing {len(STRUCTS)} structures on {a.workers} workers\n", flush=True)

    from joblib import Parallel, delayed
    fitted = Parallel(n_jobs=a.workers)(delayed(_fit_task)(s, lot, gam) for s in STRUCTS)

    print(f"{'structure':13} {'#p':>4} {'lot native':>10} {'gm native':>10} "
          f"{'lot->gm':>10} {'gm->lot':>10} {'BIC(pooled)':>12} {'transfer%':>9}")
    rows = []
    for s, th_l, th_g in fitted:
        nat_l, nat_g = nll(s, th_l, lot), nll(s, th_g, gam)
        tr_lg = nll(s, refit_T(s, th_l, gam), gam)
        tr_gl = nll(s, refit_T(s, th_g, lot), lot)
        k = STRUCTS[s] + 1
        bic = k * np.log(n_l + n_g) + 2 * (n_l + n_g) * (nat_l * n_l + nat_g * n_g) / (n_l + n_g)
        tr_mean = (max(0, (ch_g - tr_lg) / (ch_g - nat_g)) + max(0, (ch_l - tr_gl) / (ch_l - nat_l))) / 2
        rows.append((s, k, nat_l, nat_g, tr_lg, tr_gl, bic, tr_mean))
        print(f"{s:13} {k:>4} {nat_l:>10.4f} {nat_g:>10.4f} {tr_lg:>10.4f} {tr_gl:>10.4f} "
              f"{bic:>12.0f} {tr_mean*100:>8.0f}%", flush=True)
    print(f"\nchance: lot {ch_l:.4f}  games {ch_g:.4f}")
    best_tr = max(rows, key=lambda r: r[7])
    best_bic = min(rows, key=lambda r: r[6])
    print(f"best TRANSFER structure: {best_tr[0]} (mean gap-closed {best_tr[7]*100:.0f}%)")
    print(f"best BIC structure:      {best_bic[0]} ({best_bic[1]} params)")
    print("\nHONEST: winner is a HYPOTHESIS to pre-register + re-test on held-out data, not a result. "
          "If a low-param structure (isotropic/rank1) matches full on transfer, that is the parsimony "
          "win the diagonal Sigma lacked; if only 'full' transfers, interactions matter but cost params.")


if __name__ == "__main__":
    main()
