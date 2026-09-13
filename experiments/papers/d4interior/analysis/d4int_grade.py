#!/usr/bin/env python3
"""Grader for prereg-d4interior-v2. Written BEFORE any fit touched `bRate`.

Reads results.json from d4int_fit.py and reports each registered prediction
against the frozen bars. The bars live here and nowhere else.

Bars from the Section 7 simulation (stimulus columns and subject counts only,
`bRate` never read, 300 replicates, seed 20260913):

  V1  sign and presence.   c2 > 0.18774979541410625, one-sided.
  V2  magnitude agreement. c2 in [0.2218875240708106, 0.8875500962832424],
                           a factor of two either side of the CPC18 estimate.

A caveat the simulation exposed and the grader repeats in its own output. Under
a true chirality of zero this estimator returns +0.092 on average in this design,
so it carries an upward bias of roughly 0.09 to 0.12 across the alternatives
tested. V1 is unaffected, because its bar is the 95th percentile of that same
null and so is calibrated for size, measured at 0.053. V2 compares a raw
choices13k estimate against a raw CPC18 estimate, and the two designs need not
carry the same bias, so V2 is the weaker claim and is reported as approximate.

    python d4int_grade.py results.json
"""
from __future__ import annotations

import json
import sys

T_POS = 0.18774979541410625          # 95th pct of the null, one-sided
BAND_LO = 0.2218875240708106         # half the CPC18 estimate
BAND_HI = 0.8875500962832424         # twice the CPC18 estimate
CPC18_ESTIMATE = 0.4437750481416212

NULL_MEAN = 0.09206812148266742      # estimator bias under a true zero
CONVERGENCE_TOL = 1e-6               # F3

BUNDLE_SHA = "49b2f3f5392e0b7cfade6612aa5b7ce0e355e51b3260588ae7b27037ebca141c"

POWER = {"0.2219": {"V1": 0.960, "V2": 0.947},
         "0.4438": {"V1": 1.000, "V2": 1.000},
         "0.8876": {"V1": 1.000, "V2": 0.190},
         "size_at_zero": {"V1": 0.053, "V2": 0.007}}


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "results.json"
    with open(path, encoding="utf-8") as fh:
        r = json.load(fh)

    c2 = r["chirality_dq"]
    conv = r["convergence"]["abs_difference"]

    void = conv > CONVERGENCE_TOL
    v1 = c2 > T_POS
    v2 = BAND_LO <= c2 <= BAND_HI
    reversed_sign = c2 < -T_POS

    out = {
        "prereg": "prereg-d4interior-v2",
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
        out["F3"] = ("VOID. The two optimizer starts differ in the objective by "
                     "%.3g, over the registered tolerance of %g." % (conv, CONVERGENCE_TOL))
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
    print("prereg-d4interior-v2  ---  graded verdicts")
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
    print("  Estimator bias: under a true zero this estimator returns %+.3f on"
          % NULL_MEAN)
    print("  average in this design. V1's bar is the 95th percentile of that")
    print("  same null, so V1 is calibrated, size 0.053. V2 compares two raw")
    print("  estimates whose biases need not match, so V2 is approximate.")
    print("=" * 72)

    with open("grade.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("written grade.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
