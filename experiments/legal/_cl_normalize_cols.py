#!/usr/bin/env python3
"""Like _cl_normalize.py but emits only selected column indices (0-based) -- for the lean opinions
load (drop the 6 redundant html/xml text renderings, keep plain_text + html_with_citations).

    bzcat opinions.csv.bz2 | python3 _cl_normalize_cols.py 0 4 6 7 8 11 18 19 20 21 | psql ... \\copy ...
"""
import csv, sys

csv.field_size_limit(1 << 28)
cols = [int(x) for x in sys.argv[1:]]
r = csv.reader(sys.stdin, escapechar="\\")
w = csv.writer(sys.stdout, lineterminator="\n")
try:
    for row in r:
        w.writerow([row[i] if i < len(row) else "" for i in cols])
except BrokenPipeError:
    sys.exit(0)
