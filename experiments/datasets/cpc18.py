#!/usr/bin/env python3
"""CPC18 loader + gamble encoder for the job-A fit-and-transfer analysis.

Each option O = (H, pH, L, LotShape, LotNum): with prob pH draw from a "high"
sub-lottery of mean H (shape/LotNum), else get L. Per the CPC18 dictionary, H is
already the MEAN of the high part, so EV(O) = pH*H + (1-pH)*L exactly.

We compute per-option features (EV, SD, ambiguity, loss-domain) and aggregate the
DESCRIPTION choice (Trial==1, before any feedback/experience) to a per-GameID
B-rate -- the decision-from-description regime where prospect theory applies.

Variance uses the two-outcome approximation (H treated as a point); exact for
LotShape='-'/LotNum=1 (most games), a mild under-estimate of risk for multi-
outcome shapes -- flagged, refine later with the CPC generators.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "cpc18_raw.csv")


def _opt_stats(H, pH, L):
    """EV and SD of a two-branch gamble (H w.p. pH, L w.p. 1-pH)."""
    ev = pH * H + (1 - pH) * L
    var = pH * (H - ev) ** 2 + (1 - pH) * (L - ev) ** 2
    return ev, np.sqrt(np.maximum(var, 0.0))


def load_description(path: str = RAW) -> pd.DataFrame:
    """Return per-GameID description-choice table with encoded features.

    One row per GameID: B-rate over Trial==1 choices, plus option features and
    their B-minus-A differences.
    """
    cols = ["GameID", "Ha", "pHa", "La", "Hb", "pHb", "Lb", "Amb", "Trial", "B"]
    df = pd.read_csv(path, usecols=cols)
    d = df[df["Trial"] == 1].copy()  # description: first encounter, no feedback

    # per-GameID observed choice rate + n
    agg = d.groupby("GameID").agg(brate=("B", "mean"), n=("B", "size")).reset_index()

    # option-level features (constant within GameID -> take first)
    g = d.groupby("GameID").first().reset_index()
    evA, sdA = _opt_stats(g["Ha"], g["pHa"], g["La"])
    evB, sdB = _opt_stats(g["Hb"], g["pHb"], g["Lb"])
    feat = pd.DataFrame({
        "GameID": g["GameID"],
        "evA": evA, "sdA": sdA,
        "evB": evB, "sdB": sdB,
        "amb": g["Amb"].astype(float),            # Option B ambiguous
        "d_ev": evB - evA,                         # B minus A
        "d_sd": sdB - sdA,
        "loss": ((g[["Ha", "La", "Hb", "Lb"]] < 0).any(axis=1)).astype(float),
    })
    out = agg.merge(feat, on="GameID")
    return out


def split_by_game(df: pd.DataFrame, test_frac=0.3, seed=0):
    """Out-of-sample split by GameID (predict unseen games)."""
    rng = np.random.default_rng(seed)
    ids = df["GameID"].to_numpy().copy()
    rng.shuffle(ids)
    n_test = int(len(ids) * test_frac)
    test_ids = set(ids[:n_test].tolist())
    train = df[~df["GameID"].isin(test_ids)].reset_index(drop=True)
    test = df[df["GameID"].isin(test_ids)].reset_index(drop=True)
    return train, test


if __name__ == "__main__":
    df = load_description()
    print(f"games: {len(df)}  (unique GameIDs with Trial==1 choices)")
    print(f"total description choices: {int(df['n'].sum())}")
    print(f"median n/game: {int(df['n'].median())}")
    print(f"ambiguous games: {int(df['amb'].sum())}, loss-domain games: {int(df['loss'].sum())}")
    print(f"B-rate: mean {df['brate'].mean():.3f}, range [{df['brate'].min():.2f}, {df['brate'].max():.2f}]")
    print(df[["GameID", "brate", "n", "d_ev", "d_sd", "amb", "loss"]].head(6).to_string(index=False))
