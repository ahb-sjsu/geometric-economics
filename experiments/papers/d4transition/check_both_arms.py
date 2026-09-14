#!/usr/bin/env python3
"""Both arms must run through one analysis, and the pair rule must be able to fail.

Arm A names its controls `CTRL_G` and `CTRL_M`. Arm B names them `CTRL_LO` and
`CTRL_HI`. `pilot_analysis` reads the names from the data rather than hardcoding
arm A's, because a hardcoded lookup would have missed every arm B record and
discarded the cell **silently**, which is the failure mode this programme keeps
finding.

What is required is structural and is enforced. Exactly three pair types, exactly
one of them the crossing pair.

    python check_both_arms.py
"""
from __future__ import annotations

import json
import os

import pilot_analysis as P

HERE = os.path.dirname(os.path.abspath(__file__))

ARM_A = ("CROSS", "CTRL_G", "CTRL_M")
ARM_B = ("CROSS", "CTRL_LO", "CTRL_HI")


def main():
    print("=" * 72)
    print("ONE ANALYSIS, BOTH ARMS")
    print("=" * 72)
    ok = True
    for label, pairs in (("arm A", ARM_A), ("arm B", ARM_B)):
        recs = P.simulate(pairs=list(pairs), mean_excess=0.5, seed=77)
        out = P.analyse(recs, provenance="simulated")
        print("  %-6s pairs %-34s families %d  between-family sd %.4f"
              % (label, ",".join(pairs), out["n_families"],
                 out["between_family_sd"]))
        if out["n_families"] != 30:
            print("       families lost, the pair lookup dropped records")
            ok = False

    print()
    print("  the pair rule must reject what it cannot analyse")
    for label, bad, expect in (
        ("two pair types", [{"pair": "CROSS"}, {"pair": "CTRL_LO"}], "three"),
        ("four pair types", [{"pair": x} for x in ("CROSS", "A", "B", "C")], "three"),
        ("no crossing pair", [{"pair": x} for x in ("X", "Y", "Z")], "CROSS"),
    ):
        try:
            P.pair_names(bad)
            print("    %-18s -> ACCEPTED, which is wrong" % label)
            ok = False
        except AssertionError as e:
            hit = expect in str(e)
            print("    %-18s -> %s" % (label, "rejected" if hit else "rejected for the wrong reason"))
            ok = ok and hit

    print()
    print("  arm B stimuli, delivered")
    with open(os.path.join(HERE, "stimuli_armb.json"), encoding="utf-8") as fh:
        b = json.load(fh)
    names = sorted(b["families"][0]["pairs"])
    print("    %d families, pair names %s" % (b["n_families"], names))
    if sorted(ARM_B) != names:
        print("    stimulus pair names do not match what the analysis expects")
        ok = False
    else:
        print("    they match what the analysis reads")

    print()
    print("=" * 72)
    print("BOTH ARMS: %s" % ("OK" if ok else "FAILURE"))
    print("=" * 72)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
