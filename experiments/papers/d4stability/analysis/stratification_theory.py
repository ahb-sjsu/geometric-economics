#!/usr/bin/env python3
"""EXPLORATORY. The stratification, checked rather than asserted.

**Not part of any registration and it changes no verdict.**

`SEAM.md` calls the domain of kappa "stratified in the weak sense" and declines to
say more. This does the work properly, separating what is a theorem from what is
measurable, and testing only the second.

WHAT IS A THEOREM AND NEEDS NO MEASUREMENT

The stimulus space is `{(H, p, L)}` with `H >= L`. The three regions are cut out
by sign conditions, `L >= 0` for no loss branch, `H <= 0` for no gain branch, and
`H > 0 > L` for mixed. That is a hyperplane arrangement, hence semialgebraic, and
every semialgebraic set admits a Whitney stratification. For an arrangement the
strata are open subsets of affine subspaces, so their tangent spaces are constant
and conditions A and B hold at once. **Testing Whitney regularity of the domain
empirically would be a category error.** It is true by construction.

WHAT IS MEASURABLE

Three things, and only the third is about people.

    T1  The rank of the coordinate map. `phi(H, p, L) = (d, q)` should have rank
        two on the mixed region and rank one on the unmixed regions, because `d`
        is constant there. Checked numerically by finite differences.

    T2  The regularity of `d` across the frontier. `d` should be continuous and
        not differentiable at `L = 0`, with a one-sided derivative of
        `2(1-p)/(pH)` from the mixed side and zero from the other. Checked
        against the analytic value.

    T3  **The frontier condition for the graph of kappa.** Whitney A and B
        presuppose that the closure of the big stratum contains the small one. For
        the graph of a behavioural function that is an empirical question, and if
        it fails then A and B are not merely unverified, they are inapplicable.
        Tested by comparing the limit of kappa from inside against kappa on the
        edge.

    T4  Whitney A for the graph, in the one direction where it is defined. If the
        frontier condition held, A would require the tangent plane of the graph
        over the mixed region to converge to something containing the tangent
        line of the graph over the edge. In the `q` direction that is the
        statement that the `q` slope of kappa just inside matches the `q` slope
        on the edge. Tested whether or not T3 passes, because the comparison is
        informative either way.

A SECOND SEAM, WHICH NOTHING SO FAR HAS EXAMINED

`q = 2 * p_salient - 1` where the salient outcome is the one of larger absolute
value. At `|H| = |L|` the salient outcome switches, so `q` jumps from `2p - 1` to
`1 - 2p`. **That is a discontinuity of size `2|2p - 1|` strictly inside the mixed
region**, on a set the analysis has treated as ordinary interior. T5 locates it
and T6 asks whether kappa jumps across it.

    python stratification_theory.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
V3 = os.path.abspath(os.path.join(HERE, "..", "..", "d4interior", "analysis"))
sys.path.insert(0, DATASETS)
sys.path.insert(0, V3)
sys.path.insert(0, HERE)

from d4_rotation import _opt_coords  # noqa: E402  IMPORTED, never restated
from kappa_mle import _nll_grad_hess, fit  # noqa: E402
from stability_rows_v2 import load_covariates, load_outcome  # noqa: E402

CLUSTER_INFL = 1.76
MIN_CELL = 250


def _z(x):
    s = x.std()
    return (x - x.mean()) / (s if s > 1e-12 else 1.0)


def fit_se(X, y):
    th, info = fit(X, y)
    _n, _g, H = _nll_grad_hess(X, y, th)
    try:
        se = np.sqrt(np.diag(np.linalg.inv(H)))
    except np.linalg.LinAlgError:
        se = np.full(len(th), np.nan)
    return th, se, info


def kappa_linear_in_q(eZ, sZ, y, sel, label):
    """kappa = a + b*q on a subset. Returns (a, b, se_a, se_b, n)."""
    if sel.sum() < MIN_CELL:
        return None
    q = label
    X = np.vstack([eZ[sel], sZ[sel], q[sel] * sZ[sel]]).T
    th, se, _i = fit_se(X, y[sel])
    return (float(th[1]), float(th[2]),
            float(se[1] * CLUSTER_INFL), float(se[2] * CLUSTER_INFL),
            int(sel.sum()))


def main():
    out = {"note": "EXPLORATORY, changes no registered verdict"}

    # ---------------- T1, rank of the coordinate map -----------------------
    print("=" * 78)
    print("T1. RANK OF THE COORDINATE MAP phi(H, p, L) = (d, q)")
    print("=" * 78)
    rng = np.random.default_rng(20260913)
    h = 1e-6

    def jac(H, p, L):
        J = np.zeros((2, 3))
        base = np.array(_opt_coords(H, p, L))
        for k, (dH, dp, dL) in enumerate(((h, 0, 0), (0, h, 0), (0, 0, h))):
            up = np.array(_opt_coords(H + dH, p + dp, L + dL))
            J[:, k] = (up - base) / h
        return J

    for name, gen in (
        ("mixed, H > 0 > L",
         lambda: (rng.uniform(10, 100), rng.uniform(0.2, 0.8), -rng.uniform(10, 100))),
        ("no loss branch, L > 0",
         lambda: (rng.uniform(50, 100), rng.uniform(0.2, 0.8), rng.uniform(1, 40))),
        ("no gain branch, H < 0",
         lambda: (-rng.uniform(1, 40), rng.uniform(0.2, 0.8), -rng.uniform(50, 100))),
    ):
        ranks = []
        for _ in range(400):
            H, p, L = gen()
            if H < L:
                H, L = L, H
            s = np.linalg.svd(jac(H, p, L), compute_uv=False)
            ranks.append(int((s > 1e-4 * max(s[0], 1e-12)).sum()))
        vals, cnt = np.unique(ranks, return_counts=True)
        print("  %-24s rank %s   (400 random points)"
              % (name, dict(zip(vals.tolist(), cnt.tolist()))))
        out.setdefault("T1_rank", {})[name] = dict(zip([int(v) for v in vals],
                                                       [int(c) for c in cnt]))
    print()
    print("  rank two on the mixed region and rank one on the unmixed regions is")
    print("  the precise statement that the coordinate degenerates there.")

    # ---------------- T2, regularity of d across the frontier --------------
    print()
    print("=" * 78)
    print("T2. IS d DIFFERENTIABLE ACROSS L = 0 ?")
    print("=" * 78)
    print("  analytic one-sided derivatives at L = 0:")
    print("    from the mixed side   dd/dL = 2(1-p)/(pH)")
    print("    from the gain side    dd/dL = 0")
    print()
    print("     H      p     numeric from below   analytic   from above")
    rows = []
    for H, p in ((50.0, 0.5), (20.0, 0.8), (80.0, 0.25), (10.0, 0.6)):
        eps = 1e-7
        d_at = _opt_coords(H, p, 0.0)[0]
        d_lo = _opt_coords(H, p, -eps)[0]
        d_hi = _opt_coords(H, p, +eps)[0]
        below = (d_at - d_lo) / eps
        above = (d_hi - d_at) / eps
        ana = 2 * (1 - p) / (p * H)
        print("  %6.1f  %5.2f   %16.6f   %8.6f   %9.6f"
              % (H, p, below, ana, above))
        rows.append({"H": H, "p": p, "numeric_below": float(below),
                     "analytic": float(ana), "numeric_above": float(above)})
    out["T2_derivative"] = rows
    print()
    print("  d is continuous and NOT differentiable at L = 0. The derivative")
    print("  from the mixed side is bounded away from zero and the derivative")
    print("  from the other side is exactly zero.")

    # ---------------- data for T3 to T6 ------------------------------------
    dEV, dSD, d, q, pid, fold, scale, part = load_covariates()
    y = load_outcome()
    eZ, sZ = _z(dEV), _z(dSD)
    z = np.load(os.path.join(HERE, "seam_covariates.npz"))
    rH, rL, rp = z["risky_H"], z["risky_L"], z["risky_p"]
    mixed = (np.minimum(rH, rL) < 0) & (np.maximum(rH, rL) > 0)
    gain_only = np.minimum(rH, rL) >= 0

    # ---------------- T3, frontier condition for the graph -----------------
    print()
    print("=" * 78)
    print("T3. FRONTIER CONDITION FOR THE GRAPH OF kappa")
    print("=" * 78)
    print("  Whitney A and B presuppose that the closure of the big stratum")
    print("  contains the small one. For a graph that is an empirical question.")
    gap = 1.0 - np.abs(d)
    edges = [(0.0, 0.02), (0.02, 0.05), (0.05, 0.10), (0.10, 0.20)]
    lab, grp = [], np.full(len(y), "none", dtype=object)
    for lo, hi in edges:
        m = mixed & (d > 0) & (gap > lo) & (gap <= hi)
        if m.sum() >= MIN_CELL:
            nm = "inside_%.2f_%.2f" % (lo, hi)
            grp[m] = nm
            lab.append(nm)
    grp[gain_only] = "edge"
    lab.append("edge")
    cols = [eZ] + [np.where(grp == g, sZ, 0.0) for g in lab]
    th, se, _i = fit_se(np.vstack(cols).T, y)
    print()
    print("    stratum                n      kappa       se")
    rec = []
    for j, nm in enumerate(lab):
        n = int((grp == nm).sum())
        print("    %-18s %7d   %+8.4f  %7.4f"
              % (nm, n, th[1 + j], se[1 + j] * CLUSTER_INFL))
        rec.append({"stratum": nm, "n": n, "kappa": float(th[1 + j]),
                    "se": float(se[1 + j] * CLUSTER_INFL)})
    lim = th[1]                      # nearest stratum inside
    edgev = th[1 + lab.index("edge")]
    sej = float(np.hypot(se[1], se[1 + lab.index("edge")]) * CLUSTER_INFL)
    print()
    print("    limit from inside  %+.4f" % lim)
    print("    value on the edge  %+.4f" % edgev)
    print("    difference         %+.4f +/- %.4f   (%.1f se)"
          % (edgev - lim, sej, abs(edgev - lim) / sej))
    holds = abs(edgev - lim) < 2 * sej
    print()
    print("    FRONTIER CONDITION: %s"
          % ("holds, kappa extends continuously" if holds else
             "FAILS. kappa does not extend continuously to the edge, so the"))
    if not holds:
        print("    graph is not a stratified set and Whitney A and B are")
        print("    INAPPLICABLE to it, not merely unverified.")
    out["T3_frontier"] = {"strata": rec, "limit_inside": float(lim),
                          "edge": float(edgev), "difference": float(edgev - lim),
                          "se": sej, "holds": bool(holds)}

    # ---------------- T4, Whitney A in the q direction ---------------------
    print()
    print("=" * 78)
    print("T4. WHITNEY A FOR THE GRAPH, IN THE q DIRECTION")
    print("=" * 78)
    print("  if the frontier condition held, A would require the q slope of")
    print("  kappa just inside to converge to the q slope on the edge.")
    print()
    print("    stratum                   n     kappa_0      q slope")
    t4 = []
    for lo, hi in edges:
        m = mixed & (d > 0) & (gap > lo) & (gap <= hi)
        r = kappa_linear_in_q(eZ, sZ, y, m, q)
        if r:
            a, b, sa, sb, n = r
            print("    inside %.2f to %.2f      %6d   %+8.4f   %+8.4f +/- %.4f"
                  % (lo, hi, n, a, b, sb))
            t4.append({"stratum": "inside_%.2f_%.2f" % (lo, hi), "n": n,
                       "kappa0": a, "q_slope": b, "q_slope_se": sb})
    r = kappa_linear_in_q(eZ, sZ, y, gain_only, q)
    a, b, sa, sb, n = r
    print("    edge                    %6d   %+8.4f   %+8.4f +/- %.4f"
          % (n, a, b, sb))
    t4.append({"stratum": "edge", "n": n, "kappa0": a, "q_slope": b,
               "q_slope_se": sb})
    inner = t4[0]
    diff = inner["q_slope"] - b
    sed = float(np.hypot(inner["q_slope_se"], sb))
    print()
    print("    innermost minus edge  %+.4f +/- %.4f   (%.1f se)"
          % (diff, sed, abs(diff) / sed))
    print("    WHITNEY A in q: %s"
          % ("consistent" if abs(diff) < 2 * sed else "VIOLATED"))
    out["T4_whitney_A_q"] = {"strata": t4, "difference": float(diff),
                             "se": sed,
                             "consistent": bool(abs(diff) < 2 * sed)}

    # ---------------- T5, the second seam, located --------------------------
    print()
    print("=" * 78)
    print("T5. A SECOND SEAM. q JUMPS WHERE |H| = |L|")
    print("=" * 78)
    ratio = np.abs(rH) / np.maximum(np.abs(rL), 1e-12)
    lr = np.log10(np.maximum(ratio, 1e-12))
    print("  q = 2 p_salient - 1 and the salient outcome is the larger in")
    print("  absolute value, so at |H| = |L| the definition switches and q")
    print("  jumps by 2|2p - 1|.")
    print()
    for lo, hi, nm in ((-10, -0.05, "|L| clearly larger"),
                       (-0.05, 0.0, "|L| just larger"),
                       (0.0, 0.05, "|H| just larger"),
                       (0.05, 10, "|H| clearly larger")):
        m = mixed & (lr > lo) & (lr <= hi)
        if m.sum():
            print("    %-20s n %6d   mean q %+.3f   mean jump if switched %.3f"
                  % (nm, m.sum(), q[m].mean(),
                     float(np.mean(2 * np.abs(2 * rp[m] - 1)))))
    near = mixed & (np.abs(lr) <= 0.05)
    print()
    print("    rows within 12 percent of |H| = |L|: %d" % int(near.sum()))
    out["T5_second_seam"] = {"n_near": int(near.sum()),
                             "mean_jump_size": float(np.mean(2 * np.abs(2 * rp[near] - 1)))
                             if near.sum() else None}

    # ---------------- T6, does kappa jump across it? ------------------------
    print()
    print("=" * 78)
    print("T6. DOES kappa JUMP ACROSS THE SECOND SEAM?")
    print("=" * 78)
    lab2, grp2 = [], np.full(len(y), "none", dtype=object)
    bands = [(-10, -0.30), (-0.30, -0.10), (-0.10, -0.02), (-0.02, 0.0),
             (0.0, 0.02), (0.02, 0.10), (0.10, 0.30), (0.30, 10)]
    for lo, hi in bands:
        m = mixed & (lr > lo) & (lr <= hi)
        if m.sum() >= MIN_CELL:
            nm = "lr_%+.2f_%+.2f" % (lo, hi)
            grp2[m] = nm
            lab2.append(nm)
    cols = [eZ] + [np.where(grp2 == g, sZ, 0.0) for g in lab2]
    th2, se2, _i = fit_se(np.vstack(cols).T, y)
    print("    log10 |H|/|L| band        n      kappa       se")
    rec2 = []
    for j, nm in enumerate(lab2):
        n = int((grp2 == nm).sum())
        mark = "   <-- seam" if nm.startswith("lr_-0.02") or nm.startswith("lr_+0.00") else ""
        print("    %-22s %7d   %+8.4f  %7.4f%s"
              % (nm, n, th2[1 + j], se2[1 + j] * CLUSTER_INFL, mark))
        rec2.append({"band": nm, "n": n, "kappa": float(th2[1 + j]),
                     "se": float(se2[1 + j] * CLUSTER_INFL)})
    below = [r for r in rec2 if r["band"].startswith("lr_-0.02")]
    above = [r for r in rec2 if r["band"].startswith("lr_+0.00")]
    if below and above:
        jump = above[0]["kappa"] - below[0]["kappa"]
        sej2 = float(np.hypot(below[0]["se"], above[0]["se"]))
        print()
        print("    jump across |H| = |L|:  %+.4f +/- %.4f   (%.1f se)"
              % (jump, sej2, abs(jump) / sej2))
        print("    %s" % ("A SECOND DISCONTINUITY" if abs(jump) > 2 * sej2
                          else "no detectable jump, the seam is benign for kappa"))
        out["T6_second_seam_jump"] = {"bands": rec2, "jump": float(jump),
                                      "se": sej2,
                                      "significant": bool(abs(jump) > 2 * sej2)}
    else:
        out["T6_second_seam_jump"] = {"bands": rec2, "jump": None}

    with open(os.path.join(HERE, "stratification_theory.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written stratification_theory.json")


if __name__ == "__main__":
    main()
