#!/bin/bash
# Rehearsal of the registered chain from a fresh clone of the public repository, on one
# development month. Usage: run_rehearsal.sh 2026-08
# Mines with the cloned code and the committed targets, runs the registered analysis and the
# grader, and compares both outputs with the files committed in the clone.
# One core, lowest priority, never core 0. Run on Atlas inside a named screen session.
set -u
M="$1"
R=/archive/experiments/paths/chess/rehearsal
SRC=/archive/ahb-sjsu/lichess/lichess_db_standard_rated_${M}.pgn.zst
PY=/home/claude/env/bin/python3
rm -rf "$R/clone" && mkdir -p "$R" && cd "$R" || exit 1
git clone -q --depth 1 https://github.com/ahb-sjsu/geometric-economics.git clone || exit 1
C="$R/clone/experiments/papers/paths/chess"
echo "commit $(git -C clone rev-parse HEAD) start $(date -u +%FT%TZ)"
cd "$C" || exit 1
export PATHS_PLAYER_KEY="$(cat /home/claude/.paths_player_key)"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
zstd -dc "$SRC" | taskset -c 22 nice -n 19 $PY mine_targets.py --targets results/targets.tsv \
  --out "$R/within_${M}.tsv.gz" --max-games 0 || { echo "REHEARSAL_FAILED mine"; exit 1; }
echo "mined $(date -u +%FT%TZ)"
taskset -c 22 nice -n 19 $PY analyze_memory.py "$R/within_${M}.tsv.gz" "$R/memory_reg_${M}.json" 24 > "$R/analyze.out" 2>&1 \
  || { echo "REHEARSAL_FAILED analyze"; exit 1; }
$PY grade_memory.py "$R/memory_reg_${M}.json" "$R/graded_${M}.json" > "$R/grade.out" 2>&1 \
  || { echo "REHEARSAL_FAILED grade"; exit 1; }
cmp "$R/memory_reg_${M}.json" "results/memory_reg_${M}.json" && echo "ANALYSIS_IDENTICAL" || echo "ANALYSIS_DIFFERS"
cmp "$R/graded_${M}.json" "results/graded_dev_${M}.json" && echo "GRADE_IDENTICAL" || echo "GRADE_DIFFERS"
echo "REHEARSAL_DONE $(date -u +%FT%TZ)"
