#!/usr/bin/env python3
"""EXPLORATORY. Problem-clustered uncertainty on the interior chirality.

**Not part of any registration and it changes no verdict.**

`cross_corpus_regimes.py` reports the chirality inside mixed gambles at
`+0.9679 +/- 0.0946` on CPC18 and `-0.0293 +/- 0.0306` on peterson, which looks
like a ten standard error difference between corpora. **Those standard errors
come from a trial-level likelihood that treats every trial as independent, and
they are not credible for CPC18.**

CPC18's 26,467 first-trial rows come from **270 distinct games**, about ninety
eight subjects per game. Subjects seeing the same gamble do not contribute
independent information about how kappa depends on that gamble's coordinate: the
coordinate is a property of the problem, not of the trial. The effective sample
for a coefficient on `(d, q)` is the number of PROBLEMS, and a trial-level
standard error can understate it by the square root of the cluster size, which
here is about ten.

The same argument applies to peterson with much less force, 5,672 problems at
about seventeen trials each, and `prereg-d4stability-v2` already measured that
inflation at 1.82 from its own permutation null.

This resamples **problems** with replacement, refits, and reports the spread of
the estimate. That is the uncertainty that respects the design.

    python cluster_bootstrap.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
V3 = os.path.abspath(os.path.join(HERE, "..", "..", "d4interior", "analysis"))
sys.path.insert(0, DATASETS)
sys.path.insert(0, V3)
sys.path.insert(0, HERE)

from cross_corpus_regimes import _z, feats, fit_design, rows_from, terms  # noqa: E402
from d4_rotation import _opt_coords  # noqa: E402
from kappa_mle import TERM_NAMES  # noqa: E402

B = 400
SEED = 20260913
IDQ = 1 + TERM_NAMES.index("d*q")


def chirality(dEV, dSD, d, q, y):
    t, _se, info = fit_design(np.vstack([_z(dEV), terms(d, q) * _z(dSD)]).T, y)
    return (float(t[IDQ]), bool(info["converged"]))


def cluster_boot(dEV, dSD, d, q, y, pid, b=B, seed=SEED):
    rng = np.random.default_rng(seed)
    uids = np.unique(pid)
    idx = {u: np.where(pid == u)[0] for u in uids}
    est = []
    for _ in range(b):
        pick = rng.choice(uids, size=len(uids), replace=True)
        rows = np.concatenate([idx[u] for u in pick])
        try:
            c, ok = chirality(dEV[rows], dSD[rows], d[rows], q[rows], y[rows])
            if ok and np.isfinite(c):
                est.append(c)
        except np.linalg.LinAlgError:
            continue
    return np.array(est)


def report(tag, dEV, dSD, d, q, y, pid, rH, rL, store):
    has_loss = np.minimum(rH, rL) < 0
    has_gain = np.maximum(rH, rL) > 0
    m = has_loss & has_gain            # mixed gambles only
    n_prob = len(np.unique(pid[m]))
    point, _ok = chirality(dEV[m], dSD[m], d[m], q[m], y[m])
    est = cluster_boot(dEV[m], dSD[m], d[m], q[m], y[m], pid[m])
    lo, hi = np.percentile(est, [2.5, 97.5])
    print()
    print("%s" % tag)
    print("   mixed trials %6d over %5d distinct problems (%.0f trials each)"
          % (m.sum(), n_prob, m.sum() / max(n_prob, 1)))
    print("   d*q inside mixed            %+.4f" % point)
    print("   problem-clustered bootstrap  sd %.4f   95%% CI [%+.4f, %+.4f]"
          % (est.std(ddof=1), lo, hi))
    print("   contains zero: %s" % ("YES" if lo <= 0 <= hi else "NO"))
    store[tag] = {"n_mixed_trials": int(m.sum()), "n_mixed_problems": int(n_prob),
                  "dq_mixed": point, "boot_sd": float(est.std(ddof=1)),
                  "ci_lo": float(lo), "ci_hi": float(hi),
                  "contains_zero": bool(lo <= 0 <= hi),
                  "n_bootstrap_ok": int(len(est))}


def main():
    store = {}
    print("=" * 78)
    print("PROBLEM-CLUSTERED UNCERTAINTY ON THE INTERIOR CHIRALITY")
    print("=" * 78)
    print("resampling PROBLEMS with replacement, %d draws, refitting each time" % B)

    c = pd.read_csv(os.path.join(DATASETS, "raw", "cpc18_raw.csv"))
    c = c.dropna(subset=["Ha", "pHa", "La", "Hb", "pHb", "Lb", "B"])
    t1 = c[c["Trial"] == 1]
    for tag, df in (("CPC18 trial 1, all lotteries", t1),
                    ("CPC18 trial 1, two-outcome only",
                     t1[(t1["LotNumA"] == 1) & (t1["LotNumB"] == 1)])):
        recs, gid = [], []
        for r in df.itertuples():
            recs.append((r.Ha, r.pHa, r.La, r.Hb, r.pHb, r.Lb, 1.0 - float(r.B)))
            gid.append(r.GameID)
        dEV, dSD, d, q, y, rH, rL = rows_from(recs)
        # rows_from may drop rows; rebuild the id vector the same way
        keep, g2 = [], []
        for i, rec in enumerate(recs):
            Ha, pHa, La, Hb, pHb, Lb, _y = rec
            _e, sA = feats(Ha, pHa, La)
            _e2, sB = feats(Hb, pHb, Lb)
            if abs(sA - sB) < 1e-12:
                continue
            H, p, L = (Ha, pHa, La) if sA >= sB else (Hb, pHb, Lb)
            if max(abs(H), abs(L)) <= 1e-12:
                continue
            g2.append(gid[i])
        pid = np.array(g2)
        assert len(pid) == len(y), "id vector misaligned: %d vs %d" % (len(pid), len(y))
        report(tag, dEV, dSD, d, q, y, pid, rH, rL, store)

    from stability_rows_v2 import load_covariates, load_outcome
    dEV, dSD, d, q, pid, fold, scale, part = load_covariates()
    z = np.load(os.path.join(HERE, "seam_covariates.npz"))
    report("peterson description, individual", dEV, dSD, d, q, load_outcome(),
           pid, z["risky_H"], z["risky_L"], store)

    print()
    print("=" * 78)
    ks = list(store)
    for k in ks:
        v = store[k]
        print("  %-34s %+.4f  CI [%+.4f, %+.4f]  %s"
              % (k, v["dq_mixed"], v["ci_lo"], v["ci_hi"],
                 "includes 0" if v["contains_zero"] else "excludes 0"))
    print("=" * 78)
    with open(os.path.join(HERE, "cluster_bootstrap.json"), "w",
              encoding="utf-8") as fh:
        json.dump(store, fh, indent=2)
    print("written cluster_bootstrap.json")


if __name__ == "__main__":
    main()
