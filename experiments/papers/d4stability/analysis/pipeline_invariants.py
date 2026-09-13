#!/usr/bin/env python3
"""Metamorphic tests on the analysis pipeline. A gate, not a diagnostic.

`prereg-d4stability-v1` was void because its design matrix was oriented against
its outcome. Every check that registration carried passed. The coordinate was
imported and asserted and was correct. The estimator was verified against a
published value to `6.2e-12` and was correct, while being handed the wrong
design. The bundle was hashed on two machines and sealed the defect. The
covariates and the outcomes were written to separate files, which constrains what
the simulation may read and says nothing about how the two relate. The press
accounting balanced, and was about parsing.

**Every one of those tested a component. None tested the pipeline.**

This file takes the adversarial mindset of `structural-fuzzing`, which mutates a
model to find the failures it hides, and points it at the pipeline's
*representation of the data* rather than at the model's parameters. Each test
mutates the input in a way whose effect on the answer is known in advance, and
fails if the answer does not move exactly as it should. That is the class of test
that catches wiring errors, because a wiring error is precisely a transformation
that the analysis handles wrongly.

    I1  RELABEL       swap which option is called A and which B, everywhere.
                      Every coefficient must be UNCHANGED. This is the direct
                      detector of the v1 defect and it is strictly stronger than
                      a sign check on bEV, because it fails for any dependence on
                      declaration order at all.
    I2  FLIP          negate the outcome. Every coefficient must NEGATE.
    I3  RESCALE       multiply both outcomes of both options by a positive
                      constant. Every coefficient must be UNCHANGED, which is
                      also what makes outcome scale a legitimate split axis.
    I4  PLANT         generate choices from a known kappa in OPTION space, push
                      them through the whole parser and row builder, and recover
                      it. v1's power simulation generated its data from the same
                      design it then fitted, so it could measure the size and
                      power of a procedure aimed at the wrong estimand without
                      ever noticing. Planting in option space breaks that
                      circularity.
    I5  BEV           on real data, more expected value must make an option more
                      attractive. bEV <= 0 is not a finding, it is a symptom.

I1 and I4 are the two that would have caught v1. I5 is the cheap one that also
would have, and it is registered as a void condition in the grader besides.

    python pipeline_invariants.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.abspath(os.path.join(HERE, "..", "..", "d4interior", "analysis"))
sys.path.insert(0, HERE)
sys.path.insert(0, V3)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets")))

from kappa_mle import TERM_NAMES, _nll_grad_hess, design, fit  # noqa: E402
from stability_rows_v2 import row_from_menu  # noqa: E402
from stability_stat import _z  # noqa: E402

TOL = 1e-7
SEED = 20260913
N_MENUS = 40000
# I4 is judged in standard errors, not in absolute units. A first version used an
# absolute tolerance of 0.06 where the standard error on the chirality was 0.101,
# so it failed a pipeline that was recovering the truth to within 1.9 standard
# errors. That threshold was measuring its own noise, which is the same mistake
# as the 1e-6 convergence tolerance earlier in this lineage. Four standard errors
# across seven coefficients keeps the gate from crying wolf while still catching
# anything as large as a sign reversal.
Z_MAX = 4.0


def _opt_from(a, b):
    """(d, q) of the riskier option, which both orientations agree on."""
    from d4_rotation import _opt_coords
    from stability_rows_v2 import feats
    risky = a if feats(*a)[1] >= feats(*b)[1] else b
    return _opt_coords(*risky)


def fit_theta(dEV, dSD, d, q, y, with_se=False):
    X = design(_z(dEV), _z(dSD), d, q)
    theta, info = fit(X, y)
    assert info["converged"], "invariance fit did not converge"
    if not with_se:
        return theta
    _n, _g, H = _nll_grad_hess(X, y, theta)
    return theta, np.sqrt(np.diag(np.linalg.inv(H)))


def synthetic_menus(n, rng):
    """Two-outcome menus spanning the plane, with a random A/B declaration order
    so that a pipeline sensitive to that order has somewhere to fail."""
    out = []
    for _ in range(n):
        H = float(rng.uniform(1, 100))
        L = float(-rng.uniform(0, 100) if rng.random() < 0.6 else rng.uniform(0, H))
        p = float(rng.uniform(0.05, 0.95))
        m = float(rng.uniform(min(L, 0), H))
        a, b = (H, p, L), (m, 1.0, m)
        if rng.random() < 0.5:
            a, b = b, a
        out.append((a, b))
    return out


def build(menus, choices):
    rows = [row_from_menu(a, b, c)[0] for (a, b), c in zip(menus, choices)]
    rows = [r for r in rows if r is not None]
    A = lambda j: np.array([r[j] for r in rows])
    return A(0), A(1), A(2), A(3), A(4)


def main():
    rng = np.random.default_rng(SEED)
    menus = synthetic_menus(N_MENUS, rng)
    truth = {"const": -0.05, "d2+q2": 0.09, "d*q": 0.25,
             "d": -0.17, "q": 0.02, "d2-q2": -0.015}
    bEV_true = 0.60

    # Keep only menus the builder accepts, BEFORE anything is generated. A menu
    # that the builder drops would otherwise shift every later pairing of a menu
    # to its choice by one, which silently scrambles the planted truth.
    menus = [m for m in menus if row_from_menu(m[0], m[1], True)[0] is not None]

    # --- I4 PLANT, done first because everything else needs choices ----------
    # Generate in OPTION space: build the covariates from the menus, form the
    # true linear predictor, draw choices, and only then hand the whole thing to
    # the pipeline. Nothing here reuses a fitted design.
    dEV, dSD, d, q, _ = build(menus, [True] * len(menus))
    assert len(dEV) == len(menus), "menu filtering did not align"
    T = np.vstack([np.ones_like(d), d ** 2 + q ** 2, d * q, d, q, d ** 2 - q ** 2])
    coef = np.array([truth[t] for t in TERM_NAMES])
    lin = bEV_true * _z(dEV) + (coef @ T) * _z(dSD)
    pr = 1.0 / (1.0 + np.exp(-lin))
    y_risky = rng.random(len(pr)) < pr

    # the participant's key press, recovered from "took the risk"
    choices = []
    for (a, b), yr in zip(menus, y_risky):
        from stability_rows_v2 import feats
        a_is_risky = feats(*a)[1] >= feats(*b)[1]
        choices.append(bool(yr) == bool(a_is_risky))

    dEV, dSD, d, q, y = build(menus, choices)
    theta, se = fit_theta(dEV, dSD, d, q, y, with_se=True)
    zs = {"bEV": float((theta[0] - bEV_true) / se[0])}
    for i, t in enumerate(TERM_NAMES):
        zs[t] = float((theta[1 + i] - truth[t]) / se[1 + i])
    worst_z = max(abs(v) for v in zs.values())
    i4 = worst_z < Z_MAX
    print("I4 PLANT     recover a known kappa through the whole pipeline (n=%d)"
          % len(y))
    print("     term    planted   recovered       se     err/se")
    print("     %-6s  %+.4f   %+.4f   %.4f   %+6.2f"
          % ("bEV", bEV_true, theta[0], se[0], zs["bEV"]))
    for i, t in enumerate(TERM_NAMES):
        print("     %-6s  %+.4f   %+.4f   %.4f   %+6.2f"
              % (t, truth[t], theta[1 + i], se[1 + i], zs[t]))
    print("     worst |err/se| %.2f against a bar of %.1f   -> %s"
          % (worst_z, Z_MAX, "PASS" if i4 else "FAIL"))

    # --- I1 RELABEL ----------------------------------------------------------
    swapped = [(b, a) for (a, b) in menus]
    ch_sw = [not c for c in choices]
    t1 = fit_theta(*build(swapped, ch_sw))
    d1 = float(np.max(np.abs(t1 - theta)))
    i1 = d1 < TOL
    print()
    print("I1 RELABEL   swap which option is called A and which B")
    print("     max coefficient change %.3e  -> %s" % (d1, "PASS" if i1 else "FAIL"))
    if not i1:
        print("     the estimand depends on declaration order. THIS IS THE v1 DEFECT.")

    # --- I2 FLIP -------------------------------------------------------------
    t2 = fit_theta(dEV, dSD, d, q, 1.0 - y)
    d2 = float(np.max(np.abs(t2 + theta)))
    i2 = d2 < 1e-5
    print()
    print("I2 FLIP      negate the outcome, expect every coefficient to negate")
    print("     max |theta_flipped + theta| %.3e  -> %s" % (d2, "PASS" if i2 else "FAIL"))

    # --- I3 RESCALE ----------------------------------------------------------
    lam = 13.7
    scaled = [((a[0] * lam, a[1], a[2] * lam), (b[0] * lam, b[1], b[2] * lam))
              for (a, b) in menus]
    t3 = fit_theta(*build(scaled, choices))
    d3 = float(np.max(np.abs(t3 - theta)))
    i3 = d3 < 1e-6
    print()
    print("I3 RESCALE   multiply every outcome by %.1f" % lam)
    print("     max coefficient change %.3e  -> %s" % (d3, "PASS" if i3 else "FAIL"))

    # --- I5 BEV, on the real corpus -----------------------------------------
    print()
    print("I5 BEV       sign of the expected-value coefficient on the real corpus")
    try:
        from stability_rows_v2 import load_covariates, load_outcome
        rEV, rSD, rd, rq, rpid, rfold, rscale, rpart = load_covariates()
        ry = load_outcome()
        rt = fit_theta(rEV, rSD, rd, rq, ry)
        i5 = rt[0] > 0
        print("     bEV %+.4f  -> %s" % (rt[0], "PASS" if i5 else "FAIL"))
        if not i5:
            print("     a negative bEV says people choose against expected value.")
    except FileNotFoundError:
        i5 = None
        print("     SKIPPED, rows_covariates_v2.npz not built yet")

    # --- I0, does the gate work at all? --------------------------------------
    # A check that cannot fail is not a check. The v1 row builder is rebuilt here
    # deliberately, differencing in declaration order against a risk-oriented
    # outcome, and I1 and I5 MUST both fail on it. If they do not, this file is
    # decoration and the v2 seal means nothing.
    def build_v1_style(menus, choices):
        from stability_rows_v2 import feats
        rows = []
        for (a, b), chose_a in zip(menus, choices):
            evA, sdA = feats(*a)
            evB, sdB = feats(*b)
            if abs(sdA - sdB) < 1e-12:
                continue
            rows.append((evA - evB, sdA - sdB,
                         *_opt_from(a, b), float(chose_a == (sdA >= sdB))))
        A = lambda j: np.array([r[j] for r in rows])
        return A(0), A(1), A(2), A(3), A(4)

    v1EV, v1SD, v1d, v1q, v1y = build_v1_style(menus, choices)
    tv1 = fit_theta(v1EV, v1SD, v1d, v1q, v1y)
    sw1EV, sw1SD, sw1d, sw1q, sw1y = build_v1_style(swapped, ch_sw)
    tv1s = fit_theta(sw1EV, sw1SD, sw1d, sw1q, sw1y)
    v1_relabel_change = float(np.max(np.abs(tv1s - tv1)))
    i0 = (v1_relabel_change > TOL) and (tv1[0] <= 0 or abs(tv1[0] - bEV_true) > 0.2)
    print()
    print("I0 SELF-TEST the gate must REJECT the v1 orientation")
    print("     v1-style bEV %+.4f (planted %+.4f)" % (tv1[0], bEV_true))
    print("     v1-style relabel change %.3e (must exceed %.0e)" % (v1_relabel_change, TOL))
    print("     v1-style chirality %+.4f (planted %+.4f)" % (tv1[3], truth["d*q"]))
    print("     -> %s" % ("PASS, the gate detects the known defect" if i0
                          else "FAIL, the gate is blind and cannot be relied on"))

    checks = {"I0_gate_detects_v1": i0, "I1_relabel": i1, "I2_flip": i2,
              "I3_rescale": i3, "I4_plant": i4, "I5_bev_sign": i5}
    checks = {k: (None if v is None else bool(v)) for k, v in checks.items()}
    ok = all(v for v in checks.values() if v is not None)
    print()
    print("=" * 70)
    print("PIPELINE INVARIANTS: %s" % ("ALL PASS" if ok else "FAILURE"))
    print("=" * 70)
    with open(os.path.join(HERE, "pipeline_invariants.json"), "w",
              encoding="utf-8") as fh:
        json.dump({"checks": checks, "all_pass": bool(ok), "seed": SEED,
                   "planted": truth, "planted_bEV": bEV_true,
                   "recovered": {t: float(theta[1 + i])
                                 for i, t in enumerate(TERM_NAMES)},
                   "plant_z_scores": zs, "plant_z_bar": Z_MAX,
                   "n_menus": N_MENUS,
                   "recovered_bEV": float(theta[0]),
                   "relabel_max_change": d1, "flip_residual": d2,
                   "rescale_max_change": d3}, fh, indent=2)
    print("written pipeline_invariants.json")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
