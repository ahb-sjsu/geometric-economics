#!/usr/bin/env python3
"""Embed every text the study uses with one frozen sentence encoder. Runs on Atlas.

    CUDA_VISIBLE_DEVICES=1 python3 embed.py --model labse --raw /archive/experiments/learned-coords/raw/dilemmas --out /archive/experiments/learned-coords/emb

Writes <out>/<model>.npz with `vecs` (float32, unit norm) and `texts` (the
strings, in row order), plus <model>.meta.json recording the encoder's resolved
snapshot hash. The hash is what V1 checks: a run with a different snapshot is void.
"""
from __future__ import annotations

import argparse
import glob
import json
import os

import numpy as np

MODELS = {
    "labse": "sentence-transformers/LaBSE",
    "bgem3": "BAAI/bge-m3",
}
HERE = os.path.dirname(os.path.abspath(__file__))


def all_texts(raw: str) -> list[str]:
    texts: set[str] = set()
    for path in sorted(glob.glob(os.path.join(raw, "*.scruples-dilemmas.jsonl"))):
        with open(path, encoding="utf-8") as f:
            for line in f:
                for a in json.loads(line)["actions"]:
                    texts.add(a["description"])
    inp = json.load(open(os.path.join(HERE, "inputs.json"), encoding="utf-8"))
    for a in inp["anchors"]:
        texts.update([a["zero"], a["one"]])
    for p in inp["panel"]:
        for pole in p["poles"].values():
            texts.update(pole.values())
    return sorted(texts)


def snapshot(name: str) -> str:
    root = os.path.expanduser("~/.cache/huggingface/hub/models--" + name.replace("/", "--"))
    ref = os.path.join(root, "refs", "main")
    return open(ref).read().strip() if os.path.exists(ref) else "UNKNOWN"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=sorted(MODELS), required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    from sentence_transformers import SentenceTransformer

    name = MODELS[args.model]
    texts = all_texts(args.raw)
    enc = SentenceTransformer(name, device="cuda")
    vecs = enc.encode(texts, batch_size=256, normalize_embeddings=True,
                      convert_to_numpy=True, show_progress_bar=False).astype(np.float32)
    os.makedirs(args.out, exist_ok=True)
    np.savez(os.path.join(args.out, f"{args.model}.npz"), vecs=vecs,
             texts=np.array(texts, dtype=object))
    meta = {"model": name, "snapshot": snapshot(name), "n_texts": len(texts),
            "dim": int(vecs.shape[1])}
    json.dump(meta, open(os.path.join(args.out, f"{args.model}.meta.json"), "w"), indent=1)
    print(json.dumps(meta))


if __name__ == "__main__":
    main()
