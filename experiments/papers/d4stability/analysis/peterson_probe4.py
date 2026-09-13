#!/usr/bin/env python3
"""Fourth structure probe. Full press accounting and the description subset.

Probe 3 found the first parser was discarding 91 percent of the press tokens in
the corpus, because a problem is declared once and then chosen from five times
with outcome feedback after each press. `peterson_parse` replaces it and puts
every press token into a named bucket. This runs that accounting on the real
corpus and then describes the bucket the registration will actually use.

Covariates only, with one exception stated plainly: the marginal fraction of
first presses that took the riskier option is reported, because a corpus whose
overall risk rate is absurd is a corpus that has been misparsed. That single
number is a marginal and is never joined to a covariate here, and no model is
fitted.

    python peterson_probe4.py
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


def main():
    from datasets import load_dataset
    ds = load_dataset("marcelbinz/Psych-101", split="train")
    rows = [r for r in ds if r["experiment"] == "peterson2021using/exp1.csv"]
    print("participants:", len(rows))

    counts = {b: 0 for b in BUCKETS}
    total_tokens = 0
    first = []                      # (dEV, dSD, d, q, chose_risky, scale, part)
    parts_with_first = set()

    for i, r in enumerate(rows):
        text = r["text"]
        total_tokens += len(PRESS.findall(text))
        for bucket, a, b, chose_a, idx, had_fb in trials(text):
            counts[bucket] += 1
            if bucket != PRESS_FIRST:
                continue
            evA, sdA = feats(*a)
            evB, sdB = feats(*b)
            risky_is_a = sdA >= sdB
            H, p, L = a if risky_is_a else b
            dc, qc = _opt_coords(H, p, L)
            chose_risky = (chose_a == risky_is_a)
            first.append((evA - evB, sdA - sdB, dc, qc, chose_risky,
                          max(abs(H), abs(L)), i,
                          (round(a[0], 4), round(a[1], 4), round(a[2], 4),
                           round(b[0], 4), round(b[1], 4), round(b[2], 4))))
            parts_with_first.add(i)

    bucketed = sum(counts.values())
    print()
    print("PRESS ACCOUNTING")
    for b in BUCKETS:
        print("  %-32s %9d  %6.2f%%"
              % (b, counts[b], 100.0 * counts[b] / max(total_tokens, 1)))
    print("  %-32s %9d" % ("bucketed total", bucketed))
    print("  %-32s %9d" % ("press tokens in corpus", total_tokens))
    assert bucketed == total_tokens, "accounting does not balance"
    print("  balances exactly")

    dEV = np.array([f[0] for f in first])
    dSD = np.array([f[1] for f in first])
    d = np.array([f[2] for f in first])
    q = np.array([f[3] for f in first])
    y = np.array([f[4] for f in first], dtype=float)
    scale = np.array([f[5] for f in first])
    part = np.array([f[6] for f in first])
    keys = [f[7] for f in first]
    uniq = {}
    for k in keys:
        uniq.setdefault(k, len(uniq))
    pid = np.array([uniq[k] for k in keys])

    print()
    print("DESCRIPTION SUBSET, first press on each problem")
    print("  trials                 %d" % len(first))
    print("  participants           %d" % len(parts_with_first))
    print("  distinct problems      %d" % len(uniq))
    print("  trials per problem     mean %.1f"
          % (len(first) / max(len(uniq), 1)))
    print("  marginal risky rate    %.4f" % y.mean())
    print("  interior |d| < 0.9     %d problems"
          % len(set(pid[np.abs(d) < 0.9].tolist())))
    print("  d < 0 / d > 0          %d / %d trials"
          % (int((d < -1e-9).sum()), int((d > 1e-9).sum())))
    print("  rows with dSD == 0     %d" % int((np.abs(dSD) < 1e-12).sum()))
    print("  rows with scale == 0   %d" % int((scale <= 1e-12).sum()))

    # the pre-declared split axis, computed per distinct problem so fold sizes
    # are balanced in problems rather than in trials
    ok = scale > 1e-12
    pscale = {}
    for j in range(len(first)):
        if ok[j]:
            pscale.setdefault(pid[j], scale[j])
    ids = np.array(sorted(pscale))
    ls = np.log10(np.array([pscale[i] for i in ids]))
    cuts = np.quantile(ls, [0.25, 0.5, 0.75])
    fold_of = {i: int(np.digitize(l, cuts)) for i, l in zip(ids, ls)}
    print()
    print("  log10 scale cuts       %.6f  %.6f  %.6f" % tuple(cuts))
    print()
    print("  fold  problems   trials   interior   d<0    d>0   sd(d*q)   mean|dSD|")
    folds = {}
    for f in range(4):
        pm = np.array([fold_of.get(p, -1) == f for p in pid])
        probs = set(pid[pm].tolist())
        folds[str(f)] = {
            "n_problems": len(probs),
            "n_trials": int(pm.sum()),
            "n_interior_trials": int((np.abs(d[pm]) < 0.9).sum()),
            "n_d_negative": int((d[pm] < -1e-9).sum()),
            "n_d_positive": int((d[pm] > 1e-9).sum()),
            "dq_sd": float((d[pm] * q[pm]).std()),
            "mean_abs_dSD": float(np.abs(dSD[pm]).mean()),
        }
        print("  %4d  %8d %8d %10d %6d %6d %9.3f %11.3f"
              % (f, len(probs), pm.sum(), (np.abs(d[pm]) < 0.9).sum(),
                 (d[pm] < -1e-9).sum(), (d[pm] > 1e-9).sum(),
                 (d[pm] * q[pm]).std(), np.abs(dSD[pm]).mean()))

    out = {
        "n_participants": len(rows),
        "press_accounting": {b: int(counts[b]) for b in BUCKETS},
        "press_tokens_total": int(total_tokens),
        "description": {
            "n_trials": len(first),
            "n_participants": len(parts_with_first),
            "n_distinct_problems": len(uniq),
            "marginal_risky_rate": float(y.mean()),
            "n_rows_zero_dSD": int((np.abs(dSD) < 1e-12).sum()),
            "n_rows_zero_scale": int((scale <= 1e-12).sum()),
            "n_d_negative": int((d < -1e-9).sum()),
            "n_d_positive": int((d > 1e-9).sum()),
        },
        "log10_scale_cuts": [float(c) for c in cuts],
        "scale_folds": folds,
    }
    with open(os.path.join(HERE, "peterson_probe4.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written peterson_probe4.json")


if __name__ == "__main__":
    main()
