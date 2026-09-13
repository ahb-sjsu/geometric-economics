# prereg-d4stability-v1 — Is the Interior Chirality Stable Inside One Corpus?

**Status:** v1, FROZEN 2026-09-13. Section 13 steps 1 to 3 executed. The signed
tag is step 4 and OSF registration is the owner's step, its GUID recorded in
`prereg-d4stability-v1.sha256` and not here so this file's hash stays fixed. **No
fit has been run on `rows_outcome.npz`.**

**One statistic was replaced before freezing and the reason is on the record.**
The first version tested the plain standard deviation of the four fold estimates.
Its size came out at 0.110 against a nominal 0.05, because folds split by scale
are of unequal precision where random folds are not. It was rewritten to Cochran's
Q, whose size is 0.025. Section 6 gives the argument, Section 10 both numbers, and
Section 14 item 8 the lesson. The mis-sized run is kept as
`power/power_UNWEIGHTED_VOID.log`.

**Author:** Andrew H. Bond, San José State University.

**Relation to the lineage.** `prereg-d4interior-v3` found that the CPC18 interior
chirality of `+0.4438` does not replicate on choices13k, coming out at `−0.1216`,
a sign reversal at a power of 1.000. That leaves two readings and the record
cannot choose between them. Either the chirality is a real quantity and one of
those corpora is unrepresentative, or it is not a stable quantity at all and
moves with whatever stimuli happen to be in hand. This registration asks the
second question of a single corpus, where no between-corpus difference can be
blamed.

A search for a third corpus was run first and closed. `DATASET-INVENTORY.md`
records it. Nothing public covers the interior better than choices13k, which has
already been used, so more of the same data will not settle this.

> **What has been done before this draft.** The peterson2021using transcripts
> were parsed and audited five times, and the corpus structure in Sections 2 to 5
> comes from those audits. The choice column was counted and its overall marginal
> reported. It has not been joined to any covariate and no model has been fitted
> to it. The generative coefficients used in Section 10 are read at run time from
> `results_v3.json`, which is on record.

---

## 1. The question

Does the interior chirality `c2` hold still inside one corpus?

Split a single corpus into folds along a stimulus property declared in advance,
fit `c2` separately in each fold, and measure how far the estimates spread. If
they spread as far as `+0.4438` and `−0.1216` are apart, then the disagreement
between CPC18 and choices13k is what this quantity does routinely, and it needs
no explanation beyond stimulus composition. If instead `c2` holds still, the
between-corpus disagreement is a real difference between those two corpora and
has to be explained.

**The second outcome is the expensive one and this registration is built to be
able to deliver it.** It would mean the question cannot be closed with data in
hand and that the designed grid in `experiments/papers/d4design/` has to be run
as a study.

## 2. Corpus, and the audit that defined it

`peterson2021using/exp1.csv` from Psych-101, 13,735 participants, 1,097,375
recorded key presses. It is choices13k at the level of the individual choice
rather than a rate over a median of sixteen subjects.

**Three parsers were written before one was correct, and the corpus is what the
third one says it is.** The first yielded a trial only when exactly two option
declarations were pending. It captured the first press on each problem and
discarded the four that followed, losing 91 percent of the corpus without a
word. The second replaced silence with accounting, and the accounting
immediately indicted it, putting 45.8 percent of presses in a bucket named "no
declared menu". Reading the line templates showed why. Many options are lotteries
of three to ten branches written as a comma list, which a two-branch pattern
cannot see.

`peterson_parse.py` is the third. **Its rule is that every press token lands in a
named bucket and the buckets sum to the corpus total**, which `census` asserts.
The counts:

| bucket | presses | share |
|---|---|---|
| `first_press_description` | 96,237 | 8.77% |
| `repeat_press_experience` | 384,948 | 35.08% |
| `ambiguous_unknown_probability` | 210,965 | 19.22% |
| `multi_outcome_out_of_scope` | 405,225 | 36.93% |
| `press_with_no_declared_menu` | **0** | 0.00% |
| `press_key_not_on_menu` | **0** | 0.00% |

No bucket is a shrug and nothing is unexplained.

## 3. Coordinate, inherited rather than restated

`stability_rows.py` imports `_opt_coords` from `d4_rotation` and asserts at
import that a pure-gain certain option returns `d = +1`. `prereg-d4gate-v1` was
voided because its analysis code reimplemented that function and got both its
form and its sign convention wrong.

This is also why multi-branch lotteries are excluded rather than approximated.
`_opt_coords` is a two-outcome function of `(H, p, L)`. Extending it to a
ten-branch lottery would mean writing a new coordinate and calling it the old
one, which is the same error in a more respectable coat.

**A note the record is owed.** Both CPC18 and choices13k contain multi-branch
lotteries, 122 of 270 games and 1,095 of 2,380 rows respectively, and the fits
that produced `+0.4438` and `−0.1216` read only the `(H, p, L)` columns for all
of them. This corpus is restricted to strictly two-outcome problems and is
cleaner in that respect. It also means its `c2` is not numerically the same
estimand as theirs. The stability question is internal to this corpus and does
not depend on that comparison, but Section 9's second prediction does, and
Section 12 says what that costs.

## 4. Inclusion, declared here and not later

Only `first_press_description` is kept. A problem is declared once and chosen
from five times, with outcome feedback reported inline after each press, so only
the first choice on a problem is a decision from description. Presses two onward
follow feedback on that same problem and are decisions from experience, which is
a different phenomenon.

Two mechanical exclusions follow. Rows whose two options have equal standard
deviation are dropped, 489 of them, because `dSD` is zero and the row carries no
information about kappa at all. Rows whose riskier option has both outcomes zero
are dropped, 0 of them here, because the scale used by the split axis would be
undefined.

What remains is **95,748 first-choice trials over 5,674 distinct problems from
13,735 participants**. The marginal rate at which the riskier option was taken
is 0.4893, measured over the 96,237 first-press trials before the two mechanical
exclusions. That single number is reported because a corpus whose overall risk
rate is absurd is a corpus that has been misparsed. It was never joined to a
covariate.

## 5. The split axis

Quartiles of `log10` of the outcome scale of the riskier option, `max(|H|, |L|)`,
computed over distinct problems so the folds are balanced in problems rather than
in trials. The cuts are `1.380211241711606`, `1.5797835966168101` and
`1.7708520116421442`, giving folds of 1,394, 1,392, 1,441 and 1,447 problems and
23,003, 23,608, 24,197 and 24,940 trials.

**Scale was chosen because the coordinate cannot see it.** Multiplying both
outcomes of a gamble by any positive constant leaves `(d, q)` exactly unchanged,
since `d` is a ratio of probability-weighted parts and `q` is a probability.
`stability_rows.parse_corpus` checks this on every kept row at two scale
factors, 191,496 checks in all, and refuses to build the corpus if one ever
fails. The axis is verified in the sealed code rather than argued for here. So scale carries no direct
information about the coordinate, and movement of `c2` across these folds is
movement the model's own coordinate does not represent.

**What the folds do not have is equal composition, and that is stated rather
than buried.** Interior trials rise across the folds through 9,952, 11,358, 14,695 and 15,372,
the count at `d < 0` falls through 7,520, 5,628, 4,464 and 4,636, and the spread
of `d·q` falls through 0.572, 0.523, 0.416 and 0.417. Scale is not independent of what the stimuli look like in the
coordinate. This makes the split a real test of composition sensitivity and a
weaker test of the pure invariance argument, and Section 11 says what may and may
not be concluded from it.

## 6. The statistic and its null

**A raw spread on its own means nothing.** Every fold is a quarter of the corpus
and so noisier than the whole, and any split whatsoever produces some spread. The
statistic is therefore compared against random partitions of the 5,674 problems
into four folds of exactly the observed sizes, refitting every fold every time.
The permutation p-value counts the observed value among the null, so it can never
be zero.

**The statistic is studentised, and a first version of this registration was
wrong not to be.** That version tested the plain standard deviation of the four
fold estimates. Its power simulation put the size of the test at **0.110 against
a nominal 0.05**, and the cause is structural. The scale folds differ in
composition, so they differ in how precisely `c2` can be estimated in them, while
a random fold always has average composition and so average precision. Under a
perfectly constant `c2` the real split therefore spreads further than the null
does, and a test on the raw spread rejects more than twice as often as it should.

Dividing each fold's deviation by its own standard error removes exactly that
asymmetry. The statistic is Cochran's Q,

    Q = sum_f (c2_f - c2_bar)^2 / se_f^2

with `c2_bar` the precision-weighted mean and `se_f` taken from the inverse
Hessian at the fold optimum, which is the observed information for this model.

The permutation null is kept rather than leaning on the chi-square form Q takes
asymptotically. Trials are clustered inside problems, about seventeen to a
problem, and the logistic standard errors understate that. Clustering inflates Q
for the observed split and for every permutation alike, because problems are
assigned to folds whole, so the permutation p-value stays calibrated while the
studentisation does the separate job of removing the precision differences.

The plain spread and the range are still computed and reported, because they are
in the units of the chirality and so are readable. Only Q is tested.

## 7. Why each fold is standardised on its own columns

In the linear predictor `b0·dEV + kappa(d,q)·dSD`, multiplying `dSD` by a
positive constant divides every kappa coefficient by that same constant. The
kappa coefficients are identified only up to the scale of `dSD`. The mean
absolute `dSD` runs 5.06, 10.43, 18.72 and 27.78 across these four folds, a
factor of five and a half, so comparing raw fold coefficients would be comparing
units and not chiralities.

Standardising `dEV` and `dSD` inside each fold fixes that scale at unity
everywhere. **This is exactly how CPC18 and choices13k were each treated**, each
standardised on its own columns before their chiralities were compared, so a fold
here is handled the way a corpus was handled there and the two comparisons are of
the same kind. The same standardisation is applied inside the null, so the
comparison is exact. `fit_fold` performs it internally, where no caller can skip
it.

## 8. The estimand

`c2`, the coefficient on `d·q`, fitted by the convex Newton solver of
`kappa_mle.py` separately within each fold, and the heterogeneity of the four
measured by Cochran's Q.

**The fitting path was checked against a known answer before it was trusted.**
Handed the choices13k rows that `prereg-d4interior-v3` ran on, `fit_fold`
returns `−0.121583489680128` against the published `−0.121583489686356`, a
difference of `6.2e-12`, at a gradient infinity norm of `1.5e-12`. That
exercises the standardisation, the design construction and the coefficient
index in one go. The v3 record credits this kind of check with catching the
optimizer failure that voided v2, and it is cheap enough that there is no reason
to skip it.

## 9. Predictions

Bars live in `analysis/d4stab_grade_v1.py` and nowhere else.

- **W1, composition sensitivity.** Permutation `p < 0.05` on Cochran's Q. `c2`
  moves with stimulus scale by more than resampling of the same fold sizes
  explains.
- **W2, sufficiency.** The observed range across the four folds is at least
  `0.5653585378279767`, the CPC18 estimate minus the choices13k estimate. One
  corpus split by composition then moves `c2` by as much as the between-corpus
  disagreement did.
- **W3, sign instability.** The four fold estimates are not all of one sign.

Reported separately. **No composite verdict is registered.**

## 10. Power and size

200 replicates at each true fold spread, each with its own 250-permutation null,
seed 20260913. Generative coefficients read at run time from `results_v3.json`
rather than transcribed. The alternative sets the four fold chiralities to
`−0.1216` plus offsets monotone in scale with the stated sample standard
deviation. **The choices are never read**, the simulation loading only
`rows_covariates.npz`, which has no outcome column.

| true fold sd | W1 | W2 | W3 | mean Q | mean spread | mean range | mean fold `c2` |
|---|---|---|---|---|---|---|---|
| **0.00** | **0.025** | 0.005 | 0.300 | 2.98 | 0.0919 | 0.2063 | −0.1253 |
| 0.10 | 0.315 | 0.040 | 0.640 | 7.56 | 0.1345 | 0.2995 | −0.1139 |
| 0.20 | **0.900** | 0.285 | 0.840 | 19.56 | 0.2182 | 0.4919 | −0.1188 |
| 0.30 | **1.000** | 0.795 | 0.955 | 38.36 | 0.3107 | 0.7116 | −0.1169 |
| 0.40 | 1.000 | 0.995 | 0.995 | 64.81 | 0.4102 | 0.9423 | −0.1161 |

**W1 at a true fold spread of zero is the size of the test, and it is 0.025
against a nominal 0.05.** The test is calibrated and slightly conservative. Mean Q
under the null is 2.98 against the 3 expected of a chi-square on three degrees of
freedom, which is the form Q takes when the standard errors are right, so the
studentisation is behaving as its derivation says it should. The unweighted
statistic this replaced had a size of 0.110 at the same settings.

**The effect size that matters is `0.24`.** A range of `0.5654`, the gap between
CPC18 and choices13k, corresponds under the monotone alternative to a fold spread
of about `0.24`. W1 is already at 0.900 by `0.20` and 1.000 by `0.30`, so it
detects the amount of instability that would explain the between-corpus
disagreement with a probability near 0.95. **A W1 failure is therefore evidence
of stability and not a weak test failing to see something**, which is what makes
F1 reportable.

W1 detects half of that, a spread of `0.10`, only 32 percent of the time. The
test is not sensitive to small heterogeneity and no claim of stability below a
fold spread of about `0.15` should be read into a failure.

**W3 fires 30 percent of the time under a constant `c2`, and that must be stated
beside it whenever it is reported.** The chirality sits near zero at `−0.1216`,
so ordinary noise flips the sign of a fold estimate often. A W3 pass on its own
is close to uninformative and is not a third independent confirmation of
anything. It is retained because sign disagreement is what a reader will look for
first, and it is better to have its false-positive rate registered in advance than
to have the observation made without one.

The estimator is unbiased across the whole range. The mean fold `c2` reads
−0.1253, −0.1139, −0.1188, −0.1169 and −0.1161 against a true −0.1216. **There
was no non-convergence in any of the 1,000 replicates, nor in any of the 250,000
permutation refits behind them.**

## 11. Falsifiers

- **F1, the one that costs us something.** If W1 fails, `c2` is stable against
  outcome scale inside this corpus. The between-corpus disagreement is then a
  real corpus-level difference, it is not explained by stimulus composition on
  this axis, and **the question is not closed**. The designed grid becomes the
  next step and it requires a study to be run. This outcome is to be reported as
  plainly as the cheap one.
- **F2.** W1 passing while W2 fails means composition moves `c2` by less than the
  between-corpus gap. That is a partial explanation and must not be written up as
  closing the question.
- **F3.** A gradient infinity norm above `1e-5` on any fold or on the whole
  corpus voids the run. It is reported as void and not retried.
- **F4, against ourselves.** Scale is one axis. Failing to find instability along
  it is not evidence of stability in general, only of stability along scale, and
  the write-up must say so whichever way W1 goes. Equally, W1 passing shows that
  composition moves `c2` on an axis that correlates with coordinate composition,
  as Section 5 records, so it does not by itself establish that scale is the
  operative variable.

## 12. What this cannot settle

W2 compares a range computed on two-outcome problems against a gap computed on
corpora that included multi-branch lotteries collapsed to three columns. The two
numbers are not measurements of the same estimand and W2 is therefore a
calibration against the size of the disagreement, not a like-for-like test. It is
registered because the size of that gap is the thing needing explanation, and a
range that clears it is informative about scale even when the estimands differ.
W1 and W3 are internal to this corpus and carry no such caveat.

This registration also says nothing about decisions from experience, which is 35
percent of the corpus by press count, and nothing about ambiguity or multi-branch
lotteries, which are a further 56 percent. It is a statement about the
description subset.

## 13. Freezing procedure

1. Write the bars into `analysis/d4stab_grade_v1.py`. Done.
2. Run `power/power_d4stability_v1.py`, which cannot read the choices, and fill
   Section 10.
3. Finalise this document, **then** hash the bundle with `--hash` into
   `prereg-d4stability-v1.sha256`. v1 of the interior lineage hashed before
   finalising and had to recompute.
4. Commit, sign the tag `prereg-d4stability-v1`, push.
5. Only then run `analysis/launch_fit.sh`, which pins the BLAS thread counts
   and calls `analysis/d4stab_fit_v1.py`, the one script in the bundle that
   opens `rows_outcome.npz`.

The thread pins are part of the bundle because they are part of the result. A
first run of the power simulation at twenty workers with BLAS left unpinned took
Atlas CPU package 0 to 100 C, its critical alarm, and had to be shed. Six workers
at one BLAS thread each holds the package near eighty against a baseline of
seventy-four.

**The covariates and the choices are in separate files.** The power simulation
loads `rows_covariates.npz`, which has no outcome column, so it cannot read the
choices even by accident. This is the structural version of a discipline the v3
lineage had to keep by attention.

## 14. Errors in this lineage, all recorded

Carried forward from `prereg-d4interior-v3` Section 11, with the new ones added.

1. **A coordinate reimplemented rather than imported, wrong in form and sign.**
   Fixed by importing and asserting at import.
2. **A power simulation drawing one choice per row** where the target was a rate
   over many subjects. Fixed by drawing at the real counts. Does not arise here,
   where the target is an individual binary choice.
3. **Generative coefficients transcribed, five of six wrong.** Fixed by reading
   them from the record at run time, which this registration also does.
4. **A derivative-free optimizer on a convex problem.** Fixed by Newton and by
   verifying the estimator against a known answer before trusting it.
5. **A convergence threshold that measured itself.** Set to `1e-5`.
6. **New here. A parser that dropped 91 percent of a corpus silently.** Fixed by
   requiring that every press token be counted into a named bucket and that the
   buckets sum to the corpus, asserted in code.
7. **New here. A second parser whose largest bucket was "not understood".** An
   accounting that balances is necessary and not sufficient. Fixed by reading the
   line templates until every bucket had a reason, which took the unexplained
   share from 45.8 percent to zero.
8. **New here. A test statistic whose size was 0.110 against a nominal 0.05.**
   The first version of this registration tested the plain standard deviation of
   the four fold estimates. Folds split by scale are of unequal precision where
   random folds are not, so the real split outspread its own null under a
   constant `c2`. Caught by simulating the null world before sealing, which is
   the only reason it was caught at all. Fixed by studentising, and the mis-sized
   run is kept as `power/power_UNWEIGHTED_VOID.log` rather than deleted.

The generalisation the v3 record drew still holds and is strengthened. Every one
of these was caught by machinery rather than by care. Errors 6 and 7 were caught
by an audit that counted what it was throwing away, and the first parser, which
threw the same material away without counting it, would have produced a
publishable number. Error 8 was caught by the requirement that a registration
state its own size before it is sealed. A spread statistic against a permutation
null is the obvious thing to do here and it is wrong, and nothing but simulating
the null world would have said so.
