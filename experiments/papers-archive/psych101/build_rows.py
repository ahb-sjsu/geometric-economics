#!/usr/bin/env python3
"""Rows for prereg-psych101-v1 from wulff2018description/exp1.csv in Psych-101.

Covariates and outcomes go to SEPARATE files. The rehearsal and every check that
runs before the seal load only `rows_covariates.npz`, so they cannot read a choice.

What the transcripts contain, read with choices masked (`inspect_stimuli.py`):

    Lottery W offers 4.0 points with 80.0% probability or 0.0 points with 20.0% probability.
    Lottery H offers 3.0 points with 100.0% probability.
    You press <<W>>.

One description, one press, per problem. Every press token lands in a named bucket
and the buckets must sum to the number of press tokens in the corpus. `census`
asserts it, and a failed assertion voids the study (V1).

Option A is the first lottery listed, option B the second. Each option is reduced
to (H, pH, L) with H >= L. A one-branch option is (x, 1, x).

Problems that repeat a CPC18 problem are dropped, keyed as in `overlap_stimuli.py`
(unordered pair of the options' expected value and minimum outcome).

    python build_rows.py      # on Atlas, writes rows_covariates.npz and rows_outcome.npz
"""
from __future__ import annotations

import collections
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from overlap_stimuli import cpc18_keys, opt_key  # noqa: E402  the overlap key, not restated

EXPERIMENT = "wulff2018description/exp1.csv"
LOT = re.compile(r"Lottery ([A-Z]) offers (.+?)\.\s*$")
BRANCH = re.compile(r"(-?[\d.]+) points with ([\d.]+)% probability")
PRESS = re.compile(r"You press <<([^>]*)>>")
TOKEN = re.compile(r"<<[^>]*>>")
CPC18_RAW = os.path.join(HERE, "..", "..", "datasets", "raw", "cpc18_raw.csv")


def option(payload):
    br = [(float(x), float(p) / 100.0) for x, p in BRANCH.findall(payload)]
    if not br:
        return None, "branches_not_parsed"
    if len(br) > 2:
        return None, "more_than_two_branches"
    if abs(sum(p for _, p in br) - 1.0) > 1e-6:
        return None, "probabilities_do_not_sum_to_one"
    if len(br) == 1:
        x = br[0][0]
        return (x, 1.0, x), None
    (x1, p1), (x2, p2) = br
    return ((x1, p1, x2) if x1 >= x2 else (x2, p2, x1)), None


def census(text):
    """Yield (bucket, optA, optB, chose_B) per press token, in transcript order."""
    menu, order = {}, []
    for ln in text.split("\n"):
        m = LOT.search(ln.strip())
        if m:
            menu[m.group(1)] = m.group(2)
            order.append(m.group(1))
            continue
        for key in PRESS.findall(ln):
            if len(order) != 2:
                yield ("press_without_two_lottery_menu", None, None, None)
            elif key not in menu:
                yield ("press_key_not_on_menu", None, None, None)
            else:
                a, ea = option(menu[order[0]])
                b, eb = option(menu[order[1]])
                if ea or eb:
                    yield (ea or eb, None, None, None)
                else:
                    yield ("two_option_described", a, b, int(key == order[1]))
            menu, order = {}, []


def main():
    from datasets import load_dataset
    ds = load_dataset("marcelbinz/Psych-101", split="train")
    ds = ds.filter(lambda r: r["experiment"] == EXPERIMENT)
    ck = cpc18_keys(CPC18_RAW)

    buckets = collections.Counter()
    n_tokens = 0
    cov, out = [], []
    for pi, r in enumerate(ds):
        n_tokens += len(TOKEN.findall(r["text"]))
        for bucket, a, b, y in census(r["text"]):
            if bucket == "two_option_described":
                ka = opt_key([(a[0], a[1]), (a[2], 1 - a[1])] if a[1] < 1 else [(a[0], 1.0)])
                kb = opt_key([(b[0], b[1]), (b[2], 1 - b[1])] if b[1] < 1 else [(b[0], 1.0)])
                if tuple(sorted([ka, kb])) in ck:
                    bucket = "repeats_a_cpc18_problem"
            buckets[bucket] += 1
            if bucket == "two_option_described":
                cov.append((pi, *a, *b))
                out.append(y)
    assert sum(buckets.values()) == n_tokens, (dict(buckets), n_tokens)

    cov = np.array(cov, dtype=float)
    keys = [repr(tuple(sorted([tuple(row[1:4]), tuple(row[4:7])]))) for row in cov]
    uniq = {k: i for i, k in enumerate(sorted(set(keys)))}
    np.savez_compressed(os.path.join(HERE, "rows_covariates.npz"),
                        participant=cov[:, 0].astype(int),
                        problem=np.array([uniq[k] for k in keys]),
                        A=cov[:, 1:4], B=cov[:, 4:7])
    np.savez_compressed(os.path.join(HERE, "rows_outcome.npz"), chose_B=np.array(out, dtype=np.int8))
    print("participants", len(ds), "press tokens", n_tokens)
    for k, v in sorted(buckets.items()):
        print(f"  {k:<36} {v:>7}  {100 * v / n_tokens:6.2f}%")
    print("rows kept", len(out), "distinct problems", len(uniq))


if __name__ == "__main__":
    main()
