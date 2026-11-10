#!/bin/bash
# The registered analysis and its grader, run on both development months as the grader's self-test.
# Waits for the opponent-rating control to free the two cores.
W=/archive/experiments/paths/chess
cd "$W/src" || exit 1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
while ! grep -q OPP_DONE "$W/opp.log" 2>/dev/null; do sleep 30; done
PY=/home/claude/env/bin/python3
( taskset -c 22 nice -n 19 $PY analyze_memory.py "$W/rows/within_2026-07.tsv.gz" "$W/results/memory_reg_2026-07.json" 24 > "$W/reg_07.out" 2>&1
  $PY grade_memory.py "$W/results/memory_reg_2026-07.json" "$W/results/graded_dev_2026-07.json" ) &
( taskset -c 23 nice -n 19 $PY analyze_memory.py "$W/rows/within_2026-08.tsv.gz" "$W/results/memory_reg_2026-08.json" 24 > "$W/reg_08.out" 2>&1
  $PY grade_memory.py "$W/results/memory_reg_2026-08.json" "$W/results/graded_dev_2026-08.json" ) &
wait
echo "SELFTEST_DONE $(date -u +%FT%TZ)"
