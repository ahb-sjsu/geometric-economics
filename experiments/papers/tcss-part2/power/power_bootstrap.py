#!/usr/bin/env python3
"""prereg-dimensions-v1 §9.1 power protocol — parametric bootstrap.

Two committed calculations, both run BEFORE any fit to a dataset's outcomes:

  phase2_panel_power(delta, n_models=6, k=5, per_choice_se, n_choices)
      Power of the "sign in >= k/n_models models" test given a true per-model effect `delta`.
      A model "shows the sign" when its estimated per-model Delta (SE = per_choice_se/sqrt(n_choices))
      is on the correct side of 0 at one-sided alpha. Power = P(Binomial(n_models, p_detect) >= k).

  phase1_activation_power(delta_nll, n_choices, n_boot)
      Power to beat the d1-only model by the pre-registered margin (mean paired per-choice NLL
      improvement >= MARGIN) at a dataset's registered N, under assumed per-choice improvement
      `delta_nll` with paired-choice noise. Reported per module; < TARGET => exploratory (§9).

Deterministic (seeded); no dataset outcomes are read. Numbers go in the bundle as power/results.json.
"""
from __future__ import annotations

import argparse
import json

import numpy as np
from scipy import stats

TARGET = 0.80          # required power (§9.1)
MARGIN = 0.01          # ΔNLL/choice margin over d1-only (§2 activation, §9.1)
ALPHA = 0.05           # one-sided per-test (FDR applied across the family separately)


def phase2_panel_power(delta, per_choice_se, n_choices, n_models=6, k=5):
    """P(>= k of n_models show the correct sign)."""
    se = per_choice_se / np.sqrt(n_choices)
    p_detect = float(stats.norm.cdf(delta / se - stats.norm.ppf(1 - ALPHA)))
    power = float(1 - stats.binom.cdf(k - 1, n_models, p_detect))
    return {"p_detect": p_detect, "power": power, "adequate": power >= TARGET}


def phase1_activation_power(delta_nll, sd_nll, n_choices, n_boot=5000, seed=0):
    """Power that the mean paired per-choice NLL improvement exceeds MARGIN at N=n_choices."""
    rng = np.random.default_rng(seed)
    crit = MARGIN
    hits = 0
    for _ in range(n_boot):
        sample = rng.normal(delta_nll, sd_nll, n_choices)
        # one-sided test H0: mean <= MARGIN
        t = (sample.mean() - crit) / (sample.std(ddof=1) / np.sqrt(n_choices))
        if t > stats.t.ppf(1 - ALPHA, n_choices - 1):
            hits += 1
    power = hits / n_boot
    return {"power": power, "adequate": power >= TARGET}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modules", default="modules.json",
                    help="per-module {name, phase, delta, per_choice_se|sd_nll, n} — assumed effects "
                         "and REGISTERED N only; never outcomes")
    ap.add_argument("--out", default="results.json")
    a = ap.parse_args()
    mods = json.load(open(a.modules, encoding="utf-8"))
    out = {}
    for m in mods:
        if m["phase"] == 2:
            out[m["name"]] = phase2_panel_power(m["delta"], m["per_choice_se"], m["n"])
        else:
            out[m["name"]] = phase1_activation_power(m["delta"], m["sd_nll"], m["n"])
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=2)
    for k, v in out.items():
        print(f"{k}: power={v['power']:.3f} adequate={v['adequate']}")


if __name__ == "__main__":
    main()
