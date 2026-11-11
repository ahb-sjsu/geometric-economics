#!/usr/bin/env python3
"""Hash the prereg-chess-memory-v1 bundle, in the format this repository already uses.

A file is in the bundle if changing it would change what the study concludes.

    python seal_chess.py           # verify against the recorded seal
    python seal_chess.py --write   # write it
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEAL = os.path.join(HERE, "prereg-chess-memory-v1.sha256")

BUNDLE = [
    "prereg-chess-memory-v1.md",             # the registration
    "mine_paths.py",                         # game reader, digests
    "mine_targets.py",                       # the registered miner
    "analyze_paths.py",                      # speed categories
    "analyze_memory.py",                     # the registered statistic, H1 to H4
    "grade_memory.py",                       # the bars of H1 to H4
    "results/targets.tsv",                   # the positions and move orders
    "DEVELOPMENT.md",                        # what development found
    "results/memory_reg_2026-07.json",       # development results the bands come from
    "results/memory_reg_2026-08.json",
    "mine_movetime.py",                      # second pass: the miner plus the clock after the move
    "analyze_pull.py",                       # the pull, shared rules
    "analyze_pull_time.py",                  # the pull by time spent, H5
    "analyze_memory_time.py",                # the curve by time spent, reported without a bar
    "grade_pull.py",                         # the bar of H5
    "results/pull_time_2026-08.json",        # development result H5 comes from
]

META = {
    "prereg": "prereg-chess-memory-v1",
    "title": "How far back does history reach in a chess player's choice of move?",
    "author": "Andrew H. Bond, San Jose State University",
    "frozen_predictions": "H1-H5 in prereg-chess-memory-v1.md Section 5; void conditions in Section 8.",
    "data": "Lichess rated games, October 2026, sha256 "
            "043906ebfade1bfeb7c00087590fac505370936c028525e4722e2dbd4986ae86. Not decompressed before sealing.",
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
