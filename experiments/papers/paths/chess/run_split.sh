#!/bin/bash
# The curves of Section 6 of prereg-chess-memory-v1.md that the sealed run left out:
# by speed category, by rating band, and on pairs with different opponents.
# Written after the sealed result. Reads the October rows the sealed run mined.
# Two cores, lowest priority, never core 0. Run on Atlas inside a named screen session.
set -u
R=/archive/experiments/paths/chess/sealed
O=/archive/experiments/paths/chess/split
C=/archive/experiments/paths/chess/split_code
PY=/home/claude/env/bin/python3
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
mkdir -p "$O" && cd "$C" || exit 1
one() {  # core, subset
  taskset -c "$1" nice -n 19 $PY analyze_memory_split.py "$R/within_2026-10.tsv.gz" "$O/split_${2//=/_}.json" "$2" \
    > "$O/split_${2//=/_}.out" 2>&1 && echo "ok $2 $(date -u +%T)" || echo "SPLIT_FAILED $2"
}
( for s in diffopp speed=bullet speed=rapid band=0-1400 band=1800-2200; do one 18 "$s"; done ) &
( for s in speed=blitz speed=classical band=1400-1800 band=2200-4000; do one 19 "$s"; done ) &
wait
echo "SPLIT_DONE $(date -u +%FT%TZ)"
