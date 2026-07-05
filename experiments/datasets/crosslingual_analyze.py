#!/usr/bin/env python3
"""Analyze the behavioral cross-lingual panel: universal shape, culture-specific scale.

Per language, the projection-gap vector over the REAL contrasts is
    g_lang = [ P(A|hi,c) - P(A|lo,c)  for c in real contrasts ].
Then:
  * direction universality -- per-language sign-match rate (sign g == sign_pred)
                              and per-contrast cross-language sign agreement.
  * universal SHAPE        -- cos(g_lang, g_en) and mean pairwise cos across langs
                              (high => same coordinate structure). Null: shuffle
                              the contrast labels (should collapse to ~0).
  * culture-specific SCALE -- ||g_lang|| (L2) per language (may recalibrate while
                              the shape / direction holds).

    python crosslingual_analyze.py --data xling.jsonl
"""
from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def gaps(rows):
    # counts[lang][contrast][pole] = [nA, n]
    counts = defaultdict(lambda: defaultdict(lambda: {"lo": [0, 0], "hi": [0, 0]}))
    meta = {}
    for r in rows:
        if r.get("status") != "ok" or r.get("choice") not in ("A", "B"):
            continue
        lang, c, pole = r.get("lang"), r["contrast"], r.get("pole")
        if pole not in ("lo", "hi"):
            continue
        cell = counts[lang][c][pole]
        cell[0] += int(r["choice"] == "A")
        cell[1] += 1
        meta.setdefault(c, {k: r.get(k) for k in ("kind", "coord", "sign_pred")})
    out = {}
    for lang, cc in counts.items():
        d = {}
        for c, pc in cc.items():
            (kA_hi, n_hi), (kA_lo, n_lo) = pc["hi"], pc["lo"]
            if n_hi and n_lo:
                d[c] = {"delta": kA_hi / n_hi - kA_lo / n_lo, "n_hi": n_hi, "n_lo": n_lo, **meta[c]}
        out[lang] = d
    return out, meta


def _cos(a, b):
    num = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return num / (na * nb) if na and nb else float("nan")


def _norm(a):
    return math.sqrt(sum(x * x for x in a))


def analyze(g, meta):
    langs = [lang for lang in ["en", "es", "zh", "ar", "hi", "sw", "de", "ja"] if lang in g]
    real = sorted(c for c, m in meta.items() if m["kind"] == "real")
    sign_pred = {c: meta[c]["sign_pred"] for c in real}

    # gap vectors over real contrasts common to all langs
    common = [c for c in real if all(c in g[lang] for lang in langs)]
    vec = {lang: [g[lang][c]["delta"] for c in common] for lang in langs}

    # direction universality
    match = {}
    for lang in langs:
        m = [1 if (v > 0) == (sign_pred[c] > 0) else 0
             for c, v in zip(common, vec[lang]) if abs(v) > 1e-9]
        match[lang] = (sum(m), len(m))
    sign_agree = []  # per contrast, do all langs agree on sign?
    for i, c in enumerate(common):
        signs = {(vec[lang][i] > 0) for lang in langs if abs(vec[lang][i]) > 1e-9}
        sign_agree.append((c, len(signs) == 1, sum(1 for lang in langs if vec[lang][i] > 0)))

    # shape: cosine to en + mean pairwise
    shape_to_en = {lang: _cos(vec[lang], vec["en"]) for lang in langs if lang != "en"}
    pair = [_cos(vec[a], vec[b]) for i, a in enumerate(langs) for b in langs[i + 1:]]
    mean_pair = sum(pair) / len(pair) if pair else float("nan")

    # DEMEANED shape: remove each vector's mean so cosine reflects the *pattern* of
    # relative gaps, not the shared positive valence (6/7 contrasts have sign_pred=+1).
    def _dm(v):
        mu = sum(v) / len(v)
        return [x - mu for x in v]
    vecd = {lang: _dm(vec[lang]) for lang in langs}
    paird = [_cos(vecd[a], vecd[b]) for i, a in enumerate(langs) for b in langs[i + 1:]]
    mean_pair_dm = sum(paird) / len(paird) if paird else float("nan")

    # null: shuffle contrast order for non-en langs, recompute mean cos to en (raw + demeaned)
    rng = random.Random(0)
    null, nulld = [], []
    for _ in range(1000):
        perm = list(range(len(common)))
        rng.shuffle(perm)
        null.append(sum(_cos([vec[lang][p] for p in perm], vec["en"])
                        for lang in langs if lang != "en") / max(1, len(langs) - 1))
        nulld.append(sum(_cos([vecd[lang][p] for p in perm], vecd["en"])
                         for lang in langs if lang != "en") / max(1, len(langs) - 1))
    null_mean = sum(null) / len(null)
    null_mean_dm = sum(nulld) / len(nulld)

    scale = {lang: _norm(vec[lang]) / math.sqrt(len(common)) for lang in langs}  # RMS gap
    return {"langs": langs, "common": common, "vec": vec, "match": match,
            "sign_agree": sign_agree, "shape_to_en": shape_to_en, "mean_pair": mean_pair,
            "null_mean": null_mean, "mean_pair_dm": mean_pair_dm, "null_mean_dm": null_mean_dm,
            "scale": scale, "sign_pred": sign_pred}


def report(a):
    L = ["# Behavioral cross-lingual panel — universal shape, culture-specific scale\n"]
    L.append(f"Languages: {', '.join(a['langs'])}   |   real contrasts (common): {len(a['common'])}\n")

    L.append("## Direction universality (sign-match rate per language)\n")
    L.append("| lang | sign-match | RMS gap (scale) | shape cos->en |")
    L.append("|---|--:|--:|--:|")
    for lang in a["langs"]:
        k, n = a["match"][lang]
        s = a["scale"][lang]
        sh = "1.000 (ref)" if lang == "en" else f"{a['shape_to_en'][lang]:.3f}"
        L.append(f"| {lang} | {k}/{n} | {s:.3f} | {sh} |")

    L.append("\n## Universal shape\n")
    L.append(f"- mean pairwise cos(gap vectors) across languages: **{a['mean_pair']:.3f}** "
             f"(shuffled null {a['null_mean']:.3f}; **{a['mean_pair'] - a['null_mean']:+.3f}** above chance)")
    L.append(f"- **demeaned** (shape beyond shared valence): **{a['mean_pair_dm']:.3f}** "
             f"(shuffled null {a['null_mean_dm']:.3f}; **{a['mean_pair_dm'] - a['null_mean_dm']:+.3f}** above chance)")
    scales = [a["scale"][lang] for lang in a["langs"]]
    L.append(f"- scale (RMS gap) range: **{min(scales):.3f} .. {max(scales):.3f}** "
             f"({max(scales) / max(min(scales), 1e-9):.2f}x) — the culture-specific magnitude")

    L.append("\n## Per-contrast cross-language sign agreement\n")
    L.append("| contrast | coord | sign_pred | all-langs agree | #langs +ve |")
    L.append("|---|---|--:|:--:|--:|")
    for c, agree, npos in a["sign_agree"]:
        L.append(f"| {c} | {a.get('sign_pred',{}).get(c,'')} | {a['sign_pred'][c]:+d} | "
                 f"{'yes' if agree else 'NO'} | {npos}/{len(a['langs'])} |")

    agree_n = sum(1 for _, ag, _ in a["sign_agree"] if ag)
    L.append("\n## Verdict\n")
    L.append(f"- **shape universality**: mean cross-language gap-vector cosine "
             f"**{a['mean_pair']:.3f}** vs null {a['null_mean']:.3f}.")
    L.append(f"- **direction**: {agree_n}/{len(a['sign_agree'])} real contrasts have the SAME "
             f"gap sign in all {len(a['langs'])} languages.")
    L.append(f"- **scale**: RMS gap varies {min(scales):.3f}..{max(scales):.3f} across languages — "
             f"the theory's 'culture-specific scale' while the shape holds.")
    return "\n".join(L)


def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="xling.jsonl")
    ap.add_argument("--md")
    a = ap.parse_args()
    rows = load(a.data)
    g, meta = gaps(rows)
    res = analyze(g, meta)
    md = report(res)
    print(md)
    if a.md:
        open(a.md, "w", encoding="utf-8").write(md + "\n")


if __name__ == "__main__":
    main()
