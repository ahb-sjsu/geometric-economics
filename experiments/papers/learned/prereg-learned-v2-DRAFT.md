# prereg-learned-v2. Do the learned metric and its leading direction carry to rated behaviours from other sources?

**Status: DRAFT, 2026-11-09. Not sealed, not rehearsed, no code written, no rating file opened.**
Drafted by Claude at the owner's request ("go with your recommendation": harden the two passes of
`prereg-learned-v1` with new sealed tests). Every design choice below is Claude's and is open to the
owner. Sealing needs the owner's explicit OK after the rehearsal of Section 8.

**Companion to.** `prereg-learned-v1` (run 2026-10-30, `RESULTS.md`) and its exploration record
(`explore/DEVELOPMENT.md`).

## 1. What v1 left open, and what a new test can and cannot settle

`prereg-learned-v1` passed two predictions on Scruples Dilemmas. Learned coordinates beat the nine
codebook coordinates (H1), and a distance from a learned reference beat a linear scalar (H2). Three
things limit those passes.

1. **One corpus.** Both passes are on Scruples, whose actions come from one Reddit forum.
2. **No model of equal capacity.** H2's comparison was a linear scalar. The exploration then compared
   the distance with a squared distance (SQD) and with a low-rank quadratic of free sign and no
   reference (QUAD). It did so on the Scruples test split, which is therefore spent for this question.
   There the distance tied the squared distance and beat the free-sign quadratic by 0.023 nats (LaBSE)
   and 0.027 (BGE-M3).
3. **One direction carries most of the metric,** and its meaning is a hypothesis. The exploration
   found direction 0 stable (0.93) and read it as harm to people the actor is close to. That reading
   was formed and tested on the same 27,982 Scruples actions.

A confirmatory test needs judgments that were not used above. A search on 2026-11-09 (Section 2)
found **no independent public corpus of pairwise judgments** of the Scruples kind. Every pairwise
candidate is built from Scruples, written by a language model, or not text. What exists is a set of
small norming studies in which many raters score single behaviours. This fixes the design.

- The test is a **transfer with nothing refit**. Models are fit on Scruples, frozen, and scored on how
  well each item's frozen cost orders the raters' mean judgment.
- **Distance against squared distance cannot be tested here, and this is declared now.** On single
  rated items the score is a rank statistic, and a distance and its square give the same ranks from the
  same metric. The two frozen models differ only in the metrics their fits happened to reach. Whether
  distance is the right curvature needs pairwise choices from a new source, which this search did not
  find. v1's caveat on this point stays open.

## 2. Data

Found by reading papers, repository pages and file listings only. No rating file has been opened.
Items marked UNVERIFIED must be checked, from listings and documentation only, before sealing.

| Set | Items | Raters per item | Judgment used | Source of texts | To verify before sealing |
|---|---|---|---|---|---|
| **MICK.** Mickelberg et al. 2022, PLOS ONE 17(6) e0269393, OSF `qnv95` | 160 one-sentence behaviours | 100 | morality, −4 to +4 | written by the authors or adapted from earlier studies | whether `SGdata.csv` is rater-level; licence (none set on the OSF node) |
| **KRUE.** Kruepke et al. 2018, Behav. Res. Methods 50:922–936, OSF `26tyy` | 117 first-person vignettes | about 216 to 225 | moral appropriateness; harm to others (used in H4) | condensed from autobiographical memories (Knutson et al. 2010) | file contents and format; licence |
| **MFV.** Clifford et al. 2015, Behav. Res. Methods 47:1178–1198 | 132 one-sentence scenarios | about 30 | wrongness, 5 points | written by the authors | a machine-readable table of item means; rater-level data |
| KNUT (reserve). Knutson et al. 2010, SCAN 5(4):378–384 | 312 vignettes, a superset of KRUE | 30 | moral appropriateness and 12 other scales | as KRUE | whether the supplement with item ratings is obtainable |

**Not used.** Scruples Anecdotes, Commonsense Norm Bank, the long ETHICS commonsense items, UniMoral
and the Reddit r/AmItheAsshole part of Social Chemistry 101 share Scruples' source. MoralChoice,
DailyDilemmas and NormBank are written by language models. Moral Stories and ETHICS release one binary
label per item. The other three domains of Social Chemistry 101 are independent and large, but about
99% of rows have one rater. Their five-rater subset is reported without a bar if it exceeds 1,000
situations (size UNVERIFIED).

**Primary sets are MICK, KRUE and MFV**, 409 items. If KNUT is obtainable it replaces KRUE as the
vignette set (312 items, 30 raters), and KRUE's harm ratings are still used for H4 on its 117 items.
That choice is made from availability alone, before sealing.

**What may be read before sealing.** Item texts, because the encoder needs them. Column names and row
counts. No rating, and no statistic of any rating. The parser writes texts and ratings to separate
files, as in `prereg-psych101-v1`.

**Overlap.** Any item whose text matches a Scruples action after lower-casing and stripping
punctuation is dropped. Counts are reported.

## 3. Frozen models

All are fit on Scruples train and train-extra and selected on Scruples dev with `fit_learned.py` and
`explore/explore_learned.py` as they stand, LaBSE at the v1 snapshot. No new item is seen in fitting.

- **GDT.** The registered v1 metric, `results/gdt_labse.npz`, unchanged.
- **LIN**, **SQD**, **QUAD**, **ANCHOR.** Refit with the v1 and exploration code and seeds, because
  only GDT's parameters were saved. Their Scruples test log-loss must reproduce the recorded values
  (0.6549, 0.6433, 0.6638 and 0.6875) to four decimals. If one does not, that is reported and the
  refit is used.
- **D0.** The first right singular vector of GDT's metric, as a direction. **GDT−0** is GDT with that
  direction projected out of the metric.
- **XBSE.** The nine graded moral axes of moral-spectrum-analyzer, as scored in the exploration,
  combined by weights fit on Scruples train.

Each frozen model gives one number per item, its cost. For LIN the number is `w·e`. Higher reads as
less ethical in every model, as fit.

A BGE-M3 copy of every model is scored and reported, not graded, as in v1.

## 4. Score

For a model and a set, the score is Spearman's correlation between the model's cost and the raters'
mean judgment, signed so that a positive score means higher cost for behaviours rated worse. The pooled
score is the mean over the three sets, each weighted equally. Intervals are 95% percentile intervals
from 2,000 bootstrap resamples of items within each set. A comparison of two models is the paired
bootstrap difference of their pooled scores.

**Margin.** A difference counts only if its interval lies beyond a margin `m`. `m` is set in the
rehearsal as the 95th percentile of the absolute pooled difference between two refits of the same GDT
from different seeds, so that seed noise cannot pass a test.

MFV contains only violations and MICK spans praise to blame. A model can order praise against blame and
still fail to order one violation against another. Scores are therefore also reported within MICK's
negative-moral items alone.

## 5. Predictions (bars to live in `grade_learned_v2.py`)

Each stands alone. No composite verdict.

- **H1. The learned metric carries to other sources.** GDT's pooled score has an interval above 0.20,
  and its score is positive on each of the three sets. The bar of 0.20 is provisional. The rehearsal
  replaces it with the score a model of GDT's Scruples accuracy would reach under Section 8's
  simulation, halved.
- **H2. Learned coordinates beat the nine codebook coordinates out of corpus.** GDT minus ANCHOR,
  pooled, beyond `m`. This is v1's H1 by transfer.
- **H3. A reference point beats free-sign curvature of the same rank.** GDT minus QUAD, pooled, beyond
  `m`. This is the comparison at equal capacity that v1 lacked, confirmed on data the exploration did
  not touch. QUAD has more parameters than GDT at the same rank, so a GDT win is not a win of capacity.
- **H4. Direction 0 tracks closeness beyond harm.** On KRUE, each vignette is rated blind for how close
  the affected party is to the actor (Section 6). In a regression of D0's score on KRUE's rated harm to
  others and on closeness, closeness adds at least 0.02 to R², with a bootstrap interval excluding
  zero. The exploration's value on Scruples was 0.087 with severity rated by language models. Here harm
  is rated by about 220 people per vignette, which removes the weakest part of that analysis.
- **H5. Direction 0 carries the transfer.** GDT minus GDT−0, pooled, beyond `m`, and larger than the
  same difference for at least 95 of 100 random directions drawn from the metric's row space and
  scaled to direction 0's singular value.

**Declared not assessable.** Distance against squared distance (Section 1). GDT minus SQD is reported
without a bar.

**Reported without a bar.** GDT minus LIN. On Scruples the distance beat the linear scalar by 0.013
nats, a small edge that 409 items are unlikely to resolve. The rehearsal reports its power. If that
power is at least 0.8 the comparison is promoted to a prediction before sealing, and not after.

## 6. Closeness ratings for H4

As in the exploration's Hohfeld test. Two language models (gemma and qwen3-small on the NRP gateway)
rate each KRUE vignette for the closeness of the affected party to the actor, on the scale and wording
of `explore/hohfeld_rate.py`, with thinking off and without seeing any model score or human rating.
The two ratings are averaged. Their Spearman agreement is reported. If it is below 0.6, H4 is void.
Human closeness ratings would be better and are not available.

## 7. Void conditions

- **V1.** The LaBSE snapshot differs from v1's.
- **V2.** After exclusions a primary set has fewer than 80 items. That set is dropped and the pooled
  score is over the others. With fewer than two sets the study is void.
- **V3.** H4 only: closeness rater agreement below 0.6.

## 8. Rehearsal and the decision to seal

To be run on Atlas before sealing, on the real item texts with ratings never loaded.

1. Simulate item means from known truths on the real embeddings: the frozen GDT with rater noise
   matched to each set's rater count, the frozen LIN, the frozen QUAD, and a truth with no relation to
   any model. Rater noise per item is a free input swept over a stated range, because the real spread
   is unknown until the ratings are opened.
2. Check that H1 to H3 and H5 fail under the truths that should fail them. The no-relation truth must
   pass nothing in 200 simulated studies. Under the LIN truth H3 must not pass in more than 5%.
3. Report the power of each prediction under the GDT truth.
4. Set `m` and H1's bar as described above.

**Rule written now.** The study is sealed only if H2 and H3 each have power of at least 0.8 under the
GDT truth at the middle of the noise range. If they do not, 409 items cannot decide the question, the
draft is not sealed, and the options are the reserve set KNUT, the Social Chemistry subset, or new
pairwise judgments collected for the purpose.

## 9. Not claimed

A pass says the metric learned from one forum's dilemmas orders behaviours from laboratory norming
studies as their raters do. It says nothing about choices with consequences, and nothing about
monetary choice. v1's failures stand: the metric is not low rank (H3), the codebook axes are not
inside its span (H4), and it did not transfer to the Part II panel (H5). Nothing here retests them.
The encoder may have seen these published stimuli in training. That does not leak the ratings.

## 10. To build before sealing

`fetch_norms.py` (texts and ratings to separate files, bucket accounting), `freeze_v2.py` (refits and
the reproduction check of Section 3), `score_v2.py`, `grade_learned_v2.py`, `rehearse_v2.py`,
`seal_learned_v2.py`. Then the data checks marked UNVERIFIED, the rehearsal, a prior-art check on
transfer of learned moral metrics to norming sets, and the owner's OK on the exact bundle.
