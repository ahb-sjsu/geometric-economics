# strata2: a probability reader for the stratified geometry. Development record

**This is development, not a test.** It was run 2026-10-31, after `prereg-strata-v1` was graded
(`../strata/RESULTS.md`). The five corpora it uses had already been read, so nothing here confirms
anything. A confirmatory test needs corpora this programme has not used.

## The problem

In `prereg-strata-v1`, H7 failed in the wrong direction. GDT-S builds its coordinates g, l, π⁺ and π⁻
linearly in probability, so it cannot distort a probability. In four of the five corpora, people
showed a stronger inverse-S than on CPC18.

## What was tried

The coordinates are rebuilt from rank-dependent decision weights W(c) inside each stratum (`readers.py`).
The strata boundaries stay exact: W(0) = 0 and W(1) = 1. Four readers were tried:

| Reader | W | Free parameters | Source |
|---|---|---|---|
| lin | c | 0 | GDT-S as registered |
| fr | (2/π) arcsin √c, the Fisher-Rao arc length on the Bernoulli family | 0 | |
| llo | logistic(γ logit c + δ) | 2 | Gonzalez and Wu 1999. Zhang, Ren and Maloney (PNAS 2020) bound and adapt it |
| eff | posterior-mean decode of an arcsine code set by each corpus's own prior, with capacity n | 1 | Frydman and Jin (NBER w31573). See also arXiv 2510.04698 |

Two variants of lin and llo also add one exponent on share magnitudes (`-pow`), for diminishing
sensitivity. CPT, as registered, is the yardstick.

## Protocol

Leave one corpus out (`explore_readers.py`). For each held-out corpus, the shared parameters are fit
jointly on CPC18 and the other four corpora. Each training set gets its own logit scale, and the corpora
are weighted equally. The held-out corpus then refits one scale on the registered calibration half and
is scored on the registered test half. The splits reproduce the registered ones exactly. CPT gets the
same protocol and chooses its coding on the calibration half.

## Result (`explore_readers.json`)

Pooled over the five held-out corpora: log-loss difference per choice in nats, 95% bootstrap interval
over problems.

| Comparison | Difference |
|---|---|
| llo minus lin | **−0.0117** [−0.0168, −0.0063] |
| fr minus lin | −0.0004 [−0.0060, +0.0058] |
| eff minus lin | +0.0003 [−0.0002, +0.0008] |
| lin-pow minus lin | −0.0078 [−0.0120, −0.0039] |
| llo-pow minus llo | −0.0019 [−0.0041, +0.0001] |
| lin minus CPT | +0.0287 [+0.0213, +0.0365] |
| llo minus CPT | +0.0169 [+0.0126, +0.0217] |
| llo-pow minus CPT | +0.0150 [+0.0110, +0.0194] |

Test log-loss by held-out corpus:

| Held out | lin | fr | llo | eff | llo-pow | CPT |
|---|---|---|---|---|---|---|
| Glöckner and Pachur 2012 | 0.6023 | 0.5861 | 0.5763 | 0.6026 | 0.5802 | 0.5560 |
| Pachur et al. 2017 | 0.6501 | 0.6425 | 0.6388 | 0.6500 | 0.6360 | 0.6305 |
| Pachur et al. 2018 | 0.5896 | 0.5912 | 0.5822 | 0.5909 | 0.5771 | 0.5413 |
| Zilker et al. 2020 | 0.5267 | 0.5221 | 0.4971 | 0.5265 | 0.4943 | 0.4871 |
| Babula 2018 | 0.6034 | 0.6285 | 0.6194 | 0.6036 | 0.6165 | 0.6141 |

## Reading

1. **A fitted log-odds reader is the probability fix.** It closes 41% of the leave-one-out gap to CPT.
   It learns nearly the same curve in every fold: γ ≈ 0.78 and W(0.5) ≈ 0.40, which over-weights
   0.01 (0.019) and under-weights mid and high probabilities. Babula 2018 alone is hurt by it, which
   matches its near-linear γ in the registered H7.
2. **Neither theory-native reader works.** The parameter-free Fisher-Rao reader helps in four corpora
   and hurts Babula, about zero pooled. The efficient code from each corpus's prior is never wanted:
   training pushed its capacity to the top of the grid in every fold, which reads probabilities exactly.
   So the corpus-to-corpus variation in distortion is still not predicted from the stimuli.
3. **Most of the remaining gap is not about probabilities.** Even with the reader and curvature, GDT-S
   stays 0.015 behind CPT, and it is worst on Pachur 2018, the mixed-gamble corpus. In every fold the
   fit drives the weights on π⁻ and on spread to nearly zero. Under joint training GDT-S also does
   worse on Pachur 2018 (0.590) than the version frozen on CPC18 alone did in the registered run (0.553),
   so its parameters are not stable across corpora. The next suspect is the cost itself: the
   menu-relative reference and the treatment of losses, not the reading of probabilities.
4. **Caveat.** A fitted LLO reader with rank-dependent weights is CPT's own probability ingredient. The
   fix moves GDT-S toward CPT rather than deriving the distortion from geometry.

## Round 2: where the rest of the gap is (`explore_readers_diag.json`, `explore_readers_ablate.json`)

Same corpora, same leave-one-out protocol. The variants all keep the LLO reader:

- `pow2` uses separate curvature exponents for gains and losses.
- `L1` and `Lq` replace the Euclidean cost with a Minkowski exponent:
  (Σ (√w_k |Δ_k|)^q)^(1/q), where q = 2 is GDT-S and q = 1 is additive. With two options under L1, the
  menu reference cancels, and the cost difference is linear in the coordinates.
- `nos`, `nobeta` and `core` switch off the spread term, the loss-boundary step β, and everything except
  w_g and w_l, respectively.

**The data choose an additive cost, not a Euclidean one.** The free exponent q fits to 1.03, 0.91,
0.85, 0.95 and 0.96 in the five folds. L1 beats L2 (−0.0026 [−0.0050, −0.0003]).

**The remaining gap is in mixed gambles.** Test log-loss by domain, pooled over held-out corpora:

| Domain | Choices | L1 | core | CPT |
|---|---|---|---|---|
| Gains only | 13,214 | 0.5616 | 0.5612 | 0.5593 |
| Losses only | 12,271 | 0.5184 | 0.5196 | 0.5206 |
| Mixed | 8,634 | 0.5938 | 0.5776 | 0.5667 |

**The stratified model's own coordinates hurt, and they hurt in mixed gambles.** Switching off the
extra coordinates helps:

| Ablation | Change in loss |
|---|---|
| β off | −0.0022 [−0.0030, −0.0015] |
| β, π⁺, π⁻ and spread all off (`core`) | −0.0083 [−0.0123, −0.0043] |

On Pachur 2018, all mixed gambles, `core` scores 0.5412 against CPT's 0.5414. Pooled, `core` trails CPT
by 0.0041 [0.0014, 0.0073]. All of that comes from Glöckner and Pachur 2012, where CPT chose the money
unit over the stake share (0.556 against 0.579, and `core` gets 0.577).

**What `core` is.** It is an additive value with rank- and sign-dependent LLO weights (γ ≈ 0.70–0.77),
power curvature (gains 0.72–0.75, losses 0.84–0.97), and loss aversion √(w_l/w_g) of 1.07–1.25, on
share-coded payoffs. That is cumulative prospect theory with an LLO weighting function. Once
probabilities are read correctly, every element that made the model geometric is either refused by
the data or costs accuracy out of corpus:

- the Euclidean norm,
- the menu-relative reference,
- the strata masses π⁺ and π⁻,
- the loss-boundary step,
- the spread term.

What survives from this programme is the share coding, which CPT also prefers in four of five corpora
and which H4 supported.

**Where geometry could still differ, untested here.** With three or more options, the menu reference
does not cancel even under L1. A menu-relative cost then predicts context effects (decoy, compromise)
that CPT cannot produce. Binary choice cannot tell the two apart, and every corpus here is binary.
