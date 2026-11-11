"""Development analysis, pass 8: the pull of pass 7 by the time spent on the move.

    python analyze_pull_time.py movetime_rows.tsv.gz out.json

Rows come from mine_movetime.py. Time spent is the mover's clock before the
move, minus the clock after it, plus the increment, in whole seconds. Within
each speed the pull of analyze_pull.py is computed on two sets of games: moves
that took zero seconds ("zero") and moves that took two seconds or more
("slow"). One-second moves are left out. Both groups of a pair come from the
same set. Also reported: slow minus zero over players who have both.
"""
import gzip
import itertools
import json
import sys
from collections import Counter, defaultdict

import numpy as np

from analyze_paths import speed
from analyze_pull import MIN_PLAYERS, SEED, dest, dist


def interval(v, rng):
    boots = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(2000)]
    return [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]


def main(rows, out):
    rng = np.random.default_rng(SEED)
    cells = defaultdict(lambda: defaultdict(lambda: defaultdict(Counter)))
    skipped = Counter()
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            sp = speed(r[8])
            if sp is None:
                continue
            before, after = int(r[9]), int(r[13])
            if before < 0 or after < 0:
                skipped["no_clock"] += 1
                continue
            try:
                inc = int(r[8].split("+")[1])
            except (IndexError, ValueError):
                skipped["no_increment"] += 1
                continue
            spent = before - after + inc
            if spent < 0:
                skipped["negative_time"] += 1
                continue
            if spent == 1:
                skipped["one_second"] += 1
                continue
            cls = "zero" if spent == 0 else "slow"
            ply = int(r[1])
            path = r[3].split(" ")
            white = ply % 2 == 0
            if dest(path[-1], not white) is None or dest(r[4], white) is None:
                skipped["unread_square"] += 1
                continue
            own = " ".join(path[ply % 2::2])
            cells[(r[5], sp, cls)][(r[2], ply, own)][path[-1]][r[4]] += 1
    per = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0, 0]))   # (speed, class) -> mover -> [sum w*pull, sum w, pairs]
    for (mover, sp, cls), positions in cells.items():
        for (zkey, ply, own), groups in positions.items():
            if len(groups) < 2:
                continue
            white = ply % 2 == 0
            for (la, ca), (lb, cb) in itertools.combinations(sorted(groups.items()), 2):
                a, b = dest(la, not white), dest(lb, not white)
                if a == b:
                    continue

                def mean_x(c):
                    n = sum(c.values())
                    return sum(k * (dist(dest(m, white), b) - dist(dest(m, white), a)) for m, k in c.items()) / n, n

                (xa, na), (xb, nb) = mean_x(ca), mean_x(cb)
                w = min(na, nb)
                cell = per[(sp, cls)][mover]
                cell[0] += w * (xa - xb)
                cell[1] += w
                cell[2] += 1
    res = {"skipped": dict(skipped), "pull": {}}
    for sp in sorted({k[0] for k in per}):
        entry = {}
        vals = {}
        for cls in ("zero", "slow"):
            d = {m: c[0] / c[1] for m, c in per.get((sp, cls), {}).items()}
            vals[cls] = d
            v = np.array(list(d.values()))
            if len(v) < MIN_PLAYERS:
                entry[cls] = {"players": int(len(v))}
                continue
            entry[cls] = {"players": int(len(v)),
                          "group_pairs": int(sum(c[2] for c in per[(sp, cls)].values())),
                          "pull_king_steps": float(v.mean()), "ci95": interval(v, rng)}
        both = sorted(set(vals["zero"]) & set(vals["slow"]))
        if len(both) >= MIN_PLAYERS:
            d = np.array([vals["slow"][m] - vals["zero"][m] for m in both])
            entry["slow_minus_zero"] = {"players": int(len(d)), "difference": float(d.mean()),
                                        "ci95": interval(d, rng)}
        else:
            entry["slow_minus_zero"] = {"players": len(both)}
        res["pull"][sp] = entry
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
