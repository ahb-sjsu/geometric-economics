#!/bin/bash
# Pass 7 on both development months. Two cores, lowest priority, never core 0.
# Run on Atlas inside a named screen session.
W=/archive/experiments/paths/chess
cd "$W/src" || exit 1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=/home/claude/env/bin/python3
taskset -c 18 nice -n 19 $PY analyze_pull.py $W/rows/within_2026-07.tsv.gz $W/results/pull_2026-07.json > $W/pull_07.out 2>&1 &
taskset -c 19 nice -n 19 $PY analyze_pull.py $W/rows/within_2026-08.tsv.gz $W/results/pull_2026-08.json > $W/pull_08.out 2>&1 &
wait
tail -3 $W/pull_07.out $W/pull_08.out
echo "PULL_DONE $(date -u +%FT%TZ)"
