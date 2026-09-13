# prereg-d4gate-v1 — run record

**Run 2026-09-13 on Atlas.** CPC18 description regime, `Trial == 1`, 270 interior
rows, 169 certain and 101 uncertain, Kahneman and Tversky corners excluded as
registered. Seal verified before the fit. Bundle combined sha256
`bc85ddd92cdabe48daa81014748d6e1e2732a850ca7212882540ed606501f35b`, signed tag
`prereg-d4gate-v1` on commit `d7ede62`, good signature.

`results.json` and `grade.json` are committed as executed. Bars live in
`analysis/d4gate_grade.py`, written before any fit touched the outcome column and
not edited.

## Verdicts

| | Prediction | Verdict | Statistic | Bar |
|---|---|---|---|---|
| G1 | The chirality differs by gate | **FAIL** | `gamma` = −0.0468 | 0.2778 |
| G2 | A chirality is present where the gate fires | **PASS** | `c2 + gamma` = −0.7382 | 0.1810 |

No falsifier fired. F1 requires both under their bars and F3 requires G1 passing
with G2 failing. Neither describes this outcome.

## What the run says

**The gated reading is refuted.** `gamma` is −0.047 against a bar of 0.278, so the
chirality does not differ between the cell where a sure outcome is on the menu and
the cell where one is not. The certainty gate does nothing. Since the power
simulation gives G1 a detection rate of 0.95 at a gated chirality of 0.50, a
gating effect of that size would have been found and was not. The reading proposed
in `D4_REHABILITATION.md`, that the rotation is gated rather than absent, does not
survive its own test on this corpus under this gate.

**The absent reading is also refuted, and by more.** The chirality is not near zero
anywhere in the interior. It is −0.691 where the gate does not fire and −0.738
where it does, against a bar of 0.181. It is large, negative, and uniform.

So neither reading that motivated the registration is right. The interior carries
a substantial chirality that does not care about the gate.

## An open question this run raises about the earlier result

`RESULTS_d4_rotation.md` reports the interior chirality at **+0.003** and concludes
the fourfold pattern is a corner phenomenon. This run, on the interior alone, puts
it at about **−0.73**. That is not a small disagreement and it has to be explained
before either number is used.

It is not an optimizer artifact. A diagnostic refit of the interior-only data with
the earlier test's exact optimizer settings, one Powell start at zero with 20000
iterations, returns −0.7509, and starts at +0.1 and −0.1 return −0.7499 and
−0.7294 with likelihoods agreeing to three decimals. The interior-only estimate is
stable.

The difference must therefore come from what the earlier fit pools with the
interior. It fits the Kahneman and Tversky corner rows together with CPC18 and
standardises the two predictors over the combined set, so the corner rows both
enter the likelihood and rescale every interior row. The earlier record's own
caveat anticipates the direction of this, saying that pooling adversarial Kahneman
and Tversky problems with normal CPC18 "can attenuate the `d·q` term". If the
present estimate is right, the caveat understates what happens. The pooling does
not attenuate the term, it removes it and reverses its sign.

**This is stated as a question and not as a verdict.** The earlier pooled fit has
not been reproduced here, and until it is, the honest position is that two fits on
overlapping data disagree and the reason is identified but not demonstrated.
Reproducing `part_b` of `d4_rotation.py` and then refitting it with the corners
dropped is the next step, and it is a diagnostic rather than a registration,
because no prediction is at stake in it.

## What this does not settle

The registration is spent. Anything further on this corpus is exploratory and must
be labelled so, including the diagnostic above.

The run says nothing about the corners. Part A of the earlier test remains as
written, with the exact D₄ broken at the corners at `χ² = 75.4`, and this run did
not examine them.

It says nothing about a continuous rotation, which nothing here tests, and
nothing about the moral-domain generator asymmetry reported in `sqnd-probe`, which
was measured on different subjects with a different instrument. What
`D4_REHABILITATION.md` argued about the earlier verdict's target still stands. What
it proposed as the repair does not.

Power is the standing caveat in the other direction. At a true gated chirality of
0.25 the design finds gating only 29 percent of the time, so the G1 failure rules
out a gating effect of 0.5 and leaves one of 0.1 untested. The registration
requires that sentence to appear here and it does.
