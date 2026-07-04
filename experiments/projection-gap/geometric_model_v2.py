#!/usr/bin/env python3
"""Geometric decision model v2 — FIXED-temperature choice rule (Part III redesign).

v1 (`geometric_model.py`, frozen at prereg-v1) used a cost-dependent temperature
T(Δ)=max(0.5, 0.24·Δ^2.13). The six-model panel falsified two of its predictions
(peaked dose-response; ~5× magnitude under-shoot), and choice-rule fuzzing on
CPC18 traced both to the super-linear exponent α=2.13 (an artifact of calibrating
on aggregate targets; individual data wants α≈0.42, i.e. near-flat). See
`../datasets/RESULTS_choice_rule.md`.

v2 keeps the SAME active metric Σ (which the panel *confirmed* for the signs) and
replaces the temperature with a single FIXED temperature. Consequences:
  - sign(Δ) is unchanged (T-invariant) — the confirmed primary claim carries over;
  - the dose-response is now MONOTONE (v1 predicted an inverted-U that was rejected);
  - magnitude is a single per-population scale (T), fit to data, not throttled.

Σ is frozen from the TCSS calibration and confirmed by the panel; only the choice
rule changes. This module backs prereg-v2 (re-derive → re-register → re-run).
"""
from __future__ import annotations

import math

from geometric_model import SIGMA2, DIM_NAMES, ACTIVE, cost  # unchanged, panel-confirmed

# Fixed reference temperature (the redesign). Sign predictions are T-invariant;
# magnitude scales with T and is a single fitted per-population parameter. T_FIXED
# is the reference at which illustrative magnitudes are reported.
T_FIXED = 1.0


def temperature(c_a: float = 0.0, c_b: float = 0.0) -> float:
    """Fixed temperature (no cost dependence) — the v2 redesign."""
    return T_FIXED


def p_choose_a(delta_a: dict[int, float], delta_b: dict[int, float]) -> float:
    c_a, c_b = cost(delta_a), cost(delta_b)
    z_a, z_b = -c_a / T_FIXED, -c_b / T_FIXED
    m = max(z_a, z_b)
    ea, eb = math.exp(z_a - m), math.exp(z_b - m)
    return ea / (ea + eb)


def predict_delta(delta_a_lo, delta_b_lo, delta_a_hi, delta_b_hi) -> dict:
    p_lo = p_choose_a(delta_a_lo, delta_b_lo)
    p_hi = p_choose_a(delta_a_hi, delta_b_hi)
    d = p_hi - p_lo
    return {"p_a_lo": p_lo, "p_a_hi": p_hi, "delta": d,
            "sign": (1 if d > 0 else (-1 if d < 0 else 0))}


if __name__ == "__main__":
    # sign parity with v1 (T-invariant), but dose is now monotone
    assert p_choose_a({6: 0.0}, {6: 5.0}) > 0.5
    assert abs(p_choose_a({1: 100.0}, {1: 0.0}) - 0.5) < 1e-12  # d1 inactive
    print("geometric_model_v2 (fixed T) self-test OK")
