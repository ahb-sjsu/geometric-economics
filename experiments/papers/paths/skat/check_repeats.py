"""Are deals in the Skat development archive repeated with the seats turned?

    bzcat skatgame-games-2016-05-2026.bz2 | python check_repeats.py out.json

Written 2026-11-11 after the first rates by history gave non-zero differences
for the programs, which a fair independent deal and a memoryless program should
not. Programs are often tested by playing one deal several times with the hands
moved round the table. If the archive holds such games, a player's hand is tied
to the hands and results of the games before, and the randomness that the
design rests on fails for them.

For each game, the deal is reduced to the set of its three ten-card hands and
the skat, ignoring which seat held which. A game repeats if the same set was
seen earlier in the same series. Counts are split by how many of the three
seats are held by one of the four programs.
"""
import json
import re
import sys
from collections import Counter, defaultdict

FIELD = re.compile(r"(\w+)\[([^\]]*)\]")
PROGRAMS = {"xskat", "kermit", "zoot", "theCount"}


def main(out):
    seen = defaultdict(set)
    games, repeats, exact = Counter(), Counter(), Counter()
    for line in sys.stdin:
        f = dict(FIELD.findall(line))
        mv = f.get("MV", "").split()
        if len(mv) < 2:
            continue
        d = mv[1].split(".")
        if len(d) != 32:
            continue
        n = sum(f.get("P%d" % s, "").split(":")[0] in PROGRAMS for s in (0, 1, 2))
        key = frozenset((frozenset(d[0:10]), frozenset(d[10:20]), frozenset(d[20:30])))
        games[n] += 1
        s = seen[f.get("SE", "")]
        if key in s:
            repeats[n] += 1
        if mv[1] in s:
            exact[n] += 1
        s.add(key)
        s.add(mv[1])
    res = {"by_number_of_program_seats": {str(n): {"games": games[n], "same_hands_seen_earlier_in_series": repeats[n],
                                                    "identical_deal_string_seen_earlier_in_series": exact[n]}
                                          for n in sorted(games)}}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
