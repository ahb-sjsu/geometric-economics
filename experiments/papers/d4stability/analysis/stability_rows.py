#!/usr/bin/env python3
"""Row builder for prereg-d4stability-v1. Description trials of peterson2021using.

The coordinate is IMPORTED from `d4_rotation` and never restated, and this module
asserts at import that it is the real one. `prereg-d4gate-v1` was voided because
its analysis code reimplemented that function and got both its form and its sign
convention wrong.

**Covariates and outcomes are written to separate files on purpose.** The power
simulation loads `rows_covariates.npz` and that file contains no choice column,
so the simulation cannot read the outcome even by accident. `rows_outcome.npz`
holds the choices and is opened only by the confirmatory fit, after the
registration is sealed. This is a structural version of the discipline that the
v3 lineage had to enforce by attention.

**Inclusion, declared here and not later.** From the press accounting of
`peterson_parse`, only `first_press_description` is kept: the first choice on a
problem, made before any outcome feedback on that problem. Repeat presses follow
feedback and are decisions from experience. Ambiguity trials state no
probability. Multi-branch lotteries are outside the two-outcome coordinate and
are excluded rather than approximated by their extreme branches.

Note that both CPC18 and choices13k contain multi-branch lotteries too, and the
fits that produced `+0.4438` and `−0.1216` read only the `(H, p, L)` columns for
all of them. This corpus is restricted to strictly two-outcome problems and is
cleaner in that respect, which also means its `c2` is not numerically the same
estimand as theirs. The stability question is internal to this corpus and does
not depend on that comparison.

Two further exclusions, both mechanical:

  * rows whose two options have equal standard deviation, so `dSD` is zero and
    the row carries no information about kappa at all;
  * rows whose riskier option has both outcomes zero, so the scale used by the
    split axis is undefined.

    python stability_rows.py          # parse once, write both files
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
sys.path.insert(0, DATASETS)
sys.path.insert(0, HERE)

from d4_rotation import _opt_coords  # noqa: E402  IMPORTED, never restated
from peterson_parse import (BUCKETS, PRESS, PRESS_FIRST, feats,  # noqa: E402
                            trials)

_d, _q = _opt_coords(10.0, 1.0, 10.0)
assert abs(_d - 1.0) < 1e-9, "imported _opt_coords is not the expected coordinate"

COV = os.path.join(HERE, "rows_covariates.npz")
OUT = os.path.join(HERE, "rows_outcome.npz")
N_FOLDS = 4


def parse_corpus():
    from datasets import load_dataset
    ds = load_dataset("marcelbinz/Psych-101", split="train")
    rows = [r for r in ds if r["experiment"] == "peterson2021using/exp1.csv"]

    counts = {b: 0 for b in BUCKETS}
    total_tokens = 0
    keep, excl_zero_sd, excl_zero_scale = [], 0, 0
    uniq = {}
    n_scale_violations = [0]

    for i, r in enumerate(rows):
        text = r["text"]
        total_tokens += len(PRESS.findall(text))
        for bucket, a, b, chose_a, idx, had_fb in trials(text):
            counts[bucket] += 1
            if bucket != PRESS_FIRST:
                continue
            evA, sdA = feats(*a)
            evB, sdB = feats(*b)
            if abs(sdA - sdB) < 1e-12:
                excl_zero_sd += 1
                continue
            risky_is_a = sdA >= sdB
            H, p, L = a if risky_is_a else b
            scale = max(abs(H), abs(L))
            if scale <= 1e-12:
                excl_zero_scale += 1
                continue
            dc, qc = _opt_coords(H, p, L)
            # The split axis is outcome scale, and it is only a legitimate axis
            # if the coordinate cannot see it. Checked on every kept row rather
            # than argued for, at two scale factors on either side of one.
            for lam in (7.3, 0.137):
                d2, q2 = _opt_coords(H * lam, p, L * lam)
                if abs(d2 - dc) > 1e-9 or abs(q2 - qc) > 1e-9:
                    n_scale_violations[0] += 1
            key = (round(a[0], 4), round(a[1], 4), round(a[2], 4),
                   round(b[0], 4), round(b[1], 4), round(b[2], 4))
            pid = uniq.setdefault(key, len(uniq))
            keep.append((evA - evB, sdA - sdB, dc, qc,
                         float(chose_a == risky_is_a), scale, pid, i))

    assert sum(counts.values()) == total_tokens, "press accounting does not balance"
    assert n_scale_violations[0] == 0, (
        "the coordinate is not invariant under outcome scaling on %d checks, "
        "so outcome scale is not a legitimate split axis"
        % n_scale_violations[0])
    meta = {
        "press_accounting": {b: int(counts[b]) for b in BUCKETS},
        "press_tokens_total": int(total_tokens),
        "excluded_zero_dSD": int(excl_zero_sd),
        "excluded_zero_scale": int(excl_zero_scale),
        "n_trials_kept": len(keep),
        "n_distinct_problems": len(uniq),
        "n_participants": len(rows),
        "scale_invariance_checks": 2 * len(keep),
        "scale_invariance_violations": n_scale_violations[0],
    }
    return keep, meta


def fold_map(scale_by_problem):
    """Quartiles of log10 outcome scale over DISTINCT PROBLEMS, so the folds are
    balanced in problems rather than in trials.

    The split axis is the scale of the riskier option, `max(|H|, |L|)`. It is
    chosen because the coordinate `(d, q)` is exactly invariant under positive
    scaling of both outcomes. `parse_corpus` checks that on every kept row at two
    scale factors and refuses to build the corpus if it ever fails, so the axis
    is verified rather than argued for. Scale therefore carries no direct
    information about the coordinate, and movement of `c2` across these folds is
    movement the model's own coordinate does not represent.
    """
    ids = np.array(sorted(scale_by_problem))
    ls = np.log10(np.array([scale_by_problem[i] for i in ids]))
    cuts = np.quantile(ls, [0.25, 0.5, 0.75])
    fold = np.digitize(ls, cuts)
    out = np.empty(len(ids), dtype=int)
    out[ids] = fold
    return out, [float(c) for c in cuts]


def main():
    keep, meta = parse_corpus()
    dEV = np.array([k[0] for k in keep])
    dSD = np.array([k[1] for k in keep])
    d = np.array([k[2] for k in keep])
    q = np.array([k[3] for k in keep])
    y = np.array([k[4] for k in keep])
    scale = np.array([k[5] for k in keep])
    pid = np.array([k[6] for k in keep], dtype=int)
    part = np.array([k[7] for k in keep], dtype=int)

    sbp = {}
    for j in range(len(keep)):
        sbp.setdefault(int(pid[j]), float(scale[j]))
    fold, cuts = fold_map(sbp)
    sizes = [int((fold == f).sum()) for f in range(N_FOLDS)]

    np.savez_compressed(COV, dEV=dEV, dSD=dSD, d=d, q=q, scale=scale,
                        pid=pid, participant=part, fold_of_problem=fold)
    np.savez_compressed(OUT, y=y)

    meta["log10_scale_cuts"] = cuts
    meta["fold_sizes_problems"] = sizes
    meta["fold_sizes_trials"] = [int((fold[pid] == f).sum())
                                 for f in range(N_FOLDS)]
    with open(os.path.join(HERE, "rows_meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)

    for k, v in meta.items():
        print("  %-24s %s" % (k, v))
    print()
    print("written rows_covariates.npz (no choice column) and rows_outcome.npz")


def load_covariates():
    z = np.load(COV)
    return (z["dEV"], z["dSD"], z["d"], z["q"], z["pid"],
            z["fold_of_problem"], z["scale"], z["participant"])


def load_outcome():
    """Opened only by the confirmatory fit, after the seal."""
    return np.load(OUT)["y"]


if __name__ == "__main__":
    main()
