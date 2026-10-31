#!/usr/bin/env python3
"""Print a compact view of explore_readers.json."""
import json
import os

o = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "explore_readers.json")))
for h, f in o["folds"].items():
    m = f["models"]
    print(h, "cpt", f["cpt_coding"], {k: round(v["test_nll"], 4) for k, v in m.items()})
    print("   llo gamma, delta", [round(t, 3) for t in m["GDTS-llo"]["theta"][6:]], m["GDTS-llo"]["reader_on_heldout"])
    print("   eff train loss by n", {k: round(v, 5) for k, v in m["GDTS-eff"]["train_loss_by_n"].items()})
    print("   gdts weights lin", [round(t, 2) for t in m["GDTS-lin"]["theta"][:6]], "llo", [round(t, 2) for t in m["GDTS-llo"]["theta"][:6]])
print(json.dumps(o["pooled"], indent=1))
