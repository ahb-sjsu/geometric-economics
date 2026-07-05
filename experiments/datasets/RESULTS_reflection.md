# The reflection encoding — one geometric mirror spans gains and losses

The standing caveat across every leg of `prereg-sigma-v1` was the **loss/reflection domain**: raw
geometric features (EV, SD, skew, worst, p-fav) fit gains well but miss the reflection effect —
risk-aversion for gains flips to risk-seeking for losses — so a metric fit on gains transferred to
losses at **0%** (Ruggeri leg). `eris-econ/prospect.py` hand-coded a domain flip of d5/d9. Here we
**discover** the reflection encoding by fuzzing, then sharpen it with a PolarQuant-style continuous
mirror. Data: Ruggeri (17 KT problems × 19 countries, 323 country×problem cells, 133 loss / 190 gain).

## 1. The geometric-native mechanism is the *reference*, not the features

In gains the ideal (reference) has **low SD** — the safe option is closest, so it's chosen
(risk-averse). Under losses the ideal should have **high SD** — the gamble is closest (risk-seeking).
Same metric Σ, domain-flipped ideal. We fuzzed over **which** coordinate-ideals flip in the loss
domain (`reflection_fuzz.py`, rank-2 metric):

| loss-domain ideal flip | gain→loss transfer | loss→gain |
|---|--:|--:|
| (none = raw) | **0%** | 39% |
| SD | 54% | 86% |
| SD + pfav | 72% | 88% |
| **SD + worst + pfav** | **80%** | 84% |

The single decisive flip is **SD** (0% → 54%): the reflection effect *is* a flip of the risk
reference. Adding worst and p-favorable refines it to 80%.

## 2. PolarQuant makes the mirror *continuous* — and one metric spans both domains

The discrete flip is binary (ideal = min *or* max SD). PolarQuant's lesson — split magnitude from
direction, transfer the **angle**, recalibrate the scale — makes reflection a **continuous** operation:
the loss domain is the gain domain *reflected across the value axis*, with a fitted reflection
strength `ρ` per coordinate. We fit **one** shared metric + reflection **jointly** on all gain+loss
cells (`polar_reflection.py`):

| model | pooled NLL | |
|---|--:|---|
| raw (one metric, ρ=1) | 0.6478 | the failing baseline |
| **polar (one metric + reflection)** | **0.5936** | ONE model, both domains |
| ceiling (two separate best models) | 0.5931 | best any gain/loss split can do |

**The single polar metric reaches the two-model ceiling — it closes 99% of the raw→two-model gap.**
One shared metric plus a geometric mirror fits gains and losses as well as two entirely separate
theories. This is the unification the raw encoding could not deliver.

### Recovered reflection coefficients (interpretable prospect theory, discovered geometrically)

- **ρ[SD] = −0.80** — the value-risk plane reflects across the value axis at ~80% strength. The
  aversion **angle flips sign** in the loss domain (risk-averse → risk-seeking) — the PolarQuant
  angle-lock. The ~0.2 shortfall from a full mirror (−1.0) is the **loss-aversion asymmetry**.
- **ρ[worst] = +2.96** — the worst outcome looms ~3× larger under losses (loss aversion on the tail).
- **ρ[pfav] = +0.21** — favorable-probability weight collapses in the loss domain.

The SD reflection is the robust core; ρ[worst]/ρ[pfav] are refinements fit on 133 loss cells and are
less stable.

## Honest caveats

- **Fit on Ruggeri.** Both the discrete flip and the polar coefficients were *selected/fit* on this
  corpus. Per the discipline, this is a **discovered encoding to pre-register and re-test** on a
  held-out loss corpus (CPC18 / choices13k contain loss and mixed gambles) — not yet a confirmed
  result. `prereg-reflection-v1` freezes it (below).
- **Pure loss vs mixed.** This covers the gain/loss reflection; mixed-domain gambles and the framing
  (isolation) items are separate.
- **The ceiling comparison is fair now** (the loss model in the ceiling gets its own reflection), so
  "99% of the gap" is a real like-for-like statement, not an artifact.

## What changes in the theory

Reflection is not a second theory or a hand-coded flip — it is **one geometric mirror**: the loss
domain is the gain domain reflected across the value axis (ρ[SD]≈−0.8), with the worst-case amplified
(loss aversion). Combined with the low-rank Σ, the geometry now spans **risky gains, risky losses,
strategic games, and social allocation** with a single shared, low-rank, mirror-symmetric metric —
the loss-domain weak spot that dogged every prior leg is closed (pending held-out confirmation).

*Reproduce: `python reflection_fuzz.py` (discrete) · `python polar_reflection.py` (continuous).*
