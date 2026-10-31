#!/usr/bin/env python3
"""DEVELOPMENT. Is discovered direction 0 moral-spectrum-analyzer's general-valence factor?

Two versions of general valence are checked, because moral-spectrum-analyzer uses both:
    pc0  the first principal component of the nine xbse axis scores (SPECTRUM_FINDINGS, DISCOVERY_ROADMAP)
    G    the trained general-valence channel, xbse feeder `general_valence_joint` (gate AUROC 0.868)
The discovered directions are the right singular vectors of the registered GDT metric
(out/gdt_labse.npz); discover_dims.py found its refit agrees with them at |cos| = 1.00 for the top 3.

For each of the top directions: Pearson r with G and with pc0 over all 27,982 action texts, and R^2
from (nine axes), (nine axes + G). Direction 0 is "general valence rediscovered" if |r| with G or pc0
is large; it is new structure if R^2 from nine axes + G stays low.

    CUDA_VISIBLE_DEVICES=1 python check_valence.py EMB_DIR OUT_DIR OUT.json
"""
import json
import os
import sys

os.environ.setdefault("HF_HOME", "/archive/cache/huggingface")
HOME = os.path.expanduser("~")
sys.path.insert(0, f"{HOME}/xbse/src")

import numpy as np  # noqa: E402
import torch  # noqa: E402
from xbse.encoder import BSEEncoder  # noqa: E402
from xbse.instances.joint_builders import BUILDERS  # noqa: E402
from xbse.report import Report  # noqa: E402
from xbse.scorer import DimensionScorer, _np  # noqa: E402

FEEDER = "general_valence_joint"
SEEDS = ["s0", "s1", "s2"]          # s0 is the calibrated production channel (has the calibration backup)
TOP = 6


def r2(y, X):
    Xc = np.c_[np.ones(len(X)), (X - X.mean(0)) / X.std(0)]
    beta, *_ = np.linalg.lstsq(Xc, y, rcond=None)
    return float(1 - (y - Xc @ beta).var() / y.var())


def main(emb_dir, out_dir, out):
    lab = np.load(os.path.join(emb_dir, "labse.npz"), allow_pickle=True)
    texts, E = lab["texts"].tolist(), lab["vecs"]
    xz = np.load(os.path.join(emb_dir, "xbse_scores.npz"), allow_pickle=True)
    assert xz["texts"].tolist() == texts, "xbse scores must be in the LaBSE text order"
    X = xz["scores"].astype(float)

    Gs, meta = {}, {}
    for seed in SEEDS:
        rep = Report(**json.load(open(f"{HOME}/xbse_ckpt/{FEEDER}_report_{seed}.json")))
        src = BUILDERS[FEEDER]()
        enc = BSEEncoder(base_model="BAAI/bge-m3", max_len=src.max_len, device="cuda")
        enc.load_state_dict(torch.load(f"{HOME}/xbse_ckpt/{FEEDER}_{seed}.pt", map_location="cuda"))
        enc.eval()
        sc = DimensionScorer.from_pairsource(enc, src, rep, rep.checkpoint_hash)
        g = np.empty(len(texts))
        with torch.no_grad():
            for i in range(0, len(texts), 128):
                g[i:i + 128] = (_np(enc.encode(texts[i:i + 128])) @ sc.axis - sc.center) / sc.scale
        Gs[seed] = g
        meta[seed] = {"passed": bool(rep.passed), "checkpoint_hash": rep.checkpoint_hash}
        del enc
        torch.cuda.empty_cache()
    G = Gs["s0"]

    Xs = (X - X.mean(0)) / X.std(0)
    w, vecs = np.linalg.eigh(np.cov(Xs.T))
    pc0 = Xs @ vecs[:, -1]
    U = np.load(os.path.join(out_dir, "gdt_labse.npz"))["U"]
    _, S, Vt = np.linalg.svd(U, full_matrices=False)

    res = {"G_seeds": meta, "corr_between_G_seeds": {f"{a}-{b}": float(np.corrcoef(Gs[a], Gs[b])[0, 1]) for a, b in (("s0", "s1"), ("s0", "s2"), ("s1", "s2"))},
           "pc0_variance_share": float(w[-1] / w.sum()),
           "pc0_loadings": dict(zip(xz["dims"].tolist(), vecs[:, -1].round(3).tolist())),
           "corr_G_pc0": float(np.corrcoef(G, pc0)[0, 1]), "directions": []}
    for i in range(TOP):
        s = E @ Vt[i]
        res["directions"].append({
            "index": i, "singular_value": float(S[i]),
            "r_with_G": float(np.corrcoef(s, G)[0, 1]), "r_with_G_seeds": {k: float(np.corrcoef(s, v)[0, 1]) for k, v in Gs.items()}, "r_with_pc0": float(np.corrcoef(s, pc0)[0, 1]),
            "R2_nine_axes": r2(s, X), "R2_nine_axes_plus_G": r2(s, np.c_[X, G])})
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
