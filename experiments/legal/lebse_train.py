#!/usr/bin/env python3
"""Train LeBSE -- a legal-domain-adapted LaBSE -- by unsupervised SimCSE fine-tuning on legal
sentences from the CourtListener replica. Runs ON ATLAS, GPU-1 only (GPU-0 hosts artemis).

SimCSE (Gao et al. 2021): each sentence is its own positive pair (two dropout views); other
in-batch sentences are negatives (MultipleNegativesRankingLoss). No labels needed. Result is a
LaBSE encoder whose geometry is tuned to legal register -> feeds the ErisML rule extractor
(canonicalizer model_name) so the moral vectors are computed in legal-aware embedding space.

    CUDA_VISIBLE_DEVICES=1 python3 lebse_train.py --n-opinions 6000 --epochs 1 --out /archive/courtlistener/lebse
"""
import argparse, os, random, re, subprocess, sys

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")   # GPU-1 only; never touch GPU-0 (artemis)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def legal_sentences(n_opinions, max_sent):
    # collapse whitespace so each opinion is one psql line (plain_text has newlines), then split.
    sql = ("SELECT regexp_replace(plain_text, E'\\s+', ' ', 'g') FROM search_opinion "
           "WHERE length(plain_text) BETWEEN 1500 AND 25000 ORDER BY id LIMIT %d;" % n_opinions)
    r = subprocess.run(["sudo", "-u", "postgres", "psql", "-d", "courtlistener", "-tA", "-c", sql],
                       capture_output=True, text=True, timeout=600)
    sents = []
    for line in r.stdout.split("\n"):
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if 40 <= len(s) <= 350 and any(c.isalpha() for c in s):
                sents.append(s)
    random.Random(0).shuffle(sents)
    return sents[:max_sent]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-opinions", type=int, default=6000)
    ap.add_argument("--max-sent", type=int, default=250000)
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--out", default="/archive/courtlistener/lebse")
    a = ap.parse_args()

    import torch
    from sentence_transformers import SentenceTransformer, InputExample, losses
    from torch.utils.data import DataLoader
    print(f"[lebse] cuda={torch.cuda.is_available()} dev={torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu'}")

    sents = legal_sentences(a.n_opinions, a.max_sent)
    print(f"[lebse] {len(sents):,} legal sentences from {a.n_opinions} opinions")
    train = [InputExample(texts=[s, s]) for s in sents]        # SimCSE: same sentence = positive pair
    model = SentenceTransformer("sentence-transformers/LaBSE", device="cuda")
    loader = DataLoader(train, batch_size=a.batch, shuffle=True, drop_last=True)
    loss = losses.MultipleNegativesRankingLoss(model)
    steps = (len(train) // a.batch) * a.epochs
    print(f"[lebse] training {a.epochs} epoch(s), {steps} steps, batch {a.batch} -> {a.out}")
    model.fit(train_objectives=[(loader, loss)], epochs=a.epochs,
              warmup_steps=min(200, steps // 10), show_progress_bar=True,
              output_path=a.out, use_amp=True)
    print(f"[lebse] DONE -> {a.out}")


if __name__ == "__main__":
    main()
