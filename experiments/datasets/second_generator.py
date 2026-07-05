#!/usr/bin/env python3
"""Second-generator (V4) test — does the fourfold pattern have Klein-four structure?

We found one involution empirically: the value reflection sigma_v (gain<->loss, rho_SD=-0.8).
The fourfold pattern needs a SECOND involution sigma_p (certainty<->possibility) that COMMUTES
with sigma_v to generate the Klein four-group V4. The algebraic signature of V4 is that the risk
attitude depends ONLY on the PRODUCT of the two flips: r = -d*q (pure interaction, no main effects).

Test: pool the 17 KT problems x 19 countries into one conditional logit where the risk-attitude
coefficient on Delta-SD is decomposed over domain d (gain +1 / loss -1) and probability level
q (certainty/high +1 / possibility/low -1):

    P(A) = sigma( beta_EV * dEV  +  (b0 + b_d*d + b_q*q + b_dq*d*q) * dSD )

V4 predicts: b_dq is large and negative (risk attitude ~ -d*q); the main effects b_d, b_q ~ 0.
Then sigma_v (d->-d) flips the risk attitude, sigma_p (q->-q) flips it, and doing BOTH returns it
(the diagonal cells agree) -- two commuting involutions = V4.

    python second_generator.py
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

import ruggeri as R


def build():
    Xprob, cnt = R.load()
    meta = {}
    for q in R.KT:
        pa, pb, dom = R.KT[q]
        fa, fb = np.array(R.feats(pa)), np.array(R.feats(pb))
        risky = pa if fa[1] >= fb[1] else pb
        nz = [(a, p) for a, p in risky if a != 0]
        p_ext = max(nz, key=lambda ap: abs(ap[0]))[1] if nz else 1.0
        meta[q] = {"dEV": fa[0] - fb[0], "dSD": fa[1] - fb[1],
                   "d": 1.0 if dom == "gain" else -1.0,
                   "q": 1.0 if p_ext >= 0.5 else -1.0}
    dEV = np.array([meta[q]["dEV"] for q in R.KT])
    dSD = np.array([meta[q]["dSD"] for q in R.KT])
    mE, sE, mS, sS = dEV.mean(), dEV.std(), dSD.mean(), dSD.std()
    rows = []
    for q in R.KT:
        m = meta[q]
        zE, zS = (m["dEV"] - mE) / sE, (m["dSD"] - mS) / sS
        for ctry in cnt:
            nA, n = cnt[ctry][q]
            if n:
                rows.append((zE, zS, m["d"], m["q"], nA, n, ctry, q))
    return rows


def arrs(rows):
    zE = np.array([r[0] for r in rows]); zS = np.array([r[1] for r in rows])
    d = np.array([r[2] for r in rows]); q = np.array([r[3] for r in rows])
    kA = np.array([r[4] for r in rows]); n = np.array([r[5] for r in rows])
    return zE, zS, d, q, kA, n


def nll(beta, A):
    zE, zS, d, q, kA, n = A
    bEV, b0, bd, bq, bdq = beta
    risk = b0 + bd * d + bq * q + bdq * d * q
    lin = bEV * zE + risk * zS
    p = np.clip(1 / (1 + np.exp(-lin)), 1e-9, 1 - 1e-9)
    return -np.sum(kA * np.log(p) + (n - kA) * np.log(1 - p))


def fit(A):
    best = None
    for s in range(6):
        rng = np.random.default_rng(s)
        r = minimize(nll, rng.normal(0, 0.5, 5), args=(A,), method="BFGS",
                     options={"maxiter": 800, "gtol": 1e-7})
        if best is None or r.fun < best.fun:
            best = r
    return best.x


def main():
    rows = build()
    A = arrs(rows)
    beta = fit(A)
    bEV, b0, bd, bq, bdq = beta

    # bootstrap over countries
    countries = sorted({r[6] for r in rows})
    rng = np.random.default_rng(0)
    boots = []
    for _ in range(300):
        take = set(rng.choice(countries, len(countries), replace=True))
        # resample WITH replacement -> weight rows by multiplicity
        mult = {c: 0 for c in countries}
        for c in rng.choice(countries, len(countries), replace=True):
            mult[c] += 1
        sub = [(r[0], r[1], r[2], r[3], r[4] * mult[r[6]], r[5] * mult[r[6]], r[6], r[7])
               for r in rows if mult[r[6]] > 0]
        boots.append(fit(arrs(sub)))
    boots = np.array(boots)
    ci = lambda i: np.percentile(boots[:, i], [2.5, 97.5])

    names = ["beta_EV", "b0 (base)", "b_d (domain)", "b_q (prob)", "b_dq (INTERACTION)"]
    print("Risk-attitude decomposition on Delta-SD (pooled logit, 17 KT x 19 countries):\n")
    print(f"{'param':22} {'estimate':>10} {'95% CI':>20}")
    for i, nm in enumerate(names):
        lo, hi = ci(i)
        print(f"{nm:22} {beta[i]:>+10.3f}  [{lo:>+7.3f},{hi:>+7.3f}]")

    print("\n== The four cells (risk-attitude coefficient on Delta-SD) ==")
    print("  (negative = risk-averse, positive = risk-seeking)")
    for d, dl in [(1, "gain"), (-1, "loss")]:
        for qq, ql in [(1, "high/cert"), (-1, "low/poss")]:
            coef = b0 + bd * d + bq * qq + bdq * d * qq
            print(f"  {dl:>5} x {ql:<9}: {coef:>+7.3f}  ({'risk-seeking' if coef>0 else 'risk-averse'})")

    print("\n== V4 verdict ==")
    interaction = abs(bdq)
    mains = abs(bd) + abs(bq) + abs(b0)
    print(f"|interaction b_dq| = {interaction:.3f}   vs   |main effects| (|b0|+|b_d|+|b_q|) = {mains:.3f}")
    print(f"interaction / main-effects ratio = {interaction/max(mains,1e-9):.2f} "
          f"(>>1 => pure interaction => V4)")
    lo, hi = ci(4)
    sig = (lo < 0 and hi < 0) or (lo > 0 and hi > 0)
    print(f"b_dq sign {'CONSISTENT' if sig else 'not consistent'} (CI excludes 0: {sig})")

    # involution + commutation check on the fitted cells
    r = {(dd, qq): b0 + bd * dd + bq * qq + bdq * dd * qq for dd in (1, -1) for qq in (1, -1)}
    sv = np.mean([abs(r[(1, qq)] + r[(-1, qq)]) for qq in (1, -1)])   # sigma_v flips sign -> sum ~0
    sp = np.mean([abs(r[(dd, 1)] + r[(dd, -1)]) for dd in (1, -1)])   # sigma_p flips sign -> sum ~0
    comm = abs(r[(1, 1)] - r[(-1, -1)]) + abs(r[(1, -1)] - r[(-1, 1)])  # diagonal cells agree
    scale = np.mean([abs(v) for v in r.values()])
    print(f"\nsigma_v (domain flip) residual |r(g)+r(l)| = {sv:.3f}  ({100*sv/scale:.0f}% of scale; ~0 => clean involution)")
    print(f"sigma_p (prob flip)   residual |r(hi)+r(lo)| = {sp:.3f}  ({100*sp/scale:.0f}% of scale; ~0 => SECOND involution found)")
    print(f"commutation sigma_v.sigma_p = id: diagonal mismatch = {comm:.3f}  ({100*comm/(2*scale):.0f}% of scale; ~0 => V4 closes)")

    print("\nHONEST: r = -d*q is the V4 signature (two commuting involutions). This tests the "
          "GROUP structure of the fourfold pattern; whether it lifts to the full D4 needs the "
          "cross-axis rotation (separate test). sigma_v was independently confirmed as rho_SD=-0.8.")


if __name__ == "__main__":
    main()
