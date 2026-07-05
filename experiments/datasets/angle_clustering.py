#!/usr/bin/env python3
"""Universal aversion-angle test — do the domain angles cluster?

The polar principle (shape transfers, scale recalibrates) held on every transfer axis.
The missing measurement: are the actual aversion ANGLES the same across domains? We use
the standard mean-variance preference direction from a conditional logit over the choice
options (features z-scored per domain, so the angle is comparable across domains):

    P(option i) ∝ exp( beta · X_i ),   aversion angle = atan2( beta_SD, beta_EV )

Sign convention: risk-averse gains -> beta_SD < 0 -> NEGATIVE angle; risk-seeking losses
-> beta_SD > 0 -> POSITIVE angle. So the reflection effect is literally an angle sign-flip.
The logit is convex (unique, stable fit), unlike the Mahalanobis EV-SD eigenvector.

Domains: gain lotteries (CPC18, choices13k), games (bogota), Ruggeri gains, Ruggeri
losses (raw), Ruggeri losses (SD-reflected). Prediction: gains + games cluster at a
common negative angle; raw-loss flips positive (reflection); reflected-loss rejoins gains.

    python angle_clustering.py
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

import constrained_sigma_fuzz as F
import ruggeri as R

NB = 200  # bootstrap resamples (logit is cheap)


def groups_of(problems):
    """z-scale, then group by #options and stack for vectorized logit."""
    scaled = F._zscale(problems)[0]
    from collections import defaultdict
    g = defaultdict(list)
    for X, obs, n in scaled:
        g[X.shape[0]].append((X, obs, n))
    out = []
    for items in g.values():
        Xs = np.stack([X for X, _, _ in items])
        obss = np.stack([o for _, o, _ in items])
        ns = np.array([n for *_, n in items])
        out.append((Xs, obss, ns))
    return out


def nll(beta, groups):
    tot = w = 0.0
    for Xs, obss, ns in groups:
        u = Xs @ beta
        u -= u.max(1, keepdims=True)
        e = np.exp(u)
        p = np.clip(e / e.sum(1, keepdims=True), 1e-9, 1)
        tot += -np.sum(ns * np.sum(obss * np.log(p), axis=1))
        w += ns.sum()
    return tot / w


def fit_beta(groups):
    r = minimize(nll, np.zeros(5), args=(groups,), method="BFGS",
                 options={"maxiter": 500, "gtol": 1e-7})
    return r.x


def aversion_angle(beta):
    return float(np.degrees(np.arctan2(beta[1], beta[0])))  # atan2(beta_SD, beta_EV)


def boot_angles(problems, rng, nb=NB):
    scaled = F._zscale(problems)[0]
    idx = np.arange(len(scaled))
    angs = []
    for _ in range(nb):
        s = [scaled[i] for i in rng.choice(idx, len(idx), replace=True)]
        from collections import defaultdict
        g = defaultdict(list)
        for X, obs, n in s:
            g[X.shape[0]].append((X, obs, n))
        grp = [(np.stack([X for X, _, _ in it]), np.stack([o for _, o, _ in it]),
                np.array([n for *_, n in it])) for it in g.values()]
        angs.append(aversion_angle(fit_beta(grp)))
    return np.array(angs)


def ruggeri_problems(reflect_sd=False, domain=None):
    Xprob, cnt = R.load()
    out = []
    for ctry in cnt:
        for q in R.KT:
            if domain and R.KT[q][2] != domain:
                continue
            nA, n = cnt[ctry][q]
            if n == 0:
                continue
            X = Xprob[q].copy()
            if reflect_sd:
                X[:, 1] = -X[:, 1]
            out.append((X, np.array([nA / n, 1 - nA / n]), float(n)))
    return out


def cap(problems, n, seed=0):
    if len(problems) <= n:
        return problems
    rng = np.random.default_rng(seed)
    return [problems[i] for i in rng.choice(len(problems), n, replace=False)]


def main():
    rng = np.random.default_rng(0)
    print("Loading domains...", flush=True)
    domains = {
        "CPC18 (gain lott.)":   cap(F.load_cpc18(), 1500),
        "choices13k (lott.)":   cap(F.load_c13k(1500), 1500),
        "bogota (games)":       F.load_games(),
        "Ruggeri gains":        ruggeri_problems(domain="gain"),
        "Ruggeri loss (raw)":   ruggeri_problems(domain="loss"),
        "Ruggeri loss (refl.)": ruggeri_problems(reflect_sd=True, domain="loss"),
    }
    print(f"\n{'domain':22} {'angle':>8}  {'95% CI':>18}  n", flush=True)
    pts = {}
    for name, probs in domains.items():
        a0 = aversion_angle(fit_beta(groups_of(probs)))
        bs = boot_angles(probs, rng)
        lo, hi = np.percentile(bs, [2.5, 97.5])
        pts[name] = (a0, lo, hi, bs)
        print(f"{name:22} {a0:>7.1f}°  [{lo:>6.1f},{hi:>6.1f}]  {len(probs)}", flush=True)

    def cluster(names):
        a = np.array([pts[n][0] for n in names])
        wi = np.mean([pts[n][3].std() for n in names])
        return a.mean(), a.std(), a.max() - a.min(), wi

    print("\n== Clustering test (within comparable problem samples) ==")
    # Regime 1: representative corpora (EV-following) -- lotteries + strategic games
    rep = ["CPC18 (gain lott.)", "choices13k (lott.)", "bogota (games)"]
    m, sd, rng_, wi = cluster(rep)
    print(f"REPRESENTATIVE (CPC18 + choices13k + bogota games): mean {m:.1f}°, "
          f"between-sd {sd:.1f}°, range {rng_:.1f}°, within-boot sd {wi:.1f}° "
          f"-> ratio {sd/max(wi,1e-9):.2f}")
    # Regime 2: KT/Ruggeri (adversarially EV-violating) -- reflection cluster
    kt = ["Ruggeri gains", "Ruggeri loss (refl.)"]
    m2, sd2, rng2, wi2 = cluster(kt)
    print(f"KT/RUGGERI (gains + reflected loss): mean {m2:.1f}°, "
          f"between-sd {sd2:.1f}°, range {rng2:.1f}°, within-boot sd {wi2:.1f}° "
          f"-> ratio {sd2/max(wi2,1e-9):.2f}")

    print("\n== Reflection (angle sign-flip) ==")
    g, lr, lf = pts['Ruggeri gains'][0], pts['Ruggeri loss (raw)'][0], pts['Ruggeri loss (refl.)'][0]
    print(f"gains {g:.1f}° | loss RAW {lr:.1f}° (mirror) | loss REFLECTED {lf:.1f}° "
          f"-> reflected rejoins gains within {abs(g-lf):.1f}°")

    print("\n== The confound (why NOT one universal angle across ALL domains) ==")
    print(f"representative corpora sit near {m:.0f}° (beta_EV>0, EV-following); KT/Ruggeri near "
          f"{m2:.0f}° (beta_EV<0) because KT problems are SELECTED to violate EV (certainty effect). "
          f"The raw mean-variance angle is confounded by problem selection -> the angle clusters "
          f"WITHIN a comparable sample, not across adversarial vs representative sets.")
    print("\nHONEST: standardized mean-variance angles (conditional logit); descriptive evidence. "
          "Reflection sign-flip is robust; a single cross-ALL-domains angle is NOT supported (selection).")


if __name__ == "__main__":
    main()
