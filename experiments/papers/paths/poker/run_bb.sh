#!/bin/bash
# The contrasts by big blind level, listed in Section 6 of prereg-poker-recency-v1.md and
# written after the sealed result. Reads the hands the sealed run mined.
# Two cores, lowest priority, never core 0. Run on Atlas inside a named screen session.
set -u
R=/archive/experiments/paths/poker/sealed
O=/archive/experiments/paths/poker/bb
C=/archive/experiments/paths/poker/bb_code
PY=/home/claude/env/bin/python3
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
mkdir -p "$O" && cd "$C" || exit 1
one() {  # site core
  for band in "0 1 low" "1 5 mid" "5 1000 high"; do
    set -- "$1" "$2" $band
    taskset -c "$2" nice -n 19 $PY analyze_recency_bb.py "$R/$1_hands.tsv.gz" "$O/bb_$5_$1.json" "$1" "$3" "$4" \
      > "$O/bb_$5_$1.out" 2>&1 && echo "ok $1 $5 $(date -u +%T)" || echo "BB_FAILED $1 $5"
  done
}
one PS 20 &
one PTY 21 &
wait
echo "BB_DONE $(date -u +%FT%TZ)"
