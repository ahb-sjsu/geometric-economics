#!/usr/bin/env python3
"""DEVELOPMENT. Draw the actions the LLM raters will label, for the Hohfeld test of direction 0.

Proportionate stratified sample: N_PER actions drawn at random from each decile of direction 0 over all
action texts, so every decile carries its population share. The texts go to one file and the direction-0
scores to another; the rater script reads only the first.

    python hohfeld_sample.py EMB_DIR OUT_DIR DEST_DIR
"""
import json
import os
import re
import sys

import numpy as np

SEED = 20261031
N_PER = 100
KIN = re.compile(r"\b(mom|mother|dad|father|parents?|sister|brother|grandma|grandpa|family|wife|husband|son|daughter)\b",
                 re.I)                                     # orientation only, as in probe_dir0.py


def main(emb_dir, out_dir, dest):
    lab = np.load(os.path.join(emb_dir, "labse.npz"), allow_pickle=True)
    texts, E = lab["texts"].tolist(), lab["vecs"]
    U = np.load(os.path.join(out_dir, "gdt_labse.npz"))["U"]
    v = np.linalg.svd(U, full_matrices=False)[2][0]
    s = E @ v
    if np.corrcoef(s, [bool(KIN.search(t)) for t in texts])[0, 1] > 0:
        s = -s                                             # harm to close others at the LOW end
    dec = np.minimum((s.argsort().argsort() * 10) // len(s), 9)
    rng = np.random.default_rng(SEED)
    pick = np.concatenate([rng.choice(np.where(dec == d)[0], N_PER, replace=False) for d in range(10)])
    rng.shuffle(pick)                                      # rating order carries no score information
    os.makedirs(dest, exist_ok=True)
    with open(os.path.join(dest, "hohfeld_items.jsonl"), "w", encoding="utf-8") as f:
        for i, j in enumerate(pick):
            f.write(json.dumps({"item": i, "text": texts[j]}) + "\n")
    with open(os.path.join(dest, "hohfeld_scores.jsonl"), "w", encoding="utf-8") as f:
        for i, j in enumerate(pick):
            f.write(json.dumps({"item": i, "text_index": int(j), "dir0": float(s[j]), "decile": int(dec[j])}) + "\n")
    print(f"{len(pick)} items from {len(texts)} texts, seed {SEED}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
