#!/usr/bin/env python3
"""Move 1 -- transfer the SOCIAL coordinate across two different social tasks.

The cross-domain-transfer pillar (paper Section III) shares the RISK part of the metric
(EV, SD) between lotteries and games. This is the social analog: does the geometric metric's
self<->other tradeoff -- the social analog of the scale-invariant "aversion angle" -- transfer
between two structurally different social-allocation tasks, recalibrating only a scalar magnitude?

Model (the paper's metric, restricted to the 2-D social space (own, other)):
    each option is an allocation (s, o) = (own payoff, other's payoff);
    per-menu ideal (s*, o*) = (max feasible own, max feasible other);
    geometric cost C = sqrt( ((s*-s)/sigma_s)^2 + ((o*-o)/sigma_o)^2 );
    P(option) = softmax(-C / T).
The social tradeoff angle is set by the ratio sigma_s : sigma_o (scale-invariant): small sigma_o =>
the metric is very sensitive to shortfalls in the OTHER's payoff => other-regarding.

Domains (different tasks, different subjects, different labs):
  A = FKM (Fisman-Kariv-Markovits 2007) 2-person budget-line giving -- POWERED, 3,800 individual
      choices; each budget line is a menu of (s, o) points, discretized to K frontier allocations.
  B = Charness-Rabin (2002) 7 two-person dictator games -- discrete binary menus, aggregate freqs.

Transfer (the polar angle-lock of Section III): fit the angle on one domain, predict the other with
only sigma-scale + T refit. Reported: native / chance / full / angle-locked NLL, gap closed, angles.

    python social_transfer.py
"""
from __future__ import annotations

import os
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
FKM2 = os.path.join(HERE, "raw_fkm", "20050757", "Tobit", "Tobit_2D", "Data_2D.mat")
K = 21

CR = [
    ("Berk29", [(400, 400), (400, 750)], [0.31, 0.69], 26),
    ("Barc2",  [(400, 400), (375, 750)], [0.52, 0.48], 48),
    ("Berk17", [(400, 400), (375, 750)], [0.50, 0.50], 32),
    ("Berk23", [(200, 800), (0,   0)],   [1.00, 0.00], 36),
    ("Berk8",  [(600, 300), (500, 700)], [0.67, 0.33], 36),
    ("Berk15", [(700, 200), (600, 600)], [0.27, 0.73], 22),
    ("Berk26", [(800, 0),   (400, 400)], [0.78, 0.22], 32),
]


# ----- FKM: vectorized menu arrays S[N,K], O[N,K], obs idx[N] -----------------------------------
def load_fkm():
    import scipy.io as sio
    d = sio.loadmat(FKM2)["Data_2D"]
    wo, price = d[:, 2], d[:, 3]
    N = len(price)
    grid = np.linspace(0.0, 1.0, K)                 # fraction of max giving
    O = grid[None, :] * (1.0 / price)[:, None]      # o in [0, 1/p]
    S = 1.0 - price[:, None] * O                     # s = 1 - p*o
    idx = np.clip(np.round(wo * (K - 1)).astype(int), 0, K - 1)  # o_obs/o_max = w_other
    return S, O, idx


def encode_cr():
    out = []
    for _, opts, obs, n in CR:
        S = np.array([o for o, _ in opts], float)
        O = np.array([x for _, x in opts], float)
        out.append((S, O, np.array(obs, float), n))
    return out


# Isotropic-ridge floor/ceiling on sigma (the model's "PSD pseudometric + ridge P+eps*I"):
# bounds sigma away from the degenerate corner (sigma->0 = infinite sensitivity) that a pooled,
# heterogeneous population would otherwise drive one axis to. SIG in normalized (per-dataset) units.
SIG_LO, SIG_HI = 0.05, 20.0


def _clip(x):
    return np.clip(x, SIG_LO, SIG_HI)


def sigmas(params, angle):
    if angle is None:
        ls, lo, lt = params
        return _clip(np.exp(ls)), _clip(np.exp(lo)), np.exp(lt)
    lscale, lt = params
    m = np.exp(lscale)
    return _clip(m * angle[0]), _clip(m * angle[1]), np.exp(lt)


# ----- vectorized FKM NLL -----------------------------------------------------------------------
def nll_fkm(params, data, sc, angle=None):
    S, O, idx = data
    sig_s, sig_o, T = sigmas(params, angle)
    s_star = S.max(1, keepdims=True); o_star = O.max(1, keepdims=True)
    C = np.sqrt(((s_star - S) / (sc * sig_s)) ** 2 + ((o_star - O) / (sc * sig_o)) ** 2)
    u = -C / T
    u -= u.max(1, keepdims=True)
    e = np.exp(u)
    p = e / e.sum(1, keepdims=True)
    return -np.sum(np.log(np.clip(p[np.arange(len(idx)), idx], 1e-12, 1.0)))


def nll_cr(params, menus, sc, angle=None):
    sig_s, sig_o, T = sigmas(params, angle)
    tot = 0.0
    for S, O, obs, n in menus:
        C = np.sqrt(((S.max() - S) / (sc * sig_s)) ** 2 + ((O.max() - O) / (sc * sig_o)) ** 2)
        u = -C / T; u -= u.max(); e = np.exp(u); p = np.clip(e / e.sum(), 1e-12, 1.0)
        tot -= n * np.sum(obs * np.log(p))
    return tot


def chance_fkm(data):
    return len(data[2]) * (-np.log(1.0 / K))


def chance_cr(menus):
    return sum(-n * np.sum(obs * np.log(1.0 / len(obs))) for _, _, obs, n in menus)


def fit(nll, data, sc, k=3, seeds=8):
    best = None
    for s in range(seeds):
        r = minimize(nll, np.random.default_rng(s).normal(0, 1, k), args=(data, sc, None),
                     method="Nelder-Mead", options={"maxiter": 2500, "xatol": 1e-6, "fatol": 1e-8})
        if best is None or r.fun < best.fun:
            best = r
    return best


def transfer_angle(nll, angle, data, sc, seeds=8):
    best = np.inf
    for s in range(seeds):
        r = minimize(nll, np.random.default_rng(s).normal(0, 1, 2), args=(data, sc, angle),
                     method="Nelder-Mead", options={"maxiter": 2500, "xatol": 1e-6, "fatol": 1e-8})
        best = min(best, r.fun)
    return best


def angle_of(params):
    sig_s, sig_o = _clip(np.exp(params[0])), _clip(np.exp(params[1]))
    n = np.hypot(sig_s, sig_o)
    return np.array([sig_s / n, sig_o / n])


def gap(ch, nat, tr):
    return (ch - tr) / (ch - nat + 1e-12)


def main():
    print("== Move 1: transfer the SOCIAL coordinate (self<->other tradeoff) across two tasks ==\n")
    S, O, idx = load_fkm()
    fkm = (S, O, idx)
    cr = encode_cr()
    sc_f = np.r_[S.ravel(), O.ravel()].mean()
    sc_c = np.concatenate([np.r_[a, b] for a, b, _, _ in cr]).mean()
    print(f"FKM 2-person: {len(idx)} individual choices (76 subjects); Charness-Rabin: {len(cr)} games.\n")

    rf, rc = fit(nll_fkm, fkm, sc_f), fit(nll_cr, cr, sc_c)
    nat_f, nat_c = rf.fun, rc.fun
    ch_f, ch_c = chance_fkm(fkm), chance_cr(cr)
    ang_f, ang_c = angle_of(rf.x), angle_of(rc.x)
    cos = float(ang_f @ ang_c)

    print("== Native fits (each domain fit on itself) ==")
    print(f"  FKM native NLL {nat_f/len(idx):.4f}/choice (chance {ch_f/len(idx):.4f})  "
          f"angle sig_s:sig_o = {ang_f[0]:.3f}:{ang_f[1]:.3f}")
    print(f"  CR  native NLL {nat_c:.3f} (chance {ch_c:.3f})  angle sig_s:sig_o = {ang_c[0]:.3f}:{ang_c[1]:.3f}")
    print(f"  cos(angle_FKM, angle_CR) = {cos:+.3f}\n")

    full_fc = nll_cr(rf.x, cr, sc_c, None)
    ang_fc = transfer_angle(nll_cr, ang_f, cr, sc_c)
    full_cf = nll_fkm(rc.x, fkm, sc_f, None)
    ang_cf = transfer_angle(nll_fkm, ang_c, fkm, sc_f)

    print("== Transfer (fit angle on A, predict B; % of chance->native gap closed) ==")
    print(f"  FKM -> CR : full {gap(ch_c,nat_c,full_fc)*100:5.0f}%   angle-locked {gap(ch_c,nat_c,ang_fc)*100:5.0f}%")
    print(f"  CR -> FKM : full {gap(ch_f,nat_f,full_cf)*100:5.0f}%   angle-locked {gap(ch_f,nat_f,ang_cf)*100:5.0f}%")

    print("\n== Verdict ==")
    g_fc, g_cf = gap(ch_c, nat_c, ang_fc), gap(ch_f, nat_f, ang_cf)
    lo, hi = min(g_fc, g_cf), max(g_fc, g_cf)
    if cos > 0.9 and hi > 0.85 and lo > 0.35:
        print(f"THE SOCIAL COORDINATE TRANSFERS. Fit independently, the self<->other tradeoff SHAPE is "
              f"nearly identical across the two tasks (cos={cos:.2f}). Angle-locked transfer: the powered "
              f"FKM metric (3,800 choices) predicts Charness-Rabin dictator play at {g_fc*100:.0f}% of a "
              f"native fit with only a scale recalibration; the reverse (7 games -> 3,800 choices) reaches "
              f"{g_cf*100:.0f}%. Same richer-domain-transfers-better asymmetry as the RISK leg (Sec III), "
              f"now on the OTHER-REGARDING coordinate -- powered, bidirectional, and above the untestable "
              f"9-game attempt (move2c).")
    elif cos > 0.7 and hi > 0.5:
        print(f"PARTIAL: shapes aligned (cos={cos:.2f}); transfer {g_fc*100:.0f}%/{g_cf*100:.0f}% -- "
              f"positive both ways but below the risk leg.")
    else:
        print(f"WEAK: social tradeoff does not cleanly transfer (cos={cos:.2f}, {g_fc*100:.0f}%/{g_cf*100:.0f}%).")
    print("HONEST: single pooled metric over a heterogeneous population (FKM ~40% keep-everything drives "
          "one axis to the ridge floor); the level of other-regard differs across populations even though "
          "the tradeoff shape is shared; CR side is 7 aggregate games. Ridge SIG_LO=0.05 regularizes the "
          "degenerate self-regard corner (the model's PSD-pseudometric-plus-isotropic-ridge).")


if __name__ == "__main__":
    main()
