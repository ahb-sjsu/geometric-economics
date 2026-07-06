#!/usr/bin/env python3
"""Normalize a CourtListener bulk CSV stream to canonical CSV that Postgres COPY accepts.

Python's csv parses these files cleanly (verified: 0 field-count anomalies) where Postgres CSV
desyncs on quotes/embedded newlines. Read with Python's reader, re-emit canonical CSV (doubled-quote
escaping, \n terminators). Streaming; safe for the 51 GB opinions file.

    bzcat file.csv.bz2 | python3 _cl_normalize.py | psql -c "\\copy tbl (...) FROM STDIN CSV HEADER"
"""
import csv, sys

csv.field_size_limit(1 << 28)   # opinion text fields are large
# CourtListener escapes some embedded quotes with a backslash (\"); escapechar handles that AND
# doubled-quotes. Reader parses the messy input; writer emits canonical doubled-quote CSV for Postgres.
r = csv.reader(sys.stdin, escapechar="\\")
w = csv.writer(sys.stdout, lineterminator="\n")
try:
    for row in r:
        w.writerow(row)
except BrokenPipeError:
    sys.exit(0)   # consumer (psql) closed early
