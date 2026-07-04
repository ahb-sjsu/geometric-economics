# Discriminating test — shared geometry vs the behavioral ensemble

Does the geometry beat a "bag of independent behavioral models," or is it a repackaging? Run on human
data (CPC18 lotteries + bogota games). **Honest, mixed verdict.**

## What does NOT discriminate them (stated plainly)

For the projection-gap **sign** contrasts, the diagonal-Σ geometry (one free `σ_k` per coordinate) is
**near-equivalent** to an ensemble with one free effect `β_k` per coordinate — same parameters, same
sign predictions. **The projection-gap does not discriminate the two.** It falsifies scalar
expected-utility (money-only), which is the weaker win. This corrects an earlier overstatement.

## Where the geometry DOES earn its keep: cross-domain transfer

| | lotteries | games | #params |
|---|--:|--:|---|
| Ensemble (2 disjoint specialists) — within-domain | 0.624 | 0.876 | 6 |
| Geometry (one shared metric) — within-domain | 0.627 | 0.914 | 3 |
| **price of sharing** | +0.003 | +0.038 | |

| Cross-domain transfer (fit one domain, predict the other, one model) | lot→games | games→lot |
|---|--:|--:|
| **Behavioral ensemble (CPT + game model)** | **chance** | **chance** |
| Geometry (shared, polar angle-lock) | 0.876 (**130%** of gap) | 0.627 (**101%**) |

The behavioral ensemble transfers at **chance by construction**: CPT has no game input and a game
model no lottery input. The shared geometry transfers at ~100% of a native fit **in both directions**,
at a **small within-domain price** (+0.003 / +0.038) and **half the parameters**.

## The honest limits

- **Parsimony (BIC) favors the ensemble**, not the geometry (53,616 vs 54,579). BIC rewards the
  specialists' slightly-better within-domain fit and is **blind to their transfer failure**. So the
  geometry does **not** win on a standard within-domain parsimony criterion — its advantage is
  entirely *cross-domain*.
- A skeptic can call the transfer win **definitional**: "a general model transfers, a specialized one
  doesn't — is that surprising?" The reply: it is not guaranteed that a *single, low-complexity* metric
  fits each domain nearly as well as its specialist **and** transfers. That conjunction (small price +
  real transfer + fewer params) is the non-trivial content — but it is a claim about *unification*,
  not about being a better within-domain predictor.

## Verdict (what the paper may honestly claim)

> The geometry is **not** a superior within-domain predictor, and a standard parsimony criterion
> favors the ensemble. Its genuine, defensible advantage is **cross-domain transfer/unification**: one
> shared metric spans risky and strategic choice — predicting each at a small cost and transferring
> between them — which no ensemble of domain-specialized behavioral models can do at any parameter
> count. Claim exactly that, and no more.

This matches the honest confidence assessment: the theory's real weight is *unification and transfer*,
not within-domain superiority. **The open path to a stronger claim** is a *constrained* Σ (a genuine
low-dimensional structure) that would earn a parsimony win the free-diagonal Σ does not — a target for
structural fuzzing scored on held-out transfer.

*Reproduce: `python ensemble_test.py`.*
