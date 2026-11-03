#!/usr/bin/env python3
"""The stimulus set of the correlation-attitude design (DESIGN.md). Deterministic from SEED.

    python stimuli.py OUT.json

Units are points. `a` is the self shortfall (100 minus self points) and `b` the charity shortfall
(100 minus charity points), so the ideal is (0, 0). An option has one outcome (sure) or two at even
odds, each outcome an (a, b) pair. Within every trial of the main set (R, S, X, A) all outcomes sit on
one side of a = b, so no main trial crosses self = charity and inequality aversion is linear inside
each. The crossing set (XC, SC) crosses on purpose.

  R  40 riskless pairs, neither option dominating. Locations a in 5..40 and b in 50..100; tradeoff
     ratios of 0.5, 1, 2 and 3 charity points per self point, 10 pairs each.        role calib
  S  48 even-odds lotteries against a sure amount on one attribute. Self lotteries at charity
     shortfall b = 0, 50, 75, 100; charity lotteries at self shortfall a = 0, 10, 25, 40. The b = 0
     and a = 0 cells (12 each) are calibration, because the metric adds nothing there; the rest (4
     per level) are test. Version 2 had 4 calibration lotteries per attribute (32 S trials).
  X  24 correlation pairs: equal marginals, correlated against anticorrelated, 12 configurations
     in both left-right orders.                                                       role test
  A  8 dominated riskless pairs, attention checks.                                    role check
  XC 8 crossing correlation pairs (version 4): the correlated option pays equal splits (a = b in both
     outcomes), the anticorrelated one pays one split favouring self and one favouring the charity;
     4 spreads in both orders.                                                   role secondary
  SC 12 straddle lotteries (version 4): an even-odds lottery against its expected value on one
     attribute, the other attribute at 50; sure shortfalls 25, 50 and 75 with spreads 10 and 20. At 50
     the outcomes straddle self = charity (`straddle`); 25 and 75 are the controls.  role secondary

Option 0 is shown on the left. S and SC trials record which option is the lottery (`lot_option`), X and
XC trials which is the correlated one (`corr_option`). `order` is the presentation order: R first,
then everything else shuffled together. Only the crossing set (`cross`) crosses self = charity.

The pilot (PILOT.md) adds 20 trials after the main set, role "pilot", from their own random stream, so
build() is unchanged (`pilot_extras`). `presentation` gives one participant's order from their recorded
seed; `order` is one such shuffle. `digest` is the hash the instrument's export must declare.
"""
import hashlib
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
        assert extra.get("cross") or one_side(t), t
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

    # S: single-attribute lotteries against a sure amount. At the other attribute's ideal there are 12 per
    # attribute (version 3; version 2 had 4): fitted kappa from 4 is biased upward by small samples
    # (REHEARSAL.md). Off the ideal there are 4 per level, as before.
    self_cells = (((5, 35), 15), ((5, 35), 25), ((10, 40), 20), ((10, 40), 30),
                  ((5, 25), 10), ((5, 25), 20), ((15, 35), 20), ((15, 35), 30),
                  ((20, 40), 25), ((20, 40), 35), ((5, 40), 15), ((5, 40), 30))
    charity_cells = (((50, 100), 65), ((50, 100), 85), ((60, 100), 70), ((60, 100), 90),
                     ((50, 80), 60), ((50, 80), 70), ((70, 100), 80), ((70, 100), 90),
                     ((50, 70), 55), ((50, 70), 65), ((60, 90), 70), ((60, 90), 80))
    # `matched` marks the 4 lotteries that appear at every level. A model-free comparison across levels
    # must use only those, or it compares different gambles (the version 3 rehearsal found this).
    for b in (0, 50, 75, 100):
        for k, ((lo, hi), sure) in enumerate(self_cells if b == 0 else self_cells[:4]):
            left = int(rng.random() < 0.5)
            lot, s = opt((lo, b), (hi, b)), opt((sure, b))
            add("S", f"S_self_b{b}", "calib" if b == 0 else "test", *((lot, s) if left else (s, lot)),
                lot_option=0 if left else 1, side="self", level=b, matched=k < 4)
    for a in (0, 10, 25, 40):
        for k, ((lo, hi), sure) in enumerate(charity_cells if a == 0 else charity_cells[:4]):
            left = int(rng.random() < 0.5)
            lot, s = opt((a, lo), (a, hi)), opt((a, sure))
            add("S", f"S_charity_a{a}", "calib" if a == 0 else "test", *((lot, s) if left else (s, lot)),
                lot_option=0 if left else 1, side="charity", level=a, matched=k < 4)

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

    # XC and SC: the crossing set (version 4; DESIGN.md, secondary). Outcomes cross self = charity on
    # purpose, so inequality aversion, linear inside the main set, shows its kink here. Role "secondary":
    # H1 to H4 never see these trials. Sides come from a separate stream, so the main set's draws are
    # unchanged; the main trials keep their ids and contents.
    rng2 = np.random.default_rng([SEED, 2])
    for lo, hi in ((10, 50), (20, 60), (30, 70), (40, 80)):
        cor = opt((lo, lo), (hi, hi))          # equal splits in both outcomes
        anti = opt((lo, hi), (hi, lo))         # one outcome favours self, the other the charity
        add("XC", f"XC_s{lo}-{hi}", "secondary", cor, anti, corr_option=0, cross=True)
        add("XC", f"XC_s{lo}-{hi}", "secondary", anti, cor, corr_option=1, cross=True)
    for side in ("self", "charity"):
        for level in (25, 50, 75):             # sure shortfall on the varied attribute; the other is at 50
            for d in (10, 20):
                lo, hi = level - d, level + d
                if side == "self":
                    lot, s = opt((lo, 50), (hi, 50)), opt((level, 50))
                else:
                    lot, s = opt((50, lo), (50, hi)), opt((50, level))
                left = int(rng2.random() < 0.5)
                add("SC", f"SC_{side}_{level}_d{d}", "secondary", *((lot, s) if left else (s, lot)),
                    lot_option=0 if left else 1, side=side, level=level, spread=d, straddle=level == 50,
                    cross=True)

    rest = [t["id"] for t in trials if t["block"] != "R"]
    rng.shuffle(rest)
    order = [t["id"] for t in trials if t["block"] == "R"] + rest
    for pos, tid in enumerate(order):
        trials[tid]["order"] = pos
    return trials


def self_option(trial):
    """The self-favouring option of a riskless tradeoff pair (R, PR, PW): the one with the smaller self
    shortfall."""
    return int(trial["options"][1][0][1] < trial["options"][0][0][1])


def pilot_extras(trials=None):
    """The 20 pilot-only trials (PILOT.md), shown after the main set and numbered after it, role "pilot".

      PR  8 repeats: two block R pairs from each tradeoff ratio, shown again with the sides swapped
          (`repeat_of`). Agreement with the first answer measures choice noise without a model.
      PW  8 wide-ratio riskless pairs at block R's locations: 4 offer the charity 30 points for 5 of the
          participant's own (ratio 6), 4 offer 5 for 20 (ratio 1/4).
      PS  4 even-odds lotteries at the ideal whose sure amount is 12 to 15 points worse than the
          lottery's expected value (`premium`), two per attribute. For any kappa up to 4 the lottery
          has the lower expected cost.
    """
    trials = build() if trials is None else trials
    rng3 = np.random.default_rng([SEED, 3])
    extra = []

    def add(block, cell, o0, o1, **kw):
        t = {"id": len(trials) + len(extra), "block": block, "cell": cell, "role": "pilot", "options": [o0, o1], **kw}
        assert one_side(t), t
        extra.append(t)

    for ratio in (0.5, 1, 2, 3):
        cell = [t for t in trials if t["cell"] == f"R_ratio{ratio}"]
        for k in sorted(rng3.choice(len(cell), 2, replace=False)):
            t = cell[int(k)]
            add("PR", f"PR_ratio{ratio}", t["options"][1], t["options"][0], repeat_of=t["id"],
                self_option=1 - self_option(t))
    seen = set()
    for da, db, name in ((5, 30, "PW_ratio6"), (20, 5, "PW_ratio0.25")):
        while sum(t["cell"] == name for t in extra) < 4:
            a1 = int(rng3.choice(np.arange(5, 41 - da, 5)))
            b2 = int(rng3.choice(np.arange(50, 101 - db, 5)))
            if (a1, b2, da) in seen:
                continue
            seen.add((a1, b2, da))
            pair = (opt((a1, b2 + db)), opt((a1 + da, b2)))      # self-favouring first
            left = int(rng3.random() < 0.5)
            add("PW", name, *(pair if left else pair[::-1]), self_option=0 if left else 1, ratio=db / da)
    for side, (lo, hi), sure in (("self", (5, 35), 32), ("self", (10, 40), 37),
                                 ("charity", (50, 100), 90), ("charity", (60, 100), 92)):
        if side == "self":
            lot, s = opt((lo, 0), (hi, 0)), opt((sure, 0))
        else:
            lot, s = opt((0, lo), (0, hi)), opt((0, sure))
        left = int(rng3.random() < 0.5)
        add("PS", f"PS_{side}", *((lot, s) if left else (s, lot)), lot_option=0 if left else 1, side=side,
            level=0, premium=sure - (lo + hi) / 2)
    for pos, k in enumerate(rng3.permutation(len(extra))):
        extra[int(k)]["order"] = len(trials) + pos
    return extra


def presentation(seed, trials=None, extras=None):
    """One participant's order of trial ids (PILOT.md): block R first, then the rest of the main set
    interleaved, then the pilot-only trials (none in the main study: extras=[]), each part shuffled
    afresh from the participant's recorded seed."""
    trials = build() if trials is None else trials
    extras = pilot_extras(trials) if extras is None else extras
    rng = np.random.default_rng([SEED, 4, int(seed)])
    parts = ([t["id"] for t in trials if t["block"] == "R"], [t["id"] for t in trials if t["block"] != "R"],
             [t["id"] for t in extras])
    return [int(i) for part in parts for i in (rng.permutation(part) if part else [])]


def digest(trials=None, extras=None):
    """sha256 of the stimulus set as the instrument shows it, the main set and the pilot-only trials."""
    trials = build() if trials is None else trials
    extras = pilot_extras(trials) if extras is None else extras
    return hashlib.sha256(json.dumps(trials + extras, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


if __name__ == "__main__":
    tr = build()
    ex = pilot_extras(tr)
    json.dump({"seed": SEED, "trials": tr, "pilot_extras": ex, "sha256": digest(tr, ex)}, open(sys.argv[1], "w"), indent=1)
    print({blk: sum(t["block"] == blk for t in tr + ex) for blk in ("R", "S", "X", "A", "XC", "SC", "PR", "PW", "PS")})
