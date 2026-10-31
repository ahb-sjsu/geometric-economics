#!/usr/bin/env python3
"""Probability readers for the stratified geometry (development, after prereg-strata-v1).

prereg-strata-v1 found that GDT-S reads probabilities linearly: its coordinates g, l, pi+, pi- are all
linear in p, so it cannot produce the inverse-S distortion people showed in four of five corpora. Here
the coordinates are built from decision weights instead of raw probabilities. Weights are
rank-dependent within each stratum (as in CPT): branches are ordered from the most extreme outcome
towards zero, and each takes W(cumulative) - W(cumulative before it). So pi+ = W(P(X > 0)) and
pi- = W(P(X < 0)), and W(0) = 0, W(1) = 1 exactly: the strata boundaries are read without error.

Readers W:
    lin   W(c) = c                                       GDT-S as registered
    fr    W(c) = (2/pi) arcsin(sqrt c)                   Fisher-Rao arc length on the Bernoulli family; no parameter
    llo   W(c) = logistic(gamma logit c + delta)          linear in log-odds (Gonzalez and Wu 1999); two parameters
    eff   W(c) = E[decoded c]                             efficient code for the corpus's own probabilities
                                                          (Frydman and Jin): encode theta = sin^2(pi F(c) / 2) with F
                                                          the corpus prior's CDF, observe k ~ Bin(n, theta), decode the
                                                          posterior mean. One parameter, the capacity n. The prior,
                                                          and so the distortion, comes from each corpus's stimuli.
"""
from __future__ import annotations

import os
import sys

import numpy as np
from scipy.stats import binom

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "strata"))
import strata_models as M  # noqa: E402

GRID = 400
PG = (np.arange(GRID) + 0.5) / GRID


def w_fr(c, th=None):
    return 2 / np.pi * np.arcsin(np.sqrt(np.clip(c, 0, 1)))


def w_llo(c, th):
    g, d = np.exp(th[0]), th[1]
    c = np.clip(c, 1e-12, 1 - 1e-12)
    out = 1 / (1 + np.exp(-(g * (np.log(c) - np.log1p(-c)) + d)))
    return out


def decumulatives(X, P):
    """All decumulative probabilities within each stratum, strictly inside (0, 1)."""
    out = []
    for sign in (1, -1):
        Ps = np.where(sign * X > 0, P, 0.0)
        Xs = np.where(sign * X > 0, np.abs(X), 0.0)
        o = np.argsort(-Xs, axis=1)
        cum = np.cumsum(np.take_along_axis(Ps, o, 1), 1)
        out.append(cum[(cum > 1e-9) & (cum < 1 - 1e-9)])
    return np.concatenate(out)


class Prior:
    """A corpus's prior over probabilities: kernel density of its decumulative probabilities in
    log-odds (bandwidth 0.35), mixed with 5% uniform so no probability has zero prior."""

    def __init__(self, pr: "M.Problems", bw=0.35, mix=0.05):
        c = np.r_[decumulatives(pr.XA, pr.PA), decumulatives(pr.XB, pr.PB)]
        lo = np.log(c) - np.log1p(-c)
        lg = np.log(PG) - np.log1p(-PG)
        dens = np.exp(-0.5 * ((lg[:, None] - lo[None, :]) / bw) ** 2).sum(1) / (PG * (1 - PG))
        dens /= dens.sum()
        self.f = (1 - mix) * dens + mix / GRID
        self.F = np.cumsum(self.f) - self.f / 2
        self.n_probs = int(c.size)
        self._cache = {}

    def curve(self, n):
        """W on the grid for capacity n (integer number of binomial samples)."""
        if n not in self._cache:
            theta = np.sin(np.pi * self.F / 2) ** 2
            k = np.arange(n + 1)
            L = binom.pmf(k[None, :], n, theta[:, None])           # grid x k
            post = self.f[:, None] * L
            m = (post * PG[:, None]).sum(0) / post.sum(0)          # posterior mean per k
            self._cache[n] = L @ m
        return self._cache[n]

    def w(self, c, n):
        cv = self.curve(n)
        out = np.interp(c, PG, cv)
        return np.where(c <= 1e-12, 0.0, np.where(c >= 1 - 1e-12, 1.0, out))


def weighted_coords(X, P, W):
    """g, l, pi+, pi-, s from rank-dependent decision weights. s stays on the raw probabilities."""
    g, l, pp, pm = (np.zeros(len(X)) for _ in range(4))
    for sign in (1, -1):
        Xs = np.where(sign * X > 0, np.abs(X), 0.0)
        Ps = np.where(sign * X > 0, P, 0.0)
        o = np.argsort(-Xs, axis=1)
        Xo, Po = np.take_along_axis(Xs, o, 1), np.take_along_axis(Ps, o, 1)
        cum = np.cumsum(Po, 1)
        dec = np.where(Po > 0, W(cum) - W(cum - Po), 0.0)
        if sign > 0:
            g, pp = (dec * Xo).sum(1), dec.sum(1)
        else:
            l, pm = (dec * Xo).sum(1), dec.sum(1)
    return g, l, pp, pm, M.sd(X, P)


def cost_pair(th, cA, cB, norm="L2", q=None):
    """GDT-S cost with a Minkowski exponent: (sum_k (sqrt(w_k) |Delta_k|)^q)^(1/q) + beta [pi- > 0].
    q = 2 is GDT-S as registered. q = 1 makes the cost difference of two options linear in their
    coordinates, an additive value model: the menu reference cancels."""
    if norm == "L2":
        return M.gdts_cost_pair(th, cA, cB)
    w = np.exp(np.asarray(th[:5]))
    beta = np.exp(th[5])
    (gA, lA, ppA, pmA, sA), (gB, lB, ppB, pmB, sB) = cA, cB
    ref = (np.maximum(gA, gB), np.minimum(lA, lB), np.maximum(ppA, ppB), np.minimum(pmA, pmB), 0.0)
    qq = 1.0 if norm == "L1" else q

    def cost(g, l, pp, pm, s):
        d = [np.sqrt(w[0]) * (ref[0] - g), np.sqrt(w[1]) * (l - ref[1]), np.sqrt(w[2]) * (ref[2] - pp),
             np.sqrt(w[3]) * (pm - ref[3]), np.sqrt(w[4]) * s]
        tot = sum(np.abs(x) ** qq for x in d)
        return (tot + 1e-300) ** (1 / qq) + beta * (pm > 0)
    return cost(gA, lA, ppA, pmA, sA), cost(gB, lB, ppB, pmB, sB)


def make_gdts(reader, prior=None, curved=False, norm="L2"):
    """GDT-S logit. Parameters: six GDT-S, then the reader's, then curvature (`curved`: 0, 1 shared
    exponent, or 2 = separate exponents for gains and losses), then q if norm == "Lq".
    For 'eff' the capacity n is fixed per call through `n`, not optimised (it is an integer)."""
    curved = int(curved)
    def logit(th, pr, n=None):
        if reader == "lin":
            W = lambda c: c
        elif reader == "fr":
            W = w_fr
        elif reader == "llo":
            W = lambda c: w_llo(c, th[6:8])
        elif reader == "eff":
            W = lambda c: prior.w(c, n)
        XA, PA, XB, PB = pr.coded("share")
        i = 6 + N_READER[reader]
        if curved:                                   # diminishing sensitivity on share magnitudes
            a = np.exp(th[i])
            b = np.exp(th[i + 1]) if curved == 2 else a
            bend = lambda X: np.where(X >= 0, np.abs(X) ** a, -np.abs(X) ** b)
            XA, XB = bend(XA), bend(XB)
        q = np.exp(th[i + curved]) if norm == "Lq" else None
        cA, cB = cost_pair(th[:6], weighted_coords(XA, PA, W), weighted_coords(XB, PB, W), norm, q)
        return cA - cB
    return logit


N_READER = {"lin": 0, "fr": 0, "llo": 2, "eff": 0}
