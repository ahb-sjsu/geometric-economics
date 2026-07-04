#!/usr/bin/env python3
"""Run the frozen projection-gap panel on the NRP LLM ladder (via llm-panel).

Subjects = model x persona; each subject answers every contrast at both poles,
`SAMPLES` times, output-only forced choice. Idempotent + preemption-tolerant
(llm-panel ResultStore). Politely bursts via the AIMD admission controller.

    # local wiring check (no network): fake choices, verify results feed analyze.py
    python panel_run.py --fake --out results_fake.jsonl

    # real smoke run on Atlas (needs ~/.llmtoken):
    MODELS=gemma-small,gpt-oss NPERSONAS=4 SAMPLES=5 \
        /home/claude/env/bin/python panel_run.py --out results_smoke.jsonl

Predictions are frozen (prereg-v1). This script never touches the model or the
predictions -- it only collects choices.
"""
from __future__ import annotations

import argparse
import os
import random

import contrasts as K
from llmpanel import AIMDController, ResultStore, WorkItem, run
from llmpanel import personas as P

DEFAULT_MODELS = ["gemma-small", "qwen3-small", "gemma", "gpt-oss", "glm-5",
                  "qwen3", "minimax-m2", "kimi"]


def build_items(models, n_personas, samples, seed=0):
    grid = P.grid()
    random.Random(seed).shuffle(grid)
    personas = grid[:n_personas]
    items = []
    for model in models:
        for persona in personas:
            subject = f"{model}::{persona.id}"
            for c in K.ALL_CONTRASTS:
                for pole, prompt in (("lo", c.prompt_lo), ("hi", c.prompt_hi)):
                    for k in range(samples):
                        items.append(WorkItem(
                            id=f"{c.id}|{pole}|{subject}|{k}",
                            model=model, prompt=prompt,
                            system=persona.system_prompt(),
                            meta={"contrast": c.id, "pole": pole, "subject": subject,
                                  "model": model, "persona": persona.id},
                        ))
    return items


def fake_call_fn(seed=0):
    rng = random.Random(seed)

    def call(model, prompt, system):
        # crude: bias toward A on 'hi' cues so the wiring test yields non-trivial data
        pa = 0.55 if "shelter" in prompt or "verified" in prompt or "community" in prompt else 0.5
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
    ap.add_argument("--out", default="results.jsonl")
    ap.add_argument("--fake", action="store_true", help="offline wiring check (no NRP)")
    ap.add_argument("--models", default=os.environ.get("MODELS", ",".join(DEFAULT_MODELS)))
    ap.add_argument("--npersonas", type=int, default=int(os.environ.get("NPERSONAS", "8")))
    ap.add_argument("--samples", type=int, default=int(os.environ.get("SAMPLES", "10")))
    a = ap.parse_args()

    models = [m.strip() for m in a.models.split(",") if m.strip()]
    items = build_items(models, a.npersonas, a.samples)
    store = ResultStore(a.out)
    print(f"panel: {len(models)} models x {a.npersonas} personas x "
          f"{len(K.ALL_CONTRASTS)} contrasts x 2 poles x {a.samples} samples "
          f"= {len(items)} items ({len(store)} already done)", flush=True)

    call_fn = fake_call_fn() if a.fake else nrp_call_fn()
    ctrl = AIMDController(w_min=1, w_max=32, target_violation=0.05)
    run(items, call_fn, store, controller=ctrl, options=("A", "B"))
    print(f"done: {len(store)} results -> {a.out}", flush=True)
    print(f"controller final window={ctrl.window()} violation_rate={ctrl.violation_rate():.3f}", flush=True)


if __name__ == "__main__":
    main()
