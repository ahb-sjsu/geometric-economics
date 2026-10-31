# prereg-psych101-v1. Run record

**Run 2026-10-30 on Atlas**, after the registration commit `28e4516` and signed tag
`prereg-psych101-v1` were on public `main`. The seal was verified intact before and after the run
(`results/seal_check_*.txt`). No fit was void: every native fit passed the convergence check. Outputs as
executed: `results/results_real.json`, `results/grade_real.json`.

Data: 24,124 choices by 1,959 participants on 991 problems (22 of the 1,981 participants had no kept
row). Calibration half 495 problems and 11,332 choices; test half 496 problems and 12,792 choices.
Payoff unit for this corpus 148.0 points.

## Verdicts

One prediction for the geometric model passes, and it is the weak one. Each stands alone.

| | Prediction | Verdict | Numbers (test log-loss difference per choice, nats) |
|---|---|---|---|
| H1 | Frozen GDT beats expected value refit here | **FAIL** | −0.0053, 95% interval [−0.0124, +0.0015], margin 0.0005 |
| H2 | Frozen GDT beats frozen linear random utility | **FAIL** | −0.0017 [−0.0050, +0.0012] |
| H3 | Frozen CPT beats frozen GDT | **PASS** | CPT minus GDT −0.0174 [−0.0250, −0.0107] |
| H4 | CPC18 angle inside this corpus's 95% interval | **PASS** | 0.105 inside [0.071, 0.314], native estimate 0.188 |
| H5 | GDT's deficit to CPT larger with losses | **FAIL** | difference in differences −0.0006 [−0.0146, +0.0153] |

Test log-loss per choice: constant 0.6984, expected value 0.6514, random utility (frozen) 0.6478, GDT
(frozen) 0.6461, CPT at the 1992 estimates 0.6444, CPT (frozen) 0.6287, CPT refit here 0.6055.

## The reading

**Part II's ordering against CPT replicates out of corpus, by a wider margin.** On CPC18, CPT led GDT by
about 0.006 in mean absolute error. Here frozen CPT leads frozen GDT by 0.017 nats per choice, and CPT
refit on this corpus leads GDT refit on it by 0.040. GDT does not separate from expected value or from
linear random utility. Its numbers sit in the same order as on CPC18 (GDT ahead of both), but neither
interval clears zero.

**The geometric shape transfers, but the shape is not doing much.** Frozen GDT closes 99% of the
distance from chance to a GDT refit on this corpus, so the CPC18 shape loses almost nothing in the move.
CPT's frozen parameters close only 74% of the distance to its own refit. That would favour the geometric
model if its refit were competitive. It is not: the best GDT on this corpus is worse than frozen CPT.
H4 passes, but the interval is wide (a factor of four) and the rehearsal showed H4 also passes when CPT
is the true model, so with H3 passing, H4 is not evidence for the geometric model.

**H5 fails, and not narrowly.** GDT's deficit to CPT is the same with and without losses. Refit on this
corpus, CPT's advantage is in fact larger on gains-only problems (0.6195 against GDT's 0.6758) than on
problems with a loss (0.5904 against 0.6134). The failure Part II attributed to losses is not specific
to losses here.

**CPT at the 1992 estimates ties frozen GDT** (difference +0.0017, interval −0.0137 to +0.0184). A
four-number model from 1992 with one fitted temperature does as well as the geometric model frozen on
CPC18.

## What this does not settle

One corpus. Its problems come from the description-experience literature and differ from CPC18's;
by the coordinate in `../../datasets/DATASET-INVENTORY.md`, 88% of them sit at its corners. The payoff unit is a stimulus-defined convention; a different convention would change
CPT's frozen predictions, though not GDT's, which are homogeneous in payoffs.
