#!/usr/bin/env python3
"""Power and size for prereg-d4stability-v2, and the seal hash.

**This script cannot read the choices.** It loads `rows_covariates_v2.npz`, which
holds no outcome column. The choices live in `rows_outcome_v2.npz` and are opened
only by the confirmatory fit after the seal. The separation is structural rather
than a matter of care.

What is being sized. The statistic is Cochran's Q over the interior chirality
`c2` fitted separately in four folds of the corpus split by outcome scale,
compared against random partitions of the problems into folds of exactly the same
sizes.

**The first version of this test used the plain standard deviation of the four
fold estimates, and this script is what caught it.** Its size at a true fold
spread of zero came out at **0.110 against a nominal 0.05**. The scale folds
differ in composition and so in how precisely `c2` can be estimated in them,
while a random fold always has average composition and average precision, so the
real split spread further than the null even under a constant `c2`. Studentising
each fold's deviation by its own standard error removes that asymmetry. The
registration was rewritten before it was sealed and the old log is kept beside
this one as `power_UNWEIGHTED_VOID.log`.

**The generative model is written in within-fold standardised columns**, which is
the same convention the fit uses and the same one under which CPC18 and
choices13k were each standardised on their own columns before their chiralities
were compared. Under a constant standardised `c2` the size of the test should be
nominal. That is measured here and not assumed.

Generative coefficients are READ AT RUN TIME from `results_v3.json`. The v1
lineage transcribed six coefficients and got five of them wrong.

    python power_d4stability_v2.py            # power and size
    python power_d4stability_v2.py --hash     # seal the bundle
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ANALYSIS = os.path.abspath(os.path.join(HERE, "..", "analysis"))
V3 = os.path.abspath(os.path.join(HERE, "..", "..", "d4interior", "analysis"))
sys.path.insert(0, ANALYSIS)
sys.path.insert(0, V3)

from kappa_mle import TERM_NAMES  # noqa: E402
from stability_rows_v2 import load_covariates  # noqa: E402
from stability_stat import (C2_INDEX, fold_estimates, heterogeneity,  # noqa: E402
                            null_stats, p_value, random_fold_map, spread)

SEED = 20260913
N_FOLDS = 4
R_REPLICATES = 200
B_INNER = 250
# Atlas is a Z840 whose coolers cannot sustain full load. A first run of this
# script at 20 joblib workers with BLAS left unpinned took CPU package 0 to
# 100 C, its critical alarm, and was shed. Ten workers with one BLAS thread each
# was still adding heat to a package already sitting in the eighties under a
# pre-existing container load, so the setting is six.
N_JOBS = 6
# 0.24 is the fold spread that reproduces the CPC18 to choices13k gap, so
# 0.20 and 0.30 bracket the effect size that matters. 0.40 is dropped from
# the v1 grid because W1 was already 1.000 at 0.30 and the run costs an hour.
TRUE_SPREADS = (0.0, 0.10, 0.20, 0.30)
# the gap this test exists to explain: CPC18 minus choices13k
CPC18 = 0.4437750481416212
C13K = -0.12158348968635554
GAP = CPC18 - C13K

BUNDLE = [
    ("analysis", "peterson_parse.py"),
    ("analysis", "stability_rows_v2.py"),
    ("analysis", "stability_stat.py"),
    ("analysis", "pipeline_invariants.py"),
    ("analysis", "d4stab_fit_v2.py"),
    ("analysis", "launch_fit_v2.sh"),
    ("analysis", "d4stab_grade_v2.py"),
    ("power", "power_d4stability_v2.py"),
    (".", "prereg-d4stability-v2.md"),
]


def _z(x):
    s = x.std()
    return (x - x.mean()) / (s if s > 1e-12 else 1.0)


def generative(dEV, dSD, d, q, fold, coef, bEV, deltas):
    """Choice probabilities under a world whose chirality is `coef['d*q'] +
    deltas[f]` in fold `f`, written in within-fold standardised columns."""
    lin = np.empty(len(d))
    base = np.array([coef[t] for t in TERM_NAMES])
    for f in range(N_FOLDS):
        m = fold == f
        c = base.copy()
        c[TERM_NAMES.index("d*q")] += deltas[f]
        T = np.vstack([np.ones(m.sum()), d[m] ** 2 + q[m] ** 2, d[m] * q[m],
                       d[m], q[m], d[m] ** 2 - q[m] ** 2])
        lin[m] = bEV * _z(dEV[m]) + (c @ T) * _z(dSD[m])
    return 1.0 / (1.0 + np.exp(-lin))


def delta_pattern(sd):
    """Four fold offsets, monotone in scale, with sample sd exactly `sd`."""
    base = np.array([-1.5, -0.5, 0.5, 1.5])
    return base * (sd / np.std(base, ddof=1)) if sd > 0 else np.zeros(4)


def main():
    dEV, dSD, d, q, pid, fold_of_problem, scale, part = load_covariates()
    fold = fold_of_problem[pid]
    n_problems = len(fold_of_problem)
    sizes = [int((fold_of_problem == f).sum()) for f in range(N_FOLDS)]

    with open(os.path.join(V3, "results_v3.json"), encoding="utf-8") as fh:
        v3 = json.load(fh)
    coef, bEV = v3["coefficients"], v3["bEV"]
    print("generative coefficients read from results_v3.json, not transcribed:")
    for t in TERM_NAMES:
        print("    %-8s %+.6f" % (t, coef[t]))
    print("    %-8s %+.6f" % ("bEV", bEV))
    print()
    print("trials %d, problems %d, fold sizes in problems %s"
          % (len(d), n_problems, sizes))
    print("fold sizes in trials %s"
          % [int((fold == f).sum()) for f in range(N_FOLDS)])
    print()

    from joblib import Parallel, delayed

    def replicate(sd_true, pr, r):
        """One simulated corpus and its own permutation null. Parallelised at
        this level rather than inside the null, because each fold fit takes
        about 20 ms and dispatch overhead dominates any finer split."""
        rng = np.random.default_rng([SEED, int(sd_true * 1000), r])
        y = (rng.random(len(pr)) < pr).astype(float)
        rows = (dEV, dSD, d, q, y, pid)
        c2s, ses, infos = fold_estimates(rows, fold_of_problem, N_FOLDS)
        if not all(i["converged"] for i in infos):
            return None
        q_obs = heterogeneity(c2s, ses)
        nq, nsp, ok = null_stats(rows, sizes, n_problems, B_INNER,
                                 seed=int(rng.integers(1 << 30)), n_jobs=1)
        return (q_obs, spread(c2s), float(c2s.max() - c2s.min()),
                p_value(q_obs, nq[ok]), float(np.mean(c2s)),
                bool(np.all(c2s > 0) or np.all(c2s < 0)))

    results = {}
    for sd_true in TRUE_SPREADS:
        deltas = delta_pattern(sd_true)
        pr = generative(dEV, dSD, d, q, fold, coef, bEV, deltas)
        got = Parallel(n_jobs=N_JOBS)(delayed(replicate)(sd_true, pr, r)
                                  for r in range(R_REPLICATES))
        nonconv = sum(1 for g in got if g is None)
        got = [g for g in got if g is not None]
        n = len(got)
        qq = np.array([g[0] for g in got])
        sp = np.array([g[1] for g in got])
        rg = np.array([g[2] for g in got])
        pv = np.array([g[3] for g in got])
        mn = np.array([g[4] for g in got])
        same_sign = np.array([g[5] for g in got])
        results["%.2f" % sd_true] = {
            "true_fold_sd": sd_true,
            "true_fold_offsets": [float(x) for x in deltas],
            "replicates_used": n,
            "nonconvergent": nonconv,
            "mean_Q": float(qq.mean()),
            "mean_observed_spread": float(sp.mean()),
            "mean_observed_range": float(rg.mean()),
            "mean_fold_c2": float(mn.mean()),
            "W1": float((pv < 0.05).mean()),
            "W2": float((rg >= GAP).mean()),
            "W3": float((~same_sign).mean()),
        }
        print("  true fold sd %.2f : W1 %.3f  W2 %.3f  W3 %.3f   "
              "mean Q %7.2f  mean spread %.4f  mean range %.4f  "
              "mean fold c2 %+.4f  nonconv %d"
              % (sd_true, (pv < 0.05).mean(), (rg >= GAP).mean(),
                 (~same_sign).mean(), qq.mean(), sp.mean(), rg.mean(),
                 mn.mean(), nonconv))

    print()
    print("  the gap this test exists to explain, CPC18 minus choices13k: %.10f"
          % GAP)
    print("  W1 at a true fold sd of zero is the SIZE of the test.")

    with open(os.path.join(HERE, "power_d4stability_v2.json"), "w",
              encoding="utf-8") as fh:
        json.dump({"seed": SEED, "replicates": R_REPLICATES,
                   "inner_permutations": B_INNER, "n_folds": N_FOLDS,
                   "gap_cpc18_minus_c13k": GAP,
                   "generative_source": "results_v3.json",
                   "by_true_spread": results}, fh, indent=2)
    print()
    print("written power_d4stability_v2.json")


def do_hash():
    """Write the seal. Hashes are taken with CRLF normalised to LF, so a
    checkout on either platform verifies.

    **The grader is inside the bundle.** v3 kept its grader out, because the
    grader carried the combined hash and could not contain a digest of itself.
    That left the bars resting on the signed tag alone. Here the grader reads the
    hash from this file at run time instead of storing it, so the bars are hashed
    with everything else.
    """
    root = os.path.abspath(os.path.join(HERE, ".."))
    comp, h_all = {}, hashlib.sha256()
    for sub, name in BUNDLE:
        rel = name if sub == "." else "%s/%s" % (sub, name)
        with open(os.path.join(root, rel), "rb") as fh:
            b = fh.read().replace(b"\r\n", b"\n")
        dig = hashlib.sha256(b).hexdigest()
        h_all.update(dig.encode())
        comp[rel] = dig
        print("%s  %s" % (dig, rel))
    combined = h_all.hexdigest()

    with open(os.path.join(root, "power", "power_d4stability_v2.json"),
              encoding="utf-8") as fh:
        pw = json.load(fh)
    at_zero = pw["by_true_spread"]["0.00"]

    seal = {
        "prereg": "prereg-d4stability-v2",
        "title": "Is the Interior Chirality Stable Inside One Corpus? (v2, orientation fixed)",
        "level": 1,
        "author": "Andrew H. Bond, San Jose State University",
        "supersedes": "prereg-d4stability-v1 (VOID: design oriented A-B against an outcome oriented chose-the-riskier, reversing 74.8% of rows)",
        "follows": "prereg-d4interior-v3 (V1 FAIL, V2 FAIL, F2 fired)",
        "frozen_at": "2026-09-13",
        "bars": {
            "F5_bEV_must_be_positive": True,
            "F6_pipeline_invariants_must_pass": True,
            "W1_permutation_alpha": 0.05,
            "W2_range_at_least": GAP,
            "W3": "fold estimates not all of one sign",
            "grad_tol": 1e-5,
            "held_in": "analysis/d4stab_grade_v1.py",
        },
        "statistic": ("sample sd of c2 across four folds split by log10 outcome "
                      "scale, against random partitions of the problems into "
                      "folds of the same sizes; each fold standardised on its "
                      "own dEV and dSD columns"),
        "estimator": ("convex Newton on the logistic log-loss, "
                      "d4interior/analysis/kappa_mle.py"),
        "size_at_true_spread_zero": at_zero["W1"],
        "data": ("Psych-101 peterson2021using/exp1.csv, first-press description "
                 "trials of strictly two-outcome problems, 95748 trials over "
                 "5674 problems from 13735 participants"),
        "press_accounting_balances": True,
        "bundle_files": [name if sub == "." else "%s/%s" % (sub, name)
                         for sub, name in BUNDLE],
        "component_sha256": comp,
        "hash_note": ("sha256 per file with CRLF normalised to LF; combined = "
                      "sha256 over concatenated digests in bundle order. "
                      "Document finalised before hashing. The grader IS in the "
                      "bundle and reads this hash at run time rather than "
                      "storing it."),
        "combined_sha256": combined,
        "osf_registration": "OWNER STEP, not yet registered",
    }
    with open(os.path.join(root, "prereg-d4stability-v2.sha256"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(seal, fh, indent=2)
        fh.write("\n")
    print()
    print("combined %s" % combined)
    print("size at a true spread of zero: %.3f" % at_zero["W1"])
    print("written prereg-d4stability-v2.sha256")


if __name__ == "__main__":
    if "--hash" in sys.argv:
        do_hash()
    else:
        main()
