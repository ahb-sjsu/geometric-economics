#!/bin/bash
# Counts repeated player labels in the HandHQ hands once the archive has arrived.
# Reads header lines only. One core, lowest priority.
W=/archive/experiments/paths/poker
cd "$W" || exit 1
while ! grep -q CURL_EXIT fetch.log 2>/dev/null; do sleep 30; done
tail -3 fetch.log
echo "start $(date -u +%FT%TZ)"
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 taskset -c 23 nice -n 19 /home/claude/env/bin/python3 count_labels.py \
  poker-hand-histories-v2.zip labels.json
echo "COUNT_EXIT=$? $(date -u +%FT%TZ)"
