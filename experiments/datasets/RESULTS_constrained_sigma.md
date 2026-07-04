# Constrained-Σ structural fuzz — the decision metric is effectively low-rank

Searching Σ⁻¹ structures (geometric-methods-inspired) scored on **held-out cross-domain transfer +
parsimony (BIC)**, across CPC18 + choices13k (1,770 lotteries) and bogota (110 games), K=5 features
(EV, SD, skew, worst, p-favorable). The question the ensemble test left open: is there a *constrained*
Σ that beats the free-diagonal on parsimony *and* transfers?

## Result

| structure | #params | lot native | gm native | lot→gm | gm→lot | pooled BIC | transfer% |
|---|--:|--:|--:|--:|--:|--:|--:|
| isotropic | 2 | 0.685 | 1.040 | 1.040 | 0.685 | 94,100 | 50% |
| **diagonal** | 6 | 0.660 | 0.928 | 0.944 | 0.663 | 89,131 | 89% |
| **rank-1** | 6 | **0.636** | **0.873** | 0.883 | 0.644 | 85,440 | **90%** |
| rank-2 | 11 | 0.634 | 0.867 | 0.878 | 0.650 | **85,165** | 83% |
| banded | 10 | 0.637 | 0.873 | 0.881 | 0.639 | 85,575 | **96%** |
| block | 10 | 0.637 | 0.870 | 0.886 | 0.643 | 85,532 | 90% |
| lowrank+diag | 16 | 0.635 | 0.874 | 0.882 | 0.645 | 85,494 | 89% |
| full | 16 | 0.634 | 0.867 | 0.878 | 0.644 | 85,237 | 88% |

## The finding

**A rank-1 precision matrix (6 params) matches the full metric (16 params) on within-domain fit and
beats it on transfer.** rank-1: lot 0.636 / games 0.873 / 90% transfer, vs full: 0.634 / 0.867 / 88% —
at **10 fewer parameters.** The decision cost is **effectively low-rank**: the 5 features collapse to
essentially *one dominant direction of "goodness,"* and adding higher-rank structure barely helps
(rank-2 → full move the needle < 0.01 NLL).

Two consequences that matter for the theory:

1. **The parsimony win the diagonal Σ lacked — recovered.** A rank-1 Σ gets *full-metric performance at
   diagonal-parameter-count* **and** transfers cross-domain (which the behavioral ensemble cannot do at
   any parameter count). So the honest ensemble verdict updates: with a *low-rank* Σ (not the free
   diagonal), the geometry earns a parsimony *and* transfer advantage.
2. **The diagonal default is not the best structure.** At the *same* 6 parameters, **rank-1 beats
   diagonal** on both fit (0.636 vs 0.660) and transfer — because the off-diagonal correlations it
   captures are real (this supports the TCSS reviewer's "diagonal is convenient but severe"). And
   banded (local coupling) transfers best of all (96%). Interactions are real, but **low-rank** — so
   they cost few parameters.

## Honest caveats (the discipline)

- The **winner is a hypothesis, not a result.** It was selected on transfer across two domains; it must
  be **pre-registered and re-tested** on held-out domains/datasets before it enters the theory. Scored
  on out-of-sample transfer (not in-sample fit), whole table reported — but that is not a substitute
  for confirmation.
- **BIC still slightly favors rank-2/full** within-domain (85,165 / 85,237 vs rank-1's 85,440) — the
  transfer favors rank-1/banded, the pure within-domain parsimony favors rank-2. The differences are
  small (~0.3%); the robust statement is "**low-rank (1–2) is the sweet spot; full is unnecessary,
  diagonal is suboptimal.**"
- Two domains, one belief model for games (uniform), K=5 hand-chosen features. A cleaner test adds more
  domains (the social-preference games; cross-lingual data) and CV.

## Takeaway for the program

The theory should **replace the diagonal Σ with a low-rank (rank-1 or rank-2) Σ**: it fits as well as
the full metric, uses ~diagonal parameter count, transfers cross-domain, and captures the real (but
low-rank) attribute interactions the diagonal misses. This is a concrete, fuzzing-discovered structural
improvement — to be frozen as `prereg` and re-tested, per the discipline.

*Reproduce: `python constrained_sigma_fuzz.py --workers N` (needs CPC18 + choices13k + bogota in raw/).*
