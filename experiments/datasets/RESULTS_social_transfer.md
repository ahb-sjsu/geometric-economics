# Move 2c — integrating Engelmann-Strobel + FKM; the social-transfer test is underpowered

Goal: the social analog of the cross-domain-transfer pillar — does *one* social preference direction
span 2-person and 3-person allocations, recalibrating only a scalar magnitude (the polar shape/scale
split)? Integrated **Charness-Rabin (2002)** 7 two-person dictator games + **Engelmann-Strobel (2004)**
3-person dictator choices. Identified multinomial logit over features [own, disadv, adv, other_mean,
minpay], payoffs normalized per dataset.

## What each dataset says (both confirm known features)

- **Charness-Rabin (2-person):** advantageous-inequality aversion / guilt drives it — β = 0.34
  (Move 2b), matching the Nunnari-Pozzi meta-analytic dictator β = 0.39.
- **Engelmann-Strobel (3-person):** the shared fit puts the **largest weight on minpay (maximin), +0.84**
  — people help the worst-off third player. This reproduces Engelmann-Strobel's own headline (efficiency
  + maximin dominate pure difference-aversion; 77% chose the efficient+maximin option A).

So each dataset independently confirms its established social-preference feature.

## The transfer test — underpowered, not a clean answer

- cos(shape_CR, shape_ES) = **−0.05**; transfer CR→ES 100% / ES→CR 0% (asymmetric).

**This is not a real "directions are orthogonal" finding — it is underpowered.** With **7 + 2 games**
and a 5-dimensional preference direction, each dataset's fitted direction is heavily overfit, so a
near-zero cosine is exactly what noise produces. The combined sample cannot robustly identify — let
alone transfer — a shared social metric. Honest verdict: **the social analog of the transfer pillar is
not testable at this sample size.**

## FKM — data gated, structure corroborates the thesis

**Fisman-Kariv-Markovits (2007)** is the right dataset for a powered version (graphical dictator with
budget lines over (own, other), rich individual-level data, plus 3-person budgets). Its replication
data is on **OpenICPSR (project 116294)** behind registration — not fetchable in this environment. From
the surveys we do have its structure and aggregate results, which corroborate the thesis (recorded in
`EVIDENCE.md`): preferences are **CES over (own, other)**, ~90% of subjects are **GARP-consistent**
(utility-maximizing — supports the geometric/utility view), and the type distribution is
low-dimensional (~47% selfish; egalitarian/intermediate/near-selfish splits). What FKM would add over
the aggregate stats is a *powered* shape/scale transfer test across 2- and 3-person budgets.

## Honest status

- **Engelmann-Strobel: integrated.** Confirms maximin/efficiency dominance in 3-person allocation.
- **Shared-metric social transfer: underpowered** (9 games). Needs individual-level data.
- **FKM: gated** (OpenICPSR login); its CES + GARP + type structure corroborate the low-dimensional and
  geometric claims but do not give a fittable choice matrix here.

The powered social-transfer test — the social analog of the cross-domain-transfer pillar — remains open
and requires the FKM or Bruhin individual data. The reflection-motif result (Move 2b, real Charness-
Rabin data, β matched to meta) stands; this transfer extension does not reach significance.

*Reproduce: `python move2c_social_transfer.py`.*
