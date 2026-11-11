# Deal or No Deal: development record

**Status: development only. Nothing here is a registered result.** The data are the development set
fixed in `../DESIGN.md`, Section 6: Post, van den Assem, Baltussen and Thaler 2008, DataverseNL
doi:10.34894/TXJK6K, CC BY 4.0. The Australian set and the laboratory set are held out and have not
been downloaded.

## The file

`20060455_Data.xls`, md5 `82ff53d01092bcf806bb9014011278fd`, with its user guide
(md5 `ed24f8b66f4052076288d4110d99b09a`). Copy on Atlas at `/archive/experiments/paths/dond/dev`.
Eight sheets, one row per contestant and round.

| Sheet | What | Contestants | Rows |
|---|---|---|---|
| NL1a, NL1b | Dutch television | 47, 4 | 242, 23 |
| GE1, GE2 | German television | 20, 27 | 127, 227 |
| US, USX | United States television | 47, 6 | 355, 52 |
| EXP1, EXP2 | Classroom experiments at about 40 and 400 euros | 40, 40 | 271, 274 |

Counts are from the sheet sizes and the identifier column, read 2026-11-10 before any decision was
read. Each row gives the round, the bank offer, the decision, and a 0 or 1 for each prize on the
board. The file also has each contestant's first name, education, sex and age. The parser drops the
name and writes the states and the decisions to separate files.

## Why this arena, after chess and poker

Chess fixed the state exactly and had no money. Poker had money, but the history was the player's
own doing. Here the history is drawn at random. The cases a contestant opens are unlabelled, so
which prizes leave the board in a round is chance. Money is real and large on the television sheets.

What the arena lacks is size. There are 151 television contestants and each accepts at most one
offer, so there are at most 151 acceptances. **A lag curve as sharp as the chess curve is not
possible here, and a null result would say little.** The pass is run to build the parser, to see how
wide the intervals are, and to decide whether the held-out Australian set (399 contestants) could
carry a registered test at all.

## Pass 1, planned: does the timing of a loss matter beyond the board it leaves?

Written 2026-11-10 before any decision was read.

**Quantities.** For contestant i at round r, E(r) is the mean of the prizes still on the board and
B(r) the bank offer. The step into round r is s(r) = log E(r) − log E(r − 1), with E(0) the mean of
the full board. It is the random event of that round. Using the mean is a choice made by hand, which
the main design avoids for its models. A scalar is needed to place events at lags, and the mean is
the one the literature uses.

**The comparison.** A logistic model of accepting the offer on

- the present state: log B(r) − log E(r), log E(r), the standard deviation of the remaining prizes
  divided by E(r), round indicators and sheet indicators, and
- the path: s(r), s(r − 1), s(r − 2).

With log E(r) in the model, the coefficient on s(r) asks whether two contestants facing the same
board value decide differently when one of them got there by a recent fall and the other by an
earlier one. Standard errors are clustered by contestant. Television sheets are pooled, and the two
experiments are pooled separately.

**Prediction carried from chess and poker.** The most recent step matters more than the one before
it. The coefficient on s(r) is larger in absolute size than the coefficient on s(r − 1), and the one
on s(r − 2) is not distinguishable from zero. No sign is predicted. Post et al. report that risk
aversion falls after both bad and good luck, which a signed linear term can miss, so the same model
is also run with the absolute steps.

**Limits known before running.**

- The present state is controlled by a model with three summaries, not matched exactly. A path
  coefficient can stand for a part of the state the summaries miss.
- The bank's offer may itself depend on the path. The offer is in the model, so this affects the
  reading of the offer term and not the path terms.
- Few acceptances. Intervals will be wide.

**What each outcome means.** Path coefficients with intervals clear of zero in the predicted order
would agree with the earlier arenas, on development data and through a model. Intervals that
include both zero and effects of practical size mean the set cannot answer the question, and the
Australian set is unlikely to either at under three times the size.

## Result of pass 1 (development)

`parse_post.py` and `analyze_steps.py`, run 2026-11-10 on Atlas. File `results/steps_dev.json`.

**Two things found on the way.**

- The USX sheet repeats a header row before each of its six contestants, each with that
  contestant's own prize board. The first version of the parser used the first board for all six.
  It was caught from the states file before any decision was read, and fixed.
- Nobody accepts an offer in rounds 1 or 2 in either pool. With round indicators those rounds are
  predicted perfectly and the first run did not converge in 8 of 12 fits. Rounds with one outcome
  are now dropped. The coefficients did not change in the second decimal. Every fit therefore uses
  rounds 3 onward: 719 rows, 151 contestants and 132 acceptances on television, and 385 rows, 80
  participants and 71 acceptances in the experiments.

**Television, signed steps, three lags.** Coefficients are in log-odds of accepting per unit of
the variable, with 95% intervals clustered by contestant.

| Term | Coefficient | 95% interval |
|---|---|---|
| Offer relative to the mean remaining prize (log) | +2.05 | +0.77 to +3.32 |
| Mean remaining prize (log) | +0.72 | +0.33 to +1.10 |
| Spread of remaining prizes | +2.67 | +1.73 to +3.61 |
| Step into this round | −0.07 | −0.59 to +0.45 |
| Step one round earlier | −0.06 | −0.68 to +0.55 |
| Step two rounds earlier | +0.26 | −0.31 to +0.83 |

The standard deviation of a step is 0.97, so the interval on the latest step runs from about −0.6
to +0.4 log-odds for a typical step.

**The other fits.** With absolute steps on television the three path coefficients are −0.08, +0.04
and −0.36, each with an interval that includes zero. In the experiments the signed coefficients are
−0.73, −0.32 and +0.14 and the absolute ones +0.94, +0.43 and −0.13. Those fall in the order the
prediction gave, largest for the latest step, and every interval includes zero.

**Reading, by the rule written before the run.** The state terms behave as expected, which checks
the parser. A more generous offer, a richer board and a wider spread each raise acceptance. The
path terms are not distinguishable from zero and their intervals also include effects of the same order
as the effect of the board's value. **This set cannot answer the question of how far back the
path reaches.** It neither supports nor contradicts the chess and poker curves.

**What follows for the held-out sets.** The Australian set has 399 contestants. At 2.6 times the
contestants the intervals would be about 0.6 as wide, still roughly ±0.3 on the latest step. A
registered lag test there would be unlikely to resolve an effect of the size seen here, so none is
drafted. What the main design planned for this game was a comparison of fitted models against the
path-dependent prospect theory of Post et al., and that remains open and is a different question.
The Australian and laboratory sets stay unread.

**Not done.** Post et al. report path dependence in these data with a structural model. This pass
did not fit their model and does not test their result.
