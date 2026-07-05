#!/usr/bin/env python3
"""Behavioral cross-lingual panel — run the projection-gap letters per language.

For each language we present the LaBSE-verified translated letter body + translated
option labels to the NRP panel (models x personas) as BETWEEN-SUBJECTS forced choices,
then measure the projection-gap per contrast per language. Tests:

  * direction universality  -- does the gap SIGN replicate in every language?
  * universal shape         -- do the per-contrast gap VECTORS correlate across
                               languages (same coordinate structure)?
  * culture-specific scale  -- does the gap MAGNITUDE (vector norm / temperature)
                               recalibrate per language while the shape holds?

English ('en') uses the original letters; other languages use translations.json.
Option labels are translated once (cached to options_tr.json). The parseable
"FINAL CHOICE=<A or B>" marker stays in English (A/B are language-neutral).

    MODELS=gemma-small,qwen3-small,gemma,gpt-oss,glm-5,qwen3 NPERSONAS=12 \
    LANGS=en,es,zh,ar,hi,sw LETTERS=~/projgap/human_pilot/letters.json \
    TRANSLATIONS=~/translations.json \
        /home/claude/env/bin/python crosslingual_panel.py --out /tmp/xling.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import random

from llmpanel import AIMDController, ResultStore, WorkItem, run
from llmpanel import personas as P

HERE = os.path.dirname(os.path.abspath(__file__))
LANG_NAMES = {"es": "Spanish", "zh": "Chinese (Simplified)", "ar": "Arabic",
              "hi": "Hindi", "sw": "Swahili", "de": "German", "ja": "Japanese"}
ANSWER = "\nAnswer with ONLY this line: FINAL CHOICE=<A or B>"


def option_translations(contrasts, langs, model, cache_path, fake=False):
    """Translate optionA/optionB per contrast into each non-en language (cached)."""
    cache = json.load(open(cache_path, encoding="utf-8")) if os.path.exists(cache_path) else {}
    need = [(c, lang) for c in contrasts for lang in langs if lang != "en"
            and cache.get(c["id"], {}).get(lang) is None]
    if need and not fake:
        from llmpanel import nrp
        token = nrp.load_token()

        def tr(text, lang):
            p = (f"Translate into {LANG_NAMES.get(lang, lang)}. Output ONLY the translation, "
                 f"no notes, preserve dollar amounts.\n\nTEXT:\n{text}")
            t, _ = nrp.call(model, p, token=token, temperature=0.2)
            return t.strip().strip('"')

        for c, lang in need:
            cache.setdefault(c["id"], {})[lang] = {"A": tr(c["optionA"], lang), "B": tr(c["optionB"], lang)}
        json.dump(cache, open(cache_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    elif need:  # fake
        for c, lang in need:
            cache.setdefault(c["id"], {})[lang] = {"A": f"[{lang}] {c['optionA']}",
                                                   "B": f"[{lang}] {c['optionB']}"}
    return cache


def build_items(letters, translations, opt_tr, langs, models, n_personas, samples=1, seed=0):
    grid = P.grid()
    random.Random(seed).shuffle(grid)
    personas = grid[:n_personas]
    rng = random.Random(seed + 1)
    items = []
    for lang in langs:
        for model in models:
            for persona in personas:
                subject = f"{lang}::{model}::{persona.id}"
                for c in letters["contrasts"]:
                    cid = c["id"]
                    pole = "hi" if rng.random() < 0.5 else "lo"
                    if lang == "en":
                        bodies = c["poles"][pole]["reframings"]
                        oa, ob = c["optionA"], c["optionB"]
                    else:
                        bodies = translations.get(cid, {}).get(pole, {}).get(lang)
                        o = opt_tr.get(cid, {}).get(lang, {})
                        oa, ob = o.get("A", c["optionA"]), o.get("B", c["optionB"])
                    if not bodies:
                        continue
                    for k in range(samples):
                        v = rng.randrange(len(bodies))
                        prompt = f"{bodies[v]}\nOption A: {oa}\nOption B: {ob}{ANSWER}"
                        items.append(WorkItem(
                            id=f"{cid}|{lang}|{pole}|{v}|{subject}|{k}",
                            model=model, prompt=prompt, system=persona.system_prompt(),
                            meta={"contrast": cid, "lang": lang, "pole": pole, "variant": v,
                                  "subject": subject, "model": model, "coord": c["coord"],
                                  "kind": c["kind"], "sign_pred": c["sign_pred"]}))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "xling.jsonl"))
    ap.add_argument("--letters", default=os.environ.get("LETTERS",
                    os.path.join(HERE, "..", "projection-gap", "human_pilot", "letters.json")))
    ap.add_argument("--translations", default=os.environ.get("TRANSLATIONS",
                    os.path.join(HERE, "translations.json")))
    ap.add_argument("--langs", default=os.environ.get("LANGS", "en,es,zh,ar,hi,sw"))
    ap.add_argument("--models", default=os.environ.get("MODELS",
                    "gemma-small,qwen3-small,gemma,gpt-oss,glm-5,qwen3"))
    ap.add_argument("--npersonas", type=int, default=int(os.environ.get("NPERSONAS", "12")))
    ap.add_argument("--samples", type=int, default=int(os.environ.get("SAMPLES", "1")))
    ap.add_argument("--optmodel", default=os.environ.get("OPTMODEL", "qwen3"))
    ap.add_argument("--fake", action="store_true")
    a = ap.parse_args()

    langs = [x.strip() for x in a.langs.split(",") if x.strip()]
    models = [x.strip() for x in a.models.split(",") if x.strip()]
    letters = json.load(open(a.letters, encoding="utf-8"))
    translations = json.load(open(a.translations, encoding="utf-8"))
    opt_cache = os.path.join(os.path.dirname(a.out) or ".", "options_tr.json")
    opt_tr = option_translations(letters["contrasts"], langs, a.optmodel, opt_cache, fake=a.fake)

    items = build_items(letters, translations, opt_tr, langs, models, a.npersonas, a.samples)
    store = ResultStore(a.out)
    print(f"xling panel: {langs} x {len(models)} models x {a.npersonas} personas x "
          f"{len(letters['contrasts'])} contrasts = {len(items)} items ({len(store)} done)", flush=True)

    if a.fake:
        rng = random.Random(0)

        def call(model, prompt, system):
            pa = 0.6 if any(w in prompt for w in ("well", "clinic", "community", "verified",
                                                  "integrity", "shelter")) else 0.45
            return (f"FINAL CHOICE={'A' if rng.random() < pa else 'B'}", "ok")
    else:
        from llmpanel import nrp
        token = nrp.load_token()

        def call(model, prompt, system):
            return nrp.call(model, prompt, token=token, system=system, temperature=0.9)

    run(items, call, store, controller=AIMDController(w_min=1, w_max=32), options=("A", "B"))
    print(f"done: {len(store)} -> {a.out}", flush=True)


if __name__ == "__main__":
    main()
