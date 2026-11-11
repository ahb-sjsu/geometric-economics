"""Pass 1: does the timing of a loss matter beyond the board it leaves?

    python analyze_steps.py states.tsv decisions.tsv out.json

Logistic model of accepting the bank offer on the present state (log offer over
mean remaining prize, log mean remaining prize, spread, round and sheet
indicators) and on the path: the last three steps s(r) = log E(r) - log E(r-1).
Standard errors clustered by contestant. Television and experiment sheets are
fitted separately. The same model is fitted with absolute steps.
"""
import json
import sys
from collections import defaultdict

import numpy as np
import statsmodels.api as sm

TV = ("NL1a", "NL1b", "GE1", "GE2", "US", "USX")
EXP = ("EXP1", "EXP2")


def load(states, decisions):
    dec = {}
    for line in open(decisions):
        cid, rnd, d = line.rstrip("\n").split("\t")
        dec[(cid, int(rnd))] = d
    by = defaultdict(dict)
    for line in open(states):
        cid, sheet, rnd, offer, left, board = line.rstrip("\n").split("\t")
        left = np.array([float(x) for x in left.split(" ")])
        board = np.array([float(x) for x in board.split(" ")])
        by[(sheet, cid)][int(rnd)] = (float(offer), left, board)
    rows = []
    for (sheet, cid), g in by.items():
        logE = {0: np.log(next(iter(g.values()))[2].mean())}
        for r in sorted(g):
            logE[r] = np.log(g[r][1].mean())
        for r in sorted(g):
            offer, left, _ = g[r]
            d = dec.get((cid, r), "")
            if d not in ("D", "ND") or offer <= 0 or len(left) < 2:
                continue
            s = [logE[r - k] - logE[r - k - 1] if (r - k) in logE and (r - k - 1) in logE else None
                 for k in range(3)]
            rows.append({"sheet": sheet, "id": sheet + ":" + cid, "round": r, "deal": int(d == "D"),
                         "gen": np.log(offer) - logE[r], "logE": logE[r],
                         "spread": left.std() / left.mean(), "s": s})
    return rows


def fit(rows, sheets, nlags, absolute):
    rows = [x for x in rows if x["sheet"] in sheets and all(v is not None for v in x["s"][:nlags])]
    # A round in which nobody (or everybody) in this pool accepted is predicted perfectly by its
    # indicator and stops the fit converging. Such rounds carry no information on the other terms
    # and are dropped.
    live = {r for r in {x["round"] for x in rows}
            if len({x["deal"] for x in rows if x["round"] == r}) == 2}
    dropped = len([x for x in rows if x["round"] not in live])
    rows = [x for x in rows if x["round"] in live]
    y = np.array([x["deal"] for x in rows])
    out = {"rows": len(rows), "contestants": len({x["id"] for x in rows}), "acceptances": int(y.sum()),
           "rows_dropped_in_rounds_with_one_outcome": dropped}
    cols, names = [], []
    for nm in ("gen", "logE", "spread"):
        cols.append([x[nm] for x in rows])
        names.append(nm)
    for k in range(nlags):
        cols.append([abs(x["s"][k]) if absolute else x["s"][k] for x in rows])
        names.append("step_lag%d" % (k + 1))
    # round and sheet indicators, kept only where the level has both outcomes; first level dropped
    for key in ("round", "sheet"):
        levels = sorted({x[key] for x in rows}, key=str)
        for lv in levels[1:]:
            c = np.array([float(x[key] == lv) for x in rows])
            if key == "round" or 0 < y[c == 1].sum() < c.sum():
                cols.append(c)
                names.append("%s=%s" % (key, lv))
    X = sm.add_constant(np.array(cols, dtype=float).T)
    groups = np.unique([x["id"] for x in rows], return_inverse=True)[1]
    try:
        m = sm.Logit(y, X).fit(disp=0, maxiter=200, cov_type="cluster", cov_kwds={"groups": groups})
    except Exception as e:                       # separation or a singular design is reported, not hidden
        out["error"] = repr(e)
        return out
    out["converged"] = bool(m.mle_retvals["converged"])
    ci = m.conf_int()
    for i, nm in enumerate(["const"] + names):
        if nm in ("gen", "logE", "spread") or nm.startswith("step"):
            out[nm] = {"coef": float(m.params[i]), "se": float(m.bse[i]),
                       "ci95": [float(ci[i][0]), float(ci[i][1])]}
    out["sd_of_step_lag1"] = float(np.std([abs(x["s"][0]) if absolute else x["s"][0] for x in rows]))
    return out


def main(states, decisions, out):
    rows = load(states, decisions)
    res = {}
    for label, sheets in (("television", TV), ("experiments", EXP)):
        for absolute in (False, True):
            for nlags in (1, 2, 3):
                key = "%s_%s_lags%d" % (label, "absolute" if absolute else "signed", nlags)
                res[key] = fit(rows, sheets, nlags, absolute)
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
