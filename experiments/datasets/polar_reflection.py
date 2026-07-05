#!/usr/bin/env python3
"""Polar (PolarQuant-style) reflection encoding — ONE metric spanning gain & loss.

The discrete reflection fuzz (reflection_fuzz.py) found that flipping the loss-domain
ideal on {SD, worst, pfav} lifts gain<->loss transfer from 0% to ~80%. That flip is
BINARY (ideal = min or max). PolarQuant's lesson — split magnitude (radius) from
direction (angle), transfer the angle, recalibrate the scale — makes the reflection
CONTINUOUS: the loss domain is the gain domain *reflected across the value axis*, and
the reflection strength per coordinate is a fitted, scale-invariant shape parameter.

Encoding: apply a per-coordinate reflection coefficient rho_c to the loss-domain
features (c in {SD, worst, pfav}); rho=+1 is no reflection (raw), rho=-1 is a full
mirror. Then ONE shared metric + ONE temperature are fit JOINTLY on all gain+loss
cells (true unification, not fit-one-transfer-other). We compare:

  raw (rho=1, one model)      -- the failing baseline
  polar (rho fitted, one model) -- one metric + reflection spanning both domains
  ceiling (two separate models) -- the best any gain/loss split can do

If polar approaches the ceiling with ONE metric, reflection is captured as a
geometric mirror, and the recovered rho reports HOW MUCH each coordinate reflects.

    python polar_reflection.py
"""
from __future__ import annotations

import os

import numpy as np
from scipy.optimize import minimize

import constrained_sigma_fuzz as F
from reflection_fuzz import build

HERE = os.path.dirname(os.path.abspath(__file__))
STRUCT = "rank2"
REFLECT = [1, 3, 4]          # coords with fitted reflection: SD, worst, pfav
NAMES = ["EV", "SD", "skew", "worst", "pfav"]


def transform(X, is_loss, rho):
    """Multiply the loss-domain features on REFLECT coords by rho (per-coord)."""
    Xt = X.copy()
    for c, r in zip(REFLECT, rho):
        Xt[is_loss, :, c] = X[is_loss, :, c] * r
    return Xt


def _ideal(Xt):
    hi = Xt.max(1)
    lo = Xt.min(1)
    ideal = hi.copy()
    ideal[:, 1] = lo[:, 1]        # SD: low is ideal (in the transformed space, reflection handles loss)
    return ideal


def nll_raw(struct, theta, X, obs, ns, ideal):
    nparam = F.STRUCTS[struct]
    Pinv, _ = F.make_L(struct, theta[:nparam])
    T = np.abs(theta[nparam]) + 1e-6
    d = ideal[:, None, :] - X
    c = np.sqrt(np.maximum(np.einsum("mpi,ij,mpj->mp", d, Pinv, d), 0))
    z = -c / T
    z -= z.max(1, keepdims=True)
    e = np.exp(z)
    p = np.clip(e / e.sum(1, keepdims=True), 1e-6, 1)
    return -np.sum(ns * np.sum(obs * np.log(p), axis=1)) / ns.sum()


def nll_polar(theta, X, obs, ns, is_loss):
    nparam = F.STRUCTS[STRUCT]
    rho = theta[nparam + 1: nparam + 1 + len(REFLECT)]
    Xt = transform(X, is_loss, rho)
    return nll_raw(STRUCT, theta[:nparam + 1], Xt, obs, ns, _ideal(Xt))


def fit_polar(X, obs, ns, is_loss, fix_rho=None, seed=0):
    np1 = F.STRUCTS[STRUCT]
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(6):
        if fix_rho is None:
            x0 = np.r_[rng.uniform(0.3, 1.0, np1), [1.0], rng.uniform(-1.0, 1.0, len(REFLECT))]
            fn = lambda th: nll_polar(th, X, obs, ns, is_loss)
        else:
            x0 = np.r_[rng.uniform(0.3, 1.0, np1), [1.0]]
            fn = lambda th: nll_polar(np.r_[th, fix_rho], X, obs, ns, is_loss)
        r = minimize(fn, x0, method="Nelder-Mead",
                     options={"maxiter": 12000, "xatol": 1e-4, "fatol": 1e-6})
        if best is None or r.fun < best.fun:
            best = r
    return best.x


def two_model_ceiling(X, obs, ns, is_loss):
    """FAIR ceiling: a separate best model per domain. The gain model uses the raw
    ideal; the LOSS model gets its own reflection (fitted rho) -- so the loss domain
    is fit as well as it can be. This is the true 'two separate theories' bound."""
    # gain-only (raw): rho irrelevant (no loss cells among these)
    thg = fit_polar(X[~is_loss], obs[~is_loss], ns[~is_loss], is_loss[~is_loss],
                    fix_rho=np.ones(len(REFLECT)))
    ng = nll_polar(np.r_[thg, np.ones(len(REFLECT))], X[~is_loss], obs[~is_loss], ns[~is_loss],
                   is_loss[~is_loss])
    # loss-only WITH its own reflection: treat every loss cell as reflectable
    all_loss = np.ones(is_loss.sum(), bool)
    thl = fit_polar(X[is_loss], obs[is_loss], ns[is_loss], all_loss)
    nl = nll_polar(thl, X[is_loss], obs[is_loss], ns[is_loss], all_loss)
    wg, wl = ns[~is_loss].sum(), ns[is_loss].sum()
    return (ng * wg + nl * wl) / (wg + wl)


def main():
    X, obs, ns, is_loss = build(None)
    print(f"Polar reflection: {len(X)} cells ({is_loss.sum()} loss / {(~is_loss).sum()} gain), "
          f"structure={STRUCT}\n")

    # baseline: one model, no reflection (rho=1)
    th_raw = fit_polar(X, obs, ns, is_loss, fix_rho=np.ones(len(REFLECT)))
    nll_raw_pooled = nll_polar(np.r_[th_raw, np.ones(len(REFLECT))], X, obs, ns, is_loss)

    # polar: one model + fitted reflection
    th_pol = fit_polar(X, obs, ns, is_loss)
    nll_pol = nll_polar(th_pol, X, obs, ns, is_loss)
    rho = th_pol[F.STRUCTS[STRUCT] + 1:]

    ceiling = two_model_ceiling(X, obs, ns, is_loss)

    print("model                                pooled NLL   note")
    print(f"raw (one metric, rho=1)             {nll_raw_pooled:>10.4f}   the failing baseline")
    print(f"polar (one metric + reflection)     {nll_pol:>10.4f}   ONE model, both domains")
    print(f"ceiling (two separate metrics)      {ceiling:>10.4f}   best any split can do")
    closed = (nll_raw_pooled - nll_pol) / (nll_raw_pooled - ceiling) if nll_raw_pooled > ceiling else 0
    print(f"\npolar closes {100 * closed:.0f}% of the raw->two-model gap with a SINGLE metric.")
    print("recovered reflection coefficients (rho ~ -1 => full mirror across the value axis):")
    for c, r in zip(REFLECT, rho):
        print(f"    rho[{NAMES[c]:5}] = {r:+.2f}")
    print("\nHONEST: the reflection coefficients are fit on Ruggeri; PRE-REGISTER and re-test on a "
          "held-out loss corpus before claiming reflection is 'solved'.")


if __name__ == "__main__":
    main()
