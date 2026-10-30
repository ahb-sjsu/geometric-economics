#!/usr/bin/env python3
"""Hash the prereg-learned-v1 bundle, in the format this repository already uses.

A file is in the bundle if changing it would change what the study concludes.

    python seal_learned.py           # verify against the recorded seal
    python seal_learned.py --write   # write it
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEAL = os.path.join(HERE, "prereg-learned-v1.sha256")

BUNDLE = [
    "prereg-learned-v1.md",   # the registration
    "build_inputs.py",        # how anchor and panel texts are built
    "inputs.json",            # the texts themselves
    "embed.py",               # the encoders and their snapshots
    "fit_learned.py",         # models, grid, selection, test, alignment, transfer
    "grade_learned.py",       # every bar
]

META = {
    "prereg": "prereg-learned-v1",
    "title": "Learned Coordinates for the Geometric Decision Model",
    "author": "Andrew H. Bond, San Jose State University",
    "companion_to": ["prereg-boundary-v1", "prereg-v1"],
    "frozen_predictions": "H1-H5 in prereg-learned-v1.md Section 6; void conditions Section 7.",
    "data": "Scruples Dilemmas v1.0. Annotation counts not scored before freezing. "
            "Embeddings computed before freezing to fix encoder snapshots.",
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
        print(f"    {f:<24} {'ok' if good else 'CHANGED'}")
    print("  SEAL INTACT" if ok and rec["combined_sha256"] == cur["combined_sha256"] else "  SEAL BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
