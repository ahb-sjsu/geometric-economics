#!/usr/bin/env python3
"""Hash the prereg-poker-recency-v1 bundle, in the format this repository already uses.

A file is in the bundle if changing it would change what the study concludes.

    python seal_poker.py           # verify against the recorded seal
    python seal_poker.py --write   # write it
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEAL = os.path.join(HERE, "prereg-poker-recency-v1.sha256")

BUNDLE = [
    "prereg-poker-recency-v1.md",            # the registration
    "mine_hands.py",                         # mining, and the guard on held-out sites
    "analyze_lags.py",                       # shared constants and chain rules
    "analyze_recency.py",                    # the registered statistic
    "grade_recency.py",                      # every bar
    "DESIGN.md",                             # the split
    "DEVELOPMENT.md",                        # what development found
    "results/recency_dev_coarse.json",       # development result, registered specification
    "results/recency_dev_coarse_table.json",
    "results/recency_dev_bin10.json",
    "results/recency_dev_bin10_table.json",
]

META = {
    "prereg": "prereg-poker-recency-v1",
    "title": "Does a player raise less in the hand straight after a large pot?",
    "author": "Andrew H. Bond, San Jose State University",
    "frozen_predictions": "H1-H4 in prereg-poker-recency-v1.md Section 5; void conditions in Section 8.",
    "data": "PHH collection version 2, md5 0918a30f97bda0129897b7e0f1ec895a. Held out: PokerStars and "
            "PartyPoker. No action from either was read before sealing (Section 3).",
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
