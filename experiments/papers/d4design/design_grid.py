#!/usr/bin/env python3
"""Construct two-outcome gambles that sit at declared (d, q) coordinates.

The record's own recommendation, in `RESULTS_d4_rotation.md`, is that "a dataset
designed to sit at intermediate (domain, probability) angles would settle the
interior test cleanly". Both corpora used so far are opportunistic. This builds
one that is not.

The coordinate is IMPORTED from `d4_rotation`, never restated, and every
constructed gamble is verified by round-tripping it back through that function.

For a two-outcome gamble (H, p; L, 1-p) with H > 0 > L, writing
`pos = p*H` and `neg = (1-p)*|L|`,

    d = (pos - neg) / (pos + neg)

so `neg/pos = (1 - d)/(1 + d)`, and the salient outcome is the one of larger
absolute value, whose probability sets `q = 2*p_salient - 1`. Inverting:

    given q, p_salient = (q + 1)/2
    given d, |L| = p*H*(1 - d) / ((1 + d)*(1 - p))     when H is salient

Feasibility is not automatic. The construction must also satisfy the salience
assumption it used, so every candidate is checked by recomputing (d, q) from the
generated numbers and keeping only exact round-trips.

    python design_grid.py
"""
from __future__ import annotations

import itertools
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "datasets"))
sys.path.insert(0, DATASETS)

from d4_rotation import _opt_coords  # noqa: E402  IMPORTED, never restated

TOL = 1e-6


def make_mixed(d_target, q_target, scale=100.0):
    """A mixed gamble (H, p; L) at the target coordinate, or None if infeasible.

    Two branches, because `q` is read off whichever outcome is salient. Fixing
    the gain as salient can only reach gain-leaning cells, which is why a first
    version of this returned 29 cells at d > 0 against 8 at d < 0 and nothing at
    d = -0.8. The loss-salient branch supplies the other half.
    """
    cands = []

    # gain salient: q = 2p - 1, fix H and solve for L
    p = (q_target + 1.0) / 2.0
    if 1e-6 < p < 1 - 1e-6 and abs(1.0 + d_target) > 1e-9:
        H = scale
        neg = (p * H) * (1.0 - d_target) / (1.0 + d_target)
        L = -neg / (1.0 - p)
        if np.isfinite(L) and abs(L) > 1e-9 and abs(H) > abs(L):
            cands.append((round(H, 4), round(p, 4), round(L, 4)))

    # loss salient: q = 1 - 2p, fix L and solve for H
    p = (1.0 - q_target) / 2.0
    if 1e-6 < p < 1 - 1e-6 and abs(1.0 - d_target) > 1e-9:
        L = -scale
        pos = ((1.0 - p) * abs(L)) * (1.0 + d_target) / (1.0 - d_target)
        H = pos / p
        if np.isfinite(H) and H > 1e-9 and abs(L) > abs(H):
            cands.append((round(H, 4), round(p, 4), round(L, 4)))

    return cands or None


def build_grid(d_vals, q_vals):
    kept, missed = [], []
    for d_t, q_t in itertools.product(d_vals, q_vals):
        cands = make_mixed(d_t, q_t)
        if cands is None:
            missed.append((d_t, q_t, "construction infeasible"))
            continue
        hit = None
        for H, p, L in cands:
            d_a, q_a = _opt_coords(H, p, L)      # round-trip through the real one
            if abs(d_a - d_t) <= 1e-3 and abs(q_a - q_t) <= 1e-3:
                hit = (H, p, L, float(d_a), float(q_a))
                break
        if hit is None:
            H, p, L = cands[0]
            d_a, q_a = _opt_coords(H, p, L)
            missed.append((d_t, q_t, "round-trip %.3f %.3f" % (d_a, q_a)))
            continue
        H, p, L, d_a, q_a = hit
        kept.append({"d_target": d_t, "q_target": q_t,
                     "H": H, "pH": p, "L": L,
                     "d_actual": d_a, "q_actual": q_a})
    return kept, missed


def main():
    d_vals = [round(v, 3) for v in np.linspace(-0.8, 0.8, 9)]
    q_vals = [round(v, 3) for v in np.linspace(-0.8, 0.8, 9)]
    kept, missed = build_grid(d_vals, q_vals)

    da = np.array([k["d_actual"] for k in kept])
    qa = np.array([k["q_actual"] for k in kept])
    dq = da * qa

    print("requested %d cells, constructed %d, infeasible %d"
          % (len(d_vals) * len(q_vals), len(kept), len(missed)))
    print("d  range %.2f to %.2f   distinct %d" % (da.min(), da.max(), len(set(da.round(3)))))
    print("q  range %.2f to %.2f   distinct %d" % (qa.min(), qa.max(), len(set(qa.round(3)))))
    print("d*q range %.2f to %.2f  sd %.3f" % (dq.min(), dq.max(), dq.std()))
    print()
    print("coverage by sign of d, which is what the chirality needs")
    print("  d < 0 : %d cells" % int((da < -1e-9).sum()))
    print("  d = 0 : %d cells" % int((np.abs(da) <= 1e-9).sum()))
    print("  d > 0 : %d cells" % int((da > 1e-9).sum()))
    if missed:
        print()
        print("infeasible examples")
        for m in missed[:6]:
            print("  d=%+.2f q=%+.2f  %s" % m)

    with open(os.path.join(HERE, "design_grid.json"), "w", encoding="utf-8") as fh:
        json.dump({"n_cells": len(kept), "cells": kept,
                   "n_infeasible": len(missed)}, fh, indent=2)
    print()
    print("written design_grid.json")


if __name__ == "__main__":
    main()
