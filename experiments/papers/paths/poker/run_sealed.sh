#!/bin/bash
# The sealed run of prereg-poker-recency-v1, from a fresh clone at the signed tag.
# 1. Verify the bundle hashes and the archive md5 (void condition V1).
# 2. Rehearsal: rerun the development chain and compare with the committed result.
#    Stop if it differs. No held-out action is read before this point.
# 3. Mine, analyse and grade each held-out site.
# Two cores, lowest priority, never core 0. Run on Atlas inside a named screen session.
set -u
W=/archive/experiments/paths/poker
R=$W/sealed
Z=$W/poker-hand-histories-v2.zip
PY=/home/claude/env/bin/python3
TAG=prereg-poker-recency-v1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
rm -rf "$R/clone" && mkdir -p "$R" && cd "$R" || exit 1
git clone -q --depth 1 --branch "$TAG" https://github.com/ahb-sjsu/geometric-economics.git clone 2>/dev/null \
  || { echo "SEALED_FAILED clone"; exit 1; }
C="$R/clone/experiments/papers/paths/poker"
echo "tag $TAG commit $(git -C clone rev-parse HEAD) start $(date -u +%FT%TZ)"
cd "$C" || exit 1
$PY seal_poker.py || { echo "SEALED_FAILED seal"; exit 1; }
[ "$(md5sum "$Z" | cut -d' ' -f1)" = "0918a30f97bda0129897b7e0f1ec895a" ] || { echo "SEALED_VOID V1 archive md5"; exit 1; }
taskset -c 20 nice -n 19 $PY mine_hands.py "$Z" "$R/dev_hands.tsv.gz" --sites ABS FTP ONG > "$R/mine_dev.out" 2>&1 \
  || { echo "SEALED_FAILED mine dev"; exit 1; }
taskset -c 20 nice -n 19 $PY analyze_recency.py "$R/dev_hands.tsv.gz" "$R/recency_dev_coarse.json" 10 0 all > /dev/null 2>&1 \
  || { echo "SEALED_FAILED analyze dev"; exit 1; }
if cmp "$R/recency_dev_coarse.json" results/recency_dev_coarse.json; then
  echo "REHEARSAL_IDENTICAL $(date -u +%FT%TZ)"
else
  echo "REHEARSAL_DIFFERS, held-out sites not touched"; exit 1
fi
one() {
  taskset -c "$2" nice -n 19 $PY mine_hands.py "$Z" "$R/$1_hands.tsv.gz" --sites "$1" --allow-heldout > "$R/mine_$1.out" 2>&1 \
    && taskset -c "$2" nice -n 19 $PY analyze_recency.py "$R/$1_hands.tsv.gz" "$R/recency_$1.json" 10 0 "$1" > /dev/null 2>&1 \
    && $PY grade_recency.py "$R/recency_$1.json" "$R/graded_$1.json" > "$R/grade_$1.out" 2>&1 \
    && echo "GRADED $1 $(date -u +%FT%TZ)" || echo "SEALED_FAILED $1"
}
one PS 20 &
one PTY 21 &
wait
echo "SEALED_DONE $(date -u +%FT%TZ)"
