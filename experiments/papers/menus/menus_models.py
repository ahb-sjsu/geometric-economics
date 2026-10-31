#!/usr/bin/env python3
"""Models of prereg-menus-v1: choice from menus of all-or-nothing gambles (probability p of m, else 0).

An option's coordinates are x = (W(p), (m/20)^alpha), W linear in log-odds (gamma, delta). Every
option shown enters the menu statistics (range, normalisation sum); only available options can be
chosen. Choice is a softmax of minus the cost over the available options.

    ADD    a_p (r_p - x_p) + a_m (r_m - x_m), r the attribute-wise best shown: context-free
    RNG    the same with each gap divided by the menu range on that attribute raised to rho
           (rho fixed: rho = RHO_STAR for the registered model RNG, rho = 1 for RNG1, rho free in
           (0, 1.5) for RNGfree, which is fit only to estimate rho for H4)
    DN     divisive normalisation: V = x_p x_m, u = V / (sigma + sum of V over shown options), cost -beta u

Parameters theta: [log gamma, delta, log alpha, log a_p, log a_m] (+ log sigma for DN; a_p is beta).
"""
from __future__ import annotations

import numpy as np

RHO_STAR = 0.5256     # median of 40 per-participant fits, Molter et al. 2022 (development, explore_molter3.json)
X0 = [np.log(0.7), 0.0, np.log(0.9), np.log(8.0), np.log(8.0)]


def coords(th, P, M):
    g, d, al = np.exp(th[0]), th[1], np.exp(th[2])
    Pc = np.clip(P, 1e-6, 1 - 1e-6)
    W = 1 / (1 + np.exp(-np.clip(g * (np.log(Pc) - np.log1p(-Pc)) + d, -50, 50)))
    return W, (M / 20.0) ** al


def _mx(x, shown):
    return np.where(shown, x, -np.inf).max(1, keepdims=True)


def _mn(x, shown):
    return np.where(shown, x, np.inf).min(1, keepdims=True)


def costs(model, th, P, M, shown):
    """P, M: (n, 3) arrays; shown: (n, 3) bool. Entries not shown are ignored (fill them with any number)."""
    P = np.where(shown, P, 0.5); M = np.where(shown, M, 1.0)
    xp, xm = coords(th, P, M)
    if model == "DN":
        V = np.where(shown, xp * xm, 0.0)
        beta, sigma = np.exp(np.clip(th[3], -20, 20)), np.exp(np.clip(th[5], -20, 20))
        return -beta * V / (sigma + V.sum(1, keepdims=True))
    gp, gm = _mx(xp, shown) - xp, _mx(xm, shown) - xm
    if model.startswith("RNG"):
        rho = {"RNG1": 1.0, "RNG": RHO_STAR}.get(model)
        if model == "RNGfree":
            rho = 1.5 / (1 + np.exp(-th[5]))
        gp = gp / (_mx(xp, shown) - _mn(xp, shown) + 1e-6) ** rho
        gm = gm / (_mx(xm, shown) - _mn(xm, shown) + 1e-6) ** rho
    return np.exp(np.clip(th[3], -20, 20)) * gp + np.exp(np.clip(th[4], -20, 20)) * gm


def log_probs(model, th, P, M, shown, avail):
    z = np.where(avail, -costs(model, th, P, M, shown), -np.inf)
    z = z - z.max(1, keepdims=True)
    return z - np.log(np.exp(z).sum(1, keepdims=True))


def x0(model):
    return X0 + ([0.0] if model in ("DN", "RNGfree") else [])


def rho_of(th):
    return float(1.5 / (1 + np.exp(-th[5])))


MODELS = ["ADD", "RNG", "RNG1", "DN"]       # scored; RNGfree is fit only for H4
