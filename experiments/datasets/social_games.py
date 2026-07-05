#!/usr/bin/env python3
"""Social-preference games leg — held-out leg #1 of prereg-sigma-v1.

A *social* domain the constrained-Sigma fuzz never saw (it used lotteries + level-k
games). Data: Fraser & Nettle ultimatum game (stake=10), the dataset named in the
pre-registration. Two roles give discrete social choices:

  responder -- accept vs reject an offer o: accept -> payoffs (o, 10-o); reject -> (0,0).
               The acceptance curve (reconstructed from each subject's minimum
               acceptable offer) is driven by disadvantageous-inequality aversion.
  proposer  -- choose an offer o in {0..10}: proposer gets (10-o, o). 106 subjects,
               one allocation choice each -> a genuinely multi-dimensional social
               choice (own payoff vs advantageous inequality vs fairness).

Social feature space (K=5, analogous to the fuzz's risk features):
  [ own, other, disadvantageous_inequality, advantageous_inequality, efficiency ].
Cost = Mahalanobis distance from each option to the FAIR-SPLIT reference (5,5) under
Sigma^-1 = L L^T; choice = softmax(-cost/T). We reuse the fuzz's Sigma structures and
ask the pre-registered questions:

  H1  rank-1 fits within 0.02 NLL of full            (low-rank sufficiency)
  H3  rank-1 beats diagonal at equal params          (off-diagonal social structure real)
  H4  rank-2 improves transfer over rank-1 by < 5pt  (low, not full, rank)
  (H2 transfer = role-transfer proposer<->responder + condition generalization.)

    python social_games.py
"""
from __future__ import annotations

import csv
import os

import numpy as np
from scipy.optimize import minimize

from constrained_sigma_fuzz import STRUCTS, make_L

HERE = os.path.dirname(os.path.abspath(__file__))
FN1 = os.path.join(HERE, "raw_social", "fn1.csv")
STAKE = 10
FAIR = (STAKE / 2, STAKE / 2)  # Fehr-Schmidt equality reference

# structures we score (core H1/H3/H4 set + local/group structure)
CORE = ["isotropic", "diagonal", "rank1", "rank2", "banded", "block", "full"]


def _feat(own, other):
    return [own, other, max(other - own, 0.0), max(own - other, 0.0), own + other]


def load(condition=None):
    rows = list(csv.DictReader(open(FN1, encoding="utf-8-sig")))
    if condition is not None:
        rows = [r for r in rows if r.get("Condition.Name") == condition]
    mao = [int(float(r["LowestAcceptable"])) for r in rows if r["LowestAcceptable"] != ""]
    offers = [int(float(r["ProposedAmount"])) for r in rows if r["ProposedAmount"] != ""]
    return mao, offers


def responder_problems(mao):
    """Per offer o: [accept, reject] with aggregate P from the MAO thresholds."""
    n = len(mao)
    probs = []
    for o in range(STAKE + 1):
        pacc = sum(1 for m in mao if o >= m) / n
        X = np.array([_feat(o, STAKE - o), _feat(0, 0)], float)  # accept, reject
        obs = np.array([pacc, 1 - pacc])
        probs.append((X, obs, float(n)))
    return probs


def proposer_problems(offers):
    """Per subject: one-hot choice among the 11 offers (proposer gets 10-o, o)."""
    X = np.array([_feat(STAKE - o, o) for o in range(STAKE + 1)], float)  # 11 options
    probs = []
    for o in offers:
        obs = np.zeros(STAKE + 1)
        obs[o] = 1.0
        probs.append((X, obs, 1.0))
    return probs


def zscale(*problem_sets):
    allX = np.vstack([X for ps in problem_sets for X, _, _ in ps])
    mu, sd = allX.mean(0), allX.std(0) + 1e-9
    scaled = [[((X - mu) / sd, obs, n) for X, obs, n in ps] for ps in problem_sets]
    ideal = (np.array(_feat(*FAIR)) - mu) / sd
    return scaled, ideal


def nll(struct, theta, problems, ideal):
    nparam = STRUCTS[struct]
    Pinv, _ = make_L(struct, theta[:nparam])
    T = np.abs(theta[nparam]) + 1e-6
    tot = w = 0.0
    for X, obs, n in problems:
        d = X - ideal                                   # (k, K)
        c = np.sqrt(np.maximum(np.einsum("pi,ij,pj->p", d, Pinv, d), 0))
        z = -c / T
        z -= z.max()
        e = np.exp(z)
        p = np.clip(e / e.sum(), 1e-6, 1)
        tot += -n * np.sum(obs * np.log(p))
        w += n
    return tot / w


def fit(struct, problems, ideal, seed=0):
    np1 = STRUCTS[struct]
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(4):
        x0 = np.r_[rng.uniform(0.3, 1.0, np1), [1.0]]
        r = minimize(lambda th: nll(struct, th, problems, ideal), x0, method="Nelder-Mead",
                     options={"maxiter": 8000, "xatol": 1e-4, "fatol": 1e-6})
        if best is None or r.fun < best.fun:
            best = r
    return best.x


def refit_T(struct, theta, problems, ideal):
    np1 = STRUCTS[struct]
    r = minimize(lambda t: nll(struct, np.r_[theta[:np1], np.abs(t)], problems, ideal),
                 [abs(theta[np1])], method="Nelder-Mead", options={"maxiter": 3000})
    return np.r_[theta[:np1], np.abs(r.x)]


def chance(problems):
    tot = w = 0.0
    for _, obs, n in problems:
        tot += -n * np.sum(obs * np.log(1.0 / len(obs)))
        w += n
    return tot / w


def gap_closed(ch, native, transfer):
    return max(0.0, (ch - transfer) / (ch - native)) if ch > native else 0.0


def main():
    mao, offers = load()
    (resp, prop), ideal = zscale(responder_problems(mao), proposer_problems(offers))
    ch_r, ch_p = chance(resp), chance(prop)
    print(f"Fraser-Nettle ultimatum: {len(mao)} responders, {len(offers)} proposers | "
          f"K=5 social features | ideal=fair split {FAIR}")
    print(f"chance NLL: responder {ch_r:.4f}  proposer {ch_p:.4f}\n")

    print(f"{'structure':11} {'#p':>3} {'resp fit':>9} {'prop fit':>9} "
          f"{'p->r':>7} {'r->p':>7} {'role-transfer%':>14}")
    fits = {}
    for s in CORE:
        th_r = fit(s, resp, ideal)
        th_p = fit(s, prop, ideal)
        fits[s] = (th_r, th_p)
        nat_r = nll(s, th_r, resp, ideal)
        nat_p = nll(s, th_p, prop, ideal)
        tr_pr = nll(s, refit_T(s, th_p, resp, ideal), resp, ideal)   # proposer metric -> responder
        tr_rp = nll(s, refit_T(s, th_r, prop, ideal), prop, ideal)   # responder metric -> proposer
        trpct = 100 * (gap_closed(ch_r, nat_r, tr_pr) + gap_closed(ch_p, nat_p, tr_rp)) / 2
        print(f"{s:11} {STRUCTS[s] + 1:>3} {nat_r:>9.4f} {nat_p:>9.4f} "
              f"{tr_pr:>7.4f} {tr_rp:>7.4f} {trpct:>13.0f}%")

    # ----- pre-registered H1/H3/H4 on the RESPONDER task -----
    # NOTE: the proposer options all satisfy own+other=STAKE (constant efficiency) -> they
    # lie on a 1-D line, so every Sigma structure of rank>=1 ties there (a consistency check
    # for low-rank, not a test of H3). The responder task (accept efficiency=STAKE vs reject
    # efficiency=0, with own/inequality variation) is genuinely multi-dimensional.
    print("\n== Pre-registered checks (responder task; genuinely multi-dimensional) ==")
    fr = {s: nll(s, fits[s][0], resp, ideal) for s in CORE}
    d1 = fr["rank1"] - fr["full"]
    print(f"H1 low-rank sufficiency: rank1 {fr['rank1']:.4f} vs full {fr['full']:.4f} "
          f"(gap {d1:+.4f}; PASS if <= 0.02) -> {'PASS' if d1 <= 0.02 else 'FAIL'}")
    d3 = fr["diagonal"] - fr["rank1"]
    print(f"H3 rank1 beats diagonal: diagonal {fr['diagonal']:.4f} vs rank1 {fr['rank1']:.4f} "
          f"(rank1 better by {d3:+.4f}) -> {'PASS' if d3 > 1e-3 else 'FAIL/tie'}")
    d4 = fr["rank1"] - fr["rank2"]
    print(f"H4 low not full rank: rank2 {fr['rank2']:.4f} vs rank1 {fr['rank1']:.4f} "
          f"(rank2 better by {d4:+.4f}; small => low-rank) -> {'PASS' if d4 < 0.02 else 'FAIL'}")
    print(f"   (proposer task is 1-D: all structures tie at {nll('rank1', fits['rank1'][1], prop, ideal):.4f} "
          f"-> consistent with low-rank, uninformative for H3.)")

    # ----- condition generalization (Breakfast <-> No Breakfast), responder -----
    print("\n== Condition generalization (responder, rank1): Breakfast <-> No Breakfast ==")
    mb, _ = load("Breakfast")
    mn, _ = load("No Breakfast")
    (rb, rn), idl = zscale(responder_problems(mb), responder_problems(mn))
    chb, chn = chance(rb), chance(rn)
    thb = fit("rank1", rb, idl)
    thn = fit("rank1", rn, idl)
    t_bn = nll("rank1", refit_T("rank1", thb, rn, idl), rn, idl)
    t_nb = nll("rank1", refit_T("rank1", thn, rb, idl), rb, idl)
    print(f"  Breakfast->NoBreakfast: {100 * gap_closed(chn, nll('rank1', thn, rn, idl), t_bn):.0f}% gap-closed")
    print(f"  NoBreakfast->Breakfast: {100 * gap_closed(chb, nll('rank1', thb, rb, idl), t_nb):.0f}% gap-closed")


if __name__ == "__main__":
    main()
