# Part II, as a case file

*An alternative expository structure for the companion paper — the same rigorous results
(`PART2_DRAFT.md`), told as the investigation they actually were. The narrative is honest only because
each turn is guarded: pre-registration (`prereg-v1`), held-out CV, common protocols, and stated
falsifiers. Following clues is science, not story, precisely when the guards are fixed in advance.*

## The question (the crime)
Part I fit games and lotteries with one geometric metric. But a high-dimensional model can fit
anything — is the geometry a **real predictive structure**, or an elaborate alibi? To convict, it must
predict what it was never shown, where the usual suspects (EU, Nash, CPT) *can't*.

## Clue 1 — the individual-level line-up (CPC18)
Take it out of the aggregate and put it in a proper line-up: 694k individual choices, predict *unseen
games*. The geometry beats EV and random-utility out of sample and comes within a hair of CPT — **with
one fewer parameter.** A strong lead, but not a conviction: on lotteries, CPT has the better alibi.
*Guard: held-out by game, 20-split CV, common likelihood.*

## Clue 2 — the thing CPT and Nash can't do (cross-domain)
CPT can't play games; Nash can't do lotteries. So ask the one question that separates a shared metric
from a coincidence: **calibrate on risky choice, predict strategic games, no refit.** It works one
way — 66% of the way to a native fit on games it never saw — but the reverse direction fails, *worse
than chance.* A partial print. Something is off. *Guard: no refit; multinomial NLL vs chance.*

## Clue 3 — the false suspect (level-k)
The obvious suspect: the agents must be reasoning strategically, so a smarter belief model (level-k)
should tighten the case. We haul it in — and it has an alibi. Level-k makes the fit **worse**; the
naive level-0 encoding predicts better. (The literature already knew this witness: non-strategic
features carry the signal.) Suspect released. The strategic-sophistication theory didn't do it.

## Clue 4 — the break, from the wrong department (PolarQuant)
The lead comes from a KV-cache compression method. PolarQuant splits a vector into *magnitude* and
*direction* because the direction is scale-invariant. Look again at the cost: it's a radius times an
angle set by the ratio σ_ev:σ_sd — the **aversion angle**. Transfer *only the angle*, let the scale
recalibrate, and the asymmetry **dissolves**: both directions transfer at ~97–100% of native, and the
angles are nearly equal across domains. **The risk-return tradeoff shape is shared; only the stakes
differ.** That's the conviction — a shared *structure*, not a shared *number*.

## The suspect still at large — the temperature
One thread runs through every scene: the geometry gets the **sign** right and the **magnitude** wrong
(the LLM panel is ~5× more sensitive than the frozen temperature allows; CPC magnitudes need refit).
The cost-dependent temperature — the same component the Part I reviewer eyed — keeps turning up at the
scene. It is the open case for Part III.

## The trap we set (the projection-gap, running)
Meanwhile we've laid a trap the culprit can't avoid: matched decisions *identical under every scalar
projection*, so the whole suspect class is **forced** to predict "no difference," while the geometry
predicts a signed gap — pre-registered and hashed before a single subject. On the model-organism
population the trap is springing (identity/epistemic gaps, the loss-domain reversal recovered under the
placebo control). The final chapter — the six-model verdict — is still developing on the wire.

## Why the case holds up
A detective story is only admissible if the detective couldn't have known the ending: the predictions
were **frozen and hashed first**, the tests were **held out**, the competitors judged under a **common
protocol**, and every dead end (games→lotteries, level-k, magnitude) is **in the report, not buried.**
That is the difference between following the clues and planting them.

---
*Structure only; the results and their caveats live in `PART2_DRAFT.md`, `datasets/RESULTS_*.md`,
`projection-gap/`, `historical-ledger/`, and `forward-registry/`.*
