#!/usr/bin/env python3
"""Pair each designed gamble with comparisons to make choice menus.

`design_grid.py` produces one gamble per (d, q) cell. The fit needs a menu of
two, because the linear predictor is `bEV*dEV + kappa(d,q)*dSD` where the
differences are between the two options while the coordinate is read off the
riskier one. So the target gamble has to be the riskier option in every menu, or
the coordinate the menu is built for is not the coordinate the fit will use.

Two comparison families, both anchored to the target gamble's own scale so that
the design is invariant to the size of the stakes.

  SURE   a certain amount at `ev(R) + delta*sd(R)`. Its standard deviation is
         zero, so R is riskier by construction.
  RISKY  a fifty-fifty gamble with the same expected value and a fraction `rho`
         of R's standard deviation, so R is riskier provided rho < 1.

`delta` runs over a ladder, which is what gives the logistic variation in `dEV`
to fit. Without it every menu would sit at the same expected-value difference and
the choice rate would be pinned.

Both families are kept deliberately. The SURE family puts a certain outcome on
every menu and the RISKY family puts none, which is the certainty split that
`prereg-d4gate-v1` tried to test opportunistically and could not. A designed set
carries it by construction and a later gating test would have it balanced.

Every menu is verified: R must be the riskier option, and the coordinate
recomputed from R through the imported `_opt_coords` must equal the cell's.

    python build_menus.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "datasets"))
sys.path.insert(0, DATASETS)

from d4_rotation import _opt_coords  # noqa: E402  IMPORTED, never restated

DELTAS = (-0.75, -0.25, 0.25, 0.75)
RHO = 0.5


def feats(H, p, L):
    ev = p * H + (1 - p) * L
    var = p * (H - ev) ** 2 + (1 - p) * (L - ev) ** 2
    return float(ev), float(np.sqrt(max(var, 0.0)))


def build(cells):
    menus = []
    for c in cells:
        H, p, L = c["H"], c["pH"], c["L"]
        evR, sdR = feats(H, p, L)
        if sdR <= 1e-9:
            continue
        dR, qR = _opt_coords(H, p, L)
        if abs(dR - c["d_actual"]) > 1e-9 or abs(qR - c["q_actual"]) > 1e-9:
            raise SystemExit("cell coordinate does not reproduce")
        for delta in DELTAS:
            target_ev = evR + delta * sdR
            for family in ("SURE", "RISKY"):
                if family == "SURE":
                    cH = cL = round(target_ev, 4)
                    cp = 1.0
                else:
                    s = RHO * sdR
                    cH, cL, cp = round(target_ev + s, 4), round(target_ev - s, 4), 0.5
                evC, sdC = feats(cH, cp, cL)
                if sdC >= sdR:            # R must be the riskier option
                    continue
                menus.append({
                    "d_target": c["d_target"], "q_target": c["q_target"],
                    "d": dR, "q": qR, "delta": delta, "family": family,
                    "R": {"H": H, "pH": p, "L": L, "ev": round(evR, 4),
                          "sd": round(sdR, 4)},
                    "C": {"H": cH, "pH": cp, "L": cL, "ev": round(evC, 4),
                          "sd": round(sdC, 4)},
                    "dEV": round(evR - evC, 6), "dSD": round(sdR - sdC, 6),
                })
    return menus


def main():
    with open(os.path.join(HERE, "design_grid.json"), encoding="utf-8") as fh:
        cells = json.load(fh)["cells"]
    menus = build(cells)

    d = np.array([m["d"] for m in menus])
    q = np.array([m["q"] for m in menus])
    dEV = np.array([m["dEV"] for m in menus])
    dSD = np.array([m["dSD"] for m in menus])
    z = lambda x: (x - x.mean()) / (x.std() + 1e-9)
    dEVz, dSDz = z(dEV), z(dSD)

    T = np.vstack([np.ones_like(d), d ** 2 + q ** 2, d * q, d, q, d ** 2 - q ** 2])
    X = np.vstack([dEVz, T * dSDz]).T
    norms = np.linalg.norm(X, axis=0); norms[norms < 1e-12] = 1.0
    s = np.linalg.svd(X / norms, compute_uv=False)

    # is the study degenerate? predicted choice rates under the fit B coefficients
    diag = os.path.abspath(os.path.join(HERE, "..", "d4gate", "analysis",
                                        "diagnostic_pooling.json"))
    with open(diag, encoding="utf-8") as fh:
        B = json.load(fh)["fits"]["B_corners_dropped"]["coefficients"]
    coef = np.array([B[t] for t in
                     ["const", "d2+q2", "d*q", "d", "q", "d2-q2"]])
    lin = 1.0 * dEVz + (coef @ T) * dSDz
    pr = 1.0 / (1.0 + np.exp(-lin))

    print("menus %d from %d cells, %d deltas, 2 families"
          % (len(menus), len(cells), len(DELTAS)))
    print("  family SURE  %d   family RISKY %d"
          % (sum(m["family"] == "SURE" for m in menus),
             sum(m["family"] == "RISKY" for m in menus)))
    print("  d < 0 %d   d > 0 %d" % (int((d < 0).sum()), int((d > 0).sum())))
    print()
    print("  kappa design condition number: %.1f" % (s[0] / s[-1]))
    print("  (choices13k 6.1, CPC18 interior 6.0)")
    print()
    print("  predicted choice rate under fit B: min %.3f  median %.3f  max %.3f"
          % (pr.min(), np.median(pr), pr.max()))
    print("  fraction beyond 0.02 of an endpoint: %.3f"
          % float(((pr < 0.02) | (pr > 0.98)).mean()))

    with open(os.path.join(HERE, "menus.json"), "w", encoding="utf-8") as fh:
        json.dump({"n_menus": len(menus), "deltas": list(DELTAS), "rho": RHO,
                   "condition_number": float(s[0] / s[-1]), "menus": menus},
                  fh, indent=2)
    print()
    print("written menus.json")


if __name__ == "__main__":
    main()
