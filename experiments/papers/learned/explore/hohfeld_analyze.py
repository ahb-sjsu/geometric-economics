#!/usr/bin/env python3
"""DEVELOPMENT. Is direction 0 duty breached, closeness, or severity? Analysis fixed before any rating.

y is direction 0 over the sampled actions, standardised (harm to close others at the low end). The
predictors, averaged over the raters, form three blocks:

    S  severity
    C  closeness, and severity x closeness (both centred)
    H  breach and omission (share of raters saying yes)

Reported: R^2 of each block and combination, and the unique share of each block given the other two,
dR2(H | S, C), dR2(C | S, H), dR2(S | C, H), each with a 95% bootstrap interval over items (2,000).

Readings, fixed now (DEVELOPMENT.md, "Hohfeld test"):
- covered: R^2(S + C + H) >= 0.10, else the labels do not capture direction 0;
- duty: dR2(H | S, C) >= 0.02 with lower bound > 0, and larger than dR2(C | S, H);
- closeness: dR2(C | S, H) >= 0.02 with lower bound > 0, and larger than dR2(H | S, C);
- gravity: R^2(S) >= 0.8 R^2(S + C + H).
- duty is inconclusive if the raters' Cohen kappa on breach is below 0.40.
The same analysis is repeated with each rater alone; a reading counts only if it holds for the average
and for every rater.

    python hohfeld_analyze.py DIR OUT.json MODEL [MODEL ...]
"""
import json
import os
import sys

import numpy as np

B = 2000
SEED = 7


def load(d, model):
    rows = {}
    for l in open(os.path.join(d, f"hohfeld_ratings_{model}.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        if "error" not in r:
            rows[r["item"]] = r                            # last good row per item
    return rows


def kappa(a, b):
    a, b = np.asarray(a), np.asarray(b)
    cats = np.unique(np.concatenate([a, b]))
    po = np.mean(a == b)
    pe = sum(np.mean(a == c) * np.mean(b == c) for c in cats)
    return float((po - pe) / (1 - pe)) if pe < 1 else float("nan")


def spearman(a, b):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def r2(y, X):
    X1 = np.column_stack([np.ones(len(y)), *X]) if X else np.ones((len(y), 1))
    beta, *_ = np.linalg.lstsq(X1, y, rcond=None)
    res = y - X1 @ beta
    return 1 - res @ res / ((y - y.mean()) @ (y - y.mean())), beta


def blocks(sev, clo, br, om):
    sc, cc = sev - sev.mean(), clo - clo.mean()
    return {"S": [sev], "C": [clo, sc * cc], "H": [br, om]}


def stats(y, blk):
    combos = {"S": "S", "C": "C", "H": "H", "S+C": "SC", "S+H": "SH", "C+H": "CH", "S+C+H": "SCH"}
    out = {k: r2(y, [x for b in v for x in blk[b]])[0] for k, v in combos.items()}
    out["dR2_H_given_SC"] = out["S+C+H"] - out["S+C"]
    out["dR2_C_given_SH"] = out["S+C+H"] - out["S+H"]
    out["dR2_S_given_CH"] = out["S+C+H"] - out["C+H"]
    return out


def analyse(y, sev, clo, br, om):
    point = stats(y, blocks(sev, clo, br, om))
    rng = np.random.default_rng(SEED)
    boot = []
    for _ in range(B):
        i = rng.integers(0, len(y), len(y))
        boot.append(stats(y[i], blocks(sev[i], clo[i], br[i], om[i])))
    ci = {k: [float(np.percentile([b[k] for b in boot], 2.5)), float(np.percentile([b[k] for b in boot], 97.5))]
          for k in point}
    _, beta = r2((y - y.mean()) / y.std(), [(x - x.mean()) / (x.std() or 1) for x in (sev, clo, br, om)])
    full = point["S+C+H"]
    dH, dC = point["dR2_H_given_SC"], point["dR2_C_given_SH"]
    read = {
        "covered": bool(full >= 0.10),
        "duty": bool(dH >= 0.02 and ci["dR2_H_given_SC"][0] > 0 and dH > dC),
        "closeness": bool(dC >= 0.02 and ci["dR2_C_given_SH"][0] > 0 and dC > dH),
        "gravity": bool(point["S"] >= 0.8 * full),
    }
    return {"R2": {k: float(v) for k, v in point.items()}, "ci95": ci, "readings": read,
            "std_coef_sev_clo_breach_omission": [float(b) for b in beta[1:]]}


def main(d, out, *models):
    sc = {json.loads(l)["item"]: json.loads(l) for l in open(os.path.join(d, "hohfeld_scores.jsonl"))}
    rat = {m: load(d, m) for m in models}
    items = sorted(set(sc).intersection(*[set(r) for r in rat.values()]))
    y = np.array([sc[i]["dir0"] for i in items])
    y = (y - y.mean()) / y.std()

    def col(m, k, f=float):
        return np.array([f(rat[m][i][k]) for i in items])

    res = {"items_rated_by_all": len(items), "served": {m: sorted({r["served"] for r in rat[m].values()})
                                                        for m in models}}
    if len(models) >= 2:
        a, b = models[0], models[1]
        res["reliability"] = {
            "spearman_severity": spearman(col(a, "severity"), col(b, "severity")),
            "spearman_closeness": spearman(col(a, "closeness"), col(b, "closeness")),
            "kappa_position": kappa(col(a, "position", str), col(b, "position", str)),
            "kappa_breach": kappa(col(a, "breach", int), col(b, "breach", int)),
            "kappa_omission": kappa(col(a, "omission", int), col(b, "omission", int)),
            "kappa_affected": kappa(col(a, "affected", str), col(b, "affected", str)),
        }
    avg = {k: np.mean([col(m, k) for m in models], axis=0) for k in ("severity", "closeness", "breach", "omission")}
    res["average"] = analyse(y, avg["severity"], avg["closeness"], avg["breach"], avg["omission"])
    res["per_rater"] = {m: analyse(y, col(m, "severity"), col(m, "closeness"), col(m, "breach"), col(m, "omission"))
                        for m in models}
    final = {}
    for k in ("covered", "duty", "closeness", "gravity"):
        final[k] = res["average"]["readings"][k] and all(res["per_rater"][m]["readings"][k] for m in models)
    if res.get("reliability", {}).get("kappa_breach", 1) < 0.40:
        final["duty"] = "inconclusive (kappa on breach < 0.40)"
    res["readings_all_raters"] = final
    # descriptives: direction 0 (standardised) by the first rater's Hohfeld cell and affected party
    m0 = models[0]
    cell = [("O+breach" if rat[m0][i]["breach"] else rat[m0][i]["position"]) for i in items]
    res["dir0_by_cell_" + m0] = {c: {"n": int(sum(x == c for x in cell)),
                                     "mean": float(y[[x == c for x in cell]].mean())} for c in sorted(set(cell))}
    aff = [rat[m0][i]["affected"] for i in items]
    res["dir0_by_affected_" + m0] = {c: {"n": int(sum(x == c for x in aff)),
                                         "mean": float(y[[x == c for x in aff]].mean())} for c in sorted(set(aff))}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:])
