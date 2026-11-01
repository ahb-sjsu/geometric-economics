#!/usr/bin/env python3
"""Held-out eval of LeBSE-v2 vs base LaBSE from a citation-pairs JSONL (NO database needed).

The eval pairs are true (citing, cited) body snippets whose opinions are disjoint from training
(id %% 10 == 7). Positive = the true pair; negative = a random cross-pairing (a_i, b_j), i != j.
Citation-pair AUROC = P(true pair scores higher than a random pair). Also reports anisotropy and a
paired bootstrap CI on the AUROC gain. numpy-only (no sklearn) so it runs anywhere.

  python3 lebse_v2_eval.py --pairs pairs_eval.jsonl --base sentence-transformers/LaBSE --lebse ./lebse-v2
"""
import argparse
import json
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load(path, limit):
    A, B = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get("a") and d.get("b"):
                A.append(d["a"])
                B.append(d["b"])
            if limit and len(A) >= limit:
                break
    return A, B


def auroc(pos, neg):
    """Rank-based AUROC = P(pos > neg) (Mann-Whitney U). numpy-only, tie-aware."""
    pos = np.asarray(pos, float)
    neg = np.asarray(neg, float)
    s = np.r_[pos, neg]
    order = s.argsort(kind="mergesort")
    ranks = np.empty(len(s), float)
    sr = s[order]
    i = 0
    while i < len(s):  # average ranks over ties
        j = i
        while j + 1 < len(s) and sr[j + 1] == sr[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    npos, nneg = len(pos), len(neg)
    return (ranks[:npos].sum() - npos * (npos + 1) / 2.0) / (npos * nneg)


def deranged(n, rng):
    p = rng.permutation(n)
    fixed = np.where(p == np.arange(n))[0]
    if len(fixed) > 1:
        p[fixed] = p[np.roll(fixed, 1)]
    elif len(fixed) == 1:
        k = fixed[0]
        j = (k + 1) % n
        p[k], p[j] = p[j], p[k]
    return p


def eval_model(name, model, A, B, rng):
    ea = model.encode(A, batch_size=128, convert_to_numpy=True, normalize_embeddings=True,
                      show_progress_bar=False)
    eb = model.encode(B, batch_size=128, convert_to_numpy=True, normalize_embeddings=True,
                      show_progress_bar=False)
    pos = np.sum(ea * eb, axis=1)
    perm = deranged(len(B), rng)
    neg = np.sum(ea * eb[perm], axis=1)
    au = auroc(pos, neg)
    print(f"[{name}] cite_auroc={au:.4f}  mean_pos_cos={pos.mean():.4f}  "
          f"mean_neg_cos(anisotropy)={neg.mean():+.4f}", flush=True)
    return {"name": name, "auroc": au, "pos": pos, "neg": neg}


def bootstrap(rl, rb, rng, n=2000):
    diffs = np.empty(n)
    m = len(rl["pos"])
    for k in range(n):
        idx = rng.integers(0, m, m)
        diffs[k] = auroc(rl["pos"][idx], rl["neg"][idx]) - auroc(rb["pos"][idx], rb["neg"][idx])
    return float(diffs.mean()), float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--base", default="sentence-transformers/LaBSE")
    ap.add_argument("--lebse", default="./lebse-v2")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    import torch
    from sentence_transformers import SentenceTransformer

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    A, B = load(a.pairs, a.limit)
    print(f"[eval] {len(A)} held-out citation pairs; device={dev}", flush=True)

    base = SentenceTransformer(a.base, device=dev)
    lebse = SentenceTransformer(a.lebse, device=dev)
    rb = eval_model("LaBSE", base, A, B, np.random.default_rng(1))
    rl = eval_model("LeBSE-v2", lebse, A, B, np.random.default_rng(1))

    md, lo, hi = bootstrap(rl, rb, np.random.default_rng(7))
    sig = lo > 0 or hi < 0
    print("\n==================== VERDICT ====================")
    print(f"  cite_auroc   LaBSE {rb['auroc']:.4f}  ->  LeBSE-v2 {rl['auroc']:.4f}")
    print(f"  d(cite_auroc) = {md:+.4f}  95% CI [{lo:+.4f}, {hi:+.4f}]  "
          f"{'SIGNIFICANT' if sig else 'not significant'}")
    print(f"  => LeBSE-v2 {'IMPROVES' if (md > 0 and lo > 0) else 'does NOT improve'} "
          "held-out legal citation retrieval.")
    print("=================================================")


if __name__ == "__main__":
    main()
