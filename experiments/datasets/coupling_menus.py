#!/usr/bin/env python3
"""Level 2 for prereg-coupling-angle-v1: human-facing menus from the frozen encoded design.

Maps each frozen encoded option (d1, d2) shortfall (`coupling_stimuli.json`) to the concrete stimulus a
subject sees, with a fixed, INVERTIBLE per-block encoding so that re-encoding the displayed values
recovers (d1, d2) — proving the menus instantiate exactly the frozen design. Because displayed values
are rounded to nice units, the confirmatory analysis scores the **re-encoded actual** design (what
subjects saw), reported here with its max drift from the frozen template. Level 2 is NOT part of the
Level-1 hash; it precedes data collection.

Encodings (all linear, invertible), money in USD:
  RISK   option = 50/50 gamble (a, b): EV=(a+b)/2, SD=|a-b|/2.  d1 = (EV_ref-EV)/S,  d2 = SD/S.
         gain: outcomes >= 0 ; loss: outcomes negated (losses from an endowment).
  SOCIAL option = (own s, other o).  adv region: s>=o ; dis region: s<=o.  d1=(own_ref-s)/S, d2=(oth_ref-o)/S.
  TIME   option = $m in t days.      d1 = (m_ref - m)/S,  d2 = t / T_days.

  python coupling_menus.py            # write coupling_menus.json, print sample + round-trip drift
"""
from __future__ import annotations

import json

import numpy as np

from coupling_stimuli import load_designs

S = 10.0  # dollar scale per unit shortfall
CFG = {  # per-block reference points (bases) so values land in a sensible online-study range
    "risk_gain": {"ev_ref": 20.0, "sign": +1},
    "risk_loss": {"ev_ref": 20.0, "sign": -1},
    "social_adv": {"own_ref": 25.0, "oth_ref": 15.0},  # s in [~16,25] > o in [~6,15] -> advantageous
    "social_dis": {"own_ref": 15.0, "oth_ref": 25.0},  # s < o -> disadvantageous
    "patience": {"m_ref": 25.0, "t_days": 60.0},
}
ROUND = 0.50  # display rounding (USD / days rounded to whole)


def _r(x, step=ROUND):
    return float(np.round(x / step) * step)


def option_to_human(block, d):
    """Encoded (d1,d2) -> displayed stimulus dict (rounded)."""
    d1, d2 = float(d[0]), float(d[1])
    c = CFG[block]
    if block.startswith("risk"):
        ev = c["ev_ref"] - d1 * S
        sd = d2 * S
        a, b = _r(ev + sd), _r(ev - sd)
        if c["sign"] < 0:
            a, b = -a, -b
        return {"kind": "gamble", "p": 0.5, "a": a, "b": b}
    if block.startswith("social"):
        return {"kind": "alloc", "own": _r(c["own_ref"] - d1 * S), "other": _r(c["oth_ref"] - d2 * S)}
    return {"kind": "delay", "amount": _r(c["m_ref"] - d1 * S), "days": _r(d2 * c["t_days"], 1.0)}


def human_to_encoded(block, h):
    """Displayed stimulus -> (d1,d2), the actual encoding subjects faced (inverse of the above)."""
    c = CFG[block]
    if block.startswith("risk"):
        a, b = (h["a"], h["b"]) if c["sign"] > 0 else (-h["a"], -h["b"])
        ev, sd = (a + b) / 2, abs(a - b) / 2
        return np.array([(c["ev_ref"] - ev) / S, sd / S])
    if block.startswith("social"):
        return np.array([(c["own_ref"] - h["own"]) / S, (c["oth_ref"] - h["other"]) / S])
    return np.array([(c["m_ref"] - h["amount"]) / S, h["days"] / c["t_days"]])


def render(block, hA, hB):
    """One-line subject-facing text for a choice pair."""
    def money(x):
        return f"lose ${abs(x):.2f}" if x < 0 else f"${x:.2f}"

    def g(h):
        if h["kind"] == "gamble":
            return f"50% chance {money(h['a'])}, 50% chance {money(h['b'])}"
        if h["kind"] == "alloc":
            return f"you get ${h['own']:.2f}, other gets ${h['other']:.2f}"
        return f"${h['amount']:.2f} in {int(h['days'])} days"
    return f"A: {g(hA)}   |   B: {g(hB)}"


def build():
    designs = load_designs()
    menus, max_drift = {}, 0.0
    for block, (dA, dB) in designs.items():
        rows = []
        for j in range(len(dA)):
            hA, hB = option_to_human(block, dA[j]), option_to_human(block, dB[j])
            eA, eB = human_to_encoded(block, hA), human_to_encoded(block, hB)
            max_drift = max(max_drift, float(np.abs(eA - dA[j]).max()), float(np.abs(eB - dB[j]).max()))
            rows.append({"A": hA, "B": hB, "text": render(block, hA, hB),
                         "encoded_A": eA.round(4).tolist(), "encoded_B": eB.round(4).tolist()})
        menus[block] = rows
    return menus, max_drift


def check_semantics(menus):
    """Domain/region invariants the menus must satisfy."""
    for r in menus["risk_gain"]:
        assert r["A"]["a"] >= 0 and r["A"]["b"] >= 0, "gain outcomes must be >= 0"
    for r in menus["risk_loss"]:
        assert r["A"]["a"] <= 0 and r["A"]["b"] <= 0, "loss outcomes must be <= 0"
    for r in menus["social_adv"]:
        assert r["A"]["own"] >= r["A"]["other"] and r["B"]["own"] >= r["B"]["other"], "adv: s>=o"
    for r in menus["social_dis"]:
        assert r["A"]["own"] <= r["A"]["other"] and r["B"]["own"] <= r["B"]["other"], "dis: s<=o"
    for r in menus["patience"]:
        assert r["A"]["days"] >= 0 and r["B"]["days"] >= 0, "delays >= 0"


def actual_designs(path="coupling_menus.json"):
    """{block: (dA, dB)} re-encoded from the displayed (rounded) menus — the design subjects ACTUALLY
    faced. The confirmatory analysis (`coupling_analysis.py`) scores with THIS, not the pre-rounding
    template, so the encoding matches the stimuli exactly."""
    menus = json.load(open(path, encoding="utf-8"))["menus"]
    return {b: (np.array([r["encoded_A"] for r in rows]), np.array([r["encoded_B"] for r in rows]))
            for b, rows in menus.items()}


def main():
    menus, drift = build()
    check_semantics(menus)
    out = {"prereg": "prereg-coupling-angle-v1", "level": 2, "usd_scale": S, "round": ROUND,
           "config": CFG, "max_encoding_drift_from_frozen": round(drift, 4), "menus": menus}
    json.dump(out, open("coupling_menus.json", "w", encoding="utf-8"), indent=2)
    print("wrote coupling_menus.json")
    print(f"  max encoding drift from frozen design (rounding): {drift:.4f}  (small = menus match the freeze)")
    print("  sample subject-facing choices:")
    for block in ("risk_gain", "risk_loss", "social_adv", "social_dis", "patience"):
        print(f"    [{block}] {menus[block][0]['text']}")


if __name__ == "__main__":
    main()
