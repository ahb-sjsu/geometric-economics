#!/bin/bash
# Confirmatory run for prereg-d4stability-v1, on Atlas, after the seal.
#
# The thread pins are not optional. joblib gives each worker a process, and an
# unpinned BLAS then gives each worker as many threads as there are cores. A
# first run of the power simulation that way took CPU package 0 to 100 C, its
# critical alarm, and had to be shed. One BLAS thread per worker and six workers
# holds the package near eighty against a baseline of seventy-four.
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
cd "$(dirname "$0")"
exec python3 -u d4stab_fit_v1.py "${1:-2000}"
