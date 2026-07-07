#!/usr/bin/env python3
"""Validate Level-2 menus: they instantiate the frozen encoded design (small round-trip drift) and
satisfy the domain/region invariants. Run: python test_coupling_menus.py"""
import numpy as np

from coupling_menus import ROUND, build, check_semantics, human_to_encoded, option_to_human


def test_roundtrip_recovers_frozen_design():
    _, drift = build()
    # rounding to $0.50 induces at most ~ROUND/(2*S) = 0.025 drift in each encoded coordinate
    assert drift <= 0.05, f"human menus must re-encode close to the frozen design (drift {drift})"


def test_single_option_roundtrip_is_invertible_pre_rounding():
    # with no rounding the map is exact
    import coupling_menus as m
    old = m.ROUND
    m.ROUND = 1e-9
    try:
        for block in ("risk_gain", "risk_loss", "social_adv", "social_dis", "patience"):
            d = np.array([0.3, 0.6])
            back = human_to_encoded(block, option_to_human(block, d))
            assert np.abs(back - d).max() < 1e-6, f"{block} encoding not invertible"
    finally:
        m.ROUND = old


def test_domain_and_region_semantics():
    menus, _ = build()
    check_semantics(menus)  # raises on any violation
    # every block has the expected number of choices and both options rendered
    for block, rows in menus.items():
        assert len(rows) >= 8 and all("text" in r for r in rows)


def test_display_rounding_units():
    menus, _ = build()
    for r in menus["risk_gain"]:
        assert abs(round(r["A"]["a"] / ROUND) * ROUND - r["A"]["a"]) < 1e-9


if __name__ == "__main__":
    for fn in (test_roundtrip_recovers_frozen_design,
               test_single_option_roundtrip_is_invertible_pre_rounding,
               test_domain_and_region_semantics, test_display_rounding_units):
        fn()
        print("PASS", fn.__name__)
    print("all coupling-menus tests passed")
