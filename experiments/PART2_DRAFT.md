# Part II — Out-of-Sample and Cross-Domain Validation of the Geometric Decision Model

*Companion / follow-up to the submitted TCSS paper ("Geometric Prediction of Economic Behavior:
Cross-Domain Validation Across Game Theory and Prospect Theory"). Part I established the model and an
in-sample benchmark (16 aggregate targets, MAE 2.70%). Part II answers the reviewer's central asks —
individual-level, held-out, common-protocol — on large public datasets, and tests the theory's
differentiating claim (one shared metric across domains) directly.*

## Thesis

Part I showed a 9-D geometric decision model can *fit* game-theoretic and prospect-theoretic targets
with one shared metric. The open question (from the reviewer, and from `nobel-program.md`): is that a
flexible representation, or a **predictive structure**? Part II makes three out-of-sample tests, each
against a competitor that cannot be beaten on aggregate curve-fitting alone.

## Contributions (each a self-contained empirical result already run)

**C1. Held-out individual risky choice (CPC18).** On the Choice Prediction Competition benchmark
(694k choices; 270 games; predict *unseen games*, 20-split CV), the geometric model beats Expected
Value and linear random-utility out-of-sample and comes within <1 sd of CPT **with one fewer
parameter** (held-out MAE: EV 0.149, RUM 0.128, **Geometric 0.124**, CPT 0.118). Claim: the
*domain-general* geometry is competitive with the *domain-specialised* champion on its home turf.
→ `datasets/RESULTS_cpc18.md`.

**C2. Cross-domain transfer (the differentiating result).** Encoding CPC18 lotteries and 110
published normal-form games (bogota datapool: Stahl, Costa-Gomes, Goeree-Holt, Cooper, Haruvy,
Camerer) into one (EV, SD) space, a metric **fit only on risky choice predicts strategic game play**
at NLL 0.931 vs chance 1.040 — closing **66% of the chance→native gap on games it never saw.**
Neither CPT (no games) nor Nash (no lotteries) can do this. Honest asymmetry: games→lotteries transfer
fails (worse than chance), and a level-k belief does **not** help (the naive level-0 encoding is best,
consistent with the level-0-models literature). → `datasets/RESULTS_cross_domain.md`.

**C3. A designed falsification test on a model-organism population (LLM projection-gap).** A
pre-registered (hashed, `prereg-v1`) experiment constructs matched decision pairs *identical under
every scalar projection* (EU/Nash/Fehr-Schmidt/CPT) that differ only on one active non-monetary
coordinate — so the entire scalar class is *forced* to predict Δ=0 while the frozen metric predicts a
signed gap. Run on an NRP LLM panel (individual-level, thousands of synthetic subjects): [full
six-model verdict pending; interim: placebo-corrected, cross-domain signal on identity/epistemic
coordinates, loss-domain reversal recovered]. LLMs as decisive testbed + powered pre-registration for
a human study. → `projection-gap/`.

**C4. Validation apparatus (retrodiction + forward prediction).** A historical ledger of natural
experiments where scalar economics predicts the *wrong sign* and the geometry predicts the observed
direction (crowding-out: Titmuss, Gneezy-Rustichini, Frey-Oberholzer-Gee — which *is* the Part I
money-dimension corollary in the wild; plus legitimacy, bank-runs, identity-framing), and a
hashed forward-prediction registry that later history can verify. → `historical-ledger/`, `forward-registry/`.

## What Part II does NOT claim (kept honest)

- Not that the geometry beats CPT on lotteries (it doesn't; it ties with one fewer param).
- Not a symmetric shared metric (transfer is one-directional; reported as such).
- Not that magnitudes are calibrated (signs are; the cost-dependent temperature under-predicts
  effect sizes — a Part-III target, and the same issue the Part I reviewer flagged).
- Not the human economics claim yet — C3 is a model-organism result that powers the human study.

## Suggested structure

1. Introduction — from in-sample fit (Part I) to out-of-sample/cross-domain prediction; the
   representation-vs-structure question; the reviewer's asks as the agenda.
2. Model recap (frozen from Part I; no re-fit).
3. C1 CPC18 held-out prediction, common protocol vs CPT/RUM/EV.
4. C2 cross-domain transfer, the shared-metric test; belief-model robustness; honest asymmetry.
5. C3 the projection-gap design + LLM-panel result; pre-registration; human-study protocol.
6. C4 historical + forward validation.
7. Limits and Part III (temperature/magnitude calibration; social-preference games; the human study).

## Venue

Part I is at IEEE TCSS. Part II fits: a decision-theory/behavioural venue (Judgment and Decision
Making; Decision; Games and Economic Behavior for C1–C2), or a computational-social-science venue
(TCSS again, or CSS journals) given the LLM-panel and reproducibility apparatus. C2 alone (cross-domain
transfer, novel) could anchor a standalone short paper.

## Status of the artifacts (all runnable, in this repo)

- C1 `datasets/cpc18.py`, `fit_transfer.py`, `RESULTS_cpc18.md` — done.
- C2 `datasets/bogota_games.py`, `cross_domain.py`, `RESULTS_cross_domain.md` — done.
- C3 `projection-gap/` (prereg-v1) + `llm-panel` — panel running; verdict pending.
- C4 `historical-ledger/`, `forward-registry/` — done.
