#!/bin/bash
# Players with no memory through the registered poker analysis. Written after the sealed result.
# Profiles are measured on the PokerStars hands the sealed run mined. Three simulated sets.
# Two cores, lowest priority, never core 0. Run on Atlas inside a named screen session.
set -u
R=/archive/experiments/paths/poker/sealed
O=/archive/experiments/paths/poker/null
C=/archive/experiments/paths/poker/bb_code
PY=/home/claude/env/bin/python3
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
mkdir -p "$O" && cd "$C" || exit 1
taskset -c 20 nice -n 19 $PY null_sim.py measure "$R/PS_hands.tsv.gz" "$O/profile_PS.json" > "$O/measure.out" 2>&1 \
  || { echo "NULL_FAILED measure"; exit 1; }
cat "$O/measure.out"
one() {  # seed core
  taskset -c "$2" nice -n 19 $PY null_sim.py simulate "$O/profile_PS.json" "$O/sim_$1.tsv.gz" "$1" > "$O/sim_$1.out" 2>&1 \
    && taskset -c "$2" nice -n 19 $PY analyze_recency.py "$O/sim_$1.tsv.gz" "$O/null_recency_$1.json" 10 0 SIM > /dev/null 2>&1 \
    && echo "ok seed $1 $(date -u +%T)" || echo "NULL_FAILED seed $1"
}
one 1 20 &
one 2 21 &
wait
one 3 20
echo "NULL_DONE $(date -u +%FT%TZ)"
