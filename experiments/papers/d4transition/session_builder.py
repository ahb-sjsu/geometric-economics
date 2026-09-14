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

BOTH ARMS, ONE BUILDER

Arm A offers gambles and arm B offers permission states. Everything the protocol
requires is the same in both, so the schedule, the counterbalancing, the
separation and the checks are shared and only four things differ: which stimulus
file is read, how families are spread over the grid, what a cell shows, and where
the price rows sit.

**The price rule is one rule.** A row is the value difference plus a multiple of
a unit. Arm A matches expected value and spread, so its value difference is zero
and the rows sit either side of it. Arm B's pairs are all worth `v`, so its rows
sit either side of `+v` going forward and `-v` going back. The value difference
cancels out of the estimand, which is a difference of direction differences over
three pairs that share it.

    python session_builder.py                 # self-test, both arms
    python session_builder.py --arm B --write --html
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
DIRECTIONS = ("forward", "backward")
MIN_SEPARATION = 5          # at least four intervening cells
SEED = 20260913

# Money is delivered to this many decimals.
DECIMALS = 2

def both(rows):
    """The same rows in both directions."""
    return {"forward": tuple(rows), "backward": tuple(rows)}


def mirrored(fwd):
    """Forward rows, and their reflection going back."""
    return {"forward": tuple(fwd),
            "backward": tuple(sorted((-x if x else 0.0) for x in fwd))}


# Arm A, multiples of the family spread, adopted in PILOT.md Section 3 after
# price_range_sweep.py measured both failure modes. Arm A's pairs are matched in
# value, so nothing distinguishes the two directions and the rows are the same.
PRICE_ROWS_A = both((-3.0, -2.1, -1.5, -0.9, -0.45, 0.0,
                     0.45, 0.9, 1.5, 2.1, 3.0))

# Arm B, multiples of the family gain v, adopted from price_range_armb.py,
# candidate P1. THE ROWS ARE NOT SYMMETRIC. A forward row below zero pays the
# participant to take the better state and a backward row above zero charges
# them for the worse one, and both have one sensible answer. A forward row ABOVE
# the gain is the opposite of dominated: paying more than the money is worth is
# what a premium on the permission looks like, so the tail sits on that side
# only, and the backward rows mirror it.
PRICE_ROWS_B = mirrored((-1.0, -0.7, -0.45, -0.25, -0.12, 0.0,
                         0.12, 0.25, 0.45, 0.7, 1.0, 1.5))


# ----------------------------------------------------------------------------
# what differs between the arms, and nothing else does
# ----------------------------------------------------------------------------
def _best_permitted(state):
    return max(state["payoffs"][k] for k in state["permits"])


class Arm:
    def __init__(self, name, pairs, stimuli, template, sessions_out, task_dir,
                 price_rows, shape_key, sort_key, unit, intended, delivered,
                 value_tolerance, cell_view):
        self.name = name
        self.pairs = pairs
        self.stimuli = stimuli
        self.template = template
        self.sessions_out = sessions_out
        self.task_dir = task_dir
        self.price_rows = price_rows
        self.shape_key = shape_key          # fam -> grid cell to spread over
        self.sort_key = sort_key            # fam -> order within a grid cell
        self.unit = unit                    # fam -> money unit for the rows
        # The rows are centred on the value difference the pair is BUILT to
        # have, and the checks compare that against the difference the stimulus
        # actually DELIVERS. Centring on the delivered figure instead would have
        # pushed arm A's one-cent expected-value residual into 180 of its 1080
        # prices, for a design whose whole point is that the pair carries no
        # value. Keeping the two apart is what lets a stimulus that drifted past
        # its tolerance fail a check rather than quietly move the price list.
        self.intended = intended            # fam, a, b -> money, by construction
        self.delivered = delivered          # fam, frm, to -> money, as built
        self.value_tolerance = value_tolerance
        self.cell_view = cell_view          # fam, label -> what the task shows


ARMS = {
    "A": Arm(
        name="A", pairs=("CROSS", "CTRL_G", "CTRL_M"),
        stimuli="stimuli.json", template="task_template.html",
        sessions_out="sessions.json", task_dir="task",
        price_rows=PRICE_ROWS_A,
        shape_key=lambda f: (f["p_star"], f["d"]),
        sort_key=lambda f: f["sigma"],
        unit=lambda f: f["sigma"],
        # Arm A matches expected value across a pair, so the pair is built to
        # carry none, and build_stimuli.py matches to a tolerance of 0.02.
        intended=lambda f, a, b: 0.0,
        delivered=lambda f, frm, to: (
            f["states"][to]["H"] * f["states"][to]["p"]
            + f["states"][to]["L"] * (1 - f["states"][to]["p"])
            - f["states"][frm]["H"] * f["states"][frm]["p"]
            - f["states"][frm]["L"] * (1 - f["states"][frm]["p"])),
        value_tolerance=0.02,
        cell_view=lambda f, label: f["states"][label],
    ),
    "B": Arm(
        name="B", pairs=("CROSS", "CTRL_LO", "CTRL_HI"),
        stimuli="stimuli_armb.json", template="task_template_armb.html",
        sessions_out="sessions_armb.json", task_dir="task_armb",
        price_rows=PRICE_ROWS_B,
        # Arm A spreads over gamble shape first and gamble scale second. The
        # analogue here is the GAIN AS A FRACTION OF THE BASE, which is what
        # makes an elevation feel large or small, with the base payoff as the
        # scale. Grouping by the base instead would have taken the three
        # smallest gains from every cell and left the price unit barely varied,
        # and the price unit is v.
        shape_key=lambda f: round(f["v"] / f["b"], 3),
        sort_key=lambda f: (f["b"], f["a"]),
        unit=lambda f: f["v"],
        # Arm B's pairs are built to be worth exactly the family's gain, and
        # the payoffs are exact at the delivered precision, so the tolerance is
        # half of the last decimal rather than a modelling allowance.
        intended=lambda f, a, b: round(f["v"], DECIMALS),
        delivered=lambda f, frm, to: (_best_permitted(f["states"][to])
                                      - _best_permitted(f["states"][frm])),
        value_tolerance=0.5 * 10 ** (-DECIMALS),
        cell_view=lambda f, label: {
            "permits": list(f["states"][label]["permits"]),
            "payoffs": dict(f["states"][label]["payoffs"]),
            "actions": list(f["actions"]),
            "best": _best_permitted(f["states"][label]),
        },
    ),
}


def select_families(arm, stimuli, n=N_FAMILIES):
    """Span the grid rather than taking a corner of it.

    Families are grouped by shape and one is taken from each shape in turn,
    cycling, so the selection spreads over shapes first and scales second. The
    rule is deterministic and recorded, which `PILOT.md` Section 4 requires.
    """
    fams = stimuli["families"]
    by_shape = {}
    for f in fams:
        by_shape.setdefault(arm.shape_key(f), []).append(f)
    for k in by_shape:
        by_shape[k].sort(key=arm.sort_key)
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


def build_sessions(arm, stimuli, seed=SEED):
    rng = np.random.default_rng(seed)
    fams = select_families(arm, stimuli)
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
            for pair in arm.pairs:
                keys.append((fams[fi]["name"], pair))
                # deterministic counterbalance, three of six each way
                firsts.append(DIRECTIONS[k % 2])
        cells = order_cells(rng, keys, firsts)
        trials = []
        for (fam_name, pair, direction) in cells:
            fam = next(f for f in fams if f["name"] == fam_name)
            a, b = fam["pairs"][pair]
            frm, to = (a, b) if direction == "forward" else (b, a)
            unit = arm.unit(fam)
            # Taken once in the pair's stored orientation and NEGATED for the
            # other direction, so the two are exactly opposite. Rounding each
            # direction on its own does not guarantee that: a difference of
            # +0.005 and its negative do not round to opposites, and the check
            # below caught five families where they did not.
            delta = arm.intended(fam, a, b)
            if direction == "backward":
                delta = -delta
            multiples = arm.price_rows[direction]
            trials.append({
                "arm": arm.name,
                "family": fam_name, "pair": pair, "direction": direction,
                "from": arm.cell_view(fam, frm), "to": arm.cell_view(fam, to),
                "from_label": frm, "to_label": to,
                "prices": [round(delta + x * unit, 2) for x in multiples],
                "price_multiples": list(multiples),
                "value_difference": delta,
                "unit": unit,
            })
        sessions.append({"participant": "p%03d" % pi, "arm": arm.name,
                         "trials": trials})
    return fams, sessions


# ----------------------------------------------------------------------------
# the checks, each able to fail
# ----------------------------------------------------------------------------
VALUE_FRACTION = 0.25       # |value difference| this far into the unit counts


def carries_value(trial):
    return abs(trial["value_difference"]) > VALUE_FRACTION * trial["unit"]


def check_sessions(arm, fams, sessions):
    fails = []
    pairs = arm.pairs
    n_cells = len(pairs) * FAMILIES_PER_PARTICIPANT * len(DIRECTIONS)

    if len(sessions) != N_PARTICIPANTS:
        fails.append("participants %d, expected %d" % (len(sessions), N_PARTICIPANTS))

    counts = {}
    for s in sessions:
        if len(s["trials"]) != n_cells:
            fails.append("%s has %d cells, expected %d"
                         % (s["participant"], len(s["trials"]), n_cells))
        seen_fams = {t["family"] for t in s["trials"]}
        if len(seen_fams) != FAMILIES_PER_PARTICIPANT:
            fails.append("%s sees %d families, expected %d"
                         % (s["participant"], len(seen_fams), FAMILIES_PER_PARTICIPANT))
        for f in seen_fams:
            counts[f] = counts.get(f, 0) + 1
        # every family gets all three pairs in both directions
        got = {(t["family"], t["pair"], t["direction"]) for t in s["trials"]}
        for f in seen_fams:
            for pr in pairs:
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

    for s in sessions:
        for t in s["trials"]:
            # prices must be the adopted range, scaled by the family unit
            if list(t["price_multiples"]) != list(arm.price_rows[t["direction"]]):
                fails.append("%s uses price multiples that are not the adopted set"
                             % s["participant"])
                break
            # and centred on the value difference, which is the one price rule
            want = [round(t["value_difference"] + m * t["unit"], 2)
                    for m in t["price_multiples"]]
            if list(t["prices"]) != want:
                fails.append("%s %s %s prices are not the value difference plus "
                             "multiples of the unit"
                             % (s["participant"], t["family"], t["pair"]))
                break

    # WHAT THE STIMULUS DELIVERS MUST BE WHAT THE ROWS ASSUME. Arm A builds its
    # pairs to carry no value and arm B builds them to carry the family's gain.
    # If a stimulus drifted past its tolerance the rows would be centred in the
    # wrong place and nothing else here would notice.
    fam_by_name = {f["name"]: f for f in fams}
    for s in sessions:
        for t in s["trials"]:
            fam = fam_by_name.get(t["family"])
            if fam is None:
                fails.append("%s uses family %s, which is not in the selection"
                             % (s["participant"], t["family"]))
                break
            got = arm.delivered(fam, t["from_label"], t["to_label"])
            if abs(got - t["value_difference"]) > arm.value_tolerance:
                fails.append("%s %s %s %s is built to be worth %+.4f and "
                             "delivers %+.4f, past the tolerance of %.4f"
                             % (s["participant"], t["family"], t["pair"],
                                t["direction"], t["value_difference"], got,
                                arm.value_tolerance))
                break

    # the two directions of a pair must be worth opposite amounts, or the
    # design's cancellation does not hold
    bykey = {}
    for s in sessions:
        for t in s["trials"]:
            bykey.setdefault((s["participant"], t["family"], t["pair"]), {})[
                t["direction"]] = t["value_difference"]
    for k, d in bykey.items():
        if set(d) == set(DIRECTIONS) and abs(d["forward"] + d["backward"]) > 1e-6:
            fails.append("%s value differences %+.4f and %+.4f do not cancel"
                         % (k, d["forward"], d["backward"]))

    # NO DOMINATED ROWS. a forward row below zero pays the participant to take
    # the better state and a backward row above zero charges for the worse one.
    # The rule applies wherever a pair CARRIES VALUE. Arm A matches expected
    # value to a tolerance, not to the last decimal, so its residual difference
    # is a fraction of a percent of the unit and its rows straddle zero by
    # design. Comparing to zero exactly would have made the rule fire on arm A's
    # rounding, which is why the test is against the unit.
    for s in sessions:
        for t in s["trials"]:
            if not carries_value(t):
                continue
            if t["direction"] == "forward" and min(t["prices"]) < -1e-9:
                fails.append("%s %s %s has a forward row at %.2f, which pays the "
                             "participant to take the better state"
                             % (s["participant"], t["family"], t["pair"],
                                min(t["prices"])))
                break
            if t["direction"] == "backward" and max(t["prices"]) > 1e-9:
                fails.append("%s %s %s has a backward row at %.2f, which charges "
                             "for the worse state"
                             % (s["participant"], t["family"], t["pair"],
                                max(t["prices"])))
                break
    return fails


def load_stimuli(arm):
    with open(os.path.join(HERE, arm.stimuli), encoding="utf-8") as fh:
        return json.load(fh)


def self_test(arm):
    print("SELF-TEST arm %s, the checks must reject broken schedules" % arm.name)
    stim = load_stimuli(arm)
    fams, sessions = build_sessions(arm, stim)
    ok = True
    f = check_sessions(arm, fams, sessions)
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
        ("prices no longer centred on the value difference",
         lambda ss: ss[0]["trials"][0].__setitem__(
             "prices", [p + 5.0 for p in ss[0]["trials"][0]["prices"]]),
         "not the value difference plus"),
        ("a stimulus that no longer delivers what the rows assume",
         lambda ss: [t.__setitem__("value_difference",
                                   t["value_difference"] + 5.0)
                     for t in ss[0]["trials"][:1]],
         "past the tolerance"),
        ("the two directions no longer cancel",
         lambda ss: [t.__setitem__("value_difference", 1.0)
                     for t in ss[0]["trials"]],
         "do not cancel"),
    ]
    for label, break_it, expect in cases:
        ss = copy.deepcopy(sessions)
        break_it(ss)
        f = check_sessions(arm, fams, ss)
        hit = any(expect in x for x in f)
        print("  %-48s -> %s" % (label, "rejected" if hit else "NOT REJECTED"))
        if not hit:
            print("       expected %r, got %s" % (expect, f[:3]))
            ok = False

    # the dominated-row rule only bites where a pair carries value, so it is
    # tested on a cell that does
    if any(carries_value(t) for t in sessions[0]["trials"]):
        ss = copy.deepcopy(sessions)
        t = next(x for x in ss[0]["trials"] if carries_value(x))
        t["prices"] = [p - 3 * t["unit"] for p in t["prices"]]
        f = check_sessions(arm, fams, ss)
        hit = any("pays the participant" in x or "charges for the worse" in x
                  for x in f)
        print("  %-48s -> %s" % ("a dominated price row",
                                 "rejected" if hit else "NOT REJECTED"))
        ok = ok and hit
    else:
        print("  %-48s -> not applicable, arm %s pairs carry no value"
              % ("a dominated price row", arm.name))

    print("  SELF-TEST %s" % ("PASSED" if ok else "FAILED"))
    return ok, fams, sessions


def report(arm, fams, sessions):
    print()
    print("  %d families selected over %d grid cells"
          % (len(fams), len({arm.shape_key(f) for f in fams})))
    n_rows = len(arm.price_rows["forward"])
    print("  %d participants, %d cells each, %d price rows per cell"
          % (len(sessions), len(sessions[0]["trials"]), n_rows))
    print("  %d binary responses per participant"
          % sum(len(t["prices"]) for t in sessions[0]["trials"]))
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
    print("    family %s, pair %s, direction %s"
          % (t["family"], t["pair"], t["direction"]))
    if arm.name == "A":
        for side in ("from", "to"):
            st = t[side]
            print("    %-4s %s  H %.2f  p %.3f  L %.2f"
                  % (side, t[side + "_label"], st["H"], st["p"], st["L"]))
    else:
        for side in ("from", "to"):
            st = t[side]
            board = ", ".join(
                "%s %.2f%s" % (k, st["payoffs"][k],
                               "" if k in st["permits"] else " CLOSED")
                for k in st["actions"])
            print("    %-4s %s  %s  best %.2f"
                  % (side, t[side + "_label"], board, st["best"]))
    print("    value difference %+.2f, unit %.2f" % (t["value_difference"], t["unit"]))
    print("    prices %s" % ", ".join("%+.2f" % x for x in t["prices"]))


def main():
    argv = sys.argv[1:]
    arm_name = "A"
    if "--arm" in argv:
        arm_name = argv[argv.index("--arm") + 1].upper()
    if arm_name not in ARMS:
        print("unknown arm %r, expected one of %s" % (arm_name, sorted(ARMS)))
        return 1
    arm = ARMS[arm_name]

    ok, fams, sessions = self_test(arm)
    if not ok:
        return 1
    report(arm, fams, sessions)

    if "--html" in argv:
        tmpl_path = os.path.join(HERE, arm.template)
        with open(tmpl_path, encoding="utf-8") as fh:
            tmpl = fh.read()
        marker = "/*__SESSION__*/ null"
        assert tmpl.count(marker) == 1, "template marker missing"
        outdir = os.path.join(HERE, arm.task_dir)
        os.makedirs(outdir, exist_ok=True)
        for s2 in sessions:
            html = tmpl.replace(marker, json.dumps(s2))
            with open(os.path.join(outdir, "%s.html" % s2["participant"]), "w",
                      encoding="utf-8") as fh:
                fh.write(html)
        print()
        print("  written %s/%s.html through %s/%s.html, self-contained,"
              % (arm.task_dir, sessions[0]["participant"],
                 arm.task_dir, sessions[-1]["participant"]))
        print("  no server needed, each opens by double-clicking")

    if "--write" in argv:
        out = {"note": "pilot sessions, generated by session_builder.py",
               "arm": arm.name, "seed": SEED,
               "price_multiples": {d: list(v) for d, v in arm.price_rows.items()},
               "families": fams, "sessions": sessions}
        with open(os.path.join(HERE, arm.sessions_out), "w",
                  encoding="utf-8") as fh:
            json.dump(out, fh, indent=1)
        print()
        print("  written %s" % arm.sessions_out)
    else:
        print()
        print("  pass --write to emit %s" % arm.sessions_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
