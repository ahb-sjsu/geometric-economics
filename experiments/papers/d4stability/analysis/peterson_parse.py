#!/usr/bin/env python3
"""Parser for peterson2021using/exp1.csv transcripts in Psych-101.

Written after two earlier parsers were wrong in ways only an audit found.

The first yielded a trial only when exactly two option declarations were pending,
so it captured the first press on each problem and silently discarded the four
that followed. It gave a defensible subset for an indefensible reason, and 91
percent of the corpus went missing without a word.

The second replaced silence with accounting, and the accounting immediately
indicted it: 45.8 percent of press tokens landed in a bucket named "no declared
menu". Reading the line templates showed why. Many options are lotteries of three
to ten branches, written as a comma list, and a two-branch regex cannot see them.

**The rule is that every press token is accounted for, and no bucket is a
shrug.** Each press lands in a named bucket, the buckets sum to the corpus total,
and `census` asserts the sum.

What the transcripts contain, read rather than assumed:

    Option L delivers 10.0 points with 80.0% chance, or -25.0 points with 20.0% chance.
    Option B delivers 0.0 points with 20.0% chance, or 5.0 points with 80.0% chance.
    You press <<B>>. You receive 5.0 points by selecting this option. You would
      have received 10.0 points had you chosen the other option.
    ... four more presses on the same pair ...

A problem is declared once and chosen from five times, with outcome feedback
reported inline after each press. The instructions say feedback is suppressed for
some problems, so a press line carrying no feedback clause is the no-feedback
condition and not a parse failure.

Four consequences for any analysis of this corpus:

1. **Only the first press on a problem is a decision from description.** Presses
   two onward follow outcome feedback on that same problem and are decisions from
   experience, a different phenomenon.
2. **Options may have three to ten branches.** The coordinate `_opt_coords` is a
   two-outcome function of `(H, p, L)`. Extending it to a ten-branch lottery
   would mean writing a new coordinate and calling it the old one, which is
   precisely what voided `prereg-d4gate-v1`. Multi-branch problems are therefore
   **excluded and counted**, never approximated.
3. **Some options state "unknown chance".** Those are ambiguity trials with no
   stated probability and no computable coordinate.
4. **A certain option is sometimes written in two-branch form**, as "either X
   with 100.0% chance, or Y with 0.0% chance". That is two branches and is
   handled as such.

    python peterson_parse.py        # self-test on the shipped example
"""
from __future__ import annotations

import collections
import re

import numpy as np

# An option line, whatever its number of branches. The payload is split
# separately so the branch count is read rather than baked into the pattern.
OPTION_LINE = re.compile(r"Option ([A-Z]) delivers (?:either )?(.+?)\.\s*$")
BRANCH = re.compile(r"(-?[\d.]+) points with (unknown|[\d.]+%) chance")
PRESS = re.compile(r"You press <<([A-Z])>>\.")
FEEDBACK = re.compile(r"You receive (-?[\d.]+) points by selecting this option")

# Kept for callers that only need to know a line declares an option at all.
OPTION = OPTION_LINE

PRESS_FIRST = "first_press_description"
PRESS_REPEAT = "repeat_press_experience"
PRESS_AMBIGUOUS = "ambiguous_unknown_probability"
PRESS_MULTI = "multi_outcome_out_of_scope"
PRESS_NO_MENU = "press_with_no_declared_menu"
PRESS_BAD_KEY = "press_key_not_on_menu"
BUCKETS = (PRESS_FIRST, PRESS_REPEAT, PRESS_AMBIGUOUS, PRESS_MULTI,
           PRESS_NO_MENU, PRESS_BAD_KEY)

# status codes for a parsed option
OK, UNKNOWN_P, MULTI = "ok", "unknown_probability", "multi_outcome"


def parse_option(line):
    """(key, status, (H, p, L) or None, n_branches) for one option line."""
    m = OPTION_LINE.search(line)
    if not m:
        return None
    key, payload = m.group(1), m.group(2)
    br = BRANCH.findall(payload)
    if not br:
        return None
    if any(c == "unknown" for _x, c in br):
        return key, UNKNOWN_P, None, len(br)
    if len(br) > 2:
        return key, MULTI, None, len(br)
    vals = [(float(x), float(c.rstrip("%")) / 100.0) for x, c in br]
    if len(vals) == 1:
        (x1, _p1), = vals
        return key, OK, (x1, 1.0, x1), 1
    (x1, p1), (x2, p2) = vals
    if x1 >= x2:
        return key, OK, (x1, p1, x2), 2
    return key, OK, (x2, p2, x1), 2


def problems(text):
    """Yield one record per declared problem, in transcript order."""
    menu, order, presses = {}, [], []
    have_press = False

    def flush():
        return {"menu": dict(menu), "order": list(order),
                "presses": list(presses)} if order else None

    for ln in text.split("\n"):
        got = parse_option(ln)
        if got:
            if have_press:                       # a new menu closes the old one
                rec = flush()
                if rec:
                    yield rec
                menu, order, presses = {}, [], []
                have_press = False
            key, status, opt, nbr = got
            if key not in menu:
                order.append(key)
            menu[key] = (status, opt, nbr)
            continue
        m = PRESS.search(ln)
        if m:
            have_press = True
            fb = FEEDBACK.search(ln)
            presses.append((m.group(1),
                            float(fb.group(1)) if fb else None,
                            fb is not None))
    rec = flush()
    if rec:
        yield rec


def trials(text):
    """Yield (bucket, option_a, option_b, chose_a, index, had_feedback) for
    every press token in the transcript.

    Precedence among the exclusion buckets is fixed here and not left to the
    caller: a menu that is both ambiguous and multi-branch counts as ambiguous.
    """
    n_seen = 0
    for rec in problems(text):
        keys, menu = rec["order"], rec["menu"]
        two = len(keys) == 2
        if two:
            (sa, a, _na), (sb, b, _nb) = menu[keys[0]], menu[keys[1]]
        for i, (pressed, _payoff, had_fb) in enumerate(rec["presses"]):
            n_seen += 1
            if not two:
                yield PRESS_NO_MENU, None, None, None, i, had_fb
            elif UNKNOWN_P in (sa, sb):
                yield PRESS_AMBIGUOUS, None, None, None, i, had_fb
            elif MULTI in (sa, sb):
                yield PRESS_MULTI, None, None, None, i, had_fb
            elif pressed not in menu:
                yield PRESS_BAD_KEY, None, None, None, i, had_fb
            else:
                bucket = PRESS_FIRST if i == 0 else PRESS_REPEAT
                yield bucket, a, b, pressed == keys[0], i, had_fb
    total = len(PRESS.findall(text))
    for _ in range(total - n_seen):
        yield PRESS_NO_MENU, None, None, None, -1, None


def census(texts):
    """Bucket counts over many transcripts, asserting they sum to the corpus."""
    counts = collections.Counter()
    total = 0
    for t in texts:
        total += len(PRESS.findall(t))
        for rec in trials(t):
            counts[rec[0]] += 1
    assert sum(counts.values()) == total, (
        "press accounting does not balance: %d bucketed against %d tokens"
        % (sum(counts.values()), total))
    return counts, total


def feats(H, p, L):
    ev = p * H + (1 - p) * L
    var = p * (H - ev) ** 2 + (1 - p) * (L - ev) ** 2
    return float(ev), float(np.sqrt(max(var, 0.0)))


_EXAMPLE = """You will encounter a series of gambling problems.
Option L delivers 10.0 points with 80.0% chance, or -25.0 points with 20.0% chance.
Option B delivers 0.0 points with 20.0% chance, or 5.0 points with 80.0% chance.
You press <<B>>. You receive 5.0 points by selecting this option. You would have received 10.0 points had you chosen the other option.
You press <<B>>. You receive 5.0 points by selecting this option. You would have received -25.0 points had you chosen the other option.
Option L delivers either 30.0 points with 100.0% chance, or 30.0 points with 0.0% chance.
Option B delivers either 0.0 points with unknown chance, or 42.0 points with unknown chance.
You press <<L>>. You receive 30.0 points by selecting this option.
Option C delivers 1.0 points with 10.0% chance, 2.0 points with 40.0% chance, or 3.0 points with 50.0% chance.
Option D delivers 2.0 points with 100.0% chance.
You press <<C>>.
"""

if __name__ == "__main__":
    for bucket, a, b, chose_a, i, fb in trials(_EXAMPLE):
        print("  i=%2d  %-30s a=%s b=%s chose_a=%s fb=%s"
              % (i, bucket, a, b, chose_a, fb))
    counts, total = census([_EXAMPLE])
    print()
    print("  census:", dict(counts), " total press tokens:", total)
    assert counts[PRESS_FIRST] == 1, counts
    assert counts[PRESS_REPEAT] == 1, counts
    assert counts[PRESS_AMBIGUOUS] == 1, counts
    assert counts[PRESS_MULTI] == 1, counts
    assert parse_option(
        "Option C delivers 1.0 points with 10.0% chance, 2.0 points with "
        "40.0% chance, or 3.0 points with 50.0% chance.")[1] == MULTI
    assert parse_option("Option D delivers 2.0 points with 100.0% chance.")[2] \
        == (2.0, 1.0, 2.0)
    print("  self-test passed")
