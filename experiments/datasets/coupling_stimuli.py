#!/usr/bin/env python3
"""Frozen stimulus DESIGN for prereg-coupling-angle-v1 (the encoded instrument).

Emits the deterministic per-block choice designs the confirmatory analysis consumes: for each of the
five sub-blocks (risk_gain, risk_loss, social_adv, social_dis, patience), K binary choices, each a pair
of options encoded as 2-D shortfalls (d1, d2) >= 0 in that block's plane. Options are laid on a grid
of *tradeoff ratios* so the block's angle is well identified (the two coordinates trade off across the
menu), with a small seeded jitter. This is the Level-1 frozen design; the human-facing menu
instantiation (mapping each encoded (d1,d2) to displayed lottery outcomes / allocation amounts / delays
via the Part II encoding) is a Level-2 step performed before data collection.

  block planes (coordinate 1, coordinate 2):
    risk_gain / risk_loss : (EV shortfall, dispersion)          -- loss block negates outcomes
    social_adv / social_dis: (own-payoff shortfall, other's shortfall) -- adv: s>o, dis: s<o
    patience              : (sooner-amount shortfall, delay cost)

  python coupling_stimuli.py            # write coupling_stimuli.json + print a summary
"""
from __future__ import annotations

import json

import numpy as np

BLOCKS = ["risk_gain", "risk_loss", "social_adv", "social_dis", "patience"]


def _block_design(K, rng):
    """K option-pairs spanning the 2-D tradeoff plane; option A trades coord-1 for coord-2 vs B."""
    ratios = np.tan(np.linspace(0.15, np.pi / 2 - 0.15, K))  # spanning tradeoff slopes -> identifies angle
    mag = rng.uniform(0.4, 1.0, K)  # option magnitude
    jit = rng.uniform(0.9, 1.1, (K, 4))
    # A: low coord-1 shortfall, higher coord-2; B: higher coord-1, low coord-2 (the tradeoff)
    dA = np.column_stack([mag / (1 + ratios) * jit[:, 0], mag * ratios / (1 + ratios) * jit[:, 1]])
    dB = np.column_stack([mag * ratios / (1 + ratios) * jit[:, 2], mag / (1 + ratios) * jit[:, 3]])
    return np.round(dA, 4), np.round(dB, 4)


def generate(k_r=32, k_s=32, k_p=16, seed=20260707):
    rng = np.random.default_rng(seed)
    counts = {"risk_gain": k_r // 2, "risk_loss": k_r // 2, "social_adv": k_s // 2,
              "social_dis": k_s // 2, "patience": k_p}
    designs = {}
    for b in BLOCKS:
        dA, dB = _block_design(counts[b], rng)
        designs[b] = {"dA": dA.tolist(), "dB": dB.tolist(), "K": counts[b]}
    return {
        "prereg": "prereg-coupling-angle-v1",
        "seed": seed,
        "K_R": k_r, "K_S": k_s, "K_P": k_p,
        "planes": {
            "risk_gain": ["EV_shortfall", "dispersion"],
            "risk_loss": ["EV_shortfall", "dispersion", "outcomes_negated"],
            "social_adv": ["own_shortfall", "other_shortfall", "s>o"],
            "social_dis": ["own_shortfall", "other_shortfall", "s<o"],
            "patience": ["sooner_amount_shortfall", "delay_cost"],
        },
        "level2_note": "human-facing menus derived from these encoded (d1,d2) via the Part II encoding "
                       "before data collection; balanced gain/loss and adv/dis by construction.",
        "designs": designs,
    }


def load_designs(path="coupling_stimuli.json"):
    """Load and return {block: (dA, dB)} numpy arrays for the confirmatory analysis."""
    spec = json.load(open(path, encoding="utf-8"))
    return {b: (np.array(d["dA"]), np.array(d["dB"])) for b, d in spec["designs"].items()}


def main():
    spec = generate()
    json.dump(spec, open("coupling_stimuli.json", "w", encoding="utf-8"), indent=2)
    print("wrote coupling_stimuli.json")
    print(f"  K_R={spec['K_R']} (gain {spec['designs']['risk_gain']['K']} + loss "
          f"{spec['designs']['risk_loss']['K']}), K_S={spec['K_S']} (adv/dis balanced), K_P={spec['K_P']}")
    print(f"  blocks: {list(spec['designs'])}  |  seed={spec['seed']}")


if __name__ == "__main__":
    main()
