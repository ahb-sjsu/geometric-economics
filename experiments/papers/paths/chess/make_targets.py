"""List every move order seen for the positions that had two usable orders in the sample.

    python make_targets.py results/dev_2026-07.json rows/paths_2026-07.tsv.gz targets.tsv

Reads the positions that entered any comparison in the sampled analysis, then
scans the sampled rows for every distinct move order that reached one of them.
The output has one line per order: ply, position key, the moves in order.
mine_targets.py then pulls every game of a month that follows one of these
orders, by matching text, with no chess library in the loop.
"""
import gzip
import json
import sys


def main(result, rows, out):
    d = json.load(open(result))
    keys = {(r["zkey"], r["ply"]) for kind in d["pairs"].values() for r in kind}
    seen = {}
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.split("\t", 4)
            k = (r[2], int(r[1]))
            if k in keys:
                seen[(k, r[3])] = seen.get((k, r[3]), 0) + 1
    with open(out, "w") as f:
        for ((zkey, ply), path), n in sorted(seen.items(), key=lambda x: (x[0][0], -x[1])):
            f.write("%d\t%s\t%s\t%d\n" % (ply, zkey, path, n))
    print("positions", len(keys), "orders", len(seen))


if __name__ == "__main__":
    main(*sys.argv[1:4])
