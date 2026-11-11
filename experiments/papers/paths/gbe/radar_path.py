"""Development: Theory Radar on the choices a player's own habits leave open.

    PYTHONPATH=theory-radar/src python radar_path.py dev.pkl out.json [all|gain|mixed|loss] [max_rows] [band]

Reads the development half only. Written on 2026-11-11 after the first run of
radar_fit.py. There the formula found with the path columns on offer was the
same as the one found without them, `((ev_gap / lose) - g_rate_prev)`. The
effect of the last trial is about one point in a hundred (DEVELOPMENT.md) and a
search that scores one threshold over all trials has no reason to spend a term
on it.

This file asks the narrower question. On each fold a logistic regression on
the offer and person columns is fitted on the training rows. Its output `base`
is the log odds that this player gambles on this offer. Only trials where that
model gives a probability within `band` of one half are kept, the trials the
offer and the player's habits do not settle. On those, Theory Radar searches
formulas over `base` and the seven path columns of radar_fit.py.

Reported per fold on the kept test rows: the area under the ROC curve for
`base` alone, for the formula, for a logistic regression on `base` and the path
columns, and for a gradient-boosted model on the same. The gain of each over
`base` alone is how much the path adds. F1 is reported for the formula both as
Theory Radar states it and as recomputed here on the training rows, because
the first run showed the two can differ.

Everything found here is a development finding and becomes a hypothesis for
the held-out half and nothing more.
"""
import json
import pickle
import sys

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

from symbolic_search import TheoryRadar

from radar_fit import OFFER, PATH, PERSON, SEED, best_threshold, f1_at, parse, table


def cap(X, y, g, max_rows, rng):
    if len(y) <= max_rows:
        return X, y, g
    counts = dict(zip(*np.unique(g, return_counts=True)))
    keep, n = [], 0
    for i in rng.permutation(np.unique(g)):
        if n >= max_rows:
            break
        keep.append(i)
        n += counts[i]
    m = np.isin(g, keep)
    return X[m], y[m], g[m]


def main(src, out, which="mixed", max_rows=40000, band=0.2):
    recs = pickle.load(open(src, "rb"))["subjData"]
    rng = np.random.default_rng(SEED)
    X, y, g = cap(*table(recs, which), max_rows, rng)
    nb = len(OFFER) + len(PERSON)
    cols = ["base"] + PATH
    res = {"subset": which, "rows": int(len(y)), "participants": int(len(np.unique(g))), "band": band, "folds": []}
    for fold, (tr, te) in enumerate(GroupKFold(5).split(X, y, g)):
        sc = StandardScaler().fit(X[tr][:, :nb])
        lr = LogisticRegression(max_iter=500).fit(sc.transform(X[tr][:, :nb]), y[tr])
        b_tr = lr.decision_function(sc.transform(X[tr][:, :nb]))
        b_te = lr.decision_function(sc.transform(X[te][:, :nb]))
        lim = np.log((0.5 + band) / (0.5 - band))
        m_tr, m_te = np.abs(b_tr) < lim, np.abs(b_te) < lim
        A, ya = np.c_[b_tr[m_tr], X[tr][m_tr][:, nb:]], y[tr][m_tr]
        B, yb = np.c_[b_te[m_te], X[te][m_te][:, nb:]], y[te][m_te]
        r = TheoryRadar(A, ya, feature_names=cols).search(mode="fast", max_depth=3, max_expansions=5000, verbose=False)
        s_a = np.nan_to_num(parse(r.formula, {c: A[:, i] for i, c in enumerate(cols)}))
        s_b = np.nan_to_num(parse(r.formula, {c: B[:, i] for i, c in enumerate(cols)}))
        f1_tr, thr, d = best_threshold(s_a, ya)
        e = {"kept_train": int(m_tr.sum()), "kept_test": int(m_te.sum()), "gamble_rate_kept_test": float(yb.mean()),
             "formula": r.formula, "train_f1_reported": float(r.f1), "train_f1_here": f1_tr,
             "formula_test_f1": f1_at(s_b, yb, thr, d),
             "base_test_auc": float(roc_auc_score(yb, B[:, 0])),
             "formula_test_auc": float(roc_auc_score(yb, d * s_b))}
        sc2 = StandardScaler().fit(A)
        lr2 = LogisticRegression(max_iter=500).fit(sc2.transform(A), ya)
        e["lr_test_auc"] = float(roc_auc_score(yb, lr2.decision_function(sc2.transform(B))))
        e["lr_coef"] = {c: float(v) for c, v in zip(cols, lr2.coef_[0])}
        gb = HistGradientBoostingClassifier(max_iter=200, random_state=SEED).fit(A, ya)
        e["gb_test_auc"] = float(roc_auc_score(yb, gb.predict_proba(B)[:, 1]))
        res["folds"].append(e)
        print(fold, json.dumps(e), flush=True)
    keys = [k for k, v in res["folds"][0].items() if isinstance(v, float)]
    res["mean"] = {k: float(np.mean([f[k] for f in res["folds"]])) for k in keys}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res["mean"], indent=1))


if __name__ == "__main__":
    a = sys.argv
    main(a[1], a[2], a[3] if len(a) > 3 else "mixed", int(a[4]) if len(a) > 4 else 40000,
         float(a[5]) if len(a) > 5 else 0.2)
