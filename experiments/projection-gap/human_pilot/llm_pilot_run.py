#!/usr/bin/env python3
"""Run the HUMAN-pilot letters through the NRP LLM panel at scale (dry-run).

Dogfoods the human pipeline: the exact `letters.json` stimuli + the incentive
framing, presented to NRP models x personas as BETWEEN-SUBJECTS trials (one pole
per contrast per subject, one random reframing), producing rows in the SAME
schema `analyze_human.py` reads. This validates that the human letters + the
between-subjects analysis reproduce the projection-gap signal, and tests whether
the real-money incentive framing shifts behavior -- before spending on humans.

    python llm_pilot_run.py --fake --out llm_pilot.jsonl              # offline wiring check
    MODELS=gemma-small,gpt-oss NPERSONAS=6 PYTHONPATH=<llmpanel> \
        /home/claude/env/bin/python llm_pilot_run.py --out llm_pilot.jsonl   # NRP
    python analyze_human.py --data llm_pilot.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import random

from llmpanel import AIMDController, ResultStore, WorkItem, run
from llmpanel import personas as P

HERE = os.path.dirname(os.path.abspath(__file__))
LETTERS = json.load(open(os.path.join(HERE, "letters.json"), encoding="utf-8"))
DEFAULT_MODELS = ["gemma-small", "qwen3-small", "gemma", "gpt-oss", "glm-5", "qwen3"]

INCENTIVE = (
    "This is a real decision. One of your decisions will be selected at random and paid out for a "
    "genuine bonus, so answer as you truly prefer. "
)
ANSWER = "\nAnswer with ONLY this line: FINAL CHOICE=<A or B>"


def letter_prompt(contrast, pole, variant, incentive):
    c = contrast
    body = c["poles"][pole]["reframings"][variant]
    lead = INCENTIVE if incentive else ""
    return (f"{lead}{body}\nOption A: {c['optionA']}\nOption B: {c['optionB']}{ANSWER}")


def build_items(models, n_personas, incentive, seed=0):
    grid = P.grid()
    random.Random(seed).shuffle(grid)
    personas = grid[:n_personas]
    items = []
    rng = random.Random(seed + 1)
    for model in models:
        for persona in personas:
            subject = f"{model}::{persona.id}"
            for c in LETTERS["contrasts"]:
                pole = "hi" if rng.random() < 0.5 else "lo"          # between-subjects
                variant = rng.randrange(len(c["poles"][pole]["reframings"]))
                items.append(WorkItem(
                    id=f"{c['id']}|{pole}|{variant}|{subject}|{int(incentive)}",
                    model=model, prompt=letter_prompt(c, pole, variant, incentive),
                    system=persona.system_prompt(),
                    meta={"contrast": c["id"], "pole": pole, "variant": variant, "subject": subject,
                          "model": model, "kind": c["kind"], "family": c["family"],
                          "domain": c["domain"], "coord": c["coord"], "sign_pred": c["sign_pred"],
                          "incentive": incentive},
                ))
    return items


def fake_call_fn(seed=0):
    rng = random.Random(seed)

    def call(model, prompt, system):
        pa = 0.55 if ("shelter" in prompt or "verified" in prompt or "community" in prompt
                      or "integrity" in prompt) else 0.5
        return (f"FINAL CHOICE={'A' if rng.random() < pa else 'B'}", "ok")
    return call


def nrp_call_fn():
    from llmpanel import nrp
    token = nrp.load_token()

    def call(model, prompt, system):
        return nrp.call(model, prompt, token=token, system=system, temperature=0.9)
    return call


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="llm_pilot.jsonl")
    ap.add_argument("--fake", action="store_true")
    ap.add_argument("--incentive", choices=["on", "off", "both"], default="both",
                    help="run with the incentive framing, without, or both arms")
    ap.add_argument("--models", default=os.environ.get("MODELS", ",".join(DEFAULT_MODELS)))
    ap.add_argument("--npersonas", type=int, default=int(os.environ.get("NPERSONAS", "12")))
    a = ap.parse_args()

    models = [m.strip() for m in a.models.split(",") if m.strip()]
    arms = {"on": [True], "off": [False], "both": [True, False]}[a.incentive]
    items = []
    for inc in arms:
        items += build_items(models, a.npersonas, inc)
    store = ResultStore(a.out)
    print(f"LLM pilot: {len(models)} models x {a.npersonas} personas x "
          f"{len(LETTERS['contrasts'])} contrasts x {len(arms)} incentive-arm(s) "
          f"= {len(items)} items ({len(store)} done)", flush=True)

    call_fn = fake_call_fn() if a.fake else nrp_call_fn()
    run(items, call_fn, store, controller=AIMDController(w_min=1, w_max=32), options=("A", "B"))
    print(f"done: {len(store)} -> {a.out}", flush=True)


if __name__ == "__main__":
    main()
