#!/bin/bash
# Pass 4: the memory curve by speed category, both development months. Two cores.
# Waits for the poker job that is using them.
W=/archive/experiments/paths/chess
cd "$W/src" || exit 1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=/home/claude/env/bin/python3
while ! grep -q RECENCY_DONE /archive/experiments/paths/poker/recency.log 2>/dev/null; do sleep 20; done
run() {  # month core
  for S in bullet blitz rapid classical; do
    taskset -c "$2" nice -n 19 $PY analyze_memory.py "$W/rows/within_$1.tsv.gz" "$W/results/memory_speed_${S}_$1.json" 24 0 "$S" > /dev/null 2>&1
    echo "done $1 $S $(date -u +%T)"
  done
}
run 2026-08 22 &
run 2026-07 23 &
wait
echo "SPEED_DONE $(date -u +%FT%TZ)"
