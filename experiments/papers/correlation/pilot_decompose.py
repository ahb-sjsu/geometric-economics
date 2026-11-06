#!/usr/bin/env python3
"""Which of the rule's limits makes it stop (PILOT.md, "Pilot size").

    python pilot_decompose.py OUT.json --reference REF.json --table TABLE.json [--noise-q Q] RUN_DIR...

Takes the pilot rehearsal's simulated pilots (`pilot_analysis.py rehearse` outputs in each RUN_DIR) and applies the
sample-size rule (`pilot_analysis.choose_n`) again, in both populations, with one or more of its three inputs replaced
by the truth's own value:

  as_run        the rule as the pilot read it
  share         the upper limit of the share at every row set to the planted share
  noise         the agreement the rule reads set to the truth row's simulated median, the rows recomputed
  kappa         kappa's draws within 0.005 of the true kappa: the belt of a pilot without limit
  kappa_row     kappa's draws just below the true kappa, so the truth's own row is read
  noise_share   noise and share exact, kappa as the pilot read it
  exact         all three exact, kappa as the belt of a pilot without limit: where a larger pilot leads
  exact_row     all three exact and the truth's own row read: the n the truth needs, a check on the rest

--noise-q first reads each pilot at another percentile of its agreement, as `summarise --noise-q` does, so that
as_run is the rule at that level (PILOT.md, "Noise assurance").

For each it reports how often the rule stops, how often it chooses an n at which the truth's power is below 0.80, and
the n it chose. The reference must be the one the pilots were read against, for the agreement medians and flag rates.
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


def variants(rule, spec, ref, kappas, targets):
    k, t, s = spec["kappa"], spec["target"], spec["share"]

    def with_share(r):
        return {**r, "rows": {kk: ({**row, "s_upper": s} if row.get("targets") else row) for kk, row in r["rows"].items()}}

    noise = {**rule, "rows": P.noise_rows(ref["truths"][P.cell(k, t)]["agreement"]["q50"], rule["q_upper"], ref,
                                          kappas, targets)}
    narrow = [float(x) for x in np.linspace(k - 0.005, k + 0.005, P.BELT_GRID)]
    own = [k - 1e-6] * P.BELT_GRID
    both = with_share(noise)
    return {"as_run": rule, "share": with_share(rule), "noise": noise, "kappa": {**rule, "kappa_draws": narrow},
            "kappa_row": {**rule, "kappa_draws": own}, "noise_share": both, "exact": {**both, "kappa_draws": narrow},
            "exact_row": {**both, "kappa_draws": own}}


def main(out, ref_path, table_path, dirs, noise_q=None):
    ref, tab = P.load(ref_path), P.load_table(table_path)
    kappas, targets = sorted(tab["kappas"]), sorted(tab["targets"])
    by = {}
    for d in dirs:
        for p in sorted(glob.glob(os.path.join(d, "rehearse_*.json"))):
            r = P.load(p)
            if r["reference_sha256"] != P.sha256(ref_path):
                raise P.Refusal("rules", f"{p} was run against another reference")
            by.setdefault(r["truth"], []).extend(r["pilots"])
    res = {"reference_sha256": P.sha256(ref_path), "table_sha256": P.sha256(table_path), "noise_q": noise_q,
           "truths": {}}
    for truth, pp in sorted(by.items()):
        spec = R.spec(truth)
        res["truths"][truth] = {"pilots": len(pp)}
        rules = [P.read_at(q["rule"], noise_q, ref, kappas, targets) if noise_q is not None else q["rule"] for q in pp]
        V = [variants(rule, spec, ref, kappas, targets) for rule in rules]
        for pop in ("all", "unflagged"):
            tp = {m: P.true_power(tab, truth, m, pop)[0] for m in P.MAIN_NS}
            line = {"truth_needs": next((m for m in P.MAIN_NS if tp[m] >= P.TARGET_POWER), None),
                    "true_power": {str(m): v for m, v in tp.items()}}
            for name in V[0]:
                ns = [P.choose_n(v[name], tab, pop).get("n") for v in V]
                line[name] = {"stops": float(np.mean([m is None for m in ns])),
                              "bad_choices": float(np.mean([m is not None and tp[m] < P.TARGET_POWER for m in ns])),
                              "n": {str(m): ns.count(m) for m in P.MAIN_NS} | {"none": ns.count(None)}}
            res["truths"][truth][pop] = line
            print(truth, pop, "needs", line["truth_needs"], flush=True)
            for name in V[0]:
                x = line[name]
                print(f"   {name:12s} stops {x['stops']:.2f}  bad choices {x['bad_choices']:.2f}  {x['n']}", flush=True)
    P.dump(res, out)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("out")
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--reference", required=True)
    ap.add_argument("--table", required=True)
    ap.add_argument("--noise-q", type=float, default=None,
                    help="read the pilots at this percentile of agreement instead of the one they ran with")
    a = ap.parse_args()
    np.seterr(all="ignore")
    main(a.out, a.reference, a.table, a.dirs, a.noise_q)
