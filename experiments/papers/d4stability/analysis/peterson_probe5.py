#!/usr/bin/env python3
"""Fifth structure probe. What the unmatched option lines actually say.

Probe 4's accounting balanced, and in balancing it indicted the parser: 45.8
percent of press tokens, 502,680 of them, followed no menu the OPTION regex
recognised. Those presses are counted rather than dropped, which is the point of
the accounting, but a bucket holding nearly half the corpus is not a bucket, it
is an admission that the transcript format is still not understood.

This lists every distinct non-press line template in a sample of transcripts, so
the remaining option phrasings are read rather than guessed at. Numbers are
replaced by `#` and the templates counted.

    python peterson_probe5.py
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from peterson_parse import OPTION, PRESS  # noqa: E402

NUM = re.compile(r"-?\d+\.?\d*")


def main():
    from datasets import load_dataset
    ds = load_dataset("marcelbinz/Psych-101", split="train")
    rows = [r for r in ds if r["experiment"] == "peterson2021using/exp1.csv"]

    tmpl = collections.Counter()
    unmatched_option_like = collections.Counter()
    for r in rows[:1500]:
        for ln in r["text"].split("\n"):
            s = ln.strip()
            if not s or PRESS.search(s):
                continue
            t = NUM.sub("#", s)
            tmpl[t[:160]] += 1
            if OPTION.search(s) is None and ("Option" in s or "delivers" in s
                                             or "chance" in s):
                unmatched_option_like[t[:160]] += 1

    print("ALL non-press line templates in 1500 transcripts, by frequency")
    for t, c in tmpl.most_common(40):
        print("  %8d  %s" % (c, t))
    print()
    print("OPTION-LIKE lines the parser's regex does NOT match")
    for t, c in unmatched_option_like.most_common(25):
        print("  %8d  %s" % (c, t))
    if not unmatched_option_like:
        print("  none. every option-like line matches, so the unmatched presses")
        print("  are a segmentation problem and not a phrasing problem.")

    out = {
        "templates": [[c, t] for t, c in tmpl.most_common(60)],
        "unmatched_option_like": [[c, t]
                                  for t, c in unmatched_option_like.most_common(40)],
    }
    with open(os.path.join(HERE, "peterson_probe5.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written peterson_probe5.json")


if __name__ == "__main__":
    main()
