#!/usr/bin/env python3
"""Choosing the price range by measuring, rather than by widening until it looks safe.

`PILOT.md` Section 3 marked the provisional range of plus or minus one spread as
provisional, because a self-test censored the crossing pair's forward cell 22
percent of the time and attenuated the between-family standard deviation from a
planted 0.300 to 0.228.

**Widening is not free.** The number of rows is what a participant's time buys, so
a wider range over the same rows is a coarser grid, and coarse rows add
quantisation noise to every indifference price. The two failure modes pull in
opposite directions.

    too narrow   the tails of the crossing cell fall off the end and the
                 components are attenuated
    too coarse   every price is read to the nearest wide interval and the
                 components are inflated by quantisation

So this sweeps candidate row-sets against a planted truth and reports both costs
for each. The range is then chosen from the table rather than argued for.

It also sweeps a **noise level one and a half times the planted one**, because the
real noise is unknown until the pilot measures it and a range chosen at exactly
the assumed noise is a range with no margin.

    python price_range_sweep.py
"""
from __future__ import annotations

import json
import os

import numpy as np

import pilot_analysis as P

HERE = os.path.dirname(os.path.abspath(__file__))

TRUTH = {"sd_fam": 0.30, "sd_part": 0.40, "sd_res": 0.50}
N_SEEDS = 6


def hybrid(span, n_fine, fine_step):
    """Rows dense near zero and sparse in the tails, since most switches are
    near zero and the tails only need to be reachable."""
    fine = [round(i * fine_step, 4) for i in range(1, n_fine + 1)]
    out = list(fine)
    x = fine[-1]
    while x < span - 1e-9:
        x = min(span, round(x * 1.55, 4))
        out.append(x)
    rows = sorted(set([-v for v in out] + [0.0] + out))
    return tuple(rows)


CANDIDATES = {
    "A current, +/-1.0, 11 rows": (-1.0, -0.7, -0.5, -0.3, -0.15, 0.0,
                                   0.15, 0.3, 0.5, 0.7, 1.0),
    "B +/-2.0, 11 rows": tuple(2.0 * x for x in
                               (-1.0, -0.7, -0.5, -0.3, -0.15, 0.0,
                                0.15, 0.3, 0.5, 0.7, 1.0)),
    "C +/-3.0, 11 rows": tuple(3.0 * x for x in
                               (-1.0, -0.7, -0.5, -0.3, -0.15, 0.0,
                                0.15, 0.3, 0.5, 0.7, 1.0)),
    "D +/-2.5, hybrid 15 rows": hybrid(2.5, 3, 0.2),
    "E +/-3.0, hybrid 17 rows": hybrid(3.0, 4, 0.18),
    "F +/-4.0, hybrid 19 rows": hybrid(4.0, 4, 0.18),
}


def evaluate(rows, noise_mult, seeds=N_SEEDS):
    """Worst-cell censoring and recovery error, averaged over seeds."""
    edge, fam_err, part_err, res_err, nrows = [], [], [], [], len(rows)
    tf = TRUTH["sd_fam"] * noise_mult
    tp = TRUTH["sd_part"] * noise_mult
    tr = TRUTH["sd_res"] * noise_mult
    for s in range(seeds):
        recs = P.simulate(n_fam=40, n_part=120, sd_fam=tf, sd_part=tp,
                          sd_res=tr, price_rows=rows, seed=100 + s)
        out = P.analyse(recs)
        edge.append(out["worst_cell_floor_ceiling"])
        fam_err.append(out["between_family_sd"] - tf)
        part_err.append(out["participant_sd"] - tp)
        res_err.append(out["residual_sd"] - tr)
    return {"rows": nrows,
            "worst_edge": float(np.mean(edge)),
            "family_bias": float(np.mean(fam_err)),
            "family_bias_pct": float(100 * np.mean(fam_err) / tf),
            "participant_bias_pct": float(100 * np.mean(part_err) / tp),
            "residual_bias_pct": float(100 * np.mean(res_err) / tr)}


def main():
    print("=" * 78)
    print("PRICE RANGE SWEEP")
    print("=" * 78)
    print("planted components  family %.2f  participant %.2f  residual %.2f"
          % (TRUTH["sd_fam"], TRUTH["sd_part"], TRUTH["sd_res"]))
    print("averaged over %d seeds, 40 families and 120 participants each" % N_SEEDS)

    results = {}
    for mult, label in ((1.0, "AT THE ASSUMED NOISE"),
                        (1.5, "AT ONE AND A HALF TIMES THE ASSUMED NOISE")):
        print()
        print(label)
        print("  candidate                      rows   worst edge   family bias")
        for name, rows in CANDIDATES.items():
            r = evaluate(rows, mult)
            results["%s @%.1f" % (name, mult)] = r
            flag = ""
            if r["worst_edge"] > 0.15:
                flag = "  CENSORED"
            elif abs(r["family_bias_pct"]) > 12:
                flag = "  biased"
            print("  %-30s %4d   %8.3f   %+8.1f%%%s"
                  % (name, r["rows"], r["worst_edge"],
                     r["family_bias_pct"], flag))

    print()
    print("=" * 78)
    print("READING THE TABLE")
    print("=" * 78)
    print("  A candidate is usable only if it survives the HIGHER noise row,")
    print("  because the real noise is unknown until the pilot measures it and a")
    print("  range with no margin is a range that fails on contact with data.")
    ok = [n for n in CANDIDATES
          if results["%s @1.5" % n]["worst_edge"] <= 0.15
          and abs(results["%s @1.5" % n]["family_bias_pct"]) <= 12]
    print()
    if ok:
        best = min(ok, key=lambda n: results["%s @1.5" % n]["rows"])
        print("  usable at the higher noise: %s" % ", ".join(sorted(ok)))
        print("  cheapest of those in rows:  %s" % best)
        print()
        r1 = results["%s @1.0" % best]
        r15 = results["%s @1.5" % best]
        print("  chosen rows (multiples of the family spread)")
        print("    %s" % ", ".join("%+.2f" % x for x in CANDIDATES[best]))
        print("  at the assumed noise   worst edge %.3f  family bias %+.1f%%"
              % (r1["worst_edge"], r1["family_bias_pct"]))
        print("  at 1.5x the noise      worst edge %.3f  family bias %+.1f%%"
              % (r15["worst_edge"], r15["family_bias_pct"]))
        rows_per_participant = r1["rows"] * 18
        print()
        print("  cost, 18 cells per participant: %d rows, against %d on the"
              % (rows_per_participant, 11 * 18))
        print("  provisional range. About %d extra binary responses."
              % (rows_per_participant - 11 * 18))
        chosen = {"name": best, "rows": list(CANDIDATES[best]),
                  "at_assumed_noise": r1, "at_1_5x_noise": r15,
                  "rows_per_participant": rows_per_participant}
    else:
        print("  NO CANDIDATE SURVIVES. widen further or accept more rows.")
        chosen = None

    with open(os.path.join(HERE, "price_range_sweep.json"), "w",
              encoding="utf-8") as fh:
        json.dump({"truth": TRUTH, "n_seeds": N_SEEDS,
                   "candidates": {k: list(v) for k, v in CANDIDATES.items()},
                   "results": results, "chosen": chosen}, fh, indent=2)
    print()
    print("written price_range_sweep.json")


if __name__ == "__main__":
    main()
