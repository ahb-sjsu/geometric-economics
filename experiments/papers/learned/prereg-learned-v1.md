# prereg-learned-v1. Learned coordinates for the geometric decision model

**Author.** Andrew H. Bond, San José State University.
**Companion to.** Geometric Prediction of Economic Behavior I (IEEE TCSS, doi 10.1109/TCSS.2026.3734068)
and II (in preparation). Part III of the series.
**Freezing.** Section 9. Nothing here is a registered claim until the bundle is hashed, committed, tagged
with a signed tag, and the tag is pushed to the public repository. The July 2026 registrations of this
programme were committed locally and published only after their data runs, so their ordering rests on
commit timestamps. This one is public before any real label is scored.

## 1. Question

Parts I and II place each option on nine hand-specified coordinates. The coordinates, and how a scenario
is scored on them, are the researcher's choices. That is the main criticism of the programme. This study
replaces them with directions in a sentence encoder's embedding space, learned from human judgments, and
asks four things. Do learned directions predict held-out judgments better than the nine coordinates
written as text? Is a distance-from-reference cost better than a linear scalar on the same learned
features? How many directions are needed? Do the learned directions contain the hand-specified ones?
A fifth question tests the learned metric, with nothing refit, on the projection-gap contrasts of Part II.

## 2. Data

Scruples Dilemmas (Lourie, Le Bras and Choi, AAAI 2021), version 1.0, from
`storage.googleapis.com/ai2-mosaic-public/projects/scruples/v1.0/data/dilemmas.tar.gz`. Each item is a
pair of real actions, described in a short English phrase, and five crowd annotations of which action is
less ethical. The outcome is the count of annotators choosing action 0. Official splits are used as
released. Fitting uses train and train-extra (63,586 pairs). Model selection uses dev (2,340). The test
split (2,360) is scored once.

**Held out means unseen actions.** 33 dev actions and 41 test actions also occur in train. Every dev or
test pair containing a train action is dropped before anything is fit. Counts are reported.

Nothing about the annotation counts was read before freezing beyond the file format and the split sizes.
The rehearsal (Section 8) loads the real counts and overwrites them with simulated ones before any
computation, and computes nothing from them.
The action texts were read, because the encoder needs them. The overlap counts above use texts only.

## 3. Encoders

Primary and graded: `sentence-transformers/LaBSE`, 768 dimensions, Hugging Face snapshot
`836121a0533e5664b21c7aacc5d22951f2b8b25b`. Replication, reported and not graded: `BAAI/bge-m3`, dense
1024 dimensions, snapshot `5617a9f61b028005a4858fdac845db406aefb181`. Embeddings are unit-normalised.
Embedding uses no labels and was run before freezing to fix the snapshots.

## 4. Models

All predict `p`, the probability an annotator marks action 0 as less ethical, scored by binomial log-loss
per annotation in nats.

- **M0.** Constant. Position bias only.
- **LIN.** `logit p = b + w·(e0 − e1)`. A scalar utility linear in the encoder's coordinates. This is the
  scalar incumbent on the same learned features.
- **GDT_k.** `logit p = b + C(e0) − C(e1)` with `C(e) = sqrt(|U(e − r)|² + 1e-6)`, `U` of rank `k`, `r` a
  learned reference. Higher cost reads as less ethical. The temperature is absorbed into `U`, because only
  the metric divided by the squared temperature is identified. `k ∈ {1, 2, 4, 8, 16, 32}`.
- **ANCHOR.** GDT with `U = M A`. `A` holds the ten codebook axes of `tcss-part2/codebook-v1.md`
  (d1 to d9, d5 split into trust and privacy), each the embedding of the anchor-1 sentence minus the
  anchor-0 sentence, unit-normalised. `M` is a free 10 × 10 matrix. This is Part I's coordinate system as
  text, with its weights learned on the same data as every other model.

Training is full-batch Adam, learning rate 0.01, 3,000 steps, then full-batch L-BFGS (strong Wolfe line search) for up to 40 outer steps of 50 iterations, ridge penalty `λ ∈ {0, 1e-6, 1e-5, 1e-4, 1e-3}` on
`w` or on the metric, three random restarts for GDT and ANCHOR. For GDT below the largest rank, a further start is the rank-`k` truncation (top `k` singular directions) of the rank-32 fit at the same penalty. The start with the lowest training loss is kept. All
constants are in `fit_learned.py`.

## 5. Selection (dev only)

**The margin.** GDT contains LIN as the limit of a reference placed far away, so GDT can always come
arbitrarily close to LIN, and a tiny but consistent difference would exclude zero without meaning
anything. The rehearsal showed exactly this (Section 8). Every comparison therefore has to clear a
margin `m`, equal to 1% of LIN's dev improvement in log-loss over M0. `m` is computed from dev before
the test split is scored.

For each family the `(k, λ)` with the lowest dev log-loss is selected. For GDT, `k*` is the smallest `k`
whose dev log-loss exceeds the best GDT's by no more than the larger of `m` and one paired-bootstrap
standard error of that difference. The selected GDT is GDT at `k*`.

## 6. Predictions (bars live in `grade_learned.py`)

All test comparisons are paired bootstrap differences in log-loss per annotation over test dilemmas,
2,000 resamples, 95% percentile interval. "Beats" means the interval lies entirely below `−m`.

- **H1. Learned coordinates beat the codebook coordinates.** GDT at `k*` beats ANCHOR on test.
- **H2. A learned metric beats a learned linear scalar.** GDT at `k*` beats LIN on test.
- **H3. The learned metric is low rank.** `k* ≤ 8`.
- **H4. The learned directions contain the codebook directions beyond chance.** The mean squared cosine
  of the principal angles between the row space of the selected `U` and the span of the ten codebook
  axes exceeds the 99th percentile of the same statistic for 1,000 random subspaces of the same
  dimension drawn from a Gaussian with the training embeddings' covariance.
- **H5. Zero-fit sign transfer to the projection-gap panel.** The selected GDT, fitted only on Scruples,
  predicts the sign of `P(A | hi) − P(A | lo)` for each panel contrast as the sign of
  `(C_B − C_A)_hi − (C_B − C_A)_lo`, each option text being the pole's scenario followed by "I choose:"
  and the option's clause (`inputs.json`, built by `build_inputs.py`). Targets are the five contrasts
  whose placebo-corrected effect was significant in Part II, all observed positive: A1.1, A1.2, A2.1,
  A3.1, B1.1. The bar is at least 4 of 5 correct. Under chance, 4 or more of 5 occurs with probability
  0.19, so H5 is a weak test and is stated as one. The other two real contrasts and both placebos are
  reported without a bar.

Each prediction stands alone. No composite verdict is registered.

## 7. Void conditions

- **V1.** The graded run's LaBSE snapshot differs from Section 3.
- **V2.** A selected GDT, LIN or ANCHOR fit fails the convergence check in `fit_learned.py` (relative
  change in training loss above 1e-5 over the final L-BFGS outer step).

## 8. What is reported regardless

Every grid fit with train and dev log-loss, the margin `m`, the distance of the fitted reference from the mean embedding, the dev curve over `k`, test log-loss of every selected model,
the fraction of each codebook axis inside the learned span, the BGE-M3 replication run in full, the panel
predictions for all nine contrasts under both GDT and LIN, and the saved `U` and `r`. The leading learned
directions outside the codebook span are described by the training actions with the largest and smallest
projections on them. That description is exploratory and is labelled so.

**Rehearsal (run before freezing).** The whole chain was run on the real embeddings with annotation
counts replaced by draws from two known models: a rank-2 GDT and a linear scalar. It had to find the
rank-2 metric (H2 pass, `k*` in {1, 2, 4}) and had to not prefer a metric when the truth was linear
(H2 fail). Results are in `rehearsal/`.

The first rehearsal failed the linear check. With a linear truth, GDT beat LIN by 0.00007 nats per
annotation with an interval excluding zero, because GDT reproduced LIN through a distant reference.
It also picked `k* = 8` on ties at numerical noise, and the best penalty was the smallest in the grid.
Before anything real was scored, the margin of Section 5 was added to H1, H2 and the `k*` rule, and the
penalty grid was extended downward. The rehearsal was then rerun on both truths.

The second rehearsal passed the linear check, but narrowly. Under the linear truth GDT still came out
0.0021 nats better than LIN against a margin of 0.0027, because LIN at zero penalty had not converged
under Adam and GDT, with more parameters, had. A study selected that way would also have been void
under V2. Every fit now ends with a full-batch L-BFGS refinement to convergence, and the convergence
criterion was tightened to match. The rehearsal was run a third time.

The third rehearsal passed the linear check cleanly (GDT minus LIN 0.00003 nats, interval across zero)
and found the rank-2 metric decisively (GDT beat LIN by 0.083 nats), but selected `k* = 32`. The cause
was optimization. The rank-2 fit stopped at training loss 0.317 while the rank-32 fit reached 0.273,
although a rank-2 truth needs no more than rank 2. The cost is not convex and random small starts left
the rank-2 fit in a local optimum. A start from the singular-value truncation of the rank-32 fit was
added for every smaller rank, and the rehearsal was run a fourth time.

The fourth rehearsal passed both checks. Under the linear truth GDT minus LIN was 0.00002 nats with an
interval across zero, H2 failed as it should, and `k* = 1`. Under the rank-2 truth GDT beat LIN by
0.095 nats (interval −0.111 to −0.080, margin 0.0037) and `k* = 4`. The rank rule therefore found the
true structure but overstated its rank by one step of the grid, so a passing H3 bounds the rank from
above and does not measure it. No fit was void in either run. These are the code and constants sealed.

## 9. Not claimed

The outcome is a moral judgment between two described actions, not a choice with consequences for the
annotator. A pass on H1 to H4 says learned coordinates describe these judgments, and says nothing about
monetary choice. H5 is the only bridge to Part II's choices and it is weak by construction. The encoder
was trained by others on data that may include text like Scruples. That does not leak the annotation
counts, which are not text.

## 10. Freezing procedure

1. Write `prereg-learned-v1.sha256` with `seal_learned.py --write` over the bundle in that script.
2. Commit with a signed commit, tag `prereg-learned-v1` with a signed annotated tag, push commit and tag
   to `origin`.
3. Only then run `fit_learned.py` on the real labels and `grade_learned.py` on its output.
