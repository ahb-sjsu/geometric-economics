# Pre-registration: cross-domain angle coupling (the discovery gate)

*Frozen before the confirming data are in hand. This is the "novel quantitative prediction" gate — a
prediction that is NOT a re-description of a known regularity and that a named incumbent forces to a
different value. Registered here; confirmation requires same-subject risk+social choice data (below).*

## The prediction (GDT)

Geometric Decision Theory says one low-rank metric Σ governs both risky and social choice. A sharp
individual-level consequence: fit the geometric **aversion angle** θ_risk from a person's *lottery*
choices (Section III risk encoding) and the **other-regard angle** θ_social from that same person's
*allocation/giving* choices (Section III, Result 4 social encoding). Because both are projections of one
metric, GDT predicts:

- **P1 (sign).** θ_risk and θ_social are **positively coupled** across individuals: people whose metric
  weights dispersion more in lotteries also weight the other's shortfall more in giving. Signed,
  pre-committed.
- **P2 (rank).** The joint coupling is **rank-1**: a single latent metric factor explains the
  risk↔social association (partialling it out removes the cross-domain correlation). This is the
  individual-domain image of the Pillar-1 low-rank result — and is the part that goes *beyond* the known
  "preferences are somewhat correlated" regularity.
- **P3 (encoding-invariance).** The sign of P1 is invariant to monotone re-encoding of the social
  coordinate (Theorem 2, dominance case), so it is not a coding artifact.

## The incumbent contrast (why this is not free)

CPT (risk) and Fehr–Schmidt / CES giving (social) are **separate models with no shared parameter**.
Calibrated independently, they place **no constraint** on the cross-domain association: the incumbent
prediction for corr(θ_risk, θ_social) is **zero** (an unmodeled, free quantity). GDT predicts a
specific, positive, rank-1 coupling. The gap between "zero, unconstrained" and "positive, rank-1" is the
test.

## Falsifiers (pre-committed)

- P1 fails if same-subject θ_risk, θ_social are **uncorrelated** (|r| < 0.10, n.s.) or negatively
  correlated → the shared-metric claim is false at the individual level.
- P2 fails if the coupling is **full-rank** (multiple independent factors needed) → the low-rank claim
  does not extend to the individual cross-domain structure; the coupling would then be a generic
  "preferences correlate" regularity, not the GDT prediction.
- P3 fails if a monotone re-encoding of the social coordinate flips the sign of P1.

## Honest novelty boundary

That risk and social preferences *correlate at all* is a known regularity (e.g., general-factor and
GPS preference-correlation results). The **novel** content pre-registered here is not the existence of a
correlation but its **structure**: (a) a *geometric angle fit from choices* in one domain predicts the
*angle fit from choices* in the other at the individual level (never done as a same-subject
angle-to-angle test), and (b) the coupling is **rank-1**, tying it to the same low-rank Σ as Pillar 1.
Only (a)+(b) count as confirming GDT; a bare nonzero correlation does not.

## Data required to confirm (why this is registered, not yet confirmed)

Needs **same-subject choice data in both a risky-choice task and a social-allocation task**. Candidates:

- **Global Preferences Survey** (Falk et al.) — same-subject risk + altruism + trust, 76 countries.
  Registration-gated; not on disk.
- **Bruhin–Fehr–Schunk (2019)** individual data — social types; pair with a risk task if the same
  cohort has one. Supplement access.
- A purpose-run joint task (risk block + giving block) — the cheapest bespoke option.

None is currently reachable in this environment (GPS is login-gated). This prediction is therefore
**frozen and hashed now**, to be scored when such data are obtained — the same discipline as the human
projection-gap gate.

## Freeze

Compute and record the hash of this file at freeze time:

    sha256sum PREREG_cross_domain_coupling.md   # tag: prereg-coupling-v1

No line above may change without breaking the hash.
