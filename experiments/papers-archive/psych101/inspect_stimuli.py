#!/usr/bin/env python3
"""List Psych-101 risky-choice files and show their transcript format. Stimuli only.

Every choice token "<<X>>" is masked before printing, so this script cannot show
what anyone chose. It prints the experiment names with participant counts and the
first 1,200 characters of one transcript per candidate file.
"""
import re
import collections
from datasets import load_dataset

CANDIDATES = ["wulff2018description", "plonsky2018when", "hilbig2014generalized",
              "frey2017risk", "frey2017cct", "peterson2021using", "ruggeri2022globalizability",
              "wulff2018sampling"]
MASK = re.compile(r"<<[^>]*>>")

ds = load_dataset("marcelbinz/Psych-101", split="train")
counts = collections.Counter(ds["experiment"])
for e, n in sorted(counts.items()):
    print(f"{n:6d}  {e}")
print("=" * 60)
seen = set()
for r in ds:
    e = r["experiment"]
    stem = e.split("/")[0]
    if stem in CANDIDATES and e not in seen:
        seen.add(e)
        print("#####", e)
        print(MASK.sub("<<?>>", r["text"])[:1200])
