"""Does the hand straight after a large pot differ from the hands that follow it?

    python analyze_recency.py hands.tsv.gz out.json [threshold_bb [stack_bin_width [site|all [table]]]]

The comparison that survived the checks in DEVELOPMENT.md, estimated directly.
A decision is used when exactly one of the player's previous four hands at the
table was a large pot for that player (the stack moved by at least the
threshold) and the other three were not. Its lag is how many hands back that
pot was. Within a cell (player, site, big blind, seat, number of players,
whether a raise came before, stack bin, and the table if asked), the rate of
raising at lag j is compared with the rate at lag j + 1. No quiet-hand baseline
enters, so both sides of every comparison have just been through a large pot of
the same kind and sit at about the same stack.

A player's value is the mean over that player's cells, weighted by the smaller
of the two counts in the cell. The reported number is the mean over players,
with a 95% interval from 2,000 resamples of players. Three event sets: a large
loss, a large win, and either.

Chain rules are those of analyze_lags.py: the result of a hand is the change in
starting stack to the next hand dealt at the same table, and a rise that lands on
a whole multiple of 10 big blinds between 20 and 250 is treated as a possible
top-up and breaks the chain.
"""
import gzip
import json
import re
import sys
from collections import defaultdict

import numpy as np

from analyze_lags import LAGS, SEED, THRESH, possible_topup, stack_bin

DIGITS = re.compile(r"[0-9]+")


def decisions(rows, thresh, only_site=""):
    """Yield (player, site, bb, table, seat, n, faced, stack, act, event, lag) for usable decisions."""
    tables = defaultdict(lambda: defaultdict(dict))
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            if only_site and r[0] != only_site:
                continue
            hand = tuple(int(x) for x in DIGITS.findall(r[3]))
            if hand:
                tables[(r[0], r[1], r[2])][hand][r[5]] = (int(r[6]), int(r[7]), float(r[8]), r[9], r[10])
    for (site, bb, table), hands in tables.items():
        hist = defaultdict(list)
        prev = {}
        for h in sorted(hands):
            now = hands[h]
            for p in list(hist):
                if p not in now or p not in prev:
                    del hist[p]
            for p, row in now.items():
                if p in prev:
                    if possible_topup(prev[p][2], row[2]):
                        hist[p] = []
                    else:
                        d = row[2] - prev[p][2]
                        hist[p].append("L" if d <= -thresh else "W" if d >= thresh else "N")
                else:
                    hist[p] = []
            for p, (seat, n, stack, faced, act) in now.items():
                if act == "x":
                    continue
                past = hist[p][-LAGS:]
                if len(past) < LAGS:
                    continue
                past = past[::-1]
                ev = [(e, j + 1) for j, e in enumerate(past) if e != "N"]
                if len(ev) == 1:
                    yield p, site, bb, table, seat, n, faced, stack, act, ev[0][0], ev[0][1]
            prev = now


def main(rows, out, thresh=THRESH, width=0, only_site="", by_table=False):
    rng = np.random.default_rng(SEED)
    # cell -> (event, lag) -> [entered, raised, n]
    cells = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))
    used = 0
    for p, site, bb, table, seat, n, faced, stack, act, event, lag in decisions(rows, thresh, only_site):
        key = (p, site, bb, seat, n, faced, stack_bin(stack, width), table if by_table else "")
        for e in (event, "A"):
            c = cells[key][(e, lag)]
            c[0] += act in "cr"
            c[1] += act == "r"
            c[2] += 1
        used += 1
    res = {"decisions_used": used, "threshold_bb": thresh, "stack_bin_width": width,
           "site": only_site or "all", "within_table": by_table, "contrasts": {}}
    for which, idx in (("raised", 1), ("entered", 0)):
        block = {}
        for e, name in (("A", "any"), ("L", "loss"), ("W", "win")):
            rates = [c[(e, 1)][idx] / c[(e, 1)][2] for c in cells.values() if c[(e, 1)][2]]
            block["%s_rate_at_lag1" % name] = float(np.mean(rates)) if rates else None
            for j in range(1, LAGS):
                per = defaultdict(lambda: [0.0, 0.0])
                pairs = 0
                for key, c in cells.items():
                    a, b = c[(e, j)], c[(e, j + 1)]
                    if a[2] == 0 or b[2] == 0:
                        continue
                    w = min(a[2], b[2])
                    acc = per[key[0]]
                    acc[0] += w * (a[idx] / a[2] - b[idx] / b[2])
                    acc[1] += w
                    pairs += 1
                label = "%s_lag%d_minus_lag%d" % (name, j, j + 1)
                if len(per) < 30:
                    block[label] = {"players": len(per)}
                    continue
                v = np.array([s / w for s, w in per.values()])
                boots = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(2000)]
                block[label] = {"players": int(len(v)), "cells": int(pairs), "difference": float(v.mean()),
                                "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}
        res["contrasts"][which] = block
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2],
         float(sys.argv[3]) if len(sys.argv) > 3 else THRESH,
         int(sys.argv[4]) if len(sys.argv) > 4 else 0,
         sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != "all" else "",
         len(sys.argv) > 6 and sys.argv[6] == "table")
