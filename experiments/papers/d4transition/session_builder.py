#!/usr/bin/env python3
"""Build participant sessions, and verify every constraint the protocol states.

`PILOT.md` Sections 4 and 5 impose an assignment and a randomisation scheme. A
scheme that is described and not checked is a scheme that drifts, so each
requirement here is a function that can fail, and the self-test runs them against
deliberately broken schedules.

WHAT THE PROTOCOL REQUIRES

    30 families, 60 participants, 3 families each, 6 participants per family
    18 cells per participant, being 3 families times 3 pairs times 2 directions
    direction order randomised within participant and counterbalanced across them
    the two directions of a pair separated by at least four intervening cells
    pair order randomised within family, family order randomised within participant

HOW THE SEPARATION IS GUARANTEED RATHER THAN HOPED FOR

Each participant sees nine pairs. The first direction of every pair is placed in
the first nine positions in a random order, and the second direction of every
pair in the last nine, in an order drawn subject to the separation holding. Since
the halves are nine apart, a separation of five is easy to satisfy and the draw
is checked rather than assumed.

**Counterbalancing is deterministic, not random.** Each family is seen by exactly
six participants, so three get the forward direction first and three get the
backward direction first, by position in that family's list. A coin flip would
leave the balance to chance at a sample this small.

    python session_builder.py            # self-test only
    python session_builder.py --write    # write sessions.json
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

N_FAMILIES = 30
N_PARTICIPANTS = 60
FAMILIES_PER_PARTICIPANT = 3
PARTICIPANTS_PER_FAMILY = 6
PAIRS = ("CROSS", "CTRL_G", "CTRL_M")
DIRECTIONS = ("forward", "backward")
MIN_SEPARATION = 5          # at least four intervening cells
SEED = 20260913

# multiples of the family spread, adopted in PILOT.md Section 3
PRICE_ROWS = (-3.0, -2.1, -1.5, -0.9, -0.45, 0.0, 0.45, 0.9, 1.5, 2.1, 3.0)


def select_families(stimuli, n=N_FAMILIES):
    """Span the shape grid rather than taking a corner of it.

    Families are grouped by shape and one is taken from each shape in turn,
    cycling, so the selection spreads over shapes first and scales second. The
    rule is deterministic and recorded, which `PILOT.md` Section 4 requires.
    """
    fams = stimuli["families"]
    by_shape = {}
    for f in fams:
        by_shape.setdefault((f["p_star"], f["d"]), []).append(f)
    for k in by_shape:
        by_shape[k].sort(key=lambda f: f["sigma"])
    shapes = sorted(by_shape)
    out, i = [], 0
    while len(out) < n:
        progressed = False
        for sh in shapes:
            if i < len(by_shape[sh]):
                out.append(by_shape[sh][i])
                progressed = True
                if len(out) == n:
                    break
        if not progressed:
            raise AssertionError("only %d families available, need %d"
                                 % (len(out), n))
        i += 1
    return out


def assign_families(rng, n_part=N_PARTICIPANTS, n_fam=N_FAMILIES):
    """Each participant gets three families, each family six participants."""
    slots = np.repeat(np.arange(n_fam), PARTICIPANTS_PER_FAMILY)
    for _ in range(2000):
        perm = rng.permutation(slots).reshape(n_part, FAMILIES_PER_PARTICIPANT)
        if all(len(set(row.tolist())) == FAMILIES_PER_PARTICIPANT for row in perm):
            return perm
    raise AssertionError("could not assign families without repeats")


def order_cells(rng, pair_keys, first_dirs):
    """Positions for eighteen cells with the separation guaranteed.

    `pair_keys` is the nine (family, pair) keys. `first_dirs` says which
    direction leads for each. Returns a list of (family, pair, direction).
    """
    n = len(pair_keys)
    first_order = rng.permutation(n)
    for _ in range(500):
        second_order = rng.permutation(n)
        pos1 = {int(p): i for i, p in enumerate(first_order)}
        pos2 = {int(p): n + i for i, p in enumerate(second_order)}
        if all(pos2[p] - pos1[p] >= MIN_SEPARATION for p in pos1):
            cells = [None] * (2 * n)
            for p in range(n):
                fam, pair = pair_keys[p]
                d1 = first_dirs[p]
                d2 = DIRECTIONS[1 - DIRECTIONS.index(d1)]
                cells[pos1[p]] = (fam, pair, d1)
                cells[pos2[p]] = (fam, pair, d2)
            return cells
    raise AssertionError("could not order cells with the required separation")


def build_sessions(stimuli, seed=SEED):
    rng = np.random.default_rng(seed)
    fams = select_families(stimuli)
    assign = assign_families(rng)
    # how many participants have already taken each family, for counterbalancing
    seen = {i: 0 for i in range(len(fams))}
    sessions = []
    for pi in range(N_PARTICIPANTS):
        keys, firsts = [], []
        for fi in assign[pi]:
            fi = int(fi)
            k = seen[fi]
            seen[fi] += 1
            for pair in PAIRS:
                keys.append((fams[fi]["name"], pair))
                # deterministic counterbalance, three of six each way
                firsts.append(DIRECTIONS[k % 2])
        cells = order_cells(rng, keys, firsts)
        trials = []
        for (fam_name, pair, direction) in cells:
            fam = next(f for f in fams if f["name"] == fam_name)
            a, b = fam["pairs"][pair]
            frm, to = (a, b) if direction == "forward" else (b, a)
            trials.append({
                "family": fam_name, "pair": pair, "direction": direction,
                "from": fam["states"][frm], "to": fam["states"][to],
                "from_label": frm, "to_label": to,
                "prices": [round(x * fam["sigma"], 2) for x in PRICE_ROWS],
                "price_multiples": list(PRICE_ROWS),
                "sigma": fam["sigma"],
            })
        sessions.append({"participant": "p%03d" % pi, "trials": trials})
    return fams, sessions


# ----------------------------------------------------------------------------
# the checks, each able to fail
# ----------------------------------------------------------------------------
def check_sessions(fams, sessions):
    fails = []

    if len(sessions) != N_PARTICIPANTS:
        fails.append("participants %d, expected %d" % (len(sessions), N_PARTICIPANTS))

    counts = {}
    for s in sessions:
        if len(s["trials"]) != 18:
            fails.append("%s has %d cells, expected 18" % (s["participant"], len(s["trials"])))
        seen_fams = {t["family"] for t in s["trials"]}
        if len(seen_fams) != FAMILIES_PER_PARTICIPANT:
            fails.append("%s sees %d families, expected %d"
                         % (s["participant"], len(seen_fams), FAMILIES_PER_PARTICIPANT))
        for f in seen_fams:
            counts[f] = counts.get(f, 0) + 1
        # every family gets all three pairs in both directions
        got = {(t["family"], t["pair"], t["direction"]) for t in s["trials"]}
        for f in seen_fams:
            for pr in PAIRS:
                for d in DIRECTIONS:
                    if (f, pr, d) not in got:
                        fails.append("%s missing %s %s %s" % (s["participant"], f, pr, d))
        # separation
        pos = {}
        for i, t in enumerate(s["trials"]):
            pos.setdefault((t["family"], t["pair"]), []).append(i)
        for k, v in pos.items():
            if len(v) != 2:
                fails.append("%s has %d cells for %s" % (s["participant"], len(v), k))
            elif abs(v[1] - v[0]) < MIN_SEPARATION:
                fails.append("%s separation %d for %s, below %d"
                             % (s["participant"], abs(v[1] - v[0]), k, MIN_SEPARATION))

    for f, c in counts.items():
        if c != PARTICIPANTS_PER_FAMILY:
            fails.append("family %s seen by %d participants, expected %d"
                         % (f, c, PARTICIPANTS_PER_FAMILY))

    # counterbalance, by family and pair
    lead = {}
    for s in sessions:
        first_seen = {}
        for t in s["trials"]:
            k = (t["family"], t["pair"])
            if k not in first_seen:
                first_seen[k] = t["direction"]
        for k, d in first_seen.items():
            lead.setdefault(k, []).append(d)
    for k, ds in lead.items():
        fwd = sum(1 for d in ds if d == "forward")
        if abs(fwd - len(ds) / 2) > 0.5:
            fails.append("counterbalance for %s is %d forward of %d" % (k, fwd, len(ds)))

    # prices must be the adopted range, scaled by the family spread
    for s in sessions:
        for t in s["trials"]:
            if list(t["price_multiples"]) != list(PRICE_ROWS):
                fails.append("%s uses price multiples that are not the adopted set"
                             % s["participant"])
                break
    return fails


def self_test():
    print("SELF-TEST, the checks must reject broken schedules")
    with open(os.path.join(HERE, "stimuli.json"), encoding="utf-8") as fh:
        stim = json.load(fh)
    fams, sessions = build_sessions(stim)
    ok = True
    f = check_sessions(fams, sessions)
    if f:
        print("  FAIL, a valid schedule was rejected:")
        for x in f[:5]:
            print("    " + x)
        ok = False
    else:
        print("  a valid schedule passes")

    import copy
    cases = [
        ("two directions placed adjacent",
         lambda ss: ss[0]["trials"].insert(1, ss[0]["trials"].pop(9)),
         "separation"),
        ("a cell dropped",
         lambda ss: ss[0]["trials"].pop(3), "expected 18"),
        ("a family given to too many participants",
         lambda ss: [t.update({"family": ss[0]["trials"][0]["family"]})
                     for t in ss[5]["trials"]], "seen by"),
        ("counterbalance broken",
         lambda ss: [s["trials"].sort(key=lambda t: t["direction"] != "forward")
                     for s in ss], "counterbalance"),
    ]
    for label, break_it, expect in cases:
        ss = copy.deepcopy(sessions)
        break_it(ss)
        f = check_sessions(fams, ss)
        hit = any(expect in x for x in f)
        print("  %-38s -> %s" % (label, "rejected" if hit else "NOT REJECTED"))
        if not hit:
            print("       expected %r, got %s" % (expect, f[:3]))
            ok = False
    print("  SELF-TEST %s" % ("PASSED" if ok else "FAILED"))
    return ok, fams, sessions


def main():
    ok, fams, sessions = self_test()
    if not ok:
        return 1
    print()
    print("  %d families selected over %d shapes"
          % (len(fams), len({(f["p_star"], f["d"]) for f in fams})))
    print("  %d participants, %d cells each, %d price rows per cell"
          % (len(sessions), len(sessions[0]["trials"]), len(PRICE_ROWS)))
    print("  %d binary responses per participant"
          % (len(sessions[0]["trials"]) * len(PRICE_ROWS)))
    seps = []
    for s in sessions:
        pos = {}
        for i, t in enumerate(s["trials"]):
            pos.setdefault((t["family"], t["pair"]), []).append(i)
        seps += [abs(v[1] - v[0]) for v in pos.values()]
    print("  direction separation: min %d, median %d, max %d"
          % (min(seps), int(np.median(seps)), max(seps)))

    t = sessions[0]["trials"][0]
    print()
    print("  example cell for %s" % sessions[0]["participant"])
    print("    family %s, pair %s, direction %s" % (t["family"], t["pair"], t["direction"]))
    print("    from %s  H %.2f  p %.3f  L %.2f"
          % (t["from_label"], t["from"]["H"], t["from"]["p"], t["from"]["L"]))
    print("    to   %s  H %.2f  p %.3f  L %.2f"
          % (t["to_label"], t["to"]["H"], t["to"]["p"], t["to"]["L"]))
    print("    prices %s" % ", ".join("%+.2f" % x for x in t["prices"]))

    if "--html" in sys.argv:
        tmpl_path = os.path.join(HERE, "task_template.html")
        with open(tmpl_path, encoding="utf-8") as fh:
            tmpl = fh.read()
        marker = "/*__SESSION__*/ null"
        assert tmpl.count(marker) == 1, "template marker missing"
        outdir = os.path.join(HERE, "task")
        os.makedirs(outdir, exist_ok=True)
        for s2 in sessions:
            html = tmpl.replace(marker, json.dumps(s2))
            with open(os.path.join(outdir, "%s.html" % s2["participant"]), "w",
                      encoding="utf-8") as fh:
                fh.write(html)
        print()
        print("  written task/%s.html through task/%s.html, self-contained,"
              % (sessions[0]["participant"], sessions[-1]["participant"]))
        print("  no server needed, each opens by double-clicking")

    if "--write" in sys.argv:
        out = {"note": "pilot sessions, generated by session_builder.py",
               "seed": SEED, "price_multiples": list(PRICE_ROWS),
               "families": fams, "sessions": sessions}
        with open(os.path.join(HERE, "sessions.json"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=1)
        print()
        print("  written sessions.json")
    else:
        print()
        print("  pass --write to emit sessions.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
