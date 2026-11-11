"""Development: let Theory Radar look for the form in which the past enters the next choice.

    PYTHONPATH=theory-radar/src python radar_fit.py dev.pkl out.json [all|gain|mixed|loss] [max_rows]

Reads the development half only. The owner proposed on 2026-11-11 to use his
theory-radar (github.com/ahb-sjsu/theory-radar) on the patterns found in
DEVELOPMENT.md. Theory Radar searches short formulas over the columns of a table
for the one whose threshold best separates a yes from a no, and scores it on
rows it has not seen beside standard classifiers.

The yes or no here is whether the player gambled on a trial. One row per trial
from the third trial of a play on. Three sets of columns, each containing the
one before:

    offer     safe, win, lose (the three values on screen), ev_gap (mean of win
              and lose minus safe), spread (win minus lose)
    person    g_rate_prev (share of earlier trials of this play on which the
              player gambled), trial (position in the play)
    path      prev_gam (gambled on the last trial), prev_out (points from the last
              trial), prev_rpe (if gambled, outcome minus the gamble's mean, else
              0), prev2_out, prev2_rpe (the same two trials back), cum_total
              (points so far in the play), prev_lat (seconds taken on the last
              choice)

`person` is kept apart from `path` because a player's own rate of gambling is by
far the strongest predictor and says who the player is, not what just happened.

Five folds, split by participant so no person is on both sides. On each fold
and each set: the formula found on the training rows, its threshold and
direction set on the training rows, then F1 and the area under the ROC curve on
the test rows. Beside it a logistic regression and a gradient-boosted model on
the same columns, each with its threshold set on the training rows for F1.

Everything found here is a development finding. A formula that looks good
becomes a hypothesis for the held-out half and nothing more.
"""
import json
import pickle
import re
import sys

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

from symbolic_search import TheoryRadar
from symbolic_search._ops import BINARY_OPS, UNARY_OPS

from analyze_last import plays

SEED = 20261111
OFFER = ["safe", "win", "lose", "ev_gap", "spread"]
PERSON = ["g_rate_prev", "trial"]
PATH = ["prev_gam", "prev_out", "prev_rpe", "prev2_out", "prev2_rpe", "cum_total", "prev_lat"]
SETS = {"offer": OFFER, "offer_person": OFFER + PERSON, "offer_person_path": OFFER + PERSON + PATH}
TOKEN = re.compile(r"\s*([A-Za-z_][A-Za-z_0-9]*|[()+\-*/])")


def table(recs, which):
    rows, y, groups = [], [], []
    for rec in recs:
        pid = int(rec["id"])
        for p in plays(rec):
            safe, win, lose = p[:, 2], p[:, 3], p[:, 4]
            gam = (p[:, 6] == 1).astype(float)
            mean = (win + lose) / 2
            got = np.where(gam == 1, p[:, 7], safe)
            rpe = np.where(gam == 1, p[:, 7] - mean, 0.0)
            lat = np.nan_to_num(np.clip(p[:, 8], 0, 30), nan=3.0)
            cum = np.concatenate(([0.0], np.cumsum(got)[:-1]))
            for t in range(2, len(p)):
                kind = "gain" if safe[t] > 0 else "loss" if safe[t] < 0 else "mixed"
                if which != "all" and kind != which:
                    continue
                rows.append([safe[t], win[t], lose[t], mean[t] - safe[t], win[t] - lose[t],
                             gam[:t].mean(), t + 1,
                             gam[t - 1], got[t - 1], rpe[t - 1], got[t - 2], rpe[t - 2], cum[t], lat[t - 1]])
                y.append(gam[t])
                groups.append(pid)
    return np.array(rows, dtype=float), np.array(y, dtype=int), np.array(groups)


def parse(text, cols):
    """Evaluate a Theory Radar formula string: name | unary(expr) | (expr binary name)."""
    toks = TOKEN.findall(text)
    pos = [0]

    def take():
        pos[0] += 1
        return toks[pos[0] - 1]

    def expr():
        t = take()
        if t == "(":
            a = expr()
            op = take()
            b = expr()
            assert take() == ")", text
            return BINARY_OPS[op](a, b)
        if t in UNARY_OPS and pos[0] < len(toks) and toks[pos[0]] == "(":
            take()
            a = expr()
            assert take() == ")", text
            return UNARY_OPS[t](a)
        return cols[t]

    v = expr()
    assert pos[0] == len(toks), text
    return v


def best_threshold(s, y):
    """Threshold and direction maximising F1 on (s, y)."""
    best = (-1.0, 0.0, 1)
    for d in (1, -1):
        o = np.argsort(-d * s, kind="stable")
        ss, yy = (d * s)[o], y[o]
        tp = np.cumsum(yy)
        k = np.arange(1, len(yy) + 1)
        f1 = 2 * tp / (k + yy.sum())
        last = np.r_[ss[1:] != ss[:-1], True]            # cut only between distinct scores
        i = int(np.argmax(np.where(last, f1, -1)))
        if f1[i] > best[0]:
            best = (float(f1[i]), float(ss[i]), d)
    return best


def f1_at(s, y, thr, d):
    pred = d * s >= thr
    tp = float((pred & (y == 1)).sum())
    return 2 * tp / max(1.0, pred.sum() + y.sum())


def main(src, out, which="all", max_rows=120000):
    recs = pickle.load(open(src, "rb"))["subjData"]
    rng = np.random.default_rng(SEED)
    X, y, g = table(recs, which)
    names = OFFER + PERSON + PATH
    if len(y) > max_rows:
        ids = rng.permutation(np.unique(g))
        keep, n = set(), 0
        counts = dict(zip(*np.unique(g, return_counts=True)))
        for i in ids:
            if n >= max_rows:
                break
            keep.add(i)
            n += counts[i]
        m = np.isin(g, list(keep))
        X, y, g = X[m], y[m], g[m]
    res = {"subset": which, "rows": int(len(y)), "participants": int(len(np.unique(g))),
           "gamble_rate": float(y.mean()), "folds": []}
    for fold, (tr, te) in enumerate(GroupKFold(5).split(X, y, g)):
        entry = {}
        for sname, cols in SETS.items():
            idx = [names.index(c) for c in cols]
            Xtr, Xte = X[tr][:, idx], X[te][:, idx]
            radar = TheoryRadar(Xtr, y[tr], feature_names=cols)
            r = radar.search(mode="fast", max_depth=3, max_expansions=20000, verbose=False)
            s_tr = parse(r.formula, {c: Xtr[:, i] for i, c in enumerate(cols)})
            s_te = parse(r.formula, {c: Xte[:, i] for i, c in enumerate(cols)})
            s_tr, s_te = np.nan_to_num(s_tr), np.nan_to_num(s_te)
            _, thr, d = best_threshold(s_tr, y[tr])
            e = {"formula": r.formula, "train_f1_reported": float(r.f1),
                 "formula_test_f1": f1_at(s_te, y[te], thr, d), "formula_test_auc": float(roc_auc_score(y[te], d * s_te))}
            sc = StandardScaler().fit(Xtr)
            for mname, model in (("lr", LogisticRegression(max_iter=500)),
                                 ("gb", HistGradientBoostingClassifier(max_iter=200, random_state=SEED))):
                A, B = (sc.transform(Xtr), sc.transform(Xte)) if mname == "lr" else (Xtr, Xte)
                model.fit(A, y[tr])
                p_tr, p_te = model.predict_proba(A)[:, 1], model.predict_proba(B)[:, 1]
                _, thr2, d2 = best_threshold(p_tr, y[tr])
                e[mname + "_test_f1"] = f1_at(p_te, y[te], thr2, d2)
                e[mname + "_test_auc"] = float(roc_auc_score(y[te], p_te))
            entry[sname] = e
            print(fold, sname, json.dumps(e), flush=True)
        res["folds"].append(entry)
    res["mean"] = {s: {k: float(np.mean([f[s][k] for f in res["folds"]])) for k in res["folds"][0][s] if k != "formula"}
                   for s in SETS}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res["mean"], indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "all",
         int(sys.argv[4]) if len(sys.argv) > 4 else 120000)
