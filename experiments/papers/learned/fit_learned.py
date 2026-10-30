#!/usr/bin/env python3
"""Fit and score the learned-coordinates models. Runs on Atlas, GPU 1.

    CUDA_VISIBLE_DEVICES=1 python3 fit_learned.py --model labse --raw RAW --emb EMB --out OUT
    CUDA_VISIBLE_DEVICES=1 python3 fit_learned.py --model labse --raw RAW --emb EMB --out OUT --simulate gdt2
    CUDA_VISIBLE_DEVICES=1 python3 fit_learned.py --model labse --raw RAW --emb EMB --out OUT --simulate lin

The outcome is the Scruples Dilemmas annotation count: of five annotators, how
many marked action 0 as the less ethical one. Every model predicts
p = P(an annotator marks action 0) and is scored by binomial log-loss per
annotation, in nats.

Models (prereg-learned-v1 Section 4):
  M0        logit p = b. Position bias only.
  LIN       logit p = b + w.(e0 - e1). A scalar utility linear in the encoder's
            coordinates. This is the incumbent: one learned scalar.
  GDT_k     logit p = b + C(e0) - C(e1), C(e) = sqrt(|U (e - r)|^2 + eps),
            U is k x d, r is d. Cost is distance from a learned reference
            under a rank-k metric. The temperature is absorbed into U, because
            only P / T^2 is identified (theory Proposition 2).
  ANCHOR    GDT with U = M A, A the 10 codebook anchor axes (unit rows), M a
            free 10 x 10 matrix. The Part I coordinates as text, weights learned.

Selection uses dev only. Test is scored once, after selection, and every test
comparison is a paired bootstrap over test dilemmas.

--simulate replaces the annotation counts by draws from a known model built on
the real embeddings, so the whole chain can be checked before any real label
is read. Simulated runs write to results_sim_<kind>.json and never to
results.json.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import time

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
KS = [1, 2, 4, 8, 16, 32]
LAMBDAS = [0.0, 1e-6, 1e-5, 1e-4, 1e-3]
MARGIN_FRAC = 0.01  # a win must exceed 1% of LIN's dev improvement over M0
RESTARTS = 3
STEPS = 3000
LR = 1e-2
LBFGS_OUTER = 40       # outer L-BFGS steps of up to 50 iterations each
CONV_TOL = 1e-5        # V2: relative loss change over the final outer step
EPS = 1e-6
N_BOOT = 2000
N_NULL = 1000
SEED = 20261030


# ---------------------------------------------------------------- data

def load_split(raw: str, names: list[str]) -> list[dict]:
    rows = []
    for n in names:
        with open(os.path.join(raw, f"{n}.scruples-dilemmas.jsonl"), encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                rows.append({"t0": d["actions"][0]["description"],
                             "t1": d["actions"][1]["description"],
                             "n0": int(d["gold_annotations"][0]),
                             "n1": int(d["gold_annotations"][1])})
    return rows


class Emb:
    def __init__(self, path: str):
        z = np.load(path, allow_pickle=True)
        self.vecs = z["vecs"]
        self.index = {t: i for i, t in enumerate(z["texts"].tolist())}

    def __call__(self, texts: list[str]) -> np.ndarray:
        return self.vecs[[self.index[t] for t in texts]]


def tensors(rows, emb, dev):
    e0 = torch.tensor(emb([r["t0"] for r in rows]), device=dev)
    e1 = torch.tensor(emb([r["t1"] for r in rows]), device=dev)
    n0 = torch.tensor([r["n0"] for r in rows], dtype=torch.float32, device=dev)
    n1 = torch.tensor([r["n1"] for r in rows], dtype=torch.float32, device=dev)
    return e0, e1, n0, n1


# ---------------------------------------------------------------- models

class Model(torch.nn.Module):
    def __init__(self, kind: str, d: int, k: int = 0, anchors: torch.Tensor | None = None,
                 r0: torch.Tensor | None = None):
        super().__init__()
        self.kind, self.k = kind, k
        self.b = torch.nn.Parameter(torch.zeros(()))
        if kind == "LIN":
            self.w = torch.nn.Parameter(torch.zeros(d))
        elif kind == "GDT":
            self.U = torch.nn.Parameter(torch.randn(k, d) * 0.1)
            self.r = torch.nn.Parameter(r0.clone())
        elif kind == "ANCHOR":
            self.register_buffer("A", anchors)
            self.M = torch.nn.Parameter(torch.eye(anchors.shape[0]) + 0.01 * torch.randn(anchors.shape[0], anchors.shape[0]))
            self.r = torch.nn.Parameter(r0.clone())

    def metric(self) -> torch.Tensor:
        return self.U if self.kind == "GDT" else self.M @ self.A

    def cost(self, e):
        z = (e - self.r) @ self.metric().T
        return torch.sqrt((z * z).sum(-1) + EPS)

    def logit(self, e0, e1):
        if self.kind == "M0":
            return self.b.expand(e0.shape[0])
        if self.kind == "LIN":
            return self.b + (e0 - e1) @ self.w
        return self.b + self.cost(e0) - self.cost(e1)

    def penalty(self):
        if self.kind == "LIN":
            return (self.w ** 2).sum()
        if self.kind in ("GDT", "ANCHOR"):
            return (self.metric() ** 2).sum()
        return torch.zeros(())


def nll_per_pair(model, e0, e1, n0, n1):
    z = model.logit(e0, e1)
    return -(n0 * torch.nn.functional.logsigmoid(z) + n1 * torch.nn.functional.logsigmoid(-z))


def mean_nll(model, data) -> float:
    e0, e1, n0, n1 = data
    with torch.no_grad():
        return float(nll_per_pair(model, e0, e1, n0, n1).sum() / (n0 + n1).sum())


def fit(kind, d, k, lam, train, anchors, r0, seed, warm=None) -> tuple[Model, dict]:
    torch.manual_seed(seed)
    dev = train[0].device
    m = Model(kind, d, k, anchors, r0).to(dev)
    if warm is not None:  # start from the rank-k truncation of a larger fit
        with torch.no_grad():
            m.U.copy_(warm[0])
            m.r.copy_(warm[1])
    opt = torch.optim.Adam(m.parameters(), lr=LR)
    e0, e1, n0, n1 = train
    tot = (n0 + n1).sum()
    trace = []
    for step in range(STEPS):
        opt.zero_grad()
        loss = nll_per_pair(m, e0, e1, n0, n1).sum() / tot + lam * m.penalty()
        loss.backward()
        opt.step()
        if step % 100 == 0 or step == STEPS - 1:
            trace.append(float(loss))
    # Refine to convergence with full-batch L-BFGS. Adam alone left LIN short of its
    # optimum at small penalties in the rehearsal, which made the comparison unfair.
    lbfgs = torch.optim.LBFGS(m.parameters(), lr=1.0, max_iter=50, history_size=20,
                              line_search_fn="strong_wolfe")

    def closure():
        lbfgs.zero_grad()
        val = nll_per_pair(m, e0, e1, n0, n1).sum() / tot + lam * m.penalty()
        val.backward()
        return val
    prev = float(closure())
    rel = float("inf")
    for _ in range(LBFGS_OUTER):
        cur = float(lbfgs.step(closure))
        rel = abs(prev - cur) / max(abs(prev), 1e-12)
        prev = cur
        if rel < 1e-7:
            break
    trace.append(prev)
    converged = rel < CONV_TOL
    return m, {"final_loss": prev, "converged": bool(converged), "final_rel_change": rel}


# ---------------------------------------------------------------- inference

def paired_boot(a: np.ndarray, b: np.ndarray, w: np.ndarray, rng) -> dict:
    """Mean of per-annotation NLL difference a - b over pairs, bootstrap by pair."""
    diff = a - b
    n = len(diff)
    stat = diff.sum() / w.sum()
    idx = rng.integers(0, n, size=(N_BOOT, n))
    boots = diff[idx].sum(1) / w[idx].sum(1)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return {"mean": float(stat), "ci_low": float(lo), "ci_high": float(hi),
            "se": float(boots.std(ddof=1))}


def per_pair(model, data) -> np.ndarray:
    with torch.no_grad():
        return nll_per_pair(model, *data).cpu().numpy()


def subspace_alignment(U: np.ndarray, A: np.ndarray, cov: np.ndarray, rng) -> dict:
    """Mean squared cosine of principal angles between span(U) and span(A),
    against random subspaces of the same dimension drawn with the embedding
    covariance (embeddings are anisotropic, so an isotropic null is too easy)."""
    def basis(X):
        q, _ = np.linalg.qr(X.T)
        return q
    QA = basis(A)

    def stat(QU):
        return float((np.linalg.norm(QU.T @ QA) ** 2) / QU.shape[1])
    QU = basis(U)
    obs = stat(QU)
    L = np.linalg.cholesky(cov + 1e-6 * np.eye(cov.shape[0]))
    null = [stat(basis((L @ rng.standard_normal((cov.shape[0], U.shape[0]))).T))
            for _ in range(N_NULL)]
    per_axis = (np.linalg.norm(QU.T @ (A / np.linalg.norm(A, axis=1, keepdims=True)).T, axis=0) ** 2)
    return {"stat": obs, "null_p99": float(np.percentile(null, 99)),
            "null_mean": float(np.mean(null)), "per_axis_in_span": per_axis.tolist()}


def panel_transfer(model, emb, inputs, dev) -> list[dict]:
    """Zero-fit prediction of the sign of P(A|hi) - P(A|lo) for each panel contrast.
    P(choose A) rises with C_B - C_A, so the predicted sign is that of
    D_hi - D_lo with D = C_B - C_A. Nothing is fit to panel data."""
    out = []
    for p in inputs["panel"]:
        D = {}
        for pole in ("lo", "hi"):
            ea = torch.tensor(emb([p["poles"][pole]["A"]]), device=dev)
            eb = torch.tensor(emb([p["poles"][pole]["B"]]), device=dev)
            with torch.no_grad():
                if model.kind == "LIN":
                    D[pole] = float((eb - ea) @ (-model.w))
                else:
                    D[pole] = float(model.cost(eb) - model.cost(ea))
        out.append({"id": p["id"], "kind": p["kind"], "pred": D["hi"] - D["lo"]})
    return out


# ---------------------------------------------------------------- simulation

def simulate(kind, rows_by_split, emb, rng):
    """Replace annotation counts by Binomial(5, p) draws from a known model."""
    d = emb.vecs.shape[1]
    allv = emb.vecs
    if kind == "gdt2":
        U = rng.standard_normal((2, d)) * 4.0
        r = allv.mean(0) + 0.05 * rng.standard_normal(d)
        def logit(e0, e1):
            c0 = np.sqrt((((e0 - r) @ U.T) ** 2).sum(1))
            c1 = np.sqrt((((e1 - r) @ U.T) ** 2).sum(1))
            return c0 - c1
    elif kind == "lin":
        w = rng.standard_normal(d) * 2.0
        def logit(e0, e1):
            return (e0 - e1) @ w
    else:
        raise SystemExit(f"unknown simulation {kind}")
    for rows in rows_by_split.values():
        e0 = emb([r["t0"] for r in rows])
        e1 = emb([r["t1"] for r in rows])
        p = 1 / (1 + np.exp(-logit(e0, e1)))
        n0 = rng.binomial(5, p)
        for row, a in zip(rows, n0):
            row["n0"], row["n1"] = int(a), int(5 - a)
    return {"truth": kind}


# ---------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--emb", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--simulate", default=None, choices=[None, "gdt2", "lin"])
    ap.add_argument("--quick", action="store_true", help="rehearsal only: fewer steps")
    args = ap.parse_args()

    global STEPS, N_NULL
    if args.quick:
        if not args.simulate:
            raise SystemExit("--quick is for simulated rehearsal only")
        STEPS, N_NULL = 800, 200

    rng = np.random.default_rng(SEED)
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    emb = Emb(os.path.join(args.emb, f"{args.model}.npz"))
    meta = json.load(open(os.path.join(args.emb, f"{args.model}.meta.json")))
    inputs = json.load(open(os.path.join(HERE, "inputs.json"), encoding="utf-8"))

    splits = {"train": load_split(args.raw, ["train", "train-extra"]),
              "dev": load_split(args.raw, ["dev"]),
              "test": load_split(args.raw, ["test"])}
    # Held out means unseen actions: drop any dev/test pair sharing an action with train.
    seen = {t for r in splits["train"] for t in (r["t0"], r["t1"])}
    dropped = {}
    for s in ("dev", "test"):
        keep = [r for r in splits[s] if r["t0"] not in seen and r["t1"] not in seen]
        dropped[s] = len(splits[s]) - len(keep)
        splits[s] = keep
    sim = simulate(args.simulate, splits, emb, rng) if args.simulate else None

    data = {s: tensors(rows, emb, dev) for s, rows in splits.items()}
    d = emb.vecs.shape[1]
    A_np = np.stack([emb([a["one"]])[0] - emb([a["zero"]])[0] for a in inputs["anchors"]])
    A_np = A_np / np.linalg.norm(A_np, axis=1, keepdims=True)
    A = torch.tensor(A_np, device=dev)
    train_e = torch.cat([data["train"][0], data["train"][1]])
    r0 = train_e.mean(0)

    t0 = time.time()
    grid = []
    cfgs = [("M0", 0, 0.0)] + [("LIN", 0, l) for l in LAMBDAS] \
        + [("ANCHOR", 10, l) for l in LAMBDAS] + [("GDT", k, l) for k in sorted(KS, reverse=True) for l in LAMBDAS]
    fitted = {}
    for kind, k, lam in cfgs:
        best = None
        starts = [(SEED + rs, None) for rs in range(RESTARTS if kind in ("GDT", "ANCHOR") else 1)]
        if kind == "GDT" and k < max(KS):
            # The cost is not convex, and in the rehearsal random starts left a true
            # rank-2 metric in a local optimum. Add a start from the top-k singular
            # directions of the largest-rank fit at the same penalty. The start with
            # the lowest training loss is kept, so this uses training data only.
            big = fitted[("GDT", max(KS), lam)]
            Ub = big.U.detach()
            _, S, Vh = torch.linalg.svd(Ub, full_matrices=False)
            starts.append((SEED, ((S[:k, None] * Vh[:k]), big.r.detach())))
        for seed, warm in starts:
            m, info = fit(kind, d, k, lam, data["train"], A, r0, seed, warm)
            info["start"] = "random" if warm is None else "svd_of_k_max"
            if best is None or info["final_loss"] < best[1]["final_loss"]:
                best = (m, info)
        m, info = best
        row = {"kind": kind, "k": k, "lambda": lam, **info,
               "train_nll": mean_nll(m, data["train"]), "dev_nll": mean_nll(m, data["dev"])}
        grid.append(row)
        fitted[(kind, k, lam)] = m
        print(json.dumps(row), flush=True)

    def pick(kind, k=None):
        rows = [g for g in grid if g["kind"] == kind and (k is None or g["k"] == k)]
        return min(rows, key=lambda g: g["dev_nll"])

    sel = {"M0": pick("M0"), "LIN": pick("LIN"), "ANCHOR": pick("ANCHOR")}
    by_k = {k: pick("GDT", k) for k in KS}
    best_k = min(by_k.values(), key=lambda g: g["dev_nll"])
    # The margin. GDT contains LIN as the limit of a distant reference, so a tiny
    # but consistent difference is not a win. Every comparison and the k* rule
    # use this floor, fixed from dev before test is scored.
    margin = MARGIN_FRAC * (sel["M0"]["dev_nll"] - sel["LIN"]["dev_nll"])
    # k*: smallest k whose dev NLL is within max(one paired-bootstrap SE, margin) of the best.
    w_dev = (data["dev"][2] + data["dev"][3]).cpu().numpy()
    best_pp = per_pair(fitted[(best_k["kind"], best_k["k"], best_k["lambda"])], data["dev"])
    k_star = None
    k_dev = {}
    for k in KS:
        g = by_k[k]
        pp = per_pair(fitted[("GDT", k, g["lambda"])], data["dev"])
        bt = paired_boot(pp, best_pp, w_dev, rng)
        k_dev[k] = {"dev_nll": g["dev_nll"], "minus_best": bt}
        if k_star is None and bt["mean"] <= max(bt["se"], margin):
            k_star = k
    sel["GDT"] = by_k[k_star]

    # ---- test, scored once
    w_test = (data["test"][2] + data["test"][3]).cpu().numpy()
    tm = {name: fitted[(g["kind"], g["k"], g["lambda"])] for name, g in sel.items()}
    tpp = {name: per_pair(m, data["test"]) for name, m in tm.items()}
    test_nll = {name: float(v.sum() / w_test.sum()) for name, v in tpp.items()}
    comps = {f"GDT-{b}": paired_boot(tpp["GDT"], tpp[b], w_test, rng) for b in ("LIN", "ANCHOR", "M0")}

    cov = np.cov(train_e.cpu().numpy().T)
    align = subspace_alignment(tm["GDT"].metric().detach().cpu().numpy(), A_np, cov, rng)
    transfer = {"GDT": panel_transfer(tm["GDT"], emb, inputs, dev),
                "LIN": panel_transfer(tm["LIN"], emb, inputs, dev)}

    result = {"prereg": "prereg-learned-v1", "encoder": meta, "simulation": sim,
              "n": {s: len(r) for s, r in splits.items()}, "dropped_overlap": dropped, "grid": grid,
              "k_dev": {str(k): v for k, v in k_dev.items()}, "k_star": k_star,
              "selected": sel, "margin": margin, "test_nll": test_nll, "test_comparisons": comps,
              "reference_offset": float(torch.linalg.norm(tm["GDT"].r - r0)),
              "alignment": align, "anchor_axes": [a["axis"] for a in inputs["anchors"]],
              "panel_transfer": transfer, "seconds": round(time.time() - t0, 1)}
    os.makedirs(args.out, exist_ok=True)
    name = f"results_sim_{args.simulate}_{args.model}.json" if args.simulate else f"results_{args.model}.json"
    json.dump(result, open(os.path.join(args.out, name), "w"), indent=1)
    if not args.simulate:
        U = tm["GDT"].metric().detach().cpu().numpy()
        np.savez(os.path.join(args.out, f"gdt_{args.model}.npz"), U=U,
                 r=tm["GDT"].r.detach().cpu().numpy())
    print("WROTE", name, json.dumps({"k_star": k_star, "test_nll": test_nll}))


if __name__ == "__main__":
    main()
