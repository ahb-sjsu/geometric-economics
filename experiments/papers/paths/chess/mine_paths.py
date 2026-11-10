"""Development pass over one Lichess month: positions with the move order that led to them.

Reads a decompressed PGN stream on stdin and writes one row per decision ply of a
hash-sampled subset of games. It fits nothing and runs no engine.

    zstd -dc lichess_db_standard_rated_2026-06.pgn.zst | python mine_paths.py --out rows.tsv.gz

A row is one decision: the position a player faced after `ply` half-moves, the
half-moves that produced it in the order they were played, and the move the
player then chose. Two rows with the same `zkey` and different `path` are the
same position reached by different move orders.

Columns, tab separated:
    gid     keyed digest of the game URL
    ply     half-moves played before this decision (even = White to move)
    zkey    Polyglot Zobrist key of the position (pieces, side, castling, en passant), hex
    path    the half-moves so far in SAN, space separated, checks stripped
    move    the half-move chosen, SAN, checks stripped
    mover   keyed digest of the mover's account name
    elo     mover's rating
    oelo    opponent's rating
    tc      time control as "base+increment" seconds
    clk     mover's clock in seconds before this move, or -1

Sampling is by a keyed hash of the game URL, so it does not follow the file's
chronological order. Account names never leave this process undigested. The
key is read from PATHS_PLAYER_KEY.
"""
import argparse
import gzip
import hashlib
import os
import re
import sys

import chess
import chess.polyglot

PLY_MIN, PLY_MAX = 6, 16          # decisions after 6 to 16 half-moves
TAG = re.compile(r'^\[(\w+) "(.*)"\]')
TOKEN = re.compile(r"\{([^}]*)\}|(\d+\.+)|(\S+)")
CLK = re.compile(r"\[%clk (\d+):(\d+):(\d+)\]")
RESULTS = {"1-0", "0-1", "1/2-1/2", "*"}


def digest(text, key, size=8):
    return hashlib.blake2b(text.encode("utf-8", "replace"), key=key, digest_size=size).hexdigest()


def games(stream):
    """Yield (tags, movetext) for each game in a PGN stream."""
    tags, lines, in_moves = {}, [], False
    for line in stream:
        if line.startswith("["):
            if in_moves:
                yield tags, " ".join(lines)
                tags, lines, in_moves = {}, [], False
            m = TAG.match(line)
            if m:
                tags[m.group(1)] = m.group(2)
        elif line.strip():
            in_moves = True
            lines.append(line.strip())
    if in_moves:
        yield tags, " ".join(lines)


def plies(movetext, limit):
    """The first `limit` half-moves as (san, clock_after_move_or_None)."""
    out = []
    for comment, number, word in TOKEN.findall(movetext):
        if comment:
            if out and out[-1][1] is None:
                m = CLK.search(comment)
                if m:
                    out[-1] = (out[-1][0], int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3)))
        elif word:
            if word in RESULTS:
                break
            if len(out) >= limit:
                break
            out.append((word.rstrip("+#!?"), None))
    return out


def rows_for(tags, movetext, key):
    try:
        elo = (int(tags["WhiteElo"]), int(tags["BlackElo"]))
    except (KeyError, ValueError):
        return "rating", []
    if tags.get("WhiteTitle") == "BOT" or tags.get("BlackTitle") == "BOT":
        return "bot", []
    tc = tags.get("TimeControl", "")
    if "+" not in tc:
        return "timecontrol", []
    seq = plies(movetext, PLY_MAX + 1)
    if len(seq) <= PLY_MIN:
        return "short", []
    gid = digest(tags.get("Site", ""), key)
    who = (digest(tags.get("White", ""), key), digest(tags.get("Black", ""), key))
    board = chess.Board()
    out = []
    for ply, (san, _) in enumerate(seq):
        if ply >= PLY_MIN:
            side = ply % 2
            clk = seq[ply - 2][1] if ply >= 2 else None
            out.append("\t".join((
                gid, str(ply), "%016x" % chess.polyglot.zobrist_hash(board),
                " ".join(s for s, _ in seq[:ply]), san, who[side],
                str(elo[side]), str(elo[1 - side]), tc, str(-1 if clk is None else clk))))
        try:
            board.push_san(san)
        except ValueError:
            return "illegal", []
    return "ok", out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--rate", type=float, default=0.04, help="share of games sampled")
    ap.add_argument("--max-games", type=int, default=0, help="stop after this many games read (0 = all)")
    a = ap.parse_args()
    key = os.environ.get("PATHS_PLAYER_KEY", "").encode()
    if len(key) < 16:
        raise SystemExit("PATHS_PLAYER_KEY must be set (16 characters or more)")
    cut = int(a.rate * 2 ** 32)
    counts = {"read": 0, "sampled": 0, "rows": 0}
    with gzip.open(a.out, "wt", compresslevel=4) as f:
        for tags, movetext in games(sys.stdin):
            counts["read"] += 1
            if a.max_games and counts["read"] > a.max_games:
                break
            h = hashlib.blake2b(tags.get("Site", "").encode(), key=key, digest_size=4).digest()
            if int.from_bytes(h, "big") >= cut:
                continue
            counts["sampled"] += 1
            why, rows = rows_for(tags, movetext, key)
            counts[why] = counts.get(why, 0) + 1
            if rows:
                counts["rows"] += len(rows)
                f.write("\n".join(rows) + "\n")
            if counts["sampled"] % 100000 == 0:
                print(counts, flush=True)
    print("DONE", counts, flush=True)


if __name__ == "__main__":
    main()
