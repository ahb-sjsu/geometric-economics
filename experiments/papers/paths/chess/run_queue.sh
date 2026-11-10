#!/bin/bash
# Runs the August within-player pass after the July one has finished. One core at a time.
W=/archive/experiments/paths/chess
while ! grep -q WITHIN_EXIT "$W/within_2026-07.log" 2>/dev/null; do sleep 30; done
"$W/src/run_within.sh" 2026-08
