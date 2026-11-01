#!/usr/bin/env python3
"""DEVELOPMENT. LLM raters weight each relation type by the strength of the special obligations it
carries. They see only the list of relation types: no action, no direction 0, no closeness label.
Design in DEVELOPMENT.md, "Graded duty strength".

Three calls per model, the list shuffled each time, temperature 0, thinking off. Output: every raw
rating, the per-type weight (mean over all ratings, scaled to 0-1) and the weight per compiled duty
type (mean of the two directions where the compiled text loses direction).

    python duty_weights.py OUT.json MODEL [MODEL ...]
"""
import json
import os
import random
import sys
import time
import urllib.request

import numpy as np

URL = "https://ellm.nrp-nautilus.io/v1/chat/completions"
TOKEN = open(os.path.expanduser("~/.llmtoken")).read().strip()
SEEDS = (1, 2, 3)

# entry -> description shown to the rater; "your X" means the person stands in that relation to you
ENTRIES = {
    "your_parent": "your parent",
    "your_child": "your child",
    "sibling": "your sibling",
    "kin": "another relative (grandparent, grandchild, aunt, uncle, cousin, in-law, step-relative)",
    "spouse": "your spouse",
    "partner": "your romantic partner (boyfriend, girlfriend, fiance)",
    "ex_partner": "your former spouse or romantic partner",
    "friend": "your friend",
    "in_your_charge": "someone in your legal or practical charge",
    "your_guardian": "someone who has legal or practical charge of you",
    "you_care_for": "someone you look after as a carer, nurse or babysitter",
    "your_carer": "someone who looks after you as a carer, nurse or babysitter",
    "you_employ": "someone you employ or manage",
    "your_employer": "your employer or manager",
    "colleague": "a coworker or classmate",
    "roommate": "a roommate who is not family or a partner",
    "neighbour": "a neighbour",
    "you_serve": "a customer or client you serve",
    "you_are_served_by": "someone who serves you as a customer or client",
    "acquaintance": "an acquaintance you know slightly",
    "stranger": "a stranger with no prior relation to you",
}
# compiled duty text "the duties of X" -> entries averaged for its weight
COMPILED = {
    "parent": ["your_parent", "your_child"],
    "child": ["your_parent", "your_child"],
    "sibling": ["sibling"],
    "kin": ["kin"],
    "spouse": ["spouse"],
    "partner": ["partner"],
    "friend": ["friend"],
    "guardian": ["in_your_charge", "your_guardian"],
    "caregiver": ["you_care_for", "your_carer"],
    "employer": ["you_employ", "your_employer"],
    "roommate": ["roommate"],
}

SYSTEM = """You rate relationships by the strength of the special obligations they carry.

For each person below, rate how strong the special obligations are that you have toward them, beyond
what you owe anyone at all. 0 = nothing beyond what anyone is owed; 6 = the strongest obligations people
have. Use whole numbers.

Return only a JSON object mapping each id to its rating."""


def call(model, keys):
    lines = "\n".join(f'"{k}": {ENTRIES[k]}' for k in keys)
    body = {"model": model, "temperature": 0, "max_tokens": 600,
            "chat_template_kwargs": {"enable_thinking": False},
            "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": lines}]}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                out = json.load(r)
            s = out["choices"][0]["message"]["content"] or ""
            d = json.loads(s[s.index("{"): s.rindex("}") + 1])
            rat = {k: int(d[k]) for k in keys}
            if all(0 <= v <= 6 for v in rat.values()):
                return out["model"], rat
        except Exception as e:                                   # noqa: BLE001
            print(model, "attempt", attempt, repr(e)[:200], flush=True)
        time.sleep(10 * 2 ** attempt)
    raise RuntimeError(f"{model}: no valid rating")


def spearman(a, b):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def main(out, *models):
    raw = []
    for m in models:
        for seed in SEEDS:
            keys = list(ENTRIES)
            random.Random(seed).shuffle(keys)
            served, rat = call(m, keys)
            raw.append({"model": m, "served": served, "seed": seed, "ratings": rat})
            print(m, seed, rat, flush=True)
    per_model = {m: {k: float(np.mean([r["ratings"][k] for r in raw if r["model"] == m])) for k in ENTRIES}
                 for m in models}
    weight = {k: float(np.mean([r["ratings"][k] for r in raw])) / 6 for k in ENTRIES}
    res = {"raw": raw, "per_model": per_model, "weight_entry": weight,
           "weight_compiled": {c: float(np.mean([weight[e] for e in es])) for c, es in COMPILED.items()}}
    if len(models) == 2:
        a, b = (np.array([per_model[m][k] for k in ENTRIES]) for m in models)
        res["spearman_models"] = spearman(a, b)
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("weight_compiled", "spearman_models") if k in res}, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:])
