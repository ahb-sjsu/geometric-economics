"""Development: the same games with middlehand's memory removed, to measure the estimator's bias.

    python null_perm.py dev_rows.tsv.gz out_rows.tsv.gz SEED

Pass 2 found that `analyze_bids.py` returns differences by lag for the four
programs, which keep no memory of earlier games. The reading was that the
comparison selects on an earlier bid inside a short sequence. This file tests
that reading without a model of Skat.

Every game in which middlehand bid or passed is put in a cell: middlehand's
login and suffix, the number of jacks held, and the bin of aces plus tens used
by the analysis. Inside a cell the way the game went (middlehand's first action,
who declared, the game, the result, its value) is shuffled among the games. The
deal, the seats, the series and the order of games stay as they were.

After the shuffle a player's bid depends on the hand cell and on nothing that
came before, by construction. The rate of bidding of every player in every cell
is unchanged, and a game in which middlehand declares is still one in which
middlehand bid. Whatever `analyze_bids.py` then returns by lag or by the last
outcome is produced by the estimator and not by the players.

The other two seats' outcomes are shuffled with the game. Their own bidding is
not analysed.
"""
import gzip
import sys
from collections import defaultdict

import numpy as np

MOVED = (27, 28, 29, 30, 31)       # mid_first, declarer, game, result, value


def main(src, out, seed):
    rng = np.random.default_rng(int(seed))
    rows = []
    cells = defaultdict(list)
    with gzip.open(src, "rt") as f:
        for i, line in enumerate(f):
            r = line.rstrip("\n").split("\t")
            rows.append(r)
            if r[27] in "bp":
                jacks = 0 if r[14] == "-" else len(r[14])
                high = min((int(r[15]) + int(r[16])) // 2, 2)
                cells[(r[11], r[12], jacks, high)].append(i)
    moved = 0
    for idx in cells.values():
        if len(idx) < 2:
            continue
        perm = rng.permutation(len(idx))
        vals = [[rows[i][c] for c in MOVED] for i in idx]
        for k, i in enumerate(idx):
            for c, v in zip(MOVED, vals[perm[k]]):
                rows[i][c] = v
        moved += len(idx)
    with gzip.open(out, "wt") as f:
        for r in rows:
            f.write("\t".join(r) + "\n")
    print("games", len(rows), "cells", len(cells), "games in shuffled cells", moved)


if __name__ == "__main__":
    main(*sys.argv[1:4])
