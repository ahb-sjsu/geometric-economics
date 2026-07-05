#!/usr/bin/env python3
"""Reflection-encoding fuzz — find the encoding that makes ONE metric span gain & loss.

The Ruggeri leg showed the raw geometric encoding fails on the reflection effect:
a metric fit on gains does not transfer to losses (gain->loss transfer 0%), because
risk-aversion flips to risk-seeking under losses. eris-econ hand-coded a domain flip
of d5/d9. Here we DISCOVER it instead: the geometric-native mechanism for reflection
is the *reference/ideal*, not the features. In gains the ideal has LOW SD (the safe
option is closest); under losses the ideal should have HIGH SD (the gamble is closest).

We fuzz over WHICH coordinate-ideals flip in the loss domain (subsets of
{SD, skew, worst, pfav}; EV never flips — more money is always better) and score each
encoding by whether one shared low-rank metric spans both domains (gain<->loss transfer).
Baseline (no flip) = the raw encoding = 0% transfer. The winner is the pre-registerable
reflection encoding.

    python reflection_fuzz.py
"""
from __future__ import annotations

import itertools
import os

import numpy as np
from scipy.optimize import minimize

import constrained_sigma_fuzz as F
from ruggeri import KT, load, problems_for

HERE = os.path.dirname(os.path.abspath(__file__))
FLIPPABLE = [1, 2, 3, 4]  # indices into [EV, SD, skew, worst, pfav]; EV (0) never flips
NAMES = ["EV", "SD", "skew", "worst", "pfav"]
STRUCT = "rank2"  # the Ruggeri sweet-spot structure


def build(structflip):
    """Return (X, obs, n, is_loss) arrays over all country x problem cells, z-scored."""
    Xprob, cnt = load()
    countries = sorted(cnt)
    probs, isloss = [], []
    for ctry in countries:
        for q in KT:
            nA, n = cnt[ctry][q]
            if n == 0:
                continue
            probs.append((Xprob[q], np.array([nA / n, 1 - nA / n]), float(n)))
            isloss.append(KT[q][2] == "loss")
    scaled, _ = F._zscale(probs)
    X = np.stack([x for x, _, _ in scaled])      # (M, 2, 5)
    obs = np.stack([o for _, o, _ in scaled])    # (M, 2)
    ns = np.array([n for *_, n in scaled])       # (M,)
    return X, obs, ns, np.array(isloss)


def ideal_for(X, is_loss, flip):
    """Domain-aware ideal per problem. Gain: EV/skew/worst/pfav max, SD min.
    Loss: coords in `flip` take the OPPOSITE extreme (reflection)."""
    hi = X.max(1)              # (M, K) max over options
    lo = X.min(1)
    ideal = hi.copy()
    ideal[:, 1] = lo[:, 1]     # SD: min is ideal in gains (risk-averse)
    for c in flip:
        # flip this coordinate's ideal in the LOSS rows
        opp = lo[:, c] if c != 1 else hi[:, c]     # non-SD flip -> min; SD flip -> max
        ideal[is_loss, c] = opp[is_loss]
    return ideal


def nll(struct, theta, X, obs, ns, ideal):
    nparam = F.STRUCTS[struct]
    Pinv, _ = F.make_L(struct, theta[:nparam])
    T = np.abs(theta[nparam]) + 1e-6
    d = ideal[:, None, :] - X
    c = np.sqrt(np.maximum(np.einsum("mpi,ij,mpj->mp", d, Pinv, d), 0))
    z = -c / T
    z -= z.max(1, keepdims=True)
    e = np.exp(z)
    p = np.clip(e / e.sum(1, keepdims=True), 1e-6, 1)
    return -np.sum(ns * np.sum(obs * np.log(p), axis=1)) / ns.sum()


def fit(struct, X, obs, ns, ideal, seed=0):
    np1 = F.STRUCTS[struct]
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(4):
        x0 = np.r_[rng.uniform(0.3, 1.0, np1), [1.0]]
        r = minimize(lambda th: nll(struct, th, X, obs, ns, ideal), x0, method="Nelder-Mead",
                     options={"maxiter": 8000, "xatol": 1e-4, "fatol": 1e-6})
        if best is None or r.fun < best.fun:
            best = r
    return best.x


def refit_T(struct, theta, X, obs, ns, ideal):
    np1 = F.STRUCTS[struct]
    r = minimize(lambda t: nll(struct, np.r_[theta[:np1], np.abs(t)], X, obs, ns, ideal),
                 [abs(theta[np1])], method="Nelder-Mead", options={"maxiter": 3000})
    return np.r_[theta[:np1], np.abs(r.x)]


def score(struct, X, obs, ns, ideal, is_loss):
    g, l = ~is_loss, is_loss
    def sub(m):
        return X[m], obs[m], ns[m], ideal[m]
    chg = -np.sum(ns[g] * np.sum(obs[g] * np.log(0.5), 1)) / ns[g].sum()
    chl = -np.sum(ns[l] * np.sum(obs[l] * np.log(0.5), 1)) / ns[l].sum()
    thg = fit(struct, *sub(g))
    thl = fit(struct, *sub(l))
    natg = nll(struct, thg, *sub(g))
    natl = nll(struct, thl, *sub(l))
    tgl = nll(struct, refit_T(struct, thg, *sub(l)), *sub(l))   # gain metric -> loss
    tlg = nll(struct, refit_T(struct, thl, *sub(g)), *sub(g))   # loss metric -> gain
    gc = lambda ch, nat, tr: max(0.0, (ch - tr) / (ch - nat)) if ch > nat else 0.0
    return natg, natl, 100 * gc(chl, natl, tgl), 100 * gc(chg, natg, tlg)


def main():
    X, obs, ns, is_loss = build(None)
    print(f"Ruggeri reflection fuzz: {len(X)} cells ({is_loss.sum()} loss, {(~is_loss).sum()} gain), "
          f"structure={STRUCT}\n")
    print("flip (loss-domain ideal)     gain-fit  loss-fit  gain->loss  loss->gain")
    results = []
    # all subsets of the flippable coords
    subsets = []
    for r in range(len(FLIPPABLE) + 1):
        subsets += list(itertools.combinations(FLIPPABLE, r))
    for fl in subsets:
        ideal = ideal_for(X, is_loss, fl)
        natg, natl, tgl, tlg = score(STRUCT, X, obs, ns, ideal, is_loss)
        label = "+".join(NAMES[c] for c in fl) or "(none=raw)"
        results.append((label, fl, natg, natl, tgl, tlg))
        print(f"{label:28} {natg:>8.4f} {natl:>9.4f} {tgl:>10.0f}% {tlg:>10.0f}%")

    best = max(results, key=lambda r: (r[4] + r[5]) / 2)
    print(f"\nBest reflection encoding: flip {best[0]} -> "
          f"gain<->loss transfer {(best[4] + best[5]) / 2:.0f}% "
          f"(raw baseline was ~0%).")
    print("HONEST: this is a discovered encoding to PRE-REGISTER and re-test on a held-out "
          "loss corpus, not yet a confirmed result.")


if __name__ == "__main__":
    main()
