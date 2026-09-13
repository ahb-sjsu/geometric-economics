# D4 rotation test — does V₄ lift to the full dihedral group? **No.**

V₄ (Klein four) is the rotation-free subgroup of D₄; the extra element is the 90° rotation `r`
(order 4), `r² = σ_v·σ_p`. Under D₄ the risk-attitude space on the (domain d, probability q) plane
splits into irreps: **A₁** (trivial), **B** (the `d·q` pseudoscalar — rotation-covariant chirality, on
which `r` acts as a sign-flip), **E** (the standard rep `d, q`, and `d²−q²` — rotation-*breaking*).
**D₄ (risk = the B chirality) holds iff the E-component vanishes.**

## Part A — discrete irrep decomposition (KT corners)

| irrep | quantity | value |
|---|---|--:|
| A₁ (trivial) | \|b₀\| | 0.032 |
| **B** (d·q pseudoscalar, D₄-allowed) | \|b_dq\| | **0.803** |
| **E** (standard rep, rotation-breaking) | \|(b_d, b_q)\| | **0.199** (b_d=+0.199, b_q≈0) |

- **D₄ fraction B/(B+E) = 0.80** — the chirality dominates at the corners.
- **But E is significant:** D₄-constrained (E=0) vs V₄/full → **V₄ wins BIC** (87544 < 87597); LR test
  for E (2 df) **χ² = 75.4, p = 4×10⁻¹⁷**. The rotation-breaking term is real, so the **exact D₄ is
  already broken at the corners** — by loss aversion (b_d), the same term as the ρ_SD=−0.8 mirror.

## Part B — continuous rotation (KT corners + CPC18 mixed gambles fill the interior)

The decisive new test: a genuine rotation must govern the *interior*, not just the four corners.
Fitting the risk coefficient `κ(d,q)` on 287 choice-sets, split into D₄-allowed and breaking terms:

| term | coefficient | type |
|---|--:|---|
| const | −0.265 | allowed |
| d²+q² | −0.058 | allowed |
| **d·q (chiral)** | **+0.003** | allowed |
| d | −0.194 | **breaking** |
| q | +0.144 | **breaking** |
| **d²−q²** | **+0.340** | **breaking** |

**The rotation-covariant chirality `d·q` vanishes in the interior (+0.003)**, while the
rotation-*breaking* terms dominate (chiral fraction ≈ 0.00). The fourfold `d·q` pattern is a **corner
phenomenon**, not a continuous 90° symmetry. `d²−q²` (the term that distinguishes the domain axis from
the probability axis) is the largest — the two axes are **not** interchangeable.

## Verdict — V₄ confirmed, D₄ rejected

**The fourfold pattern is a rectangle (V₄), not a square (D₄).** Two commuting reflections — value
(σ_v, ρ=−0.8) and probability/certainty (σ_p) — generate the Klein four-group, and that structure is
real and dominant. But the **90° rotation is not a symmetry:** the two axes are distinguishable (loss
aversion + the `d²−q²` interior term), so V₄ does **not** lift to the full D₄.

This is a clean, informative negative for the D₄-symmetric framework: the data supports the **Klein
four-group** (two reflections) but **not** the dihedral rotation. If the framework needs full D₄, the
missing rotation is a real gap the data does not fill — the value and probability axes are genuinely
different kinds of thing (one carries loss aversion, the other does not).

## Honest caveats

- **Part A is load-bearing** (clean KT data, E highly significant). **Part B is suggestive:** the
  continuous coordinates for mixed gambles are a pragmatic construction, and pooling adversarial KT
  (β_EV<0) with normal CPC18 can attenuate the `d·q` term. Both point the same way (no exact/continuous
  rotation), which is why the verdict is D₄-rejected, but the interior estimate is not definitive.
- **Two corpora.** A dataset designed to sit at intermediate (domain, probability) angles would settle
  the interior test cleanly.

*Reproduce: `python d4_rotation.py`.*

---

**See `D4_REHABILITATION.md` (2026-09-12).** The closing verdict above is scored
against a continuous 90 degree rotation. The D4 framework of `sqnd-probe` does not
claim one and was created by abandoning the continuous group for exactly that
reason, so this negative lands on SU(2) rather than on D4. The measurements here
are unaffected and none of them changes. Whether a gated rotation survives is an
open question with an unrun registered test, Prediction G in that file.

---

**Addendum 2026-09-13. Part B's interior number is a pooling artifact, and the
six-term model it rests on describes about a third of the surface.**

Part B reports the rotation-covariant chirality `d·q` at `+0.003` in the interior
and concludes the fourfold pattern is a corner phenomenon. **The arithmetic is
right. Both the number and the conclusion are superseded, for separate reasons.**

**The number was masked.** `d4gate/analysis/diagnostic_pooling.py` reproduces
`+0.003` exactly at `+0.0032`, then shows it is pooled over seventeen Kahneman
and Tversky corner rows that dominate the likelihood. Dropping them moves the
CPC18 interior chirality to `+0.4438`. The chirality does not vanish in the
interior, and the sentence above saying it does should not be cited.

**The conclusion cannot be rescued by unpooling either**, because the quantity
is not stable. `prereg-d4stability-v2`, on 95,748 individual description choices
from peterson2021using, split the corpus into four folds by outcome scale:

| fold | `c2` | | registration | interior `d·q` |
|---|---|---|---|---|
| smallest stakes | **+0.2279** | | `prereg-d4interior-v3`, choices13k | `−0.1216` |
| | −0.2609 | | `prereg-d4stability-v2`, whole corpus | `+0.2506` |
| | −0.4216 | | CPC18, corners dropped | `+0.4438` |
| largest stakes | **−0.5003** | | | |

Cochran's Q of `103.0` against a random-split null mean of `9.93`, permutation
`p = 0.0005`, range `0.728`. **One corpus split by stake size moves the chirality
by more than the entire gap between CPC18 and choices13k.**

**And the reason is that the model is wrong.** Estimating kappa freely, one
coefficient per cell of the `(d, q)` plane with no functional form imposed, the
six-term quadratic explains a weighted `R² = 0.361` of the resulting surface,
with a largest cell residual of 6.39 standard errors. The strongest feature is a
discontinuity at `|d| = 1`: two adjacent cells at `d = +0.962` and `d = +1.000`
carry kappa of `+0.7397` and `−0.5535`, a jump of `1.29` across `Δd = 0.038`.
No smooth function of `(d, q)` can do that.

Fit a badly misspecified model to subsamples of different stimulus composition
and its coefficients move, because each subsample projects the same
non-quadratic surface onto a different quadratic. **The fold heterogeneity and
the corpus-to-corpus disagreement are the same artifact seen twice.** A chiral
component does survive, the free surface projecting onto `d·q` at `+0.2155`
without the term being imposed, but it is a projection coefficient and not a
parameter of anything.

**The D₄ verdict itself stands, on Part A and not on Part B.** The E component is
significant at the corners, likelihood-ratio `χ² = 75.4`, `p = 4×10⁻¹⁷`, and the
free V₄ model beats the D₄-constrained model on BIC. Nothing here touches that.
What changes is that the interior is not a second and independent reason, and the
reading that the chirality lives only at the corners is wrong.

See `../papers/d4stability/RESULTS-v2.md`. Note also that this record's own
`d4_rotation.py` coordinate is a two-outcome function, while CPC18 contains 122
multi-branch games of 270 and choices13k 1,095 rows of 2,380, all read through
three columns. That approximation is shared across both corpora so it does not
explain their disagreement, and restricting choices13k to its 1,285 two-outcome
rows leaves the chirality at `−0.0659`, still negative.
