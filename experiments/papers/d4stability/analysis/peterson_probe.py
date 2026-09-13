#!/usr/bin/env python3
"""SUPERSEDED. Kept as the audit trail, not as working code.

**Its `parse` is wrong and its numbers are wrong.** It yields a trial only when
exactly two option declarations are pending, which captures the first press on a
problem and silently discards the four that follow, losing 91 percent of the
corpus. Probe 3 measured that. `peterson_parse.py` is the parser to use, and it
accounts for every press token rather than dropping what it does not recognise.

This file survives because the registration's Section 14 cites it, and because a
lineage that deletes its wrong turns cannot show that it found them.

The original docstring follows.

---

Structure probe for peterson2021using/exp1.csv in Psych-101. Covariates only.

Answers the questions a registration has to answer before it can declare folds:
how many participants, how many trials each, how many distinct problems, whether
participants share stimuli (which decides whether a participant split holds
stimulus composition roughly constant), and how outcome scale is distributed
(which is the pre-declared stimulus axis of the stability test).

The choice token is parsed and counted, because a transcript whose choices do not
parse is a transcript we do not understand. It is never joined to a covariate and
no model is fitted here.

The coordinate is IMPORTED from `d4_rotation` and never restated, which is the
condition `prereg-d4gate-v1` failed.

    python peterson_probe.py
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
sys.path.insert(0, DATASETS)

from d4_rotation import _opt_coords  # noqa: E402  IMPORTED, never restated

_d, _q = _opt_coords(10.0, 1.0, 10.0)
assert abs(_d - 1.0) < 1e-9, "imported _opt_coords is not the expected coordinate"

# "Option L delivers 10.0 points with 80.0% chance, or -25.0 points with 20.0% chance."
# "Option F delivers 3.0 points with 100.0% chance."
OPT = re.compile(
    r"Option ([A-Z]) delivers (-?[\d.]+) points with ([\d.]+)% chance"
    r"(?:,? or (-?[\d.]+) points with ([\d.]+)% chance)?\.")
PRESS = re.compile(r"You press <<([A-Z])>>\.")


def feats(H, p, L):
    ev = p * H + (1 - p) * L
    var = p * (H - ev) ** 2 + (1 - p) * (L - ev) ** 2
    return float(ev), float(np.sqrt(max(var, 0.0)))


def parse(text):
    """Yield (optA, optB, pressed_key, (keyA, keyB)), each option (H, p, L)."""
    pend = {}
    for ln in text.split("\n"):
        m = OPT.search(ln)
        if m:
            key, x1, p1, x2, p2 = m.groups()
            x1, p1 = float(x1), float(p1) / 100.0
            if x2 is None:
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


def main():
    from datasets import load_dataset
    ds = load_dataset("marcelbinz/Psych-101", split="train")
    rows = [r for r in ds if r["experiment"] == "peterson2021using/exp1.csv"]
    print("participants:", len(rows))

    per_part, prob_parts = [], collections.defaultdict(set)
    d_all, q_all, scale_all = [], [], []
    n_trials = n_unparsed_press = 0
    seen = {}

    for i, r in enumerate(rows):
        k = 0
        for a, b, pressed, keys in parse(r["text"]):
            k += 1
            if pressed not in keys:
                n_unparsed_press += 1
            _, sda = feats(*a)
            _, sdb = feats(*b)
            risky = a if sda >= sdb else b
            key = (round(a[0], 4), round(a[1], 4), round(a[2], 4),
                   round(b[0], 4), round(b[1], 4), round(b[2], 4))
            prob_parts[key].add(i)
            if key not in seen:
                dd, qq = _opt_coords(*risky)
                scale = max(abs(risky[0]), abs(risky[2]))
                seen[key] = (dd, qq, scale)
                d_all.append(dd); q_all.append(qq); scale_all.append(scale)
        per_part.append(k)
        n_trials += k

    per_part = np.array(per_part)
    d = np.array(d_all); q = np.array(q_all); scale = np.array(scale_all)

    print("trials parsed:", n_trials, " press tokens off-menu:", n_unparsed_press)
    print("trials per participant: min %d  median %d  max %d"
          % (per_part.min(), int(np.median(per_part)), per_part.max()))
    print("distinct problems:", len(seen))
    print()

    # does a participant split hold stimuli common? if each problem is seen by a
    # handful of participants, it does not, and the participant arm is really a
    # second stimulus split.
    subj_per_prob = np.array([len(v) for v in prob_parts.values()])
    print("participants per problem: min %d  median %d  mean %.1f  max %d"
          % (subj_per_prob.min(), int(np.median(subj_per_prob)),
             subj_per_prob.mean(), subj_per_prob.max()))

    # the pre-declared stimulus axis. (d, q) is exactly invariant under positive
    # scaling of both outcomes, so a split on scale is a split the coordinate
    # cannot see. verified here rather than asserted.
    lam = 7.3
    bad = 0
    for key, (dd, qq, _s) in list(seen.items())[:2000]:
        Ha, pa, La, Hb, pb, Lb = key
        _, sa = feats(Ha, pa, La)
        _, sb = feats(Hb, pb, Lb)
        H, p, L = (Ha, pa, La) if sa >= sb else (Hb, pb, Lb)
        d2, q2 = _opt_coords(H * lam, p, L * lam)
        if abs(d2 - dd) > 1e-9 or abs(q2 - qq) > 1e-9:
            bad += 1
    print("scale invariance of (d, q) at lambda=%.1f: %d violations in %d checked"
          % (lam, bad, min(2000, len(seen))))
    print()

    ls = np.log10(np.maximum(scale, 1e-9))
    cuts = np.quantile(ls, [0.25, 0.5, 0.75])
    fold = np.digitize(ls, cuts)
    print("log10 outcome scale: min %.2f  q25 %.2f  q50 %.2f  q75 %.2f  max %.2f"
          % (ls.min(), cuts[0], cuts[1], cuts[2], ls.max()))
    print()
    print("  scale fold   n_problems   interior |d|<0.9   d<0    d>0    sd(d*q)")
    folds = {}
    for f in range(4):
        m = fold == f
        folds[str(f)] = {
            "n_problems": int(m.sum()),
            "n_interior": int((np.abs(d[m]) < 0.9).sum()),
            "n_d_negative": int((d[m] < -1e-9).sum()),
            "n_d_positive": int((d[m] > 1e-9).sum()),
            "dq_sd": float((d[m] * q[m]).std()),
        }
        print("  %10d   %10d   %16d   %4d   %4d   %8.3f"
              % (f, m.sum(), (np.abs(d[m]) < 0.9).sum(),
                 (d[m] < -1e-9).sum(), (d[m] > 1e-9).sum(),
                 (d[m] * q[m]).std()))

    out = {
        "n_participants": len(rows),
        "n_trials": int(n_trials),
        "n_distinct_problems": len(seen),
        "off_menu_press_tokens": int(n_unparsed_press),
        "trials_per_participant": {
            "min": int(per_part.min()), "median": int(np.median(per_part)),
            "max": int(per_part.max())},
        "participants_per_problem": {
            "min": int(subj_per_prob.min()),
            "median": int(np.median(subj_per_prob)),
            "mean": float(subj_per_prob.mean()),
            "max": int(subj_per_prob.max())},
        "scale_invariance_violations": int(bad),
        "log10_scale_quartile_cuts": [float(c) for c in cuts],
        "scale_folds": folds,
        "n_interior_total": int((np.abs(d) < 0.9).sum()),
        "d_distinct": int(len(np.unique(np.round(d, 3)))),
    }
    with open(os.path.join(HERE, "peterson_probe.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written peterson_probe.json")


if __name__ == "__main__":
    main()
