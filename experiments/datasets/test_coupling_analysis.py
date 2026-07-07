#!/usr/bin/env python3
"""Validate the frozen confirmatory analysis: it must detect a reflection-structured coupling when
present, control false positives when absent, and keep its null controls ~0. Run: python test_...py"""
import numpy as np

from coupling_analysis import analyze, simulate_study


def _run(coupled, seed):
    rng = np.random.default_rng(seed)
    ch, de = simulate_study(N=400, K=32, load=0.30, idio=0.15, rng=rng, coupled=coupled)
    return analyze(ch, de, np.random.default_rng(seed + 1))


def test_detects_coupling_when_present():
    r = _run(True, 0)
    lad = r["ladder"]
    assert lad["aversion"][1] > 0.10, "aversion contrast must PASS (CI lower > 0.10) under coupling"
    assert lad["joint_factor"][1] > 0.10, "joint factor must PASS under coupling"
    # rank-0 scalar is BLIND under reflection -> must NOT pass (and that is not a falsification)
    assert lad["scalar"][1] <= 0.10, "scalar is a rank-0 shadow; should be blind here"


def test_controls_false_positive_when_absent():
    for seed in (10, 11, 12):
        r = _run(False, seed)
        for rung in ("scalar", "aversion", "joint_factor"):
            assert r["ladder"][rung][1] <= 0.10, f"{rung} false-positive under NO coupling (seed {seed})"


def test_null_controls_are_null():
    r = _run(True, 0)
    assert abs(r["nulls"]["permutation_null"]) < 0.10, "subject-permutation null must be ~0"
    assert abs(r["nulls"]["magnitude_channel"]) < 0.15, "magnitude channel must be weak (Keep-the-Angle)"


def test_reliability_reported():
    r = _run(True, 0)
    for b in ("risk_gain", "risk_loss", "social_adv", "social_dis"):
        assert 0.0 < r["reliability"][b] <= 1.0


if __name__ == "__main__":
    for fn in (test_detects_coupling_when_present, test_controls_false_positive_when_absent,
               test_null_controls_are_null, test_reliability_reported):
        fn()
        print("PASS", fn.__name__)
    print("all coupling-analysis tests passed")
