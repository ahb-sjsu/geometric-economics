#!/usr/bin/env python3
"""Grader for prereg-d4stability-v1. Written BEFORE any fit touched the choices.

The bars live here and nowhere else. `d4stab_fit_v1.py` computes numbers and
decides nothing.

  W1  composition sensitivity. permutation p < 0.05 on Cochran's Q against
      random splits of the same fold sizes. `c2` moves with stimulus scale by
      more than resampling alone explains. The statistic is studentised because
      an unweighted spread gave a size of 0.110 against a nominal 0.05, the
      scale folds being of unequal precision where random folds are not.
  W2  sufficiency. the observed range across the four folds is at least
      0.5653585378279767, the CPC18 estimate minus the choices13k estimate. one
      corpus split by composition then moves `c2` by as much as the
      between-corpus disagreement, which therefore needs no further explanation.
  W3  sign instability. the four fold estimates are not all of one sign.

Reported separately. **No composite verdict is registered.**

The falsifier that costs us something is F1. If W1 fails, `c2` is stable against
this axis inside this corpus, the between-corpus disagreement is a real
corpus-level difference, and the cheap close is unavailable. That outcome sends
the line to the designed grid and a study that has to be run.

    python d4stab_grade_v1.py results_stability_v1.json
"""
from __future__ import annotations

import json
import os
import sys

ALPHA = 0.05                          # W1, one-sided permutation p
GAP = 0.5653585378279767              # W2, CPC18 minus choices13k
CPC18 = 0.4437750481416212
C13K = -0.12158348968635554
GRAD_TOL = 1e-5                       # F3, infinity norm of the gradient

# The seal hash is READ from the seal file rather than stored here. v3 kept its
# grader out of the bundle because the grader carried the hash, which left the
# bars themselves outside the seal and resting on the signed tag alone. Reading
# the hash instead removes the circularity and lets this file, and so every bar
# in it, be hashed with the rest.
SEAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "prereg-d4stability-v1.sha256")


def bundle_sha():
    try:
        with open(SEAL, encoding="utf-8") as fh:
            return json.load(fh)["combined_sha256"]
    except (OSError, ValueError, KeyError):
        return "SEAL FILE NOT READABLE"


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "results_stability_v1.json"
    with open(path, encoding="utf-8") as fh:
        r = json.load(fh)

    grads = list(r["grad_by_fold"]) + [r["grad_whole_corpus"]]
    void = (max(grads) > GRAD_TOL) or (not r["converged_all_folds"])

    c2s = r["c2_by_fold"]
    w1 = r["permutation_p"] < ALPHA
    w2 = r["range"] >= GAP
    w3 = not (all(c > 0 for c in c2s) or all(c < 0 for c in c2s))

    out = {
        "prereg": "prereg-d4stability-v1",
        "bundle_sha256": bundle_sha(),
        "corpus": r["corpus"],
        "void": void,
        "max_grad_inf_norm": max(grads),
        "c2_by_fold": c2s,
        "c2_whole_corpus": r["c2_whole_corpus"],
        "Q": r["Q"],
        "se_by_fold": r["se_by_fold"],
        "spread_reported_not_tested": r["spread"],
        "range": r["range"],
        "permutation_p": r["permutation_p"],
        "W1_composition_sensitivity": {
            "bar": "permutation p on Q < %.2f" % ALPHA,
            "value": r["permutation_p"], "pass": bool(w1)},
        "W2_sufficiency": {
            "bar": "range >= %.16f" % GAP,
            "value": r["range"], "pass": bool(w2)},
        "W3_sign_instability": {
            "bar": "fold estimates not all of one sign",
            "value": c2s, "pass": bool(w3)},
        "reference": {"cpc18": CPC18, "choices13k": C13K, "gap": GAP},
    }

    if void:
        out["verdict"] = "VOID under F3, gradient tolerance not met"
    else:
        out["verdict"] = "W1 %s, W2 %s, W3 %s" % (
            "PASS" if w1 else "FAIL",
            "PASS" if w2 else "FAIL",
            "PASS" if w3 else "FAIL")
        if not w1:
            out["F1"] = ("W1 FAILED. c2 is stable against outcome scale inside "
                         "this corpus. The CPC18 and choices13k disagreement is "
                         "a real corpus-level difference and is not explained "
                         "by stimulus composition on this axis. The question is "
                         "NOT closed and the designed grid is the next step.")
        if w1 and not w2:
            out["F2"] = ("W1 passed and W2 failed. Composition moves c2, but by "
                         "less than the between-corpus gap. That is a partial "
                         "explanation and must not be reported as closing the "
                         "question.")

    print(json.dumps(out, indent=2))
    with open("grade_stability_v1.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
