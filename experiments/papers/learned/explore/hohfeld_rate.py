#!/usr/bin/env python3
"""DEVELOPMENT. LLM raters label each sampled action for the Hohfeld test of direction 0.

Each rater sees one action text at a time and nothing else: not direction 0, not the decile, not the
other rater. Labels, about the party most directly affected by the act:

- affected: who that party is;
- closeness 0-6: how close the narrator is to them;
- position: the narrator's Hohfeldian position toward them regarding this act (erisml HohfeldianState):
  O, the narrator owes them a duty here (they hold a claim, C), or L, the narrator is at liberty (they
  hold no claim, N);
- breach: the act violates that duty (only possible under O);
- omission: the act is a failure to act rather than an action;
- severity 0-6: how much harm or wrong the act does to them, whoever they are.

Calls go to the NRP managed LLM gateway at temperature 0, one item per call, a few in flight per model
(fair-use limits: 8 concurrent for gemma and qwen3-small), with growing back-off on errors. The output
is resumable: items already rated are skipped. The served model name is recorded on every row.

    python hohfeld_rate.py ITEMS.jsonl OUT_DIR MODEL [MODEL ...]
"""
import json
import os
import random
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = "https://ellm.nrp-nautilus.io/v1/chat/completions"
TOKEN = open(os.path.expanduser("~/.llmtoken")).read().strip()
IN_FLIGHT = 4
AFFECTED = ["self_only", "family", "romantic_partner", "friend", "acquaintance_or_coworker",
            "stranger_or_public", "animal", "nobody"]

SYSTEM = """You label short descriptions of something a person (the narrator, "I") did or considered doing.
Judge the act as described. Do not guess at missing context.

Identify the party most directly affected by the act, other than the narrator. If only the narrator is
affected, that party is "self_only".

Return only a JSON object with these keys:
"affected": one of "self_only", "family", "romantic_partner", "friend", "acquaintance_or_coworker",
  "stranger_or_public", "animal", "nobody".
"closeness": integer 0-6, how close the narrator is to that party. 0 = stranger, no relation, or self_only;
  3 = acquaintance, coworker or casual friend; 6 = immediate family, spouse or partner.
"position": the narrator's position toward that party regarding this act, in Hohfeld's terms.
  "O" if the narrator owes that party a duty concerning this act, so that the party has a claim against
  the narrator here (for example a claim not to be harmed, deceived, abandoned or exposed, or a claim to
  care, support or a kept promise). "L" if the narrator is at liberty to do it: the party has no claim
  against the narrator concerning this act.
"breach": true if position is "O" and the act, as described, violates that duty; otherwise false.
"omission": true if the act is a failure or refusal to do something (not helping, not attending, refusing,
  cutting off contact); false if it is a positive action.
"severity": integer 0-6, how much harm or wrong the act does to that party, whoever they are.
  0 = none, 3 = moderate, 6 = grave.
"""


def call(model, text):
    body = {"model": model, "temperature": 0, "max_tokens": 200,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": f"Act: {text}"}]}
    body["chat_template_kwargs"] = {"enable_thinking": False}  # qwen reasons otherwise; gemma ignores it
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        out = json.load(r)
    return out["model"], out["choices"][0]["message"]["content"] or ""


def parse(raw):
    s = raw.strip()
    if s.startswith("```"):
        s = s.strip("`").removeprefix("json").strip()
    d = json.loads(s[s.index("{"): s.rindex("}") + 1])
    lab = {"affected": d["affected"], "closeness": int(d["closeness"]), "position": d["position"],
           "breach": bool(d["breach"]), "omission": bool(d["omission"]), "severity": int(d["severity"])}
    if (lab["affected"] not in AFFECTED or lab["position"] not in ("O", "L")
            or not 0 <= lab["closeness"] <= 6 or not 0 <= lab["severity"] <= 6):
        raise ValueError(f"out of range: {lab}")
    if lab["position"] == "L":
        lab["breach"] = False                              # breach is defined only under a duty
    return lab


def rate(model, item, lock, f):
    delay = 5.0
    for attempt in range(6):
        try:
            served, raw = call(model, item["text"])
            try:
                lab = parse(raw)
                row = {"item": item["item"], "model": model, "served": served, **lab}
            except (ValueError, KeyError, TypeError) as e:
                if attempt < 2:
                    continue                               # malformed answer: ask again
                row = {"item": item["item"], "model": model, "served": served, "error": f"parse: {e}",
                       "raw": raw[:500]}
            with lock:
                f.write(json.dumps(row) + "\n")
                f.flush()
            return
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            time.sleep(delay + random.random() * delay)
            delay = min(delay * 2, 300)
            last = str(e)
    with lock:
        f.write(json.dumps({"item": item["item"], "model": model, "error": f"http: {last}"}) + "\n")
        f.flush()


def main(items_path, out_dir, *models):
    items = [json.loads(l) for l in open(items_path, encoding="utf-8")]
    for model in models:
        path = os.path.join(out_dir, f"hohfeld_ratings_{model}.jsonl")
        done = set()
        if os.path.exists(path):
            done = {json.loads(l)["item"] for l in open(path, encoding="utf-8")
                    if "error" not in json.loads(l)}
        todo = [it for it in items if it["item"] not in done]
        print(f"{model}: {len(todo)} to rate", flush=True)
        lock = threading.Lock()
        t0 = time.time()
        with open(path, "a", encoding="utf-8") as f, ThreadPoolExecutor(IN_FLIGHT) as ex:
            for k, _ in enumerate(ex.map(lambda it: rate(model, it, lock, f), todo), 1):
                if k % 100 == 0:
                    print(f"  {model} {k}/{len(todo)} {time.time() - t0:.0f}s", flush=True)
        print(f"{model} DONE", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
