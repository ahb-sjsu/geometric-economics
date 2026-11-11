#!/bin/bash
# Pass 6: the last-move effect at two speeds, same player and same position. Two cores.
cd /archive/experiments/paths/chess/src || exit 1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=/home/claude/env/bin/python3
taskset -c 22 nice -n 19 $PY analyze_cross_speed.py ../rows/within_2026-07.tsv.gz ../results/cross_speed_matched_2026-07.json 24 matched > ../matched_07.out 2>&1 &
taskset -c 23 nice -n 19 $PY analyze_cross_speed.py ../rows/within_2026-08.tsv.gz ../results/cross_speed_matched_2026-08.json 24 matched > ../matched_08.out 2>&1 &
wait
echo "MATCHED_DONE $(date -u +%FT%TZ)"
