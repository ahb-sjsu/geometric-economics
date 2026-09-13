#!/usr/bin/env python3
"""Third structure probe. Parse completeness and the description assumption.

Probe 2 found 206 participants parsing to zero trials while all 206 contain a
press token. A parser that drops transcripts it does not understand selects its
own sample, so the first job here is to count every press token in the corpus and
account for each one. The 206 are visible. Presses dropped inside an otherwise
working transcript are not, and those are the dangerous ones.

The second job is the description assumption. The aggregate fit of
`prereg-d4interior-v3` used choices13k with `Block == 1` and `Feedback == 0`,
which is decision from description with no outcome feedback. Only 18.1 percent of
peterson's problems are in that subset, so whether peterson's trials are
themselves description-only is not a detail, it decides what corpus this is. If
outcome feedback appears in the transcripts then later trials are decisions from
experience and are a different phenomenon.

Covariates and transcript structure only. No model is fitted.

    python peterson_probe3.py
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from peterson_probe import OPT, PRESS, parse  # noqa: E402

# candidate feedback markers. a decision-from-experience trial has to tell the
# participant what happened, so it has to say so somewhere in the transcript.
FEEDBACK_PAT = re.compile(
    r"you (?:receive|received|get|got|earn|earned|win|won|lose|lost)\b"
    r"|outcome|payoff|feedback|resulted in|you obtain", re.I)


def main():
    from datasets import load_dataset
    ds = load_dataset("marcelbinz/Psych-101", split="train")
    rows = [r for r in ds if r["experiment"] == "peterson2021using/exp1.csv"]

    n_press = n_parsed = 0
    n_fb_lines = 0
    fb_examples, unparsed_examples = [], []
    line_shapes = collections.Counter()

    for i, r in enumerate(rows):
        text = r["text"]
        presses = PRESS.findall(text)
        n_press += len(presses)
        k = sum(1 for _ in parse(text))
        n_parsed += k

        for ln in text.split("\n"):
            if FEEDBACK_PAT.search(ln):
                n_fb_lines += 1
                if len(fb_examples) < 6:
                    fb_examples.append(ln.strip()[:140])

        if k < len(presses) and len(unparsed_examples) < 3:
            unparsed_examples.append((i, len(presses), k, text))

    print("press tokens in corpus : %d" % n_press)
    print("trials parsed          : %d" % n_parsed)
    print("DROPPED                : %d  (%.2f%%)"
          % (n_press - n_parsed, 100.0 * (n_press - n_parsed) / max(n_press, 1)))
    print()
    print("lines matching a feedback marker: %d" % n_fb_lines)
    for e in fb_examples:
        print("    | " + e)
    print()

    # what do the transcripts of participants with dropped presses look like?
    for i, npress, k, text in unparsed_examples:
        print("participant %d: %d presses, %d parsed. full transcript:" % (i, npress, k))
        for ln in text.split("\n"):
            if ln.strip():
                print("    | " + ln.strip()[:150])
        print()

    # the shape of every distinct line template, so nothing is assumed about the
    # format. numbers are replaced by a placeholder and the templates counted.
    num = re.compile(r"-?\d+\.?\d*")
    for r in rows[:400]:
        for ln in r["text"].split("\n"):
            s = ln.strip()
            if s:
                line_shapes[num.sub("#", s)[:120]] += 1
    print("line templates in the first 400 transcripts, by frequency:")
    for t, c in line_shapes.most_common(12):
        print("  %7d  %s" % (c, t))

    out = {
        "n_press_tokens": int(n_press),
        "n_trials_parsed": int(n_parsed),
        "n_dropped": int(n_press - n_parsed),
        "dropped_fraction": float((n_press - n_parsed) / max(n_press, 1)),
        "n_feedback_marker_lines": int(n_fb_lines),
        "feedback_examples": fb_examples,
        "line_templates_top12": [[c, t] for t, c in line_shapes.most_common(12)],
    }
    with open(os.path.join(HERE, "peterson_probe3.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print()
    print("written peterson_probe3.json")


if __name__ == "__main__":
    main()
