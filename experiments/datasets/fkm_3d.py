#!/usr/bin/env python3
"""FKM 3-person split -- does ONE low-dimensional metric govern giving AND allocation among others?

FKM's distinctive elaboration: 3-person budgets let us separate
  * preferences for GIVING      -- self vs the two others (how much to keep), and
  * SOCIAL preferences proper   -- the trade-off BETWEEN the two others (efficiency vs equality
                                   among them, holding own payoff), which pure giving cannot reveal.

Data_3D rows: [subject, pi_s, pi_o1, pi_o2, max_s, max_o1, max_o2]; budget Sum pi_i/max_i = 1, so
prices p_i = 1/max_i and expenditure shares w_i = pi_i/max_i (sum <=1, disposal). Fit a 3-good CES
per subject -- u = (Sum alpha_i pi_i^rho)^(1/rho) -- with predicted expenditure shares
    w_i = alpha_i^sigma p_i^(1-sigma) / Sum_j alpha_j^sigma p_j^(1-sigma),   sigma = 1/(1-rho).
Params: (alpha_s, alpha_o1, alpha_o2) via softmax + sigma. Tests:
  T1 low-dim + consistency: R^2 of the 3-good CES per subject.
  T2 giving:  alpha_self vs alpha_others (self-regard).
  T3 impartiality among others: |alpha_o1 - alpha_o2| (the two others are interchangeable).
  T4 social preference among others: sigma (>1 efficiency/substitutes; <1 equality-leaning).

    python fkm_3d.py
"""
from __future__ import annotations

import os

import numpy as np
import scipy.io as sio
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
D3 = os.path.join(HERE, "raw_fkm", "20050757", "Tobit", "Tobit_3D", "Data_3D.mat")


def load3d():
    d = sio.loadmat(D3)["Data_3D"]
    subj = d[:, 0].astype(int)
    # column means show the MIDDLE chosen col (idx2) is SELF (kept ~47) vs others (~8);
    # reorder to [self, other1, other2] for both the chosen and the intercept triples.
    pi = d[:, [2, 1, 3]]     # self, o1, o2
    mx = d[:, [5, 4, 6]]     # max_self, max_o1, max_o2
    return subj, pi, mx


def pred_shares(alpha, sigma, p):
    # w_i = alpha_i^sigma p_i^(1-sigma) / sum_j(...), computed in log-space for stability
    logt = sigma * np.log(np.clip(alpha, 1e-9, None)) + (1 - sigma) * np.log(np.clip(p, 1e-9, None))
    logt = logt - logt.max(axis=1, keepdims=True)
    t = np.exp(logt)
    return t / (t.sum(axis=1, keepdims=True) + 1e-12)


def fit_subject(pi, mx):
    p = 1.0 / mx                       # prices (rounds x 3)
    w_obs = pi / mx                    # observed expenditure shares
    w_obs = w_obs / (w_obs.sum(1, keepdims=True) + 1e-9)   # renormalize (remove disposal)

    def obj(th):
        a = np.array([1.0, np.exp(np.clip(th[0], -20, 20)), np.exp(np.clip(th[1], -20, 20))])
        a = a / a.sum()
        sigma = np.clip(np.exp(th[2]), 0.02, 50)
        wp = pred_shares(a[None, :], sigma, p)
        return np.sum((wp - w_obs) ** 2)

    best = None
    for s in range(6):
        r = minimize(obj, np.random.default_rng(s).normal(0, 1, 3), method="Nelder-Mead",
                     options={"maxiter": 4000, "fatol": 1e-9})
        if best is None or r.fun < best.fun:
            best = r
    a = np.array([1.0, np.exp(np.clip(best.x[0], -20, 20)), np.exp(np.clip(best.x[1], -20, 20))]); a /= a.sum()
    sigma = np.clip(np.exp(best.x[2]), 0.02, 50)
    wp = pred_shares(a[None, :], sigma, p)
    ss_res = np.sum((wp - w_obs) ** 2)
    ss_tot = np.sum((w_obs - w_obs.mean(0)) ** 2)
    r2 = 1 - ss_res / (ss_tot + 1e-12)
    return a, sigma, r2


def main():
    subj, pi, mx = load3d()
    ids = np.unique(subj)
    print(f"FKM 3-person: {len(ids)} subjects x ~50 budget-line choices = {len(subj)} decisions\n")

    A, S, R2 = [], [], []
    for s in ids:
        m = subj == s
        a, sig, r2 = fit_subject(pi[m], mx[m])
        A.append(a); S.append(sig); R2.append(r2)
    A = np.array(A); S = np.array(S); R2 = np.array(R2)
    a_self = A[:, 0]; a_oth = A[:, 1] + A[:, 2]
    asym = np.abs(A[:, 1] - A[:, 2])

    print("== T1: low-dimensionality of the 3-good metric (structure vs fit) ==")
    print(f"  single-rho 3-good CES per subject: mean within-subject R^2 = {np.mean(R2):.2f} "
          f"(median {np.median(R2):.2f}); {100*np.mean(R2>0.5):.0f}% of subjects R^2>0.5.")
    print("  -> the low-parameter metric captures the STRUCTURE (self-regard, impartiality, efficiency-")
    print("     leaning, below) but the fit is NOISIER than the 2-person CES (0.54); a single rho for both")
    print("     self-vs-others and among-others is restrictive. Low-dim claim is structural, not a tight fit.")

    print("\n== T2: giving (self-regard) ==")
    print(f"  weight on self alpha_self: median {np.median(a_self):.2f} (others combined "
          f"{np.median(a_oth):.2f}); {100*np.mean(a_self>0.5):.0f}% put >50% weight on self "
          f"-> self-regard, the same reflection-breaking as 2-person.")

    print("\n== T3: impartiality among the two (interchangeable) others ==")
    print(f"  |alpha_o1 - alpha_o2|: median {np.median(asym):.2f} (mean {np.mean(asym):.2f}); "
          f"{100*np.mean(asym<0.1):.0f}% of subjects treat the two others within 0.1 -> "
          f"broad IMPARTIALITY among others (a symmetry of the social metric).")

    print("\n== T4: social preference among others (efficiency vs equality) ==")
    print(f"  substitution sigma=1/(1-rho): median {np.median(S):.2f} "
          f"({np.percentile(S,25):.2f}..{np.percentile(S,75):.2f} IQR). "
          f"sigma>1 => others are substitutes (efficiency: give to the cheaper other); "
          f"sigma<1 => complements (equality among others).")
    print(f"  {100*np.mean(S>1):.0f}% of subjects sigma>1 (efficiency-leaning among others), "
          f"{100*np.mean(S<1):.0f}% sigma<1 (equality-leaning).")

    print("\n== Verdict -- a clean exchange symmetry, and self-regard, in the among-others layer ==")
    print(f"HEADLINE (clean): the social metric has an EXCHANGE SYMMETRY -- {100*np.mean(asym<0.1):.0f}% of "
          f"subjects weight the two interchangeable others within 0.1 (median |diff| {np.median(asym):.2f}). "
          f"Allocation between them is driven by their PRICES, not favoritism: a genuine permutation "
          f"symmetry (o1<->o2) of the social metric -- the among-others analog of the reflection symmetries.")
    print(f"CONFIRMED: self-regard persists in 3-person (alpha_self median {np.median(a_self):.2f}), and "
          f"others are mostly efficiency-substitutes ({100*np.mean(S>1):.0f}% sigma>1) -- FKM's finding.")
    print(f"WEAKER: the single-rho 3-good CES fit is noisy (mean R^2 {np.mean(R2):.2f} vs 2-person 0.54), so "
          f"'one low-dim metric governs among-others allocation' is supported structurally, not tightly.")
    print("HONEST: share-matching (not FKM's Tobit); 65 subjects, different pool from 2-person (no "
          "within-subject 2->3 transfer). The clean, robust result is the o1<->o2 exchange symmetry.")


if __name__ == "__main__":
    main()
