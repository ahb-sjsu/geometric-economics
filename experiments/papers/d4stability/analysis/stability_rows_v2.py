#!/usr/bin/env python3
"""Row builder for prereg-d4stability-v2. Orientation fixed, and made structural.

**What went wrong in v1.** The regressors were differenced in the order the two
options happened to be declared in the transcript,

    dEV = evA - evB ,  dSD = sdA - sdB

while the outcome was built as "chose the riskier option". Those two orientations
disagree on every problem where B is the riskier option, which is 74.8 percent of
rows, so the risk term was fitted with its sign reversed on three quarters of the
corpus. Reorienting improved the fit by 2,675 log-likelihood units and flipped
the chirality from `-0.1775` to `+0.2506`.

**The fix is not to difference more carefully. It is to remove declaration order
from the pipeline entirely.** Here every row is oriented by risk:

    dEV = ev_risky - ev_safe ,  dSD = sd_risky - sd_safe > 0

so `dSD` is positive by construction, `y = 1` means the participant took the
risk, and the two agree on every row. Which option was printed first never enters.
That makes the estimand invariant to relabelling A and B **by construction rather
than by care**, and `pipeline_invariants.py` proves it rather than trusting it.

Three guards run at build time and refuse to write the corpus if they fail:

  * `dSD > 0` on every kept row, so an orientation error cannot be written out;
  * the coordinate is invariant under positive scaling of both outcomes, which is
    what makes outcome scale a legitimate split axis;
  * the press accounting balances against the corpus total.

Everything else is unchanged from v1: the same parser, the same inclusion rules,
the same separation of covariates from outcomes into different files so that the
power simulation cannot read the choices.

    python stability_rows_v2.py
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

COV = os.path.join(HERE, "rows_covariates_v2.npz")
OUT = os.path.join(HERE, "rows_outcome_v2.npz")
N_FOLDS = 4


def row_from_menu(a, b, chose_a):
    """One row, oriented by risk and never by declaration order.

    Returns `(dEV, dSD, d, q, y, scale)` or None if the menu is excluded.
    Swapping `a` and `b` and negating `chose_a` returns exactly the same row,
    which is the property v1 lacked.
    """
    evA, sdA = feats(*a)
    evB, sdB = feats(*b)
    if abs(sdA - sdB) < 1e-12:
        return None, "zero_dSD"
    if sdA >= sdB:
        risky, safe, chose_risky = a, b, chose_a
        ev_r, sd_r, ev_s, sd_s = evA, sdA, evB, sdB
    else:
        risky, safe, chose_risky = b, a, (not chose_a)
        ev_r, sd_r, ev_s, sd_s = evB, sdB, evA, sdA
    H, p, L = risky
    scale = max(abs(H), abs(L))
    if scale <= 1e-12:
        return None, "zero_scale"
    dc, qc = _opt_coords(H, p, L)
    return (ev_r - ev_s, sd_r - sd_s, dc, qc, float(chose_risky), scale), None


def problem_key(a, b):
    """Identity of a problem, independent of which option was declared first."""
    ka = (round(a[0], 4), round(a[1], 4), round(a[2], 4))
    kb = (round(b[0], 4), round(b[1], 4), round(b[2], 4))
    return tuple(sorted([ka, kb]))


def parse_corpus():
    from datasets import load_dataset
    ds = load_dataset("marcelbinz/Psych-101", split="train")
    rows = [r for r in ds if r["experiment"] == "peterson2021using/exp1.csv"]

    counts = {b: 0 for b in BUCKETS}
    total_tokens = 0
    keep, excl = [], {"zero_dSD": 0, "zero_scale": 0}
    uniq = {}
    n_scale_checks = n_scale_violations = 0

    for i, r in enumerate(rows):
        text = r["text"]
        total_tokens += len(PRESS.findall(text))
        for bucket, a, b, chose_a, idx, had_fb in trials(text):
            counts[bucket] += 1
            if bucket != PRESS_FIRST:
                continue
            row, why = row_from_menu(a, b, chose_a)
            if row is None:
                excl[why] += 1
                continue
            dEV, dSD, dc, qc, y, scale = row
            for lam in (7.3, 0.137):
                H, p, L = (a if feats(*a)[1] >= feats(*b)[1] else b)
                d2, q2 = _opt_coords(H * lam, p, L * lam)
                n_scale_checks += 1
                if abs(d2 - dc) > 1e-9 or abs(q2 - qc) > 1e-9:
                    n_scale_violations += 1
            pid = uniq.setdefault(problem_key(a, b), len(uniq))
            keep.append((dEV, dSD, dc, qc, y, scale, pid, i))

    assert sum(counts.values()) == total_tokens, "press accounting does not balance"
    assert n_scale_violations == 0, (
        "the coordinate is not invariant under outcome scaling on %d checks, so "
        "outcome scale is not a legitimate split axis" % n_scale_violations)
    dsd = np.array([k[1] for k in keep])
    assert bool((dsd > 0).all()), (
        "ORIENTATION GUARD FAILED: %d rows have dSD <= 0. Every row must be "
        "oriented risky-minus-safe. This is the guard v1 did not have."
        % int((dsd <= 0).sum()))

    meta = {
        "press_accounting": {b: int(counts[b]) for b in BUCKETS},
        "press_tokens_total": int(total_tokens),
        "excluded_zero_dSD": excl["zero_dSD"],
        "excluded_zero_scale": excl["zero_scale"],
        "n_trials_kept": len(keep),
        "n_distinct_problems": len(uniq),
        "n_participants": len(rows),
        "scale_invariance_checks": n_scale_checks,
        "scale_invariance_violations": n_scale_violations,
        "orientation_guard": "all dSD > 0",
        "min_dSD": float(dsd.min()),
    }
    return keep, meta


def fold_map(scale_by_problem):
    """Quartiles of log10 outcome scale over DISTINCT PROBLEMS.

    Scale is the axis because the coordinate `(d, q)` is exactly invariant under
    positive scaling of both outcomes, checked on every kept row above.
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
    arr = lambda j: np.array([k[j] for k in keep])
    dEV, dSD, d, q, y, scale = (arr(0), arr(1), arr(2), arr(3), arr(4), arr(5))
    pid = np.array([k[6] for k in keep], dtype=int)
    part = np.array([k[7] for k in keep], dtype=int)

    sbp = {}
    for j in range(len(keep)):
        sbp.setdefault(int(pid[j]), float(scale[j]))
    fold, cuts = fold_map(sbp)

    np.savez_compressed(COV, dEV=dEV, dSD=dSD, d=d, q=q, scale=scale,
                        pid=pid, participant=part, fold_of_problem=fold)
    np.savez_compressed(OUT, y=y)

    meta["log10_scale_cuts"] = cuts
    meta["fold_sizes_problems"] = [int((fold == f).sum()) for f in range(N_FOLDS)]
    meta["fold_sizes_trials"] = [int((fold[pid] == f).sum()) for f in range(N_FOLDS)]
    meta["marginal_risky_rate"] = float(y.mean())
    with open(os.path.join(HERE, "rows_meta_v2.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
    for k, v in meta.items():
        print("  %-26s %s" % (k, v))
    print()
    print("written rows_covariates_v2.npz (no choice column) and rows_outcome_v2.npz")


def load_covariates():
    z = np.load(COV)
    return (z["dEV"], z["dSD"], z["d"], z["q"], z["pid"],
            z["fold_of_problem"], z["scale"], z["participant"])


def load_outcome():
    """Opened only by the confirmatory fit, after the seal."""
    return np.load(OUT)["y"]


if __name__ == "__main__":
    main()
