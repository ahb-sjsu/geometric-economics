#!/usr/bin/env python3
"""Freeze every model of Part II's CPC18 comparison by fitting it on all 270 CPC18 games.

The models and the fitter are IMPORTED from `experiments/datasets/fit_transfer.py`,
the code behind Part II's CPC18 table, and are not restated. CPC18 has been used
before; nothing from Psych-101 is read here. The output, `frozen_cpc18.json`, is in
the sealed bundle, so the parameters carried to Psych-101 are fixed before any
Psych-101 choice is scored.

CPT_TK92 is cumulative prospect theory at Tversky and Kahneman's 1992 estimates
(alpha = beta = 0.88, lambda = 2.25, gamma = 0.61) with only its temperature fit on
CPC18. `fit_transfer.pred_cpt` has one weighting exponent for gains and losses, so
the 1992 loss exponent (0.69) is not represented. That is stated in the registration.

    python freeze_cpc18.py     # on Atlas
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.join(HERE, "..", "..", "datasets")
sys.path.insert(0, DATASETS)
import cpc18  # noqa: E402
from fit_transfer import MODELS, fit, evaluate, pred_cpt, _nll  # noqa: E402

TK92 = [0.88, 0.88, 2.25, 0.61]


PAYOFF_COLS = ["evA", "evB", "sdA", "sdB", "d_ev", "d_sd", "_Ha", "_La", "_Hb", "_Lb"]


def cpc18_frame():
    """CPC18 games with payoffs in the common unit: divided by the SD of option EVs over games.

    The same unit is applied to the new corpus from its own stimuli. Without it, CPT's
    unequal gain and loss curvature makes "frozen CPT" depend on an arbitrary currency
    (rehearsal round 2 failed on exactly that).
    """
    df = cpc18.load_description()
    raw = pd.read_csv(cpc18.RAW, usecols=["GameID", "Ha", "pHa", "La", "Hb", "pHb", "Lb"]).groupby("GameID").first()
    df = df.merge(raw.rename(columns=lambda c: "_" + c).reset_index(), on="GameID")
    unit = float(np.std(np.r_[df["evA"], df["evB"]]))
    df[PAYOFF_COLS] = df[PAYOFF_COLS] / unit
    return df, unit


def main():
    df, unit = cpc18_frame()
    out = {"source": "CPC18 description choices (Trial 1), all games", "payoff_unit": unit,
           "n_games": int(len(df)),
           "n_choices": int(df["n"].sum()), "models": {}}
    for name, (fn, x0) in MODELS.items():
        theta = [float(t) for t in fit(fn, x0, df)]
        out["models"][name] = {"theta": theta, "in_sample": evaluate(fn, theta, df)}

    def nll_T(logT):
        return _nll(pred_cpt(TK92 + [10 ** logT], df), df["brate"].to_numpy(), df["n"].to_numpy())
    r = minimize_scalar(nll_T, bounds=(-3, 4), method="bounded")
    theta = TK92 + [float(10 ** r.x)]
    out["models"]["CPT_TK92"] = {"theta": theta, "in_sample": evaluate(pred_cpt, theta, df)}
    with open(os.path.join(HERE, "frozen_cpc18.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
