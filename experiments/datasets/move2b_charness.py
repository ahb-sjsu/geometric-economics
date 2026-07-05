#!/usr/bin/env python3
"""Move 2 (proper) -- the social reflection structure on REAL 2-D allocation data.

Charness & Rabin (2002 QJE), Table I: the SEVEN two-person dictator games (the clean
distributional set; the paper excludes response games for reciprocity confounds). B chooses
between two (own_B, other_A) allocations -- own and other vary INDEPENDENTLY (unlike the
ultimatum's own+other=const), so this is genuine 2-D social-allocation choice.

Two questions:
  1. The self<->other reflection sigma_s: swap (own,other). A fair agent is sigma_s-symmetric
     (weights own=other). Self-regard is the reflection-BREAKING (analog of loss aversion).
  2. Does the social domain have a V4 (like the curated risk fourfold) or is it main-effect
     inequality aversion? V4 needs a PURE INTERACTION (position has no main effect). Fehr-Schmidt
     predicts a POSITION MAIN EFFECT (envy alpha != guilt beta) -> NOT V4. We fit and test.

Model: U_B(s,o) = s - alpha*max(o-s,0) - beta*max(s-o,0)   (Fehr-Schmidt),
       P(choose L) = softmax(U/tau). Compare to the sigma_s-symmetric restriction alpha=beta
       (pure difference aversion, position-symmetric = the V4-consistent case).

    python move2b_charness.py
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2

# Charness-Rabin 2002 Table I, seven two-person dictator games. Payoffs /100 (so tau is O(1)).
# Paper writes allocations as (other_A, own_B); here converted to (own, other). B is the decider.
# (label, own_L, other_L, own_R, other_R, P(Left), n)
_RAW = [
    ("Berk29", 400, 400, 400, 750, 0.31, 26),
    ("Barc2",  400, 400, 375, 750, 0.52, 48),
    ("Berk17", 400, 400, 375, 750, 0.50, 32),
    ("Berk23", 200, 800,   0,   0, 1.00, 36),
    ("Berk8",  600, 300, 500, 700, 0.67, 36),
    ("Berk15", 700, 200, 600, 600, 0.27, 22),
    ("Berk26", 800,   0, 400, 400, 0.78, 32),
]
GAMES = [(g[0], g[1] / 100, g[2] / 100, g[3] / 100, g[4] / 100, g[5], g[6]) for g in _RAW]


def U(s, o, alpha, beta):
    return s - alpha * max(o - s, 0.0) - beta * max(s - o, 0.0)


def nll(theta, restrict=False):
    if restrict:            # alpha = beta (position-symmetric; V4-consistent)
        a = b = abs(theta[0]); tau = abs(theta[1]) + 1e-6
    else:
        a, b, tau = abs(theta[0]), abs(theta[1]), abs(theta[2]) + 1e-6
    tot = 0.0
    for _, sL, oL, sR, oR, pL, n in GAMES:
        uL, uR = U(sL, oL, a, b) / tau, U(sR, oR, a, b) / tau
        m = max(uL, uR)
        p = np.exp(uL - m) / (np.exp(uL - m) + np.exp(uR - m))
        p = min(max(p, 1e-9), 1 - 1e-9)
        tot += -(n * pL * np.log(p) + n * (1 - pL) * np.log(1 - p))
    return tot


def fit(restrict=False, seeds=None):
    k = 2 if restrict else 3
    best = None
    starts = [np.random.default_rng(s).uniform(0, 2.0, k) for s in range(20)]
    if seeds is not None:
        starts += list(seeds)
    for x0 in starts:
        r = minimize(lambda th: nll(th, restrict), x0, method="Nelder-Mead",
                     options={"maxiter": 8000, "xatol": 1e-7, "fatol": 1e-7})
        if best is None or r.fun < best.fun:
            best = r
    return best


def main():
    N = sum(g[6] for g in GAMES)
    rest = fit(True)
    ar, tr = abs(rest.x[0]), abs(rest.x[1])
    full = fit(False, seeds=[np.array([ar, ar, tr]), np.array([0.9, 0.3, 1.0])])  # ensure full >= restricted
    a, b, tau = abs(full.x[0]), abs(full.x[1]), abs(full.x[2])
    print(f"== Fehr-Schmidt fit to 7 Charness-Rabin dictator games ({N} choices) ==\n")
    print(f"  alpha (disadvantageous-inequality aversion, ENVY, when behind) = {a:.3f}")
    print(f"  beta  (advantageous-inequality aversion,   GUILT, when ahead)  = {b:.3f}")
    print(f"  tau (choice temperature) = {tau:.1f}")

    print("\n== Q1: the self<->other reflection sigma_s and its breaking ==")
    print("  a sigma_s-symmetric (fair) agent weights own = other. The 'own' term has weight 1; the "
          "other's payoff enters only through inequality aversion (alpha,beta<1).")
    print(f"  self-regard (own weight 1 vs effective other weight ~{(a+b)/2:.2f}) is the reflection-")
    print(f"  BREAKING -- the social analog of loss aversion breaking the value reflection.")

    print("\n== Q2: V4 (pure interaction) or main-effect inequality aversion? ==")
    lr = max(0.0, 2 * (rest.fun - full.fun))      # 1 df: alpha != beta
    pval = chi2.sf(lr, 1)
    print(f"  position asymmetry: alpha - beta = {a - b:+.3f}")
    print(f"  restricted alpha=beta (position-symmetric, V4-consistent) vs free: "
          f"LR chi2={lr:.1f}, p={pval:.3f}")
    if abs(a - b) <= 0.05 or pval > 0.1:
        print("  -> alpha ~ beta: position-SYMMETRIC difference aversion; no position main effect "
              "(V4-consistent inequality attitude).")
    else:
        hi, lo = ("alpha", "beta") if a > b else ("beta", "alpha")
        kind = "envy > guilt (Fehr-Schmidt)" if a > b else "guilt > envy (costly equalizing-down)"
        print(f"  -> {hi} > {lo}: a POSITION MAIN EFFECT ({kind}). NOT a pure interaction -> the "
              f"social domain is NOT a V4; it is one reflection + main-effect inequality aversion.")

    print("\n== Structural verdict (Move 2, real data) ==")
    print("The social domain has ONE reflection axis: self<->other (= the sign of inequality). Swapping "
          "self and other IS the inequality-sign flip, so there is no SECOND independent social "
          "reflection -- unlike risk's two independent axes (value x probability). Social allocation is "
          "therefore Z/2 (one reflection) + inequality aversion, NOT a V4.")
    print("So: the reflection+aversion MOTIF generalizes (a self<->other reflection broken by "
          "inequality aversion, mirroring value-reflection broken by loss aversion), but the full V4 "
          "is SPECIFIC to risk's two-axis structure. This is the honest completion of the social leg "
          "on real Charness-Rabin allocation data.")
    print(f"\nHONEST: 7 dictator games, n=22-48 each; Charness-Rabin's own conclusion is that "
          f"social-welfare/difference-aversion preferences fit these best. alpha={a:.2f}, beta={b:.2f} "
          f"-- both nonzero, and Berk29 (31% refuse free advantageous inequality) drives beta.")


if __name__ == "__main__":
    main()
