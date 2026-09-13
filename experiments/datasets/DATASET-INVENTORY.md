# Risky-choice dataset inventory for the interior (d, q) question

*Searched 2026-09-13, after `prereg-d4interior-v3` found the CPC18 interior
chirality of `+0.4438` does not replicate on choices13k, coming out at `−0.1216`.
The question was whether a third corpus exists or whether new data must be
collected. Written down because a search whose result is "no" is worth as much as
one whose result is "yes", and neither survives being left in a chat log.*

## What we already had, and what each can say about the interior

| Source | Interior rows | `d` coverage | Verdict |
|---|---|---|---|
| CPC18 | 270 | continuous | used, gives `+0.4438` with corners dropped |
| choices13k, aggregate | 2,380 | continuous, 573 negative against 1,793 positive | used, gives `−0.1216` |
| **Ruggeri / KT, 17 problems** | **0** | **every problem at `\|d\| = 1` exactly** | **cannot test the interior at all** |
| Fraser-Nettle | n/a | ultimatum, not lotteries | n/a |
| bogota, 110 games | n/a | games, not lotteries | n/a |
| Global Preferences Survey | n/a | preference scores, not choices | n/a |

The Ruggeri result is the structural one and is worth keeping in mind whenever
the corners come up. **The Kahneman and Tversky canon is the corners.** All
seventeen problems sit at `d = ±1`. That is why Part A of the rotation test works
on it and why it is silent about the interior, not for want of subjects but
because the stimuli do not live there.

`/archive` on Atlas holds no lottery data beyond the Fraser-Nettle and Ruggeri
files already local.

## Kaggle

Searched with the CLI. One relevant dataset, `kylefengkfeng209/would-you-take-this-gamble`,
which is **choices13k re-uploaded with renamed columns**. Verified rather than
assumed: 14,568 rows against 14,568, 13,006 problems against 13,006, and a
maximum absolute difference in the choice rate of **0.0**. It adds nothing.

Its companion, `kylefengkfeng209/can-llms-predict-human-choices`, is small but
carries `human_datasets.csv`, an index of the human corpora used across
LLM-versus-human studies. That index is what turned the search around.

## Psych-101, which is the answer

`marcelbinz/Psych-101` on HuggingFace, from Binz et al. 2025 in *Nature*.
Downloaded and inspected on Atlas, no authentication needed. 60,092 participants,
76 experiment files, 10.7 million choices, stored as natural-language transcripts
of trial-by-trial behaviour.

Risky-choice experiments in it, by participant count:

| Experiment | Participants | What it is |
|---|---|---|
| `peterson2021using/exp1.csv` | **13,735** | choices13k **at the individual trial level** |
| `wulff2018sampling/exp1.csv` | 3,942 | sampling paradigm |
| `wulff2018description/exp1.csv` | 1,981 | description-experience meta-analysis |
| `ruggeri2022globalizability/exp1.csv` | 11,937 | the KT corners, known to have no interior |
| `frey2017cct`, `frey2017risk` | 1,368, 1,331 | Columbia Card Task, risk-taking battery |
| `plonsky2018when/exp1.csv` | 216 | |

**The transcripts are trivially parseable.** Both formats are fully regular:

```
Lottery W offers 4.0 points with 80.0% probability or 0.0 points with 20.0% probability.
Option L delivers 10.0 points with 80.0% chance, or -25.0 points with 20.0% chance.
You press <<B>>.
```

so `(H, p, L)` and the individual choice both come out with a regular expression.
The `peterson2021using` sample above is a mixed gamble, gain and loss in one
option, which is interior `d` by construction.

## What each of these would and would not buy

**`peterson2021using` fixes precision, not coverage.** It is the same 13,006
problems as the choices13k we already used, so its `(d, q)` coverage is
identical. What changes is that the target becomes an individual binary choice
rather than a rate over a median of 16 subjects. That is a large gain in
information and it makes a within-subject stability test possible, which the
aggregate file cannot support. It is **not** an independent replication, because
it is the same stimuli and the same people.

**`wulff2018description` and `wulff2018sampling` are the candidates for new
coverage.** They come from a different literature with differently constructed
gambles, so their `(d, q)` occupancy is unknown and worth measuring. That
measurement is covariates-only and can be done before any registration.

**Nothing here is a designed interior grid.** All of it is opportunistic. The
designed set in `experiments/papers/d4design/` remains the only thing that would
place stimuli at chosen intermediate angles, and whether it is needed depends on
what the Wulff coverage turns out to be.

## Not obtained

Rieskamp 2008, 180 pairs spanning gain, loss and mixed domains, and Glöckner and
Pachur 2012, are the right shape and no public download was found. Author contact
or institutional access would be needed.

## The Wulff coverage, measured 2026-09-13

`wulff2018sampling` is **excluded on inspection**. It is the experience paradigm,
where the participant samples rather than being shown the lottery, so `(H, p, L)`
never appears in the transcript and could only be inferred from observed draws.

`wulff2018description` was parsed: 1,981 participants, 27,835 choices, 1,575
distinct problems. The transcripts are fully regular and the coordinate was
imported rather than restated. Measured against the two corpora already used, on
identical metrics:

| | wulff2018description | CPC18 | choices13k |
|---|---|---|---|
| distinct problems | 1,575 | 270 | 2,380 |
| distinct `d` values | 89 | 126 | **849** |
| `d < 0` / `d > 0` | 794 / 770 | 58 / 207 | 573 / 1,791 |
| interior, `\|d\| < 0.9` | 189 | 122 | **1,244** |
| **interior share** | **12.0%** | 45.2% | **52.3%** |
| sd of `d·q` | 0.578 | 0.564 | 0.517 |

**Wulff does not help.** It is 88 percent corners. Its one virtue is near-perfect
sign balance, 794 negative against 770 positive, which neither other corpus has,
but its interior holds 189 problems against the 1,244 choices13k already
supplied. Adding it would add corners to a question about the interior.

**choices13k is the best interior corpus available and it has already been used.**
It carries more interior problems than the other two combined, ten times the
distinct `d` values of Wulff, and it is what `prereg-d4interior-v3` ran on. The
verdict there, no replication with a sign reversal at power 1.000, is therefore
the best available evidence and not a limitation of the corpus.

## What that leaves

**The search for a third corpus is closed.** Nothing public has better interior
coverage than the corpus already used, and the negative is worth as much as the
positive would have been.

Two routes remain and they answer different questions.

1. **`peterson2021using` at the individual level.** Same 13,006 problems, so no
   coverage gain, but the target becomes an individual binary choice from 13,735
   participants instead of a rate over a median of 16. That buys precision and,
   more usefully, makes a **within-subject** stability test possible. If the
   chirality will not hold still inside one subject or one corpus, the
   between-corpus disagreement needs no further explanation and the question is
   closed without new data.
2. **The designed grid** in `experiments/papers/d4design/`. Still the only way to
   place stimuli at chosen intermediate angles, and still requiring a study to be
   run. Worth doing only if the stability test says the quantity is real but
   poorly sampled.

Route 1 first. It is cheaper, it uses data in hand, and its likeliest outcome
makes route 2 unnecessary.

## Route 1 was taken, and the corpus is not what the file above assumed

`experiments/papers/d4stability/` holds the registration. Two corrections to what
is written above are owed, both found by auditing the transcripts rather than
trusting them.

**`peterson2021using` is not 13,006 problems of usable description data.** A
problem is declared once and then chosen from five times, with outcome feedback
inline after each press, so only the first press on a problem is a decision from
description. The other four are decisions from experience. A first parser took
the first press and discarded the rest in silence, losing 91 percent of the
corpus without saying so.

**Most of its options are not two-outcome gambles.** Many are lotteries of three
to ten branches written as a comma list. The coordinate `_opt_coords` is a
two-outcome function and extending it would mean writing a new coordinate and
calling it the old one, so those problems are excluded and counted.

Every one of the 1,097,375 press tokens is now accounted for in a named bucket,
and the buckets sum to the corpus:

| bucket | presses | share |
|---|---|---|
| `first_press_description` | 96,237 | 8.77% |
| `repeat_press_experience` | 384,948 | 35.08% |
| `ambiguous_unknown_probability` | 210,965 | 19.22% |
| `multi_outcome_out_of_scope` | 405,225 | 36.93% |
| `press_with_no_declared_menu` | 0 | 0.00% |
| `press_key_not_on_menu` | 0 | 0.00% |

What is usable is **95,748 first-choice description trials over 5,674 strictly
two-outcome problems from 13,735 participants**, which is 40 times the 2,380
aggregate rows the v3 fit used and still the largest individual-level interior
sample available.

**A correction the record is owed.** Both CPC18 and choices13k contain
multi-branch lotteries, 122 of 270 games and 1,095 of 2,380 rows, and the fits
that produced `+0.4438` and `−0.1216` read only the `(H, p, L)` columns for all
of them. That approximation is shared across both corpora, so it does not explain
their disagreement, but it is a limit on what either number measures and it was
not previously written down.
