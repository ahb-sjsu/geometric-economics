#!/usr/bin/env python3
"""Write one small problems file per corpus for score.py: XA, PA, XB, PB, k (choices of B), n, unit.
Problems are built exactly as in ../strata/fit_strata.py.

    python prep.py ROWS_DIR OUT_DIR
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "strata"))
import fit_strata as F  # noqa: E402


def save(out, name, pr, k, n):
    np.savez_compressed(os.path.join(out, f"problems_{name}.npz"), XA=pr.XA, PA=pr.PA, XB=pr.XB, PB=pr.PB,
                        k=k, n=n, unit=pr.unit)
    print(name, len(pr), int(n.sum()))


def main(rows_dir, out):
    os.makedirs(out, exist_ok=True)
    save(out, "cpc18", *F.cpc18_problems())
    for name in F.CORPORA:
        r = F.corpus_rows(rows_dir, name)
        keep = ~np.load(os.path.join(rows_dir, f"{name}_overlap_mask.npy"))
        y = np.load(os.path.join(rows_dir, f"{name}_outcome.npz"))["chose_B"][keep].astype(float)
        pr, k, n, _ = F.to_problems(r, y)
        save(out, name, pr, k, n)


if __name__ == "__main__":
    main(*sys.argv[1:])
