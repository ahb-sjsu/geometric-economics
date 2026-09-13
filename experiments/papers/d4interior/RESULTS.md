# prereg-d4interior-v2 — run record. VOID under its own F3

**Run 2026-09-13 on Atlas.** choices13k, `Block == 1` and `Feedback == 0`, 2,380
rows. Seal verified and tag signature good before the fit. Bundle combined sha256
`49b2f3f5392e0b7cfade6612aa5b7ce0e355e51b3260588ae7b27037ebca141c`, signed tag
`prereg-d4interior-v2` on commit `302ef88`.

**The run is VOID.** F3 fired. The registration says a void run is reported as
void and is not retried with other starts, so it has not been.

---

## What happened

| Start | nll | `d·q` |
|---|---|---|
| 0.0 | 1560.411999 | −0.0923 |
| 0.1 | 1560.393846 | −0.1088 |

The objectives differ by **0.0182** against a registered tolerance of `1e-6`. The
optimizer did not reach a common optimum from the two starts, so the estimate is
not identified by the procedure as registered and nothing may be read off it.

The graded verdicts, recorded and not claimed, were V1 FAIL and V2 FAIL with
`c2 = −0.1088` against a one-sided bar of 0.1877. **These do not count.** They
were computed from the better of two runs that disagree, and a number the
procedure cannot reproduce from a different start is not an estimate.

## Why F3 exists and why this is the system working rather than failing

F3 was registered before the fit, against the possibility that the fit would not
converge, with the remedy fixed in advance as voiding rather than retrying.
Without it the natural move on seeing two disagreeing starts is to try a third,
keep the one that looks best, and report it. That is fitting the optimizer.

This is the second registration in this line not to yield a verdict, and the two
failures are of different kinds and should not be read together. v1 was void
because its code did not implement what its document registered, which is an
error. v2 is void because a falsifier written against ourselves fired exactly as
intended, which is the instrument doing its job.

## Diagnosis, which is not part of the registration

Powell is derivative-free and is being asked to optimise seven parameters on a
likelihood that appears flat along some direction of the kappa terms. Two starts
`0.1` apart end `0.018` apart in objective and `0.017` apart in the chirality,
which is a scale of disagreement comparable to the estimate itself at `−0.1`.
The choices13k design also carries a median of 16 subjects per problem against
CPC18's 120, so each row's rate is noisier even though there are nine times as
many rows.

The estimator, not the corpus, is what failed here. That is a fixable thing and
it is fixed by changing the estimator, not by changing the bars or the starts.

## What a v3 would need

1. **A convergent estimator.** An analytic gradient with a quasi-Newton method, or
   a convexified parameterisation, with the convergence criterion registered as a
   gradient norm rather than as agreement between arbitrary starts.
2. **A conditioning check on the design**, run on covariates only before freezing,
   reporting the condition number of the kappa term matrix. If the terms are close
   to collinear on choices13k, the question needs a different term set and not a
   different optimizer.
3. **The bias carried forward.** The v2 simulation found this estimator returns
   `+0.092` under a true zero. A v3 should either register a bias-corrected
   estimator or keep the one-sided calibrated bar and drop the magnitude claim,
   since comparing raw estimates across designs was already the weaker half of v2.

## What is unaffected

The pooling diagnostic stands. It imports `d4_rotation`'s own row builder and
optimizer settings and reproduces the published `+0.003` exactly at `+0.0032`,
and its decomposition showing the CPC18 interior chirality at `+0.4438` with the
corners dropped does not depend on anything voided here.

What remains untested is whether that `+0.4438` replicates. This run did not test
it. The interior question is open and the CPC18 estimate is still a
single-corpus result discovered on the corpus it was measured on.
