#!/usr/bin/env python3
"""Power and size simulation for prereg-d4interior-v2. Outcomes are never read.

Reads the choices13k stimulus columns and the per-problem subject count `n`
only. `bRate` is never read, so running this cannot inform any threshold with an
outcome. Row building and the coordinate come from `analysis/c13k_rows.py`,
which imports `_opt_coords` from `d4_rotation` rather than restating it.

Synthetic outcomes are generated from the CPC18 corners-dropped fit of
`experiments/papers/d4gate/analysis/diagnostic_pooling.json`, fit B, a result
already on record. Those coefficients are READ FROM THAT FILE at run time and
are not transcribed here. An earlier draft of this script transcribed them and
got five of the six wrong, which is the same class of error that voided
prereg-d4gate-v1, so the file is the only source.

  NULL     no chirality: c_dq = 0, every other coefficient at its fit B value.
  ALT(x)   c_dq = x, every other coefficient at its fit B value.

Targets are drawn as rates at the true per-problem subject counts, because the
fitted target is a rate. prereg-d4gate-v1 recorded that drawing one choice per
row instead overstates the noise by about an order of magnitude.

    python power_d4interior.py --reps 300 --seed 20260913
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "analysis")))

from c13k_rows import build, kappa_terms, fit_kappa, TERM_NAMES  # noqa: E402

# Fit B of the pooling diagnostic, CPC18 interior with corners dropped, read
# from the record rather than transcribed.
DIAG = os.path.abspath(os.path.join(
    HERE, "..", "..", "d4gate", "analysis", "diagnostic_pooling.json"))
with open(DIAG, encoding="utf-8") as _fh:
    _B = json.load(_fh)["fits"]["B_corners_dropped"]
FITB = np.array([_B["coefficients"][t] for t in TERM_NAMES])
FITB_BEV = 1.0  # not recorded in the diagnostic; fixed for simulation only
CPC18_CHIRALITY = float(_B["d*q"])


def run(reps, seed, alts):
    dEV, dSD, d, q, _, nsub = build(with_outcome=False)
    rng = np.random.default_rng(seed)
    T = kappa_terms(d, q)
    dq = d * q
    out = {
        "n_rows": int(len(d)),
        "n_nonzero_dq": int((dq != 0).sum()),
        "n_d_negative": int((d < 0).sum()),
        "n_d_positive": int((d > 0).sum()),
        "distinct_d_values": int(len(np.unique(np.round(d, 6)))),
        "subjects_per_problem_median": int(np.median(nsub)),
        "reps": reps, "seed": seed,
        "generative_coefficients": {k: float(v) for k, v in zip(TERM_NAMES, FITB)},
        "note": "outcomes never read; synthetic draws only",
    }

    def draw(c_dq):
        coef = FITB.copy()
        coef[2] = c_dq
        lin = FITB_BEV * dEV + (coef @ T) * dSD
        ptrue = 1.0 / (1.0 + np.exp(-lin))
        return rng.binomial(nsub, ptrue) / nsub

    def sample(c_dq):
        vals = []
        for _ in range(reps):
            r = fit_kappa(dEV, dSD, d, q, draw(c_dq))
            vals.append(float(r.x[3]))
        return np.array(vals)

    null = sample(0.0)
    T_pos = float(np.quantile(null, 0.95))   # one-sided, the sign is predicted
    out["null"] = {"T_pos_95pct_one_sided": T_pos,
                   "null_mean": float(null.mean()),
                   "null_sd": float(null.std())}

    out["power"] = {}
    for x in alts:
        v = sample(float(x))
        band_lo, band_hi = 0.5 * CPC18_CHIRALITY, 2.0 * CPC18_CHIRALITY
        out["power"][str(x)] = {
            "V1_sign_and_presence": float(np.mean(v > T_pos)),
            "V2_within_factor_two_band": float(np.mean((v >= band_lo) & (v <= band_hi))),
            "mean_estimate": float(v.mean()),
            "sd_estimate": float(v.std()),
        }
    out["factor_two_band"] = [0.5 * CPC18_CHIRALITY, 2.0 * CPC18_CHIRALITY]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=300)
    ap.add_argument("--seed", type=int, default=20260913)
    ap.add_argument("--alts", default="0.0,0.2219,0.4438,0.8876")
    ap.add_argument("--out", default=os.path.join(HERE, "power_d4interior.json"))
    a = ap.parse_args()
    res = run(a.reps, a.seed, [float(x) for x in a.alts.split(",")])
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
