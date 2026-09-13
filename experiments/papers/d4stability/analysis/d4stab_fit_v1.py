#!/usr/bin/env python3
"""Confirmatory fit for prereg-d4stability-v1. Run only after the seal.

This is the one script in the bundle that opens `rows_outcome.npz`. It fits the
interior chirality `c2` separately in each of the four scale folds, computes the
registered spread statistic, and compares it against random partitions of the
problems into folds of exactly the same sizes.

It computes no verdict. `d4stab_grade_v1.py` holds every threshold and is the
only place a pass or fail is decided.

    python d4stab_fit_v1.py [n_permutations]
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from stability_rows import N_FOLDS, load_covariates, load_outcome  # noqa: E402
from stability_stat import (fit_fold, fold_estimates, heterogeneity,  # noqa: E402
                            null_stats, p_value, spread)

SEED = 20260913
# Atlas is a Z840 whose coolers cannot sustain full load. Running the power
# simulation at twenty workers with BLAS left unpinned took CPU package 0 to
# 100 C, its critical alarm, and the job was shed. Six workers with one BLAS
# thread each holds the package near eighty against a baseline of
# seventy-four. Run this through `launch_fit.sh`, which pins the thread counts.
N_JOBS = 6


def main():
    b = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    dEV, dSD, d, q, pid, fold_of_problem, scale, part = load_covariates()
    y = load_outcome()
    assert len(y) == len(d), "outcome and covariate files disagree on length"

    rows = (dEV, dSD, d, q, y, pid)
    fold = fold_of_problem[pid]
    sizes = [int((fold_of_problem == f).sum()) for f in range(N_FOLDS)]
    n_problems = len(fold_of_problem)

    # the whole corpus in one fit, as a reference point rather than a prediction
    c2_all, se_all, info_all = fit_fold(dEV, dSD, d, q, y)

    c2s, ses, infos = fold_estimates(rows, fold_of_problem, N_FOLDS)
    q_obs = heterogeneity(c2s, ses)
    s_obs = spread(c2s)
    rng_obs = float(c2s.max() - c2s.min())

    nq, nsp, ok = null_stats(rows, sizes, n_problems, b, seed=SEED,
                             n_jobs=N_JOBS)
    p = p_value(q_obs, nq[ok])

    print("whole corpus c2 = %+.6f +/- %.6f   grad %.3e   rows %d"
          % (c2_all, se_all, info_all["grad_inf_norm"], len(y)))
    print()
    print("  fold  problems  trials      c2        se        grad norm   min eig")
    for f in range(N_FOLDS):
        print("  %4d  %8d %7d  %+9.6f  %.6f  %.3e  %8.3f"
              % (f, sizes[f], int((fold == f).sum()), c2s[f], ses[f],
                 infos[f]["grad_inf_norm"], infos[f]["hessian_min_eig"]))
    print()
    print("  Q (studentised, the statistic)  %.6f" % q_obs)
    print("  spread (sd of the four)         %.6f   reported, not tested" % s_obs)
    print("  range  (max minus min)          %.6f" % rng_obs)
    print("  random-split null on Q: %d usable of %d, mean %.4f, 95th pct %.4f"
          % (int(ok.sum()), b, float(nq[ok].mean()),
             float(np.quantile(nq[ok], 0.95))))
    print("  permutation p                   %.6f" % p)

    out = {
        "prereg": "prereg-d4stability-v1",
        "corpus": "peterson2021using/exp1.csv, first-press description trials",
        "n_trials": int(len(y)),
        "n_problems": int(n_problems),
        "fold_sizes_problems": sizes,
        "fold_sizes_trials": [int((fold == f).sum()) for f in range(N_FOLDS)],
        "c2_whole_corpus": float(c2_all),
        "se_whole_corpus": float(se_all),
        "grad_whole_corpus": float(info_all["grad_inf_norm"]),
        "c2_by_fold": [float(x) for x in c2s],
        "se_by_fold": [float(x) for x in ses],
        "Q": q_obs,
        "grad_by_fold": [float(i["grad_inf_norm"]) for i in infos],
        "min_eig_by_fold": [float(i["hessian_min_eig"]) for i in infos],
        "converged_all_folds": bool(all(i["converged"] for i in infos)
                                    and info_all["converged"]),
        "spread": s_obs,
        "range": rng_obs,
        "n_permutations": int(b),
        "n_permutations_usable": int(ok.sum()),
        "null_Q_mean": float(nq[ok].mean()),
        "null_Q_p95": float(np.quantile(nq[ok], 0.95)),
        "permutation_p": p,
    }
    with open(os.path.join(HERE, "results_stability_v1.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written results_stability_v1.json")


if __name__ == "__main__":
    main()
