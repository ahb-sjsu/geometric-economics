#!/usr/bin/env python3
"""EXPLORATORY. Does regime composition explain the corpus disagreement?

**Not part of any registration and it changes no verdict.**

The seam account says the pooled `d*q` chirality is not a structure but an
accounting artifact: at `|d| = 1` the column degenerates into `+/-q`, so a corpus
weighted toward gambles with no loss branch reports a large positive chirality
and a corpus weighted toward mixed gambles reports roughly nothing.

That account makes a sharp prediction about the three estimates this whole line
has been trying to reconcile:

    CPC18 interior, corners dropped              +0.4438
    choices13k aggregate, prereg-d4interior-v3   -0.1216
    peterson2021using, individual choices        +0.2506

**The prediction is that the three pooled values differ because the three corpora
have different regime mixes, and that inside mixed gambles all three agree at
about zero.** If instead the mixed-gamble chirality differs between corpora, the
seam account is wrong and something corpus-specific is real.

CPC18 is used here at the **individual trial level**, which the earlier fits did
not do. `cpc18_raw.csv` carries `SubjID`, `Trial` and `B`, the binary choice, so
first-trial rows are decisions from description with no feedback, directly
comparable to the peterson description arm.

Orientation is risky-minus-safe on every row, as in `stability_rows_v2`, and the
guard is asserted. The coordinate is imported from `d4_rotation` and never
restated.

    python cross_corpus_regimes.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATASETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "datasets"))
V3 = os.path.abspath(os.path.join(HERE, "..", "..", "d4interior", "analysis"))
sys.path.insert(0, DATASETS)
sys.path.insert(0, V3)
sys.path.insert(0, HERE)

from d4_rotation import _opt_coords  # noqa: E402  IMPORTED, never restated
from kappa_mle import TERM_NAMES, _nll_grad_hess, fit  # noqa: E402

_d, _q = _opt_coords(10.0, 1.0, 10.0)
assert abs(_d - 1.0) < 1e-9, "imported _opt_coords is not the expected coordinate"

MIN_CELL = 150


def _z(x):
    s = x.std()
    return (x - x.mean()) / (s if s > 1e-12 else 1.0)


def feats(H, p, L):
    ev = p * H + (1 - p) * L
    var = p * (H - ev) ** 2 + (1 - p) * (L - ev) ** 2
    return float(ev), float(np.sqrt(max(var, 0.0)))


def terms(d, q):
    return np.vstack([np.ones_like(d), d ** 2 + q ** 2, d * q,
                      d, q, d ** 2 - q ** 2])


def fit_design(X, y):
    theta, info = fit(X, y)
    _n, _g, H = _nll_grad_hess(X, y, theta)
    try:
        se = np.sqrt(np.diag(np.linalg.inv(H)))
    except np.linalg.LinAlgError:
        se = np.full(len(theta), np.nan)
    return theta, se, info


def rows_from(recs):
    """recs: iterable of (Ha,pHa,La, Hb,pHb,Lb, y_chose_A). Oriented by risk."""
    out = []
    for Ha, pHa, La, Hb, pHb, Lb, yA in recs:
        evA, sdA = feats(Ha, pHa, La)
        evB, sdB = feats(Hb, pHb, Lb)
        if abs(sdA - sdB) < 1e-12:
            continue
        if sdA >= sdB:
            rk, sf, yr, evr, sdr, evs, sds = (Ha, pHa, La), None, yA, evA, sdA, evB, sdB
        else:
            rk, sf, yr, evr, sdr, evs, sds = (Hb, pHb, Lb), None, 1.0 - yA, evB, sdB, evA, sdA
        H, p, L = rk
        if max(abs(H), abs(L)) <= 1e-12:
            continue
        dc, qc = _opt_coords(H, p, L)
        out.append((evr - evs, sdr - sds, dc, qc, float(yr), H, L))
    A = lambda j: np.array([r[j] for r in out], float)
    return A(0), A(1), A(2), A(3), A(4), A(5), A(6)


def analyse(tag, dEV, dSD, d, q, y, rH, rL, store):
    assert bool((dSD > 0).all()), "%s: orientation guard failed" % tag
    has_loss = np.minimum(rH, rL) < 0
    has_gain = np.maximum(rH, rL) > 0
    regime = np.where(~has_loss, "gain_only",
                      np.where(~has_gain, "loss_only", "mixed"))
    eZ, sZ = _z(dEV), _z(dSD)
    n = len(y)
    frac = {r: float((regime == r).mean()) for r in ("gain_only", "mixed", "loss_only")}

    tp, sep, _ = fit_design(np.vstack([eZ, terms(d, q) * sZ]).T, y)
    pooled = float(tp[1 + TERM_NAMES.index("d*q")])
    pooled_se = float(sep[1 + TERM_NAMES.index("d*q")])

    mixed = regime == "mixed"
    mdq = mdq_se = float("nan")
    md2 = md2_se = float("nan")
    if mixed.sum() >= 200:
        em, sm = _z(dEV[mixed]), _z(dSD[mixed])
        tm, sem, _ = fit_design(
            np.vstack([em, terms(d[mixed], q[mixed]) * sm]).T, y[mixed])
        mdq = float(tm[1 + TERM_NAMES.index("d*q")])
        mdq_se = float(sem[1 + TERM_NAMES.index("d*q")])
        md2 = float(tm[1 + TERM_NAMES.index("d2-q2")])
        md2_se = float(sem[1 + TERM_NAMES.index("d2-q2")])

    print()
    print("%-34s n=%6d   gain_only %.2f  mixed %.2f  loss_only %.2f"
          % (tag, n, frac["gain_only"], frac["mixed"], frac["loss_only"]))
    print("   pooled d*q              %+.4f +/- %.4f" % (pooled, pooled_se))
    print("   d*q INSIDE MIXED        %+.4f +/- %.4f" % (mdq, mdq_se))
    print("   d2-q2 inside mixed      %+.4f +/- %.4f" % (md2, md2_se))
    store[tag] = {"n": int(n), "regime_fraction": frac,
                  "pooled_dq": pooled, "pooled_dq_se": pooled_se,
                  "mixed_dq": mdq, "mixed_dq_se": mdq_se,
                  "mixed_d2q2": md2, "mixed_d2q2_se": md2_se}


def main():
    store = {}
    print("=" * 78)
    print("REGIME COMPOSITION AND THE CHIRALITY, ACROSS CORPORA")
    print("=" * 78)
    print("prediction of the seam account: pooled d*q tracks the gain_only share,")
    print("and d*q inside mixed gambles is near zero in every corpus.")

    # ---- CPC18 at the individual trial level ------------------------------
    c = pd.read_csv(os.path.join(DATASETS, "raw", "cpc18_raw.csv"))
    c = c.dropna(subset=["Ha", "pHa", "La", "Hb", "pHb", "Lb", "B"])
    t1 = c[c["Trial"] == 1]
    two = t1[(t1["LotNumA"] == 1) & (t1["LotNumB"] == 1)]
    for tag, df in (("CPC18 trial 1, all lotteries", t1),
                    ("CPC18 trial 1, two-outcome only", two)):
        recs = [(r.Ha, r.pHa, r.La, r.Hb, r.pHb, r.Lb, 1.0 - float(r.B))
                for r in df.itertuples()]
        analyse(tag, *rows_from(recs), store)

    # ---- choices13k aggregate, the v3 corpus ------------------------------
    k = pd.read_csv(os.path.join(DATASETS, "raw", "choices13k", "c13k_selections.csv"))
    k = k[(k["Block"] == 1) & (k["Feedback"] == 0)].dropna(
        subset=["Ha", "pHa", "La", "Hb", "pHb", "Lb", "bRate"])
    for tag, df in (("choices13k aggregate, all", k),
                    ("choices13k aggregate, two-outcome", k[k["LotNumB"] == 1])):
        recs = [(r.Ha, r.pHa, r.La, r.Hb, r.pHb, r.Lb, 1.0 - float(r.bRate))
                for r in df.itertuples()]
        analyse(tag, *rows_from(recs), store)

    # ---- peterson, for comparison, from the sealed covariates -------------
    from stability_rows_v2 import load_covariates, load_outcome
    dEV, dSD, d, q, pid, fold, scale, part = load_covariates()
    z = np.load(os.path.join(HERE, "seam_covariates.npz"))
    analyse("peterson description, individual", dEV, dSD, d, q,
            load_outcome(), z["risky_H"], z["risky_L"], store)

    # ---- the prediction, stated as a number -------------------------------
    print()
    print("=" * 78)
    print("  corpus                              gain_only   pooled d*q   mixed d*q")
    rows = []
    for tag, v in store.items():
        print("  %-34s  %.2f      %+.4f     %+.4f"
              % (tag, v["regime_fraction"]["gain_only"], v["pooled_dq"], v["mixed_dq"]))
        rows.append((v["regime_fraction"]["gain_only"], v["pooled_dq"], v["mixed_dq"]))
    g = np.array([r[0] for r in rows])
    pdq = np.array([r[1] for r in rows])
    mdq = np.array([r[2] for r in rows])
    ok = ~np.isnan(mdq)
    if ok.sum() >= 3:
        rg = float(np.corrcoef(g, pdq)[0, 1])
        print()
        print("  correlation of pooled d*q with the gain_only share: %+.3f" % rg)
        print("  spread of pooled d*q across corpora: %.4f" % float(pdq.max() - pdq.min()))
        print("  spread of mixed  d*q across corpora: %.4f"
              % float(mdq[ok].max() - mdq[ok].min()))
        store["summary"] = {
            "corr_pooled_dq_with_gain_share": rg,
            "spread_pooled_dq": float(pdq.max() - pdq.min()),
            "spread_mixed_dq": float(mdq[ok].max() - mdq[ok].min())}
    print("=" * 78)

    with open(os.path.join(HERE, "cross_corpus_regimes.json"), "w",
              encoding="utf-8") as fh:
        json.dump(store, fh, indent=2)
    print("written cross_corpus_regimes.json")


if __name__ == "__main__":
    main()
