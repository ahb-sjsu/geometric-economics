#!/usr/bin/env python3
"""Translate the projection-gap letters into a typologically diverse language set.

Uses an NRP-hosted multilingual model (default qwen3) via llmpanel.nrp, low
temperature, with a bounded polite thread pool. Output feeds labse_crosslingual.py,
which LaBSE-gates each translation for fidelity before scoring axis invariance.

    MODEL=qwen3 LANGS=es,zh,ar,hi,sw PYTHONPATH=<llmpanel> \
        /home/claude/env/bin/python translate.py --out translations.json

Offline wiring check (no NRP):
    python translate.py --fake --out /tmp/tr.json
"""
from __future__ import annotations

import argparse
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
PILOT = os.path.join(HERE, "..", "projection-gap", "human_pilot", "letters.json")

LANG_NAMES = {
    "es": "Spanish", "zh": "Chinese (Simplified)", "de": "German", "ar": "Arabic",
    "hi": "Hindi", "sw": "Swahili", "ja": "Japanese", "fr": "French", "ru": "Russian",
    "tr": "Turkish", "ko": "Korean", "id": "Indonesian",
}

PROMPT = (
    "Translate the following text into {lang}. Output ONLY the translation with no "
    "preamble, notes, or quotation marks. Preserve the meaning, tone, and any dollar "
    "amounts exactly.\n\nTEXT:\n{text}"
)


def _clean(s: str) -> str:
    s = (s or "").strip()
    # strip a leading label some models emit ("Translation:", quotes)
    for pre in ("Translation:", "翻译：", "الترجمة:"):
        if s.startswith(pre):
            s = s[len(pre):].strip()
    return s.strip('"').strip()


def build_jobs(contrasts, langs):
    for c in contrasts:
        for pole in ("hi", "lo"):
            for i, text in enumerate(c["poles"][pole]["reframings"]):
                for lang in langs:
                    yield (c["id"], pole, i, lang, text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "translations.json"))
    ap.add_argument("--langs", default=os.environ.get("LANGS", "es,zh,ar,hi,sw"))
    ap.add_argument("--model", default=os.environ.get("MODEL", "qwen3"))
    ap.add_argument("--workers", type=int, default=int(os.environ.get("WORKERS", "8")))
    ap.add_argument("--letters", default=os.environ.get("LETTERS", PILOT))
    ap.add_argument("--fake", action="store_true")
    a = ap.parse_args()

    langs = [x.strip() for x in a.langs.split(",") if x.strip()]
    contrasts = json.load(open(a.letters, encoding="utf-8"))["contrasts"]
    jobs = list(build_jobs(contrasts, langs))

    # resume: load existing
    out = json.load(open(a.out, encoding="utf-8")) if os.path.exists(a.out) else {}

    def done(cid, pole, i, lang):
        return out.get(cid, {}).get(pole, {}).get(lang, [None] * 99)[i] is not None \
            if out.get(cid, {}).get(pole, {}).get(lang) else False

    todo = [j for j in jobs if not (len(out.get(j[0], {}).get(j[1], {}).get(j[3], [])) > j[2]
                                    and out[j[0]][j[1]][j[3]][j[2]])]
    print(f"translate: {len(contrasts)} contrasts x {langs} = {len(jobs)} strings, "
          f"{len(todo)} to do, model={a.model}", flush=True)

    if a.fake:
        def call(text, lang):
            return f"[{lang}] {text}"
    else:
        from llmpanel import nrp
        token = nrp.load_token()

        def call(text, lang):
            txt, _ = nrp.call(a.model, PROMPT.format(lang=LANG_NAMES.get(lang, lang), text=text),
                              token=token, temperature=0.2)
            return _clean(txt)

    def put(cid, pole, i, lang, txt):
        d = out.setdefault(cid, {}).setdefault(pole, {}).setdefault(lang, [])
        while len(d) <= i:
            d.append(None)
        d[i] = txt

    n = 0
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(call, j[4], j[3]): j for j in todo}
        for f in as_completed(futs):
            cid, pole, i, lang, _ = futs[f]
            try:
                put(cid, pole, i, lang, f.result())
            except Exception as e:  # noqa: BLE001
                print(f"  ! {cid}/{pole}/{lang}: {e}", flush=True)
                continue
            n += 1
            if n % 25 == 0:
                json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                print(f"  {n}/{len(todo)}", flush=True)

    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"done: {n} translations -> {a.out}", flush=True)


if __name__ == "__main__":
    main()
