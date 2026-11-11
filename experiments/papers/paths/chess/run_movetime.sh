#!/bin/bash
# Pass 8: mine one development month with move times, then the pull by time spent.
# Usage: run_movetime.sh 2026-08
# One core, lowest priority, never core 0. Run on Atlas inside a named screen session.
set -u
M="$1"
W=/archive/experiments/paths/chess
SRC=/archive/ahb-sjsu/lichess/lichess_db_standard_rated_${M}.pgn.zst
PY=/home/claude/env/bin/python3
case "$M" in 2026-07|2026-08) ;; *) echo "MOVETIME_FAILED not a development month"; exit 1;; esac
cd "$W/src" || exit 1
export PATHS_PLAYER_KEY="$(cat /home/claude/.paths_player_key)"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
echo "start $(date -u +%FT%TZ)"
zstd -dc "$SRC" | taskset -c 21 nice -n 19 $PY mine_movetime.py --targets "$W/results/targets.tsv" \
  --out "$W/rows/movetime_${M}.tsv.gz" --max-games "${2:-0}" || { echo "MOVETIME_FAILED mine"; exit 1; }
echo "mined $(date -u +%FT%TZ)"
taskset -c 21 nice -n 19 $PY analyze_pull_time.py "$W/rows/movetime_${M}.tsv.gz" "$W/results/pull_time_${M}.json" \
  > "$W/pull_time_${M}.out" 2>&1 || { echo "MOVETIME_FAILED analyze"; exit 1; }
echo "MOVETIME_DONE $(date -u +%FT%TZ)"
