#!/usr/bin/env python3
"""Hash the prereg-psych101-v1 bundle, in the format this repository already uses.

A file is in the bundle if changing it would change what the study concludes.

    python seal_psych101.py           # verify against the recorded seal
    python seal_psych101.py --write   # write it
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEAL = os.path.join(HERE, "prereg-psych101-v1.sha256")

BUNDLE = [
    "prereg-psych101-v1.md",  # the registration
    "inspect_stimuli.py",     # what was looked at, choices masked
    "overlap_stimuli.py",     # the CPC18 overlap key
    "build_rows.py",          # parser, press accounting, covariate/outcome split
    "freeze_cpc18.py",        # how the frozen parameters were made
    "frozen_cpc18.json",      # the frozen parameters
    "fit_psych101.py",        # split, transfer, native, bootstrap, angle
    "grade_psych101.py",      # every bar
    "../../datasets/fit_transfer.py",  # the models and fitter, imported
    "../../datasets/cpc18.py",         # the CPC18 loader and option statistics, imported
]

META = {
    "prereg": "prereg-psych101-v1",
    "title": "Part II's Risky-Choice Models, Frozen, on a Corpus They Have Not Seen",
    "author": "Andrew H. Bond, San Jose State University",
    "companion_to": ["prereg-learned-v1", "prereg-boundary-v1"],
    "frozen_predictions": "H1-H5 in prereg-psych101-v1.md Section 5; void conditions Section 6.",
    "data": "wulff2018description/exp1.csv in Psych-101. No choice statistic computed before freezing.",
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
        print(f"    {f:<34} {'ok' if good else 'CHANGED'}")
    print("  SEAL INTACT" if ok and rec["combined_sha256"] == cur["combined_sha256"] else "  SEAL BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
