export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8
cd /archive/experiments/strata/repo/experiments/papers/strata2
/home/claude/env/bin/python explore_readers.py /archive/experiments/strata/rows --models GDTS-llo-pow2-L1,GDTS-llo-pow2-L1-nos,GDTS-llo-pow2-L1-nobeta,GDTS-llo-pow2-L1-core,CPT_unit,CPT_share --tag _ablate > ablate.log 2>&1
echo DONE >> ablate.log
