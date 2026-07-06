#!/usr/bin/env python3
"""Diagnose CourtListener bulk CSV format: read stdin, report field-count anomalies vs expected,
and infer the quote-escaping convention. Usage: bzcat file.csv.bz2 | python3 _cl_diag.py [expected_ncols]"""
import csv, sys

expected = int(sys.argv[1]) if len(sys.argv) > 1 else None
bad = 0
rows = 0
sample_bad = []
# raise field size limit for big opinion text
csv.field_size_limit(10_000_000)
for i, r in enumerate(csv.reader(sys.stdin)):
    rows += 1
    if i == 0:
        expected = expected or len(r)
        print(f"header ncols = {len(r)}")
        continue
    if len(r) != expected:
        bad += 1
        if len(sample_bad) < 5:
            sample_bad.append((i, len(r)))
    if i > 500000:
        break
print(f"rows read = {rows}, expected_ncols = {expected}, bad_rows = {bad}")
for i, n in sample_bad:
    print(f"  row {i}: {n} fields")
print("VERDICT:", "standard CSV (python parses cleanly)" if bad == 0
      else "NON-standard escaping (python also desyncs)")
