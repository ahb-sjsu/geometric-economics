#!/usr/bin/env python3
"""Efficient-coding test — is the aversion angle what an information-limited decider MUST use?

The clustering result showed the z-scored aversion angle is shared across comparable domains. The
question this test answers: is that a coincidence, or is the angle the *efficient code* for the
choice environment? Efficient coding (Barlow; Woodford; rational inattention) makes a sharp,
non-circular, falsifiable prediction:

    a capacity-limited decider normalizes its feature-sensitivity by the environment's variance.

So the RAW sensitivity to a feature, beta_raw_k, should scale as 1/sigma_k (adaptation), leaving a
CONSTANT intrinsic weight beta_z_k = beta_raw_k * sigma_k underneath. Equivalently: the z-scored
logit weight is the invariant; the raw behavior adapts to the local statistics.

Decisive test (within a single corpus, controlling for everything else): bin the problems into
sub-environments with DIFFERENT feature spread sigma_SD, and ask
    - does beta_raw_SD track 1/sigma_SD ?           (adaptation -> efficient coding)
    - is beta_z_SD (= beta_raw_SD * sigma_SD) constant across bins?  (the intrinsic invariant)
If yes, the shared angle is the efficient code, not a fitted coincidence. If beta_z_SD varies as much
as beta_raw_SD, normalization does no work and the angle is intrinsic preference (Shannon = vocabulary).

    python efficient_coding.py
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

import constrained_sigma_fuzz as F
import ruggeri as R


def _groups(scaled):
    from collections import defaultdict
    g = defaultdict(list)
    for X, obs, n in scaled:
        g[X.shape[0]].append((X, obs, n))
    return [(np.stack([X for X, _, _ in it]), np.stack([o for _, o, _ in it]),
             np.array([n for *_, n in it])) for it in g.values()]


def _nll(beta, groups):
    tot = w = 0.0
    for Xs, obss, ns in groups:
        u = Xs @ beta
        u -= u.max(1, keepdims=True)
        e = np.exp(u)
        p = np.clip(e / e.sum(1, keepdims=True), 1e-9, 1)
        tot += -np.sum(ns * np.sum(obss * np.log(p), 1))
        w += ns.sum()
    return tot / w


def analyze(problems):
    """Fit the z-scored logit; return intrinsic weights beta_z, raw sensitivities beta_raw, and sigma."""
    scaled, (mu, sd) = F._zscale(problems)
    r = minimize(_nll, np.zeros(5), args=(_groups(scaled),), method="BFGS",
                 options={"maxiter": 500, "gtol": 1e-7})
    beta_z = r.x
    beta_raw = beta_z / sd            # raw-unit sensitivity: z = (x-mu)/sd -> d/dx = beta_z/sd
    return beta_z, beta_raw, sd


def problem_sd(problems):
    """Per-problem risk level: mean option SD (raw feature index 1)."""
    return np.array([X[:, 1].mean() for X, _, _ in problems])


def ruggeri_problems(domain=None):
    Xprob, cnt = R.load()
    out = []
    for ctry in cnt:
        for q in R.KT:
            if domain and R.KT[q][2] != domain:
                continue
            nA, n = cnt[ctry][q]
            if n:
                out.append((Xprob[q], np.array([nA / n, 1 - nA / n]), float(n)))
    return out


def cv(x):
    x = np.array(x, float)
    return float(np.std(x) / (np.abs(np.mean(x)) + 1e-12))


def main():
    EV, SD = 0, 1
    # ---------- decisive test: within-corpus adaptation ----------
    print("== Within-corpus adaptation (choices13k binned by risk spread) ==")
    probs = F.load_c13k(3000)
    lvl = problem_sd(probs)
    order = np.argsort(lvl)
    bins = np.array_split(order, 4)
    rows = []
    print(f"{'bin':>4} {'sigma_SD':>9} {'beta_raw_SD':>12} {'beta_z_SD':>10} {'angle_raw':>10} {'angle_z':>8}")
    for i, idx in enumerate(bins):
        sub = [probs[j] for j in idx]
        bz, br, sd = analyze(sub)
        ang_raw = np.degrees(np.arctan2(br[SD], br[EV]))
        ang_z = np.degrees(np.arctan2(bz[SD], bz[EV]))
        rows.append((sd[SD], br[SD], bz[SD], ang_raw, ang_z))
        print(f"{i:>4} {sd[SD]:>9.1f} {br[SD]:>12.5f} {bz[SD]:>10.3f} {ang_raw:>9.1f}° {ang_z:>7.1f}°")

    sig = np.array([r[0] for r in rows])
    braw = np.array([r[1] for r in rows])
    bz = np.array([r[2] for r in rows])
    # adaptation: beta_raw_SD vs 1/sigma_SD should be strongly correlated
    corr = np.corrcoef(braw, 1 / sig)[0, 1]
    print(f"\nadaptation: corr(beta_raw_SD, 1/sigma_SD) = {corr:+.3f} "
          f"(near +1 => raw sensitivity tracks 1/sigma, the efficient-coding signature)")
    print(f"invariance: CV(beta_raw_SD) = {cv(braw):.3f}  vs  CV(beta_z_SD) = {cv(bz):.3f} "
          f"-> normalization {'REDUCES' if cv(bz) < cv(braw) else 'does NOT reduce'} spread "
          f"by {cv(braw)/max(cv(bz),1e-9):.1f}x")
    print(f"intrinsic risk weight beta_z_SD across bins: {bz.round(3)} (mean {bz.mean():.3f})")

    # ---------- cross-domain: same invariant across corpora? ----------
    print("\n== Cross-domain (representative corpora): intrinsic weight vs raw angle ==")
    doms = {
        "CPC18": F.load_cpc18(),
        "choices13k": F.load_c13k(1500),
        "bogota games": F.load_games(),
    }
    print(f"{'domain':13} {'sigma_EV':>9} {'sigma_SD':>9} {'angle_raw':>10} {'angle_z(intrinsic)':>18}")
    az, araw = [], []
    for name, p in doms.items():
        bz_, br_, sd_ = analyze(p)
        ar = np.degrees(np.arctan2(br_[SD], br_[EV]))
        azz = np.degrees(np.arctan2(bz_[SD], bz_[EV]))
        araw.append(ar); az.append(azz)
        print(f"{name:13} {sd_[EV]:>9.1f} {sd_[SD]:>9.1f} {ar:>9.1f}° {azz:>17.1f}°")
    print(f"\nspread of RAW angle across corpora:       {np.std(araw):.1f}°")
    print(f"spread of INTRINSIC (z) angle across corpora: {np.std(az):.1f}°")
    print(f"-> normalization {'reveals a shared' if np.std(az) < np.std(araw) else 'does NOT reveal a'} "
          f"intrinsic angle ({np.std(araw)/max(np.std(az),1e-9):.1f}x tighter)")

    print("\n== Verdict ==")
    ok_adapt = corr > 0.8
    ok_inv = cv(bz) < cv(braw)
    if ok_adapt and ok_inv:
        print("Efficient coding SUPPORTED: raw sensitivity tracks 1/sigma (adaptation), and the "
              "z-normalized weight is the invariant. The shared aversion angle is what a "
              "variance-normalizing, capacity-limited decider MUST use -- a first-principles account, "
              "not a fitted coincidence.")
    else:
        print("Efficient coding NOT cleanly supported: "
              f"adaptation corr {corr:+.2f}, invariance {'yes' if ok_inv else 'no'}. "
              "The angle looks intrinsic, not an environment-normalized code; the Shannon framing "
              "would be vocabulary, not mechanism.")
    print("\nHONEST: within-corpus binning controls for domain; the adaptation signature is the "
          "load-bearing evidence, not the vocabulary.")


if __name__ == "__main__":
    main()
