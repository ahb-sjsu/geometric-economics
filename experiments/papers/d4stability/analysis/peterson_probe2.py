#!/usr/bin/env python3
"""Second structure probe. Three open questions the first probe raised.

1. `trials per participant: min 0`. How many transcripts parse to nothing, and
   is that a real empty record or a format this parser does not handle? A parser
   that silently drops transcripts is a parser that selects its own sample.
2. `log10 outcome scale: min -9.00`, which is the floor this code substitutes for
   a scale of exactly zero. How many problems have a riskier option whose
   outcomes are both zero, and what should be done with them?
3. How much of peterson's problem set is the choices13k Block 1, Feedback 0
   subset the aggregate fit of `prereg-d4interior-v3` ran on? That overlap
   decides whether an anchor comparing the two is a like-for-like check.

Covariates only. The choice token is counted, never joined.

    python peterson_probe2.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
sys.path.insert(0, DATASETS)
sys.path.insert(0, HERE)

from d4_rotation import _opt_coords  # noqa: E402  IMPORTED, never restated
from peterson_probe import OPT, PRESS, feats, parse  # noqa: E402

C13K = os.path.join(DATASETS, "raw", "choices13k", "c13k_selections.csv")


def main():
    from datasets import load_dataset
    ds = load_dataset("marcelbinz/Psych-101", split="train")
    rows = [r for r in ds if r["experiment"] == "peterson2021using/exp1.csv"]

    # --- 1. empty transcripts -------------------------------------------------
    empties, n_empty_with_press, n_empty_with_opt = [], 0, 0
    counts = []
    for i, r in enumerate(rows):
        k = sum(1 for _ in parse(r["text"]))
        counts.append(k)
        if k == 0:
            empties.append(i)
            if PRESS.search(r["text"]):
                n_empty_with_press += 1
            if OPT.search(r["text"]):
                n_empty_with_opt += 1
    counts = np.array(counts)
    print("participants with zero parsed trials: %d of %d"
          % (len(empties), len(rows)))
    print("  of those, containing a press token : %d" % n_empty_with_press)
    print("  of those, containing an option line: %d" % n_empty_with_opt)
    if empties:
        t = rows[empties[0]]["text"]
        print("  first empty transcript, %d chars, head:" % len(t))
        for ln in t.split("\n")[:6]:
            print("    | " + ln[:110])
    print("  trials per participant histogram:",
          dict(zip(*[x.tolist() for x in np.unique(counts, return_counts=True)])))
    print()

    # --- 2. degenerate scale --------------------------------------------------
    seen = {}
    for r in rows:
        for a, b, pressed, keys in parse(r["text"]):
            _, sa = feats(*a)
            _, sb = feats(*b)
            risky = a if sa >= sb else b
            key = (round(a[0], 4), round(a[1], 4), round(a[2], 4),
                   round(b[0], 4), round(b[1], 4), round(b[2], 4))
            if key not in seen:
                seen[key] = (risky, sa, sb)

    zero_scale, zero_sd = [], 0
    for key, (risky, sa, sb) in seen.items():
        if max(abs(risky[0]), abs(risky[2])) <= 1e-12:
            zero_scale.append(key)
        if max(sa, sb) <= 1e-12:
            zero_sd += 1
    print("problems whose riskier option has both outcomes zero: %d of %d"
          % (len(zero_scale), len(seen)))
    print("problems where NEITHER option varies (both sd zero)  : %d" % zero_sd)
    for k in zero_scale[:4]:
        print("    A=(%g, %g, %g)  B=(%g, %g, %g)" % k)
    print()

    # --- 3. overlap with the aggregate fit's subset ---------------------------
    c = pd.read_csv(C13K, usecols=["Block", "Feedback", "Ha", "pHa", "La",
                                   "Hb", "pHb", "Lb"])
    c13k_all = set()
    for r in c.dropna(subset=["Ha", "pHa", "La", "Hb", "pHb", "Lb"]).itertuples():
        for k in (
            (round(r.Ha, 4), round(r.pHa, 4), round(r.La, 4),
             round(r.Hb, 4), round(r.pHb, 4), round(r.Lb, 4)),
            (round(r.Hb, 4), round(r.pHb, 4), round(r.Lb, 4),
             round(r.Ha, 4), round(r.pHa, 4), round(r.La, 4)),
        ):
            c13k_all.add(k)
    sub = c[(c["Block"] == 1) & (c["Feedback"] == 0)].dropna(
        subset=["Ha", "pHa", "La", "Hb", "pHb", "Lb"])
    c13k_desc = set()
    for r in sub.itertuples():
        for k in (
            (round(r.Ha, 4), round(r.pHa, 4), round(r.La, 4),
             round(r.Hb, 4), round(r.pHb, 4), round(r.Lb, 4)),
            (round(r.Hb, 4), round(r.pHb, 4), round(r.Lb, 4),
             round(r.Ha, 4), round(r.pHa, 4), round(r.La, 4)),
        ):
            c13k_desc.add(k)

    # peterson keys are stored A-then-B in sorted-letter order, so match either
    # orientation, which is why both were added above
    pk = set(seen)
    n_in_all = sum(1 for k in pk if k in c13k_all)
    n_in_desc = sum(1 for k in pk if k in c13k_desc)
    print("peterson distinct problems              : %d" % len(pk))
    print("  also in choices13k, any block/feedback: %d (%.1f%%)"
          % (n_in_all, 100.0 * n_in_all / len(pk)))
    print("  also in choices13k Block1 Feedback0   : %d (%.1f%%)"
          % (n_in_desc, 100.0 * n_in_desc / len(pk)))
    print("choices13k Block1 Feedback0 problems    : %d" % (len(c13k_desc) // 2))

    out = {
        "n_participants": len(rows),
        "n_zero_trial_participants": len(empties),
        "n_zero_trial_with_press_token": int(n_empty_with_press),
        "n_zero_trial_with_option_line": int(n_empty_with_opt),
        "n_distinct_problems": len(seen),
        "n_zero_scale_problems": len(zero_scale),
        "n_both_options_certain": int(zero_sd),
        "n_overlap_c13k_any": int(n_in_all),
        "n_overlap_c13k_description": int(n_in_desc),
        "n_c13k_description_problems": len(c13k_desc) // 2,
    }
    with open(os.path.join(HERE, "peterson_probe2.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written peterson_probe2.json")


if __name__ == "__main__":
    main()
