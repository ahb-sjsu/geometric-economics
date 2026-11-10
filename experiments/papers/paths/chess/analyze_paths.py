"""Development analysis: does the move order matter once the position is fixed?

Reads the rows written by mine_paths.py and, for each position reached by more
than one move order, compares the distribution of the next move between orders.
Development only. Nothing here is a registered test.

    python analyze_paths.py rows.tsv.gz out.json [--min-n 150] [--perms 200]

Three comparisons, each between two path classes at one position:

    own    the opponent's moves in the same order, the mover's own in a different order
    opp    the mover's own moves in the same order, the opponent's in a different order
    opp3   as opp, and the opponent's last move is the same in both

For a pair of classes the statistic is the total variation distance between the
two next-move distributions, minus its mean under random relabelling of the
pooled rows with class sizes kept. The raw distance is biased upward in small
samples and the subtraction removes that. Rows are first reduced to one per
player per position and class, and strata are rating band by speed category.
"""
import argparse
import gzip
import json
from collections import defaultdict

import numpy as np

COLS = ("gid", "ply", "zkey", "path", "move", "mover", "elo", "oelo", "tc", "clk")
SEED = 20261110


def speed(tc):
    try:
        base, inc = tc.split("+")
        est = int(base) + 40 * int(inc)
    except ValueError:
        return None
    if est < 30:
        return None
    return "bullet" if est < 180 else "blitz" if est < 480 else "rapid" if est < 1500 else "classical"


def tv(a, b, k):
    pa = np.bincount(a, minlength=k) / len(a)
    pb = np.bincount(b, minlength=k) / len(b)
    return 0.5 * np.abs(pa - pb).sum()


def excess(a, b, k, perms, rng):
    obs = tv(a, b, k)
    pool = np.concatenate([a, b])
    null = np.empty(perms)
    for i in range(perms):
        rng.shuffle(pool)
        null[i] = tv(pool[:len(a)], pool[len(a):], k)
    return obs, float(null.mean()), float(null.std()), float((null >= obs).mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rows")
    ap.add_argument("out")
    ap.add_argument("--min-n", type=int, default=150)
    ap.add_argument("--perms", type=int, default=200)
    a = ap.parse_args()
    rng = np.random.default_rng(SEED)

    # (zkey, ply, stratum) -> (own order, opponent order) -> {mover: move}
    cells = defaultdict(lambda: defaultdict(dict))
    n_rows = 0
    with gzip.open(a.rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            if len(r) != len(COLS):
                continue
            n_rows += 1
            ply, path = int(r[1]), r[3].split(" ")
            sp = speed(r[8])
            if sp is None:
                continue
            band = min(max(int(r[6]) // 400 * 400, 800), 2400)
            side = ply % 2
            own = " ".join(path[side::2])
            opp = " ".join(path[1 - side::2])
            cells[(r[2], ply, band, sp)][(own, opp)].setdefault(r[5], r[4])

    results = {"own": [], "opp": [], "opp3": []}
    for (zkey, ply, band, sp), classes in cells.items():
        big = {c: m for c, m in classes.items() if len(m) >= a.min_n}
        if len(big) < 2:
            continue
        keys = sorted(big, key=lambda c: -len(big[c]))
        moves = sorted({mv for m in big.values() for mv in m.values()})
        code = {mv: i for i, mv in enumerate(moves)}
        arr = {c: np.array([code[mv] for mv in big[c].values()]) for c in keys}
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                (own_a, opp_a), (own_b, opp_b) = keys[i], keys[j]
                if opp_a == opp_b and own_a != own_b:
                    kind = "own"
                elif own_a == own_b and opp_a != opp_b:
                    kind = "opp3" if opp_a.split(" ")[-1] == opp_b.split(" ")[-1] else "opp"
                else:
                    continue
                obs, mu, sd, p = excess(arr[keys[i]].copy(), arr[keys[j]].copy(), len(moves), a.perms, rng)
                both = len(set(big[keys[i]]) & set(big[keys[j]]))
                results[kind].append({
                    "zkey": zkey, "ply": ply, "band": band, "speed": sp,
                    "path_a": " | ".join(keys[i]), "path_b": " | ".join(keys[j]),
                    "n_a": len(arr[keys[i]]), "n_b": len(arr[keys[j]]), "players_in_both": both,
                    "tv": obs, "null_mean": mu, "null_sd": sd, "excess": obs - mu, "p_perm": p})

    summary = {"rows_read": n_rows, "cells": len(cells), "min_n": a.min_n, "perms": a.perms}
    for kind, rs in results.items():
        if not rs:
            summary[kind] = {"pairs": 0}
            continue
        ex = np.array([r["excess"] for r in rs])
        w = np.array([min(r["n_a"], r["n_b"]) for r in rs], float)
        positions = {r["zkey"] for r in rs}
        # interval by resampling positions, since pairs at one position share rows
        by_pos = defaultdict(list)
        for r, e, wi in zip(rs, ex, w):
            by_pos[r["zkey"]].append((e, wi))
        plist = list(by_pos.values())
        boots = []
        for _ in range(1000):
            pick = rng.integers(0, len(plist), len(plist))
            e = np.array([x[0] for i in pick for x in plist[i]])
            wi = np.array([x[1] for i in pick for x in plist[i]])
            boots.append((e * wi).sum() / wi.sum())
        summary[kind] = {
            "pairs": len(rs), "positions": len(positions),
            "mean_excess_weighted": float((ex * w).sum() / w.sum()),
            "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],
            "share_p_below_05": float(np.mean([r["p_perm"] < 0.05 for r in rs])),
            "median_tv": float(np.median([r["tv"] for r in rs])),
            "median_null": float(np.median([r["null_mean"] for r in rs]))}
    json.dump({"summary": summary, "pairs": results}, open(a.out, "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
