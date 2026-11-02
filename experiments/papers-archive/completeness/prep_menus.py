#!/usr/bin/env python3
"""Write the two menus datasets as small arrays for confidence.py: P, M (n, 3), shown, avail, y, subj.

    python prep_menus.py MOLTER_TRIALS_CSV GLUTH_ROWS_DIR OUT_DIR

Molter: three options, all available. Gluth: HV and LV available, the distractor shown when present
but not available; trials where it was pressed or no choice was made are dropped.
"""
import os
import sys

import numpy as np
import pandas as pd


def main(molter_csv, gluth_rows, out):
    t = pd.read_csv(molter_csv)
    t = t[t["choice"].isin(["A", "B", "C"])].reset_index(drop=True)
    P, M = t[["pA", "pB", "pC"]].to_numpy(float), t[["mA", "mB", "mC"]].to_numpy(float)
    ones = np.ones_like(P, bool)
    np.savez_compressed(os.path.join(out, "problems_menus_molter.npz"), P=P, M=M, shown=ones, avail=ones,
                        y=t["choice"].map({"A": 0, "B": 1, "C": 2}).to_numpy(), subj=t["subject"].to_numpy())
    print("molter", len(t), t["subject"].nunique())

    c = np.load(os.path.join(gluth_rows, "gluth_covariates.npz"))
    ch = np.load(os.path.join(gluth_rows, "gluth_outcome.npz"))["choice"]
    keep = np.isin(ch, ["HV", "LV"])
    has_d = ~np.isnan(c["d_mag"])
    P = np.c_[c["hv_prob"], c["lv_prob"], np.where(has_d, c["d_prob"], 0.5)][keep]
    M = np.c_[c["hv_mag"], c["lv_mag"], np.where(has_d, c["d_mag"], 1.0)][keep]
    shown = np.c_[np.ones_like(has_d), np.ones_like(has_d), has_d][keep]
    avail = np.c_[np.ones_like(has_d), np.ones_like(has_d), np.zeros_like(has_d)][keep]
    y = np.where(ch[keep] == "HV", 0, 1)
    ids = np.char.add(np.char.add(c["exp"].astype(str), "_"), c["subject"].astype(str))
    subj = np.unique(ids, return_inverse=True)[1].ravel()[keep]
    np.savez_compressed(os.path.join(out, "problems_menus_gluth.npz"), P=P, M=M, shown=shown, avail=avail, y=y,
                        subj=subj)
    print("gluth", int(keep.sum()), "of", len(ch), "trials,", len(np.unique(subj)), "participants,",
          int(has_d[keep].sum()), "with a distractor")


if __name__ == "__main__":
    main(*sys.argv[1:])
