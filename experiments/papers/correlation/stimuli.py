#!/usr/bin/env python3
"""The stimulus set of the correlation-attitude design (DESIGN.md). Deterministic from SEED.

    python stimuli.py OUT.json

Units are points. `a` is the self shortfall (100 minus self points) and `b` the charity shortfall
(100 minus charity points), so the ideal is (0, 0). An option has one outcome (sure) or two at even
odds, each outcome an (a, b) pair. Within every trial all outcomes sit on one side of a = b, so no
trial crosses self = charity and inequality aversion is linear inside each trial.

  R  40 riskless pairs, neither option dominating. Locations a in 5..40 and b in 50..100; tradeoff
     ratios of 0.5, 1, 2 and 3 charity points per self point, 10 pairs each.        role calib
  S  32 even-odds lotteries against a sure amount on one attribute. Self lotteries at charity
     shortfall b = 0, 50, 75, 100; charity lotteries at self shortfall a = 0, 10, 25, 40. The b = 0
     and a = 0 cells are calibration, because the metric adds nothing there; the rest are test.
  X  24 correlation pairs: equal marginals, correlated against anticorrelated, 12 configurations
     in both left-right orders.                                                       role test
  A  8 dominated riskless pairs, attention checks.                                    role check

Option 0 is shown on the left. S trials record which option is the lottery (`lot_option`), X trials
which is the correlated one (`corr_option`). `order` is the presentation order: R first, then S, X
and A shuffled together.
"""
import json
import sys

import numpy as np

SEED = 20261102


def opt(*outs):
    if len(outs) == 1:
        return [[1.0, float(outs[0][0]), float(outs[0][1])]]
    return [[0.5, float(o[0]), float(o[1])] for o in outs]


def one_side(trial):
    outs = [o for option in trial["options"] for o in option]
    return all(o[1] < o[2] for o in outs) or all(o[1] > o[2] for o in outs)


def build():
    rng = np.random.default_rng(SEED)
    trials = []

    def add(block, cell, role, o0, o1, **extra):
        t = {"id": len(trials), "block": block, "cell": cell, "role": role, "options": [o0, o1], **extra}
        assert one_side(t), t
        trials.append(t)

    # R: riskless tradeoffs. The self-favouring option gives up `da` self points less, the other gives
    # the charity `ratio * da` points more.
    seen, counts = set(), {0.5: 0, 1: 0, 2: 0, 3: 0}
    while min(counts.values()) < 10:
        ratio = min(counts, key=counts.get)
        da = int(rng.choice([5, 10, 15]))
        db = int(round(ratio * da / 5)) * 5
        if db == 0:
            continue
        a1 = int(rng.choice(np.arange(5, 41 - da, 5)))
        b2 = int(rng.choice(np.arange(50, 101 - db, 5)))
        a2, b1 = a1 + da, b2 + db
        if (a1, b1, a2, b2) in seen:
            continue
        seen.add((a1, b1, a2, b2))
        counts[ratio] += 1
        pair = (opt((a1, b1)), opt((a2, b2)))
        if rng.random() < 0.5:
            pair = pair[::-1]
        add("R", f"R_ratio{ratio}", "calib", *pair)

    # S: single-attribute lotteries against a sure amount
    for b in (0, 50, 75, 100):
        for (lo, hi), sure in (((5, 35), 15), ((5, 35), 25), ((10, 40), 20), ((10, 40), 30)):
            left = int(rng.random() < 0.5)
            lot, s = opt((lo, b), (hi, b)), opt((sure, b))
            add("S", f"S_self_b{b}", "calib" if b == 0 else "test", *((lot, s) if left else (s, lot)),
                lot_option=0 if left else 1, side="self", level=b)
    for a in (0, 10, 25, 40):
        for (lo, hi), sure in (((50, 100), 65), ((50, 100), 85), ((60, 100), 70), ((60, 100), 90)):
            left = int(rng.random() < 0.5)
            lot, s = opt((a, lo), (a, hi)), opt((a, sure))
            add("S", f"S_charity_a{a}", "calib" if a == 0 else "test", *((lot, s) if left else (s, lot)),
                lot_option=0 if left else 1, side="charity", level=a)

    # X: correlated against anticorrelated, equal marginals
    for alo, ahi in ((5, 25), (10, 40), (5, 40), (20, 40)):
        for blo, bhi in ((50, 80), (60, 100), (50, 100)):
            cor, anti = opt((alo, blo), (ahi, bhi)), opt((alo, bhi), (ahi, blo))
            cell = f"X_a{alo}-{ahi}_b{blo}-{bhi}"
            add("X", cell, "test", cor, anti, corr_option=0)
            add("X", cell, "test", anti, cor, corr_option=1)

    # A: dominated pairs
    for _ in range(8):
        a1, b1 = int(rng.choice(np.arange(5, 31, 5))), int(rng.choice(np.arange(50, 91, 5)))
        good, bad = opt((a1, b1)), opt((a1 + 10, b1 + 10))
        left = int(rng.random() < 0.5)
        add("A", "A_dominated", "check", *((good, bad) if left else (bad, good)), good_option=0 if left else 1)

    rest = [t["id"] for t in trials if t["block"] != "R"]
    rng.shuffle(rest)
    order = [t["id"] for t in trials if t["block"] == "R"] + rest
    for pos, tid in enumerate(order):
        trials[tid]["order"] = pos
    return trials


if __name__ == "__main__":
    tr = build()
    json.dump({"seed": SEED, "trials": tr}, open(sys.argv[1], "w"), indent=1)
    print({blk: sum(t["block"] == blk for t in tr) for blk in "RSXA"})
