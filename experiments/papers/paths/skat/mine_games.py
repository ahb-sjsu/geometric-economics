"""One row per Skat game: who sat where, what each held, how the bidding opened, how it ended.

    bzcat skatgame-games-2016-05-2026.bz2 | python mine_games.py rows.tsv.gz

Development archive only. The held-out archive is not to be passed to this
script before a seal.

A login is written as a keyed digest (PATHS_PLAYER_KEY, as in chess), except the
four program names, which are written as they are since they are not people.
A login with a ":n" suffix is a further connection of the same login. The digest
is of the login without the suffix, and the suffix is kept in its own column.

Columns, tab separated:
    id, series, time
    then for each seat 0 (forehand), 1 (middlehand), 2 (rearhand):
        who       digest or program name
        suffix    the ":n" suffix, or 0
        rating    as given
        jacks     the suits of the jacks held, from CSHD, or "-"
        aces      number of aces held
        tens      number of tens held
        longest   most cards held in one suit, jacks not counted
        maxbid    highest value the seat said or held, 0 if it passed at once or never spoke
    mid_first     b if middlehand's first action was a bid, p if a pass, x if the game ended first
    declarer      seat, or -1
    game          the declared game type, or "-"
    result        win, loss, passed or other
    value         the v: field of the result, or 0
    bad_cards     cards played by a seat that held neither that card nor, as declarer, the skat

The last column tests the reading that the first ten cards of the deal are
seat 0's, the next ten seat 1's, the next ten seat 2's and the last two the skat.
"""
import gzip
import hashlib
import os
import re
import sys

FIELD = re.compile(r"(\w+)\[([^\]]*)\]")
CARD = re.compile(r"^[CSHD][789TJQKA]$")
PROGRAMS = {"xskat", "kermit", "zoot", "theCount"}


def digest(text, key, size=8):
    return hashlib.blake2b(text.encode("utf-8", "replace"), key=key, digest_size=size).hexdigest()


def hand_columns(cards):
    jacks = "".join(s for s in "CSHD" if s + "J" in cards) or "-"
    plain = [c for c in cards if c[1] != "J"]
    longest = max((sum(c[0] == s for c in plain) for s in "CSHD"), default=0)
    return [jacks, str(sum(c[1] == "A" for c in cards)), str(sum(c[1] == "T" for c in cards)), str(longest)]


def main(out):
    key = os.environ.get("PATHS_PLAYER_KEY", "").encode()
    if len(key) < 16:
        raise SystemExit("PATHS_PLAYER_KEY must be set (16 characters or more)")
    counts = {"lines": 0, "rows": 0, "skipped": 0, "games_with_bad_cards": 0}
    with gzip.open(out, "wt", compresslevel=4) as g:
        for line in sys.stdin:
            counts["lines"] += 1
            f = dict(FIELD.findall(line))
            mv = f.get("MV", "").split()
            if not all(k in f for k in ("P0", "P1", "P2", "DT", "R", "ID")) or len(mv) < 2 or mv[0] != "w":
                counts["skipped"] += 1
                continue
            deal = mv[1].split(".")
            if len(deal) != 32 or not all(CARD.match(c) for c in deal):
                counts["skipped"] += 1
                continue
            hands = [set(deal[0:10]), set(deal[10:20]), set(deal[20:30])]
            skat = set(deal[30:32])
            maxbid = [0, 0, 0]
            current = 0
            mid_first, game, declared, bad = "x", "-", -1, 0
            rest = mv[2:]
            for i in range(0, len(rest) - 1, 2):
                who, what = rest[i], rest[i + 1]
                if who not in "012":
                    continue
                p = int(who)
                if declared < 0:
                    if what.isdigit():
                        current = int(what)
                        maxbid[p] = current
                        if p == 1 and mid_first == "x":
                            mid_first = "b"
                    elif what == "y":
                        maxbid[p] = current
                    elif what == "p":
                        if p == 1 and mid_first == "x":
                            mid_first = "p"
                    elif what != "s":
                        declared, game = p, what.split(".")[0]
                elif CARD.match(what):
                    if what not in hands[p] and not (p == declared and what in skat):
                        bad += 1
            res = f["R"]
            m = re.match(r"d:(-?\d+)", res)
            v = re.search(r"\bv:(-?\d+)", res)
            kind = "passed" if res.startswith("passed") else "win" if " win " in res + " " else "loss" if " loss " in res + " " else "other"
            row = [f["ID"], f.get("SE", ""), f["DT"]]
            for s in (0, 1, 2):
                name = f["P%d" % s]
                base, _, suf = name.partition(":")
                row += [base if base in PROGRAMS else digest(base, key), suf or "0", f.get("R%d" % s, "")]
                row += hand_columns(hands[s]) + [str(maxbid[s])]
            row += [mid_first, m.group(1) if m else "-1", game, kind, v.group(1) if v else "0", str(bad)]
            g.write("\t".join(row) + "\n")
            counts["rows"] += 1
            counts["games_with_bad_cards"] += bad > 0
    print("DONE", counts, flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
