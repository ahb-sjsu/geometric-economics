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
    Mrow = np.zeros((n0, n1))   # player-0 (row) payoff, indexed [s0, s1]
    Mcol = np.zeros((n0, n1))   # player-1 (col) payoff, indexed [s0, s1]
    for s1 in range(n1):
        for s0 in range(n0):
            c = s0 + n0 * s1  # player-0 strategy varies fastest
            Mrow[s0, s1] = payoffs[2 * c]
            Mcol[s0, s1] = payoffs[2 * c + 1]
    return Mrow, Mcol


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
            parsed = _parse_nfg(path)
            if parsed is None:
                continue
            Mrow, Mcol = parsed
            freqs = [float(x) for x in farr.split(",") if x.strip() != ""]
            n0 = Mrow.shape[0]
            freqs = freqs[:n0]
            if len(freqs) != n0 or abs(sum(freqs)) < 1e-9:
                continue
            games.append({"id": f"{study}:{gvar}", "study": study, "N": int(N),
                          "freqs": np.array(freqs), "M": Mrow, "Mcol": Mcol})
    return games


def _softmax(x, lam):
    z = lam * (x - x.max())
    e = np.exp(z)
    return e / e.sum()


def opponent_belief(M: np.ndarray, Mcol: np.ndarray, level: int, lam: float):
    """Column player's action distribution believed by a level-(level+1) row player.
    Iterated quantal best responses starting from uniform (level 0). Returns a
    length-n1 distribution over the opponent's actions.

    M    = row payoff [s0, s1] (row's own payoff)
    Mcol = col payoff [s0, s1] (col's own payoff)
    """
    n0, n1 = M.shape
    row_dist = np.ones(n0) / n0
    col_dist = np.ones(n1) / n1
    for _ in range(max(1, level)):
        col_dist = _softmax(row_dist @ Mcol, lam)      # col BR to row_dist
        row_dist = _softmax(M @ col_dist, lam)         # row BR to col_dist
    return col_dist


def encode_strategies(M: np.ndarray, Mcol: np.ndarray | None = None,
                      belief: str = "uniform", level: int = 1, lam: float = 0.1):
    """Per row strategy: (EV, SD) under a belief about the column player.

    belief='uniform' : opponent uniform (level-0)  -> row is level-1.
    belief='lk'      : opponent plays level-`level` quantal BR (precision lam)
                       -> row is level-(level+1). Needs Mcol.
    Same (EV, SD) feature space as CPC18 lotteries in every case.
    """
    if belief == "lk" and Mcol is not None:
        w = opponent_belief(M, Mcol, level, lam)
    else:
        w = np.ones(M.shape[1]) / M.shape[1]
    ev = M @ w
    sd = np.sqrt((((M - ev[:, None]) ** 2) @ w))
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
    evu, sdu = encode_strategies(g["M"])
    evk, sdk = encode_strategies(g["M"], g["Mcol"], belief="lk", level=1, lam=0.1)
    print(f"\nexample {g['id']}: N={g['N']} shape={g['M'].shape}")
    print(f"  observed freqs   = {np.round(g['freqs'], 3)}")
    print(f"  EV uniform (l0)  = {np.round(evu, 2)}   SD = {np.round(sdu, 2)}")
    print(f"  EV level-k belief= {np.round(evk, 2)}   SD = {np.round(sdk, 2)}")
