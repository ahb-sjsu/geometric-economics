# `prereg-coupling-v1` — scorecard (scored on GPS, the frozen prediction's confirming data)

**Frozen prediction:** `PREREG_cross_domain_coupling.md`, sha256 `1eac580f…` (verified unchanged at
score time). **Scorer:** `datasets/gps_coupling.py`, committed `38b0308` before the data were opened.
**Data:** Global Preferences Survey (Falk et al. 2018 QJE), obtained 2026-07; individual-level
(80,337 rows; 76,752 with all six preferences) and country-level (76 countries).

## Verdict: the strong coupling prediction is FALSIFIED on the GPS proxy.

| test | prediction (GDT) | individual-level (n=76,752) | country-level (n=76) | result |
|------|------------------|------------------------------|----------------------|--------|
| **P1 sign** | risk↔social **positive**, coupling ≥ 0.10 | risk–altruism **+0.086**, –trust +0.040, –posrecip +0.033 (all p<1e-19) | mean **−0.025** (posrecip −0.168) | **FAIL** — positive & significant at individual level but **all r < 0.10** (below the pre-committed magnitude); sign flips at country level |
| **P2 rank** | **rank-1** (one latent metric factor) | PC1 **27%**, PC1+PC2 49%, λ1/λ2 **1.24** | PC1 33%, PC1+PC2 60%, λ1/λ2 1.26 | **FAIL** — not rank-1, not even low-rank; multiple independent factors |
| **P3 invariance** | sign invariant to monotone re-encode | (not reached — P1/P2 fail first) | — | n/a |

**What the data show instead.** The six preferences form **two coherent bundles**, exactly as Falk
et al. report and as the scorer pre-warned would falsify P1/P2: a self-regarding/risk cluster
(risk–patience +0.30) and an other-regarding cluster (altruism–posrecip **+0.72**, posrecip–trust
+0.40, altruism–trust +0.27). Risk sits *outside* the social bundle, weakly (individual) or negatively
(country) related to it — not the single low-rank metric GDT's one-Σ claim requires.

**Against the pre-committed novelty boundary.** The prereg stated that only (a) a same-subject
angle-to-angle coupling **and** (b) **rank-1** structure count as confirming GDT; a bare nonzero
correlation does not. (b) fails decisively. The weak, significant, positive individual-level
correlations are precisely the "bare nonzero correlation" the prereg excluded in advance. So this does
**not** confirm GDT and, on P2, actively falsifies the distinctive rank-1 claim. On this proxy the
incumbent (separate CPT + inequality-aversion, zero coupling) is closer to the data than GDT's
positive-rank-1 prediction.

## Honest caveats (pre-committed in the prereg and scorer, not post-hoc)
1. **Proxy, not the gold standard.** GPS ships survey/experimental preference *scores*, not the
   choice-fit geometric *angles* θ_risk, θ_social of the paper's own encodings. The same-subject
   **angle-to-angle** test (fit θ_risk from a person's lottery choices, θ_social from that person's
   giving choices) remains unrun and is the only test that can *confirm* GDT here; it could differ.
   A bespoke joint risk+giving task, or Bruhin–Fehr–Schunk individual social types paired with a risk
   task, is the route.
2. **A faint directional echo.** The individual-level risk↔social sign is correct (positive, hugely
   significant) — but at r≈0.03–0.09 it is an order of magnitude below a "shared-metric" coupling and
   below the pre-committed 0.10. Sign-consistent, magnitude- and rank-inconsistent.
3. **Scorer level-label bug (cosmetic).** The frozen scorer prefers the country-level file and
   mislabels it "individual-level" in its printout (it checks for "Country" with a capital C; the file
   is `country.dta`). The computation is correct country-level; the individual-level numbers above were
   computed separately on `individual_new.dta`. Recorded, not edited (the scorer is frozen).

## Program consequence
The **cross-domain coupling gate** — a pre-registered Tier-A "novel quantitative prediction" — **fails
on the GPS proxy** (P2 decisively; P1 by magnitude). It joins the graveyard alongside the killed
universal-angle / Shannon / D₄ / V₄-generality overclaims. The surviving GDT pillars are unaffected
(low-rank Σ `prereg-sigma-v1`; encoding-invariant projection-gap): those are *within-domain* results
and do not depend on the individual *cross-domain* coupling, which this proxy finds is not rank-1.
The gold-standard angle-to-angle test is the outstanding way to revisit the coupling claim.
