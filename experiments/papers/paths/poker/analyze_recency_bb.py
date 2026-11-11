"""The registered contrasts within one range of big blind. Written after the sealed result.

    python analyze_recency_bb.py hands.tsv.gz out.json site LO HI

Section 6 of prereg-poker-recency-v1.md lists "the contrasts by big blind level"
as reported without a bar. This file was written on 2026-11-11 after H1 to H4
were graded. The three ranges used (under 1 dollar, 1 to under 5, 5 and over)
were chosen then, from the counts of rows by big blind on the two held-out
sites and before any contrast by level was computed. Everything else is
analyze_recency.py at its registered settings (threshold 10 big blinds, coarse
stack bins, no table in the cell), which is imported and not changed. Only
hands with LO <= big blind < HI are read.
"""
import gzip
import os
import sys
import tempfile

import analyze_recency


def main(rows, out, site, lo, hi):
    fd, tmp = tempfile.mkstemp(suffix=".tsv.gz", dir=os.path.dirname(os.path.abspath(out)))
    os.close(fd)
    try:
        with gzip.open(rows, "rt") as f, gzip.open(tmp, "wt", compresslevel=1) as g:
            for line in f:
                r = line.split("\t", 2)
                if r[0] == site and lo <= float(r[1]) < hi:
                    g.write(line)
        analyze_recency.main(tmp, out, analyze_recency.THRESH, 0, site, False)
    finally:
        os.remove(tmp)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5]))
