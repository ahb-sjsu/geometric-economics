#!/bin/bash
# The sealed run of prereg-chess-memory-v1, from a fresh clone at the signed tag.
# 1. Verify the bundle hashes and the October file's sha256 (void condition V1).
# 2. Rehearsal of the H5 chain: mine August with the cloned mine_movetime.py, run
#    analyze_pull_time.py, compare with the committed result. Stop if it differs.
#    October is not decompressed before this point. (The H1 to H4 chain was
#    rehearsed on commit 0bedf33 and its files are unchanged, which step 1 checks
#    against the sealed hashes.)
# 3. October: both mining passes, the registered analyses, both graders, and the
#    two curves reported without a bar that need no further mining.
# Two cores, lowest priority, never core 0. Run on Atlas inside a named screen session.
set -u
W=/archive/experiments/paths/chess
R=$W/sealed
L=/archive/ahb-sjsu/lichess
PY=/home/claude/env/bin/python3
TAG=prereg-chess-memory-v1
OCT=$L/lichess_db_standard_rated_2026-10.pgn.zst
AUG=$L/lichess_db_standard_rated_2026-08.pgn.zst
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export PATHS_PLAYER_KEY="$(cat /home/claude/.paths_player_key)"
rm -rf "$R/clone" && mkdir -p "$R" && cd "$R" || exit 1
git clone -q --depth 1 --branch "$TAG" https://github.com/ahb-sjsu/geometric-economics.git clone 2>/dev/null \
  || { echo "SEALED_FAILED clone"; exit 1; }
C="$R/clone/experiments/papers/paths/chess"
echo "tag $TAG commit $(git -C clone rev-parse HEAD) start $(date -u +%FT%TZ)"
cd "$C" || exit 1
$PY seal_chess.py || { echo "SEALED_FAILED seal"; exit 1; }
[ "$(taskset -c 18 nice -n 19 sha256sum "$OCT" | cut -d' ' -f1)" = "043906ebfade1bfeb7c00087590fac505370936c028525e4722e2dbd4986ae86" ] \
  || { echo "SEALED_VOID V1 October sha256"; exit 1; }
echo "october sha256 ok $(date -u +%FT%TZ)"

zstd -dc "$AUG" | taskset -c 18 nice -n 19 $PY mine_movetime.py --targets results/targets.tsv \
  --out "$R/movetime_2026-08.tsv.gz" --max-games 0 > "$R/mine_aug.out" 2>&1 || { echo "SEALED_FAILED mine august"; exit 1; }
taskset -c 18 nice -n 19 $PY analyze_pull_time.py "$R/movetime_2026-08.tsv.gz" "$R/pull_time_2026-08.json" > /dev/null 2>&1 \
  || { echo "SEALED_FAILED analyze august"; exit 1; }
if cmp "$R/pull_time_2026-08.json" results/pull_time_2026-08.json; then
  echo "REHEARSAL_IDENTICAL $(date -u +%FT%TZ)"
else
  echo "REHEARSAL_DIFFERS, October not opened"; exit 1
fi
rm -f "$R/movetime_2026-08.tsv.gz"

( zstd -dc "$OCT" | taskset -c 18 nice -n 19 $PY mine_targets.py --targets results/targets.tsv \
    --out "$R/within_2026-10.tsv.gz" --max-games 0 > "$R/mine_oct.out" 2>&1 \
  && taskset -c 18 nice -n 19 $PY analyze_memory.py "$R/within_2026-10.tsv.gz" "$R/memory_reg_2026-10.json" 24 > /dev/null 2>&1 \
  && $PY grade_memory.py "$R/memory_reg_2026-10.json" "$R/graded_2026-10.json" > "$R/grade_memory.out" 2>&1 \
  && echo "GRADED H1-H4 $(date -u +%FT%TZ)" \
  && taskset -c 18 nice -n 19 $PY analyze_memory.py "$R/within_2026-10.tsv.gz" "$R/memory_reg_opp50_2026-10.json" 24 50 > /dev/null 2>&1 \
  || echo "SEALED_FAILED H1-H4 chain" ) &
( zstd -dc "$OCT" | taskset -c 19 nice -n 19 $PY mine_movetime.py --targets results/targets.tsv \
    --out "$R/movetime_2026-10.tsv.gz" --max-games 0 > "$R/mine_oct_movetime.out" 2>&1 \
  && taskset -c 19 nice -n 19 $PY analyze_pull_time.py "$R/movetime_2026-10.tsv.gz" "$R/pull_time_2026-10.json" > /dev/null 2>&1 \
  && $PY grade_pull.py "$R/pull_time_2026-10.json" "$R/graded_pull_2026-10.json" > "$R/grade_pull.out" 2>&1 \
  && echo "GRADED H5 $(date -u +%FT%TZ)" \
  && taskset -c 19 nice -n 19 $PY analyze_memory_time.py "$R/movetime_2026-10.tsv.gz" "$R/memory_time_2026-10" "$R" > /dev/null 2>&1 \
  || echo "SEALED_FAILED H5 chain" ) &
wait
echo "SEALED_DONE $(date -u +%FT%TZ)"
