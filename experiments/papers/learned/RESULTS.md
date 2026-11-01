# prereg-learned-v1. Run record

**Run 2026-10-30 on Atlas, GPU 1**, LaBSE snapshot `836121a0533e5664b21c7aacc5d22951f2b8b25b` (matches
the registration, so V1 does not apply). The seal was verified intact after the run. The registration
commit `6d64fc1` and signed tag `prereg-learned-v1` were on public `main` before the fit started.
Outputs as executed: `results/results_labse.json`, `results/grade_labse.json`, and the selected metric
and reference in `results/gdt_labse.npz`. No fit was void.

Data after dropping dev and test pairs that share an action with train: train 63,586, dev 2,274 (66
dropped), test 2,266 (94 dropped).

## Verdicts

Two of five pass. Each stands alone.

| | Prediction | Verdict | Numbers |
|---|---|---|---|
| H1 | Learned coordinates beat the codebook coordinates | **PASS** | GDT minus ANCHOR −0.0465 nats per annotation, 95% interval [−0.0536, −0.0393], margin 0.0005 |
| H2 | A learned metric beats a learned linear scalar | **PASS** | GDT minus LIN −0.0129, interval [−0.0177, −0.0082] |
| H3 | The learned metric is low rank, `k* ≤ 8` | **FAIL** | `k* = 32`, the top of the grid. Dev log-loss still falls at 32 |
| H4 | The learned span contains the codebook axes beyond chance | **FAIL** | 0.038 against a null 99th percentile of 0.068. The null MEAN is 0.060, so the codebook axes sit inside the learned span LESS than a random subspace does |
| H5 | Zero-fit sign transfer to the projection-gap panel | **FAIL** | 1 of 5 correct (B1.1). A1.1, A1.2, A2.1 and A3.1 came out with the opposite sign |

Test log-loss per annotation: constant 0.6927, codebook axes 0.6875, linear scalar 0.6539, learned
metric 0.6410. All models explain little of these judgments. The learned metric removes 7.5% of the
constant model's loss.

## The reading

**The geometric form helps.** A cost measured as distance from a learned reference beats a linear
scalar on the same features, held out, by about 27 times the registered margin. For these moral
judgments, a distance-from-reference cost describes the data better than one learned direction does.

**The low-rank claim fails here.** The selected rank is the largest tried and the dev curve had not
flattened, so these judgments use at least 32 directions of the encoder space. The rehearsal showed
the rank rule overstates rank by about one grid step, which does not rescue a selection at the top
of the grid.

**The nine coordinates are not where the structure is.** The codebook axes, written as text and given
learned weights, barely beat a constant model (0.6875 against 0.6927). Their overlap with the learned
span is below what random subspaces of the same dimension achieve. On these data, Part I's coordinate
system does not describe the structure the judgments follow. Each axis has between 10% and 17% of its
length inside the learned span (d3 fairness the highest at 0.169).

**The learned metric does not transfer to the panel.** It predicts the wrong sign for four of the five
contrasts. The two tasks differ (short descriptions of actions judged for ethics, against long
scenarios followed by a choice), and H5 was registered as weak. A result below chance is still a
failure, and it is reported as one.

## What this does not settle

H2 compares the learned metric with a linear scalar. It does not compare it with other nonlinear
models of the same capacity, such as a low-rank quadratic utility without a reference point. A win
over LIN shows that curvature helps. It does not show that distance from a reference is the right
curvature. That comparison was not registered and would be exploratory.

The outcome is a judgment of which action is less ethical, not a choice with consequences. None of
these results bears on monetary choice.

## BGE-M3 replication (registered as reported, not graded)

Same splits, same code, `BAAI/bge-m3` snapshot `5617a9f61b028005a4858fdac845db406aefb181`, 1024
dimensions. All selected fits converged. Outputs: `results/results_bgem3.json`, `results/gdt_bgem3.npz`.

| | LaBSE (graded) | BGE-M3 (not graded) |
|---|---|---|
| Learned metric minus codebook axes | −0.0465 [−0.0536, −0.0393] | −0.0589 [−0.0658, −0.0516] |
| Learned metric minus linear scalar | −0.0129 [−0.0177, −0.0082] | −0.0079 [−0.0123, −0.0037] |
| Selected rank `k*` | 32 | 32 |
| Codebook alignment (null 99th pct, null mean) | 0.038 (0.068, 0.060) | 0.031 (0.048, 0.042) |
| Panel targets with the predicted sign | 1 of 5 | 4 of 5 (A1.2 wrong) |

Test log-loss for BGE-M3: constant 0.6927, codebook axes 0.6785, linear scalar 0.6275, learned metric
0.6196.

The first four rows replicate in a second encoder: the metric beats both the codebook axes and the
linear scalar, the rank sits at the top of the grid, and the codebook axes overlap the learned span
less than random subspaces do. The panel transfer does not replicate the LaBSE failure. BGE-M3 gets
4 of 5 signs, which would meet the registered bar. It does not count as support. It is ungraded by
registration, the two encoders disagree on three of the five signs, and the BGE-M3 prediction for the
wording-only placebo P.A1 (+0.035) is as large as its predictions for the real contrasts (+0.015 to
+0.039). A transfer that moves a placebo as much as the real manipulations is not reading the
manipulated coordinate.
