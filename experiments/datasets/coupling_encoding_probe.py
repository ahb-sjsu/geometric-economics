#!/usr/bin/env python3
"""Does the ENCODING geometry mask a real cross-domain coupling? (a viable-path-to-B probe)

Hypothesis: a single latent metric factor f governs both domains, but *through* each domain's
reflection axis (gain/loss in risk; advantageous/disadvantageous in social — the V4 'reflection broken
by aversion' motif that recurs across the program). If f loads with OPPOSITE sign across the reflection
(loss aversion / inequality aversion = the symmetry-breaking term), then fitting ONE pooled angle per
domain averages the two halves and f cancels -> naive corr(theta_risk, theta_social) ~ 0 (the GPS
'no coupling' outcome), EVEN THOUGH one rank-1 factor governs both.

We simulate CHOICES under this structure (reusing the frozen choice model), fit angles two ways, and
compare what each recovers:
  NAIVE      one pooled angle per domain -> corr                       (the test that failed on GPS)
  RESOLVED   four reflection-resolved sub-angles (risk-gain, risk-loss,
             social-adv, social-dis), sign-aligned by the KNOWN reflection axis, then a joint factor
             -> cross-domain corr + rank

If NAIVE ~ 0 while RESOLVED recovers a strong rank-1 factor, the encoding (pooling over the reflection)
was the miss, and the reflection-resolved joint factor is a viable path to Level B.

    python coupling_encoding_probe.py
"""
from __future__ import annotations

import numpy as np

from coupling_power_sim import GRID, THETA_MEAN, design, grid_mle, sim_choices


def draw_subangles(n, load, idio, rng):
    """4 reflection-resolved sub-angles per subject: a shared factor f loads +load on the '+' side of
    each domain's reflection axis and -load on the '-' side (reflection broken by the shared aversion),
    plus block-idiosyncratic noise. Returns (theta_rg, theta_rl, theta_sa, theta_sd), each (n,)."""
    f = rng.normal(size=n)  # the single shared latent metric factor
    signs = {"rg": +1, "rl": -1, "sa": +1, "sd": -1}  # reflection: + and - sides load oppositely
    out = {}
    for k, s in signs.items():
        out[k] = np.clip(THETA_MEAN + load * s * f + idio * rng.normal(size=n), GRID[0], GRID[-1])
    return out["rg"], out["rl"], out["sa"], out["sd"], f


def fit_block(theta_true, K, rng):
    dA, dB = design(K, rng)
    y, _ = sim_choices(theta_true, dA, dB, rng)
    return grid_mle(y, dA, dB)


def corr(a, b):
    if np.std(a) < 1e-9 or np.std(b) < 1e-9:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def run(N=400, K=32, load=0.30, idio=0.15, reps=60, seed=0):
    rng = np.random.default_rng(seed)
    naive, res_cross, pc1, recov = [], [], [], []
    for _ in range(reps):
        trg, trl, tsa, tsd, f = draw_subangles(N, load, idio, rng)
        # fit each reflection-resolved sub-angle from its own choices
        hrg = fit_block(trg, K // 2, rng); hrl = fit_block(trl, K // 2, rng)
        hsa = fit_block(tsa, K // 2, rng); hsd = fit_block(tsd, K // 2, rng)
        # NAIVE: pool across the reflection (average the two halves) -> one angle per domain
        naive.append(corr((hrg + hrl) / 2, (hsa + hsd) / 2))
        # RESOLVED: sign-align by the known reflection axis (flip the '-' side), then couple
        A = np.c_[hrg, -hrl, hsa, -hsd]  # 4 sign-aligned sub-angles
        A = (A - A.mean(0)) / A.std(0)
        res_cross.append(np.mean([corr(A[:, i], A[:, j]) for i in (0, 1) for j in (2, 3)]))
        R = np.corrcoef(A, rowvar=False)
        ev = np.sort(np.linalg.eigvalsh(R))[::-1]
        pc1.append(ev[0] / ev.sum())
        recov.append(corr(A.mean(1), f))  # does the joint factor recover the true f?
    def s(x):
        return f"{np.mean(x):+.3f} ± {np.std(x):.3f}"
    print(f"== reflection-structured single-factor coupling (N={N}, K={K}, load={load}, reps={reps}) ==\n")
    print(f"  NAIVE   corr(pooled theta_risk, pooled theta_social) = {s(naive)}   "
          f"<- the test that failed on GPS")
    print(f"  RESOLVED mean cross-domain corr (sign-aligned sub-angles) = {s(res_cross)}")
    print(f"  RESOLVED joint-factor PC1 share = {np.mean(pc1)*100:.0f}%   "
          f"(rank-1 if >60%)")
    print(f"  RESOLVED recovers the true latent factor f: corr = {s(recov)}")
    print("\n  => if NAIVE ~ 0 but RESOLVED is strong + rank-1, the encoding (pooling over the")
    print("     reflection) masked a real rank-1 coupling. The reflection-resolved joint factor is")
    print("     the path to B; the naive angle correlation is the wrong statistic.")


if __name__ == "__main__":
    run()
    print()
    # control: if the factor does NOT flip across the reflection (no reflection structure), the naive
    # test should ALSO work -- confirms the masking is specifically the reflection sign-flip.
    print("---- control: same-sign loadings (no reflection flip) => naive should also recover ----")
    import coupling_encoding_probe as m

    def _draw_samesign(n, load, idio, rng):
        f = rng.normal(size=n)
        out = [np.clip(THETA_MEAN + load * f + idio * rng.normal(size=n), GRID[0], GRID[-1])
               for _ in range(4)]
        return (*out, f)

    m.draw_subangles = _draw_samesign
    m.run(reps=60, seed=1)
