#!/usr/bin/env bash
# Validate NATIVE Postgres COPY (fast, no Python) on a 100k-row sample of the opinions file:
# all-text target (so quoted-empty "" is valid text, no type errors) + ESCAPE '\' (handles
# backslash-escaped quotes and doubled-quotes; fixes the embedded-CR desync too).
set -uo pipefail
DB=courtlistener; PG="sudo -u postgres psql"; BULK=/archive/courtlistener/bulk; DUMP=2026-06-30

echo "[test] kill any slow opinions load ($(date))"
ps -eo pid,cmd | grep -E "opinions-$DUMP|_cl_normalize|copy search_opinion|load_opinions" \
  | grep -v grep | awk '{print $1}' | xargs -r sudo kill 2>/dev/null || true
sleep 2

echo "[test] native COPY of FULL originating (has backslash-quotes), all-text + ESCAPE backslash:"
cols=$(python3 -c "print(','.join('c%d text'%i for i in range(16)))")
$PG -d "$DB" -c "DROP TABLE IF EXISTS scratch_orig;"
$PG -d "$DB" -c "CREATE TABLE scratch_orig ($cols);"
time $PG -d "$DB" -c "COPY scratch_orig FROM PROGRAM 'bzcat $BULK/originating-court-information-$DUMP.csv.bz2' WITH (FORMAT csv, HEADER true, ESCAPE '\');"
echo -n "[test] rows loaded (expect 973419): "
$PG -d "$DB" -tc "SELECT count(*) FROM scratch_orig;"
$PG -d "$DB" -c "DROP TABLE scratch_orig;"
echo "[test] done"
