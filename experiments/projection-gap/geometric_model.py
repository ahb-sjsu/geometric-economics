#!/usr/bin/env python3
"""Frozen geometric decision model — TCSS calibration (revised_manuscript_v2).

This module is the *pre-registered* model. The constants below are the published
calibration and MUST NOT be re-fit for the projection-gap experiment: the whole
point is a no-refit out-of-sample prediction. Any change here invalidates the
pre-registration hash.

Model (manuscript Eqs. mahalanobis_diag / softmax / temperature):
    cost c(Δa)   = sqrt( sum_k Δa_k^2 / sigma_k^2 )          # diagonal Mahalanobis
    T(Δ)         = max(T_floor, T_base * Δ^T_alpha),  Δ=|c_A-c_B|
    P(A)         = exp(-c_A/T) / (exp(-c_A/T)+exp(-c_B/T))

Active dimensions (1-indexed as in the paper): d6 Social Impact, d7 Virtue/Identity,
d9 Epistemic Status. All other dimensions are inactive (sigma^2 -> inf => zero cost),
including the monetary dimension d1 (stake-scaling-invariance corollary).
"""
from __future__ import annotations

import math

# ---- FROZEN calibration constants (TCSS revised_manuscript_v2) ----------------
# 1-indexed dimension -> variance. Inactive dims are omitted (sigma^2 -> inf).
SIGMA2 = {6: 78.26, 7: 32.28, 9: 0.013}  # d6 Social Impact, d7 Virtue/Identity, d9 Epistemic Status
T_BASE = 0.24
T_ALPHA = 2.13
T_FLOOR = 0.5
DIM = 9
ACTIVE = tuple(sorted(SIGMA2))  # (6, 7, 9)

# Human-readable coordinate names (1-indexed) for reporting.
DIM_NAMES = {
    1: "Monetary", 2: "Rights", 3: "Fairness", 4: "Autonomy", 5: "Privacy/Trust",
    6: "Social Impact", 7: "Virtue/Identity", 8: "Legitimacy", 9: "Epistemic Status",
}


def cost(delta: dict[int, float]) -> float:
    """Diagonal Mahalanobis cost of a 9-D displacement (1-indexed dict; missing=0).

    Only active dimensions contribute; movement on inactive dims is free.
    """
    s = 0.0
    for k, s2 in SIGMA2.items():
        d = float(delta.get(k, 0.0))
        s += (d * d) / s2
    return math.sqrt(s)


def temperature(c_a: float, c_b: float) -> float:
    """Cost-dependent temperature T(Δ)=max(T_floor, T_base*Δ^T_alpha), Δ=|c_A-c_B|."""
    gap = abs(c_a - c_b)
    return max(T_FLOOR, T_BASE * (gap ** T_ALPHA))


def p_choose_a(delta_a: dict[int, float], delta_b: dict[int, float]) -> float:
    """P(choose A) under the frozen model for two option displacements."""
    c_a, c_b = cost(delta_a), cost(delta_b)
    t = temperature(c_a, c_b)
    # numerically stable 2-way softmax over -c/T
    z_a, z_b = -c_a / t, -c_b / t
    m = max(z_a, z_b)
    ea, eb = math.exp(z_a - m), math.exp(z_b - m)
    return ea / (ea + eb)


def predict_delta(
    delta_a_lo: dict[int, float], delta_b_lo: dict[int, float],
    delta_a_hi: dict[int, float], delta_b_hi: dict[int, float],
) -> dict[str, float]:
    """No-refit prediction for a projection-gap contrast.

    lo/hi are the two poles of the manipulated coordinate; A/B are the two options.
    Returns P(A) at each pole and the signed gap Δ = P(A|hi) - P(A|lo).
    Scalar theories (money/lottery unchanged across poles) are forced to predict
    Δ = 0; this model predicts Δ from the frozen Σ, T.
    """
    p_lo = p_choose_a(delta_a_lo, delta_b_lo)
    p_hi = p_choose_a(delta_a_hi, delta_b_hi)
    d = p_hi - p_lo
    return {
        "p_a_lo": p_lo,
        "p_a_hi": p_hi,
        "delta": d,
        "sign": (1 if d > 0 else (-1 if d < 0 else 0)),
    }


if __name__ == "__main__":  # sanity checks against hand-computed values
    # identical options -> P(A)=0.5, zero gap
    assert abs(p_choose_a({6: 1.0}, {6: 1.0}) - 0.5) < 1e-12
    # cheaper option (smaller active displacement) is preferred
    assert p_choose_a({6: 0.0}, {6: 5.0}) > 0.5
    # inactive dimension (d1 monetary) contributes zero cost -> no effect
    assert abs(p_choose_a({1: 100.0}, {1: 0.0}) - 0.5) < 1e-12
    # d9 (tiny sigma^2=0.013) is highly sensitive: small moves cost a lot
    c_small_d9 = cost({9: 0.1})
    c_big_d6 = cost({6: 0.1})
    assert c_small_d9 > c_big_d6  # d9 far more costly per unit than d6
    print("geometric_model self-test OK")
    print(f"  cost d9=0.1 -> {c_small_d9:.4f}; cost d6=0.1 -> {c_big_d6:.6f}")
