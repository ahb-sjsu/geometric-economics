#!/usr/bin/env python3
"""Hash the registration bundle, in the format this repository already uses.

WHAT IS IN THE BUNDLE

Everything that fixes a bar, a procedure, or a stimulus. A file is in if changing
it would change what the study concludes, and out if it only reports.

The arm B files are deliberately OUT. Arm B is built and is not registered in v1,
so sealing it would imply a commitment that has not been made. `check_both_arms.py`
and the arm B builder, sweep and template stay in the repository, unsealed, and a
later registration can seal them.

    python seal_bundle.py           # verify against the recorded seal
    python seal_bundle.py --write   # write it
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEAL = os.path.join(HERE, "prereg-d4transition-v1.sha256")

BUNDLE = [
    "prereg-d4transition-v1.md",     # the registration
    "DESIGN.md",                     # the design of record
    "PILOT.md",                      # the protocol
    "grade_transition.py",           # every bar lives here
    "power_transition.py",           # the registered sample
    "pilot_analysis.py",             # what the pilot may and may not emit
    "analysis_invariants.py",        # the suite V2 depends on
    "build_stimuli.py",              # the stimuli and the V4 tolerances
    "session_builder.py",            # the schedule and its checks
    "task_template.html",            # the instrument
]

META = {
    "prereg": "prereg-d4transition-v1",
    "title": "Is a Boundary Penalty Directional? Measuring an Edge Asymmetry "
             "with Bidirectional Price Lists",
    "level": 1,
    "author": "Andrew H. Bond, San Jose State University",
    "companion_to": ["prereg-d4stability-v2", "prereg-boundary-v1"],
    "frozen_predictions":
        "P1 and P2 in prereg-d4transition-v1.md Section 9; void conditions "
        "Section 10; sample and power Section 11; falsifiers Section 12. "
        "P3 was removed before any data and arm B is not registered.",
    "data": "NONE COLLECTED. This is a prospective registration. The pilot has "
            "not run and the confirmatory sample has not been collected. The "
            "document is frozen BEFORE the pilot deliberately, so that nothing "
            "the pilot measures can reach back into a bar or the sample size.",
    "hash_note": "sha256 of each file with CRLF normalized to LF; combined = "
                 "sha256 over the concatenated component hex digests in "
                 "bundle_files order",
}


def digest(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def build(frozen_at):
    comp = {}
    for rel in BUNDLE:
        p = os.path.join(HERE, rel)
        if not os.path.exists(p):
            raise SystemExit("bundle file missing: %s" % rel)
        comp[rel] = digest(p)
    combined = hashlib.sha256(
        "".join(comp[r] for r in BUNDLE).encode("ascii")).hexdigest()
    out = dict(META)
    out["frozen_at"] = frozen_at
    out["bundle_files"] = list(BUNDLE)
    out["component_sha256"] = comp
    out["combined_sha256"] = combined
    return out


def main():
    if "--write" in sys.argv:
        import datetime
        frozen = datetime.date.today().isoformat()
        if os.path.exists(SEAL):
            with open(SEAL, encoding="utf-8") as fh:
                frozen = json.load(fh).get("frozen_at", frozen)
            print("seal exists, keeping frozen_at %s" % frozen)
        out = build(frozen)
        with open(SEAL, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2)
            fh.write("\n")
        print("written %s" % os.path.basename(SEAL))
        print("  combined sha256 %s" % out["combined_sha256"])
        for r in BUNDLE:
            print("    %-32s %s" % (r, out["component_sha256"][r][:16]))
        return 0

    if not os.path.exists(SEAL):
        print("no seal recorded. run with --write")
        return 1
    with open(SEAL, encoding="utf-8") as fh:
        rec = json.load(fh)
    now = build(rec["frozen_at"])
    bad = [r for r in BUNDLE
           if rec["component_sha256"].get(r) != now["component_sha256"][r]]
    missing = [r for r in rec["bundle_files"] if r not in BUNDLE]
    print("SEAL CHECK, %s, frozen %s" % (rec["prereg"], rec["frozen_at"]))
    print("  recorded  %s" % rec["combined_sha256"])
    print("  computed  %s" % now["combined_sha256"])
    for r in BUNDLE:
        same = rec["component_sha256"].get(r) == now["component_sha256"][r]
        print("    %-32s %s" % (r, "ok" if same else "CHANGED SINCE THE SEAL"))
    if missing:
        print("  files in the seal but not in the bundle list: %s" % missing)
    ok = not bad and not missing and rec["combined_sha256"] == now["combined_sha256"]
    print("  %s" % ("SEAL INTACT" if ok else "SEAL BROKEN"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
