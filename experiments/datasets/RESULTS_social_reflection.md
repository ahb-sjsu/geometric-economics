# Track A completed — the social reflection on real Charness-Rabin allocation data

The reflection-motif push needed choice-level 2-D allocation data. It arrived: **Charness & Rabin
(2002 QJE), Table I** — the seven two-person **dictator games** (the paper's clean distributional set;
response games are excluded for reciprocity confounds). B allocates between two (own, other) pairs with
own and other varying *independently* — real 2-D social choice, unlike the ultimatum's own+other=const.
(Payoffs transcribed from the PDF; the paper writes allocations as (other, own).)

## Fit (Fehr-Schmidt, 232 choices)

`U_B(own,other) = own − α·max(other−own,0) − β·max(own−other,0)`, softmax choice.

| parameter | value |
|---|--:|
| α (envy, disadvantageous-inequality aversion) | **0.00** |
| β (guilt, advantageous-inequality aversion) | **0.34** |
| τ (choice temperature) | 0.7 |

- α ≈ 0: in these games, being *behind* triggers no aversion (e.g., Berk29 R=(own 400, other 750):
  69% take it over the equal split — they don't mind the other being ahead if total is higher).
- β = 0.34: people **pay to reduce advantageous inequality** — Berk29's 31% choose the equal (400,400)
  over (400,750) at no cost to themselves; the signature result. Consistent with Charness-Rabin's
  own social-welfare / difference-aversion conclusion.

## Q1 — the self↔other reflection and its breaking

A σ_s-symmetric (fair) agent weights own = other. Here own has weight 1 and the other enters only
through inequality aversion (effective other-weight ≈ 0.17). **Self-regard is the reflection-breaking**
— the social analog of loss aversion breaking the value reflection. The *reflection + aversion motif*
holds on real allocation data.

## Q2 — is the social domain a V₄, or main-effect inequality aversion?

**Main effect.** The position asymmetry α − β = −0.34 is significant: the α=β restriction
(position-symmetric, the V₄-consistent case) is rejected against the free fit, **LR χ² = 24.8,
p < 0.001**. The inequality attitude depends on position (ahead vs behind) as a **main effect**, not a
pure interaction. That is exactly what Fehr-Schmidt / Charness-Rabin predict, and exactly *not* the
pure-interaction (b_q≈0) signature that defined the risk V₄.

## Structural verdict — Track A, resolved with real data

The social domain has **one** reflection axis: self↔other. Swapping self and other *is* the
inequality-sign flip, so there is no *second, independent* social reflection — unlike risk's two
genuinely independent axes (value × probability). Social allocation is therefore **ℤ/2 (one reflection)
+ main-effect inequality aversion**, **not a V₄**.

So the honest, real-data conclusion:
- **The reflection + aversion motif generalizes** (self↔other broken by self-regard, mirroring
  value-reflection broken by loss aversion). This is real cross-domain structure.
- **The full V₄ does not** — it required risk's two independent axes; the social domain has one. And
  even within it, inequality aversion is a *main effect* (α≠β), not the pure interaction V₄ needs.

This completes Track A on real Charness-Rabin data and confirms the a-priori (Fehr-Schmidt) prediction:
the social domain is one reflection with main-effect inequality aversion — not a second V₄.

## Honest caveats

- 7 dictator games, n = 22–48 each (232 choices). Small; α is identified mainly off a few
  behind-positions, so "α ≈ 0" is "no envy *in these games*," not a universal claim.
- β > α (guilt > envy) is the reverse of standard Fehr-Schmidt magnitudes because *dictator* games
  mostly probe advantageous positions; it matches Charness-Rabin's own headline (costly reduction of
  advantageous inequality), so it is a feature of this dataset, not a contradiction.

*Data: Charness & Rabin (2002), QJE 117(3), Table I. Reproduce: `python move2b_charness.py`.*
