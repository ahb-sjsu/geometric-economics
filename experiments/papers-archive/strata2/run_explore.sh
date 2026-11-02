export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8
cd /archive/experiments/strata/repo/experiments/papers/strata2
/home/claude/env/bin/python explore_readers.py /archive/experiments/strata/rows > explore.log 2>&1
echo DONE >> explore.log
