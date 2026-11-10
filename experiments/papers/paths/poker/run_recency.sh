#!/bin/bash
# The baseline-free contrast on the development sites under four specifications. Two cores.
W=/archive/experiments/paths/poker
cd "$W" || exit 1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=/home/claude/env/bin/python3
R=rows/dev_hands.tsv.gz
( taskset -c 22 nice -n 19 $PY analyze_recency.py $R results/recency_dev_bin10_table.json 10 10 all table > /dev/null 2>&1
  taskset -c 22 nice -n 19 $PY analyze_recency.py $R results/recency_dev_coarse.json 10 0 all > /dev/null 2>&1 ) &
( taskset -c 23 nice -n 19 $PY analyze_recency.py $R results/recency_dev_bin10.json 10 10 all > /dev/null 2>&1
  taskset -c 23 nice -n 19 $PY analyze_recency.py $R results/recency_dev_coarse_table.json 10 0 all table > /dev/null 2>&1 ) &
wait
echo "RECENCY_DONE $(date -u +%FT%TZ)"
