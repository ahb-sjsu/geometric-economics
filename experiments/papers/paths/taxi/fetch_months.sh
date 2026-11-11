#!/bin/bash
# Fetch Chicago "Taxi Trips (2013-2023)" (wrvz-psew) one month at a time, since the
# single full export stalled at 6.5 GB on 2026-11-11 and cannot be resumed.
# For each month: ask the portal for the row count, fetch the rows as CSV, and
# accept the file only if its line count matches. Rerunning skips finished months.
# The rows are not sorted by the server, since sorting a month took over three minutes
# before the first byte. The count check does not need an order. No row is parsed here.
# Usage: fetch_months.sh [first_year [last_year]]. Several instances may run on
# different year ranges. Each writes to its own partial file and renames it on success.
# Run on Atlas inside a named screen session.
set -u
D=/archive/experiments/paths/taxi/raw/months
B=https://data.cityofchicago.org/resource/wrvz-psew
mkdir -p "$D" && cd "$D" || exit 1
for y in $(seq "${1:-2013}" "${2:-2023}"); do
  for m in 01 02 03 04 05 06 07 08 09 10 11 12; do
    f="taxi_${y}-${m}.csv"
    [ -s "$f.ok" ] && continue
    if [ "$m" = 12 ]; then ny=$((y + 1)); nm=01; else ny=$y; nm=$(printf "%02d" $((10#$m + 1))); fi
    w="trip_start_timestamp >= '${y}-${m}-01T00:00:00' AND trip_start_timestamp < '${ny}-${nm}-01T00:00:00'"
    n=""
    for try in 1 2 3 4 5; do
      n=$(curl -sS -G --max-time 600 "$B.csv" --data-urlencode "\$select=count(*)" --data-urlencode "\$where=$w" | tail -1 | tr -d '"\r')
      [[ "$n" =~ ^[0-9]+$ ]] && break
      n=""; sleep 30
    done
    [ -z "$n" ] && { echo "COUNT_FAILED $y-$m"; continue; }
    ok=0
    for try in 1 2 3 4 5; do
      curl -sS -G --speed-limit 2000 --speed-time 600 -o "$f.part.$$" "$B.csv" \
        --data-urlencode "\$where=$w" --data-urlencode "\$limit=20000000"
      got=$(($(wc -l < "$f.part.$$") - 1))
      if [ "$got" = "$n" ]; then mv "$f.part.$$" "$f"; ok=1; break; fi
      echo "retry $y-$m try $try got $got want $n"; sleep 30
    done
    if [ "$ok" = 1 ]; then echo "$n" > "$f.ok"; echo "ok $y-$m $n $(date -u +%T)"; else echo "MONTH_FAILED $y-$m"; fi
  done
done
echo "FETCH_MONTHS_END $(ls *.ok 2>/dev/null | wc -l) of 132 $(date -u +%FT%TZ)"
