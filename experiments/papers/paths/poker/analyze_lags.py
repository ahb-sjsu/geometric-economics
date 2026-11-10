"""Development analysis: does a recent large win or loss change the next decision, and how far back?

    python analyze_lags.py dev_hands.tsv.gz out.json [threshold_bb [stack_bin_width [site]]]

`stack_bin_width` replaces the coarse stack bins with bins that many big blinds
wide, to check that a deeper stack after a win is not what moves the curve.
`site` restricts the analysis to one site ("all" for every site). A final
argument `table` adds the table to the cell, so that a player is compared only
with the same player at the same table. Tables where large pots are common are
played differently, and without this a player's quiet hands at a quiet table
would be the baseline for hands after a large pot at a wild one.

Rows come from mine_hands.py. The design is in DESIGN.md, Sections 4 and 5.

The result of a hand for a player is the change in that player's starting stack
from that hand to the next hand dealt at the same table, in big blinds. It is
defined only when the player was dealt into both. A rise that lands the stack on
a whole multiple of 10 big blinds between 20 and 250 is treated as a possible
top-up and breaks the chain, since a top-up cannot be told from a win by the
stack alone. A large loss is a fall of at least THRESH big blinds, a large win a
rise of at least THRESH.

For a decision with four measured results behind it at the same table:
    baseline      none of the four previous hands held a large win or loss
    loss at j     the hand j back was a large loss and the other three held neither
    win at j      likewise for a large win
The state is held fixed within a cell: player, site, big blind, seat in the
betting order, number of players, whether a raise came before, and stack bin.
For each cell with baseline decisions and decisions of a given kind, the
difference in the rate of entering the pot (and of raising) is taken. A player's
value is the mean over that player's cells weighted by the number of event
decisions. The curve is the mean over players, with an interval from resampling
players. The fall from lag 1 to lag 2 is computed over players who have both.
"""
import gzip
import json
import re
import sys
from collections import defaultdict

import numpy as np

THRESH = 10.0
LAGS = 4
SEED = 20261110
BINS = (40, 80, 120, 200)
DIGITS = re.compile(r"[0-9]+")


def stack_bin(s, width=0):
    """Coarse bins by default. With `width`, bins that many big blinds wide, capped at 300."""
    if width:
        return int(min(s, 300) // width)
    for i, b in enumerate(BINS):
        if s < b:
            return i
    return len(BINS)


def possible_topup(prev, new):
    return new > prev and 20 <= new <= 250 and abs(new / 10 - round(new / 10)) < 0.005


def main(rows, out, thresh=THRESH, width=0, only_site="", by_table=False):
    rng = np.random.default_rng(SEED)
    tables = defaultdict(lambda: defaultdict(dict))     # (site, bb, table) -> hand -> player -> row
    n_rows = n_skipped = 0
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            if only_site and r[0] != only_site:
                continue
            # Hand numbers are plain integers on some sites and text such as 'R5-1704660-533'
            # on Ongame. The order key is the tuple of integer groups in the label.
            hand = tuple(int(x) for x in DIGITS.findall(r[3]))
            if not hand:
                n_skipped += 1
                continue
            n_rows += 1
            tables[(r[0], r[1], r[2])][hand][r[5]] = (int(r[6]), int(r[7]), float(r[8]), r[9], r[10])
    # cell -> kind -> [entered, raised, n]; kind is "base" or (event, lag)
    cells = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))
    counts = defaultdict(int)
    for (site, bb, table), hands in tables.items():
        order = sorted(hands)
        hist = defaultdict(list)                          # player -> results of consecutive previous hands
        prev = {}
        for h in order:
            now = hands[h]
            # results of the previous hand, known now that this hand's stacks are seen
            for p in list(hist):
                if p not in now or p not in prev:
                    del hist[p]
            for p, row in now.items():
                if p in prev:
                    d = row[2] - prev[p][2]
                    if possible_topup(prev[p][2], row[2]):
                        hist[p] = []
                        counts["chain_breaks_topup"] += 1
                    else:
                        hist[p].append("L" if d <= -thresh else "W" if d >= thresh else "N")
                else:
                    hist[p] = []
            for p, (pos, n, stack, faced, act) in now.items():
                if act == "x":
                    continue
                past = hist[p][-LAGS:]
                if len(past) < LAGS:
                    continue
                past = past[::-1]                         # past[0] is the hand just before
                events = [(e, j + 1) for j, e in enumerate(past) if e != "N"]
                if not events:
                    kind = "base"
                elif len(events) == 1:
                    kind = events[0]
                else:
                    counts["decisions_with_two_events"] += 1
                    continue
                c = cells[(p, site, bb, pos, n, faced, stack_bin(stack, width),
                           table if by_table else "")][kind]
                c[0] += act in "cr"
                c[1] += act == "r"
                c[2] += 1
                counts["decisions_used"] += 1
            prev = now
    res = {"rows": n_rows, "rows_without_hand_number": n_skipped, "tables": len(tables), "threshold_bb": thresh, "stack_bin_width": width, "site": only_site or "all", "within_table": by_table, **counts, "curves": {}}
    for which, idx in (("entered", 0), ("raised", 1)):
        per = {}                                          # kind -> player -> [sum w*diff, sum w]
        base_rates = []
        for cell, kinds in cells.items():
            if kinds["base"][2] == 0:
                continue
            r0 = kinds["base"][idx] / kinds["base"][2]
            for kind, c in kinds.items():
                if kind == "base" or c[2] == 0:
                    continue
                acc = per.setdefault(kind, {}).setdefault(cell[0], [0.0, 0.0])
                acc[0] += c[2] * (c[idx] / c[2] - r0)
                acc[1] += c[2]
                base_rates.append(r0)
        curve = {"baseline_rate_in_compared_cells": float(np.mean(base_rates)) if base_rates else None}
        means = {}
        for kind in sorted(per):
            v = {p: a / w for p, (a, w) in per[kind].items()}
            means[kind] = v
            x = np.array(list(v.values()))
            n_dec = int(sum(w for _, w in per[kind].values()))
            if len(x) < 30:
                curve["%s_lag%d" % kind] = {"players": int(len(x)), "decisions": n_dec}
                continue
            boots = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(2000)]
            curve["%s_lag%d" % kind] = {
                "players": int(len(x)), "decisions": n_dec, "difference": float(x.mean()),
                "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}
        for e in ("L", "W"):
            a, b = means.get((e, 1), {}), means.get((e, 2), {})
            both = sorted(set(a) & set(b))
            if len(both) >= 30:
                d = np.array([abs(a[p]) - abs(b[p]) for p in both])
                s = np.array([a[p] - b[p] for p in both])
                boots = [s[rng.integers(0, len(s), len(s))].mean() for _ in range(2000)]
                curve["%s_lag1_minus_lag2" % e] = {
                    "players": int(len(both)), "difference": float(s.mean()),
                    "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],
                    "mean_difference_in_size": float(d.mean())}
        res["curves"][which] = curve
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2],
         float(sys.argv[3]) if len(sys.argv) > 3 else THRESH,
         int(sys.argv[4]) if len(sys.argv) > 4 else 0,
         sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != "all" else "",
         len(sys.argv) > 6 and sys.argv[6] == "table")
