# Efficient-coding test — is the aversion angle a fundamental (Shannon-like) invariant?

Motivated by the conjecture that the polar encoding hides something fundamental (a Shannon-Hartley-style
constant). The falsifiable version: is the aversion angle the **efficient code** for the choice
environment — i.e., does a capacity-limited decider normalize its feature-sensitivity by the
environment's variance, leaving a **constant intrinsic weight** underneath? Non-circular signature:
`β_raw_k ∝ 1/σ_k` (adaptation) with `β_z_k = β_raw_k·σ_k` (the invariant). Decisive within-corpus test:
bin choices13k into sub-environments with different risk spread σ_SD and check whether the normalized
weight is constant.

## Within-corpus adaptation (choices13k, 4 bins by risk level)

| bin | σ_SD | β_raw_SD | β_z_SD | angle_raw | angle_z |
|---|--:|--:|--:|--:|--:|
| 0 | 1.9 | +0.031 | **+0.060** | +10.8° | +1.7° |
| 1 | 5.5 | +0.009 | **+0.051** | +4.9° | +2.2° |
| 2 | 10.8 | −0.007 | **−0.078** | −5.8° | −5.2° |
| 3 | 18.8 | −0.002 | **−0.045** | −2.9° | −4.5° |

- **Adaptation is present but partly mechanical:** `corr(β_raw_SD, 1/σ_SD) = +0.97`. Since `β_raw ≡ β_z/σ`
  by definition, a high correlation only says β_z varies slower than σ — it is not by itself evidence of
  a normalized invariant.
- **The invariant FAILS:** the z-normalized risk weight **β_z_SD is not constant — it sign-flips**
  (+0.06 → −0.08) as the environment's risk level rises. People are slightly **risk-seeking for
  small-variance gambles and risk-averse for large** ones — the classic **fourfold pattern** of risk
  attitudes, not a conserved constant.

## Cross-domain (representative corpora)

| domain | σ_EV | σ_SD | angle_raw | angle_z (intrinsic) |
|---|--:|--:|--:|--:|
| CPC18 | 11.8 | 16.0 | −2.6° | −3.5° |
| choices13k | 12.3 | 14.3 | −0.7° | −0.8° |
| bogota games | 92.2 | 56.3 | +3.2° | +2.0° |

Raw-angle spread 2.4°, intrinsic-angle spread 2.2° — normalization does essentially nothing (1.1×).
The cross-domain angle stability is because these corpora happen to have **similar σ ratios** and small
risk weights, **not** because normalization reveals a deep invariant.

## Verdict — the honest answer to the Shannon-Hartley question

**No fundamental conserved constant hides in the polar encoding.** The test found:
- **Real, established mechanism (stands):** softmax choice = rational inattention; temperature = the
  price of a bit. That is a genuine information-theoretic foundation — but it is about the *form* of the
  choice rule, not a conserved angle.
- **The would-be-fundamental claim (falsified):** the aversion angle is **not** a normalized invariant.
  The normalized risk weight varies with — and sign-flips across — the environment's risk level (the
  fourfold pattern). The apparent cross-domain constancy is a coincidence of similar variance ratios,
  not a law.

So the polar decomposition is a **useful, real** description (shape/direction vs scale/temperature), and
the rational-inattention link is a **real** foundation, but there is **no Shannon-Hartley-style universal
constant** in the aversion angle. Naming things "capacity" and "SNR" would be flattering vocabulary; the
mechanism that is actually there is **variance-adaptive, risk-level-dependent** weighting — adaptation,
not a conservation law.

## What this means for the program (the useful part)

The result is not a dead end — it **redirects**: the thing to model is the **risk-level-dependence** of
the weight (the fourfold pattern / diminishing sensitivity), which is exactly the **magnitude/temperature
family** that has been the program's recurring open problem. Rational inattention (temperature = price of
information, adapting to stakes) is the principled candidate for *that*, and it is testable — but it will
explain the *temperature*, not conjure a conserved angle.

*Reproduce: `python efficient_coding.py`.*
