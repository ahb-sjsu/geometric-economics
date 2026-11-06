#!/usr/bin/env python3
"""The limit for kappa as the rule read it until 2026-11-05, scored on the seventh pilot rehearsal's simulated pilots
(PILOT.md, "The limit for kappa"). For comparison only: the bars read the revised limit (`pilot_analysis.py
summarise`).

    python kappa_compare.py OUT.json --old-reference REF.json --table TABLE.json RUN_DIR...

Each pilot's rate over both attributes and the unflagged people, which `analyse` stores beside the rule's statistic,
is read against the reference that rule used (results/pilot_reference_n120.json: format 3, 400 simulated pilots per
row), with the noise rows from that reference, at each percentile of agreement in NOISE_LEVELS. Printed per truth:
how often the 80% upper limit is at or above the true kappa.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pilot_analysis as P  # noqa: E402
import rehearsal as R  # noqa: E402


def old_rates(ref, row):
    """The old reference's simulated pilots' rate over both attributes and the unflagged people."""
    return ref["truths"][row]["lottery_rate_unflagged_draws"]


def main(out, old_path, table_path, dirs):
    old, tab = P.load(old_path), P.load_table(table_path)
    if old.get("format") != "correlation-pilot-reference/3":
        raise P.Refusal("format", f"{old_path} is not the reference the old rule read (format 3)")
    kappas, targets = sorted(tab["kappas"]), sorted(tab["targets"])
    by = {}
    for d in dirs:
        for p in sorted(glob.glob(os.path.join(d, "rehearse_*.json"))):
            r = P.load(p)
            by.setdefault(r["truth"], []).extend(r["pilots"])
    res = {"old_reference_sha256": P.sha256(old_path), "table_sha256": P.sha256(table_path), "truths": {}}
    for truth, pp in sorted(by.items()):
        k = R.spec(truth)["kappa"]
        line = {"pilots": len(pp), "covers": {}}
        for q in P.NOISE_LEVELS:
            limits = []
            for x in pp:
                u = x["rule"]
                rows = P.noise_rows(u["a_levels"][f"{q:g}"], u["q_upper"], old, kappas, targets)
                draws, _ = P.kappa_belt(u["lottery_rate_unflagged"], rows, old, kappas, targets, simulated=old_rates)
                limits.append(float(np.quantile(draws, 0.8)))
            line["covers"][f"{q:g}"] = float(np.mean([v >= k for v in limits]))
        res["truths"][truth] = line
        print(truth, json.dumps(line), flush=True)
    P.dump(res, out)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("out")
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--old-reference", required=True)
    ap.add_argument("--table", required=True)
    a = ap.parse_args()
    np.seterr(all="ignore")
    main(a.out, a.old_reference, a.table, a.dirs)
