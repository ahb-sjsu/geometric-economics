#!/usr/bin/env python3
"""DEVELOPMENT. Compile each sampled action with erisml-compiler and keep its duty structure.

Each action goes through `compile_document` (LLM tier, default projections, default DEME weights) as
"I did the following: <action>." The model is reached through the compiler's own ModelAdapter
interface; the adapter here only adds what the compiler's NRP adapter lacks for this model: thinking
off and temperature 0. One row per action records the narrator's commitments, the ethical facts, and
DEME's nine-dimension MoralVector. Resumable.

    python compile_actions.py ITEMS.jsonl OUT.jsonl [MODEL]
"""
import json
import os
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from openai import OpenAI

from erisml_compiler.annotation.llm_extractor import ModelAdapter
from erisml_compiler.pipeline.orchestrator import CompileOptions, compile_document
from erisml_compiler.tiers import CompilerTier

try:                                                       # present once the duty-breach fix is installed
    from erisml_compiler.erisml_backend.v3_bridge import breached_duties
except ImportError:
    breached_duties = None

DEME_DIMS = ("physical_harm", "rights_respect", "fairness_equity", "autonomy_respect", "privacy_protection",
             "societal_environmental", "virtue_care", "legitimacy_trust", "epistemic_quality")
IN_FLIGHT = 4


class GatewayAdapter(ModelAdapter):
    name = "nrp_gateway_thinking_off"

    def __init__(self, model):
        self.model = model
        self._client = OpenAI(base_url="https://ellm.nrp-nautilus.io/v1",
                              api_key=open(os.path.expanduser("~/.llmtoken")).read().strip(), timeout=300)
        self.served = set()

    def call(self, system, user, **kwargs):
        delay = 5.0
        for attempt in range(6):
            try:
                r = self._client.chat.completions.create(
                    model=self.model, temperature=0, max_tokens=kwargs.get("max_tokens", 2048),
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                    extra_body={"chat_template_kwargs": {"enable_thinking": False}})
                self.served.add(r.model)
                return (r.choices[0].message.content or "").strip()
            except Exception:
                if attempt == 5:
                    raise
                time.sleep(delay)
                delay = min(delay * 2, 300)


def narrator(ir):
    agents = [s for s in ir.stakeholders if "agent" in s.roles]
    for s in agents:
        if s.id in ("narrator", "i", "me", "self") or "narrator" in s.id or s.label.lower() in ("i", "me", "narrator"):
            return s.id
    return agents[0].id if agents else None


def compile_one(adapter, item):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(f"I did the following: {item['text']}.\n")
        path = f.name
    try:
        ir = compile_document(path, CompileOptions(tier=CompilerTier.LLM, extractor="llm", llm_adapter=adapter))
    finally:
        os.unlink(path)
    me = narrator(ir)
    mv = ir.moral_vectors[0] if ir.moral_vectors else None
    return {
        "item": item["item"], "agent": me,
        "stakeholders": [{"id": s.id, "label": s.label, "roles": list(s.roles), "vulnerability": s.vulnerability}
                         for s in ir.stakeholders],
        "commitments": [{"type": c.type, "holder": c.holder, "beneficiary": c.beneficiary, "status": c.status,
                         "content": c.content} for c in ir.commitments],
        "facts": [{"kind": e.kind, "subjects": list(e.subjects), "severity": e.severity} for e in ir.ethical_facts],
        "moral_vector": {d: float(getattr(mv, d)) for d in DEME_DIMS} if mv is not None else None,
        "deme_verdict": (ir.deme_verdict.model_dump(mode="json") if hasattr(ir.deme_verdict, "model_dump")
                         else None),
        "duties_breached": breached_duties(ir) if breached_duties else None,
        "ir": {"stakeholders": [s.model_dump(mode="json") for s in ir.stakeholders],
               "commitments": [c.model_dump(mode="json") for c in ir.commitments],
               "ethical_facts": [e.model_dump(mode="json") for e in ir.ethical_facts]},
    }


def main(items_path, out, model="qwen3-small"):
    items = [json.loads(l) for l in open(items_path, encoding="utf-8")]
    done = set()
    if os.path.exists(out):
        done = {json.loads(l)["item"] for l in open(out, encoding="utf-8") if "error" not in json.loads(l)}
    todo = [it for it in items if it["item"] not in done]
    adapter = GatewayAdapter(model)
    lock = threading.Lock()
    t0 = time.time()
    print(f"{len(todo)} to compile with {model}", flush=True)

    def work(it):
        try:
            row = compile_one(adapter, it)
        except Exception as e:                              # noqa: BLE001 - recorded, counted toward void
            row = {"item": it["item"], "error": f"{type(e).__name__}: {str(e)[:300]}"}
        row["model"], row["served"] = model, sorted(adapter.served)
        with lock, open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")

    with ThreadPoolExecutor(IN_FLIGHT) as ex:
        for k, _ in enumerate(ex.map(work, todo), 1):
            if k % 50 == 0:
                print(f"  {k}/{len(todo)} {time.time() - t0:.0f}s", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
