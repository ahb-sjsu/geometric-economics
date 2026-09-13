#!/usr/bin/env python3
"""Rebuild the raw option parameters alongside the sealed v2 covariates.

`stability_rows_v2.py` is sealed and is not touched. It stores `(dEV, dSD, d, q,
scale, pid, participant, fold)` and not the option parameters themselves, which
the seam analysis needs: whether an option has a loss branch at all is a fact
about `(H, p, L)` and the claim that `d` encodes it has to be checked rather than
asserted.

This re-walks the identical loop, keeps the identical rows, and writes the risky
and safe option parameters in the identical order. **It asserts that the `d`, `q`
and `dSD` it recomputes match the sealed file exactly**, so any drift in the
parse, the filters or the ordering fails here rather than silently producing a
misaligned analysis.

    python seam_covariates.py
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

from peterson_parse import PRESS_FIRST, feats, trials  # noqa: E402
from stability_rows_v2 import load_covariates, row_from_menu  # noqa: E402

OUT = os.path.join(HERE, "seam_covariates.npz")


def main():
    from datasets import load_dataset
    ds = load_dataset("marcelbinz/Psych-101", split="train")
    rows = [r for r in ds if r["experiment"] == "peterson2021using/exp1.csv"]

    keep = []
    for r in rows:
        for bucket, a, b, chose_a, idx, had_fb in trials(r["text"]):
            if bucket != PRESS_FIRST:
                continue
            row, why = row_from_menu(a, b, chose_a)
            if row is None:
                continue
            evA, sdA = feats(*a)
            evB, sdB = feats(*b)
            risky, safe = (a, b) if sdA >= sdB else (b, a)
            keep.append((risky[0], risky[1], risky[2],
                         safe[0], safe[1], safe[2],
                         row[2], row[3], row[1]))

    arr = lambda j: np.array([k[j] for k in keep], float)
    rH, rp, rL = arr(0), arr(1), arr(2)
    sH, sp, sL = arr(3), arr(4), arr(5)
    d_new, q_new, dSD_new = arr(6), arr(7), arr(8)

    dEV, dSD, d, q, pid, fold, scale, part = load_covariates()
    assert len(d_new) == len(d), (
        "row count differs from the sealed file: %d against %d" % (len(d_new), len(d)))
    for name, new, old in (("d", d_new, d), ("q", q_new, q), ("dSD", dSD_new, dSD)):
        worst = float(np.max(np.abs(new - old)))
        assert worst < 1e-12, "%s does not match the sealed file, worst %.3e" % (name, worst)
        print("  %-4s matches the sealed covariates exactly (worst %.1e)" % (name, worst))

    np.savez_compressed(OUT, risky_H=rH, risky_p=rp, risky_L=rL,
                        safe_H=sH, safe_p=sp, safe_L=sL)
    print()
    print("rows %d, written seam_covariates.npz" % len(rH))

    # the claim the seam analysis rests on, checked here rather than assumed
    has_loss = (np.minimum(rH, rL) < 0)
    has_gain = (np.maximum(rH, rL) > 0)
    mixed = has_loss & has_gain
    print()
    print("  d == +1 exactly : %d rows" % int((d == 1.0).sum()))
    print("  d == -1 exactly : %d rows" % int((d == -1.0).sum()))
    print("  |d| <  1        : %d rows" % int((np.abs(d) < 1.0).sum()))
    print("  risky option is mixed (a gain branch AND a loss branch): %d"
          % int(mixed.sum()))
    agree_pos = bool(np.all((d == 1.0) == (~has_loss)))
    agree_neg = bool(np.all((d == -1.0) == (~has_gain)))
    agree_mix = bool(np.all((np.abs(d) < 1.0) == mixed))
    print()
    print("  d == +1  <=>  the risky option has NO loss branch : %s" % agree_pos)
    print("  d == -1  <=>  the risky option has NO gain branch : %s" % agree_neg)
    print("  |d| < 1  <=>  the risky option is mixed           : %s" % agree_mix)
    with open(os.path.join(HERE, "seam_covariates.json"), "w",
              encoding="utf-8") as fh:
        json.dump({"n_rows": int(len(rH)),
                   "n_d_plus_one": int((d == 1.0).sum()),
                   "n_d_minus_one": int((d == -1.0).sum()),
                   "n_interior": int((np.abs(d) < 1.0).sum()),
                   "d_plus_one_iff_no_loss_branch": agree_pos,
                   "d_minus_one_iff_no_gain_branch": agree_neg,
                   "abs_d_lt_one_iff_mixed": agree_mix}, fh, indent=2)
    print("written seam_covariates.json")


if __name__ == "__main__":
    main()
