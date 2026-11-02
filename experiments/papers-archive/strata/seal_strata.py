#!/usr/bin/env python3
"""Hash the prereg-strata-v1 bundle, in the format this repository already uses.

A file is in the bundle if changing it would change what the study concludes.

    python seal_strata.py           # verify against the recorded seal
    python seal_strata.py --write   # write it
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEAL = os.path.join(HERE, "prereg-strata-v1.sha256")

BUNDLE = [
    "prereg-strata-v1.md",             # the registration
    "fetch_corpora.py",                # where the corpora came from
    "corpora.py",                      # parsers, exclusion rules, accounting
    "stimuli_check.py",                # de-duplication and environment checks, stimuli only
    "accounting.json",                 # row accounting per corpus
    "stimuli_check.json",              # overlap and probability environments, stimuli only
    "strata_models.py",                # every model
    "fit_strata.py",                   # freezing, recovery, transfer, pooling, effects
    "frozen_strata.json",              # the frozen parameters
    "recovery_v4.json",                # the V4 identification check
    "grade_strata.py",                 # every bar
    "../../datasets/cpc18_raw_sha256.txt",  # the CPC18 file the freeze used
]

META = {
    "prereg": "prereg-strata-v1",
    "title": "Refusing the Early Projection: A Stratified Encoding of Lotteries",
    "author": "Andrew H. Bond, San Jose State University",
    "companion_to": ["prereg-psych101-v1", "prereg-learned-v1"],
    "frozen_predictions": "H1-H8 in prereg-strata-v1.md Section 6; void conditions Section 8.",
    "data": "Five public corpora (Appendix A). No choice statistic of any test corpus computed before freezing.",
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
