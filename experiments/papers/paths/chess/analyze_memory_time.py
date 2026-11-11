"""Development analysis, pass 9: the registered curve by the time spent on the move.

    python analyze_memory_time.py movetime_rows.tsv.gz out_prefix work_dir

Splits rows from mine_movetime.py into games whose chosen move took two seconds
or more ("slow") and games where it took zero seconds ("zero"), by the rule of
analyze_pull_time.py, then runs the registered analysis unchanged on each:
analyze_memory.main(rows, out, 24). Writes out_prefix_slow.json and
out_prefix_zero.json.
"""
import gzip
import os
import sys

import analyze_memory


def main(rows, prefix, work):
    paths = {c: os.path.join(work, "movetime_split_%s.tsv.gz" % c) for c in ("slow", "zero")}
    outs = {c: gzip.open(p, "wt", compresslevel=1) for c, p in paths.items()}
    n = {"slow": 0, "zero": 0}
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            before, after = int(r[9]), int(r[13])
            if before < 0 or after < 0:
                continue
            try:
                inc = int(r[8].split("+")[1])
            except (IndexError, ValueError):
                continue
            spent = before - after + inc
            if spent < 0 or spent == 1:
                continue
            c = "zero" if spent == 0 else "slow"
            outs[c].write(line)
            n[c] += 1
    for o in outs.values():
        o.close()
    print(n, flush=True)
    for c in ("slow", "zero"):
        analyze_memory.main(paths[c], "%s_%s.json" % (prefix, c), 24.0)
        os.remove(paths[c])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
