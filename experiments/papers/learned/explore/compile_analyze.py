#!/usr/bin/env python3
"""DEVELOPMENT. Do the compiler's duties absorb closeness? Rules fixed in DEVELOPMENT.md (amended
after the smoke test, before the full compile).

K, from the compiled IR only:
    duty_owed          a role_duty fact names the narrator and another party
    harm_under_duty    largest severity magnitude (compiler map) among harm, coercion, deception and
                       externality facts falling on a party named in one of the narrator's role_duty facts
    commit_violated    a commitment held by the narrator has status violated

Q1  ten-fold CV R^2 of direction 0 from DEME's nine dimensions against the nine xbse axes, same items.
Q2  dR2(C | S, H, K) and dR2(K | S, C, H), S, C, H as in hohfeld_analyze.py (raters' average).

    python compile_analyze.py HOHFELD_DIR COMPILED.jsonl XBSE.npz OUT.json MODEL [MODEL ...]
"""
import json
import os
import sys

import numpy as np

from hohfeld_analyze import load, r2

SEV = {"minor": 0.25, "moderate": 0.5, "grave": 0.75, "catastrophic": 1.0, None: 0.5}
HARMS = {"harm", "coercion", "deception", "externality"}
DIMS = ("physical_harm", "rights_respect", "fairness_equity", "autonomy_respect", "privacy_protection",
        "societal_environmental", "virtue_care", "legitimacy_trust", "epistemic_quality")
B = 2000
SEED = 11


def duty_features(row):
    me = row.get("agent")
    if me is None:
        return 0.0, 0.0, 0.0
    duty_parties = set()
    for f in row["facts"]:
        if f["kind"] == "role_duty" and me in f["subjects"]:
            duty_parties |= set(f["subjects"]) - {me}
    if row.get("duties_breached") is not None:          # rerun: the compiler's own duties and breaches
        duty_parties |= {c["beneficiary"] for c in row["commitments"]
                         if c["type"] == "role_duty" and c["holder"] == me and c["beneficiary"]}
        harm = max([SEV.get(s, 0.5) for s in row["duties_breached"].values()], default=0.0)
        viol = any(c["holder"] == me and c["status"] == "violated" for c in row["commitments"])
        return float(bool(duty_parties)), harm, float(viol)
    harm = max([SEV.get(f["severity"], 0.5) for f in row["facts"]
                if f["kind"] in HARMS and duty_parties & set(f["subjects"])], default=0.0)
    viol = any(c["holder"] == me and c["status"] == "violated" for c in row["commitments"])
    return float(bool(duty_parties)), harm, float(viol)


def cv_sq_err(y, X, folds=10, seed=0):
    idx = np.random.default_rng(seed).permutation(len(y))
    err = np.empty(len(y))
    for k in range(folds):
        te = idx[k::folds]
        tr = np.setdiff1d(idx, te)
        X1 = np.column_stack([np.ones(len(tr)), X[tr]])
        beta, *_ = np.linalg.lstsq(X1, y[tr], rcond=None)
        err[te] = (y[te] - np.column_stack([np.ones(len(te)), X[te]]) @ beta) ** 2
    return err


def dr2(y, base, extra):
    return r2(y, base + extra)[0] - r2(y, base)[0]


def main(d, compiled, xbse, out, *models):
    sc = {json.loads(l)["item"]: json.loads(l) for l in open(os.path.join(d, "hohfeld_scores.jsonl"))}
    rat = {m: load(d, m) for m in models}
    comp = {}
    for l in open(compiled, encoding="utf-8"):
        r = json.loads(l)
        comp[r["item"]] = r                                   # last row per item
    errors = sum("error" in r for r in comp.values())
    res = {"compiled": len(comp), "compile_errors": errors, "void": errors > 0.10 * len(sc),
           "served": sorted({s for r in comp.values() for s in r.get("served", [])}),
           "no_agent": sum(r.get("agent") is None for r in comp.values() if "error" not in r)}
    items = sorted(i for i in sc if i in comp and "error" not in comp[i] and all(i in rat[m] for m in models))
    y = np.array([sc[i]["dir0"] for i in items])
    y = (y - y.mean()) / y.std()
    avg = {k: np.mean([[float(rat[m][i][k]) for i in items] for m in models], axis=0)
           for k in ("severity", "closeness", "breach", "omission")}
    sev, clo = avg["severity"], avg["closeness"]
    S = [sev]
    C = [clo, (sev - sev.mean()) * (clo - clo.mean())]
    H = [avg["breach"], avg["omission"]]
    K3 = np.array([duty_features(comp[i]) for i in items])
    K = [K3[:, 0], K3[:, 1], K3[:, 2]]
    res["K_means_duty_owed_harm_under_duty_commit_violated"] = K3.mean(0).tolist()
    res["corr_closeness_with_K"] = [float(np.corrcoef(clo, k)[0, 1]) if k.std() > 0 else None for k in K]

    def q2(idx):
        yy = y[idx]
        s, c, h, k = ([x[idx] for x in b] for b in (S, C, H, K))
        return {"dR2_C_given_SHK": dr2(yy, s + h + k, c), "dR2_K_given_SCH": dr2(yy, s + c + h, k),
                "dR2_C_given_SH": dr2(yy, s + h, c), "R2_K": r2(yy, k)[0], "R2_SCHK": r2(yy, s + c + h + k)[0]}

    point = q2(np.arange(len(y)))
    rng = np.random.default_rng(SEED)
    boot = [q2(rng.integers(0, len(y), len(y))) for _ in range(B)]
    ci = {k: [float(np.percentile([b[k] for b in boot], q)) for q in (2.5, 97.5)] for k in point}
    dC, dK = point["dR2_C_given_SHK"], point["dR2_K_given_SCH"]
    res["Q2"] = {"n": len(items), "R2": {k: float(v) for k, v in point.items()}, "ci95": ci, "readings": {
        "relationships_decompose_into_duties": bool(dC < 0.02 and dK >= 0.02 and ci["dR2_K_given_SCH"][0] > 0),
        "closeness_survives_duties": bool(dC >= 0.02 and ci["dR2_C_given_SHK"][0] > 0)}}

    # Q1: DEME vector against xbse axes, on items with a vector
    xz = np.load(xbse, allow_pickle=True)
    X = xz["scores"].astype(float)
    mv_items = [j for j, i in enumerate(items) if comp[i].get("moral_vector")]
    yq = y[mv_items]
    MV = np.array([[comp[items[j]]["moral_vector"][dname] for dname in DIMS] for j in mv_items])
    XB = X[[sc[items[j]]["text_index"] for j in mv_items]]
    e_mv, e_xb = cv_sq_err(yq, MV), cv_sq_err(yq, XB)
    tss = ((yq - yq.mean()) ** 2).sum()
    diffs = []
    for _ in range(B):
        b = rng.integers(0, len(yq), len(yq))
        t = ((yq[b] - yq[b].mean()) ** 2).sum()
        diffs.append((e_xb[b].sum() - e_mv[b].sum()) / t)
    res["Q1"] = {"n_with_vector": len(mv_items), "cv_R2_deme_vector": float(1 - e_mv.sum() / tss),
                 "cv_R2_xbse_axes": float(1 - e_xb.sum() / tss),
                 "deme_minus_xbse_ci95": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))],
                 "dims_constant": [dname for dname, col in zip(DIMS, MV.T) if col.std() < 1e-9],
                 "dims_sd": {dname: float(col.std()) for dname, col in zip(DIMS, MV.T)}}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:])
