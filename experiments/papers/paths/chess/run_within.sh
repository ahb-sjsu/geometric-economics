#!/bin/bash
# Within-player development pass for one month. Usage: run_within.sh 2026-07 [max_games]
# Targets always come from the July sample. One core, lowest priority, never core 0.
set -u
M="$1"
MAXG="${2:-0}"
W=/archive/experiments/paths/chess
SRC=/archive/ahb-sjsu/lichess/lichess_db_standard_rated_${M}.pgn.zst
PY=/home/claude/env/bin/python3
cd "$W/src" || exit 1
export PATHS_PLAYER_KEY="$(cat /home/claude/.paths_player_key)"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
TAG="$M"; [ "$MAXG" != "0" ] && TAG="test_$M"
echo "start $(date -u +%FT%TZ) month=$M max_games=$MAXG"
if [ ! -s "$W/results/targets.tsv" ]; then
  taskset -c 22 nice -n 19 $PY make_targets.py "$W/results/dev_2026-07.json" "$W/rows/paths_2026-07.tsv.gz" "$W/results/targets.tsv"
fi
wc -l "$W/results/targets.tsv"
zstd -dc "$SRC" | taskset -c 22 nice -n 19 $PY mine_targets.py --targets "$W/results/targets.tsv" \
  --out "$W/rows/within_${TAG}.tsv.gz.tmp" --max-games "$MAXG" && mv "$W/rows/within_${TAG}.tsv.gz.tmp" "$W/rows/within_${TAG}.tsv.gz"
echo "mined $(date -u +%FT%TZ)"
taskset -c 22 nice -n 19 $PY analyze_within.py "$W/rows/within_${TAG}.tsv.gz" "$W/results/within_${TAG}.json"
echo "WITHIN_EXIT=$? $(date -u +%FT%TZ)"
