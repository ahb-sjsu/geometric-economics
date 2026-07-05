#!/usr/bin/env python3
"""Cross-lingual universality test via LaBSE — "universal shape, culture-specific scale."

The geometric theory claims the decision *coordinate directions* (the societal /
epistemic / identity axes) are universal, while the *scale* (temperature) may
recalibrate per culture. LaBSE gives language-agnostic sentence embeddings, so
the same letter in different languages lands in nearby coordinates.

We operationalize a coordinate axis as the difference vector between the two
poles of a projection-gap contrast, in LaBSE space:

    axis_lang(c) = mean_v emb(hi_pole, v, lang) - mean_v emb(lo_pole, v, lang)

The universality prediction is that this axis is **parallel across languages**:

    cos( axis_en(c), axis_lang(c) )  ~ 1     for real coordinate contrasts
                                     ~ 0/noise for placebo contrasts (control)

This is the encoding-invariance of the keystone theorem (Thm 5) extended from
"any scalar projection" to "any language" — a strong, directly-measurable form
of the theory, needing no choice data (that is the separate behavioral leg).

Inputs
------
letters.json          the projection-gap stimuli (English source of truth)
translations.json     {contrast_id: {pole: {lang: [reframing_text, ...]}}}
                      produced by translate.py (NRP LLM translate + LaBSE gate)

Usage
-----
    python labse_crosslingual.py --translations translations.json
    python labse_crosslingual.py --translations translations.json --json out.json
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PILOT = os.path.join(HERE, "..", "projection-gap", "human_pilot", "letters.json")

FIDELITY_GATE = 0.75  # min EN<->lang cosine for a translation to count (LaBSE parallel-text floor)


def load_letters(path=PILOT):
    return json.load(open(path, encoding="utf-8"))["contrasts"]


def pole_texts(contrast, pole):
    """All reframings for a pole, as full letter text (matches the panel prompt body)."""
    return list(contrast["poles"][pole]["reframings"])


def _labse():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("sentence-transformers/LaBSE")


def _axis(model, hi_texts, lo_texts):
    """Coordinate axis = mean(hi) - mean(lo) in normalized LaBSE space."""
    hi = model.encode(hi_texts, normalize_embeddings=True)
    lo = model.encode(lo_texts, normalize_embeddings=True)
    return hi.mean(0) - lo.mean(0), hi.mean(0), lo.mean(0)


def run(translations, letters=None, model=None, gate=FIDELITY_GATE):
    """Return per-contrast axis invariance across languages, grouped by coordinate."""
    letters = letters or load_letters()
    model = model or _labse()
    by_id = {c["id"]: c for c in letters}
    langs = sorted({lang for t in translations.values() for p in t.values() for lang in p})

    rows = []
    for cid, tr in translations.items():
        c = by_id.get(cid)
        if not c:
            continue
        # English axis (source of truth)
        en_axis, en_hi, en_lo = _axis(model, pole_texts(c, "hi"), pole_texts(c, "lo"))
        en_axis_n = en_axis / (np.linalg.norm(en_axis) + 1e-9)
        row = {"id": cid, "coord": c["coord"], "kind": c["kind"], "family": c["family"],
               "en_axis": en_axis_n.tolist(), "langs": {}}
        for lang in langs:
            hi_t = tr.get("hi", {}).get(lang)
            lo_t = tr.get("lo", {}).get(lang)
            if not hi_t or not lo_t:
                continue
            ax, hi_m, lo_m = _axis(model, hi_t, lo_t)
            ax_n = ax / (np.linalg.norm(ax) + 1e-9)
            # translation fidelity: does the lang pole match the EN pole meaning?
            fid = 0.5 * (float(en_hi @ hi_m) / (np.linalg.norm(en_hi) * np.linalg.norm(hi_m) + 1e-9)
                         + float(en_lo @ lo_m) / (np.linalg.norm(en_lo) * np.linalg.norm(lo_m) + 1e-9))
            row["langs"][lang] = {
                "axis_cos": float(en_axis_n @ ax_n),  # THE universality number
                "fidelity": fid,
                "gated": fid >= gate,
                "axis": ax_n.tolist(),
            }
        rows.append(row)
    return {"langs": langs, "rows": rows, "gate": gate}


def summarize(res):
    rows, langs = res["rows"], res["langs"]
    out = ["# Cross-lingual universality (LaBSE axis invariance)\n"]
    out.append(f"Languages: {', '.join(langs)}   |   fidelity gate: {res['gate']}\n")

    # per-contrast table
    out.append("## Axis invariance cos(axis_en, axis_lang) per contrast\n")
    hdr = "| id | coord | kind | " + " | ".join(langs) + " | mean |"
    out.append(hdr)
    out.append("|" + "---|" * (len(langs) + 4))
    real_by_coord, placebo = {}, []
    for r in rows:
        cells = []
        vals = []
        for lang in langs:
            d = r["langs"].get(lang)
            if d and d["gated"]:
                cells.append(f"{d['axis_cos']:.2f}")
                vals.append(d["axis_cos"])
            elif d:
                cells.append(f"({d['axis_cos']:.2f})")  # below fidelity gate
            else:
                cells.append("-")
        m = float(np.mean(vals)) if vals else float("nan")
        out.append(f"| {r['id']} | {r['coord']} | {r['kind']} | " + " | ".join(cells) + f" | {m:.2f} |")
        if r["kind"] == "placebo":
            placebo.extend(vals)
        elif r["kind"] == "real":
            real_by_coord.setdefault(r["coord"], []).extend(vals)

    out.append("\n## Verdict\n")
    for coord, vals in sorted(real_by_coord.items()):
        if vals:
            out.append(f"- **{coord}** (real): mean axis-invariance **{np.mean(vals):.3f}** "
                       f"(n={len(vals)}, min {min(vals):.2f})")
    allreal = [v for vs in real_by_coord.values() for v in vs]
    if allreal:
        out.append(f"- **all real coordinates**: mean **{np.mean(allreal):.3f}** (n={len(allreal)})")
    if placebo:
        out.append(f"- **placebo** (control, should be lower/noisier): mean "
                   f"**{np.mean(placebo):.3f}** (n={len(placebo)})")
        if allreal:
            out.append(f"- **real - placebo gap**: **{np.mean(allreal) - np.mean(placebo):+.3f}** "
                       f"(positive => real axes are more language-invariant than placebos)")
    return "\n".join(out)


def coherence(res):
    """Discriminating test: do contrasts sharing a coordinate point the SAME way
    (a single universal direction), and is that preserved across languages, while
    different coordinates stay distinct? Placebos should NOT cohere (control).

    For each language we build, per contrast, the axis in THAT language's LaBSE
    space (English uses en_axis; other langs use the per-lang axis, gated). Then:
      within-coord = mean pairwise cos among real contrasts of the same coord
      cross-coord  = mean cos between real contrasts of different coords
      placebo->coord = mean cos of each placebo axis to its nearest coord centroid
    """
    rows = res["rows"]
    langs = ["en"] + res["langs"]

    def axis(r, lang):
        if lang == "en":
            return np.array(r["en_axis"])
        d = r["langs"].get(lang)
        if not d or not d["gated"] or "axis" not in d:
            return None
        return np.array(d["axis"])

    out = ["\n## Cross-contrast coherence (the discriminating test)\n"]
    out.append("Do same-coordinate contrasts share ONE direction, preserved across languages?\n")
    out.append("| lang | within-coord | cross-coord | separation | placebo->coord |")
    out.append("|---|--:|--:|--:|--:|")
    summary = {}
    for lang in langs:
        real = [(r["coord"], axis(r, lang)) for r in rows if r["kind"] == "real"]
        real = [(c, a) for c, a in real if a is not None]
        plac = [axis(r, lang) for r in rows if r["kind"] == "placebo"]
        plac = [a for a in plac if a is not None]
        if len(real) < 2:
            continue
        within, cross = [], []
        for i in range(len(real)):
            for j in range(i + 1, len(real)):
                ci, ai = real[i]
                cj, aj = real[j]
                cos = float(ai @ aj / (np.linalg.norm(ai) * np.linalg.norm(aj) + 1e-9))
                (within if ci == cj else cross).append(cos)
        # coord centroids for placebo test
        cents = {}
        for c, a in real:
            cents.setdefault(c, []).append(a)
        cents = {c: np.mean(v, 0) for c, v in cents.items()}
        pc = [max(float(a @ m / (np.linalg.norm(a) * np.linalg.norm(m) + 1e-9))
                  for m in cents.values()) for a in plac]
        w = float(np.mean(within)) if within else float("nan")
        x = float(np.mean(cross)) if cross else float("nan")
        p = float(np.mean(pc)) if pc else float("nan")
        summary[lang] = (w, x, w - x, p)
        out.append(f"| {lang} | {w:.3f} | {x:.3f} | {w - x:+.3f} | {p:.3f} |")

    # verdict
    nonen = [v for k, v in summary.items() if k != "en"]
    if nonen and "en" in summary:
        w_en = summary["en"][0]
        w_other = np.mean([v[0] for v in nonen])
        sep = np.mean([v[2] for v in summary.values()])
        out.append("\n**Reading:**")
        out.append(f"- within-coord coherence: en **{w_en:.3f}**, other-langs mean **{w_other:.3f}** "
                   f"(preserved across languages ⇒ universal coordinate directions)")
        out.append(f"- within − cross separation (mean over langs): **{sep:+.3f}** "
                   f"(positive ⇒ coordinates are distinguishable, not one blob)")
        real_c = summary["en"][0]
        plac_c = np.mean([v[3] for v in summary.values() if not np.isnan(v[3])])
        out.append(f"- real within-coord **{real_c:.3f}** vs placebo→coord **{plac_c:.3f}** "
                   f"(gap **{real_c - plac_c:+.3f}**; positive ⇒ placebos don't load on a coordinate)")
    return "\n".join(out).replace("⇒", "=>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--translations", default=os.path.join(HERE, "translations.json"))
    ap.add_argument("--json", help="write raw results JSON here")
    ap.add_argument("--md", help="write markdown summary here")
    a = ap.parse_args()

    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    translations = json.load(open(a.translations, encoding="utf-8"))
    res = run(translations)
    md = summarize(res) + "\n" + coherence(res)
    print(md)
    if a.json:
        # drop the bulky axis vectors from the on-disk summary
        slim = {**res, "rows": [{k: v for k, v in r.items() if k != "en_axis"} for r in res["rows"]]}
        for r in slim["rows"]:
            r["langs"] = {lg: {k: v for k, v in d.items() if k != "axis"} for lg, d in r["langs"].items()}
        json.dump(slim, open(a.json, "w", encoding="utf-8"), indent=2, default=float)
    if a.md:
        open(a.md, "w", encoding="utf-8").write(md + "\n")


if __name__ == "__main__":
    main()
