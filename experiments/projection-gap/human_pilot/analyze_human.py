#!/usr/bin/env python3
"""Between-subjects analysis for the human projection-gap pilot.

Each subject saw ONE pole per contrast (between-subjects), so the effect is a
group difference: Delta = P(A | hi pole) - P(A | lo pole). We test each real
contrast against the scalar-class null Delta=0 (two-proportion z), BH-FDR across
contrasts, sign-match to prereg-v2, a placebo correction (subtract the
domain-matched placebo's group Delta), cross-domain, and dose monotonicity.
Subjects failing the attention check are excluded (pre-registered).

    python analyze_human.py                      # simulation self-test
    python analyze_human.py --data pilot.jsonl   # real pilot data (concatenated records)
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict


def _phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def two_prop_z(kA, nA, kB, nB):
    """Two-sided z-test for P(A) equal across the two pole groups. Returns (delta, p)."""
    if nA == 0 or nB == 0:
        return 0.0, 1.0
    p1, p2 = kA / nA, kB / nB
    pp = (kA + kB) / (nA + nB)
    se = math.sqrt(max(pp * (1 - pp) * (1 / nA + 1 / nB), 1e-12))
    z = (p1 - p2) / se if se > 0 else 0.0
    return p1 - p2, 2 * (1 - _phi(abs(z)))


def bh_fdr(pvals, q=0.05):
    n = len(pvals)
    order = sorted(range(n), key=lambda i: pvals[i])
    thresh, passed = 0, [False] * n
    for rank, i in enumerate(order, 1):
        if pvals[i] <= q * rank / n:
            thresh = rank
    for rank, i in enumerate(order, 1):
        if rank <= thresh:
            passed[i] = True
    return passed


def load(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    failed = {r["subject"] for r in rows if r.get("kind") == "attn" and not r.get("attn_pass", True)}
    return [r for r in rows if r.get("kind") != "attn" and r["subject"] not in failed], failed


def analyze(rows):
    # counts[contrast][pole] = [nA, n]
    counts = defaultdict(lambda: {"lo": [0, 0], "hi": [0, 0]})
    meta = {}
    for r in rows:
        c, pole = r["contrast"], r.get("pole")
        if pole not in ("lo", "hi"):
            continue
        cell = counts[c][pole]
        cell[1] += 1
        if r["choice"] == "A":
            cell[0] += 1
        meta.setdefault(c, {k: r.get(k) for k in ("kind", "family", "domain", "coord", "sign_pred")})

    per = {}
    for c, pc in counts.items():
        (kA_lo, n_lo), (kA_hi, n_hi) = pc["lo"], pc["hi"]
        delta, p = two_prop_z(kA_hi, n_hi, kA_lo, n_lo)
        per[c] = {**meta[c], "n_lo": n_lo, "n_hi": n_hi, "delta": delta, "p": p,
                  "sign_obs": (1 if delta > 0 else (-1 if delta < 0 else 0))}

    # placebo correction: real minus its domain-matched placebo group-delta
    placebo_delta = {per[c]["domain"]: per[c]["delta"] for c in per if per[c]["kind"] == "placebo"}
    real = [c for c in per if per[c]["kind"] == "real"]
    for c in real:
        per[c]["delta_corr"] = per[c]["delta"] - placebo_delta.get(per[c]["domain"], 0.0)
        per[c]["sign_corr"] = (1 if per[c]["delta_corr"] > 0 else (-1 if per[c]["delta_corr"] < 0 else 0))
    fdr = dict(zip(real, bh_fdr([per[c]["p"] for c in real])))
    for c in real:
        per[c]["fdr"] = bool(fdr[c])
        per[c]["match"] = per[c]["sign_corr"] == per[c]["sign_pred"]

    dose = sorted((c for c in per if per[c]["kind"] == "dose"), key=lambda c: c)
    dmeans = [per[c]["delta"] for c in dose]
    placebos = [per[c] for c in per if per[c]["kind"] == "placebo"]
    verdict = {
        "H1_pass_fraction": sum(per[c]["fdr"] and per[c]["match"] for c in real) / len(real) if real else 0,
        "H2_cross_domain": (any(per[c]["fdr"] and per[c]["match"] and per[c]["domain"] == "game" for c in real)
                            and any(per[c]["fdr"] and per[c]["match"] and per[c]["domain"] == "lottery" for c in real)),
        "H4_dose_monotone": all(b >= a - 0.02 for a, b in zip(dmeans, dmeans[1:])) and len(dmeans) >= 2,
        "H4_placebo_null": all(abs(p["delta"]) < 0.08 and p["p"] > 0.05 for p in placebos),
    }
    return {"per_contrast": per, "verdict": verdict}


def report(res):
    print(f"{'contrast':8} {'kind':8} {'n(lo/hi)':>10} {'d_raw':>7} {'d_corr':>7} {'p':>8} {'fdr':>5} match")
    for c, r in sorted(res["per_contrast"].items()):
        print(f"{c:8} {str(r['kind']):8} {str(r['n_lo'])+'/'+str(r['n_hi']):>10} "
              f"{r['delta']:>+7.3f} {r.get('delta_corr', float('nan')):>+7.3f} {r['p']:>8.4f} "
              f"{str(r.get('fdr','')):>5} {r.get('match','')}")
    print("\nVerdict:")
    for k, v in res["verdict"].items():
        print(f"  {k}: {v}")


def _simulate(n=800, effect=0.18, seed=0):
    """Synthesize between-subjects pilot data: each subject one pole per contrast,
    with a planted group effect on real contrasts (sign per prereg-v2) and null placebos."""
    import random
    rng = random.Random(seed)
    letters = json.load(open("letters.json", encoding="utf-8"))["contrasts"]
    rows = []
    for s in range(n):
        subj = f"sim{s}"
        for c in letters:
            pole = "hi" if rng.random() < 0.5 else "lo"
            base = 0.5
            eff = 0.0
            if c["kind"] in ("real", "dose") and pole == "hi":
                lvl = c.get("dose_level", 4) / 4.0 if c["kind"] == "dose" else 1.0
                eff = c["sign_pred"] * effect * lvl
            pA = min(0.97, max(0.03, base + eff + rng.gauss(0, 0.03)))
            rows.append({"subject": subj, "contrast": c["id"], "pole": pole, "kind": c["kind"],
                         "family": c["family"], "domain": c["domain"], "coord": c["coord"],
                         "sign_pred": c["sign_pred"], "choice": "A" if rng.random() < pA else "B"})
    return rows


def _selftest():
    res = analyze(_simulate(effect=0.18, seed=1))
    assert res["verdict"]["H1_pass_fraction"] >= 0.6, res["verdict"]
    assert res["verdict"]["H2_cross_domain"], res["verdict"]
    assert res["verdict"]["H4_placebo_null"], res["verdict"]
    res0 = analyze(_simulate(effect=0.0, seed=2))
    assert res0["verdict"]["H1_pass_fraction"] <= 0.15, res0["verdict"]
    print("analyze_human self-test OK")
    print(f"  signal run: H1 {res['verdict']['H1_pass_fraction']:.2f}, cross-domain {res['verdict']['H2_cross_domain']}")
    print(f"  null run:   H1 {res0['verdict']['H1_pass_fraction']:.2f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data")
    a = ap.parse_args()
    if not a.data:
        _selftest(); return
    rows, failed = load(a.data)
    print(f"{len(rows)} records, {len(failed)} subjects excluded (attention)")
    arms = sorted({r.get("incentive") for r in rows if "incentive" in r})
    if len(arms) > 1:  # LLM dry-run with both incentive framings -> compare
        for arm in arms:
            sub = [r for r in rows if r.get("incentive") == arm]
            print(f"\n===== incentive framing = {arm} ({len(sub)} records) =====")
            report(analyze(sub))
    else:
        print()
        report(analyze(rows))


if __name__ == "__main__":
    main()
