#!/usr/bin/env python3
"""Round trip. What the task emits must be what the analysis reads.

A format mismatch between the instrument and the analysis is the kind of thing
discovered after sixty people have sat through a session. This parses the session
back out of a delivered task file, synthesises answers, assembles the response
document in **exactly the shape the task's own save step produces**, and pushes it
through `pilot_analysis`.

It also checks the two things a silent mismatch would hide. Every cell the task
delivers must appear in the analysis table, and the price rows must be ascending,
because `read_list` finds the switch by walking them in order and would read a
descending list backwards without complaining.

    python roundtrip_check.py
"""
from __future__ import annotations

import json
import os
import re
import sys

import numpy as np

import pilot_analysis as P

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.join(HERE, "task")


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
    threshold, with noise. Not a model of anything, just a filled-in form."""
    records = []
    for t in session["trials"]:
        thr = centre_shift * t["sigma"] * (1 if t["direction"] == "forward" else -1)
        thr += rng.normal(0, 0.5 * t["sigma"])
        accepts = [1 if pr < thr else 0 for pr in t["prices"]]
        records.append({"participant": session["participant"],
                        "family": t["family"], "pair": t["pair"],
                        "direction": t["direction"], "prices": t["prices"],
                        "accepts": accepts})
    # exactly the shape task_template.html assembles in finish()
    return {"source": "human", "participant": session["participant"],
            "generated": "roundtrip", "records": records}


def main():
    files = sorted(f for f in os.listdir(TASK) if f.endswith(".html"))
    print("=" * 74)
    print("ROUND TRIP, TASK OUTPUT INTO THE ANALYSIS")
    print("=" * 74)
    print("  %d delivered task files" % len(files))

    rng = np.random.default_rng(4)
    all_records, cells_delivered = [], 0
    ascending_ok = True
    for fn in files:
        s = session_from_html(os.path.join(TASK, fn))
        cells_delivered += len(s["trials"])
        for t in s["trials"]:
            pr = t["prices"]
            if any(pr[i] >= pr[i + 1] for i in range(len(pr) - 1)):
                ascending_ok = False
        doc = answer(s, rng)
        # the analysis must accept the document as the task writes it
        tmp = os.path.join(HERE, "_roundtrip_tmp.json")
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(doc, fh)
        src, recs = P.load_responses(tmp)
        os.remove(tmp)
        assert src == "human", "task must declare human responses"
        all_records += recs

    print("  price rows ascending in every cell: %s" % ascending_ok)
    if not ascending_ok:
        print("  FAIL. read_list walks the rows in order and would read a")
        print("  descending list backwards without complaining.")
        return 1

    excess, flags = P.excess_table(all_records)
    print("  cells delivered by the task            %d" % cells_delivered)
    print("  cells read by the analysis             %d" % flags["total"])
    print("  participant and family pairs recovered %d" % len(excess))
    expected_pairs = len(files) * 3
    print("  expected pairs                         %d" % expected_pairs)

    ok = (flags["total"] == cells_delivered) and (len(excess) == expected_pairs)
    print()
    if not ok:
        print("  MISMATCH. the instrument and the analysis do not agree.")
        return 1

    out = P.analyse(all_records, provenance="simulated")
    print("  the analysis runs end to end on task-shaped input")
    print("    non-monotone share      %.3f" % out["nonmonotone_share"])
    print("    worst cell at an edge   %.3f" % out["worst_cell_floor_ceiling"])
    print("    price slope z           %.1f" % out["price_slope_z"])
    print()
    print("  ROUND TRIP OK. Every cell the task delivers is read, and nothing")
    print("  is invented. The numbers above come from synthetic answers and")
    print("  mean nothing about people.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
