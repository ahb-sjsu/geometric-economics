"""Development: do the ten busiest logins that are not known programs look like people?

    python check_busiest.py dev_rows.tsv.gz out.json

The lag result of pass 3 changes when the ten logins with the most middlehand
decisions are left out. This file describes them beside the four known programs
and beside the other busy logins (1,000 decisions or more). No login or digest
is written, only ranks.

For each login, from the games in which it sat middlehand and bid or passed:

    decisions            how many
    days                 distinct dates on which it played
    busiest_day          most decisions on one date
    hours_covered        how many of the 24 hours of the day hold at least 1% of its decisions
    longest_run_hours    longest stretch with no pause of 30 minutes or more between its decisions
    bid_rate
    nearest_program      the known program whose rate of bidding by hand cell is closest,
    distance             and the root mean square difference over hand cells, weighted by the
                         login's own counts

A person sleeps, so few hours covered, short runs and a day's count a person
could play are the signs looked for. A program can run all day.
"""
import gzip
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime

import numpy as np

PROGRAMS = ("xskat", "kermit", "zoot", "theCount")


def main(rows, out):
    times = defaultdict(list)
    cells = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    with gzip.open(rows, "rt") as f:
        for line in f:
            r = line.rstrip("\n").split("\t")
            if r[27] not in "bp":
                continue
            who = r[11]
            if who not in PROGRAMS and r[12] != "0":
                continue
            jacks = 0 if r[14] == "-" else len(r[14])
            high = min((int(r[15]) + int(r[16])) // 2, 2)
            c = cells[who][(jacks, high)]
            c[0] += r[27] == "b"
            c[1] += 1
            try:
                times[who].append(datetime.strptime(r[2], "%Y-%m-%d/%H:%M:%S/UTC"))
            except ValueError:
                pass
    prog_rate = {p: {k: v[0] / v[1] for k, v in cells[p].items()} for p in PROGRAMS}

    def describe(who):
        ts = sorted(times[who])
        n = sum(v[1] for v in cells[who].values())
        d = {"decisions": n, "bid_rate": sum(v[0] for v in cells[who].values()) / n}
        if ts:
            days = Counter(t.date() for t in ts)
            hours = Counter(t.hour for t in ts)
            run = best = 0.0
            for a, b in zip(ts, ts[1:]):
                gap = (b - a).total_seconds()
                run = run + gap if gap < 1800 else 0.0
                best = max(best, run)
            d.update({"days": len(days), "busiest_day": max(days.values()),
                      "hours_covered": sum(1 for h in range(24) if hours[h] >= 0.01 * len(ts)),
                      "longest_run_hours": best / 3600})
        best = None
        for p in PROGRAMS:
            if p == who:
                continue
            num = den = 0.0
            for k, v in cells[who].items():
                if k in prog_rate[p]:
                    num += v[1] * (v[0] / v[1] - prog_rate[p][k]) ** 2
                    den += v[1]
            dist = (num / den) ** 0.5
            if best is None or dist < best[1]:
                best = (p, dist)
        d["nearest_program"], d["distance"] = best
        return d

    people = sorted((w for w in cells if w not in PROGRAMS), key=lambda w: -sum(v[1] for v in cells[w].values()))
    res = {"programs": {p: describe(p) for p in PROGRAMS},
           "ten_busiest": [describe(w) for w in people[:10]]}
    rest = [describe(w) for w in people[10:] if sum(v[1] for v in cells[w].values()) >= 1000]
    res["other_logins_with_1000_or_more"] = {"n": len(rest)}
    for k in ("decisions", "days", "busiest_day", "hours_covered", "longest_run_hours", "bid_rate", "distance"):
        v = np.array([d[k] for d in rest if k in d])
        res["other_logins_with_1000_or_more"][k] = {q: float(np.percentile(v, p)) for q, p in
                                                    (("p10", 10), ("median", 50), ("p90", 90), ("max", 100))}
    json.dump(res, open(out, "w"), indent=1)
    fmt = "%-10s dec %7d days %4d busiest %5d hours %2d run %5.1f bid %.3f near %-8s %.3f"
    row = lambda name, d: print(fmt % (name, d["decisions"], d.get("days", 0), d.get("busiest_day", 0),
                                       d.get("hours_covered", 0), d.get("longest_run_hours", 0), d["bid_rate"],
                                       d["nearest_program"], d["distance"]))
    for p in PROGRAMS:
        row(p, res["programs"][p])
    for i, d in enumerate(res["ten_busiest"]):
        row("rank %d" % (i + 1), d)
    print(json.dumps(res["other_logins_with_1000_or_more"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
