#!/usr/bin/env python3
"""Ruggeri leg — held-out leg #2 of prereg-sigma-v1 (a clean discrete-choice re-test).

Ruggeri et al. (2020, Nature Human Behaviour) replicated the 17 Kahneman-Tversky
(1979) choice problems across 19 countries (4,098 subjects). Each column 1..17 is a
binary choice (1 = option A, 0 = option B). This is a *clean* discrete-choice lottery
corpus in the SAME 5-feature space as the constrained-Σ fuzz, so it is a direct,
apples-to-apples re-test of the low-rank hypothesis (H1/H3/H4) on held-out data, plus
a cross-country transfer test (H2 analog).

Problem definitions transcribed from eris-econ/prospect.py (KT 1979 as replicated).
Economically-correct encoding: item 11 uses the effective two-stage prospect; items
12-13 fold in the endowment (final-wealth outcomes).

    python ruggeri.py
"""
from __future__ import annotations

import csv
import os

import numpy as np

import constrained_sigma_fuzz as F

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "raw_social", "ruggeri.csv")

# (option_a, option_b) as [(amount, prob), ...]; domain for diagnostics.
KT = {
    1:  ([(2500, .33), (2400, .66), (0, .01)], [(2400, 1.)], "gain"),
    2:  ([(2500, .33), (0, .67)], [(2400, .34), (0, .66)], "gain"),
    3:  ([(4000, .80), (0, .20)], [(3000, 1.)], "gain"),
    4:  ([(4000, .20), (0, .80)], [(3000, .25), (0, .75)], "gain"),
    5:  ([(6000, .45), (0, .55)], [(3000, .90), (0, .10)], "gain"),
    6:  ([(6000, .001), (0, .999)], [(3000, .002), (0, .998)], "gain"),
    7:  ([(-4000, .80), (0, .20)], [(-3000, 1.)], "loss"),
    8:  ([(-4000, .20), (0, .80)], [(-3000, .25), (0, .75)], "loss"),
    9:  ([(-6000, .45), (0, .55)], [(-3000, .90), (0, .10)], "loss"),
    10: ([(-6000, .001), (0, .999)], [(-3000, .002), (0, .998)], "loss"),
    11: ([(4000, .20), (0, .80)], [(3000, .25), (0, .75)], "gain"),        # effective two-stage
    12: ([(3000, .50), (2000, .50)], [(2500, 1.)], "gain"),                # +2000 endowment
    13: ([(2000, .50), (4000, .50)], [(3000, 1.)], "loss"),                # +4000 endowment
    14: ([(6000, .25), (0, .75)], [(4000, .25), (2000, .25), (0, .50)], "gain"),
    15: ([(-6000, .25), (0, .75)], [(-4000, .25), (-2000, .25), (0, .50)], "loss"),
    16: ([(5000, .001), (0, .999)], [(5, 1.)], "gain"),
    17: ([(-5000, .001), (0, .999)], [(-5, 1.)], "loss"),
}


def feats(payoffs):
    a = np.array([x for x, _ in payoffs], float)
    p = np.array([q for _, q in payoffs], float)
    ev = float((a * p).sum())
    var = float((p * (a - ev) ** 2).sum())
    sd = np.sqrt(max(var, 0.0))
    sk = float((p * ((a - ev) / sd) ** 3).sum()) if sd > 1e-9 else 0.0
    worst = float(a.min())
    pfav = float(p[a >= ev].sum())
    return [ev, sd, sk, worst, pfav]


def load():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    Xprob = {q: np.array([feats(KT[q][0]), feats(KT[q][1])]) for q in KT}  # [A,B] x 5
    # counts[country][q] = [nA, n]
    from collections import defaultdict
    cnt = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for r in rows:
        ctry = r["Country"]
        for q in KT:
            v = r.get(str(q), "")
            if v in ("", "NA", None):
                continue
            cnt[ctry][q][0] += int(float(v) >= 0.5)  # chose A
            cnt[ctry][q][1] += 1
    return Xprob, cnt


def problems_for(Xprob, cnt, countries, qs=None):
    qs = qs or list(KT)
    out = []
    for ctry in countries:
        for q in qs:
            nA, n = cnt[ctry][q]
            if n == 0:
                continue
            obs = np.array([nA / n, 1 - nA / n])
            out.append((Xprob[q], obs, float(n)))
    return out


def main():
    Xprob, cnt = load()
    countries = sorted(cnt)
    print(f"Ruggeri: {len(countries)} countries, 17 KT problems, "
          f"{sum(n for c in cnt.values() for _, n in c.values())} choices | K=5 lottery features\n")

    # ---- pooled H1/H3/H4 (all country x problem cells) ----
    pooled = F._zscale(problems_for(Xprob, cnt, countries))[0]
    ch = F.uniform_nll(pooled)
    structs = ["isotropic", "diagonal", "rank1", "rank2", "banded", "block", "full"]
    fit = {}
    print(f"{'structure':11} {'#p':>3} {'native NLL':>11}")
    for s in structs:
        th = F.fit(s, pooled)
        fit[s] = th
        print(f"{s:11} {F.STRUCTS[s] + 1:>3} {F.nll(s, th, pooled):>11.4f}")
    print(f"chance: {ch:.4f}\n")

    fp = {s: F.nll(s, fit[s], pooled) for s in structs}
    print("== Pre-registered checks ==")
    d1 = fp["rank1"] - fp["full"]
    print(f"H1 low-rank sufficiency: rank1 {fp['rank1']:.4f} vs full {fp['full']:.4f} "
          f"(gap {d1:+.4f}; PASS <= 0.02) -> {'PASS' if d1 <= 0.02 else 'FAIL'}")
    d3 = fp["diagonal"] - fp["rank1"]
    print(f"H3 rank1 beats diagonal: diagonal {fp['diagonal']:.4f} vs rank1 {fp['rank1']:.4f} "
          f"(rank1 better by {d3:+.4f}) -> {'PASS' if d3 > 1e-3 else 'FAIL/tie'}")
    d4 = fp["rank1"] - fp["rank2"]
    print(f"H4 low not full rank: rank2 {fp['rank2']:.4f} vs rank1 {fp['rank1']:.4f} "
          f"(rank2 better by {d4:+.4f}) -> {'PASS' if d4 < 0.02 else 'FAIL'}")

    # ---- cross-country transfer (H2): fit half the countries, predict the other half ----
    print("\n== Cross-country transfer (rank1): split 19 countries ==")
    half = len(countries) // 2
    A, B = countries[:half], countries[half:]
    pA = F._zscale(problems_for(Xprob, cnt, A))[0]
    pB = F._zscale(problems_for(Xprob, cnt, B))[0]
    chA, chB = F.uniform_nll(pA), F.uniform_nll(pB)
    thA, thB = F.fit("rank1", pA), F.fit("rank1", pB)
    natA, natB = F.nll("rank1", thA, pA), F.nll("rank1", thB, pB)
    tAB = F.nll("rank1", F.refit_T("rank1", thA, pB), pB)
    tBA = F.nll("rank1", F.refit_T("rank1", thB, pA), pA)
    gc = lambda ch, nat, tr: max(0.0, (ch - tr) / (ch - nat)) if ch > nat else 0.0
    print(f"  group A->B: {100 * gc(chB, natB, tAB):.0f}% gap-closed   "
          f"B->A: {100 * gc(chA, natA, tBA):.0f}%")

    # ---- gain/loss diagnostic (raw features do NOT flip in the loss domain) ----
    print("\n== Gain vs loss diagnostic (rank1) ==")
    gq = [q for q in KT if KT[q][2] == "gain"]
    lq = [q for q in KT if KT[q][2] == "loss"]
    pg = F._zscale(problems_for(Xprob, cnt, countries, gq))[0]
    pl = F._zscale(problems_for(Xprob, cnt, countries, lq))[0]
    chg, chl = F.uniform_nll(pg), F.uniform_nll(pl)
    thg, thl = F.fit("rank1", pg), F.fit("rank1", pl)
    natg, natl = F.nll("rank1", thg, pg), F.nll("rank1", thl, pl)
    tgl = F.nll("rank1", F.refit_T("rank1", thg, pl), pl)
    print(f"  gain native {natg:.4f} (chance {chg:.4f}); loss native {natl:.4f} (chance {chl:.4f})")
    print(f"  gain->loss transfer: {100 * gc(chl, natl, tgl):.0f}% gap-closed "
          f"(low => raw features miss the reflection sign-flip; the known loss-domain caveat)")


if __name__ == "__main__":
    main()
