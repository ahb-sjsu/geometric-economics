# prereg-d4gate-v1 — run record, and why the registration is void

**Run 2026-09-13 on Atlas.** Seal verified and tag signature good before the fit.
Bundle combined sha256
`bc85ddd92cdabe48daa81014748d6e1e2732a850ca7212882540ed606501f35b`, signed tag
`prereg-d4gate-v1` on commit `d7ede62`.

**The registration is VOID.** The graded verdicts below were computed on a
coordinate the registration did not register. They are kept because deleting the
record of a run that happened is the file drawer, and they are not evidence for
or against anything.

---

## Why this registration is void

Section 3 of `prereg-d4gate-v1.md` says the coordinates are those of
`d4_rotation.py` and are not changed. The analysis code reimplemented
`_opt_coords` instead of importing it, and reimplemented it wrongly.

| | `d4_rotation.py` | `d4gate_fit.py` as run |
|---|---|---|
| domain coordinate `d` | continuous on `[-1, 1]`, the value-weighted balance `(pos − neg) / (pos + neg)` over the option's outcomes, **`+1` a pure gain** | three-valued indicator in `{-1, 0, +1}`, **`+1` a pure loss** |
| probability coordinate `q` | `2p − 1` on the **salient** outcome, the one of largest absolute value | `2p − 1` on the high outcome |

The domain coordinate differs in form and in sign, so `d·q` in the run is not the
`d·q` of the earlier test and the run tests a different quantity than the document
describes.

The error was made in writing, not in running. `_opt_coords` was never read. It
sits above the part of the file that was read, and a definition that looked
obvious was written from the docstring of the surrounding function instead.

**What falls with it.**

- The cross-tabulation in Section 4 of the registration, and with it the claim
  that the uncertain cell holds four pure-loss rows. "Pure loss" is a category the
  real coordinate does not have, being continuous, so the estimability argument
  that motivated the interaction design was about an artifact.
- The power simulation, which used the same wrong design matrix.
- Both graded verdicts.

**What does not fall.** The registration, its hash, its signed tag, the run
record, and this file are all kept. A corrected registration is a new one with a
new hash and a new tag, not an edit of this one.

## The verdicts as computed, kept and not claimed

| | Prediction | Verdict | Statistic | Bar |
|---|---|---|---|---|
| G1 | The chirality differs by gate | FAIL | `gamma` = −0.0468 | 0.2778 |
| G2 | A chirality is present where the gate fires | PASS | `c2 + gamma` = −0.7382 | 0.1810 |

No falsifier fired. These numbers describe a fit on a coordinate nobody
registered and are recorded for completeness only.

## The pooling diagnostic, which is valid and is the useful result

`analysis/diagnostic_pooling.py` does not reimplement anything. It imports
`d4_rotation.build_continuous` and uses that module's own rows, coordinates and
optimizer settings, so it is unaffected by the error above. It answers the
question the earlier run raised, which is why the interior chirality is reported
at `+0.003`.

287 rows, 270 CPC18 interior and 17 Kahneman and Tversky corners.

| Fit | Rows fitted | Standardised over | `d·q` | nll |
|---|---|---|---|---|
| **A**, as published | all | all | **+0.0032** | 401.15 |
| **B**, corners dropped | CPC18 | CPC18 | **+0.4438** | 168.70 |
| C, corners in likelihood only | all | CPC18 | −0.0002 | 401.85 |
| D, corners in scaling only | CPC18 | all | −2.3546 | 169.00 |

**A reproduces the published number exactly.** `+0.0032` against the `+0.003` of
`RESULTS_d4_rotation.md`, so the earlier pipeline is reproduced and is not in
question.

**A against B is the answer.** Both are internally consistent, each standardised
over the rows it fits. Dropping seventeen corner rows moves the interior chirality
from `+0.003` to `+0.444`. The chirality does not vanish in the interior. It is
masked when the corners are pooled with it.

A against C separates the two channels and shows the masking is carried by the
corner rows' own contribution to the likelihood rather than by their effect on
standardisation, since holding the scaling to CPC18 while keeping the corners in
the fit still gives `−0.0002`. D is reported for completeness and is not a
sensible fit, since standardising CPC18 over a set containing the corners shrinks
every interior predictor and the coefficients blow up to compensate.

The earlier record's own caveat says pooling adversarial Kahneman and Tversky
problems with normal CPC18 "can attenuate the `d·q` term". That is right in
direction and understated in degree. On this decomposition the pooling does not
attenuate the term, it removes it.

## What follows

**The interior question is open again, and in the opposite direction.** The
earlier conclusion that the fourfold pattern is a corner phenomenon rests on
Part B, and Part B's interior estimate is a pooled estimate. Unpooled, the
interior carries a chirality of `+0.44`. That does not restore D₄, it does not
address Part A's `χ² = 75.4` breaking term at the corners, and it is a single
diagnostic on one corpus. It does mean the sentence "the chirality vanishes in
the interior" is not supported by the fit that produced it.

**A corrected registration is worth writing, with three changes.** It must import
`_opt_coords` rather than restate it. It must redo the estimability analysis on
the real continuous coordinate, where the cross-tabulation that motivated the
interaction design does not apply. And it should register the unpooled interior
estimate as its own object, since that is now the live question and the gating
question was always secondary to it.

**A note for the next registration.** The failure here was not caught by the
seal, the signature, the grader separation or the power analysis, all of which
worked. It was caught by a diagnostic that imported the original code instead of
restating it. An analysis that reimplements a definition it claims to inherit
should import it, and where that is impossible the registration should carry the
definition verbatim rather than a description of it.
