#!/usr/bin/env python3
"""Hash the prereg-gbe-last-outcome-v1 bundle, in the format this repository already uses.

A file is in the bundle if changing it would change what the study concludes.

    python seal_gbe.py           # verify against the recorded seal
    python seal_gbe.py --write   # write it, on the owner's word only

The registration is sealed under the name without -DRAFT. Rename the draft
before writing the seal.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEAL = os.path.join(HERE, "prereg-gbe-last-outcome-v1.sha256")

BUNDLE = [
    "prereg-gbe-last-outcome-v1.md",         # the registration
    "split_gbe.py",                          # the split
    "analyze_last.py",                       # shared constants and the reading of plays
    "analyze_matched.py",                    # the matched comparison and its next-trial check
    "analyze_onesided.py",                   # the slopes on the size of the last gamble
    "grade_gbe.py",                          # every bar
    "DESIGN.md",                             # the split rule, fixed before the download
    "DEVELOPMENT.md",                        # what development found
    "results/split_counts.json",             # participants on each side
    "results/dev_matched.json",              # development results the bars were set on
    "results/dev_matched_lead.json",
    "results/dev_onesided.json",
    "results/dev_onesided_first.json",
]

META = {
    "prereg": "prereg-gbe-last-outcome-v1",
    "title": "What the last gamble does to the next choice, and whether the points held carry it",
    "author": "Andrew H. Bond, San Jose State University",
    "frozen_predictions": "H1-H6 and checks K1-K3 in prereg-gbe-last-outcome-v1.md Section 5; void "
                          "conditions in Section 8.",
    "data": "Dryad doi 10.5061/dryad.prr4xgxkk, archive sha256 "
            "456859176aece7ac40dc2303aec210490a90bb5d395f713ddf75ffb91fb82168. Held out: the 23,478 "
            "participants of DESIGN.md Section 4. Nothing of theirs but the count was read before sealing.",
    "hash_note": "sha256 of each file with CRLF normalized to LF; combined = sha256 over "
                 "the concatenated component hex digests in bundle_files order",
}


def digest(path):
    data = open(path, "rb").read().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def compute():
    files = {f: digest(os.path.join(HERE, f)) for f in BUNDLE}
    combined = hashlib.sha256("".join(files[f] for f in BUNDLE).encode()).hexdigest()
    return {**META, "bundle_files": BUNDLE, "files": files, "combined_sha256": combined}


def main():
    cur = compute()
    if "--write" in sys.argv:
        with open(SEAL, "w", encoding="utf-8", newline="\n") as f:
            json.dump(cur, f, indent=2)
            f.write("\n")
        print("wrote", SEAL, cur["combined_sha256"])
        return
    old = json.load(open(SEAL, encoding="utf-8"))
    bad = [f for f in BUNDLE if old["files"].get(f) != cur["files"][f]]
    if bad or old["combined_sha256"] != cur["combined_sha256"]:
        print("SEAL BROKEN:", bad)
        sys.exit(1)
    print("seal intact", cur["combined_sha256"])


if __name__ == "__main__":
    main()
