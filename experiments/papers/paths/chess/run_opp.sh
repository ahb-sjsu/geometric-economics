#!/bin/bash
# Memory curve with pairs a day apart and opponents rated within 50 points. Two cores.
W=/archive/experiments/paths/chess
cd "$W/src" || exit 1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
taskset -c 22 nice -n 19 /home/claude/env/bin/python3 analyze_memory.py "$W/rows/within_2026-07.tsv.gz" "$W/results/memory_gap24_opp50_2026-07.json" 24 50 > "$W/opp_07.out" 2>&1 &
taskset -c 23 nice -n 19 /home/claude/env/bin/python3 analyze_memory.py "$W/rows/within_2026-08.tsv.gz" "$W/results/memory_gap24_opp50_2026-08.json" 24 50 > "$W/opp_08.out" 2>&1 &
wait
echo "OPP_DONE $(date -u +%FT%TZ)"
