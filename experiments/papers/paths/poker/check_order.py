"""Do hand labels order play within a table? A check that reads no action.

    python check_order.py poker-hand-histories-v2.zip out.json [max_hands_per_site]

Reads four header lines of each hand (table, hand, players, starting_stacks) and
the blinds line for the size of the big blind. The actions line is never parsed
or kept. Because no decision is read, the check may be run on held-out sites
before the seal.

If labels order play, then a player seated in two consecutive hands at a table
mostly starts the second with nearly the stack they started the first with.
Between two hands of the same table taken at random that is much rarer. For
each site the share of seated-in-both players whose stack is unchanged, and the
share whose stack moved by under 1.5 big blinds, is given for consecutive labels
and for random pairs. Also the share of hands whose label holds no digits, which
the registration's rule V3 caps at 2%.
"""
import ast
import json
import re
import sys
import zipfile
from collections import defaultdict

import numpy as np

DIGITS = re.compile(r"\d+")
KEEP = ("blinds_or_straddles", "starting_stacks", "players", "table", "hand")
SEED = 20261111


def main(archive, out, cap=1000000):
    rng = np.random.default_rng(SEED)
    tables = defaultdict(lambda: defaultdict(dict))     # site -> (bb, table) -> label -> {player: stack in bb}
    seen = defaultdict(int)
    nodigit = defaultdict(int)
    with zipfile.ZipFile(archive) as z:
        names = sorted(n for n in z.namelist() if n.endswith(".phhs") and "/handhq/" in n)
        for name in names:
            site = name.split("/handhq/")[1].split("/")[0].split("-")[0]
            if seen[site] >= cap:
                continue
            h = {}
            with z.open(name) as g:
                for raw in g:
                    line = raw.decode("utf-8", "replace").rstrip("\n")
                    if line.startswith("[") or not line.strip():
                        if h:
                            add(h, site, tables, seen, nodigit)
                        h = {}
                        continue
                    key, _, val = line.partition(" = ")
                    if key in KEEP:
                        h[key] = val
                if h:
                    add(h, site, tables, seen, nodigit)
    res = {"max_hands_per_site": cap, "sites": {}}
    for site in sorted(tables):
        cons = [0, 0, 0]                                 # unchanged, within 1.5 bb, players
        rand = [0, 0, 0]
        for hands in tables[site].values():
            labels = sorted(hands)
            if len(labels) < 3:
                continue
            perm = rng.permutation(len(labels))
            for i in range(len(labels) - 1):
                tally(hands[labels[i]], hands[labels[i + 1]], cons)
                j = int(perm[i])
                if j != i:
                    tally(hands[labels[i]], hands[labels[j]], rand)
        res["sites"][site] = {
            "hands_read": seen[site],
            "share_of_labels_with_no_digits": nodigit[site] / max(1, seen[site]),
            "consecutive": {"players": cons[2], "unchanged": cons[0] / max(1, cons[2]),
                            "within_1.5_bb": cons[1] / max(1, cons[2])},
            "random_pair_same_table": {"players": rand[2], "unchanged": rand[0] / max(1, rand[2]),
                                       "within_1.5_bb": rand[1] / max(1, rand[2])}}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


def tally(a, b, t):
    for p, s in a.items():
        if p in b:
            d = abs(b[p] - s)
            t[0] += d < 1e-9
            t[1] += d < 1.5
            t[2] += 1


def add(h, site, tables, seen, nodigit):
    try:
        blinds = ast.literal_eval(h["blinds_or_straddles"])
        stacks = ast.literal_eval(h["starting_stacks"])
        players = ast.literal_eval(h["players"])
        table = ast.literal_eval(h["table"])
        bb = float(max(blinds))
        if bb <= 0 or len(stacks) != len(players):
            return
    except (KeyError, ValueError, SyntaxError):
        return
    seen[site] += 1
    label = tuple(int(x) for x in DIGITS.findall(h.get("hand", "")))
    if not label:
        nodigit[site] += 1
        return
    tables[site][(bb, table)][label] = {p: s / bb for p, s in zip(players, stacks)}


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1000000)
