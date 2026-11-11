"""Every game of a month that reaches a listed position by a listed move order.

    zstd -dc month.pgn.zst | python mine_targets.py --targets targets.tsv --out rows.tsv.gz

No sampling and no chess library. A game is matched by the text of its first
half-moves against the orders written by make_targets.py. Output columns are
those of mine_paths.py, with the position key taken from the target list, plus
two final columns: the game's UTC date and time, so that one player's games can
be put in order, and Lichess's engine evaluation after the chosen move where the
game carries one (empty otherwise). The evaluation column was added on
2026-11-10 after the July pass had started, so July's rows lack it. A last
column, the keyed digest of the opponent's account, was added later the same
day and is in neither development month's rows.

This copy, mine_movetime.py, adds one more final column: the mover's clock after
the chosen move (-1 if absent), so that the time spent on the move can be
computed from column 10 and the increment. It exists so that the registered
miner, mine_targets.py, stays byte for byte as committed.
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
            sans = [s for s, _, _ in seq]
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
                    tags.get("UTCDate", "") + " " + tags.get("UTCTime", ""),
                    seq[ply][2] or "",
                    digest(tags.get("Black" if side == 0 else "White", ""), key),
                    str(-1 if seq[ply][1] is None else seq[ply][1]))) + "\n")
                counts["rows"] += 1
            if counts["read"] % 5000000 == 0:
                print(counts, flush=True)
    print("DONE", counts, flush=True)


if __name__ == "__main__":
    main()
