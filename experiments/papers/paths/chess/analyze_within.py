"""Development analysis within players: same person, same position, different move order.

    python analyze_within.py rows.tsv.gz out.json

The sampled comparison between groups of players (analyze_paths.py) cannot rule
out that the groups differ: a player whose own moves were the same may still
have chosen them against different replies. Here each player is compared with
themselves. For a player who met one position in several games, every pair of
those games is classed by how the two move orders differ:

    same    the same order
    opp3    own moves in the same order, opponent's in a different order, opponent's last move the same
    opp     own moves in the same order, opponent's in a different order, opponent's last move different
    own     own moves in a different order

and scored by whether the player chose a different next move in the two games.
The baseline is the rate at which a player changes move when nothing about the
order differs. The quantity of interest is the change rate in a class minus the
baseline, averaged over players who have pairs of both kinds at one position,
with an interval from resampling players.

Pairs are restricted to the same speed category, and games within a pair are
taken from one month, so rating drift is small. Development only.
"""
import gzip
import itertools
import json
import sys
from collections import defaultdict

import numpy as np

from analyze_paths import speed

SEED = 20261110
MAX_GAMES = 40      # per player and position, to bound the number of pairs


def kind(path_a, path_b, ply):
    if path_a == path_b:
        return "same"
    a, b = path_a.split(" "), path_b.split(" ")
    side = ply % 2
    if a[side::2] != b[side::2]:
        return "own"
    return "opp3" if a[-1] == b[-1] else "opp"


def main(rows, out):
    rng = np.random.default_rng(SEED)
    by = defaultdict(list)                      # (zkey, ply, mover, speed) -> [(path, move)]
    n = 0
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            sp = speed(r[8])
            if sp is None:
                continue
            n += 1
            by[(r[2], int(r[1]), r[5], sp)].append((r[3], r[4]))
    # per (position, player): change rate by class
    per = defaultdict(lambda: defaultdict(lambda: [0, 0]))   # (zkey, ply, mover) -> kind -> [changed, pairs]
    for (zkey, ply, mover, sp), g in by.items():
        if len(g) < 2:
            continue
        if len(g) > MAX_GAMES:
            g = [g[i] for i in rng.choice(len(g), MAX_GAMES, replace=False)]
        for (pa, ma), (pb, mb) in itertools.combinations(g, 2):
            c = per[(zkey, ply, mover)][kind(pa, pb, ply)]
            c[0] += ma != mb
            c[1] += 1
    summary = {"rows": n, "player_positions_with_2plus_games": len(per)}
    detail = {}
    for k in ("opp3", "opp", "own"):
        # one number per player: mean over that player's positions of (rate in class - rate in same)
        diffs = defaultdict(list)
        base, treat, pairs = [], [], 0
        pos = defaultdict(list)
        for (zkey, ply, mover), c in per.items():
            if c["same"][1] == 0 or c[k][1] == 0:
                continue
            r0 = c["same"][0] / c["same"][1]
            r1 = c[k][0] / c[k][1]
            diffs[mover].append(r1 - r0)
            pos[zkey].append(r1 - r0)
            base.append(r0)
            treat.append(r1)
            pairs += c[k][1]
        if not diffs:
            summary[k] = {"players": 0}
            continue
        v = np.array([np.mean(x) for x in diffs.values()])
        boots = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(2000)]
        summary[k] = {
            "players": int(len(v)), "player_positions": int(len(base)), "pairs_in_class": int(pairs),
            "positions": int(len(pos)),
            "change_rate_same_order": float(np.mean(base)),
            "change_rate_this_class": float(np.mean(treat)),
            "difference": float(v.mean()),
            "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}
        detail[k] = sorted(
            ({"zkey": z, "player_positions": len(x), "difference": float(np.mean(x))}
             for z, x in pos.items() if len(x) >= 30),
            key=lambda r: -r["difference"])
    json.dump({"summary": summary, "by_position": detail}, open(out, "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
