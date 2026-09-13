#!/usr/bin/env python3
"""Measure the (d, q) coverage of wulff2018description in Psych-101. Stimuli only.

Answers one question before anything is registered: does this corpus occupy parts
of the interior that CPC18 and choices13k do not? Only the lottery parameters are
read. The choice tokens are parsed to confirm the transcript structure is
understood, and are counted, but no model is fitted to them here.

`wulff2018sampling` is excluded. It is the experience paradigm, where the
participant samples rather than being shown the lottery, so the parameters never
appear in the transcript and would have to be inferred from observed draws.

The coordinate is IMPORTED from `d4_rotation` and never restated, which is the
condition `prereg-d4gate-v1` failed.

    python wulff_coverage.py
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from d4_rotation import _opt_coords  # noqa: E402  IMPORTED, never restated

# "Lottery W offers 4.0 points with 80.0% probability or 0.0 points with 20.0% probability."
# "Lottery H offers 3.0 points with 100.0% probability."
LOT = re.compile(
    r"Lottery ([A-Z]) offers (-?[\d.]+) points with ([\d.]+)% probability"
    r"(?:,? or (-?[\d.]+) points with ([\d.]+)% probability)?\.")
PRESS = re.compile(r"You press <<([A-Z])>>\.")


def feats(H, p, L):
    ev = p * H + (1 - p) * L
    var = p * (H - ev) ** 2 + (1 - p) * (L - ev) ** 2
    return float(ev), float(np.sqrt(max(var, 0.0)))


def parse(text):
    """Yield (optionA, optionB, chosen_key) per problem, each option (H, p, L)."""
    lines = text.split("\n")
    pend = {}
    for ln in lines:
        m = LOT.search(ln)
        if m:
            key, x1, p1, x2, p2 = m.groups()
            x1, p1 = float(x1), float(p1) / 100.0
            if x2 is None:                       # degenerate lottery
                pend[key] = (x1, 1.0, x1)
            else:
                x2, p2 = float(x2), float(p2) / 100.0
                H, pH, L = (x1, p1, x2) if x1 >= x2 else (x2, p2, x1)
                pend[key] = (H, pH, L)
            continue
        m = PRESS.search(ln)
        if m and len(pend) == 2:
            (ka, a), (kb, b) = sorted(pend.items())
            yield a, b, m.group(1), (ka, kb)
            pend = {}


def summarise(name, d, q, n_problems, n_choices):
    dq = d * q
    return {
        "corpus": name,
        "n_problems": int(n_problems),
        "n_choices": int(n_choices),
        "d_min": float(d.min()), "d_max": float(d.max()),
        "d_distinct": int(len(np.unique(np.round(d, 3)))),
        "q_min": float(q.min()), "q_max": float(q.max()),
        "n_d_negative": int((d < -1e-9).sum()),
        "n_d_zero": int((np.abs(d) <= 1e-9).sum()),
        "n_d_positive": int((d > 1e-9).sum()),
        "n_interior_absd_lt_0p9": int((np.abs(d) < 0.9).sum()),
        "dq_sd": float(dq.std()),
    }


def main():
    from datasets import load_dataset
    ds = load_dataset("marcelbinz/Psych-101", split="train")
    rows = [r for r in ds if r["experiment"] == "wulff2018description/exp1.csv"]
    print("participants:", len(rows))

    seen, d_list, q_list, n_choices = set(), [], [], 0
    for r in rows:
        for a, b, chosen, keys in parse(r["text"]):
            n_choices += 1
            eva, sda = feats(*a)
            evb, sdb = feats(*b)
            risky = a if sda >= sdb else b
            key = (round(a[0], 4), round(a[1], 4), round(a[2], 4),
                   round(b[0], 4), round(b[1], 4), round(b[2], 4))
            if key in seen:
                continue
            seen.add(key)
            dd, qq = _opt_coords(*risky)
            d_list.append(dd); q_list.append(qq)

    d = np.array(d_list); q = np.array(q_list)
    out = summarise("wulff2018description", d, q, len(seen), n_choices)

    print("choices parsed:", n_choices, " distinct problems:", len(seen))
    print()
    for k, v in out.items():
        if k != "corpus":
            print("  %-28s %s" % (k, v))

    # occupancy grid, which is what "coverage" actually means here
    print()
    print("  occupancy, d rows by q columns, counts of distinct problems")
    db = np.digitize(d, [-0.6, -0.2, 0.2, 0.6])
    qb = np.digitize(q, [-0.6, -0.2, 0.2, 0.6])
    labels = ["<-0.6", "-0.6..-0.2", "-0.2..0.2", "0.2..0.6", ">0.6"]
    grid = collections.Counter(zip(db, qb))
    print("            " + "".join("%12s" % l for l in labels))
    for i, dl in enumerate(labels):
        print("  %-10s" % dl + "".join("%12d" % grid.get((i, j), 0)
                                       for j in range(5)))

    # the same metrics on the two corpora already used, so the comparison is
    # like for like rather than eyeballed
    allsum = {"wulff2018description": out}

    import pandas as pd
    raw = (pd.read_csv(os.path.join(HERE, "raw", "cpc18_raw.csv"),
                       usecols=["GameID", "Ha", "pHa", "La", "Hb", "pHb", "Lb"])
           .groupby("GameID").first().reset_index())
    dl, ql = [], []
    for r in raw.itertuples():
        _, sda = feats(r.Ha, r.pHa, r.La)
        _, sdb = feats(r.Hb, r.pHb, r.Lb)
        H, pp, L = (r.Ha, r.pHa, r.La) if sda >= sdb else (r.Hb, r.pHb, r.Lb)
        dd, qq = _opt_coords(H, pp, L)
        dl.append(dd); ql.append(qq)
    allsum["cpc18"] = summarise("cpc18", np.array(dl), np.array(ql), len(dl), len(dl))

    c = pd.read_csv(os.path.join(HERE, "raw", "choices13k", "c13k_selections.csv"),
                    usecols=["Block", "Feedback", "Ha", "pHa", "La", "Hb", "pHb", "Lb"])
    c = c[(c["Block"] == 1) & (c["Feedback"] == 0)].dropna()
    dl, ql = [], []
    for r in c.itertuples():
        _, sda = feats(r.Ha, r.pHa, r.La)
        _, sdb = feats(r.Hb, r.pHb, r.Lb)
        H, pp, L = (r.Ha, r.pHa, r.La) if sda >= sdb else (r.Hb, r.pHb, r.Lb)
        dd, qq = _opt_coords(H, pp, L)
        dl.append(dd); ql.append(qq)
    allsum["choices13k"] = summarise("choices13k", np.array(dl), np.array(ql),
                                     len(dl), len(dl))

    print()
    print("  like-for-like comparison")
    keys = ["n_problems", "d_distinct", "n_d_negative", "n_d_positive",
            "n_interior_absd_lt_0p9", "dq_sd"]
    print("  %-26s" % "metric" + "".join("%22s" % k for k in allsum))
    for k in keys:
        print("  %-26s" % k + "".join("%22s" % (
            ("%.3f" % allsum[c2][k]) if isinstance(allsum[c2][k], float)
            else allsum[c2][k]) for c2 in allsum))
    for c2 in allsum:
        n = allsum[c2]["n_problems"]
        i = allsum[c2]["n_interior_absd_lt_0p9"]
        print("  %-22s interior share %.1f%%" % (c2, 100.0 * i / max(n, 1)))

    with open(os.path.join(HERE, "wulff_coverage.json"), "w",
              encoding="utf-8") as fh:
        json.dump(allsum, fh, indent=2)
    print()
    print("written wulff_coverage.json")


if __name__ == "__main__":
    main()
