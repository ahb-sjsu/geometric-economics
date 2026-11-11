"""Development analysis: is the next move drawn toward where the opponent just moved?

    python analyze_pull.py within_rows.tsv.gz out.json

One player at one position, games in which the player's own moves came in the
same order. Games are grouped by the opponent's last move. For two groups A and
B whose last moves ended on different squares a and b, every game gets
x = dist(t, b) - dist(t, a), where t is the square the player's next move ends
on and dist counts king steps. The position is the same in both groups, so x is
one fixed function of the chosen move. The pull is mean(x | A) - mean(x | B):
zero if the order does not matter, positive if the move lands nearer the square
the opponent moved to last.

Pairs of groups are weighted by the smaller group. A player's value is the
weighted mean over that player's positions and group pairs. The reported number
is the mean over players with a 95% interval from 2,000 resamples of players,
overall and by speed. Squares are read from the move text, and castling counts
as the king's square.
"""
import gzip
import itertools
import json
import re
import sys
from collections import Counter, defaultdict

import numpy as np

from analyze_paths import speed

SEED = 20261111
SQUARE = re.compile(r"[a-h][1-8]")
MIN_PLAYERS = 30


def dest(san, white):
    """Square a move ends on, as (file, rank), or None if it cannot be read."""
    if san.startswith("O-O-O"):
        return (2, 0 if white else 7)
    if san.startswith("O-O"):
        return (6, 0 if white else 7)
    m = SQUARE.findall(san)
    if not m:
        return None
    return (ord(m[-1][0]) - 97, int(m[-1][1]) - 1)


def dist(p, q):
    return max(abs(p[0] - q[0]), abs(p[1] - q[1]))


def main(rows, out):
    rng = np.random.default_rng(SEED)
    # (mover, speed) -> (position, ply, own order) -> opponent's last move -> Counter of next moves
    cells = defaultdict(lambda: defaultdict(lambda: defaultdict(Counter)))
    unread = 0
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            sp = speed(r[8])
            if sp is None:
                continue
            ply = int(r[1])
            path = r[3].split(" ")
            mover_white = ply % 2 == 0
            if dest(path[-1], not mover_white) is None or dest(r[4], mover_white) is None:
                unread += 1
                continue
            own = " ".join(path[ply % 2::2])
            cells[(r[5], sp)][(r[2], ply, own)][path[-1]][r[4]] += 1
    per = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0, 0]))   # speed -> mover -> [sum w*pull, sum w, pairs]
    for (mover, sp), positions in cells.items():
        for (zkey, ply, own), groups in positions.items():
            if len(groups) < 2:
                continue
            white = ply % 2 == 0
            for (la, ca), (lb, cb) in itertools.combinations(sorted(groups.items()), 2):
                a, b = dest(la, not white), dest(lb, not white)
                if a == b:
                    continue

                def mean_x(c):
                    n = sum(c.values())
                    return sum(k * (dist(dest(m, white), b) - dist(dest(m, white), a)) for m, k in c.items()) / n, n

                (xa, na), (xb, nb) = mean_x(ca), mean_x(cb)
                w = min(na, nb)
                for key in (sp, "all"):
                    cell = per[key][mover]
                    cell[0] += w * (xa - xb)
                    cell[1] += w
                    cell[2] += 1
    res = {"rows_with_unread_squares": unread, "pull": {}}
    for key in sorted(per):
        v = np.array([c[0] / c[1] for c in per[key].values()])
        if len(v) < MIN_PLAYERS:
            res["pull"][key] = {"players": int(len(v))}
            continue
        boots = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(2000)]
        res["pull"][key] = {"players": int(len(v)), "group_pairs": int(sum(c[2] for c in per[key].values())),
                            "pull_king_steps": float(v.mean()),
                            "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
