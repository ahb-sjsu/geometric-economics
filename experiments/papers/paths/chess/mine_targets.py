"""Every game of a month that reaches a listed position by a listed move order.

    zstd -dc month.pgn.zst | python mine_targets.py --targets targets.tsv --out rows.tsv.gz

No sampling and no chess library. A game is matched by the text of its first
half-moves against the orders written by make_targets.py. Output columns are
those of mine_paths.py, with the position key taken from the target list, plus
a final column: the game's UTC date and time, so that one player's games can be
put in order.
"""
import argparse
import gzip
import hashlib
import os
import sys

from mine_paths import digest, games, plies


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-games", type=int, default=0)
    a = ap.parse_args()
    key = os.environ.get("PATHS_PLAYER_KEY", "").encode()
    if len(key) < 16:
        raise SystemExit("PATHS_PLAYER_KEY must be set (16 characters or more)")
    target = {}
    for line in open(a.targets):
        ply, zkey, path, _ = line.rstrip("\n").split("\t")
        target.setdefault(int(ply), {})[path] = zkey
    wanted = sorted(target)
    top = max(wanted)
    counts = {"read": 0, "rows": 0}
    with gzip.open(a.out, "wt", compresslevel=4) as f:
        for tags, movetext in games(sys.stdin):
            counts["read"] += 1
            if a.max_games and counts["read"] > a.max_games:
                break
            seq = plies(movetext[:900], top + 1)
            if len(seq) <= wanted[0]:
                continue
            sans = [s for s, _ in seq]
            for ply in wanted:
                if len(seq) <= ply:
                    break
                path = " ".join(sans[:ply])
                zkey = target[ply].get(path)
                if zkey is None:
                    continue
                if tags.get("WhiteTitle") == "BOT" or tags.get("BlackTitle") == "BOT":
                    break
                try:
                    elo = (int(tags["WhiteElo"]), int(tags["BlackElo"]))
                except (KeyError, ValueError):
                    break
                side = ply % 2
                clk = seq[ply - 2][1]
                f.write("\t".join((
                    digest(tags.get("Site", ""), key), str(ply), zkey, path, sans[ply],
                    digest(tags.get("White" if side == 0 else "Black", ""), key),
                    str(elo[side]), str(elo[1 - side]), tags.get("TimeControl", ""),
                    str(-1 if clk is None else clk),
                    tags.get("UTCDate", "") + " " + tags.get("UTCTime", ""))) + "\n")
                counts["rows"] += 1
            if counts["read"] % 5000000 == 0:
                print(counts, flush=True)
    print("DONE", counts, flush=True)


if __name__ == "__main__":
    main()
