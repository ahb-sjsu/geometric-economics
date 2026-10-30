#!/usr/bin/env python3
"""Build every text the learned-coordinates study embeds, from frozen sources.

Three sets, written to inputs.json:

  anchors   The codebook's anchor pairs (tcss-part2/codebook-v1.md), one per
            coordinate, parsed verbatim. Each pair defines a hand-specified axis
            as e(anchor 1) - e(anchor 0). These are the Part I coordinates
            expressed as text, fixed before any behavior is seen.
  panel     The projection-gap panel contrasts (projection-gap/contrasts.py),
            real and placebo. For each contrast and each pole (lo, hi), one text
            per option: the pole's scenario followed by the option's own clause.
  scruples  Not built here. fit_learned.py reads the Scruples jsonl directly,
            because its action texts are the data and need no construction.

Run locally or on Atlas. It reads only the repository and writes inputs.json.
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CODEBOOK = os.path.join(REPO, "experiments", "papers", "tcss-part2", "codebook-v1.md")
PG = os.path.join(REPO, "experiments", "projection-gap")

OPTION_RE = re.compile(r"(?:Option|Choice) A: (.*?)\.\s+(?:Option|Choice) B: (.*?)\.(?:\s|$)")


def parse_anchors() -> list[dict]:
    s = open(CODEBOOK, encoding="utf-8").read()
    out = []
    for sec in re.finditer(r"^## (d\d)[^\n]*\n(.*?)(?=^## |\Z)", s, re.S | re.M):
        coord, body = sec.group(1), sec.group(2)
        m = re.search(r"- \*\*Anchors[^*]*\*\*(.*?)(?=\n- \*\*|\Z)", body, re.S)
        if not m:
            continue
        text = " ".join(m.group(1).split())
        parts = re.split(r"\*\*\((5b)\)\.\*\*", text)
        chunks = [(coord if len(parts) == 1 else coord + "a", parts[0])]
        if len(parts) == 3:
            chunks.append((coord + "b", parts[2]))
        for name, chunk in chunks:
            a = re.search(r"0 = (.*?); 1 = (.*?)\.?\s*$", chunk.strip())
            if not a:
                sys.exit(f"anchor parse failed for {name}: {chunk!r}")
            out.append({"axis": name, "zero": a.group(1).strip(), "one": a.group(2).strip()})
    return out


def panel_texts() -> list[dict]:
    sys.path.insert(0, PG)
    import contrasts  # noqa: E402  (frozen stimulus module)

    rows = []
    for c in contrasts.GAME + contrasts.LOTTERY + contrasts.PLACEBO:
        cid, kind, coord = c.id, c.kind, c.coord
        lo = c.prompt_lo[: -len(contrasts.ANSWER)]
        hi = c.prompt_hi[: -len(contrasts.ANSWER)]
        if kind not in ("real", "placebo"):
            continue
        poles = {}
        for pole, text in (("lo", lo), ("hi", hi)):
            m = OPTION_RE.search(text)
            if not m:
                sys.exit(f"option parse failed for {cid} {pole}: {text!r}")
            poles[pole] = {
                "A": f"{text} I choose: {m.group(1)}.",
                "B": f"{text} I choose: {m.group(2)}.",
            }
        rows.append({"id": cid, "kind": kind, "coord": coord, "poles": poles})
    return rows


def main() -> None:
    out = {"anchors": parse_anchors(), "panel": panel_texts()}
    assert len(out["anchors"]) == 10, len(out["anchors"])
    with open(os.path.join(HERE, "inputs.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"anchors {len(out['anchors'])}, panel contrasts {len(out['panel'])}")
    for p in out["panel"]:
        print(p["id"], p["kind"], p["coord"])


if __name__ == "__main__":
    main()
