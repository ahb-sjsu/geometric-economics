#!/usr/bin/env python3
"""Projection-gap analysis: observed within-pair gaps vs the frozen predictions.

Statistical methodology follows the fun-hypothesis tester
(github.com/ahb-sjsu/fun-hypothesis): paired non-parametric test (Wilcoxon
signed-rank) on per-subject differences, Benjamini-Hochberg multiple-comparison
control, paired Cohen's d effect size, bootstrap CIs.

Pipeline:
  panel results (JSONL) --> per-subject Delta = P(A|hi) - P(A|lo) per contrast
  --> test each real contrast vs the scalar-theory null Delta=0
  --> compare sign & magnitude to predictions.json (prereg-v1)
  --> verdicts on H1 (sign), H2 (cross-domain), H3 (magnitude), H4 (structure).

Result row schema (from the panel):
  {"id": "<contrast>|<pole>|<subject>|<sample>", "choice": "A"|"B"|None,
   "contrast": str, "pole": "lo"|"hi", "subject": str, "model": str}
Run `python analyze.py --results results.jsonl` after the panel; run with no args
for the simulation self-test.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict

import numpy as np
from scipy import stats


# ---- aggregation ------------------------------------------------------------
def per_subject_delta(rows: list[dict]) -> dict[str, dict[str, float]]:
    """rows -> {contrast: {subject: Delta}} where Delta = P(A|hi)-P(A|lo).

    Only subjects with >=1 valid (A/B) choice at BOTH poles are kept.
    """
    # counts[contrast][subject][pole] = [n_A, n_total]
    counts: dict = defaultdict(lambda: defaultdict(lambda: {"lo": [0, 0], "hi": [0, 0]}))
    for r in rows:
        ch = r.get("choice")
        if ch not in ("A", "B"):
            continue
        cell = counts[r["contrast"]][r["subject"]][r["pole"]]
        cell[1] += 1
        if ch == "A":
            cell[0] += 1
    out: dict[str, dict[str, float]] = {}
    for contrast, subs in counts.items():
        d = {}
        for subject, poles in subs.items():
            nlo, tlo = poles["lo"]
            nhi, thi = poles["hi"]
            if tlo == 0 or thi == 0:
                continue
            d[subject] = (nhi / thi) - (nlo / tlo)
        if d:
            out[contrast] = d
    return out


# ---- statistics (fun-hypothesis methodology) --------------------------------
def bh_fdr(pvals: list[float], q: float = 0.05) -> list[bool]:
    n = len(pvals)
    order = sorted(range(n), key=lambda i: pvals[i])
    passed = [False] * n
    thresh = 0
    for rank, i in enumerate(order, start=1):
        if pvals[i] <= q * rank / n:
            thresh = rank
    for rank, i in enumerate(order, start=1):
        if rank <= thresh:
            passed[i] = True
    return passed


def per_model_consistency(deltas: dict, pred_by_id: dict) -> dict:
    """Cross-model consistency (DESIGN.md): per real contrast, the fraction of
    models whose mean per-subject Delta matches the predicted sign.

    Subjects are keyed "model::persona"; we group by the model prefix.
    """
    out = {}
    for cid, subj_delta in deltas.items():
        pr = pred_by_id.get(cid, {})
        if pr.get("kind") != "real":
            continue
        by_model: dict = defaultdict(list)
        for subject, d in subj_delta.items():
            model = subject.split("::", 1)[0]
            by_model[model].append(d)
        model_sign = {m: int(np.sign(np.mean(v))) for m, v in by_model.items()}
        match = sum(1 for s in model_sign.values() if s == pr.get("sign_pred"))
        out[cid] = {
            "n_models": len(model_sign),
            "n_match": match,
            "frac_match": match / len(model_sign) if model_sign else 0.0,
            "model_sign": model_sign,
            "sign_pred": pr.get("sign_pred"),
        }
    return out


def placebo_corrected(deltas: dict, pred_by_id: dict) -> dict:
    """Within-subject placebo correction: for each real contrast, subtract the
    subject's OWN domain-matched placebo Delta, removing their generic
    wording/demand sensitivity. Returns {real_contrast: test_contrast(corrected)}.

    corrected_delta[subject] = Delta_real[subject] - Delta_placebo(domain)[subject]
    Only subjects present in both the real contrast and its domain placebo count.
    """
    placebo_by_domain = {
        pr["domain"]: pid
        for pid, pr in pred_by_id.items()
        if pr.get("kind") == "placebo"
    }
    out = {}
    for cid, subj_delta in deltas.items():
        pr = pred_by_id.get(cid, {})
        if pr.get("kind") != "real":
            continue
        pid = placebo_by_domain.get(pr.get("domain"))
        pl = deltas.get(pid, {}) if pid else {}
        corrected = {s: d - pl[s] for s, d in subj_delta.items() if s in pl}
        if not corrected:
            continue
        res = test_contrast(np.array(list(corrected.values())))
        res["placebo_used"] = pid
        res["sign_pred"] = pr.get("sign_pred")
        res["sign_match"] = res["sign_obs"] == pr.get("sign_pred")
        out[cid] = res
    return out


def paired_cohens_d(x: np.ndarray) -> float:
    sd = x.std(ddof=1)
    return float(x.mean() / sd) if sd > 0 else 0.0


def boot_ci(x: np.ndarray, n_boot: int = 5000, seed: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    means = rng.choice(x, size=(n_boot, len(x)), replace=True).mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def test_contrast(deltas: np.ndarray) -> dict:
    """Wilcoxon signed-rank of per-subject Delta vs 0 (+ effect size, CI, sign)."""
    x = np.asarray(deltas, float)
    x = x[np.isfinite(x)]
    n = len(x)
    mean = float(x.mean()) if n else float("nan")
    if n < 6 or np.allclose(x, 0):
        p = 1.0
    else:
        try:
            p = float(stats.wilcoxon(x, zero_method="wilcox", alternative="two-sided").pvalue)
        except ValueError:
            p = 1.0
    lo, hi = boot_ci(x) if n else (float("nan"), float("nan"))
    return {
        "n": n, "mean_delta": mean, "sign_obs": int(np.sign(mean)),
        "p": p, "cohens_d": paired_cohens_d(x) if n > 1 else 0.0,
        "ci_low": lo, "ci_high": hi,
    }


# ---- main analysis ----------------------------------------------------------
def analyze(rows: list[dict], predictions: dict) -> dict:
    pred_by_id = {p["id"]: p for p in predictions["predictions"]}
    deltas = per_subject_delta(rows)

    per = {}
    real_ids = [p["id"] for p in predictions["predictions"] if p["kind"] == "real"]
    pvals, keys = [], []
    for cid, subj_delta in deltas.items():
        res = test_contrast(np.array(list(subj_delta.values())))
        pr = pred_by_id.get(cid, {})
        res["sign_pred"] = pr.get("sign_pred")
        res["delta_pred"] = pr.get("delta_pred")
        res["kind"] = pr.get("kind")
        res["family"] = pr.get("family")
        res["domain"] = pr.get("domain")
        res["sign_match"] = (res["sign_obs"] == res["sign_pred"]) if pr else None
        res["mag_covered"] = (
            pr and res["ci_low"] <= pr.get("delta_pred", 0) <= res["ci_high"]
        )
        per[cid] = res
        if pr.get("kind") == "real":
            pvals.append(res["p"]); keys.append(cid)
    fdr = dict(zip(keys, bh_fdr(pvals))) if pvals else {}
    for cid, ok in fdr.items():
        per[cid]["fdr_sig"] = bool(ok)

    # ---- verdicts ----
    real = {c: per[c] for c in real_ids if c in per}
    h1 = {c: (r["fdr_sig"] and r["sign_match"]) for c, r in real.items()}
    game = [r for r in real.values() if r["domain"] == "game"]
    lot = [r for r in real.values() if r["domain"] == "lottery"]
    h2_cross = (
        any(r.get("fdr_sig") and r["sign_match"] for r in game)
        and any(r.get("fdr_sig") and r["sign_match"] for r in lot)
    )
    h3 = {c: r["mag_covered"] for c, r in real.items()}
    # H4 structure
    dose = sorted((c for c in per if per[c]["kind"] == "dose"), key=lambda c: c)
    dose_means = [per[c]["mean_delta"] for c in dose]
    dose_peak = (dose_means.index(max(dose_means)) + 1) if dose_means else None
    b1 = per.get("B1.1", {}).get("sign_obs")
    b1l = per.get("B1L.1", {}).get("sign_obs")
    placebos = [per[c] for c in per if per[c]["kind"] == "placebo"]
    placebo_null = all((not p.get("fdr_sig", False)) and abs(p["mean_delta"]) < 0.05 for p in placebos)

    cross_model = per_model_consistency(deltas, pred_by_id)
    cm_fracs = [v["frac_match"] for v in cross_model.values()]

    # placebo-corrected (within-subject) effects + their own BH-FDR
    corrected = placebo_corrected(deltas, pred_by_id)
    cpk = list(corrected)
    cfdr = dict(zip(cpk, bh_fdr([corrected[c]["p"] for c in cpk]))) if cpk else {}
    for c, ok in cfdr.items():
        corrected[c]["fdr_sig"] = bool(ok)
    corr_pass = {c: (corrected[c].get("fdr_sig") and corrected[c]["sign_match"]) for c in cpk}
    verdict = {
        "H1_sign_significant": h1,
        "H1_pass_fraction": (sum(h1.values()) / len(h1)) if h1 else 0.0,
        "H2_cross_domain": bool(h2_cross),
        "H3_magnitude_covered": h3,
        "H4_dose_peak_level": dose_peak,
        "H4_loss_reversal": (b1 == 1 and b1l == -1),
        "H4_placebo_null": bool(placebo_null),
        "cross_model_mean_frac_match": (sum(cm_fracs) / len(cm_fracs)) if cm_fracs else 0.0,
        "H1_placebo_corrected_pass_fraction": (sum(corr_pass.values()) / len(corr_pass)) if corr_pass else 0.0,
        "H1_placebo_corrected_significant": corr_pass,
    }
    return {"per_contrast": per, "cross_model": cross_model,
            "placebo_corrected": corrected, "verdict": verdict}


def print_report(res: dict):
    print(f"{'contrast':8} {'kind':8} {'n':>4} {'d_obs':>8} {'d_pred':>8} "
          f"{'sign':>4} {'p':>8} {'coh_d':>6} {'fdr':>4} match cover")
    for cid, r in sorted(res["per_contrast"].items()):
        print(f"{cid:8} {str(r['kind']):8} {r['n']:>4} {r['mean_delta']:>+8.3f} "
              f"{(r['delta_pred'] or 0):>+8.3f} {str(r['sign_obs']):>4} {r['p']:>8.4f} "
              f"{r['cohens_d']:>6.2f} {str(r.get('fdr_sig','')):>4} "
              f"{str(r['sign_match']):>5} {str(r['mag_covered'])}")
    if res.get("cross_model"):
        print("\nCross-model consistency (real contrasts):")
        print(f"  {'contrast':8} {'models match pred sign':>24}")
        for cid, cm in sorted(res["cross_model"].items()):
            print(f"  {cid:8} {cm['n_match']}/{cm['n_models']} "
                  f"(frac {cm['frac_match']:.2f}, pred sign {cm['sign_pred']:+d})")
    if res.get("placebo_corrected"):
        print("\nPlacebo-corrected effects (real minus own domain-matched placebo, within-subject):")
        print(f"  {'contrast':8} {'n':>4} {'d_corr':>8} {'p':>8} {'coh_d':>6} {'fdr':>5} match")
        for cid, r in sorted(res["placebo_corrected"].items()):
            print(f"  {cid:8} {r['n']:>4} {r['mean_delta']:>+8.3f} {r['p']:>8.4f} "
                  f"{r['cohens_d']:>6.2f} {str(r.get('fdr_sig','')):>5} {r['sign_match']}")
    print("\nVerdict:")
    for k, v in res["verdict"].items():
        print(f"  {k}: {v}")


# ---- simulation self-test (no data / no network) ----------------------------
def _simulate(predictions: dict, n_subjects=60, samples=20, effect_scale=1.0, seed=0):
    """Synthesize panel rows where the geometric prediction is (partly) real:
    each subject has a baseline P and, at the hi pole, a shift toward the
    predicted delta (real/dose), zero for placebo. Tests that analyze recovers it.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for p in predictions["predictions"]:
        base = rng.uniform(0.3, 0.7, size=n_subjects)  # subject baselines
        for si in range(n_subjects):
            true_shift = effect_scale * (p["delta_pred"] if p["kind"] != "placebo" else 0.0)
            true_shift += rng.normal(0, 0.02)  # subject noise
            for pole in ("lo", "hi"):
                pa = base[si] + (true_shift if pole == "hi" else 0.0)
                pa = min(0.98, max(0.02, pa))
                for k in range(samples):
                    ch = "A" if rng.random() < pa else "B"
                    rows.append({"id": f"{p['id']}|{pole}|s{si}|{k}", "choice": ch,
                                 "contrast": p["id"], "pole": pole, "subject": f"s{si}",
                                 "model": "sim"})
    return rows


def _selftest():
    import os
    pred = json.load(open(os.path.join(os.path.dirname(__file__), "predictions.json")))
    # (a) signal present -> H1 should largely pass, placebos null
    res = analyze(_simulate(pred, effect_scale=1.0, seed=1), pred)
    assert res["verdict"]["H1_pass_fraction"] >= 0.7, res["verdict"]
    assert res["verdict"]["H4_placebo_null"], "placebo leaked"
    assert res["verdict"]["H4_loss_reversal"], "loss reversal not recovered"
    assert res["verdict"]["H2_cross_domain"], "cross-domain not detected"
    # (b) scalar null truth (no effect) -> H1 should mostly fail
    res0 = analyze(_simulate(pred, effect_scale=0.0, seed=2), pred)
    assert res0["verdict"]["H1_pass_fraction"] <= 0.2, res0["verdict"]
    print("analyze self-test OK")
    print(f"  signal run: H1 pass fraction = {res['verdict']['H1_pass_fraction']:.2f}, "
          f"dose peak = {res['verdict']['H4_dose_peak_level']}")
    print(f"  null run:   H1 pass fraction = {res0['verdict']['H1_pass_fraction']:.2f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", help="panel results JSONL")
    ap.add_argument("--predictions", default="predictions.json")
    a = ap.parse_args()
    if not a.results:
        _selftest(); return
    import os
    pred = json.load(open(a.predictions))
    rows = [json.loads(line) for line in open(a.results, encoding="utf-8") if line.strip()]
    res = analyze(rows, pred)
    print_report(res)
    out = os.path.splitext(a.results)[0] + "_analysis.json"
    json.dump(res, open(out, "w"), indent=2)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
