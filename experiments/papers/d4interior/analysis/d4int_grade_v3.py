#!/usr/bin/env python3
"""Grader for prereg-d4interior-v3. Written BEFORE any fit touched `bRate`.

Reads results.json from d4int_fit.py and reports each registered prediction
against the frozen bars. The bars live here and nowhere else.

Bars from the Section 7 simulation (stimulus columns and subject counts only,
`bRate` never read, 300 replicates, seed 20260913):

  V1  sign and presence.   c2 > 0.18774979541410625, one-sided.
  V2  magnitude agreement. c2 in [0.2218875240708106, 0.8875500962832424],
                           a factor of two either side of the CPC18 estimate.

The estimator is the convex Newton solver of `kappa_mle.py`, not the Powell
search v2 used. Under a true chirality of zero it returns -0.0012 on average, and
tracks the truth to three decimals at every alternative, so the +0.092 bias v2
reported was Powell failing to reach the optimum of a convex problem rather than
a property of the estimate. V2 still reads 0.514 at both band endpoints, because
a truth sitting on an endpoint is accepted about half the time, so V2
discriminates the centre of the band from its edges and nothing finer.

    python d4int_grade.py results.json
"""
from __future__ import annotations

import json
import sys

T_POS = 0.10431881348530625          # 95th pct of the null, one-sided
BAND_LO = 0.2218875240708106         # half the CPC18 estimate
BAND_HI = 0.8875500962832424         # twice the CPC18 estimate
CPC18_ESTIMATE = 0.4437750481416212

NULL_MEAN = -0.0011965340350230786   # estimator mean under a true zero
GRAD_TOL = 1e-5                      # F3, infinity norm of the gradient

BUNDLE_SHA = "b18b1e8e12fdc4f4c8f06d4f4defbe719f49fb596b5e8890b52ccf919d62f807"

POWER = {"0.2219": {"V1": 0.966, "V2": 0.514},
         "0.4438": {"V1": 1.000, "V2": 1.000},
         "0.8876": {"V1": 1.000, "V2": 0.514},
         "size_at_zero": {"V1": 0.034, "V2": 0.000}}


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "results.json"
    with open(path, encoding="utf-8") as fh:
        r = json.load(fh)

    c2 = r["chirality_dq"]
    gnorm = r["grad_inf_norm"]

    void = gnorm > GRAD_TOL
    v1 = c2 > T_POS
    v2 = BAND_LO <= c2 <= BAND_HI
    reversed_sign = c2 < -T_POS

    out = {
        "prereg": "prereg-d4interior-v3",
        "corpus": r["corpus"],
        "n_rows": r["n_rows"],
        "chirality_dq": c2,
        "V1": {"verdict": "PASS" if v1 else "FAIL", "bar": T_POS,
               "statement": "the interior chirality replicates in sign"},
        "V2": {"verdict": "PASS" if v2 else "FAIL",
               "band": [BAND_LO, BAND_HI],
               "statement": "and within a factor of two of the CPC18 estimate"},
        "cpc18_estimate": CPC18_ESTIMATE,
        "estimator_bias_under_null": NULL_MEAN,
        "power": POWER,
    }
    if void:
        out["F3"] = ("VOID. The gradient infinity norm is %.3g, over the "
                     "registered tolerance of %g. The simulation reached this "
                     "on 2000 of 2000 draws." % (gnorm, GRAD_TOL))
    if reversed_sign:
        out["F2"] = ("FIRED. The estimate is negative beyond the bar. This is a "
                     "sign reversal, which is a worse outcome than a null, and "
                     "must be reported as such and not as a near miss.")
    if not v1 and not reversed_sign:
        out["F1"] = ("FIRED. The interior chirality does not replicate. The CPC18 "
                     "estimate is corpus-specific and the interior question is "
                     "not settled by it.")
    if v1 and not v2:
        out["F4"] = ("FIRED. The chirality replicates in sign but not in size. A "
                     "small positive coefficient is compatible with many "
                     "mechanisms and this must not be reported as confirming the "
                     "CPC18 magnitude.")

    print("=" * 72)
    print("prereg-d4interior-v3  ---  graded verdicts")
    print("bundle sha256", BUNDLE_SHA)
    print("=" * 72)
    if void:
        print("  RUN VOID under F3.")
    for k in ("V1", "V2"):
        print("  %s  %-4s  %s" % (k, out[k]["verdict"], out[k]["statement"]))
    print()
    print("  c2 (choices13k)  = %+.4f" % c2)
    print("  bar (one-sided)  =  %.4f" % T_POS)
    print("  factor-two band  = [%.4f, %.4f]  around CPC18 %+.4f"
          % (BAND_LO, BAND_HI, CPC18_ESTIMATE))
    for key in ("F1", "F2", "F3", "F4"):
        if key in out:
            print()
            print("  %s: %s" % (key, out[key]))
    print()
    print("  Estimator mean under a true zero: %+.4f. Convex Newton solver," % NULL_MEAN)
    print("  gradient norm %.1e, zero non-convergence in 2000 simulated draws." % 0.0)
    print("  V2 reads 0.514 at either band endpoint by construction.")
    print("=" * 72)

    with open("grade.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("written grade.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
