#!/usr/bin/env python3
"""Simulation-based power analysis for prereg-coupling-angle-v1 (§6).

Generative model (the frozen GDT choice model): each subject has a latent risk angle theta_risk and
social angle theta_social, drawn correlated at rho_true. In each domain the cost of an option with
2-D shortfalls (d1,d2)>=0 is the city-block Mahalanobis form cost = cos(theta)*d1 + sin(theta)*d2
(Part II selected a variance dispersion feature + city-block norm); binary choices follow the
fixed-temperature logit P(A) = sigmoid((cost_B - cost_A)/T). We simulate K choices/domain/subject,
REFIT each angle by grid MLE from the choices (so the estimate carries realistic noise),
disattenuate the across-subject correlation for that measurement error, and test H0: rho <= 0.10 with
a subject bootstrap CI. Power = fraction of reps whose CI lower bound > 0.10 (the §4.1 pass rule).

Sweep (N subjects, K choices/block) to find the smallest design with >= 80% power.

    python coupling_power_sim.py            # default sweep
    python coupling_power_sim.py --quick    # smaller/faster
"""
from __future__ import annotations

import argparse

import numpy as np

GRID = np.linspace(0.05, np.pi / 2 - 0.05, 61)  # angle grid for the MLE
THETA_MEAN = np.pi / 4
THETA_SD = 0.35  # between-subject heterogeneity (rad); need spread to detect a correlation
T = 0.20  # choice temperature (implied per-choice accuracy reported below)
NULL = 0.10  # H0: rho <= NULL (the prereg falsifier boundary)


def design(K, rng):
    """K binary choices; each option a 2-D shortfall in [0,1]^2 (varied tradeoffs identify theta)."""
    return rng.uniform(0, 1, (K, 2)), rng.uniform(0, 1, (K, 2))


def _cost(theta, d):  # theta: (...,), d: (K,2) -> (..., K)
    return np.cos(theta)[..., None] * d[:, 0] + np.sin(theta)[..., None] * d[:, 1]


def sim_choices(thetas, dA, dB, rng):
    """thetas:(N,) -> choices y:(N,K) in {0,1}, 1 = chose A."""
    dc = _cost(thetas, dB) - _cost(thetas, dA)  # (N,K): >0 favors A
    p = 1.0 / (1.0 + np.exp(-dc / T))
    return (rng.uniform(size=p.shape) < p).astype(float), float(np.mean(np.maximum(p, 1 - p)))


def grid_mle(y, dA, dB):
    """y:(N,K) -> theta_hat:(N,) by argmax over GRID of the logit log-likelihood."""
    cA = _cost(GRID, dA)  # (G,K)
    cB = _cost(GRID, dB)
    p = 1.0 / (1.0 + np.exp(-(cB - cA) / T))  # (G,K) = P(A|theta)
    p = np.clip(p, 1e-6, 1 - 1e-6)
    ll = y @ np.log(p).T + (1 - y) @ np.log(1 - p).T  # (N,G)
    return GRID[np.argmax(ll, axis=1)]


def draw_thetas(n, rho, rng):
    z = rng.multivariate_normal([0, 0], [[1, rho], [rho, 1]], size=n)
    th = np.clip(THETA_MEAN + THETA_SD * z, GRID[0], GRID[-1])
    return th[:, 0], th[:, 1]


def corr(a, b):
    if np.std(a) < 1e-9 or np.std(b) < 1e-9:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def split_half_reliability(y, dA, dB, rng):
    """Spearman-Brown-corrected split-half reliability of theta_hat across subjects."""
    K = y.shape[1]
    idx = rng.permutation(K)
    h1, h2 = idx[: K // 2], idx[K // 2:]
    t1 = grid_mle(y[:, h1], dA[h1], dB[h1])
    t2 = grid_mle(y[:, h2], dA[h2], dB[h2])
    r = corr(t1, t2)
    return max(0.0, min(0.999, 2 * r / (1 + r) if r > 0 else 0.0))  # Spearman-Brown


def one_rep(N, K, rho, rng, n_boot=400):
    dAr, dBr = design(K, rng)
    dAs, dBs = design(K, rng)
    tr, ts = draw_thetas(N, rho, rng)
    yr, accr = sim_choices(tr, dAr, dBr, rng)
    ys, accs = sim_choices(ts, dAs, dBs, rng)
    hr, hs = grid_mle(yr, dAr, dBr), grid_mle(ys, dAs, dBs)
    r_obs = corr(hr, hs)
    rel_r = split_half_reliability(yr, dAr, dBr, rng)
    rel_s = split_half_reliability(ys, dAs, dBs, rng)
    denom = np.sqrt(max(rel_r * rel_s, 1e-6))
    r_corr = float(np.clip(r_obs / denom, -0.999, 0.999))
    # subject bootstrap CI on the disattenuated correlation
    boots = np.empty(n_boot)
    for b in range(n_boot):
        s = rng.integers(0, N, N)
        rb = corr(hr[s], hs[s])
        boots[b] = np.clip(rb / denom, -0.999, 0.999)
    lo = float(np.percentile(boots, 2.5))
    return dict(r_obs=r_obs, r_corr=r_corr, rel=np.sqrt(rel_r * rel_s), lo=lo,
                reject=lo > NULL, sign_ok=r_obs > 0, acc=(accr + accs) / 2)


def run_cell(N, K, rho, n_rep, seed):
    rng = np.random.default_rng(seed)
    res = [one_rep(N, K, rho, rng) for _ in range(n_rep)]
    power = np.mean([r["reject"] and r["sign_ok"] for r in res])
    return dict(N=N, K=K, power=float(power),
                r_obs=float(np.mean([r["r_obs"] for r in res])),
                r_corr=float(np.mean([r["r_corr"] for r in res])),
                rel=float(np.mean([r["rel"] for r in res])),
                acc=float(np.mean([r["acc"] for r in res])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rho", type=float, default=0.30, help="true latent coupling to power for")
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    Ns = [200, 300, 400] if a.quick else [200, 300, 400, 600]
    Ks = [24, 40] if a.quick else [16, 24, 32, 48]
    reps = 80 if a.quick else a.reps
    print(f"== power to reject H0: rho<=0.10, at true rho={a.rho}, T={T}, theta_sd={THETA_SD} ==")
    print(f"   (reps={reps}; pass = disattenuated bootstrap CI lower > 0.10 AND raw sign positive)\n")
    print(f"   {'N':>5} {'K':>4} {'power':>7} {'r_obs':>7} {'r_corr':>7} {'reliab':>7} {'acc':>6}")
    hits = []
    for N in Ns:
        for K in Ks:
            c = run_cell(N, K, a.rho, reps, seed=1000 + N + K)
            flag = "  <== >=0.80" if c["power"] >= 0.80 else ""
            print(f"   {N:>5} {K:>4} {c['power']:>7.2f} {c['r_obs']:>7.3f} {c['r_corr']:>7.3f} "
                  f"{c['rel']:>7.2f} {c['acc']:>6.2f}{flag}")
            if c["power"] >= 0.80:
                hits.append((N * 2 * K, N, K, c["power"]))  # total choices/subject-block proxy
    print()
    if hits:
        hits.sort()
        _, N, K, pw = hits[0]
        print(f"== smallest adequate design: N={N} subjects x K={K} choices/block "
              f"(power {pw:.2f}); K_P (patience) can be ~K/2 for the rank test ==")
    else:
        print("== no cell reached 80% power in this grid; enlarge N/K or raise assumed rho ==")


if __name__ == "__main__":
    main()
