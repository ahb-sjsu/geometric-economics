#!/usr/bin/env python3
"""DEVELOPMENT. Score every Scruples action text on the nine graded xbse moral axes.

Each axis is its own fine-tuned BGE-M3 encoder (xbse, `~/xbse_ckpt/<feeder>.pt`) with a valence
axis fit from its pair source; the score is (z . axis - center) / scale, xbse's DimensionScorer
rule. Axes whose gate report is not `passed` are skipped and listed. Texts are exactly those in
the LaBSE embedding file, in the same order, so rows line up with `fit_learned.Emb`.

    CUDA_VISIBLE_DEVICES=1 python embed_xbse.py EMB_DIR OUT.npz     # on Atlas
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

CKPT = f"{HOME}/xbse_ckpt"
GRADED = [
    ("physical_harm", "physharm_joint"), ("fairness_equity", "fairness_joint"),
    ("autonomy_respect", "autonomy_joint"), ("privacy_protection", "privacy_joint"),
    ("societal_environmental", "environmental_joint"), ("virtue_care", "care_joint"),
    ("legitimacy_trust", "legitimacy_joint"), ("epistemic_quality", "epistemic_joint"),
    ("identity_attack", "identity_attack_joint"),
]
BATCH = 128


def main(emb_dir, out):
    texts = np.load(os.path.join(emb_dir, "labse.npz"), allow_pickle=True)["texts"].tolist()
    print(f"texts {len(texts)}", flush=True)
    scores, dims, skipped, meta = [], [], [], {}
    for dim, feeder in GRADED:
        rep = Report(**json.load(open(f"{CKPT}/{feeder}_report.json")))
        if not rep.passed:
            skipped.append(dim)
            continue
        src = BUILDERS[feeder]()
        enc = BSEEncoder(base_model="BAAI/bge-m3", max_len=src.max_len, device="cuda")
        enc.load_state_dict(torch.load(f"{CKPT}/{feeder}.pt", map_location="cuda"))
        enc.eval()
        sc = DimensionScorer.from_pairsource(enc, src, rep, rep.checkpoint_hash)
        s = np.empty(len(texts), np.float32)
        with torch.no_grad():
            for i in range(0, len(texts), BATCH):
                z = _np(enc.encode(texts[i:i + BATCH]))
                s[i:i + BATCH] = (z @ sc.axis - sc.center) / sc.scale
        scores.append(s); dims.append(dim)
        meta[dim] = {"feeder": feeder, "checkpoint_hash": rep.checkpoint_hash, "mean": float(s.mean()),
                     "sd": float(s.std())}
        print(dim, json.dumps(meta[dim]), flush=True)
        del enc
        torch.cuda.empty_cache()
    np.savez(out, texts=np.array(texts, dtype=object), scores=np.stack(scores, 1), dims=np.array(dims))
    json.dump({"dims": dims, "skipped_not_passed": skipped, "per_dim": meta}, open(out + ".meta.json", "w"), indent=1)
    print("WROTE", out, "skipped", skipped)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
