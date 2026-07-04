#!/usr/bin/env python3
"""Cross-domain transfer: ONE geometric metric across lotteries AND games.

The theory's central claim (nobel-program.md): a single shared metric predicts
behaviour in BOTH risky choice and strategic games -- something CPT (no games)
and Nash (no lotteries) structurally cannot do. Here we test it directly:

  * encode CPC18 lottery options and bogota game strategies into the SAME
    (EV, SD) feature space (games: EV/SD under a uniform level-0 belief over the
    opponent), payoff-scale-normalized per dataset so the metric is transferable;
  * fit the geometric metric (sigma_ev, sigma_sd, T) on ONE domain;
  * predict the OTHER domain with NO refit (transfer);
  * compare transfer to within-domain fit and to chance (uniform / constant).

If lottery-fit sigmas predict games near the games-fit level (and beat chance),
that is shared-metric evidence. Scored by NLL (lower better) under a common loss.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

import bogota_games
import cpc18


# ---- shared geometric choice model ------------------------------------------
def _softmax_costs(costs, T):
    z = -costs / T
    z -= z.max()
    e = np.exp(z)
    return e / e.sum()


def _cost(ev, sd, s_ev, s_sd):
    evmax = ev.max()
    return np.sqrt(((evmax - ev) / s_ev) ** 2 + (sd / s_sd) ** 2)


# ---- build normalized problem sets ------------------------------------------
def lottery_problems():
    """CPC18: list of (ev[2], sd[2], obs[2], n). Payoff-scale normalized."""
    df = cpc18.load_description()
    scale = np.std(np.r_[df["evA"], df["evB"]]) or 1.0
    probs = []
    for _, r in df.iterrows():
        ev = np.array([r["evA"], r["evB"]]) / scale
        sd = np.array([r["sdA"], r["sdB"]]) / scale
        obs = np.array([1 - r["brate"], r["brate"]])
        probs.append((ev, sd, obs, r["n"]))
    return probs


def game_problems(belief="uniform", level=1, lam=0.1):
    """bogota: list of (ev[k], sd[k], obs[k], n). Payoff-scale normalized.

    belief='uniform' (level-0 opponent) or 'lk' (level-k quantal, needs Mcol).
    """
    games = bogota_games.load_games()

    def enc(g):
        return bogota_games.encode_strategies(g["M"], g.get("Mcol"), belief=belief,
                                              level=level, lam=lam)

    allev = np.concatenate([enc(g)[0] for g in games])
    scale = np.std(allev) or 1.0
    probs = []
    for g in games:
        ev, sd = enc(g)
        probs.append((ev / scale, sd / scale, g["freqs"], g["N"]))
    return probs


# ---- fit / evaluate ---------------------------------------------------------
def nll(theta, probs):
    s_ev, s_sd, T = np.abs(theta) + 1e-6
    tot, wsum = 0.0, 0.0
    for ev, sd, obs, n in probs:
        p = _softmax_costs(_cost(ev, sd, s_ev, s_sd), T)
        p = np.clip(p, 1e-6, 1)
        tot += -n * np.sum(obs * np.log(p))
        wsum += n
    return tot / wsum


def fit(probs, x0=(1.0, 1.0, 1.0)):
    res = minimize(nll, x0, args=(probs,), method="Nelder-Mead",
                   options={"maxiter": 6000, "xatol": 1e-5, "fatol": 1e-7})
    return res.x


def eval_mae(theta, probs):
    s_ev, s_sd, T = np.abs(theta) + 1e-6
    maes = []
    for ev, sd, obs, n in probs:
        p = _softmax_costs(_cost(ev, sd, s_ev, s_sd), T)
        maes.append(np.mean(np.abs(p - obs)))
    return float(np.mean(maes))


def uniform_nll(probs):
    tot, wsum = 0.0, 0.0
    for ev, sd, obs, n in probs:
        k = len(obs)
        tot += -n * np.sum(obs * np.log(1.0 / k)); wsum += n
    return tot / wsum


def _report(lot, gam, tag):
    th_lot, th_gam = fit(lot), fit(gam)
    print(f"[{tag}] games={len(gam)}  chance(games)={uniform_nll(gam):.4f}  chance(lot)={uniform_nll(lot):.4f}")
    print(f"  GAMES     within={nll(th_gam, gam):.4f}   TRANSFER lot->games={nll(th_lot, gam):.4f}")
    print(f"  LOTTERIES within={nll(th_lot, lot):.4f}   TRANSFER games->lot={nll(th_gam, lot):.4f}")
    # fraction of chance->native gap closed by the transfer (games direction)
    chance, native, transfer = uniform_nll(gam), nll(th_gam, gam), nll(th_lot, gam)
    frac = (chance - transfer) / (chance - native) if chance > native else float("nan")
    print(f"  lot->games transfer closes {frac*100:.0f}% of the chance->native gap")
    print(f"  sigmas lot: s_ev={abs(th_lot[0]):.3f} s_sd={abs(th_lot[1]):.3f} T={abs(th_lot[2]):.3f}"
          f"  |  games: s_ev={abs(th_gam[0]):.3f} s_sd={abs(th_gam[1]):.3f} T={abs(th_gam[2]):.3f}\n")


def main():
    lot = lottery_problems()
    print(f"lotteries: {len(lot)} problems (CPC18)\n")
    print("=== belief model: UNIFORM level-0 opponent ===")
    _report(lot, game_problems(belief="uniform"), "uniform")
    print("=== belief model: LEVEL-K (opponent quantal BR, level=1) ===")
    _report(lot, game_problems(belief="lk", level=1, lam=0.1), "lk-l1")
    print("=== belief model: LEVEL-K (level=2) ===")
    _report(lot, game_problems(belief="lk", level=2, lam=0.1), "lk-l2")
    print("Shared-metric evidence = lot->games TRANSFER well below chance / high gap-closed. "
          "Does a level-k belief sharpen it?")


if __name__ == "__main__":
    main()
