#!/usr/bin/env python3
"""Round trip. What the task emits must be what the analysis reads.

A format mismatch between the instrument and the analysis is the kind of thing
discovered after sixty people have sat through a session. This parses the session
back out of a delivered task file, synthesises answers, assembles the response
document in **exactly the shape the task's own save step produces**, and pushes it
through `pilot_analysis`.

It also checks the things a silent mismatch would hide.

    every cell the task delivers appears in the analysis table
    the price rows are ascending, because `read_list` walks them in order and
      would read a descending list backwards without complaining
    the rows are centred on the value difference the session recorded, because
      the analysis subtracts direction differences and a price list centred
      somewhere else would move a cell without failing anything

**Both arms run through it.** Arm B is the reason the last check exists. Its rows
sit either side of plus or minus the family gain rather than either side of zero,
so a check written against zero would have passed arm A and quietly mis-read arm
B.

    python roundtrip_check.py              # both arms
    python roundtrip_check.py --arm B
"""
from __future__ import annotations

import json
import os
import re
import sys

import numpy as np

import pilot_analysis as P
import session_builder as SB

HERE = os.path.dirname(os.path.abspath(__file__))


def session_from_html(path):
    """Recover the inlined session, the way a browser would receive it."""
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    m = re.search(r"const SESSION = (\{.*?\});\n", html, re.S)
    if not m:
        raise AssertionError("no inlined session found in %s" % path)
    return json.loads(m.group(1))


def answer(session, rng, centre_shift=0.4):
    """A synthetic participant. Switches once, where the price crosses a
    threshold, with noise. Not a model of anything, just a filled-in form.

    The threshold sits at the cell's value difference plus an asymmetry, which is
    what a participant who prices the money correctly and shows a direction
    effect would do.
    """
    records = []
    for t in session["trials"]:
        sign = 1 if t["direction"] == "forward" else -1
        thr = t["value_difference"] + centre_shift * t["unit"] * sign
        thr += rng.normal(0, 0.5 * t["unit"])
        accepts = [1 if pr < thr else 0 for pr in t["prices"]]
        records.append({"participant": session["participant"],
                        "family": t["family"], "pair": t["pair"],
                        "direction": t["direction"], "prices": t["prices"],
                        "accepts": accepts})
    # exactly the shape the task templates assemble in finish()
    return {"source": "human", "arm": session.get("arm"),
            "participant": session["participant"],
            "generated": "roundtrip", "records": records}


def run_arm(arm):
    task = os.path.join(HERE, arm.task_dir)
    if not os.path.isdir(task):
        print("  no %s directory. run session_builder.py --arm %s --html first."
              % (arm.task_dir, arm.name))
        return 1
    files = sorted(f for f in os.listdir(task) if f.endswith(".html"))
    print("  %d delivered task files in %s" % (len(files), arm.task_dir))

    rng = np.random.default_rng(4)
    all_records, cells_delivered = [], 0
    ascending_ok, centred_ok = True, True
    bad_centre = None
    for fn in files:
        s = session_from_html(os.path.join(task, fn))
        cells_delivered += len(s["trials"])
        for t in s["trials"]:
            pr = t["prices"]
            if any(pr[i] >= pr[i + 1] for i in range(len(pr) - 1)):
                ascending_ok = False
            want = [round(t["value_difference"] + m * t["unit"], 2)
                    for m in t["price_multiples"]]
            if list(pr) != want:
                centred_ok = False
                bad_centre = bad_centre or (s["participant"], t["family"], t["pair"])
        doc = answer(s, rng)
        # the analysis must accept the document as the task writes it
        tmp = os.path.join(HERE, "_roundtrip_tmp.json")
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(doc, fh)
        src, recs = P.load_responses(tmp)
        os.remove(tmp)
        assert src == "human", "task must declare human responses"
        all_records += recs

    print("  price rows ascending in every cell:              %s" % ascending_ok)
    print("  price rows centred on the value difference:      %s" % centred_ok)
    if not ascending_ok:
        print("  FAIL. read_list walks the rows in order and would read a")
        print("  descending list backwards without complaining.")
        return 1
    if not centred_ok:
        print("  FAIL at %s. the delivered rows are not the value difference"
              % (bad_centre,))
        print("  plus multiples of the unit, so a cell has been shifted.")
        return 1

    excess, flags = P.excess_table(all_records)
    print("  cells delivered by the task                     %d" % cells_delivered)
    print("  cells read by the analysis                      %d" % flags["total"])
    print("  participant and family pairs recovered          %d" % len(excess))
    expected_pairs = len(files) * SB.FAMILIES_PER_PARTICIPANT
    print("  expected pairs                                  %d" % expected_pairs)

    ok = (flags["total"] == cells_delivered) and (len(excess) == expected_pairs)
    if not ok:
        print("  MISMATCH. the instrument and the analysis do not agree.")
        return 1

    out = P.analyse(all_records, provenance="simulated")
    print("  the analysis runs end to end on task-shaped input")
    print("    non-monotone share      %.3f" % out["nonmonotone_share"])
    print("    worst cell at an edge   %.3f" % out["worst_cell_floor_ceiling"])
    print("    price slope z           %.1f" % out["price_slope_z"])
    return 0


def main():
    argv = sys.argv[1:]
    if "--arm" in argv:
        names = [argv[argv.index("--arm") + 1].upper()]
    else:
        names = sorted(SB.ARMS)
    rc = 0
    for n in names:
        print("=" * 74)
        print("ROUND TRIP, ARM %s, TASK OUTPUT INTO THE ANALYSIS" % n)
        print("=" * 74)
        rc |= run_arm(SB.ARMS[n])
        print()
    if rc == 0:
        print("ROUND TRIP OK. Every cell each task delivers is read, and nothing")
        print("is invented. The numbers above come from synthetic answers and")
        print("mean nothing about people.")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
