#!/usr/bin/env python3
"""Models of prereg-strata-v1, for binary choices between lotteries with any number of branches.

A problem is two options A and B, each given as branch arrays X (outcomes) and P (probabilities),
padded to a common width K with probability 0. Every model returns the logit of choosing B.

    GDT2   Part II's geometric model: distance from (best EV, zero SD), on payoffs in the corpus unit.
    GDTS   the stratified encoding, Section 2, on share-coded payoffs.
    GDTC   the budgeted consumer, Section 2b: GDTS on decoded readings.
    CPT    cumulative prospect theory (rank- and sign-dependent), coding "unit" or "share".
    EV     logit on the EV difference.  RUM  logit linear in dEV, dSD, plus an intercept.

On two-branch problems GDT2 and CPT reproduce `experiments/datasets/fit_transfer.py` (`selfcheck`).
Parameters are passed on a free scale and mapped to their domain inside each model.
"""
from __future__ import annotations

import numpy as np
from scipy.special import ndtri

EPS = 1e-9


# ---------------------------------------------------------------- problems
class Problems:
    """Branch arrays for a set of binary problems, with the two codings."""

    def __init__(self, XA, PA, XB, PB, unit=None):
        self.XA, self.PA, self.XB, self.PB = (np.asarray(a, float) for a in (XA, PA, XB, PB))
        self.stake = np.maximum(np.abs(self.XA).max(1), np.abs(self.XB).max(1))
        self.stake = np.where(self.stake > 0, self.stake, 1.0)
        evs = np.r_[ev(self.XA, self.PA), ev(self.XB, self.PB)]
        self.unit = float(np.std(evs)) if unit is None else unit

    def coded(self, coding):
        s = self.stake[:, None] if coding == "share" else self.unit
        return self.XA / s, self.PA, self.XB / s, self.PB

    def subset(self, m):
        out = Problems.__new__(Problems)
        out.XA, out.PA, out.XB, out.PB = self.XA[m], self.PA[m], self.XB[m], self.PB[m]
        out.stake, out.unit = self.stake[m], self.unit
        return out

    def __len__(self):
        return len(self.XA)


def ev(X, P):
    return (X * P).sum(1)


def sd(X, P):
    m = ev(X, P)
    return np.sqrt(np.maximum((P * (X - m[:, None]) ** 2).sum(1), 0.0))


# ---------------------------------------------------------------- baselines
def logit_ev(th, pr):
    XA, PA, XB, PB = pr.coded("unit")
    return np.exp(th[0]) * (ev(XB, PB) - ev(XA, PA))


def logit_rum(th, pr):
    XA, PA, XB, PB = pr.coded("unit")
    return th[0] + th[1] * (ev(XB, PB) - ev(XA, PA)) + th[2] * (sd(XB, PB) - sd(XA, PA))


def logit_gdt2(th, pr):
    """fit_transfer.pred_geom with amb = 0: cost = sqrt(((EVmax-EV)/s_ev)^2 + (SD/s_sd)^2)."""
    a, b = np.exp(th[0]), np.exp(th[1])          # 1/(s_ev T), 1/(s_sd T)
    XA, PA, XB, PB = pr.coded("unit")
    eA, eB, sA, sB = ev(XA, PA), ev(XB, PB), sd(XA, PA), sd(XB, PB)
    m = np.maximum(eA, eB)
    cA = np.sqrt((a * (m - eA)) ** 2 + (b * sA) ** 2)
    cB = np.sqrt((a * (m - eB)) ** 2 + (b * sB) ** 2)
    return cA - cB


# ---------------------------------------------------------------- CPT
def _w(p, g):
    p = np.clip(p, 0.0, 1.0)
    return p ** g / (p ** g + (1 - p) ** g) ** (1.0 / g)


def cpt_value(X, P, a, b, lam, g):
    """Rank-dependent CPT with one weighting exponent for gains and losses (as fit_transfer)."""
    V = np.zeros(len(X))
    for sign in (1, -1):
        Xs = np.where(sign * X > 0, np.abs(X), 0.0)
        Ps = np.where(sign * X > 0, P, 0.0)
        order = np.argsort(-Xs, axis=1)                         # most extreme first
        Xo = np.take_along_axis(Xs, order, 1)
        Po = np.take_along_axis(Ps, order, 1)
        cum = np.cumsum(Po, 1)
        dec = _w(cum, g) - _w(cum - Po, g)
        v = Xo ** a if sign > 0 else -lam * Xo ** b
        V += (dec * np.where(Po > 0, v, 0.0)).sum(1)
    return V


def make_cpt(coding):
    def logit_cpt(th, pr):
        a, b, lam = np.exp(th[0]), np.exp(th[1]), np.exp(th[2])
        g = 0.28 + 1.72 / (1 + np.exp(-th[3]))                 # (0.28, 2.0), as fit_transfer's clip
        XA, PA, XB, PB = pr.coded(coding)
        return (cpt_value(XB, PB, a, b, lam, g) - cpt_value(XA, PA, a, b, lam, g)) * np.exp(th[4])
    return logit_cpt


# ---------------------------------------------------------------- GDT-S
def strata_coords(X, P):
    """g, l, pi+, pi-, s for share-coded branches."""
    g = (P * np.maximum(X, 0)).sum(1)
    l = (P * np.maximum(-X, 0)).sum(1)
    pp = (P * (X > 0)).sum(1)
    pm = (P * (X < 0)).sum(1)
    return g, l, pp, pm, sd(X, P)


def gdts_cost_pair(th, cA, cB):
    w = np.exp(th[:5])
    beta = np.exp(th[5])
    (gA, lA, ppA, pmA, sA), (gB, lB, ppB, pmB, sB) = cA, cB
    rg, rl, rp, rm = np.maximum(gA, gB), np.minimum(lA, lB), np.maximum(ppA, ppB), np.minimum(pmA, pmB)

    def cost(g, l, pp, pm, s):
        return (np.sqrt(w[0] * (rg - g) ** 2 + w[1] * (l - rl) ** 2 + w[2] * (rp - pp) ** 2
                        + w[3] * (pm - rm) ** 2 + w[4] * s ** 2) + beta * (pm > 0))
    return cost(gA, lA, ppA, pmA, sA), cost(gB, lB, ppB, pmB, sB)


def logit_gdts(th, pr):
    XA, PA, XB, PB = pr.coded("share")
    cA, cB = gdts_cost_pair(th, strata_coords(XA, PA), strata_coords(XB, PB))
    return cA - cB


# ---------------------------------------------------------------- GDT-C
class Environment:
    """The efficient code for one corpus: empirical distributions of share magnitudes (log) and
    branch probabilities (log-odds) over its stimuli. Zero outcomes and probabilities 0 or 1 are
    boundaries of the strata and are read exactly, so they are not in the code."""

    def __init__(self, pr: Problems, grid=200):
        X = np.r_[pr.coded("share")[0], pr.coded("share")[2]]
        P = np.r_[pr.PA, pr.PB]
        live = P > 0
        mag = np.log(np.abs(X[live & (X != 0)]))
        prob = P[live & (P < 1)]
        lo = np.log(prob) - np.log1p(-prob)
        self.mag = self._code(mag, grid)
        self.prob = self._code(lo, grid)
        self.n_mag, self.n_prob = int(mag.size), int(lo.size)

    @staticmethod
    def _code(v, grid):
        if v.size == 0:
            return None
        qs = np.quantile(v, np.linspace(0, 1, grid))
        support = np.unique(qs)
        # prior weights from the empirical distribution on the support
        idx = np.clip(np.searchsorted(support, v), 0, len(support) - 1)
        w = np.bincount(idx, minlength=len(support)).astype(float) + 1e-3
        w /= w.sum()
        cdf = np.clip(np.cumsum(w) - w / 2, 0.005, 0.995)
        return support, w, ndtri(cdf)

    @staticmethod
    def decode(code, v, sigma, eps):
        """Posterior mean of v given a noisy probit-rank reading. v: array, eps: matching N(0,1)."""
        support, w, u_support = code
        u = np.interp(v, support, u_support)                    # encoder: probit of the rank
        r = u + sigma * eps
        ll = -0.5 * ((r[..., None] - u_support) / sigma) ** 2
        ll -= ll.max(-1, keepdims=True)
        post = w * np.exp(ll)
        return (post * support).sum(-1) / post.sum(-1)


def allocate(budget_bits, a_mag, a_prob):
    """Reverse water-filling of a budget over two unit-variance readings, weighted by importance.

    Minimise a_mag D_mag + a_prob D_prob subject to sum 0.5 log2(1/D_k) = budget, D_k <= 1.
    Returns the reading-noise sigma for each, from D = sigma^2 / (1 + sigma^2).
    """
    a = np.array([a_mag, a_prob])
    lo_t, hi_t = 1e-12, a.max()
    for _ in range(200):
        t = np.sqrt(lo_t * hi_t)
        D = np.minimum(1.0, t / a)
        bits = 0.5 * np.log2(1.0 / D).sum()
        lo_t, hi_t = (t, hi_t) if bits > budget_bits else (lo_t, t)
    D = np.clip(np.minimum(1.0, t / a), 1e-9, 1 - 1e-9)
    return np.sqrt(D / (1 - D))


def make_gdtc(env: Environment, n_draw=32, seed=20261031):
    def logit_gdtc(th, pr):
        w = np.exp(th[:5])
        sig_mag, sig_prob = allocate(np.exp(th[6]), w[0] + w[1], w[2] + w[3])
        XA, PA, XB, PB = pr.coded("share")
        rng = np.random.default_rng(seed)
        out = np.zeros(len(pr))
        for _ in range(n_draw):
            dec = []
            for X, P in ((XA, PA), (XB, PB)):
                Xd, Pd = X.copy(), P.copy()
                m = (X != 0) & (P > 0)
                if env.mag is not None and m.any():
                    e = rng.standard_normal(m.sum())
                    Xd[m] = np.sign(X[m]) * np.exp(env.decode(env.mag, np.log(np.abs(X[m])), sig_mag, e))
                q = (P > 0) & (P < 1)
                if env.prob is not None and q.any():
                    lo = np.log(P[q]) - np.log1p(-P[q])
                    e = rng.standard_normal(q.sum())
                    d = env.decode(env.prob, lo, sig_prob, e)
                    Pd[q] = 1 / (1 + np.exp(-d))
                    Pd = Pd / Pd.sum(1, keepdims=True)
                dec.append(strata_coords(Xd, Pd))
            cA, cB = gdts_cost_pair(th[:6], dec[0], dec[1])
            out += 1 / (1 + np.exp(-(cA - cB)))
        p = np.clip(out / n_draw, 1e-9, 1 - 1e-9)
        return np.log(p) - np.log1p(-p)
    return logit_gdtc


X0 = {"EV": [0.0], "RUM": [0.0, 0.5, -0.1], "GDT2": [0.0, -1.0],
      "GDTS": [0.0, 0.0, 0.0, 0.0, 0.0, -2.0], "GDTC": [0.0, 0.0, 0.0, 0.0, 0.0, -2.0, 1.0],
      "CPT_unit": [np.log(0.88), np.log(0.88), np.log(2.25), 0.0, 0.0],
      "CPT_share": [np.log(0.88), np.log(0.88), np.log(2.25), 0.0, 1.0]}
