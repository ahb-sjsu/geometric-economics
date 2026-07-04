#!/usr/bin/env python3
"""Structural fuzzing over MODEL STRUCTURES, scored by cross-domain TRANSFER.

The TCSS paper fuzzed over dimension subsets (which coordinates are active). Here
we fuzz over the mathematical STRUCTURE of the choice model itself -- value
transform, risk feature, metric norm, reference point, temperature rule -- and
score each candidate not by within-domain fit but by how well its parameters
TRANSFER across domains (lotteries <-> games). The winner is the structure whose
form is most nearly shared: the "ideal" the theory is groping toward.

Each structure maps an option to features and a cost; we fit on domain A and
predict domain B (full transfer, and polar shape-locked transfer), both
directions, and rank by the worst-case gap-closed (a structure only wins if it
transfers BOTH ways).
"""
from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import minimize

import bogota_games
import cpc18

# ---- feature builders (raw EV, SD per option, per problem) ------------------
def _lottery_raw():
    df = cpc18.load_description()
    out = []
    for _, r in df.iterrows():
        ev = np.array([r["evA"], r["evB"]]); sd = np.array([r["sdA"], r["sdB"]])
        obs = np.array([1 - r["brate"], r["brate"]])
        out.append((ev, sd, obs, r["n"]))
    return out


def _game_raw():
    games = bogota_games.load_games()
    out = []
    for g in games:
        ev, sd = bogota_games.encode_strategies(g["M"])   # uniform belief (best encoding)
        out.append((ev, sd, g["freqs"], g["N"]))
    return out


# ---- structure components ---------------------------------------------------
VALUE = {
    "identity": lambda ev, a: ev,
    "power":    lambda ev, a: np.sign(ev) * np.abs(ev) ** a,   # CPT-like concavity
}
RISK = {
    "sd":  lambda sd: sd,
    "var": lambda sd: sd ** 2,
}
NORM = {
    "L2": lambda dv, rk: np.sqrt(dv ** 2 + rk ** 2),          # Mahalanobis
    "L1": lambda dv, rk: np.abs(dv) + rk,                     # city-block
}
REF = {
    "max": lambda v: v.max(),
    "mean": lambda v: v.mean(),
}


def make_cost(struct):
    vfn, rfn, nfn, rref = VALUE[struct["value"]], RISK[struct["risk"]], NORM[struct["norm"]], REF[struct["ref"]]

    def cost(ev, sd, theta):
        s_v, s_r, a = np.abs(theta[0]) + 1e-6, np.abs(theta[1]) + 1e-6, np.clip(abs(theta[3]), 0.2, 1.5)
        v = vfn(ev, a)
        rk = rfn(sd)
        # scale features to unit scale per problem set is handled by fitting s_v,s_r
        dv = (rref(v) - v) / s_v
        return nfn(dv, rk / s_r)

    return cost


def predict(cost, ev, sd, theta):
    T = np.abs(theta[2]) + 1e-6
    c = cost(ev, sd, theta)
    z = -c / T; z -= z.max(); e = np.exp(z)
    return e / e.sum()


def nll(cost, theta, probs):
    tot = w = 0.0
    for ev, sd, obs, n in probs:
        p = np.clip(predict(cost, ev, sd, theta), 1e-6, 1)
        tot += -n * np.sum(obs * np.log(p)); w += n
    return tot / w


def fit(cost, probs, x0=(1.0, 1.0, 1.0, 0.9)):
    r = minimize(lambda th: nll(cost, th, probs), x0, method="Nelder-Mead",
                 options={"maxiter": 4000, "xatol": 1e-4, "fatol": 1e-6})
    return r.x


def uniform_nll(probs):
    tot = w = 0.0
    for ev, sd, obs, n in probs:
        tot += -n * np.sum(obs * np.log(1.0 / len(obs))); w += n
    return tot / w


def gap(chance, native, val):
    return (chance - val) / (chance - native) if chance > native + 1e-9 else 0.0


def evaluate_structure(struct, lot, gam):
    cost = make_cost(struct)
    th_l, th_g = fit(cost, lot), fit(cost, gam)
    ch_g, ch_l = uniform_nll(gam), uniform_nll(lot)
    nat_g, nat_l = nll(cost, th_g, gam), nll(cost, th_l, lot)
    lg = gap(ch_g, nat_g, nll(cost, th_l, gam))   # lot -> games
    gl = gap(ch_l, nat_l, nll(cost, th_g, lot))   # games -> lot
    return {"lg": lg, "gl": gl, "worst": min(lg, gl), "mean": (lg + gl) / 2,
            "nat_g": nat_g, "nat_l": nat_l}


def main():
    lot, gam = _lottery_raw(), _game_raw()
    grid = list(itertools.product(VALUE, RISK, NORM, REF))
    print(f"structural fuzzing: {len(grid)} candidate structures, scored by cross-domain transfer\n")
    print(f"{'value':9} {'risk':4} {'norm':4} {'ref':5} {'lot->gm':>8} {'gm->lot':>8} {'worst':>7} {'mean':>7}")
    results = []
    for value, risk, norm, ref in grid:
        s = {"value": value, "risk": risk, "norm": norm, "ref": ref}
        r = evaluate_structure(s, lot, gam)
        results.append((s, r))
        print(f"{value:9} {risk:4} {norm:4} {ref:5} {r['lg']*100:>7.0f}% {r['gl']*100:>7.0f}% "
              f"{r['worst']*100:>6.0f}% {r['mean']*100:>6.0f}%")
    best = max(results, key=lambda kr: kr[1]["worst"])
    print(f"\nBEST by worst-case transfer: {best[0]} "
          f"(worst {best[1]['worst']*100:.0f}%, mean {best[1]['mean']*100:.0f}%)")


if __name__ == "__main__":
    main()
