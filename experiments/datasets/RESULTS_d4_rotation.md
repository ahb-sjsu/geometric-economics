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
