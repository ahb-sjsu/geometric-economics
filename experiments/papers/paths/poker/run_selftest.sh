#!/bin/bash
# Self-test of the grader on development data, with the registered specification
# (threshold 10 big blinds, coarse stack bins): pooled, then each development site alone.
# Two cores, lowest priority, never core 0. Run on Atlas inside a named screen session.
W=/archive/experiments/paths/poker
cd "$W" || exit 1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=/home/claude/env/bin/python3
R=rows/dev_hands.tsv.gz
$PY grade_recency.py results/recency_dev_coarse.json results/graded_dev_pooled.json || { echo "SELFTEST_FAILED pooled"; exit 1; }
one() {
  taskset -c "$2" nice -n 19 $PY analyze_recency.py $R "results/recency_dev_coarse_$1.json" 10 0 "$1" > /dev/null 2>&1 \
    && $PY grade_recency.py "results/recency_dev_coarse_$1.json" "results/graded_dev_$1.json"
}
( one ABS 20; one ONG 20 ) &
( one FTP 21 ) &
wait
ls results/graded_dev_*.json
echo "SELFTEST_DONE $(date -u +%FT%TZ)"
