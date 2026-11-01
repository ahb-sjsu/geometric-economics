#!/usr/bin/env python3
"""LeBSE v2 — citation-supervised (SPECTER-style) fine-tune of LaBSE.

Positive pair = (citing opinion body, cited opinion body) from the CourtListener citation graph:
real legal-relatedness supervision, unlike v1's unsupervised SimCSE dropout. MultipleNegativesRanking
Loss treats the rest of the batch as negatives, so **batch size = number of negatives = the main
quality lever** — hence NRP A100/H100 with a large batch.

Reads pairs JSONL: one {"a": citing_snip, "b": cited_snip} per line. Runs on any CUDA GPU.

  python3 lebse_v2_train.py --pairs pairs_train.jsonl --batch 256 --epochs 2 --out ./lebse-v2
"""
import argparse
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load_pairs(path, limit, InputExample):
    ex = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            a, b = d.get("a"), d.get("b")
            if a and b:
                ex.append(InputExample(texts=[a, b]))
            if limit and len(ex) >= limit:
                break
    return ex


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--limit", type=int, default=0, help="cap pairs (0 = all)")
    ap.add_argument("--base", default="sentence-transformers/LaBSE")
    ap.add_argument("--batch", type=int, default=256, help="= #in-batch negatives; bigger is better")
    ap.add_argument("--max-seq-len", type=int, default=128, help="truncate tokens (memory vs context)")
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--out", default="./lebse-v2")
    a = ap.parse_args()

    import torch
    from sentence_transformers import InputExample, SentenceTransformer, losses
    from torch.utils.data import DataLoader

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    gpu = torch.cuda.get_device_name(0) if dev == "cuda" else "cpu"
    print(f"[v2] device={dev} gpu={gpu} base={a.base}", flush=True)

    train = load_pairs(a.pairs, a.limit, InputExample)
    print(f"[v2] {len(train):,} citation pairs; batch={a.batch} epochs={a.epochs}", flush=True)
    model = SentenceTransformer(a.base, device=dev)
    model.max_seq_length = a.max_seq_len   # cap tokens -> fits A10 24GB at a useful batch
    print(f"[v2] max_seq_length={model.max_seq_length}", flush=True)
    loader = DataLoader(train, batch_size=a.batch, shuffle=True, drop_last=True)
    loss = losses.MultipleNegativesRankingLoss(model)
    steps = (len(train) // a.batch) * a.epochs
    print(f"[v2] {steps} steps -> {a.out}", flush=True)
    model.fit(
        train_objectives=[(loader, loss)],
        epochs=a.epochs,
        warmup_steps=min(500, max(1, steps // 10)),
        optimizer_params={"lr": a.lr},
        show_progress_bar=True,
        output_path=a.out,
        use_amp=(dev == "cuda"),
    )
    print(f"[v2] DONE -> {a.out}", flush=True)


if __name__ == "__main__":
    main()
