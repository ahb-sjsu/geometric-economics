# prereg-d4interior-v3 — run record. The chirality does not replicate, and reverses

**Run 2026-09-13 on Atlas.** choices13k, 2,380 rows. Seal verified and tag
signature good before the fit. Bundle combined sha256
`b18b1e8e12fdc4f4c8f06d4f4defbe719f49fb596b5e8890b52ccf919d62f807`, signed tag
`prereg-d4interior-v3` on commit `977c52e`.

**This run is valid.** Gradient infinity norm `1.5e-12` against a registered
tolerance of `1e-5`, Hessian minimum eigenvalue `9.733`, and the estimate varies
by `1.7e-15` across four starts. The optimum is unique and was reached, which is
what v2 could not establish.

---

## Verdicts

| | Prediction | Verdict | | |
|---|---|---|---|---|
| V1 | The chirality replicates in sign | **FAIL** | `c2` = **−0.1216** | bar 0.1043 |
| V2 | And within a factor of two of CPC18 | **FAIL** | band [0.2219, 0.8876] | |

**F2 fired.** The estimate is negative beyond the bar. The registration states
that this is a sign reversal, a worse outcome than a null, and is to be reported
as such and not as a near miss.

## What this settles

**The CPC18 interior chirality of `+0.4438` does not replicate.** On an
independent corpus of nine times the size it comes out at `−0.1216`, reversed in
sign and past the bar in the wrong direction.

This is not a power failure. The design detects `+0.4438` with probability 1.000
and half of it with probability 0.966, at a size of 0.034. Had the CPC18 value
been a property of interior choice rather than of CPC18, this run would have
found it.

## What it does to the challenge this line was built on

The pooling diagnostic remains arithmetically correct. On CPC18, dropping the
seventeen corner rows does move the chirality from `+0.003` to `+0.4438`, and
fit C does locate the masking in the corner rows' likelihood contribution. Those
are facts about CPC18 and nothing here disturbs them.

But the quantity that decomposition revealed is not stable. It is `+0.44` on one
corpus and `−0.12` on another, and no consistent interior chirality survives the
pair. **The challenge this line raised against `RESULTS_d4_rotation.md` does not
survive its own test.**

The earlier record concluded that the fourfold chirality is a corner phenomenon
and not a property of the interior. This run supports that conclusion, by a
different route than the one the record gave. The record reached it from a pooled
estimate near zero, which the pooling diagnostic showed was masked rather than
measured. This run reaches it from two unpooled estimates that disagree in sign.
Either way there is no reliable interior chirality, and the record's conclusion
should stand as written.

The correction owed to the record is therefore smaller than it looked. Its Part B
interior estimate of `+0.003` is a pooled quantity and its own caveat about
attenuation understates what pooling does. The conclusion drawn from it happens
to be right.

## What it does to the D₄ rehabilitation

`D4_REHABILITATION.md` argued two things. The first, that the earlier verdict was
scored against a continuous rotation that the D₄ account of `sqnd-probe` does not
claim, is a reading of two documents and is untouched by any measurement here.
The second, that the rotation is gated rather than absent, was tested by
`prereg-d4gate-v1` and that registration is void for an unrelated coding error,
so it remains untested.

What this run adds is that the interior has no stable chirality to be gated. That
does not refute the gating reading, since a gated quantity could be unstable
across corpora for gating reasons, but it removes the motivation that produced
it. A future gating test would need to establish a stable interior quantity
first, and this run says there is not one on these two corpora.

## Record of the lineage

Three registrations, one verdict.

| | Outcome | Cause |
|---|---|---|
| `prereg-d4gate-v1` | VOID | the analysis reimplemented a coordinate instead of importing it, and got its form and sign wrong |
| `prereg-d4interior-v2` | VOID under its own F3 | a derivative-free optimizer did not reach the optimum of a convex problem |
| `prereg-d4interior-v3` | **Verdict: V1 FAIL, V2 FAIL, F2 fired** | valid run, gradient norm 1.5e-12 |

The two voids are different in kind. The first was an error. The second was a
falsifier written in advance against ourselves, firing as designed on a run that
would otherwise have reported a number from an optimizer that had not converged.

Section 11 of the registration lists five errors in this lineage with the
structural fix for each. The useful generalisation is that every one was caught
by machinery rather than by care. The coordinate error by a diagnostic that
imported the original code, the optimizer failure by an estimator verified
against a known answer before being trusted, the threshold error by counting
failures instead of aborting on them, and two transcription errors by reading the
values back out of the record rather than from the draft.

---

**Forward note, 2026-09-13.** This record concluded that "no consistent interior
chirality survives the pair" and that the earlier corner-phenomenon reading
happens to be right. `prereg-d4stability-v2` sharpens both halves.

The quantity is not merely inconsistent between corpora. Split **one** corpus of
95,748 individual choices by stake size and the chirality runs `+0.2279`,
`−0.2609`, `−0.4216`, `−0.5003`, Cochran's Q `103.0` against a null mean of
`9.93`, permutation `p = 0.0005`, range `0.728` against the `0.565` gap this
record was trying to explain. **Its own `−0.1216` is one draw from that spread**,
not a corpus-level fact, and the same applies to CPC18's `+0.4438`.

The cause is that the six-term model explains a weighted `R² = 0.361` of a freely
estimated kappa surface. The record's conclusion still stands, and now for a
third reason: there is no interior chirality to find because kappa is not a
quadratic in `(d, q)`.

Restricting this corpus to its 1,285 two-outcome rows, excluding the 1,095 with
`LotNumB > 1` that the fit read through three columns, leaves the chirality at
`−0.0659`. The multi-branch collapse is not what made it negative. See
`../d4stability/RESULTS-v2.md`.

**Second forward note, same day.** The reason its `−0.1216` was one draw from a
spread is now known, and it vindicates this record's closing paragraph by a route
it did not have. `|d| = 1` is the set of gambles with no loss branch or no gain
branch, not a region of the coordinate, and there `d·q` is algebraically `±q`.
Inside mixed gambles the chirality is `−0.0303 ± 0.0728`, never more than 0.8
standard errors from zero across six independent lines.

**This record said the earlier conclusion "happens to be right". It is right, and
not by accident.** The fourfold `d·q` is a corner phenomenon because at the
corners it is not a chirality. See `../d4stability/SEAM.md`.
