# Pre-registration — the reflection encoding (`prereg-reflection-v1`)

The reflection fuzz + polar encoding (`RESULTS_reflection.md`) *discovered*, on Ruggeri, that the
loss domain is the gain domain reflected across the value axis: one shared low-rank metric plus a
reflection transform reaches the two-model ceiling (99% of the raw→two-model gap). That was a
search/fit on Ruggeri — a **hypothesis**. This freezes it before a held-out re-test.

## The frozen hypothesis

> Under losses, the decision reference reflects across the value axis. Specifically, applying a
> per-coordinate reflection `ρ` to the loss-domain features {SD, worst, p-fav}, with **one** shared
> rank-2 metric and temperature fit jointly on gains + losses:
> **(R1)** the polar (one-metric + reflection) model reaches **≥ 90%** of the raw→two-model-ceiling
>   gap on a **held-out loss corpus** (one metric spans both domains);
> **(R2)** the SD reflection coefficient is negative — **ρ[SD] ∈ [−1, −0.5]** — a (partial) mirror,
>   the loss-aversion asymmetry keeping it above a full −1;
> **(R3)** discrete-flip gain→loss transfer with the {SD, worst, pfav} ideal-flip is **≥ 50%** on the
>   held-out corpus (vs ~0% for the raw ideal).

## Falsifiers

- R1 fails if the single reflected metric closes < 90% of the gap out-of-sample → reflection is not
  one geometric mirror; the domains need separate metrics.
- R2 fails if ρ[SD] is not a partial mirror (≥ 0, or a full −1 with no loss-aversion offset).
- R3 fails if the discrete ideal-flip does not transfer on held-out data → the Ruggeri flip overfit.

## Held-out re-test plan

The confirmatory corpus is the **loss and mixed gambles in CPC18 / choices13k** (a different lottery
source than Ruggeri's 17 KT items). Freeze the analysis to `reflection_fuzz.py` (discrete) and
`polar_reflection.py` (continuous), rank-2 metric, applied to that corpus, scored against R1–R3.

## Provenance (Ruggeri discovery values — NOT the confirmatory test)

- Discrete: {SD,worst,pfav} ideal-flip → gain→loss 80%, loss→gain 84% (raw 0%).
- Polar: pooled NLL 0.5936 (one metric) vs 0.5931 (two-model ceiling) → 99% gap closed;
  ρ[SD]=−0.80, ρ[worst]=+2.96, ρ[pfav]=+0.21.
- Frozen at tag `prereg-reflection-v1`.
