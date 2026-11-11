"""Raw rates of raising by lag, with no cells and no per-player step. A diagnostic.

    python null_raw.py hands.tsv.gz out.json [site]

Uses the registered `decisions` generator unchanged. For each kind of large pot
and each lag, the share of decisions that were a raise, pooled over everyone,
and the same within each stack bin. Written on 2026-11-11 to find out why the
registered contrast returns a non-zero value on simulated players whose
actions are drawn independently of the past.
"""
import json
import sys
from collections import defaultdict

from analyze_lags import THRESH, stack_bin
from analyze_recency import decisions


def main(rows, out, site=""):
    acc = defaultdict(lambda: [0, 0])
    for p, s, bb, table, seat, n, faced, stack, act, event, lag in decisions(rows, THRESH, site):
        for k in ("%s lag%d" % (event, lag), "%s lag%d faced%s" % (event, lag, faced),
                  "%s lag%d bin%d" % (event, lag, stack_bin(stack, 0))):
            acc[k][0] += act == "r"
            acc[k][1] += 1
    res = {k: {"raise_rate": v[0] / v[1], "n": v[1]} for k, v in sorted(acc.items())}
    json.dump(res, open(out, "w"), indent=1)
    for k, v in res.items():
        print("%-22s %.4f %d" % (k, v["raise_rate"], v["n"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
