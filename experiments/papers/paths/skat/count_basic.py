"""Pass 0 on the Skat development archive: what the records hold. No hypothesis is tested.

    bzcat skatgame-games-2016-05-2026.bz2 | python count_basic.py counts.json names_private.tsv

Reads only the development archive. Counts games, the span of dates, how often
the record parses, the middlehand's first bidding action (the token after the
deal in MV, which should be player 1 saying 18 or passing), the declarer, and
how many games each login played. The login counts go to the second file, which
stays on Atlas and is not committed, since logins may be people's names. The
JSON holds no login.
"""
import collections
import json
import re
import sys

FIELD = re.compile(r"(\w+)\[([^\]]*)\]")


def main(out, private):
    c = collections.Counter()
    first = collections.Counter()
    decl = collections.Counter()
    names = collections.Counter()
    years = collections.Counter()
    for line in sys.stdin:
        c["lines"] += 1
        f = dict(FIELD.findall(line))
        if not all(k in f for k in ("P0", "P1", "P2", "MV", "DT", "R")):
            c["missing_field"] += 1
            continue
        mv = f["MV"].split()
        if len(mv) < 4 or mv[0] != "w" or len(mv[1].split(".")) != 32:
            c["bad_deal"] += 1
            continue
        c["parsed"] += 1
        years[f["DT"][:4]] += 1
        first[mv[2] + " " + ("bid" if mv[3].isdigit() else mv[3])] += 1
        m = re.match(r"d:(-?\d+)", f["R"])
        decl[m.group(1) if m else "none"] += 1
        trio = [f["P0"], f["P1"], f["P2"]]
        for n in trio:
            names[n] += 1
        c["games_with_a_colon_login"] += any(":" in n for n in trio)
        c["games_all_three_distinct_base_logins"] += len({n.split(":")[0] for n in trio}) == 3
    res = {"counts": dict(c), "by_year": dict(sorted(years.items())),
           "first_action_after_deal": dict(first.most_common(12)),
           "declarer_field": dict(decl.most_common()), "distinct_logins": len(names),
           "logins_with_100_games_or_more": sum(v >= 100 for v in names.values()),
           "share_of_seats_held_by_top_20_logins": sum(v for _, v in names.most_common(20)) / max(1, sum(names.values()))}
    json.dump(res, open(out, "w"), indent=1)
    with open(private, "w") as g:
        for n, v in names.most_common(300):
            g.write("%s\t%d\n" % (n, v))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
