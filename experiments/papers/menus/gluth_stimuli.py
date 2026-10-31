#!/usr/bin/env python3
"""Stimulus-only checks on the held-back Gluth data. Reads gluth_covariates.npz, never the outcome file.

For the sealed menus test: how often D sits outside the HV-LV range on each attribute (only then can
range scaling move the HV-LV choice), and how much menu ranges vary (a crossover needs ranges spanning
an order of magnitude).

    python gluth_stimuli.py ROWS_DIR
"""
import json
import os
import sys

import numpy as np


def main(rows):
    c = np.load(os.path.join(rows, "gluth_covariates.npz"))
    out = {}
    for exp in np.unique(c["exp"]):
        m = c["exp"] == exp
        has_d = m & ~np.isnan(c["d_mag"])
        res = {"rows": int(m.sum()), "rows_with_D": int(has_d.sum()), "participants": int(len(np.unique(c["subject"][m]))),
               "trial_types": {str(k): int(v) for k, v in zip(*np.unique(c["trial_type"][m], return_counts=True))},
               "groups": {str(k): int(v) for k, v in zip(*np.unique(c["group"][m], return_counts=True))}}
        for a in ("mag", "prob"):
            hv, lv, dd = c[f"hv_{a}"][has_d], c[f"lv_{a}"][has_d], c[f"d_{a}"][has_d]
            lo, hi = np.minimum(hv, lv), np.maximum(hv, lv)
            r2 = hi - lo
            r3 = np.maximum(hi, dd) - np.minimum(lo, dd)
            res[a] = {"D_extends_range_share": float(np.mean(r3 > r2 + 1e-9)),
                      "D_above_share": float(np.mean(dd > hi + 1e-9)), "D_below_share": float(np.mean(dd < lo - 1e-9)),
                      "range_with_D_quantiles": np.percentile(r3, [5, 25, 50, 75, 95]).round(4).tolist(),
                      "range_ratio_95_5": float(np.percentile(r3[r3 > 0], 95) / max(np.percentile(r3[r3 > 0], 5), 1e-9)),
                      "range_without_D_zero_share": float(np.mean(r2 == 0))}
        out[str(exp)] = res
    json.dump(out, open(os.path.join(rows, "gluth_stimuli.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
