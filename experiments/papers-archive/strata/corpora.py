#!/usr/bin/env python3
"""Parsers for the prereg-strata-v1 test corpora. One function per corpus, one rule each.

Each parser returns a list of rows (participant, XA, PA, XB, PB, chose_B) and a Counter of
named buckets that must sum to the corpus's raw record count (`assert` in `build`). `build`
writes covariates and outcomes to SEPARATE files, so everything before the seal reads only the
covariates. Option A is the option the source labels A (or 1); B the other.

Decided before any choice was read:
  * zilker2020: "complex safe" trials are excluded (study 1 cond == 2, study 2 typeB == "B2"),
    because the sure amount is shown as an arithmetic expression, not a stated lottery.
  * pachur2018: Experiment 2 only. Experiment 1's problems exist only in the paper's table.
  * branches with probability 0 are dropped; probabilities must sum to 1 within 1e-6.
  * baselberlin: excluded. Its lottery task is adaptive (each item is set by earlier choices, so
    the stimuli carry the choices), and its description task reuses Hertwig et al. 2004 problems
    given only as labels.

    python corpora.py RAW OUT      # on Atlas, writes OUT/<corpus>_{covariates,outcome}.npz
"""
from __future__ import annotations

import collections
import os
import sys

import numpy as np
import pandas as pd

K = 2   # widened per corpus when an option has more branches


def opt(outcomes, probs):
    o = [float(x) for x, p in zip(outcomes, probs) if pd.notna(p) and float(p) > 0]
    p = [float(p) for x, p in zip(outcomes, probs) if pd.notna(p) and float(p) > 0]
    if not p or any(pd.isna(x) for x in o) or abs(sum(p) - 1) > 1e-6:
        return None
    return o, p


def gp2012(raw):
    d = pd.read_csv(os.path.join(raw, "gp2012", "par_stab1_new.csv"))
    rows, b = [], collections.Counter()
    for r in d.itertuples(index=False):
        A, B = opt([r.o1, r.o2], [r.p1, r.p2]), opt([r.o3, r.o4], [r.p3, r.p4])
        if A is None or B is None or r.decision not in (1, 2):
            b["unparsed"] += 1
            continue
        b["kept"] += 1
        rows.append((f"{r.subject}", *A, *B, int(r.decision == 2)))
    return rows, b, len(d)


def pachur2017(raw):
    f = os.path.join(raw, "pachur2017", "PachurEtAl_Who errs, who dares_Data.xlsx")
    m = pd.read_excel(f, sheet_name="Choice task", header=None)
    subj = m.iloc[1, 1:123].tolist()
    items = m.iloc[2:, 124:132].astype(float).to_numpy()      # A o1 p1 o2 p2, B o1 p1 o2 p2
    ch = m.iloc[2:, 1:123]
    rows, b = [], collections.Counter()
    n = ch.size
    for i in range(len(items)):
        o = items[i]
        A, B = opt([o[0], o[2]], [o[1], o[3]]), opt([o[4], o[6]], [o[5], o[7]])
        for j, s in enumerate(subj):
            c = ch.iat[i, j]
            if A is None or B is None or pd.isna(c) or c not in (0, 1):
                b["unparsed_or_missing"] += 1
                continue
            b["kept"] += 1
            rows.append((f"{s}", *A, *B, int(c == 0)))            # 1 = A chosen
    return rows, b, n


def pachur2018(raw):
    base = os.path.join(raw, "pachur2018", "Data")
    ids = pd.read_csv(os.path.join(base, "Experiment 2_gamble problem IDs.csv"), sep=";")
    ids.columns = ["task", "pa1", "oa1", "pa2", "oa2", "pb1", "ob1", "pb2", "ob2"]
    par = ids.set_index("task")
    d = pd.read_csv(os.path.join(base, "Experiment 2.csv"), low_memory=False)
    d = d[d["event"] == "onclick"]
    rows, b = [], collections.Counter()
    for r in d.itertuples(index=False):
        if r.task not in par.index or r.choice not in ("SpielA", "SpielB"):
            b["unparsed"] += 1
            continue
        q = par.loc[r.task]
        A, B = opt([q.oa1, q.oa2], [q.pa1, q.pa2]), opt([q.ob1, q.ob2], [q.pb1, q.pb2])
        if A is None or B is None:
            b["unparsed"] += 1
            continue
        b["kept"] += 1
        rows.append((f"{r.subject}-{r.trial}", *A, *B, int(r.choice == "SpielB")))
    return rows, b, len(d)


def zilker2020(raw):
    import pyreadr
    s1 = pyreadr.read_r(os.path.join(raw, "zilker2020", "data_study1", "data_long_study1.Rda"))["data_long"]
    s2 = pyreadr.read_r(os.path.join(raw, "zilker2020", "data_study2", "data_long_study2.Rda"))["data_long_study2"]
    rows, b = [], collections.Counter()
    for r in s1.itertuples(index=False):
        if r.cond == 2:
            b["excluded_complex_safe"] += 1
            continue
        A, B = opt([r.A_o1, r.A_o2], [r.A_p1, r.A_p2]), opt([r.B_o1, r.B_o2], [r.B_p1, r.B_p2])
        if A is None or B is None or r.choice_binary not in ("A", "B"):
            b["unparsed"] += 1
            continue
        b["kept"] += 1
        rows.append((f"s1-{r.subject_no}", *A, *B, int(r.choice_binary == "B")))
    for r in s2.itertuples(index=False):
        if r.typeB == "B2":
            b["excluded_complex_safe"] += 1
            continue
        A, B = opt([r.o_A1, r.o_A2], [r.p_A1, r.p_A2]), opt([r.o_B1, r.o_B2], [r.p_B1, r.p_B2])
        if A is None or B is None or str(r.choice) not in ("A", "B"):
            b["unparsed"] += 1
            continue
        b["kept"] += 1
        rows.append((f"s2-{r.subject_no}", *A, *B, int(str(r.choice) == "B")))
    return rows, b, len(s1) + len(s2)


def babula2018(raw):
    base = os.path.join(raw, "babula2018")
    lines = open(os.path.join(base, "Distributions_stimuli.csv"), encoding="utf-8-sig").read().splitlines()
    grid = [float(v) for v in lines[0].split(";")[1:22]]
    stim = {}
    for ln in lines[2:]:
        f = ln.split(";")
        if not f[0].strip():
            continue
        pa = [float(v or 0) for v in f[1:22]]
        pb = [float(v or 0) for v in f[22:43]]
        stim[int(f[0])] = (opt(grid, pa), opt(grid, pb))
    rows, b = [], collections.Counter()
    n = 0
    for fn in sorted(os.listdir(base)):
        if not fn.startswith("subject"):
            continue
        d = pd.read_csv(os.path.join(base, fn), sep=";")
        n += len(d)
        for r in d.itertuples(index=False):
            AB = stim.get(int(r.question_id)) if pd.notna(r.question_id) else None
            if AB is None or AB[0] is None or AB[1] is None or r.selected_B not in (0, 1):
                b["unparsed"] += 1
                continue
            b["kept"] += 1
            rows.append((fn[:-4], *AB[0], *AB[1], int(r.selected_B)))
    return rows, b, n


PARSERS = {"gp2012": gp2012, "pachur2017": pachur2017, "pachur2018": pachur2018, "zilker2020": zilker2020,
           "babula2018": babula2018}


def pad(opts):
    k = max(len(o) for o, _ in opts)
    X = np.zeros((len(opts), k)); P = np.zeros((len(opts), k))
    for i, (o, p) in enumerate(opts):
        X[i, :len(o)] = o; P[i, :len(p)] = p
    return X, P


def build(name, raw, out):
    rows, buckets, n_raw = PARSERS[name](raw)
    assert sum(buckets.values()) == n_raw, (name, dict(buckets), n_raw)
    XA, PA = pad([(r[1], r[2]) for r in rows])
    XB, PB = pad([(r[3], r[4]) for r in rows])
    k = max(XA.shape[1], XB.shape[1])
    XA, PA, XB, PB = (np.pad(a, ((0, 0), (0, k - a.shape[1]))) for a in (XA, PA, XB, PB))
    part = np.array([r[0] for r in rows])
    np.savez_compressed(os.path.join(out, f"{name}_covariates.npz"), participant=part,
                        XA=XA, PA=PA, XB=XB, PB=PB)
    np.savez_compressed(os.path.join(out, f"{name}_outcome.npz"),
                        chose_B=np.array([r[5] for r in rows], dtype=np.int8))
    return {"raw_records": n_raw, "buckets": dict(buckets), "participants": int(len(set(part)))}


if __name__ == "__main__":
    raw, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    import json
    acc = {n: build(n, raw, out) for n in (sys.argv[3:] or PARSERS)}
    print(json.dumps(acc, indent=1))
    json.dump(acc, open(os.path.join(out, "accounting.json"), "w"), indent=1)
