#!/usr/bin/env python3
"""Grader for prereg-d4gate-v1. Written BEFORE any fit was run on the outcome.

Reads results.json produced by d4gate_fit.py and reports each registered
prediction as PASS or FAIL against the frozen thresholds. The thresholds live
here and nowhere else, so the fitting code cannot see them.

Registered predictions, transcribed from prereg-d4gate-v1.md Section 5, with
bars from the Section 7 simulation (covariates and subject counts only, outcomes
never read, 400 replicates, seed 20260912):

  G1  gating.               |gamma| >= 0.2778192266034961
  G2  presence where gated. |c2 + gamma| >= 0.18095219285614153

Each bar is the 95th percentile of the null distribution of its statistic, so
each test has a size of 0.05 under no chirality anywhere.

Falsifiers, Section 6:

  F1  Both statistics under their bars means the chirality is recovered nowhere
      under the declared gate. The gated reading fails and the rotation is
      absent in the interior.
  F3  G1 passing while G2 fails means the cells differ with no chirality present
      in either. That is NOT evidence for a gated rotation and the grader says so
      in the output rather than leaving it to a reader.

No composite verdict is registered. Each prediction stands alone.

    python d4gate_grade.py results.json
"""
from __future__ import annotations

import json
import sys

T_GAMMA = 0.2778192266034961      # 95th pct of |gamma| under the null
T_PRESENCE = 0.18095219285614153  # 95th pct of |c2 + gamma| under the null

BUNDLE_SHA = "bc85ddd92cdabe48daa81014748d6e1e2732a850ca7212882540ed606501f35b"

POWER = {  # from power_d4gate.json, reported for the reader's calibration
    "0.25": {"G1": 0.2925, "G2": 0.6025},
    "0.50": {"G1": 0.9525, "G2": 1.0000},
}


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "results.json"
    with open(path, encoding="utf-8") as fh:
        r = json.load(fh)

    gamma = r["gate_increment_gamma"]
    c2 = r["chirality_uncertain_c2"]
    presence = r["chirality_certain_c2_plus_gamma"]

    g1 = abs(gamma) >= T_GAMMA
    g2 = abs(presence) >= T_PRESENCE

    out = {
        "prereg": "prereg-d4gate-v1",
        "n_total": r["n_total"],
        "G1": {"verdict": "PASS" if g1 else "FAIL", "gamma": gamma,
               "abs_gamma": abs(gamma), "bar": T_GAMMA,
               "statement": "the chirality differs by gate"},
        "G2": {"verdict": "PASS" if g2 else "FAIL",
               "c2_plus_gamma": presence, "abs": abs(presence),
               "bar": T_PRESENCE,
               "statement": "a chirality is present where the gate fires"},
        "c2_uncertain": c2,
        "power_at_alternatives": POWER,
    }

    if not g1 and not g2:
        out["F1"] = ("FIRED. The chirality is recovered nowhere under the declared "
                     "gate. The gated reading fails and the rotation is absent in "
                     "the interior, so the verdict of RESULTS_d4_rotation.md "
                     "stands as written.")
    if g1 and not g2:
        out["F3"] = ("FIRED. The cells differ but no chirality is present in "
                     "either. This is NOT evidence for a gated rotation and must "
                     "not be reported as one.")

    print("=" * 70)
    print("prereg-d4gate-v1  ---  graded verdicts")
    print("bundle sha256", BUNDLE_SHA)
    print("=" * 70)
    for k in ("G1", "G2"):
        v = out[k]
        print("  %s  %-4s  %s" % (k, v["verdict"], v["statement"]))
    print()
    print("  gamma            = %+.4f  (bar %.4f)" % (gamma, T_GAMMA))
    print("  c2 + gamma       = %+.4f  (bar %.4f)" % (presence, T_PRESENCE))
    print("  c2 (uncertain)   = %+.4f" % c2)
    for key in ("F1", "F3"):
        if key in out:
            print()
            print("  %s: %s" % (key, out[key]))
    print()
    print("  Power was 0.95 for G1 and 1.00 for G2 at a gated chirality of 0.50,")
    print("  and 0.29 and 0.60 at 0.25. A failure at a true effect below 0.25 is")
    print("  a failure of this design and not evidence of absence.")
    print("=" * 70)

    with open("grade.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("written grade.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
