#!/bin/bash
# One development month of Lichess, one core, lowest priority. Usage: run_mine.sh 2026-06 [max_games]
# Run on Atlas inside a named screen session. Core 20 is used, never core 0.
set -u
M="$1"
MAXG="${2:-0}"
W=/archive/experiments/paths/chess
SRC=/archive/ahb-sjsu/lichess/lichess_db_standard_rated_${M}.pgn.zst
PY=/home/claude/env/bin/python3
mkdir -p "$W/rows" && cd "$W/src" || exit 1
if [ ! -s /home/claude/.paths_player_key ]; then
  (umask 077; head -c 32 /dev/urandom | base64 > /home/claude/.paths_player_key)
fi
export PATHS_PLAYER_KEY="$(cat /home/claude/.paths_player_key)"
OUT="$W/rows/paths_${M}.tsv.gz"
[ "$MAXG" != "0" ] && OUT="$W/rows/test_${M}.tsv.gz"
echo "start $(date -u +%FT%TZ) month=$M max_games=$MAXG"
zstd -dc "$SRC" | taskset -c 20 nice -n 19 $PY mine_paths.py --out "$OUT.tmp" --max-games "$MAXG" \
  && mv "$OUT.tmp" "$OUT"
echo "end $(date -u +%FT%TZ) $(ls -la "$OUT")"
