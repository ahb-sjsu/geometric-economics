# prereg-boundary-v1 — run record

**Run 2026-09-12 on Atlas.** Data openICPSR 112485-V1, 1,456 responder decisions,
study counts SR 820, C 178, IN 458, matching Section 2 of the registration
exactly. Seal verified before the run: both bundle files hash to their recorded
values, combined `175bad98…`, and the signed tag `prereg-boundary-v1` checks
against commit `b3cb559`. OSF registration `osf.io/ead4x`, 2026-09-10. Section 11
step 4 authorises the fit only after those, and all were in place.

`results.json` and `grade.json` are committed as executed. Thresholds live in
`boundary_grade.py`, which was written before any fit and was not edited.

## Verdicts

**5 of 6 pass. No composite verdict is registered, so each stands alone.**

| | Prediction | Verdict | What decided it |
|---|---|---|---|
| P1 | Money enters acceptance through the responder's income units | **PASS** | `g` = 0.817 > 0, likelihood ratio p = 2.3e-10 against alpha 0.01 |
| P2 | One monetary coordinate, not three | **PASS** | LR test of equal slopes not rejected, p = 0.19 |
| P3 | Nominal stake adds nothing given the offered amount and share | **PASS** | `h` = 0.165 per decade, under the 0.25 bound, p = 0.46 |
| P4 | The shared coordinate transfers across countries | **PASS** | Leave-one-study-out, all three folds within 0.003 nats against a 0.02 margin |
| P5 | The geometric responder matches the logit | **FAIL** | Two ways, below |
| P6 | The boundary is on the responder side | **PASS** | Proposer slopes flat on SR and C, within 1.5 pp per decade |

## What P5 says

P5 failed on both of its conditions, and the first is the more informative.

**The income rescaling did no work.** `sigma_1^2` sat at 10,000, exactly its
registered upper bound. The grader's own note, written before the run, states
what that means. Model G has collapsed to Part I's responder, so the monetary
variance the model was given to fit was pushed as far toward inactive as the
registration allowed. This is a failure on its own, independent of any
log-loss comparison.

**Held-out log-loss is worse than a logit on every fold.**

| Held out | Model G | M1 logit | G minus M1 | Margin |
|---|---|---|---|---|
| SR | 0.325 | 0.292 | +0.033 | 0.03 |
| C | 0.314 | 0.254 | +0.060 | 0.03 |
| IN | 0.939 | 0.614 | **+0.325** | 0.03 |

SR misses by a hair. C misses clearly. IN, the Meghalaya high-stakes study that
motivated the whole question, misses by an order of magnitude more than the
margin.

## The reading

The registration asked two separable questions and got two different answers.

**The coordinate works.** Money reaches acceptance through the amount offered
measured in the responder's own income units, one shared slope covers three
countries, nominal stake adds nothing once that coordinate is in, and the
coordinate transfers across countries almost exactly. P1 through P4 are as clean
as this registration could have returned, and Part I Section VII.A proposed the
income-scaled coordinate as an untested construction, so this is the test it
asked for and the construction passed it.

**The model built on it does not.** Model G, the geometric responder carrying
Part I's encoding constants, is beaten by a plain logit on every fold and turns
its own monetary variance off to get there. The failure is largest exactly where
the stakes are largest.

P6 locates the boundary on the responder side, with proposer behaviour flat in
the stake for two of three studies.

## What this does not settle

The grader records that P2's pass is a non-rejection and that the registered
simulation established size rather than power against heterogeneity, so P2 is
evidence consistent with one shared coordinate and not a demonstration of it. The
descriptive ratio of largest to smallest slope is 2.32 with a bootstrap interval
of 1.13 to 9.70, which is wide, and the registration deliberately attached no
threshold to it.

P5's failure is a failure of Model G as specified, with Part I's constants fixed
and only `sigma_1^2` free. It is not a test of the geometric programme in
general, and the registration did not claim it would be.

## One observation, recorded and not claimed

A parameter pinned exactly at the boundary of its admissible range is the kind of
thing `stratification-thesis.md` is about, and it is tempting to read it that way.
That reading is not available from this run. The thesis was written from four
earlier results and this is a fifth of the same kind, which makes it discovery
material rather than evidence. It is recorded here so that a later registration
can use it, and it is claimed as nothing.
