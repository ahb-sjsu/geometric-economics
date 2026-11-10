"""One row per player per hand: the first decision before the flop, and the state it was made in.

    python mine_hands.py poker-hand-histories-v2.zip out.tsv.gz --sites ABS FTP ONG

Reads the PHH archive without extracting it. For each hand it reads the header
lines and the actions up to the first board card, and nothing after. It never
reads a held-out site unless --allow-heldout is given, and that flag is for the
sealed run only.

Columns, tab separated:
    site      folder prefix: ABS, FTP, ONG (development) or PS, IPN, PTY (held out)
    bb        the big blind in dollars
    table     table label
    hand      hand number as given by the site
    day       day of July 2009
    player    player label
    pos       place in the betting order: 0 small blind, 1 big blind, last = button
    n         players dealt in
    stack     the player's stack at the start of the hand, in big blinds
    faced     1 if a raise came before the player's first decision
    act       f fold, c call, r raise, x no decision (a big blind left unraised, or
              the hand ended before the player's turn)

A big blind who checks an unraised pot has made no choice and is written as x.
"""
import argparse
import ast
import gzip
import zipfile

DEV = {"ABS", "FTP", "ONG"}
HELD = {"PS", "IPN", "PTY"}


def first_actions(actions, n, blinds):
    """Each player's first voluntary decision before the flop, with whether a raise preceded it."""
    out = ["x"] * n
    faced = [0] * n
    raised = False
    for a in actions:
        p = a.split(" ")
        if p[0] == "d":
            if p[1] == "db":
                break
            continue
        i = int(p[0][1:]) - 1
        if not 0 <= i < n or out[i] != "x":
            if len(p) > 1 and p[1] == "cbr":
                raised = True
            continue
        kind = p[1]
        if kind == "f":
            out[i], faced[i] = "f", int(raised)
        elif kind == "cbr":
            out[i], faced[i] = "r", int(raised)
            raised = True
        elif kind == "cc":
            # a check by a player who has already posted the largest blind is not a choice
            if not raised and blinds[i] == max(blinds):
                continue
            out[i], faced[i] = "c", int(raised)
    return out, faced


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archive")
    ap.add_argument("out")
    ap.add_argument("--sites", nargs="+", required=True)
    ap.add_argument("--allow-heldout", action="store_true")
    ap.add_argument("--max-files", type=int, default=0)
    a = ap.parse_args()
    sites = set(a.sites)
    if sites & HELD and not a.allow_heldout:
        raise SystemExit("refusing held-out sites %s without --allow-heldout" % sorted(sites & HELD))
    if not sites <= DEV | HELD:
        raise SystemExit("unknown site in %s" % sorted(sites))
    counts = {"files": 0, "hands": 0, "rows": 0, "skipped": 0}
    with zipfile.ZipFile(a.archive) as z, gzip.open(a.out, "wt", compresslevel=4) as f:
        names = sorted(n for n in z.namelist() if n.endswith(".phhs") and "/handhq/" in n)
        for name in names:
            folder = name.split("/handhq/")[1].split("/")[0]
            site = folder.split("-")[0]
            if site not in sites:
                continue
            counts["files"] += 1
            if a.max_files and counts["files"] > a.max_files:
                break
            h = {}
            with z.open(name) as g:
                for raw in g:
                    line = raw.decode("utf-8", "replace").rstrip("\n")
                    if line.startswith("[") or not line.strip():
                        if h:
                            emit(h, site, f, counts)
                        h = {}
                        continue
                    key, _, val = line.partition(" = ")
                    if key in ("blinds_or_straddles", "starting_stacks", "actions", "players",
                               "table", "hand", "day"):
                        h[key] = val
                if h:
                    emit(h, site, f, counts)
            if counts["files"] % 500 == 0:
                print(counts, flush=True)
    print("DONE", counts, flush=True)


def emit(h, site, f, counts):
    try:
        blinds = ast.literal_eval(h["blinds_or_straddles"])
        stacks = ast.literal_eval(h["starting_stacks"])
        actions = ast.literal_eval(h["actions"])
        players = ast.literal_eval(h["players"])
        table = ast.literal_eval(h["table"])
        bb = float(max(blinds))
        n = len(players)
        if bb <= 0 or n < 2 or len(stacks) != n or len(blinds) != n:
            raise ValueError
    except (KeyError, ValueError, SyntaxError):
        counts["skipped"] += 1
        return
    acts, faced = first_actions(actions, n, blinds)
    counts["hands"] += 1
    for i in range(n):
        f.write("%s\t%g\t%s\t%s\t%s\t%s\t%d\t%d\t%.1f\t%d\t%s\n" % (
            site, bb, table, h.get("hand", ""), h.get("day", ""), players[i], i, n,
            stacks[i] / bb, faced[i], acts[i]))
    counts["rows"] += n


if __name__ == "__main__":
    main()
