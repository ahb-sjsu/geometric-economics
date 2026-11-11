"""Development: does middlehand's opening bid depend on that player's recent games?

    python analyze_bids.py dev_rows.tsv.gz out.json

Reads the rows of mine_games.py. Development archive only.

Chains. Games are ordered by id within a series. A seat is a login with its
suffix. A player's run of outcomes continues while the same three seats play
the next game of the series, and starts again when any seat changes.

Outcome of a game for a player: L lost as declarer, W won as declarer, N did not
declare (defended, or the game was passed in), O anything else as declarer.

Decision: middlehand's first action, bid or pass.

Three things are written, in this order.

1. Deal check. The mean number of jacks in middlehand's ten cards, by the
   player's outcome one game back. A fair deal gives 1.25 whatever came before.
   The same by the lag of the one declared game, with the raw rate of bidding,
   added after the programs gave non-zero differences by lag.
2. By the last outcome. The rate of bidding after L, after W and after N, as
   differences within a cell.
3. By lag, as in poker. Decisions where exactly one of the player's last three
   games was declared by the player and the other two were N. The rate of
   bidding when that game was j back against j + 1 back, for a loss, a win and
   either. Both sides of this comparison have just been through one declared
   game, so a player who is bidding freely in a session sits on both sides.

A cell is (unit, number of jacks, aces plus tens in three bins). A unit's value
is the mean over its cells weighted by the smaller of the two counts. The
reported number is the mean over units with a 95% interval from 2,000 resamples
of units. For people the unit is the player. For each program the unit is the
series, since a program is one player.

Groups: people (not one of the four programs, no suffix), people without the
ten with the most decisions (in case some are programs), and each program.
"""
import gzip
import json
import sys
from collections import Counter, defaultdict

import numpy as np

SEED = 20261111
PROGRAMS = ("xskat", "kermit", "zoot", "theCount")
LAGS = 3


def read(rows):
    by = defaultdict(list)
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            by[r[1]].append(r)
    return by


def decisions(by):
    """Yield (who, suffix, series, jacks, high, bid, history) with history most recent first."""
    for series, games in by.items():
        games.sort(key=lambda r: int(r[0]))
        hist, prev_trio = {}, None
        for r in games:
            seats = [(r[3 + 8 * s], r[4 + 8 * s]) for s in (0, 1, 2)]
            trio = frozenset(seats)
            if trio != prev_trio or len(trio) < 3:
                hist = {s: [] for s in seats}
            prev_trio = trio
            if r[27] in "bp":
                who, suf = seats[1]
                jacks = 0 if r[14] == "-" else len(r[14])
                high = int(r[15]) + int(r[16])
                yield who, suf, series, jacks, min(high // 2, 2), r[27] == "b", tuple(hist[seats[1]][::-1][:LAGS])
            decl = int(r[28])
            for s, seat in enumerate(seats):
                if decl != s or r[30] == "passed":
                    hist[seat].append("N")
                else:
                    hist[seat].append("L" if r[30] == "loss" else "W" if r[30] == "win" else "O")


def contrast(cells, a, b, rng):
    per = defaultdict(lambda: [0.0, 0.0])
    for (unit, _), c in cells.items():
        x, y = c.get(a), c.get(b)
        if not x or not y:
            continue
        w = min(x[1], y[1])
        per[unit][0] += w * (x[0] / x[1] - y[0] / y[1])
        per[unit][1] += w
    if len(per) < 30:
        return {"units": len(per)}
    v = np.array([s / w for s, w in per.values()])
    boots = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(2000)]
    return {"units": int(len(v)), "difference": float(v.mean()),
            "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}


def main(rows, out):
    dec = list(decisions(read(rows)))
    n_by = Counter(d[0] for d in dec if d[0] not in PROGRAMS and d[1] == "0")
    busiest = {w for w, _ in n_by.most_common(10)}
    groups = {"people": lambda d: d[0] not in PROGRAMS and d[1] == "0",
              "people_without_ten_busiest": lambda d: d[0] not in PROGRAMS and d[1] == "0" and d[0] not in busiest}
    for p in PROGRAMS:
        groups[p] = lambda d, p=p: d[0] == p
    res = {"decisions": len(dec), "people": len(n_by),
           "decisions_by_the_ten_busiest_people": int(sum(n_by[w] for w in busiest)), "groups": {}}
    for name, keep in groups.items():
        rng = np.random.default_rng(SEED)
        last = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        lag = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        jack = defaultdict(lambda: [0, 0])
        jack_lag = defaultdict(lambda: [0, 0, 0, 0])
        n = 0
        for who, suf, series, jacks, high, bid, h in dec:
            if not keep((who, suf)):
                continue
            n += 1
            unit = series if name in PROGRAMS else who
            key = (unit, (jacks, high))
            if h and h[0] in "LWN":
                c = last[key][h[0]]
                c[0] += bid
                c[1] += 1
                jack[h[0]][0] += jacks
                jack[h[0]][1] += 1
            if len(h) == LAGS and "O" not in h and sum(x != "N" for x in h) == 1:
                j = [i for i, x in enumerate(h) if x != "N"][0] + 1
                t = jack_lag["%s%d" % (h[j - 1], j)]
                t[0] += jacks
                t[1] += high
                t[2] += bid
                t[3] += 1
                for e in (h[j - 1], "A"):
                    c = lag[key][(e, j)]
                    c[0] += bid
                    c[1] += 1
        g = {"decisions": n,
             "bid_rate": float(np.mean([d[5] for d in dec if keep(d)])) if n else None,
             "deal_check_mean_jacks_by_last_outcome": {k: {"mean": v[0] / v[1], "n": v[1]} for k, v in sorted(jack.items())},
             "deal_check_by_lag": {k: {"mean_jacks": v[0] / v[3], "mean_high_bin": v[1] / v[3],
                                       "raw_bid_rate": v[2] / v[3], "n": v[3]} for k, v in sorted(jack_lag.items())},
             "by_last_outcome": {"L_minus_N": contrast(last, "L", "N", rng), "W_minus_N": contrast(last, "W", "N", rng),
                                 "L_minus_W": contrast(last, "L", "W", rng)},
             "by_lag": {}}
        for e, label in (("A", "any"), ("L", "loss"), ("W", "win")):
            for j in range(1, LAGS):
                g["by_lag"]["%s_lag%d_minus_lag%d" % (label, j, j + 1)] = contrast(lag, (e, j), (e, j + 1), rng)
        res["groups"][name] = g
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
