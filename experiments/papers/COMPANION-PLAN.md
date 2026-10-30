# Part II and the theory paper: how they divide the work

Written 2026-10-30, after Part I was published (IEEE TCSS, DOI 10.1109/TCSS.2026.3734068).

## The division

The **theory paper** states what a test of a decision theory can and cannot show, and proves it.
**Part II** runs the tests and reports what happened. Each Part II result cites the statement it
tests, and each theory statement names the Part II section that tests it, or names the sealed design
that will. Neither paper repeats the other's material beyond a one-paragraph recap.

The theory paper supersedes `paper_00_theory.md`. That draft led with scalar irrecoverability (no
continuous injection from R^d to R). The statement is true and machine checked
(`lean/ScalarIrrecoverability.lean`), but it does not bear on choice. Debreu (1954) gives every
continuous preference on a connected separable space a continuous utility. A scalar utility is
therefore always available, and GDT itself contracts to a scalar cost before choosing. The flagship
(`paper_flagship_gdt.md` section 2) already moved the target from scalarity to premature projection.
The theory paper is built on that footing, and the injection theorem becomes a remark.

## Statement to test map

| Theory paper | Statement | Tested in Part II by | Status of the test |
|---|---|---|---|
| Def. 1-2 | The model, and the class of models that read an option through a projection that omits coordinates | Section II recap | n/a |
| Prop. 1 | Limiting correspondence. Logit response at finite T, Nash at T to 0 under the payoff-loss encoding | n/a, containment only | n/a |
| Remark | Debreu and the injection theorem. A scalar is always available, so scalarity is not the issue | n/a | n/a |
| Thm 1 | Sufficient-statistic test. Behavior factors through a projection iff no matched design shows a gap. A pair matched under several incumbents at once exists iff the manipulated coordinate is not a function of their statistics | Projection-gap section | Language-model panel, `prereg-v1`. Human study `prereg-v2` frozen, not run |
| Thm 2 | Sign identification. Under an explicit cross-term bound, the sign of the gap is the same under every strictly increasing re-encoding that fixes the reference, for any menu size | Projection-gap section, design paragraph | Bound to be checked on the designs |
| Prop. 2 | Scale identification. Choice depends on (P, T) only through P/T^2, so the metric's shape is identified and its magnitude is not | Cross-domain transfer section. Angle-lock transfers the identified part | Exploratory, polar step post hoc |
| Prop. 3 | Stake invariance. Under the share encoding, choice is invariant to stake for every monetary variance. Under income units it depends on stake only through stake/income | Money-in-income-units section (new) | `prereg-boundary-v1`, OSF osf.io/ead4x, run 2026-09-12, 5 of 6 pass |
| Prop. 4 | Direction difference. With a symmetric metric, w(a to b) - w(b to a) equals the net boundary penalty, so the metric cancels exactly | None in Part II. Named as the next designed test | `prereg-d4transition-v1` sealed, no data |
| Prop. 5 | Fixed information price. With uniform prior, the rational-inattention solution is the logit in minus cost with T equal to the information cost | Temperature section | In-sample on the panel. Must be stated as in-sample |

## Order of work

1. Part II. Close the TODOs from repo records (background survey running 2026-10-30), add the
   money-in-income-units section from `boundary/RESULTS.md`, cite Part I by DOI, move the two
   theorems in its projection-gap section to statements that cite the theory paper, and apply the
   prose standard.
2. Theory paper. LaTeX source in `theory/`, statements and proofs per the table, prior art credited
   (Debreu; Tversky and Kahneman on description invariance; Salant and Rubinstein on frames;
   Bernheim and Rangel on ancillary conditions; logit scale non-identification; Matejka and McKay;
   McKelvey and Palfrey). Venue chosen after its generative-AI policy is read.
3. Cross-check. Every theorem number cited in Part II matches the theory source, and every Part II
   section the theory paper points to exists.

## Update 2026-10-30, later the same day: three papers, not two

The owner chose to ship the corrected material as Part II now and to make learned coordinates Part III.

| Paper | Where | State |
|---|---|---|
| Part II (TCSS) | `tcss-part2/part2_manuscript_revised.tex` | Corrections applied (`tcss-part2/CORRECTIONS-2026-10-30.md`), income-units section added, 7 pp, not committed |
| Theory | `theory/theory_manuscript.tex`, core in `theory/STATEMENTS.md` | Full draft, 8 pp. Theorem 2 now holds for any manipulation direction under one inner-product condition, so it covers learned coordinates. Venue open (J. Math. Psych. recommended) |
| Part III (learned coordinates) | `learned/` | Registration `prereg-learned-v1` drafted. Pipeline built. Rehearsal on simulated labels running on Atlas. Seal, signed tag and PUSH before real labels are scored |
