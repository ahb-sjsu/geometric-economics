"""Development analysis: how far back does history reach? One curve.

    python analyze_memory.py within_rows.tsv.gz out.json [min_gap_hours [max_opp_diff]]

With `max_opp_diff`, only pairs whose two opponents were rated within that many
points of each other are used, so that a player adapting to a stronger or weaker
opponent cannot stand in for an effect of history.

With `min_gap_hours`, only pairs of games at least that far apart in time are
used, in every class including the identical-order baseline. Two games minutes
apart are often a rematch in which a player repeats a line, and such pairs are
more common among identical orders, which would lower the baseline and raise
every D(k) by the same amount.

`../lean/DecisionPaths.lean` proves that if edge weights read a reference that
moves with the past, history matters only through that reference
(`ranking_depends_on_state_and_reference`), and that a reference equal to the
previous state is fixed by the last step
(`last_step_suffices_when_reference_is_previous_state`). In general, a reference
that reads no further back than m steps cannot produce any effect of history
between two games that share their last m half-moves.

So for one player at one position, take every pair of that player's games and
let k be the number of final half-moves the two move orders share (k = 0 when the
last half-move differs). The outcome is whether the player chose a different
next move. D(k) is that rate among pairs with suffix k, minus the rate among
pairs whose whole move order was identical, averaged over players who have both.

    D(k) = 0 for every k        no history beyond the state (Definition 6.2 as written)
    D(0) > 0, D(k >= 1) = 0     the reference is the previous state
    D(k) falling to 0 at k = m  a reference with memory m

Two curves are reported. In `own_same` the player's own moves came in the same
order in both games, so the difference between the games was not the player's
doing. `all` includes pairs where the player's own order differed, which can
reflect a different plan and not only a different past.
"""
import gzip
import itertools
import json
import sys
from collections import defaultdict

import numpy as np

from analyze_paths import speed

SEED = 20261110
MAX_GAMES = 40
KMAX = 5


def suffix(a, b):
    k = 0
    while k < len(a) and a[-1 - k] == b[-1 - k]:
        k += 1
    return k


def minutes(stamp):
    """Minutes since 2026-01-01 from 'YYYY.MM.DD HH:MM:SS'. Months are within one year."""
    d, t = stamp.split(" ")
    y, mo, da = (int(x) for x in d.split("."))
    h, mi, _ = (int(x) for x in t.split(":"))
    return (((mo - 1) * 31 + da) * 24 + h) * 60 + mi


def main(rows, out, min_gap_hours=0.0, max_opp_diff=0):
    rng = np.random.default_rng(SEED)
    gap = min_gap_hours * 60
    by = defaultdict(list)
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            sp = speed(r[8])
            if sp is not None:
                by[(r[2], int(r[1]), r[5], sp)].append((tuple(r[3].split(" ")), r[4], minutes(r[10]), int(r[7])))
    # (curve, mover) -> key -> [changed, pairs]; key is "same" or k
    acc = {"own_same": defaultdict(lambda: defaultdict(lambda: [0, 0])),
           "all": defaultdict(lambda: defaultdict(lambda: [0, 0]))}
    for (zkey, ply, mover, sp), g in by.items():
        if len(g) < 2:
            continue
        if len(g) > MAX_GAMES:
            g = [g[i] for i in rng.choice(len(g), MAX_GAMES, replace=False)]
        side = ply % 2
        for (pa, ma, ta, oa), (pb, mb, tb, ob) in itertools.combinations(g, 2):
            if abs(ta - tb) < gap:
                continue
            if max_opp_diff and abs(oa - ob) > max_opp_diff:
                continue
            changed = ma != mb
            if pa == pb:
                for c in acc.values():
                    cell = c[(mover, zkey)]["same"]
                    cell[0] += changed
                    cell[1] += 1
                continue
            k = min(suffix(pa, pb), KMAX)
            curves = ["all"] + (["own_same"] if pa[side::2] == pb[side::2] else [])
            for name in curves:
                cell = acc[name][(mover, zkey)][k]
                cell[0] += changed
                cell[1] += 1
    res = {}
    for name, c in acc.items():
        curve = {}
        means = {}
        rng2 = np.random.default_rng(SEED + 1)     # separate stream, so the curve's intervals do not move
        for k in range(KMAX + 1):
            per_player = defaultdict(list)
            base, n_pairs = [], 0
            for (mover, zkey), cells in c.items():
                if cells["same"][1] == 0 or cells[k][1] == 0:
                    continue
                r0 = cells["same"][0] / cells["same"][1]
                per_player[mover].append(cells[k][0] / cells[k][1] - r0)
                base.append(r0)
                n_pairs += cells[k][1]
            if len(per_player) < 30:
                curve[str(k)] = {"players": len(per_player)}
                continue
            v = np.array([np.mean(x) for x in per_player.values()])
            boots = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(2000)]
            curve[str(k)] = {"players": int(len(v)), "pairs": int(n_pairs),
                             "baseline_change_rate": float(np.mean(base)), "D": float(v.mean()),
                             "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}
            means[k] = {m: float(np.mean(x)) for m, x in per_player.items()}
        # the fall from one point of the curve to the next, over players who have both
        for a, b in ((0, 2), (2, 4)):
            both = sorted(set(means.get(a, {})) & set(means.get(b, {})))
            if len(both) < 30:
                curve["%d_minus_%d" % (a, b)] = {"players": len(both)}
                continue
            d = np.array([means[a][m] - means[b][m] for m in both])
            boots = [d[rng2.integers(0, len(d), len(d))].mean() for _ in range(2000)]
            curve["%d_minus_%d" % (a, b)] = {
                "players": int(len(d)), "difference": float(d.mean()),
                "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}
        res[name] = curve
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.0,
         int(sys.argv[4]) if len(sys.argv) > 4 else 0)
