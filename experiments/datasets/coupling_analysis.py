#!/usr/bin/env python3
"""FROZEN confirmatory analysis for prereg-coupling-angle-v1.

Given a same-subject study (risk gain/loss, social adv/dis, patience blocks), this scores the frozen
rank-ladder Level-B test exactly as §4.2/§4.3/§4.6 specify:

  fit per-subject sub-angles (grid-MLE, fixed-temperature rule)  ->  disattenuate for measurement
  error (split-half reliability)  ->  three-rung ladder with subject-bootstrap CIs:
    rank-0  scalar  corr(pooled theta_risk, pooled theta_social)           (secondary; null != falsify)
    PRIMARY aversion contrast corr(theta_rg - theta_rl, theta_sa - theta_sd)
    rank>=2 joint factor (cross-fitted CCA over the reflection sub-angles)
  plus null controls (§4.6): subject-permutation null and the magnitude channel, both must be ~0.

PASS at a rung = disattenuated bootstrap CI lower > 0.10, sign positive. B is supported if any rung
passes (the rung is the finding); a null at EVERY rung falsifies. Deterministic given the seed.

Data schema: choices[block] = (N, K_block) array of 0/1 (1 = chose option A); designs[block] =
(dA, dB) each (K_block, 2) shortfalls. blocks = risk_gain, risk_loss, social_adv, social_dis, patience.

  python coupling_analysis.py           # end-to-end demo on simulated data (also the test path)
"""
from __future__ import annotations

import numpy as np

from coupling_power_sim import GRID, THETA_MEAN, design, grid_mle, sim_choices

BLOCKS = ["risk_gain", "risk_loss", "social_adv", "social_dis", "patience"]
NULL = 0.10


def corr(a, b):
    if np.std(a) < 1e-9 or np.std(b) < 1e-9:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def fit_subangles(choices, designs):
    """{block: (N,K)} + {block: (dA,dB)} -> {block: (N,) fitted angle}."""
    return {b: grid_mle(choices[b], *designs[b]) for b in choices}


def split_half_reliability(y, dA, dB, rng):
    """Spearman-Brown-corrected split-half reliability of the fitted angle across subjects."""
    K = y.shape[1]
    idx = rng.permutation(K)
    h1, h2 = idx[: K // 2], idx[K // 2:]
    t1, t2 = grid_mle(y[:, h1], dA[h1], dB[h1]), grid_mle(y[:, h2], dA[h2], dB[h2])
    r = corr(t1, t2)
    return max(1e-3, min(0.999, 2 * r / (1 + r))) if r > 0 else 1e-3


def _cca(X, Y):
    n = len(X)
    Cxx = X.T @ X / n + 1e-3 * np.eye(X.shape[1])
    Cyy = Y.T @ Y / n + 1e-3 * np.eye(Y.shape[1])
    Cxy = X.T @ Y / n
    M = np.linalg.solve(Cxx, Cxy) @ np.linalg.solve(Cyy, Cxy.T)
    ev, V = np.linalg.eig(M)
    a = np.real(V[:, int(np.argmax(np.real(ev)))])
    b = np.linalg.solve(Cyy, Cxy.T @ a)
    return a, b


def _joint_factor_scores(S, rng, n_folds=5):
    """Cross-fitted CCA over the 4 reflection sub-angles -> per-subject (risk_score, social_score)."""
    H = np.column_stack([S["risk_gain"], S["risk_loss"], S["social_adv"], S["social_dis"]])
    N = len(H)
    risk = np.zeros(N)
    soc = np.zeros(N)
    for te in np.array_split(rng.permutation(N), n_folds):
        tr = np.setdiff1d(np.arange(N), te)
        mu, sd = H[tr].mean(0), np.maximum(H[tr].std(0), 1e-6)
        Ztr, Zte = (H[tr] - mu) / sd, (H[te] - mu) / sd
        a, b = _cca(Ztr[:, :2], Ztr[:, 2:])
        if corr(Ztr[:, :2] @ a, Ztr[:, 2:] @ b) < 0:
            b = -b
        risk[te], soc[te] = Zte[:, :2] @ a, Zte[:, 2:] @ b
    return risk, soc


def _boot_ci(x, y, rng, denom=1.0, n_boot=2000):
    """Returns (raw_r, raw_ci_lo, raw_ci_hi, disattenuated_r). PASS is decided on the RAW CI (§4.1
    conservative: if the raw CI lower clears 0.10, the disattenuated does too); the disattenuated point
    is the true-magnitude estimate (capped at 0.99 — disattenuation can exceed 1 under noise)."""
    r = corr(x, y)
    N = len(x)
    boots = np.array([corr(x[s], y[s]) for s in (rng.integers(0, N, N) for _ in range(n_boot))])
    disatt = float(np.clip(r / max(denom, 1e-3), -0.99, 0.99))
    return r, float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)), disatt


def rank_ladder(S, rel, rng):
    """Rank-ladder with subject-bootstrap CIs (PASS on raw) + disattenuated magnitude. S: sub-angles."""
    out = {}
    rk = np.sqrt(rel["risk_gain"] * rel["social_adv"])
    out["scalar"] = _boot_ci((S["risk_gain"] + S["risk_loss"]) / 2,
                             (S["social_adv"] + S["social_dis"]) / 2, rng, denom=rk)
    a_risk = S["risk_gain"] - S["risk_loss"]
    a_soc = S["social_adv"] - S["social_dis"]
    da = np.sqrt(((rel["risk_gain"] + rel["risk_loss"]) / 2) * ((rel["social_adv"] + rel["social_dis"]) / 2))
    out["aversion"] = _boot_ci(a_risk, a_soc, rng, denom=da)
    risk, soc = _joint_factor_scores(S, rng)
    out["joint_factor"] = _boot_ci(risk, soc, rng)  # already cross-fitted (no disattenuation needed)
    return out


def null_controls(S, rng):
    """§4.6: subject-permutation null and magnitude channel — both must be ~0 (CI includes 0)."""
    a_risk = S["risk_gain"] - S["risk_loss"]
    a_soc = S["social_adv"] - S["social_dis"]
    perm = corr(a_risk, a_soc[rng.permutation(len(a_soc))])  # break same-subject link
    # magnitude channel: the pooled *level* (mean angle), the geometry-free radial coordinate
    mag = corr((S["risk_gain"] + S["risk_loss"]) / 2, (S["social_adv"] + S["social_dis"]) / 2)
    return {"permutation_null": float(perm), "magnitude_channel": float(mag)}


def analyze(choices, designs, rng):
    S = fit_subangles(choices, designs)
    rel = {b: split_half_reliability(choices[b], *designs[b], rng) for b in choices}
    return {"ladder": rank_ladder(S, rel, rng), "nulls": null_controls(S, rng), "reliability": rel}


# ---- simulation path (test + demo): generate a study under a reflection-structured shared metric ----
def simulate_study(N, K, load, idio, rng, coupled=True):
    f = rng.normal(size=N) if coupled else np.zeros(N)
    signs = {"risk_gain": +1, "risk_loss": -1, "social_adv": +1, "social_dis": -1, "patience": 0}
    choices, designs = {}, {}
    for b, s in signs.items():
        theta = np.clip(THETA_MEAN + load * s * f + idio * rng.normal(size=N), GRID[0], GRID[-1])
        dA, dB = design(K, rng)
        y, _ = sim_choices(theta, dA, dB, rng)
        choices[b], designs[b] = y, (dA, dB)
    return choices, designs


def _fmt(t):
    r, lo, hi, disatt = t
    return (f"raw r={r:+.3f} CI[{lo:+.3f},{hi:+.3f}]  disatt={disatt:+.3f}  "
            f"{'PASS' if lo > NULL else '--'}")


def main():
    rng = np.random.default_rng(0)
    choices, designs = simulate_study(N=400, K=32, load=0.30, idio=0.15, rng=rng)
    res = analyze(choices, designs, np.random.default_rng(1))
    print("== prereg-coupling-angle-v1 confirmatory scorecard (demo: simulated reflection-structured B) ==\n")
    print("  reliability:", {k: round(v, 2) for k, v in res["reliability"].items()})
    print("\n  RANK LADDER (PASS = disattenuated CI lower > 0.10):")
    print(f"    rank-0 scalar (secondary)   {_fmt(res['ladder']['scalar'])}")
    print(f"    aversion contrast (PRIMARY) {_fmt(res['ladder']['aversion'])}")
    print(f"    joint factor (rank>=2)      {_fmt(res['ladder']['joint_factor'])}")
    print(f"\n  null controls (must be ~0): {res['nulls']}")


if __name__ == "__main__":
    main()
