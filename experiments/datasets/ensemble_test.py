#!/usr/bin/env python3
"""Discriminating test: shared geometry vs the behavioral ENSEMBLE.

My honest critique of the program: for the projection-gap SIGN contrasts, the
diagonal-Sigma geometry (one free sigma per coordinate) is near-equivalent to a
"bag of independent behavioral models" (one free beta per effect) -- same
parameters, same predictions. So the projection-gap does NOT discriminate the two.

Where the geometry CAN earn its keep is PARSIMONY + CROSS-DOMAIN TRANSFER: a
single shared metric fit on one domain predicts another, which a set of
domain-specialized models cannot do by construction (CPT has no representation of
a game; a game model none of a lottery). This script runs that test on human
data (CPC18 lotteries + bogota games), and reports the verdict honestly --
including the null possibility (geometry buys transfer at a large within-domain
price, i.e. it doesn't earn its keep).

Compared:
  ENSEMBLE   = two DISJOINT domain-specialist models (best within each domain,
               6 params, ZERO valid cross-domain prediction).
  GEOMETRY   = ONE shared metric (3 params) fit jointly; transfers via the polar
               angle-lock. Question: does it match the specialists within-domain
               AND transfer where the ensemble cannot, at fewer parameters?
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

import cross_domain as X


def pooled_nll(theta, lot, gam):
    nl, ng = len(lot), len(gam)
    return (X.nll(theta, lot) * nl + X.nll(theta, gam) * ng) / (nl + ng)


def bic(k, nll, n_obs):
    # binary/multinomial NLL is per-observation mean; approx BIC = k ln N + 2 N nll
    return k * np.log(n_obs) + 2 * n_obs * nll


def main():
    lot = X.lottery_problems()
    gam = X.game_problems(belief="uniform")
    n_lot = sum(int(n) for *_, n in lot)
    n_gam = sum(int(n) for *_, n in gam)

    # --- ENSEMBLE: two disjoint domain specialists ---
    th_lot = X.fit(lot)          # lottery specialist (3 params)
    th_gam = X.fit(gam)          # game specialist    (3 params)
    ens_lot = X.nll(th_lot, lot)
    ens_gam = X.nll(th_gam, gam)
    # the ensemble's ONLY option for the other domain is the wrong specialist:
    ens_transfer_lg = X.nll(th_lot, gam)   # lottery specialist on games
    ens_transfer_gl = X.nll(th_gam, lot)   # game specialist on lotteries

    # --- GEOMETRY: one shared metric fit jointly ---
    th_shared = minimize(pooled_nll, (1.0, 1.0, 1.0), args=(lot, gam),
                         method="Nelder-Mead", options={"maxiter": 8000, "xatol": 1e-5}).x
    geo_lot = X.nll(th_shared, lot)
    geo_gam = X.nll(th_shared, gam)
    # single-model cross-domain transfer via the polar angle-lock:
    geo_transfer_lg = X.nll(X.fit_shape_locked(gam, X._ratio(th_lot)), gam)   # lottery-shape -> games
    geo_transfer_gl = X.nll(X.fit_shape_locked(lot, X._ratio(th_gam)), lot)   # game-shape -> lotteries

    ch_lot, ch_gam = X.uniform_nll(lot), X.uniform_nll(gam)

    print("Discriminating test: shared GEOMETRY vs behavioral ENSEMBLE (CPC18 + bogota)\n")
    print(f"chance NLL: lotteries {ch_lot:.4f}  games {ch_gam:.4f}\n")
    print(f"{'':26} {'lotteries':>10} {'games':>10}  #params")
    print(f"{'ENSEMBLE within-domain':26} {ens_lot:>10.4f} {ens_gam:>10.4f}   6 (2x3, disjoint)")
    print(f"{'GEOMETRY within-domain':26} {geo_lot:>10.4f} {geo_gam:>10.4f}   3 (shared)")
    print(f"  price of sharing (geo-ens): lotteries {geo_lot-ens_lot:+.4f}  games {geo_gam-ens_gam:+.4f}\n")
    print("CROSS-DOMAIN TRANSFER (fit one domain, predict the other with one model):")
    print(f"  {'BEHAVIORAL ENSEMBLE (CPT+game)':32} lot->games  CHANCE   games->lot  CHANCE   (no shared representation)")
    print(f"  {'  [geo specialist, wrong domain]':32} lot->games {ens_transfer_lg:.4f}  games->lot {ens_transfer_gl:.4f}  (shares the geometric encoding!)")
    print(f"  {'GEOMETRY (shared, polar angle-lock)':32} lot->games {geo_transfer_lg:.4f}  games->lot {geo_transfer_gl:.4f}")

    def frac(chance, native, val):
        return (chance - val) / (chance - native) if chance > native else float("nan")
    print(f"\n  gap-closed (chance->native), games:  BEHAVIORAL-ENSEMBLE 0%%"
          f"   GEOMETRY {frac(ch_gam, geo_gam, geo_transfer_lg)*100:.0f}%")
    print(f"  gap-closed (chance->native), lots:   BEHAVIORAL-ENSEMBLE 0%%"
          f"   GEOMETRY {frac(ch_lot, geo_lot, geo_transfer_gl)*100:.0f}%")
    print("  (The behavioral ensemble is chance by CONSTRUCTION: a lottery model has no game input, "
          "and vice versa. The geometry transfers because encoding + metric are SHARED.)")

    # parsimony on the pooled data
    b_ens = bic(6, (ens_lot * n_lot + ens_gam * n_gam) / (n_lot + n_gam), n_lot + n_gam)
    b_geo = bic(3, (geo_lot * n_lot + geo_gam * n_gam) / (n_lot + n_gam), n_lot + n_gam)
    print(f"\nParsimony (pooled BIC, lower better): ENSEMBLE(6p) {b_ens:.0f}   GEOMETRY(3p) {b_geo:.0f}"
          f"   -> {'GEOMETRY' if b_geo < b_ens else 'ENSEMBLE'} wins")

    # verdict
    price_ok = (geo_lot - ens_lot < 0.03) and (geo_gam - ens_gam < 0.06)
    transfer_win = (geo_transfer_lg < ch_gam) and (geo_transfer_gl < ch_lot)  # vs behavioral ensemble = chance
    print("\nVERDICT:")
    print(f"  within-domain: shared geometry matches specialists at small price? {price_ok}")
    print(f"  geometry transfers where the BEHAVIORAL ensemble is chance-by-construction? {transfer_win}")
    print(f"  parsimony (pooled BIC) favors geometry? {b_geo < b_ens}  "
          f"(a wash/loss: BIC rewards the specialists' within-domain fit and ignores their transfer failure)")
    print("  NOTE (honest): the projection-gap SIGN contrasts do NOT discriminate geometry from the "
          "ensemble (free sigma_k ~ free beta_k). The discrimination here is entirely parsimony + "
          "cross-domain transfer. Steelman: the lottery specialist could be CPT (slightly better "
          "within-domain, per Paper 1) -- it still has ZERO game transfer, so the transfer verdict "
          "is unchanged.")


if __name__ == "__main__":
    main()
