#!/usr/bin/env python3
"""EXPLORATORY. The same analysis on decisions from experience.

**Not part of any registration and it changes no verdict.**

The description arm used `first_press_description`, 96,237 press tokens. The
corpus also holds **384,948 `repeat_press_experience` tokens**: presses two
through five on the same problem, made after outcome feedback on that problem.
Same stimuli, same participants, same session. It is a within-corpus contrast
with no population confound and no stimulus confound, which is rarer than it
sounds and is the reason to run it.

What it tests. The description arm found that the fourfold chirality `d*q` is
zero inside mixed gambles, `-0.0303 +/- 0.0728`, and that the pooled value of
`+0.2506` is manufactured by the unmixed regimes where `d*q` collapses
algebraically to `+/-q`. If that is a fact about the coordinate rather than about
people, it must reproduce here, because the algebra is the same. If the
regime structure itself changes under feedback, that is a fact about people.

Orientation follows `stability_rows_v2`: every row is risky-minus-safe, `dSD > 0`
by construction, and `y = 1` means the participant took the risk. The guard is
asserted here too.

    python experience_arm.py
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

from kappa_mle import TERM_NAMES, _nll_grad_hess, fit  # noqa: E402
from peterson_parse import (PRESS_FIRST, PRESS_REPEAT, feats,  # noqa: E402
                            trials)
from stability_rows_v2 import row_from_menu  # noqa: E402

CACHE = os.path.join(HERE, "experience_rows.npz")
MIN_CELL = 300


def _z(x):
    s = x.std()
    return (x - x.mean()) / (s if s > 1e-12 else 1.0)


def fit_design(X, y):
    theta, info = fit(X, y)
    assert info["converged"], "fit did not converge"
    _n, _g, H = _nll_grad_hess(X, y, theta)
    return theta, np.sqrt(np.diag(np.linalg.inv(H))), info


def terms(d, q):
    return np.vstack([np.ones_like(d), d ** 2 + q ** 2, d * q,
                      d, q, d ** 2 - q ** 2])


def build():
    if os.path.exists(CACHE):
        z = np.load(CACHE)
        return {k: z[k] for k in z.files}
    from datasets import load_dataset
    ds = load_dataset("marcelbinz/Psych-101", split="train")
    rows = [r for r in ds if r["experiment"] == "peterson2021using/exp1.csv"]
    keep = []
    for i, r in enumerate(rows):
        for bucket, a, b, chose_a, idx, had_fb in trials(r["text"]):
            if bucket != PRESS_REPEAT:
                continue
            row, why = row_from_menu(a, b, chose_a)
            if row is None:
                continue
            dEV, dSD, dc, qc, y, scale = row
            evA, sdA = feats(*a)
            evB, sdB = feats(*b)
            risky = a if sdA >= sdB else b
            keep.append((dEV, dSD, dc, qc, y, scale, idx, i,
                         risky[0], risky[2], 1.0 if had_fb else 0.0))
    A = lambda j: np.array([k[j] for k in keep], float)
    out = {"dEV": A(0), "dSD": A(1), "d": A(2), "q": A(3), "y": A(4),
           "scale": A(5), "trial_index": A(6), "participant": A(7),
           "risky_H": A(8), "risky_L": A(9), "had_feedback": A(10)}
    assert bool((out["dSD"] > 0).all()), "orientation guard failed"
    np.savez_compressed(CACHE, **out)
    return out


def report(tag, d, q, eZ, sZ, y, regime, infl, out):
    print()
    print("=" * 72)
    print(tag)
    print("=" * 72)
    for r in ("gain_only", "mixed", "loss_only"):
        print("  %-10s %7d rows" % (r, int((regime == r).sum())))
    Xp = np.vstack([eZ, terms(d, q) * sZ]).T
    tp, sep, _ = fit_design(Xp, y)
    nll_p = _nll_grad_hess(Xp, y, tp)[0]
    print("  POOLED six-term   bEV %+.4f" % tp[0])
    for i, t in enumerate(TERM_NAMES):
        star = "   <== chirality" if t == "d*q" else ""
        print("    %-6s %+.4f +/- %.4f%s" % (t, tp[1 + i], sep[1 + i] * infl, star))

    cols, names = [eZ], ["bEV"]
    for r in ("mixed", "gain_only", "loss_only"):
        m = (regime == r).astype(float)
        if m.sum() < MIN_CELL:
            continue
        basis = ([(t, terms(d, q)[i]) for i, t in enumerate(TERM_NAMES)]
                 if r == "mixed"
                 else [("1", np.ones_like(q)), ("q", q), ("q2", q ** 2)])
        for nm, col in basis:
            cols.append(col * sZ * m)
            names.append("%s:%s" % (r, nm))
    Xr = np.vstack(cols).T
    tr, ser, _ = fit_design(Xr, y)
    nll_r = _nll_grad_hess(Xr, y, tr)[0]
    print("  REGIME-SEPARATED  gain %.1f log-likelihood on %d extra parameters"
          % (nll_p - nll_r, Xr.shape[1] - Xp.shape[1]))
    for j, nm in enumerate(names):
        if nm == "bEV":
            continue
        z = tr[j] / (ser[j] * infl)
        star = ""
        if nm == "mixed:d*q":
            star = "   <== CHIRALITY INSIDE MIXED"
        elif abs(z) > 5:
            star = "   <== dominant"
        print("    %-20s %+.4f +/- %.4f  %+5.1f se%s"
              % (nm, tr[j], ser[j] * infl, z, star))
    out[tag] = {
        "n": int(len(y)),
        "pooled": {t: float(tp[1 + i]) for i, t in enumerate(TERM_NAMES)},
        "pooled_se": {t: float(sep[1 + i] * infl) for i, t in enumerate(TERM_NAMES)},
        "bEV": float(tp[0]),
        "regime": {names[j]: float(tr[j]) for j in range(1, len(names))},
        "regime_se": {names[j]: float(ser[j] * infl) for j in range(1, len(names))},
        "loglik_gain": float(nll_p - nll_r),
        "extra_params": int(Xr.shape[1] - Xp.shape[1])}
    return tp, tr, names


def main():
    with open(os.path.join(HERE, "results_stability_v2.json"), encoding="utf-8") as fh:
        infl = float(np.sqrt(json.load(fh)["null_Q_mean"] / 3.0))
    z = build()
    d, q, y = z["d"], z["q"], z["y"]
    eZ, sZ = _z(z["dEV"]), _z(z["dSD"])
    has_loss = np.minimum(z["risky_H"], z["risky_L"]) < 0
    has_gain = np.maximum(z["risky_H"], z["risky_L"]) > 0
    regime = np.where(~has_loss, "gain_only",
                      np.where(~has_gain, "loss_only", "mixed"))
    print("experience trials: %d" % len(y))
    print("  with a feedback clause on the press line: %d"
          % int(z["had_feedback"].sum()))
    print("  marginal risky rate %.4f" % y.mean())
    print("design-effect inflation carried from the description run: %.3f" % infl)

    out = {"note": "EXPLORATORY, changes no registered verdict"}
    report("EXPERIENCE, all repeat presses", d, q, eZ, sZ, y, regime, infl, out)

    # does it settle as feedback accumulates?
    for ti in (1, 2, 3, 4):
        m = z["trial_index"] == ti
        if m.sum() < 5000:
            continue
        report("EXPERIENCE, press index %d only" % (ti + 1),
               d[m], q[m], _z(z["dEV"][m]), _z(z["dSD"][m]), y[m],
               regime[m], infl, out)

    with open(os.path.join(HERE, "experience_arm.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written experience_arm.json")


if __name__ == "__main__":
    main()
