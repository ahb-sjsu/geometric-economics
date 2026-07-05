# Second-generator (V₄) test — the fourfold pattern is Klein-four + loss-aversion breaking

We had one involution empirically: the value reflection **σ_v** (gain↔loss, ρ_SD = −0.8). The
fourfold pattern needs a second, commuting involution **σ_p** (certainty↔possibility) to generate
the Klein four-group **V₄ = (ℤ/2)²**. The algebraic signature of V₄ is that the risk attitude depends
**only on the product d·q** (pure interaction, no main effects). Test: pool the 17 KT problems × 19
countries into one logit whose ΔSD (risk) coefficient is decomposed over domain d (gain +1 / loss −1)
and probability level q (certainty/high +1 / possibility/low −1):

`P(A) = σ( β_EV·ΔEV + (b₀ + b_d·d + b_q·q + b_dq·d·q)·ΔSD )`.

## Decomposition (95% CI, bootstrap over countries)

| parameter | estimate | 95% CI |
|---|--:|--:|
| β_EV | −1.045 | [−1.16, −0.94] |
| b₀ (base) | +0.032 | [−0.00, +0.07] |
| b_d (domain main effect) | **+0.199** | [+0.10, +0.29] |
| b_q (probability main effect) | **+0.004** | [−0.05, +0.05] |
| **b_dq (INTERACTION)** | **+0.803** | [+0.68, +0.91] |

## The V₄ result

- **The interaction dominates:** |b_dq| = 0.803 vs |main effects| = 0.234 → **ratio 3.4**, CI excludes
  zero. The risk attitude is primarily the **product d·q** — the Klein-four signature. The fourfold
  pattern has the group structure the Hohfeld/D₄ intuition predicted.
- **b_q ≈ 0** (CI includes 0): probability level has **no main effect** — it matters *only* through its
  interaction with domain. That is exactly how a pure involution generator behaves: σ_p is real, and it
  acts by flipping, not by an independent offset.
- **σ_v is a clean involution** (residual 8% of scale): flipping domain flips the risk attitude —
  independently confirmed as ρ_SD = −0.8.

## The symmetry-breaking term — and why it's the same loss aversion

The group is **not perfectly clean V₄**: b_d = 0.199 is a real **domain main effect**. It breaks σ_p's
involution (residual 50%) and the diagonal-cell closure (50%) — both driven by b_d. This is **loss
aversion**: gains and losses are not perfectly mirror-symmetric.

Crucially, this is the **same asymmetry** seen independently in the reflection encoding, where the
value mirror came out **ρ_SD = −0.80, not −1.0** — the 0.2 shortfall being loss aversion. Two
unrelated analyses (a polar reflection fit; a 2×2 interaction decomposition) **agree** that the
fourfold symmetry is broken by a single loss-aversion term. That convergence is the strongest evidence
the structure is real and not curve-fitting.

## Verdict

**The fourfold pattern = V₄ (Klein four) + a loss-aversion symmetry-breaking term.**
- Two commuting involutions — **σ_v** (value reflection, clean, ρ=−0.8) and **σ_p** (certainty↔
  possibility, the second generator, no main effect) — generate the dominant interaction structure.
- A single domain main effect (loss aversion) perturbs it, consistently with the −0.8 mirror.

So the group-theoretic reading of the fourfold pattern is empirically supported: it is a Klein-four
structure, not four independent facts. This is a far deeper "fundamental structure" than the Shannon
angle that was ruled out.

## Honest caveats

- **Sign labels are unreliable here.** The KT problems are adversarially EV-violating (β_EV < 0), which
  muddles the *absolute* risk-averse/seeking label on each cell. The **structural** result (interaction
  dominance, b_q≈0) is sign-convention-independent and robust; the per-cell attitude *labels* are not.
- **This is V₄, not yet D₄.** Klein-four is the rotation-free subgroup. The **full D₄** (your
  D₄-symmetric framework; Hohfeld's eight incidents) needs the **cross-axis rotation** that mixes
  domain and probability — a symmetry taking gain·high directly to loss·low. That is a separate,
  stronger test, not done here.
- **One dataset (Ruggeri KT).** Held-out replication on another gain+loss corpus would harden it.

*Reproduce: `python second_generator.py`.*
