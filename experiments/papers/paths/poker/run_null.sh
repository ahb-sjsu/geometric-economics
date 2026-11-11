#!/bin/bash
# Players with no memory through the registered poker analysis. Written after the sealed result.
# Profiles are measured on the PokerStars hands the sealed run mined, once, and reused.
# Usage: run_null.sh OUT_NAME [fixed-seat]. The first run (OUT_NAME null, fixed seat) is kept
# on Atlas. The run with rotating seats is null2. Two simulated sets each.
# Two cores, lowest priority, never core 0. Run on Atlas inside a named screen session.
set -u
R=/archive/experiments/paths/poker/sealed
O=/archive/experiments/paths/poker/${1:-null2}
P=/archive/experiments/paths/poker/null/profile_PS.json
MODE=${2:-}
C=/archive/experiments/paths/poker/bb_code
PY=/home/claude/env/bin/python3
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
mkdir -p "$O" "$(dirname "$P")" && cd "$C" || exit 1
[ -s "$P" ] || taskset -c 20 nice -n 19 $PY null_sim.py measure "$R/PS_hands.tsv.gz" "$P" || { echo "NULL_FAILED measure"; exit 1; }
one() {  # seed core
  taskset -c "$2" nice -n 19 $PY null_sim.py simulate "$P" "$O/sim_$1.tsv.gz" "$1" $MODE > "$O/sim_$1.out" 2>&1 \
    && taskset -c "$2" nice -n 19 $PY analyze_recency.py "$O/sim_$1.tsv.gz" "$O/null_recency_$1.json" 10 0 SIM > /dev/null 2>&1 \
    && taskset -c "$2" nice -n 19 $PY null_raw.py "$O/sim_$1.tsv.gz" "$O/raw_$1.json" SIM > "$O/raw_$1.out" 2>&1 \
    && echo "ok seed $1 $(date -u +%T)" || echo "NULL_FAILED seed $1"
}
one 1 20 &
one 2 21 &
wait
echo "NULL_DONE $(date -u +%FT%TZ)"
