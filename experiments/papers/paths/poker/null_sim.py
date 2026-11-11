"""Players with no memory, passed through the registered code. Written after the sealed result.

    python null_sim.py measure hands.tsv.gz profile.json
    python null_sim.py simulate profile.json sim_hands.tsv.gz [seed]

Why. On 2026-11-11 a comparison of the same shape as the registered poker
contrast, run on Skat, gave non-zero differences for card-playing programs whose
raw rates were flat. The registered contrast selects decisions by a large pot in
the hands before, and a hand in which a player raised is more likely to become
a large pot, so selecting on the pot selects on an earlier decision of the same
player. This file measures what the registered code returns when there is no
memory at all.

`measure` reads a mined hands file and keeps, with no player label:
  for each player, the number of hands and the counts of (raise came before,
  action) over the player's hands,
  samples of the change in stack to the next hand at the table, by action,
  samples of the stack at the start of a stay at a table and of the length of
  a stay.

`simulate` writes a hands file in the miner's format. Each simulated player is
one measured profile. In every hand the pair (raise came before, action) is
drawn from that player's counts, independently of everything earlier. The
change in stack is drawn from the measured changes for that action, so raising
leads to large pots as often as in the data. Nothing else links one hand to the
next except the stack. A stay ends at its drawn length or when the stack falls
under two big blinds. Each stay is its own table, so no hand has two players.

The seat moves round a table of six by one place each hand, from a random
start. The first version (still available as a fifth argument `fixed-seat`)
kept every simulated player in one seat. The registered analysis compares
within a seat, so a fixed seat put consecutive hands in the same cell, which
real play never does. That version returned about -0.005 at every lag while
the raw rates by lag were flat (null_raw.py). It is kept as a demonstration
that the estimator can be biased and is not a measure of the bias in the data.
The action drawn does not depend on the seat, which real play does.

What the simulation leaves out: tables with several players, time of day, and
any change in a player's style from one stay to the next. A style that drifts
between stays would sit on both sides of the registered comparison.
"""
import gzip
import json
import re
import sys
from collections import defaultdict

import numpy as np

from analyze_lags import possible_topup

DIGITS = re.compile(r"[0-9]+")
ACTS = "fcrx"
KEEP = 50000


def measure(rows, out):
    rng = np.random.default_rng(20261111)
    tables = defaultdict(lambda: defaultdict(dict))
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            hand = tuple(int(x) for x in DIGITS.findall(r[3]))
            if hand:
                tables[(r[0], r[1], r[2])][hand][r[5]] = (float(r[8]), r[9], r[10])
    prof = defaultdict(lambda: [0] * 8)
    delta = {a: [] for a in ACTS}
    seen = {a: 0 for a in ACTS}
    starts, lengths = [], []
    for hands in tables.values():
        prev, run = {}, {}
        for h in sorted(hands):
            now = hands[h]
            for p in list(run):
                if p not in now:
                    lengths.append(run.pop(p))
            for p, (stack, faced, act) in now.items():
                if act not in ACTS:
                    continue
                prof[p][(4 if faced == "1" else 0) + ACTS.index(act)] += 1
                if p in prev and not possible_topup(prev[p][0], stack):
                    a = prev[p][2]
                    if a in ACTS:
                        seen[a] += 1
                        if len(delta[a]) < KEEP:
                            delta[a].append(stack - prev[p][0])
                        else:
                            j = int(rng.integers(0, seen[a]))
                            if j < KEEP:
                                delta[a][j] = stack - prev[p][0]
                    run[p] = run.get(p, 1) + 1
                else:
                    if p in run:
                        lengths.append(run.pop(p))
                    run[p] = 1
                    starts.append(stack)
            prev = now
        lengths.extend(run.values())
    pick = lambda v: [float(x) for x in rng.choice(v, min(KEEP, len(v)), replace=False)]
    json.dump({"profiles": list(prof.values()), "delta": delta, "starts": pick(starts), "lengths": pick(lengths),
               "share_large_by_action": {a: float(np.mean(np.abs(delta[a]) >= 10)) for a in ACTS if delta[a]}},
              open(out, "w"))
    print("players", len(prof), "hands", sum(sum(v) for v in prof.values()),
          "share of large pots by action", {a: round(float(np.mean(np.abs(delta[a]) >= 10)), 4) for a in ACTS if delta[a]})


def simulate(profile, out, seed=1, rotate=True):
    rng = np.random.default_rng(seed)
    m = json.load(open(profile))
    delta = {a: np.array(m["delta"][a]) for a in ACTS}
    starts, lengths = np.array(m["starts"]), np.array(m["lengths"]).astype(int)
    table = rows = 0
    with gzip.open(out, "wt", compresslevel=3) as g:
        for i, counts in enumerate(m["profiles"]):
            n = int(sum(counts))
            if n < 6:
                continue
            p = np.array(counts) / n
            codes = rng.choice(8, n, p=p)
            done = 0
            while done < n:
                table += 1
                length = min(int(rng.choice(lengths)), n - done)
                stack = float(rng.choice(starts))
                seat0 = int(rng.integers(0, 6)) if rotate else 3
                for k in range(length):
                    c = int(codes[done + k])
                    act = ACTS[c % 4]
                    seat = (seat0 + k) % 6 if rotate else 3
                    g.write("SIM\t1\tt%d\t%d\t1\tp%d\t%d\t6\t%.2f\t%d\t%s\n" % (table, k + 1, i, seat, stack, c // 4, act))
                    rows += 1
                    stack += float(rng.choice(delta[act]))
                    if stack < 2:
                        length = k + 1
                        break
                done += length
    print("DONE rows", rows, "tables", table, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "measure":
        measure(sys.argv[2], sys.argv[3])
    else:
        simulate(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 1,
                 not (len(sys.argv) > 5 and sys.argv[5] == "fixed-seat"))
