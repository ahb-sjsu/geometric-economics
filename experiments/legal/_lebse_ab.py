#!/usr/bin/env python3
"""A/B proof: does swapping LaBSE->LeBSE change the rule-extractor 9-dim moral vector?
Runs the SAME fixed legal text through compile_opinion(extractor='rule') and prints the vector as
JSON. Invoke twice with different ERISML_LABSE_MODEL; identical vectors => LaBSE/LeBSE is NOT on the
rule-extractor path (as the source indicates). CPU only."""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.environ.setdefault("ERISML_LABSE_DEVICE", "cpu")   # never touch the GPUs from this probe

TEXT = ("The district court held that the defendant physician breached his duty of care when he "
        "concealed the patient's diagnosis, and that the hospital coerced the family into waiving "
        "their right to a second opinion. The court found the waiver was not voluntary and vacated "
        "the settlement, holding the town's residents were exposed to ongoing risk of harm.")

from legal_compile import compile_opinion
res = compile_opinion(TEXT, extractor="rule")
print(json.dumps({"model": os.environ.get("ERISML_LABSE_MODEL", "DEFAULT(LaBSE)"),
                  "vec": [round(x, 6) for x in (res.get("moral_vector") or [])],
                  "gate_failures": res.get("gate_failures"), "deme": res.get("deme"),
                  "vnote": res.get("_vnote")}))
