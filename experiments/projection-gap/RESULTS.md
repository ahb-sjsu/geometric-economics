# Projection-gap — full six-model verdict

Pre-registered (`prereg-v1`, sha256 `123c5f4f…`, frozen before any data). NRP LLM panel:
**216 subjects** (36 personas × 6 models: gemma-small, qwen3-small, gemma, gpt-oss, glm-5, qwen3),
**83,682 valid forced choices (99.3% parse)**, AIMD controller held 0% policy violations.

## The core claim HOLDS (decisively)

Placebo-corrected (each subject minus their own domain-matched wording placebo), FDR-controlled:

| Contrast | Coordinate / domain | Δ corrected | Cohen d | FDR | **cross-model** |
|---|---|--:|--:|:--:|:--:|
| A3.1 | Epistemic (game) | **+0.456** | 0.91 | ✓ | **6/6** |
| A1.2 | Social Impact (game) | **+0.323** | 0.81 | ✓ | **6/6** |
| A2.1 | Virtue/Identity (game) | **+0.248** | 0.64 | ✓ | **6/6** |
| B1.1 | Epistemic (lottery) | **+0.172** | 0.52 | ✓ | **6/6** |
| A1.1 | Social Impact (game) | **+0.167** | 0.56 | ✓ | **6/6** |

**5/7 real contrasts are FDR-significant with the predicted sign, placebo-corrected, cross-domain
(4 game + 1 lottery), with perfect 6/6 cross-model consistency across the entire capability ladder.**
Manipulations *invisible to every scalar theory* (EU/Nash/Fehr-Schmidt/CPT are forced to predict Δ=0)
move choices in the frozen metric's predicted direction — robustly, in every model. **Placebos are
null at full power** (P.A1 p=0.66; P.B1 |Δ|=0.027): the interim placebo leak was small-N noise. H2
(cross-domain) and the placebo control both pass.

**Not capability-gated.** The effect is present in all six models including the weakest (gemma-small),
6/6 on all five confirmed contrasts. The "*only very advanced models show it*" hypothesis is **not**
supported — the projection-gap is universal across the ladder, not emergent with capability.

## The pre-registered falsifiers that FIRED (reported, not buried)

1. **Loss-domain d₉ reversal — FALSIFIED.** B1L.1 predicted a sign flip (−0.089); observed **+0.085**
   (same sign as the gain frame), and only **1/6** models reversed. The sharp loss-flip prediction does
   not hold for LLM subjects. (The interim gemma-small hint was a low-power artifact.)
2. **Social-impact-in-lottery (B2.1) — null** after correction (−0.006, n.s.). The social-impact
   manipulation works in games but not the lottery frame: a coordinate×domain interaction.
3. **Dose-response — monotone, not the predicted peak.** The frozen cost-dependent temperature
   predicted an inverted-U peaking at level 2 (cost-gap≈1.4); observed a **monotone-increasing** curve
   (peak at level 4). The temperature-induced washout is **not** seen.
4. **Magnitudes — ~5× under-predicted.** Signs are right; sizes are far larger than the frozen model
   allows (A3.1 +0.456 observed vs +0.089 predicted). H3 (magnitude coverage) fails 0/7.

## The suspect, caught

Falsifiers 3 and 4 are the same culprit: **the cost-dependent temperature architecture.** Two
independent pre-registered tests — the dose *shape* and the effect *magnitude* — both reject it, in the
same direction (it over-damps: predicts washout and small effects; reality is monotone and large).
This is the identical component the Part I TCSS reviewer flagged and the CPC18 magnitude result
implicated. **Part III's target is now unambiguous: replace the temperature architecture.** The core
geometry (which coordinates matter, their signs, cross-domain, cross-model) survives; the *choice-rule
scaling* does not.

## Honest status

This is the **model-organism** result: a decisive existence proof that the frozen geometric metric
predicts, out of sample, projection-defying choices that the entire scalar-theory class cannot — across
216 synthetic subjects and 6 models — with placebos controlled and the failures stated. It is
**necessary, not sufficient**, for the economics claim: the confirmatory leg is the **human
replication**, which this powered, pre-registered design now sizes (effect sizes d≈0.5–0.9 on the
five confirmed contrasts). The two clean falsifiers (loss-flip, temperature) sharpen the theory rather
than sink it.

*Data: `results_full.jsonl` (gitignored). Analysis: `analyze.py --results results_full.jsonl`
→ `results_full_analysis.json`. Predictions frozen at `prereg-v1`.*
