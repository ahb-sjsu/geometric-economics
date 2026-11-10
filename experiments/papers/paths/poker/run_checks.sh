#!/bin/bash
# Development checks: stack bins 10 big blinds wide, all sites and each site alone. Two cores.
W=/archive/experiments/paths/poker
cd "$W" || exit 1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=/home/claude/env/bin/python3
( taskset -c 22 nice -n 19 $PY analyze_lags.py rows/dev_hands.tsv.gz results/lags_dev_bin10.json 10 10 > /dev/null 2>&1
  taskset -c 22 nice -n 19 $PY analyze_lags.py rows/dev_hands.tsv.gz results/lags_dev_bin10_ABS.json 10 10 ABS > /dev/null 2>&1 ) &
( taskset -c 23 nice -n 19 $PY analyze_lags.py rows/dev_hands.tsv.gz results/lags_dev_bin10_FTP.json 10 10 FTP > /dev/null 2>&1
  taskset -c 23 nice -n 19 $PY analyze_lags.py rows/dev_hands.tsv.gz results/lags_dev_bin10_ONG.json 10 10 ONG > /dev/null 2>&1 ) &
wait
echo "CHECKS_DONE $(date -u +%FT%TZ)"
