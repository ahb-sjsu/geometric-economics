#!/bin/bash
# Memory curve with pairs at least 24 hours apart, both development months, two cores.
W=/archive/experiments/paths/chess
cd "$W/src" || exit 1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
taskset -c 22 nice -n 19 /home/claude/env/bin/python3 analyze_memory.py "$W/rows/within_2026-07.tsv.gz" "$W/results/memory_gap24_2026-07.json" 24 > "$W/gap_07.out" 2>&1 &
taskset -c 23 nice -n 19 /home/claude/env/bin/python3 analyze_memory.py "$W/rows/within_2026-08.tsv.gz" "$W/results/memory_gap24_2026-08.json" 24 > "$W/gap_08.out" 2>&1 &
wait
echo "GAP_DONE $(date -u +%FT%TZ)"
