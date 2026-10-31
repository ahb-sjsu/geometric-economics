#!/usr/bin/env python3
"""DEVELOPMENT, on the spent prereg-learned-v1 data (Scruples Dilemmas). Not a registered test.

prereg-learned-v1 found that a cost measured as distance from a learned reference beats a learned
linear scalar (H2). Its own caveat: that shows curvature helps, not that distance from a reference is
the right curvature. The lottery work (strata2) found the data refuse the Euclidean form there. This
asks the same question in a learned high-dimensional space, with the same splits and fitting:

    LIN    logit = b + w.(e0 - e1)
    GDT    C(e) = ||U (e - r)||_2                       registered form
    GDTq   C(e) = (sum_i |U (e - r)|_i^q)^(1/q)         q free in (0.5, 4.5)
    SQD    C(e) = ||U (e - r)||_2^2                     squared distance: a convex quadratic utility,
                                                        the reference folds into its linear term
    QUAD   C(e) = w.e + sum_j s_j (u_j . e)^2            low-rank quadratic with free-sign curvature,
                                                        no reference; same rank, more freedom than SQD

Coordinates: LaBSE, BGE-M3 (the registered and replication encoders) and the nine xbse moral-axis
scores (standardised on train), where k = 9 is full rank.

    CUDA_VISIBLE_DEVICES=1 python explore_learned.py RAW EMB_DIR CODE_DIR OUT.json
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import torch

EPS = 1e-6
LAMBDAS = [0.0, 1e-5, 1e-4]
RESTARTS = 2
STEPS = 3000
LR = 1e-2
SEED = 20261031


class Model(torch.nn.Module):
    def __init__(self, kind, d, k, r0):
        super().__init__()
        self.kind = kind
        self.b = torch.nn.Parameter(torch.zeros(()))
        if kind == "LIN":
            self.w = torch.nn.Parameter(torch.zeros(d))
            return
        self.U = torch.nn.Parameter(torch.randn(k, d) * 0.1)
        if kind in ("GDT", "GDTq", "SQD"):
            self.r = torch.nn.Parameter(r0.clone())
        if kind == "GDTq":
            self.qraw = torch.nn.Parameter(torch.zeros(()))     # q = 0.5 + 4 sigmoid(qraw); starts at 2.5
        if kind == "QUAD":
            self.w = torch.nn.Parameter(torch.zeros(d))
            self.s = torch.nn.Parameter(torch.zeros(k))         # signs and sizes of the curvature

    def q(self):
        return 0.5 + 4 * torch.sigmoid(self.qraw)

    def cost(self, e):
        if self.kind == "QUAD":
            z = e @ self.U.T
            return e @ self.w + (self.s * z * z).sum(-1)
        z = (e - self.r) @ self.U.T
        if self.kind == "GDT":
            return torch.sqrt((z * z).sum(-1) + EPS)
        if self.kind == "SQD":
            return (z * z).sum(-1)
        q = self.q()
        return ((z.abs() + EPS) ** q).sum(-1) ** (1 / q)

    def logit(self, e0, e1):
        if self.kind == "LIN":
            return self.b + (e0 - e1) @ self.w
        return self.b + self.cost(e0) - self.cost(e1)

    def penalty(self):
        if self.kind == "LIN":
            return (self.w ** 2).sum()
        p = (self.U ** 2).sum()
        if self.kind == "QUAD":
            p = p + (self.w ** 2).sum()
        return p


def nll_pp(m, data):
    e0, e1, n0, n1 = data
    z = m.logit(e0, e1)
    return -(n0 * torch.nn.functional.logsigmoid(z) + n1 * torch.nn.functional.logsigmoid(-z))


def mean_nll(m, data):
    with torch.no_grad():
        return float(nll_pp(m, data).sum() / (data[2] + data[3]).sum())


def fit(kind, d, k, lam, train, r0, seed):
    torch.manual_seed(seed)
    m = Model(kind, d, k, r0).to(train[0].device)
    tot = (train[2] + train[3]).sum()
    opt = torch.optim.Adam(m.parameters(), lr=LR)
    for _ in range(STEPS):
        opt.zero_grad()
        loss = nll_pp(m, train).sum() / tot + lam * m.penalty()
        loss.backward()
        opt.step()
    lb = torch.optim.LBFGS(m.parameters(), lr=1.0, max_iter=50, history_size=20, line_search_fn="strong_wolfe")

    def closure():
        lb.zero_grad()
        v = nll_pp(m, train).sum() / tot + lam * m.penalty()
        v.backward()
        return v
    prev, rel = float(closure()), float("inf")
    for _ in range(40):
        cur = float(lb.step(closure))
        rel = abs(prev - cur) / max(abs(prev), 1e-12)
        prev = cur
        if rel < 1e-7:
            break
    return m, {"train_obj": prev, "converged": bool(rel < 1e-5)}


def boot(a, b, w, rng, n=2000):
    d = a - b
    idx = rng.integers(0, len(d), size=(n, len(d)))
    bs = d[idx].sum(1) / w[idx].sum(1)
    return {"mean": float(d.sum() / w.sum()), "ci_low": float(np.percentile(bs, 2.5)),
            "ci_high": float(np.percentile(bs, 97.5))}


class Scores:
    """xbse axis scores as an embedding, standardised with train statistics."""

    def __init__(self, path):
        z = np.load(path, allow_pickle=True)
        self.raw = z["scores"].astype(np.float32)
        self.index = {t: i for i, t in enumerate(z["texts"].tolist())}
        self.vecs = self.raw

    def standardise(self, train_texts):
        idx = [self.index[t] for t in train_texts]
        mu, sd = self.raw[idx].mean(0), self.raw[idx].std(0) + 1e-6
        self.vecs = (self.raw - mu) / sd

    def __call__(self, texts):
        return self.vecs[[self.index[t] for t in texts]]


def main(raw, emb_dir, code_dir, out):
    sys.path.insert(0, code_dir)
    import fit_learned as FL
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    splits = {"train": FL.load_split(raw, ["train", "train-extra"]), "dev": FL.load_split(raw, ["dev"]),
              "test": FL.load_split(raw, ["test"])}
    seen = {t for r in splits["train"] for t in (r["t0"], r["t1"])}
    for s in ("dev", "test"):
        splits[s] = [r for r in splits[s] if r["t0"] not in seen and r["t1"] not in seen]
    encoders = {"labse": ([16, 32, 64], FL.Emb(os.path.join(emb_dir, "labse.npz"))),
                "bgem3": ([16, 32, 64], FL.Emb(os.path.join(emb_dir, "bgem3.npz")))}
    xp = os.path.join(emb_dir, "xbse_scores.npz")
    if os.path.exists(xp):
        sc = Scores(xp)
        sc.standardise([t for r in splits["train"] for t in (r["t0"], r["t1"])])
        encoders["xbse"] = ([9], sc)
    rng = np.random.default_rng(SEED)
    res = {"note": "development on spent data", "n": {s: len(v) for s, v in splits.items()}, "encoders": {}}
    for name, (ks, emb) in encoders.items():
        data = {s: FL.tensors(rows, emb, dev) for s, rows in splits.items()}
        d = data["train"][0].shape[1]
        r0 = torch.cat([data["train"][0], data["train"][1]]).mean(0)
        w_test = (data["test"][2] + data["test"][3]).cpu().numpy()
        grid, best = [], {}
        cfgs = [("LIN", 0)] + [(kd, k) for k in ks for kd in ("GDT", "GDTq", "SQD", "QUAD")]
        for kind, k in cfgs:
            for lam in LAMBDAS:
                cand = None
                for rs in range(1 if kind == "LIN" else RESTARTS):
                    m, info = fit(kind, d, k, lam, data["train"], r0, SEED + rs)
                    if cand is None or info["train_obj"] < cand[1]["train_obj"]:
                        cand = (m, info)
                m, info = cand
                row = {"kind": kind, "k": k, "lambda": lam, **info, "dev_nll": mean_nll(m, data["dev"]),
                       "test_nll": mean_nll(m, data["test"])}
                if kind == "GDTq":
                    row["q"] = float(m.q())
                if kind == "QUAD":
                    row["curvature_signs"] = {"pos": int((m.s > 0).sum()), "neg": int((m.s < 0).sum())}
                grid.append(row)
                print(name, json.dumps(row), flush=True)
                key = (kind, k)
                if key not in best or row["dev_nll"] < best[key][0]["dev_nll"]:
                    best[key] = (row, m)
        # per kind: the k and lambda with the best dev loss
        sel = {}
        for kind in ("LIN", "GDT", "GDTq", "SQD", "QUAD"):
            opts = [v for (kd, _), v in best.items() if kd == kind]
            sel[kind] = min(opts, key=lambda v: v[0]["dev_nll"])
        with torch.no_grad():
            pp = {kd: nll_pp(m, data["test"]).cpu().numpy() for kd, (_, m) in sel.items()}
        comps = {f"{a} minus {b}": boot(pp[a], pp[b], w_test, rng)
                 for a, b in [("GDT", "LIN"), ("GDT", "SQD"), ("GDT", "QUAD"), ("GDTq", "GDT"),
                              ("SQD", "LIN"), ("QUAD", "LIN")]}
        res["encoders"][name] = {"grid": grid, "selected": {kd: v[0] for kd, v in sel.items()}, "test_comparisons": comps}
        print(name, json.dumps({kd: (v[0]["k"], round(v[0]["dev_nll"], 5), round(v[0]["test_nll"], 5))
                                for kd, v in sel.items()}), flush=True)
        print(name, json.dumps(comps), flush=True)
        json.dump(res, open(out, "w"), indent=1)
    print("WROTE", out)


if __name__ == "__main__":
    main(*sys.argv[1:5])
