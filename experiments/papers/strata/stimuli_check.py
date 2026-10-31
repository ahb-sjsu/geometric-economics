#!/usr/bin/env python3
"""Stimulus-only checks before sealing prereg-strata-v1. Reads covariate files, never outcomes.

1. Overlap: each corpus's problems keyed against CPC18, choices13k and Wulff. A problem is the
   unordered pair of its options, each a sorted tuple of (outcome, probability) rounded to 0.01.
   CPC18 and choices13k use the two-outcome (H, pH, L) form, so a multi-outcome CPC18 shape can
   only match a corpus problem with the same approximation; the count is a lower bound there.
2. Environment: per corpus, the distribution of branch probabilities strictly inside (0, 1),
   binned, and the U-shape index (share in the outer fifths minus share in the middle fifth).
   Frydman and Jin: an inverse-S weighting function needs a U-shaped prior over probabilities.

    python stimuli_check.py ROWS        # writes ROWS/stimuli_check.json and overlap masks
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "datasets", "raw")
CORPORA = ["gp2012", "pachur2017", "pachur2018", "zilker2020", "babula2018", "baselberlin"]


def okey(X, P):
    return tuple(sorted((round(float(x), 2), round(float(p), 2)) for x, p in zip(X, P) if p > 0))


def two(H, p, L):
    return okey([H, L], [p, 1 - p]) if p < 1 else okey([H], [1.0])


def pkey(a, b):
    return tuple(sorted([a, b]))


def reference_keys():
    keys = {}
    c = pd.read_csv(os.path.join(DATA, "cpc18_raw.csv"), usecols=["GameID", "Ha", "pHa", "La", "Hb", "pHb", "Lb"])
    for r in c.groupby("GameID").first().itertuples():
        keys.setdefault(pkey(two(r.Ha, r.pHa, r.La), two(r.Hb, r.pHb, r.Lb)), set()).add("cpc18")
    k = pd.read_csv(os.path.join(DATA, "choices13k", "c13k_selections.csv"))
    for r in k.itertuples():
        keys.setdefault(pkey(two(r.Ha, r.pHa, r.La), two(r.Hb, r.pHb, r.Lb)), set()).add("choices13k")
    w = np.load(os.path.join(HERE, "..", "psych101", "wulff_rows_covariates.npz"))
    for a, b in {(tuple(a), tuple(b)) for a, b in zip(w["A"], w["B"])}:
        keys.setdefault(pkey(two(*a), two(*b)), set()).add("wulff")
    return keys


def u_index(p):
    h = np.histogram(p, bins=5, range=(0, 1))[0] / max(len(p), 1)
    return h.tolist(), float(h[0] + h[4] - h[2])


def main(rows):
    ref = reference_keys()
    out = {}
    c = pd.read_csv(os.path.join(DATA, "cpc18_raw.csv"), usecols=["GameID", "pHa", "pHb", "Amb"])
    g = c.groupby("GameID").first()
    g = g[g["Amb"] == 0]
    p = np.r_[g["pHa"], 1 - g["pHa"], g["pHb"], 1 - g["pHb"]]
    hist, u = u_index(p[(p > 0) & (p < 1)])
    out["cpc18_environment"] = {"prob_hist_fifths": hist, "u_index": u}
    for name in CORPORA:
        f = os.path.join(rows, f"{name}_covariates.npz")
        if not os.path.exists(f):
            out[name] = "no covariates"
            continue
        d = np.load(f)
        keys = [pkey(okey(xa, pa), okey(xb, pb)) for xa, pa, xb, pb in zip(d["XA"], d["PA"], d["XB"], d["PB"])]
        hits = np.array([k in ref for k in keys])
        src = {}
        for k in set(keys):
            for s in ref.get(k, ()):
                src[s] = src.get(s, 0) + 1
        np.save(os.path.join(rows, f"{name}_overlap_mask.npy"), hits)
        P = np.r_[d["PA"].ravel(), d["PB"].ravel()]
        hist, u = u_index(P[(P > 0) & (P < 1)])
        out[name] = {"rows": int(len(keys)), "problems": len(set(keys)),
                     "overlapping_problems_by_source": src, "overlapping_rows": int(hits.sum()),
                     "prob_hist_fifths": hist, "u_index": u,
                     "max_branches": int(max((d["PA"] > 0).sum(1).max(), (d["PB"] > 0).sum(1).max()))}
    json.dump(out, open(os.path.join(rows, "stimuli_check.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
