#!/usr/bin/env python3
"""DEVELOPMENT, on the spent prereg-learned-v1 data. Steps 1-2 of dimension discovery from choices.

The registered GDT metric U (32 x 768, on LaBSE) was learned from which action annotators judged less
ethical, with no named axes. Its right singular vectors are the candidate dimensions: the directions
of embedding space that move the judged cost. Each candidate is then put through the admission screen
of moral-spectrum-analyzer's discovery roadmap (docs/DISCOVERY_ROADMAP.md), the parts that need no
second corpus:

  stability        refit on B bootstrap resamples of the training pairs; for each reference direction,
                   the median over resamples of its best |cosine| with any resample direction.
                   Bar 0.70 (the roadmap's direction-cosine bar). Subspace stability is also reported,
                   since directions with near-equal singular values can rotate into each other.
  non-redundancy   the direction's score on every action text (e . v) against the nine xbse axis
                   scores: max |Pearson r| (roadmap bar < 0.35) and R^2 from all nine together.
  importance       dev log-loss increase when the direction is projected out of the metric.

Cross-corpus replication (the roadmap's third screen) needs a second corpus and is step 3.

    CUDA_VISIBLE_DEVICES=1 python discover_dims.py RAW EMB_DIR CODE_DIR OUT.json [B]
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import torch

K, LAM = 32, 1e-5          # the registered selection (results/results_labse.json)
SEED = 20261031
STAB_BAR, REDUND_BAR = 0.70, 0.35
N_EXEMPLARS = 8


def directions(U):
    _, S, Vt = np.linalg.svd(U, full_matrices=False)
    return S, Vt                                              # rows of Vt: unit directions in embedding space


def main(raw, emb_dir, code_dir, out, B=20):
    sys.path.insert(0, code_dir)
    import fit_learned as FL
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    splits = {"train": FL.load_split(raw, ["train", "train-extra"]), "dev": FL.load_split(raw, ["dev"])}
    seen = {t for r in splits["train"] for t in (r["t0"], r["t1"])}
    splits["dev"] = [r for r in splits["dev"] if r["t0"] not in seen and r["t1"] not in seen]
    emb = FL.Emb(os.path.join(emb_dir, "labse.npz"))
    data = {s: FL.tensors(rows, emb, dev) for s, rows in splits.items()}
    d = data["train"][0].shape[1]
    r0 = torch.cat([data["train"][0], data["train"][1]]).mean(0)

    # reference fit on all training pairs, and its agreement with the registered metric
    ref, info = FL.fit("GDT", d, K, LAM, data["train"], None, r0, SEED)
    U = ref.U.detach().cpu().numpy()
    S, V = directions(U)
    reg = np.load(os.path.join(os.path.dirname(code_dir.rstrip("/")), "out", "gdt_labse.npz"))
    _, Vreg = directions(reg["U"])
    agree_registered = np.abs(V @ Vreg.T).max(1)
    print("reference fit", json.dumps(info), "dev", FL.mean_nll(ref, data["dev"]), flush=True)

    # importance: project each direction out of the metric
    base_dev = FL.mean_nll(ref, data["dev"])
    importance = []
    with torch.no_grad():
        U0 = ref.U.detach().clone()
        for i in range(K):
            v = torch.tensor(V[i], device=dev, dtype=U0.dtype)
            ref.U.copy_(U0 - (U0 @ v)[:, None] * v[None, :])
            importance.append(FL.mean_nll(ref, data["dev"]) - base_dev)
        ref.U.copy_(U0)

    # stability over bootstrap resamples of training pairs
    rng = np.random.default_rng(SEED)
    n = data["train"][0].shape[0]
    best_cos, sub = [], {str(m): [] for m in (4, 8, 16, 32)}
    for b in range(B):
        idx = torch.tensor(rng.integers(0, n, n), device=dev)
        tr = tuple(t[idx] for t in data["train"])
        mb, ib = FL.fit("GDT", d, K, LAM, tr, None, r0, SEED + 1 + b)
        _, Vb = directions(mb.U.detach().cpu().numpy())
        best_cos.append(np.abs(V @ Vb.T).max(1))
        for m in (4, 8, 16, 32):
            sv = np.linalg.svd(V[:m] @ Vb[:m].T, compute_uv=False)   # cosines of principal angles
            sub[str(m)].append(float(np.mean(sv ** 2)))
        print("bootstrap", b, "converged", ib["converged"], "median best cos", float(np.median(best_cos[-1])), flush=True)
    stab = np.median(np.array(best_cos), 0)

    # redundancy against the nine xbse axes, over every action text
    xz = np.load(os.path.join(emb_dir, "xbse_scores.npz"), allow_pickle=True)
    xdims = xz["dims"].tolist()
    xi = {t: i for i, t in enumerate(xz["texts"].tolist())}
    texts = [t for t in emb.index if t in xi]
    E = emb(texts)
    X = xz["scores"][[xi[t] for t in texts]].astype(float)
    Xc = np.c_[np.ones(len(X)), (X - X.mean(0)) / X.std(0)]
    dims = []
    for i in range(K):
        s = E @ V[i]
        r = [float(np.corrcoef(s, X[:, j])[0, 1]) for j in range(X.shape[1])]
        beta, *_ = np.linalg.lstsq(Xc, s, rcond=None)
        resid = s - Xc @ beta
        r2 = 1 - resid.var() / s.var()
        order = np.argsort(s)
        dims.append({"index": i, "singular_value": float(S[i]), "dev_loss_increase_if_removed": float(importance[i]),
                     "stability_median_best_cos": float(stab[i]), "stable": bool(stab[i] >= STAB_BAR),
                     "corr_with_xbse": dict(zip(xdims, r)), "max_abs_corr": float(np.max(np.abs(r))),
                     "nonredundant": bool(np.max(np.abs(r)) < REDUND_BAR), "r2_from_xbse": float(r2),
                     "agreement_with_registered_metric": float(agree_registered[i]),
                     "low_end": [texts[j] for j in order[:N_EXEMPLARS]],
                     "high_end": [texts[j] for j in order[-N_EXEMPLARS:]]})
    res = {"note": "development on spent data; steps 1-2 of dimension discovery", "K": K, "lambda": LAM,
           "bootstraps": B, "reference_dev_nll": base_dev, "subspace_stability_mean_cos2": {m: float(np.median(v)) for m, v in sub.items()},
           "candidates_passing_both_screens": [x["index"] for x in dims if x["stable"] and x["nonredundant"]],
           "directions": dims}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "directions"}, indent=1))
    for x in dims:
        print(x["index"], round(x["singular_value"], 3), "imp", round(x["dev_loss_increase_if_removed"], 5),
              "stab", round(x["stability_median_best_cos"], 3), "maxr", round(x["max_abs_corr"], 3),
              "R2", round(x["r2_from_xbse"], 3), flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:5], *(int(a) for a in sys.argv[5:6]))
