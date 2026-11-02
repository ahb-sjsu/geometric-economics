"""Choice models for the correlation-attitude design (DESIGN.md).

Shortfalls enter in units of 10 points. Every model returns a value per option, higher is better, and
P(choose option 0, the left one) = sigmoid(logit). All models carry a left-side bias.

  GEO    late contraction under a full Mahalanobis metric: V = -sum_s p_s C_s^kappa,
         C_s = sqrt(d_s' P d_s), P = L L' with L = [[e^l1, 0], [l21, e^l2]].
  EARLY  the order the earlier tests used: V = -C(sum_s p_s d_s)^kappa, the metric on the mean.
  RDU    additive value per outcome, v = -(a^eta + lam b^eta), even-odds lotteries weighted
         pi on the better outcome: rank-dependent, late contraction, no metric.
  CAG    expected utility with a concave aggregator: U = -(a + lam b + 1)^rho / rho.

Fitting is maximum a posteriori with fixed weak Gaussian priors on the free parameters.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize


def arrays(trials):
    """p, a, b of shape (trials, 2 options, 2 outcomes); a sure option repeats its outcome at p = 0."""
    T = len(trials)
    p, a, b = np.zeros((T, 2, 2)), np.zeros((T, 2, 2)), np.zeros((T, 2, 2))
    for t, tr in enumerate(trials):
        for o, option in enumerate(tr["options"]):
            outs = option if len(option) == 2 else [option[0], [0.0, option[0][1], option[0][2]]]
            for s, (ps, sa, sb) in enumerate(outs):
                p[t, o, s], a[t, o, s], b[t, o, s] = ps, sa / 10.0, sb / 10.0
    return p, a, b


def metric(th):
    e1 = np.exp(th[0])
    return e1 * e1, e1 * th[1], th[1] * th[1] + np.exp(2 * th[2])


def _cost(P, a, b):
    P11, P12, P22 = P
    return np.sqrt(np.maximum(P11 * a * a + 2 * P12 * a * b + P22 * b * b, 1e-12))


def v_geo(th, p, a, b):
    return -(p * _cost(metric(th), a, b) ** th[3]).sum(-1)


def v_early(th, p, a, b):
    am, bm = (p * a).sum(-1), (p * b).sum(-1)
    return -(_cost(metric(th), am, bm) ** th[3])


def v_rdu(th, p, a, b):
    eta, lam, pi = np.exp(th[1]), np.exp(th[2]), 1.0 / (1.0 + np.exp(-th[3]))
    v = -(np.power(a, eta) + lam * np.power(b, eta))
    return np.where(p[..., 1] > 0, pi * v.max(-1) + (1 - pi) * v.min(-1), v[..., 0])


def v_cag(th, p, a, b):
    lam, rho = np.exp(th[1]), th[2]
    return -(p * (a + lam * b + 1.0) ** rho).sum(-1) / rho


@dataclass
class Model:
    name: str
    value: callable
    scaled: bool          # value scaled by exp(th[0]) (RDU, CAG); GEO and EARLY carry scale in P
    bounds: list
    mu: np.ndarray
    sd: np.ndarray
    start: np.ndarray

    def logit(self, th, p, a, b):
        v = self.value(th, p, a, b)
        d = v[:, 0] - v[:, 1]
        return (np.exp(th[0]) * d if self.scaled else d) + th[-1]


_geo = dict(bounds=[(-6, 6), (-20, 20), (-8, 6), (0.5, 4.0), (-4, 4)],
            mu=np.array([0.0, 0.0, -1.0, 1.5, 0.0]), sd=np.array([3.0, 5.0, 3.0, 1.5, 1.5]),
            start=np.array([-0.5, 0.0, -1.0, 1.2, 0.0]))
MODELS = {
    "GEO": Model("GEO", v_geo, False, **_geo),
    "EARLY": Model("EARLY", v_early, False, **_geo),
    "RDU": Model("RDU", v_rdu, True, bounds=[(-8, 6), (-1.6, 1.6), (-6, 2), (-4, 4), (-4, 4)],
                 mu=np.array([0.0, 0.0, -1.0, 0.0, 0.0]), sd=np.array([3.0, 0.7, 2.0, 1.5, 1.5]),
                 start=np.array([0.0, 0.0, -0.7, 0.0, 0.0])),
    "CAG": Model("CAG", v_cag, True, bounds=[(-12, 6), (-6, 2), (1.0, 6.0), (-4, 4)],
                 mu=np.array([-1.0, -1.0, 2.0, 0.0]), sd=np.array([4.0, 2.0, 2.0, 1.5]),
                 start=np.array([-1.0, -0.7, 2.0, 0.0])),
}


def neg_log_post(th, m, data, y):
    z = m.logit(th, *data)
    nll = (y * np.logaddexp(0.0, -z) + (1 - y) * np.logaddexp(0.0, z)).sum()
    return nll + 0.5 * (((th - m.mu) / m.sd) ** 2).sum()


def fit(m, data, y, rng, starts=2):
    lo, hi = np.array([b[0] for b in m.bounds]), np.array([b[1] for b in m.bounds])
    best = None
    for k in range(starts):
        x0 = m.start if k == 0 else np.clip(m.start + rng.normal(0, 0.7, len(m.start)), lo, hi)
        r = minimize(neg_log_post, x0, args=(m, data, y), method="L-BFGS-B", bounds=m.bounds)
        if best is None or r.fun < best.fun:
            best = r
    return best.x


def log_loss(m, th, data, y):
    z = m.logit(th, *data)
    return float((y * np.logaddexp(0.0, -z) + (1 - y) * np.logaddexp(0.0, z)).mean())


def p_left(m, th, data):
    return 1.0 / (1.0 + np.exp(-m.logit(th, *data)))
