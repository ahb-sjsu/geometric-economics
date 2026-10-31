#!/usr/bin/env python3
"""Hash the prereg-menus-v1 bundle, in the format this repository already uses.

A file is in the bundle if changing it would change what the study concludes.

    python seal_menus.py           # verify against the recorded seal
    python seal_menus.py --write   # write it
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEAL = os.path.join(HERE, "prereg-menus-v1.sha256")

BUNDLE = [
    "prereg-menus-v1.md",          # the registration
    "gluth_rows.py",               # parser, response coding, exclusions, accounting
    "gluth_stimuli.py",            # stimulus-only checks
    "gluth_accounting.json",       # row accounting per experiment
    "gluth_stimuli.json",          # menu ranges and distractor placement, stimuli only
    "menus_models.py",             # every model, and the frozen exponent RHO_STAR
    "fit_menus.py",                # calibration on binary trials, scoring on distractor trials
    "grade_menus.py",              # every bar
    "explore_molter3.json",        # the development fits RHO_STAR and Molter's IQR come from
]

META = {
    "prereg": "prereg-menus-v1",
    "title": "Does the Menu Set the Scale of Evaluation?",
    "author": "Andrew H. Bond, San Jose State University",
    "companion_to": ["prereg-strata-v1"],
    "frozen_predictions": "H1-H5 in prereg-menus-v1.md Section 5; void condition there.",
    "data": "Gluth, Spektor and Rieskamp 2018 (OSF 8r4fh); zip hashes in Section 2. No choice statistic "
            "computed before sealing (Section 9).",
    "hash_note": "sha256 of each file with CRLF normalized to LF; combined = sha256 over "
                 "the concatenated component hex digests in bundle_files order",
}


def digest(path: str) -> str:
    data = open(path, "rb").read().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def compute() -> dict:
    files = {f: digest(os.path.join(HERE, f)) for f in BUNDLE}
    combined = hashlib.sha256("".join(files[f] for f in BUNDLE).encode()).hexdigest()
    return {**META, "bundle_files": BUNDLE, "files": files, "combined_sha256": combined}


def main() -> None:
    cur = compute()
    if "--write" in sys.argv:
        with open(SEAL, "w", encoding="utf-8", newline="\n") as f:
            json.dump(cur, f, indent=2)
            f.write("\n")
        print("sealed", cur["combined_sha256"])
        return
    rec = json.load(open(SEAL, encoding="utf-8"))
    ok = True
    for f in BUNDLE:
        good = rec["files"].get(f) == cur["files"][f]
        ok &= good
        print(f"    {f:<40} {'ok' if good else 'CHANGED'}")
    print("  SEAL INTACT" if ok and rec["combined_sha256"] == cur["combined_sha256"] else "  SEAL BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
