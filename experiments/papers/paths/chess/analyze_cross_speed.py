"""Pass 5: is the last-move effect larger at faster speeds within the same player?

    python analyze_cross_speed.py within_rows.tsv.gz out.json [min_gap_hours]

For each player and each speed category separately, D(0) is the rate at which
the player changes move between two of their games at one position whose move
orders differ in the opponent's last move (own moves in the same order), minus
the rate between two games with identical orders. It is the mean over that
player's positions that have pairs of both kinds at that speed. For players
with a value at two speeds the faster-speed value minus the slower-speed value
is averaged, with a 95% interval from resampling players.
"""
import gzip
import itertools
import json
import sys
from collections import defaultdict

import numpy as np

from analyze_memory import MAX_GAMES, SEED, minutes
from analyze_paths import speed

ORDER = ("bullet", "blitz", "rapid")


def main(rows, out, min_gap_hours=24.0):
    rng = np.random.default_rng(SEED)
    gap = min_gap_hours * 60
    by = defaultdict(list)
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            sp = speed(r[8])
            if sp in ORDER:
                by[(r[2], int(r[1]), r[5], sp)].append((tuple(r[3].split(" ")), r[4], minutes(r[10])))
    per = defaultdict(list)                      # (mover, speed) -> [D(0) at one position]
    for (zkey, ply, mover, sp), g in by.items():
        if len(g) < 2:
            continue
        if len(g) > MAX_GAMES:
            g = [g[i] for i in rng.choice(len(g), MAX_GAMES, replace=False)]
        side = ply % 2
        same = [0, 0]
        diff = [0, 0]
        for (pa, ma, ta), (pb, mb, tb) in itertools.combinations(g, 2):
            if abs(ta - tb) < gap:
                continue
            if pa == pb:
                same[0] += ma != mb
                same[1] += 1
            elif pa[-1] != pb[-1] and pa[side::2] == pb[side::2]:
                diff[0] += ma != mb
                diff[1] += 1
        if same[1] and diff[1]:
            per[(mover, sp)].append(diff[0] / diff[1] - same[0] / same[1])
    value = {k: float(np.mean(v)) for k, v in per.items()}
    res = {"min_gap_hours": min_gap_hours,
           "players_with_a_value": {s: sum(1 for (_, sp) in value if sp == s) for s in ORDER},
           "mean_D0": {s: float(np.mean([v for (_, sp), v in value.items() if sp == s])) for s in ORDER},
           "within_player": {}}
    movers = defaultdict(dict)
    for (m, sp), v in value.items():
        movers[m][sp] = v
    for fast, slow in (("bullet", "blitz"), ("blitz", "rapid"), ("bullet", "rapid")):
        d = np.array([v[fast] - v[slow] for v in movers.values() if fast in v and slow in v])
        if len(d) < 30:
            res["within_player"]["%s_minus_%s" % (fast, slow)] = {"players": int(len(d))}
            continue
        boots = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(2000)]
        both = [(v[fast], v[slow]) for v in movers.values() if fast in v and slow in v]
        res["within_player"]["%s_minus_%s" % (fast, slow)] = {
            "players": int(len(d)), "difference": float(d.mean()),
            "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],
            "mean_D0_fast": float(np.mean([a for a, _ in both])),
            "mean_D0_slow": float(np.mean([b for _, b in both]))}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 24.0)
