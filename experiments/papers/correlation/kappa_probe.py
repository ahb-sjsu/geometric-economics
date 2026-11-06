"""Probe, before the change of 2026-11-05: how precise, and how biased by rank-one people, each candidate kappa
statistic is (PILOT.md, "The limit for kappa"). Its output, with the code of src_v8 and 6,000 people per row, is
results/kappa_probe.txt.

    python kappa_probe.py SRC PEOPLE_PER_ROW

Per row (kappa x noise target, nobody of rank one) and per truth with 30% of rank-one people, simulated included
people (attention rule as recruitment applies it) and, per person, the calibration lotteries taken at the ideal on each
attribute and the pilot's self-only flag. Each candidate statistic is a mean over people, so a pilot's value has mean
= the people's mean and SD = the people's SD / sqrt(people used) at PILOT_N included people:

  current   both attributes, unflagged people (the rule from 2026-11-03 to 2026-11-05)
  self_all  self-attribute lotteries only, every included person (the rule from 2026-11-05)
  self_unf  self-attribute lotteries only, unflagged people

Printed: the pilot-level SD and the slope in kappa (per 0.25 step, central where possible), their ratio (the kappa
resolution: how far kappa must move to shift the statistic by one SD; smaller is sharper), and for the 30% truths
the shift the rank-one people make, in pilot SDs of the share-0 row: the statistic over the truth's people minus the
same over its traders alone (who are distributed as the share-0 row's people), with the own-row coverage of an 80%
limit it implies (Phi(0.8416 - shift)).
"""
import sys
import time

import numpy as np
from scipy.stats import norm

sys.path.insert(0, sys.argv[1])
import pilot_analysis as P  # noqa: E402

PEOPLE = int(sys.argv[2])
KAPPAS = (0.75, 1.0, 1.25, 1.5, 1.75, 2.0)
TARGETS = (1.5, 2.0)


def people(truth, m, seed):
    rng = np.random.default_rng([20261105, seed])
    out = []
    while len(out) < m:
        ch, shape = P.sim_choices(truth, rng)
        st = P.person(ch)
        if st["att_fail"] <= P.ATT_MAX:
            out.append((st["lot_cal_self"], st["lot_cal_charity"], st["self_hi"] >= P.FLAG_MIN, bool(shape.get("rank_one"))))
    a = np.array(out, float)
    return {"self": a[:, 0] / 12, "both": (a[:, 0] + a[:, 1]) / 24, "flag": a[:, 2].astype(bool), "r1": a[:, 3].astype(bool)}


def stats(p):
    unf = ~p["flag"]
    n = P.PILOT_N
    f = unf.mean()
    tr = ~p["r1"]
    # the same statistics over the traders alone: within a 30% truth they are distributed as the share-0 row's people,
    # so the difference is the shift the rank-one people make, without the noise of a second sample
    return {"current": (p["both"][unf].mean(), p["both"][unf].std() / np.sqrt(n * f), p["both"][unf & tr].mean()),
            "self_all": (p["self"].mean(), p["self"].std() / np.sqrt(n), p["self"][tr].mean()),
            "self_unf": (p["self"][unf].mean(), p["self"][unf].std() / np.sqrt(n * f), p["self"][unf & tr].mean()),
            "flagged": p["flag"].mean(), "r1_unflagged": (p["r1"] & unf).sum() / unf.sum()}


t0 = time.time()
res = {}
for t in TARGETS:
    for j, k in enumerate(KAPPAS):
        res[(k, t, 0)] = stats(people(P.cell(k, t), PEOPLE, j * 10 + int(t * 10)))
    for k in (1.0, 1.5, 2.0):
        res[(k, t, 30)] = stats(people(P.cell(k, t, 0.3), PEOPLE, 900 + int(k * 100) + int(t * 10)))
print(f"{PEOPLE} people per row, {time.time() - t0:.0f} s; pilot of {P.PILOT_N} included people")
for t in TARGETS:
    print(f"\n== noise target {t}")
    for j, k in enumerate(KAPPAS):
        r = res[(k, t, 0)]
        line = f"kappa {k:4.2f} flagged {r['flagged']:.3f} |"
        for s in ("current", "self_all", "self_unf"):
            lo, hi = KAPPAS[max(0, j - 1)], KAPPAS[min(len(KAPPAS) - 1, j + 1)]
            slope = (res[(hi, t, 0)][s][0] - res[(lo, t, 0)][s][0]) / ((hi - lo) / 0.25)
            m, sd, _ = r[s]
            line += f" {s} mean {m:.4f} sd {sd:.4f} slope/0.25 {slope:+.4f} res {abs(sd / slope) * 0.25:.3f} |"
        print(line)
    for k in (1.0, 1.5, 2.0):
        r, r0 = res[(k, t, 30)], res[(k, t, 0)]
        line = f"S30 kappa {k:4.2f} flagged {r['flagged']:.3f} rank-one among unflagged {r['r1_unflagged']:.3f} |"
        for s in ("current", "self_all", "self_unf"):
            z = (r[s][0] - r[s][2]) / r0[s][1]
            line += f" {s} shift {z:+.2f} sd -> own-row cover {norm.cdf(0.8416 - z):.3f} |"
        print(line)
