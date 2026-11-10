"""Pilot of pass 3: among moves the engine rates as equal, are boundary-crossing moves chosen less?

    python analyze_edges.py within_rows_with_evals.tsv.gz out.json

The reading was fixed in DEVELOPMENT.md before this was written. Definition 6.1
with non-negative penalties predicts that, of two moves of equal static value,
the one that crosses a boundary is chosen less often, by an amount that belongs
to the boundary and not to the position.

Static value of a move at a position: the median of Lichess's engine
evaluation after it, over the games that carry one, from the mover's side, with
at least MIN_EVALS such games. Two moves are equal when their values differ by
at most MARGIN pawns. Edge classes come from the move's notation alone:

    capture   the move takes a piece or pawn
    pawn      a pawn move that is not a capture
    castle    castling
    king      a king move that is not castling
    piece     any other move: the class that crosses nothing

For every position and every pair of equal moves, one crossing and one of class
`piece`, the quantity is the log of (games choosing the crossing move / games
choosing the piece move). It is pooled per class over pairs with equal weight
per position, with an interval from resampling positions. Pairs of two `piece`
moves are scored the same way with the order fixed by notation, as a check that
the pooling itself gives zero.

A pilot. The positions are opening positions, where how often a move is played
reflects memorised theory.
"""
import gzip
import json
import math
import sys
from collections import defaultdict

import numpy as np

MIN_EVALS = 20
MIN_PLAYS = 50
MARGIN = 0.10
SEED = 20261110


def edge_class(san):
    if san.startswith("O-O"):
        return "castle"
    if "x" in san:
        return "capture"
    if san[0] in "abcdefgh":
        return "pawn"
    if san[0] == "K":
        return "king"
    return "piece"


def value(text, side):
    if text.startswith("#"):
        v = 100.0 if not text.startswith("#-") else -100.0
    else:
        v = float(text)
    return v if side == 0 else -v


def main(rows, out):
    rng = np.random.default_rng(SEED)
    plays = defaultdict(lambda: defaultdict(int))      # (zkey, ply) -> move -> games
    evals = defaultdict(lambda: defaultdict(list))     # (zkey, ply) -> move -> values
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            if len(r) < 12:
                continue
            k = (r[2], int(r[1]))
            plays[k][r[4]] += 1
            if r[11]:
                try:
                    evals[k][r[4]].append(value(r[11], k[1] % 2))
                except ValueError:
                    pass
    per_class = defaultdict(lambda: defaultdict(list))   # class -> zkey -> [log odds]
    n_positions = 0
    for k, moves in plays.items():
        val = {m: float(np.median(v)) for m, v in evals[k].items()
               if len(v) >= MIN_EVALS and moves[m] >= MIN_PLAYS}
        if len(val) < 2:
            continue
        n_positions += 1
        names = sorted(val)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                if abs(val[a] - val[b]) > MARGIN:
                    continue
                ca, cb = edge_class(a), edge_class(b)
                if ca == "piece" and cb == "piece":
                    per_class["piece_vs_piece"][k[0]].append(math.log(moves[a] / moves[b]))
                elif cb == "piece":
                    per_class[ca][k[0]].append(math.log(moves[a] / moves[b]))
                elif ca == "piece":
                    per_class[cb][k[0]].append(math.log(moves[b] / moves[a]))
    res = {"positions_with_two_valued_moves": n_positions, "margin": MARGIN,
           "min_evals": MIN_EVALS, "min_plays": MIN_PLAYS, "classes": {}}
    for c, pos in per_class.items():
        v = np.array([np.mean(x) for x in pos.values()])
        if len(v) < 10:
            res["classes"][c] = {"positions": int(len(v))}
            continue
        boots = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(2000)]
        res["classes"][c] = {
            "positions": int(len(v)), "pairs": int(sum(len(x) for x in pos.values())),
            "mean_log_odds": float(v.mean()),
            "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],
            "sd_between_positions": float(v.std(ddof=1)),
            "share_of_positions_below_zero": float((v < 0).mean())}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
