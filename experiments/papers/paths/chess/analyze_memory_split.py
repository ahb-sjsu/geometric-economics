"""The registered curve D(k) on a subset of rows or of pairs. Written after the sealed result.

    python analyze_memory_split.py within_rows.tsv.gz out.json WHAT

WHAT is one of
    speed=bullet | speed=blitz | speed=rapid | speed=classical
    band=LO-HI       only games in which the mover's rating was LO <= rating < HI
    diffopp          only pairs of games against two different opponents

Section 6 of prereg-chess-memory-v1.md lists these curves as reported without a
bar. This file was written on 2026-11-11 after H1 to H5 were graded, so the
rating bands and every other choice here were made with the result known. The
pairing, the 24 hour minimum between the two games of a pair, the cap of 40
games, the baseline and the bootstrap are those of analyze_memory.py, whose
functions are imported and not changed. The filter applies to every class of
pair, the identical-order baseline included.

Only the curve in which the player's own moves came in the same order
(`own_same`, the registered one) and the curve over all pairs are written.
"""
import gzip
import itertools
import json
import sys
from collections import defaultdict

import numpy as np

from analyze_memory import KMAX, MAX_GAMES, SEED, minutes, suffix
from analyze_paths import speed

GAP = 24 * 60


def main(rows, out, what):
    only_speed, lo, hi, diffopp = "", 0, 10 ** 6, False
    if what.startswith("speed="):
        only_speed = what[6:]
    elif what.startswith("band="):
        lo, hi = (int(x) for x in what[5:].split("-"))
    elif what == "diffopp":
        diffopp = True
    else:
        raise SystemExit("unknown subset " + what)
    rng = np.random.default_rng(SEED)
    by = defaultdict(list)
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            sp = speed(r[8])
            if sp is None or (only_speed and sp != only_speed) or not lo <= int(r[6]) < hi:
                continue
            by[(r[2], int(r[1]), r[5], sp)].append((tuple(r[3].split(" ")), r[4], minutes(r[10]), r[12] if diffopp else ""))
    acc = {"own_same": defaultdict(lambda: defaultdict(lambda: [0, 0])),
           "all": defaultdict(lambda: defaultdict(lambda: [0, 0]))}
    for (zkey, ply, mover, sp), g in by.items():
        if len(g) < 2:
            continue
        if len(g) > MAX_GAMES:
            g = [g[i] for i in rng.choice(len(g), MAX_GAMES, replace=False)]
        side = ply % 2
        for (pa, ma, ta, oa), (pb, mb, tb, ob) in itertools.combinations(g, 2):
            if abs(ta - tb) < GAP or (diffopp and oa == ob):
                continue
            changed = ma != mb
            if pa == pb:
                for c in acc.values():
                    cell = c[(mover, zkey)]["same"]
                    cell[0] += changed
                    cell[1] += 1
                continue
            k = min(suffix(pa, pb), KMAX)
            for name in ["all"] + (["own_same"] if pa[side::2] == pb[side::2] else []):
                cell = acc[name][(mover, zkey)][k]
                cell[0] += changed
                cell[1] += 1
    res = {"subset": what, "written_after_the_result": True}
    for name, c in acc.items():
        curve = {}
        for k in range(KMAX + 1):
            per_player, base, n_pairs = defaultdict(list), [], 0
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
        res[name] = curve
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res["own_same"], indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
