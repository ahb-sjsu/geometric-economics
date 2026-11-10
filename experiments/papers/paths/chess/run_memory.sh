#!/bin/bash
# Memory curve for each month whose within-player rows are ready. Waits for them. One core.
W=/archive/experiments/paths/chess
cd "$W/src" || exit 1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
for M in 2026-07 2026-08; do
  while [ ! -s "$W/results/within_${M}.json" ]; do sleep 30; done
  echo "start $M $(date -u +%FT%TZ)"
  taskset -c 23 nice -n 19 /home/claude/env/bin/python3 analyze_memory.py \
    "$W/rows/within_${M}.tsv.gz" "$W/results/memory_${M}.json"
  echo "MEMORY_EXIT_${M}=$? $(date -u +%FT%TZ)"
done
