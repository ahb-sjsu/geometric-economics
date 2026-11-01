#!/usr/bin/env python3
"""DEVELOPMENT. Graded duty strength: does closeness's share go once each compiled duty is weighted by
how strong that kind of duty is? Rules in DEVELOPMENT.md, "Graded duty strength", fixed before the
weights were rated.

Kg, from the rerun's saved IR and the weights from duty_weights.py:
    duty_strength      largest weight among the narrator's role duties
    breach_strength    largest weight x severity over the parties in duties_breached
    commit_violated    as in K
Kt (diagnostic): the same features with each type's weight set to the raters' mean closeness over
actions carrying a duty of that type.

    python compile_graded.py HOHFELD_DIR COMPILED_V2.jsonl WEIGHTS.json OUT.json MODEL [MODEL ...]
"""
import json
import os
import sys

import numpy as np

from compile_analyze import B, SEED, SEV, dr2, duty_features
from hohfeld_analyze import load, r2

PREFIX = "the duties of "


def duty_types(row):
    """party -> compiled duty types the narrator holds toward it ('other' for free-text duties)."""
    me, out = row["agent"], {}
    for c in row["commitments"]:
        if c["type"] == "role_duty" and c["holder"] == me and c["beneficiary"]:
            t = c["content"][len(PREFIX):] if c["content"].startswith(PREFIX) else "other"
            out.setdefault(c["beneficiary"], set()).add(t)
    return out


def graded(row, w, w_other):
    types = duty_types(row)
    wt = {p: max(w.get(t, w_other) for t in ts) for p, ts in types.items()}
    duty = max(wt.values(), default=0.0)
    breach = max([wt.get(p, w_other) * SEV.get(s, 0.5) for p, s in row["duties_breached"].items()], default=0.0)
    viol = duty_features(row)[2]
    return duty, breach, viol


def main(d, compiled, weights, out, *models):
    sc = {json.loads(l)["item"]: json.loads(l) for l in open(os.path.join(d, "hohfeld_scores.jsonl"))}
    rat = {m: load(d, m) for m in models}
    comp = {}
    for l in open(compiled, encoding="utf-8"):
        r = json.loads(l)
        comp[r["item"]] = r
    items = sorted(i for i in sc if i in comp and "error" not in comp[i] and all(i in rat[m] for m in models))
    y = np.array([sc[i]["dir0"] for i in items])
    y = (y - y.mean()) / y.std()
    avg = {k: np.mean([[float(rat[m][i][k]) for i in items] for m in models], axis=0)
           for k in ("severity", "closeness", "breach", "omission")}
    sev, clo = avg["severity"], avg["closeness"]
    S = [sev]
    C = [clo, (sev - sev.mean()) * (clo - clo.mean())]
    H = [avg["breach"], avg["omission"]]

    wj = json.load(open(weights))
    wg = wj["weight_compiled"]
    duty_rel = ("parent", "child", "sibling", "kin", "spouse", "partner", "friend", "guardian", "caregiver",
                "employer")
    wg_other = float(np.mean([wg[t] for t in duty_rel]))
    # type ceiling: each type's mean rated closeness (0-1) over actions carrying a duty of that type
    by_type = {}
    for j, i in enumerate(items):
        for t in set().union(*duty_types(comp[i]).values()):
            by_type.setdefault(t, []).append(clo[j] / 6)
    wt = {t: float(np.mean(v)) for t, v in by_type.items()}
    wt_other = float(np.mean([clo[j] / 6 for j, i in enumerate(items) if duty_types(comp[i])]))

    K = np.array([duty_features(comp[i]) for i in items]).T
    Kg = np.array([graded(comp[i], wg, wg_other) for i in items]).T
    Kt = np.array([graded(comp[i], wt, wt_other) for i in items]).T
    K, Kg, Kt = list(K), list(Kg), list(Kt)

    def q(idx):
        yy = y[idx]
        s, c, h, k, kg, kt = ([x[idx] for x in b] for b in (S, C, H, K, Kg, Kt))
        dC_K, dC_Kg = dr2(yy, s + h + k, c), dr2(yy, s + h + kg, c)
        return {"dR2_C_given_SHKg": dC_Kg, "dR2_Kg_given_SCH": dr2(yy, s + c + h, kg),
                "dR2_C_given_SHK": dC_K, "grading_lowers_C_by": dC_K - dC_Kg,
                "dR2_C_given_SHKt": dr2(yy, s + h + kt, c), "dR2_Kt_given_SCH": dr2(yy, s + c + h, kt),
                "R2_Kg": r2(yy, kg)[0], "R2_K": r2(yy, k)[0], "R2_Kt": r2(yy, kt)[0]}

    point = q(np.arange(len(y)))
    rng = np.random.default_rng(SEED)
    boot = [q(rng.integers(0, len(y), len(y))) for _ in range(B)]
    ci = {k: [float(np.percentile([b[k] for b in boot], p)) for p in (2.5, 97.5)] for k in point}
    dC, dK = point["dR2_C_given_SHKg"], point["dR2_Kg_given_SCH"]
    res = {"n": len(items), "n_with_role_duty": int(sum(bool(duty_types(comp[i])) for i in items)),
           "weights_compiled": wg, "weight_other": wg_other, "spearman_models": wj.get("spearman_models"),
           "type_ceiling_weights": wt, "type_counts": {t: len(v) for t, v in by_type.items()},
           "corr_closeness_duty_strength": float(np.corrcoef(clo, Kg[0])[0, 1]),
           "corr_closeness_duty_binary": float(np.corrcoef(clo, K[0])[0, 1]),
           "R2": {k: float(v) for k, v in point.items()}, "ci95": ci,
           "readings": {"relationships_decompose_into_graded_duties":
                        bool(dC < 0.02 and dK >= 0.02 and ci["dR2_Kg_given_SCH"][0] > 0),
                        "closeness_survives_graded_duties": bool(dC >= 0.02 and ci["dR2_C_given_SHKg"][0] > 0)}}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:])
