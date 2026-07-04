#!/usr/bin/env python3
"""Parse the bogota behavioral-game-theory datapool WITHOUT importing bogota.

The pool modules store human play as literals:
    WeightedUncorrelatedProfile(N, make_profile(game_var, [f0, f1, ...]))
where N = #subjects and [f...] = observed row-player action frequencies. Payoffs
are in the companion Gambit .nfg file. We regex the literals and parse the .nfg,
yielding per-game (row-player payoff matrix, observed action freqs, N).

Each row STRATEGY is then encoded into the SAME (EV, SD) feature space as CPC18
lotteries, under a uniform level-0 belief over the column player's actions
(strategic uncertainty = payoff variance across the opponent's actions). This is
what makes the cross-domain (games <-> lotteries) transfer possible: one metric,
one feature space.
"""
from __future__ import annotations

import glob
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
POOLS = os.path.join(HERE, "raw", "bogota", "bogota", "data", "pools")

_PROF = re.compile(
    r"WeightedUncorrelatedProfile\(\s*(\d+)\s*,\s*make_profile\(\s*(\w+)\s*,\s*\[([0-9eE.,\s-]*)\]\s*\)",
)
_ASSIGN = re.compile(r"(\w+)\s*=\s*read_game\(\s*dirname\s*\+\s*['\"]/([\w.-]+\.nfg)['\"]")


def _parse_nfg(path: str):
    """Return the row-player (player 0) payoff matrix M[s0][s1] for a 2-player game,
    or None if not 2-player."""
    with open(path, encoding="utf-8", errors="replace") as f:
        txt = f.read()
    # strategy-count block: { n0 n1 ... } after the players block
    m = re.search(r"\}\s*\{\s*([\d\s]+?)\}", txt)
    if not m:
        return None
    counts = [int(x) for x in m.group(1).split()]
    if len(counts) != 2:
        return None
    n0, n1 = counts
    # payoffs: all floats after the strategy block
    tail = txt[m.end():]
    nums = [float(x) for x in re.findall(r"-?\d+\.?\d*", tail)]
    need = 2 * n0 * n1
    if len(nums) < need:
        return None
    payoffs = nums[:need]
    M = np.zeros((n0, n1))
    for s1 in range(n1):
        for s0 in range(n0):
            c = s0 + n0 * s1  # player-0 strategy varies fastest
            M[s0, s1] = payoffs[2 * c]  # player-0 payoff
    return M


def load_games():
    """Yield dicts: {id, N, freqs (row-player, len n0), payoff M[n0,n1], study}."""
    games = []
    for pool_py in glob.glob(os.path.join(POOLS, "*.py")):
        study = os.path.splitext(os.path.basename(pool_py))[0]
        if study == "__init__":
            continue
        src = open(pool_py, encoding="utf-8", errors="replace").read()
        nfg_of = {var: nfg for var, nfg in _ASSIGN.findall(src)}
        for N, gvar, farr in _PROF.findall(src):
            nfg = nfg_of.get(gvar)
            if not nfg:
                continue
            path = os.path.join(POOLS, nfg)
            if not os.path.exists(path):
                continue
            M = _parse_nfg(path)
            if M is None:
                continue
            freqs = [float(x) for x in farr.split(",") if x.strip() != ""]
            n0 = M.shape[0]
            freqs = freqs[:n0]
            if len(freqs) != n0 or abs(sum(freqs)) < 1e-9:
                continue
            games.append({"id": f"{study}:{gvar}", "study": study, "N": int(N),
                          "freqs": np.array(freqs), "M": M})
    return games


def encode_strategies(M: np.ndarray):
    """Per row strategy: (EV, SD) under a UNIFORM belief over the column actions.
    Same feature space as CPC18 lotteries (EV, risk)."""
    ev = M.mean(axis=1)                 # E_j[payoff | uniform opponent]
    sd = M.std(axis=1)                  # strategic-uncertainty risk
    return ev, sd


if __name__ == "__main__":
    games = load_games()
    studies = {}
    for g in games:
        studies[g["study"]] = studies.get(g["study"], 0) + 1
    print(f"parsed {len(games)} 2-player games from {len(studies)} studies")
    for s, n in sorted(studies.items()):
        print(f"  {s}: {n}")
    g = games[0]
    ev, sd = encode_strategies(g["M"])
    print(f"\nexample {g['id']}: N={g['N']} shape={g['M'].shape}")
    print(f"  payoff M=\n{g['M']}")
    print(f"  observed freqs = {g['freqs']}")
    print(f"  strategy EV (uniform belief) = {ev}")
    print(f"  strategy SD = {sd}")
