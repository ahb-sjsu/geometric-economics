#!/usr/bin/env python3
"""Move 2c -- does ONE social metric span 2-person AND 3-person allocations? (social transfer)

Integrates Charness-Rabin (2002) 2-person dictator games + Engelmann-Strobel (2004) 3-person dictator
choices, and asks the social analog of the cross-domain-transfer pillar: does a single shared social
preference DIRECTION fit both, recalibrating only a scalar magnitude (the polar shape/scale split)?

Identified multinomial logit (no free temperature -- magnitude is in the weight norm; payoffs
normalized per dataset so magnitudes are comparable):
    features f = [own, disadv=mean max(o-own,0), adv=mean max(own-o,0), other_mean, minpay]
    P(option) = softmax(beta . f)
Shape = beta/||beta|| (the preference DIRECTION); scale = ||beta||. Transfer = does one dataset's
shape predict the other when only the scale is refit?

    python move2c_social_transfer.py
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

CR = [
    ("Berk29", [(400, [400]), (400, [750])], [0.31, 0.69], 26),
    ("Barc2",  [(400, [400]), (375, [750])], [0.52, 0.48], 48),
    ("Berk17", [(400, [400]), (375, [750])], [0.50, 0.50], 32),
    ("Berk23", [(200, [800]), (0, [0])],     [1.00, 0.00], 36),
    ("Berk8",  [(600, [300]), (500, [700])], [0.67, 0.33], 36),
    ("Berk15", [(700, [200]), (600, [600])], [0.27, 0.73], 22),
    ("Berk26", [(800, [0]),   (400, [400])], [0.78, 0.22], 32),
]
ES = [
    ("ES-X", [(8, [16, 5]), (8, [13, 3]), (8, [10, 1])], [0.700, 0.266, 0.033], 120),
    ("ES-Y", [(7, [16, 5]), (8, [13, 3]), (9, [10, 1])], [0.767, 0.133, 0.100], 120),
]
FEAT = ["own", "disadv", "adv", "other_mean", "minpay"]


def feats(own, others):
    dis = np.mean([max(o - own, 0) for o in others])
    adv = np.mean([max(own - o, 0) for o in others])
    return np.array([own, dis, adv, float(np.mean(others)), min([own] + list(others))], float)


def encode(games):
    """Per-game (X[opt,5], obs, n); payoffs normalized by the dataset's mean payoff."""
    scale = np.mean([v for _, opts, _, _ in games for o, oth in opts for v in [o] + list(oth)])
    out = []
    for _, opts, obs, n in games:
        X = np.vstack([feats(o / scale * 4, [x / scale * 4 for x in oth]) for o, oth in opts])
        out.append((X, np.array(obs), n))
    return out


def nll(beta, enc):
    tot = 0.0
    for X, obs, n in enc:
        u = X @ beta
        u -= u.max()
        p = np.clip(np.exp(u) / np.exp(u).sum(), 1e-9, 1)
        tot += -n * np.sum(obs * np.log(p))
    return tot


def fit(enc, k=5):
    best = None
    for s in range(16):
        r = minimize(lambda b: nll(b, enc), np.random.default_rng(s).normal(0, 1, k),
                     method="BFGS", options={"maxiter": 2000, "gtol": 1e-7})
        if best is None or r.fun < best.fun:
            best = r
    return best.x


def chance(enc):
    return sum(-n * np.sum(obs * np.log(1 / len(obs))) for _, obs, n in enc)


def transfer(shape, enc):
    """Fix the DIRECTION `shape`; refit only a scalar magnitude m -> beta = m*shape."""
    r = minimize(lambda m: nll(abs(m[0]) * shape, enc), [1.0], method="Nelder-Mead")
    return nll(abs(r.x[0]) * shape, enc)


def main():
    cr, es = encode(CR), encode(ES)
    print("== Shared social metric across 2-person (Charness-Rabin) + 3-person (Engelmann-Strobel) ==\n")

    b_all = fit(cr + es)
    print("  shared direction beta/||beta|| (multinomial logit on both datasets):")
    d = b_all / (np.linalg.norm(b_all) + 1e-9)
    print("    " + "   ".join(f"{f}={v:+.2f}" for f, v in zip(FEAT, d)))
    print(f"  reading: own={d[0]:+.2f} (self-regard), adv={d[2]:+.2f} (+ => guilt/costly equalizing-down), "
          f"other_mean={d[3]:+.2f} (+ => altruism/efficiency), minpay={d[4]:+.2f} (+ => maximin).")

    b_cr, b_es = fit(cr), fit(es)
    s_cr, s_es = b_cr / np.linalg.norm(b_cr), b_es / np.linalg.norm(b_es)
    nat_cr, nat_es = nll(b_cr, cr), nll(b_es, es)
    ch_cr, ch_es = chance(cr), chance(es)
    gc = lambda ch, nat, tr: max(0.0, (ch - tr) / (ch - nat + 1e-9))
    t_cr2es = gc(ch_es, nat_es, transfer(s_cr, es))
    t_es2cr = gc(ch_cr, nat_cr, transfer(s_es, cr))

    print("\n== Direction alignment + shape transfer ==")
    print(f"  cos(shape_CR, shape_ES) = {float(s_cr @ s_es):+.2f}  (the two datasets' preference "
          f"directions; +1 = identical shape)")
    print(f"  CR-shape -> ES (refit magnitude only): {100*t_cr2es:.0f}% of gap-to-native closed")
    print(f"  ES-shape -> CR (refit magnitude only): {100*t_es2cr:.0f}%")

    print("\n== Verdict ==")
    cos = float(s_cr @ s_es)
    if cos > 0.5 and min(t_cr2es, t_es2cr) > 0.3:
        print("One social preference DIRECTION spans 2- and 3-person allocations: the shapes align and "
              "each transfers to the other with only a scalar recalibration -- a small-N social analog "
              "of the cross-domain-transfer pillar.")
    elif cos > 0.3:
        print("PARTIAL: the two directions are positively aligned but transfer is asymmetric/weak -- one "
              "social metric roughly spans both, but 2- and 3-person allocations weight the social "
              "features somewhat differently.")
    else:
        print("The 2- and 3-person preference directions do NOT align -> one social metric does not "
              "cleanly span both allocation structures at this sample size.")
    print("HONEST: 7 + 2 games only (ES is 2 choice-sets, 3 options each). Underpowered; the shape/scale "
          "split and per-dataset normalization are the polar-transfer method applied to social data. "
          "Report the cosine and transfer numbers as suggestive, not confirmatory.")


if __name__ == "__main__":
    main()
