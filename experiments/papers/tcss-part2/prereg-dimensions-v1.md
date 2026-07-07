# prereg-dimensions-v1 — Protocol for Activating and Pricing the Nine Coordinates of the Economic Decision Manifold

**Status:** READY TO FREEZE (Level 1) — pending author sign-off on §5.0 signs and `codebook-v1.md`.
All `[AUTHOR TODO]`/`[MODEL]`/`[VERIFY]` placeholders resolved (codebook §4→`codebook-v1.md`; signs
§5.0; datasets §14; power §9.1). Nothing is a registered claim until §12 is executed.
**Companion to:** Geometric Prediction of Economic Behavior I & II; registrations `prereg-v1`, `prereg-v2`, `prereg-sigma-v1`, `prereg-coupling-v1`.
**Author:** Andrew H. Bond, San José State University.
**Version:** v1-rc1 (release candidate for freeze).
**Freezing procedure:** see §12. Nothing in this document is a registered claim until §12 is executed.

> **Two global caveats, stated before anything else.**
> 1. **Sign predictions come from the frozen model, not from intuition.** Every sign in §5.0 is *derived*, not asserted: it follows mechanically from (a) the bipolar codebook orientation (`codebook-v1.md`), which fixes, once, which pole of each coordinate is "aligned," and (b) the frozen GDT cost convention already pre-committed and panel-confirmed in `projection-gap/contrasts.py` — making a value salient raises the cost of the option that *violates* it. For the four coordinates fitted on the panel (d6, d7, d9) the sign is the frozen fitted sign; for the dormant four (d2, d4, d5, d8) it is the same convention applied to their codebook orientation. Theorem 2 (Part II) makes every sign invariant to monotone re-encoding, so the orientation is the only modeling choice and it is frozen here. No sign may change after hashing; a wrong sign is a reported failure.
> 2. **All dataset locations, DOIs, and access terms must be re-verified at execution time.** Repositories move and terms change; entries below marked `[VERIFY]` are from memory and were not confirmed at drafting time. A dataset that turns out to be unavailable triggers the substitution rule in §11, not a silent swap.

---

## 1. Background and aims

Part I introduced a nine-dimensional decision manifold **E** with coordinates
d1 money, d2 rights, d3 fairness, d4 autonomy, d5 privacy/trust, d6 social impact, d7 virtue/identity, d8 legitimacy, d9 epistemic status,
evaluated by a Mahalanobis cost metric Σ with a softmax choice rule. Part II established (i) held-out competitiveness on CPC18, (ii) angle-locked cross-domain transfer of the risk and social coordinates, (iii) a pre-registered low-rank Σ, (iv) a projection-gap positive on a language-model panel activating **d6, d7, d9**, and (v) a repaired fixed-temperature (information-price) choice rule.

**The open ontological question this protocol addresses:** four coordinates (d2, d4, d5, d8) have never been activated in any test, no coordinate has a calibrated scale, and the scenario→coordinate encoder has no measured reliability. This protocol converts the nine-dimensional commitment from *asserted* to *earned* — or revises it.

**Aims.**
- **A0 (Encoder):** show the scenario→Δ**a** mapping is measurable (inter-encoder reliability).
- **A1 (Activation):** for each coordinate d_k, show behavior varies with d_k when all other coordinates, including money, are matched.
- **A2 (Scale):** estimate each coordinate's exchange rate against money (σ1 : σ_k, reported as a dollar price per unit move on d_k) with uncertainty, per dataset.
- **A3 (Stability):** test whether exchange rates agree across independent datasets — the strong form of "predictive structure."
- **A4 (Structure):** test whether the rank-1/rank-2 result survives with all coordinates active, and whether Phase-1 exchange rates reproduce as the low-rank loadings.
- **A5 (Completeness):** attempt to construct scenarios that escape the nine-coordinate basis.

**What would count as failure, welcomed in advance:** a coordinate that cannot be activated (candidate for deletion); a coordinate that refuses monetary pricing (candidate lexicographic coordinate, expected for d2); an encoder that is unreliable for a coordinate (the coordinate is not currently measurable); a residual in Phase 4 (a missing axis). Each failure mode has a named decision rule (§9).

---

## 2. Definitions and conventions

- **Numeraire.** d1 (money) is the numeraire. All scales are expressed as the dollar amount Δd1 that offsets a one-unit move on d_k at the choice margin.
- **Per-paradigm subspace fits.** Following Part II's social-coordinate methodology, each Phase-1 estimate restricts the metric to the 2-D subspace (d1, d_k), fits the scale-invariant tradeoff angle σ1 : σ_k with the ridge regularizer (σ ≥ 0.05) and the **fixed-temperature information-price rule of Part II §VI** (not the deprecated cost-dependent rule), and recalibrates only the one-parameter magnitude per dataset.
- **Price.** p_k = the fitted marginal rate of substitution in dollars per unit of d_k, derived from the fitted angle; report with bootstrap 95% CI (resampling subjects where subject identifiers exist, choices otherwise; the resampling unit is fixed per dataset in §6 and may not be changed post hoc).
- **Unit of d_k.** Each dimension's unit is defined by its codebook anchor scenarios (§4). Units are ordinal-anchored interval scales; Theorem 2 of Part II (sign invariance under monotone re-encoding) is the protection against unit arbitrariness for all sign-level claims.
- **Activation.** d_k is *active* in a dataset if the projection-gap contrast on d_k (matched on all other coordinates) rejects Δ = 0 at FDR-corrected q < .05 with the sign frozen in §5, or, for observational datasets, if the (d1, d_k) fit beats the d1-only nested model on held-out folds (paired-fold comparison, pre-specified margin ΔNLL ≥ 0.01 per choice).
- **Statistical conventions.** All CV comparisons are paired per fold. All multiple-comparison corrections are Benjamini–Hochberg within the family stated in each hypothesis. LLM-panel statistics use the model as the primary independent unit (sign counts across models), with persona-level effects descriptive only, per the Part II revision.

---

## 3. Phase 0 — Encoder reliability (gate for all subsequent phases)

**Design.** Assemble a 200-scenario corpus: 20 scenarios per dimension deliberately loading that dimension + 20 designed to be multi-dimensional, drawn evenly from the Phase-1 datasets' stimuli and from novel drafting. Encoders: **N ≥ 3 human coders** (blind to hypotheses, trained only on the codebook) and **N ≥ 3 LLM encoders** (distinct model families, frozen prompts included in the registration bundle). Each encoder produces the full Δ**a** ∈ R⁹ for every scenario.

**Measures.** Krippendorff's α (interval) per dimension, computed separately for (a) humans only, (b) LLMs only, (c) pooled; plus human–LLM ICC(2,1) per dimension.

**Hypotheses.**
- **H0.1:** α ≥ 0.667 per dimension (human coders).
- **H0.2:** human–LLM ICC ≥ 0.6 per dimension (LLM encoders are admissible substitutes at scale only for dimensions passing this).

**Decision rules.**
- Dimension passes H0.1 → advances to Phase 1.
- Dimension fails H0.1 → one codebook revision cycle is permitted (documented as an amendment, §11); a second failure freezes the dimension as **not currently measurable** and it is excluded from Phases 1–3 (reported, not hidden).
- Dimension passes H0.1 but fails H0.2 → Phase-1 encoding for that dimension uses human coders only.

**Deliverable.** Reliability table + released codebook + released scenario corpus. Publishable standalone.

---

## 4. Codebook anchors (to be completed before freeze)

For each dimension: a one-sentence construct definition, the bipolar orientation (which pole is
"aligned"), two anchor scenarios defining the unit interval [0, 1] move, and explicit *non-examples*
(what the dimension is not, to police boundaries — especially d3/d6, d7/d8, d2/d4, which are the
likeliest confusion pairs).

**The nine codebook entries are complete in the bundle file [`codebook-v1.md`](codebook-v1.md)**, which
is hashed together with this protocol. Its orientation convention is what fixes every sign in §5.0.

---

## 5. Phase 1 — Per-dimension activation and pricing on public data

Each module below specifies: paradigm; datasets (primary + backup); activation test; scale estimation; frozen sign (from §5.0); module-specific decision rule. Family for FDR: all activation tests in Phase 1 (one family).

### 5.0 Frozen sign table (derived; see the two global caveats)

All signs use the codebook's bipolar orientation (`codebook-v1.md`): the **aligned** pole honors the
value, the **violating** pole acts against it. Two equivalent statements of each sign: (i) the
**price** p_k > 0 means a move toward the violating pole must be compensated by money; (ii) the
**projection-gap** Δ > 0 (sign +1) means the coordinate-aligned option A gains probability when the
value is made salient (cost of the violating option B rises). Derivation column: **fitted** = frozen
panel sign from `prereg-v1`/`predictions_v2.json`; **convention** = the same cost mechanism applied to
this coordinate's codebook orientation.

| coord | name | price sign | projection-gap sign | derivation | notes |
|---|---|:--:|:--:|---|---|
| d2 | Rights | p2 > 0 | +1 | convention | priced branch; **lexicographic contingency** (§5 D2, §9) may replace the price with a refusal mass |
| d3 | Fairness | p3 > 0 | +1 | convention (literature positive control) | unfairness raises cost of acceptance |
| d4 | Autonomy | p4 > 0 | +1 | convention | ceding one's own decision rights raises cost (control premium) |
| d5a | Trust | p5a > 0 | +1 | convention | betraying entrusted resources raises cost |
| d5b | Privacy | p5b > 0 | +1 | convention | disclosing a private fact raises cost (WTA to disclose > 0) |
| d6 | Social impact | p6 > 0 | **+1** | **fitted** (`prereg-v1`) | worse externality raises cost; human sign must match panel |
| d7 | Virtue/identity | p7 > 0 | **+1** | **fitted** (`prereg-v1`) | dishonest/role-breaching act raises cost |
| d8 | Legitimacy | p8 > 0 | +1 | convention | complying with an illegitimate source raises cost |
| d9 | Epistemic (gain) | p9 > 0 | **+1** | **fitted** (`prereg-v1`) | vague source raises cost when clarity is desirable |
| d9 | Epistemic (loss) | — | **−1** | **fitted, registered flip** | clarity is aversive under losses → sign reverses (`contrasts.py` B1L) |

The only non-`+1` real-contrast sign in the entire manifold is **d9 under losses**; it is the frozen,
already-tested exception, not a new claim. Every other coordinate predicts +1 by the identical cost
mechanism, which is what makes the dormant-coordinate tests genuine out-of-sample uses of the frozen
model rather than fresh fits.

### D3 — Fairness (positive control; expected to activate)
- **Paradigm.** Ultimatum rejections (paying to punish unfairness) and dictator giving.
- **Datasets.** Engel (2011) dictator meta-analysis, *Exp. Econ.* 14:583–610 (data appendix) `[VERIFY]`; Oosterbeek, Sloof & van de Kuilen (2004) ultimatum meta, *Exp. Econ.* 7:171–188 `[VERIFY]`; Bruhin–Fehr–Schunk (2019) *JEEA* replication data `[VERIFY]`; FKM and Charness–Rabin (already in hand from Part II).
- **Activation.** Already established in the literature; run as a positive control on the pipeline: the (d1, d3) fit must beat d1-only on held-out folds. **If this control fails, the pipeline is broken; halt and debug before interpreting any other module.**
- **Scale.** p3 from ultimatum rejection thresholds (the money a responder forgoes at the rejection margin per unit of encoded unfairness) and, separately, from dictator giving. Two within-module estimates → first stability test.
- **Sign.** `[MODEL]` (expected: unfairness raises cost of acceptance).

### D4 — Autonomy (showcase dormant coordinate; run first among the dormant four)
- **Paradigm.** Control premium / value of decision rights: subjects pay money to retain choice even when delegation has higher expected value.
- **Datasets.** Owens, Grossman & Fackler (2014), "The control premium," *AEJ: Micro* 6(4):138–161, journal replication archive `[VERIFY]`; Bartling, Fehr & Herz (2014), "The intrinsic value of decision rights," *Econometrica* 82(6):2005–2039, journal data supplement `[VERIFY]`; Fehr, Herz & Wilkening (2013), "The lure of authority," *AER* 103(4):1325–1359 `[VERIFY]`.
- **Activation.** (d1, d4) beats d1-only held-out; the literature's headline (positive control premium) makes this the best-powered dormant test.
- **Scale.** p4 = fitted dollar value of a unit autonomy move; the Owens et al. design yields an especially direct WTP anchor. Estimate independently on all three datasets → within-module stability.
- **Sign.** `[MODEL]` (expected: losing decision rights adds cost).

### D7 — Virtue / identity
- **Paradigm.** Lying at a price (die-roll / coin-flip honesty tasks): money left on the table to preserve honest self-image.
- **Datasets.** Abeler, Nosenzo & Raymond (2019), "Preferences for truth-telling," *Econometrica* 87(4):1115–1153 — meta-analytic data across ~90 studies, published with paper `[VERIFY]`; Gerlach, Teodorescu & Hertwig (2019) dishonesty meta, *Psych. Bulletin* `[VERIFY]` as backup.
- **Activation.** Gap between payoff-maximizing report rate and observed report rate, modeled as a d7 cost; (d1, d7) vs d1-only on held-out study-level folds.
- **Scale.** p7 from the report-rate/stake-size gradient (the Abeler et al. data include stake variation across studies — the key identifying variation).
- **Sign.** `[MODEL]` (expected: dishonest report raises cost).
- **Known risk.** The meta-analytic headline is that lying aversion is surprisingly stake-insensitive; if p7 is not identified from stake variation, report the boundary honestly — a stake-insensitive d7 is itself evidence about the coordinate's form (fixed cost, not marginal price), and the decision rule in §9 covers it.

### D5 — Privacy / trust (pre-registered split test)
- **Hypothesis of interest: d5 is two coordinates.** Price the two halves separately; pre-register the test that p5-trust ≠ p5-privacy.
- **Trust datasets.** Johnson & Mislin (2011) trust-game meta-analysis, *J. Econ. Psych.* 32:865–889 (data appendix) `[VERIFY]`.
- **Privacy datasets.** Acquisti, John & Loewenstein (2013), "What is privacy worth?", *J. Legal Studies* 42(2):249–274 `[VERIFY]`; OSF-hosted WTP/WTA-for-privacy replications `[VERIFY at execution: search OSF for current best replication with public data]`.
- **Activation.** Separately for each half, per the standard test.
- **Scale.** p5a (trust: money risked per unit trust move), p5b (privacy: WTA for a unit privacy disclosure).
- **Split decision rule.** If bootstrap CIs of p5a and p5b are disjoint across ≥ 2 dataset pairs → the framework's d5 is split into two coordinates in a registered amendment (a welcomed revision, not a failure).
- **Sign.** `[MODEL]` for each half.

### D8 — Legitimacy
- **Paradigm.** Same incentive, different source: elected vs. imposed authority; lawful vs. unlawful contexts.
- **Datasets.** Baldassarri & Grossman (2011), centralized sanctioning with random vs. elected monitors, *PNAS* 108(27) `[VERIFY]`; tax-compliance lab experiments with public OSF data `[VERIFY at execution]`; Moral Machine (Awad et al. 2018, *Nature* 563:59–64; public data release `[VERIFY]`) lawful/unlawful-crossing attribute as a large-N secondary source.
- **Activation.** Behavior difference between legitimacy conditions at identical monetary incentives — this is a natural projection-gap contrast already run in the literature; re-fit under GDT.
- **Scale.** p8 from the sanction-compliance gradient across legitimacy conditions.
- **Sign.** `[MODEL]` (expected: illegitimate source raises cost of compliance).

### D2 — Rights (run last; lexicographic contingency pre-registered)
- **Paradigm risk, stated up front.** Sacred-values research (protected values / taboo tradeoffs) predicts refusal of the money exchange rate. Therefore this module pre-registers **two competing forms**: (a) d2 is priced (finite p2); (b) d2 is lexicographic — a refusal coordinate with a mass of non-trading subjects.
- **Datasets.** WVS/EVS civil-liberties tradeoff items (free, registration required) `[VERIFY terms]`; COVID-era liberties-vs-safety tradeoff studies with OSF data `[VERIFY at execution]`; Moral Machine lawful/rights-adjacent attributes as secondary.
- **Test between forms.** Fit both: (a) standard (d1, d2) angle; (b) a two-part model (probability of refusal + conditional price). Model comparison by held-out NLL. A refusal mass > 25% of subjects with (b) beating (a) → d2 registered as lexicographic.
- **Sign.** `[MODEL]` for the priced branch.
- **Either outcome is a result:** a priced d2 completes the table; a lexicographic d2 is a structural discovery about the manifold (a coordinate outside the Mahalanobis form) and bounds the metric honestly.

### D6 — Social impact (already activated on the panel; human pricing)
- **Datasets.** DellaVigna, List & Malmendier (2012), door-to-door giving field experiment, *QJE* 127(1):1–56, data published `[VERIFY]`; DonorsChoose public dataset (Kaggle/archive) `[VERIFY]` for scale-of-impact gradients; FKM (in hand).
- **Activation.** Human-side confirmation of the panel result: giving varies with encoded social impact at fixed price of giving.
- **Scale.** p6 = dollars given per unit encoded impact move.
- **Sign.** `[MODEL]` (panel sign already frozen in `prereg-v1`; the human sign must match it — a mismatch is a registered discordance between model organism and humans and must be reported as such).

### D9 — Epistemic status (already activated on the panel; human pricing)
- **Datasets.** Good Judgment Project public data, Harvard Dataverse `[VERIFY DOI]`; Metaculus public data/API `[VERIFY terms]`.
- **Activation.** Bet sizing / forecast updating varies with encoded epistemic status (evidence quality) at fixed monetary stakes.
- **Scale.** p9 from the stake-vs-evidence-quality gradient in forecasting tournaments.
- **Sign.** `[MODEL]`; same concordance requirement with the panel sign as D6.

### D1 — Money (numeraire; no activation test)
- Calibration only: per-dataset magnitude recalibration constant, as in Part II. Reported for completeness.

---

## 6. Data plan details

For each dataset at execution time, record in the registration bundle: exact source URL/DOI, download date, license/terms, N (subjects, choices), the resampling unit for bootstrap (subject if identified, else choice), inclusion/exclusion rules (drop: incomplete choices, attention-check failures where flagged by original authors; no other exclusions permitted), and the train/held-out fold construction (20-fold CV by subject where subjects exist, by problem otherwise — fixed seeds included in the bundle).

**Access-tier note.** Everything above is public or published-with-paper except: WVS (free, registered), Global Preferences Survey (application-gated; used only in `prereg-coupling-v1`, not required here). If any primary dataset is unavailable at execution, the named backup in its module is substituted and the substitution logged (§11); if both fail, the module is postponed, not improvised.

---

## 7. Phase 2 — Projection-gap contrasts on the dormant coordinates (panel first)

**Design.** For each of d2, d4, d5(×2), d8: binary forced-choice projection-equivalent pairs per Part II §IV (matched money and lottery structure; one coordinate manipulated monotonically; comparator fixed on that coordinate), plus a wording placebo per contrast (predicted Δ = 0). Run on the existing panel harness under the **fixed information-price rule**, with the Part II revision's reporting standards: named models/versions/decoding settings, per-model effects, sign count across models as the primary statistic, BH-FDR over the family of new contrasts.

**Hypotheses (per contrast).**
- **H2.k-sign:** Δ has the frozen `[MODEL]` sign in ≥ 5/6 models.
- **H2.k-placebo:** the paired placebo is null.

**Cross-term guard (from the Part II revision).** Before freezing, verify against the fitted rank-1/rank-2 loadings that each manipulated coordinate has no material off-diagonal coupling; any coupled contrast must include the explicit cross-term bound in its sign derivation.

**Role.** Effect sizes from Phase 2 power the human confirmatory study (the Part II "human gate"), exactly as the d6/d7/d9 contrasts did for `prereg-v2`.

---

## 8. Phase 3 — Joint structure: stability and low rank with all coordinates active

Run only after Phases 0–2 resolve. Freeze as **prereg-dimensions-v1/H3**:

- **H3.1 (Cross-dataset price stability).** For each dimension with ≥ 2 independent datasets, the bootstrap 95% CIs of p_k overlap across datasets. Family: all such pairs, BH-FDR. This is the strong "predictive structure" claim — a shared metric implies shared exchange rates.
- **H3.2 (Low rank survives).** Fitting Σ on the pooled Phase-1 encodings (all passing dimensions), rank-2 + ridge fits within 0.02 held-out NLL of the full metric (the `prereg-sigma-v1` H1 criterion, re-tested with more active coordinates).
- **H3.3 (Loadings reproduce prices).** The implied pairwise tradeoffs of the fitted rank-2 metric agree with the Phase-1 subspace prices within their CIs.
- **H3.4 (Diagonal still beaten).** Rank-1 beats diagonal at equal parameter count on the pooled held-out folds.

Failure of H3.1 for a dimension **localizes context dependence** to that coordinate; failure of H3.2 with more active coordinates would mean the low-rank result was an artifact of coordinate dormancy — either is decisive information.

---

## 9. Decision rules per dimension (summary matrix)

| Outcome pattern | Registered interpretation | Registered action |
|---|---|---|
| Passes H0, activates, prices stably | Coordinate earned | Retained; loadings enter Phase 3 |
| Passes H0, activates, price unstable across datasets | Context-dependent coordinate | Retained with a per-context scale; flagged in the manifold spec |
| Passes H0, activates, refuses pricing (d2 pattern) | Lexicographic coordinate | Registered amendment: coordinate moved outside the Mahalanobis form |
| Passes H0, fails activation in ≥ 2 adequately powered datasets **and** the Phase-2 panel contrast | Dormant-and-undetectable | Deleted from the manifold in a registered amendment; basis dimension reduced |
| Fails H0 twice | Not currently measurable | Excluded from Phases 1–3; reported; manifold status "reserved, unmeasured" |
| Split test fires (d5) | Basis miscounted | Coordinate split; dimension count revised upward |

**"Adequately powered," defined once here (§9.1).** Target **80% power** at the FDR-controlled α of
each hypothesis family. Effect-size source: for a coordinate with a frozen panel Δ (d6 ≈ 0.028,
d7 ≈ 0.044, d9 ≈ 0.500 from `predictions_v2.json`), that Δ is the assumed per-model effect; for a
dormant coordinate with no panel Δ, the assumed effect is a **pre-registered minimum meaningful price**
= the smallest p_k whose 95% CI excludes both 0 and the d1-only model's ΔNLL margin (0.01/choice) —
set per module before unblinding, from the dataset's own choice count, not from its outcomes.

- **Phase 2 (panel).** The test "sign in ≥ 5/6 models" has ≥ 80% power when the per-model
  sign-detection probability ≥ 0.80; with 216 personas × thousands of forced choices per model this
  holds for any true per-model Δ ≥ ~0.02, so all real contrasts with a frozen or piloted Δ ≥ 0.02 are
  adequately powered. A dormant contrast whose pilot Δ < 0.02 is labeled **underpowered → exploratory**.
- **Phase 1 (observational).** Power to beat d1-only by ΔNLL ≥ 0.01/choice is computed by parametric
  bootstrap at the **registered N** of each dataset (§14), under the assumed effect above, before any
  fit to that dataset's outcomes. A module reaching ≥ 80% at its N is confirmatory; below 80% it runs
  but is reported as exploratory (and, if two such datasets exist for a coordinate, does not by itself
  trigger the "dormant-and-undetectable" deletion in §9). The bootstrap script and the per-module N,
  assumed effect, and computed power go in the registration bundle as `power/` before hashing.

---

## 10. Phase 4 — Completeness (the escape test)

**Design.** A red-team task, run on the panel and on ≥ 2 human coders: *construct choice scenarios whose behavioral variation cannot be represented as movement on any of the (post-revision) coordinates.* Candidate escape scenarios are then encoded by the Phase-0 encoders; any pair matched on **all** coordinates (within encoder noise) but producing a reliable choice-probability difference (panel first, human study second) is a **residual**.

- **H4 (null form, the framework's claim):** no residual survives placebo correction and FDR control.
- A confirmed residual is a missing axis by the paper's own Theorem-1 logic → registered amendment adding a coordinate, with the escape scenarios becoming its first anchor set.

This phase makes the basis falsifiable *as a basis*, not only coordinate by coordinate.

---

## 11. Amendments, deviations, and substitutions

- Any deviation from this protocol is logged in a public, timestamped amendment file (`AMENDMENTS.md` in the registration repository) stating what changed, why, and whether the affected hypothesis retains confirmatory status (it usually does not — it becomes exploratory).
- Dataset substitutions are permitted only to the named backups (§5–6) and are logged.
- Codebook revision after an H0.1 failure is permitted once per dimension (§3).
- No sign prediction may be edited after freeze; a wrong sign is a reported failure, per the standing practice of `prereg-v1`.

---

## 12. Freezing and hash procedure (to execute, not yet executed)

**Two-level freeze.** The substantive anti-p-hacking commitments are coordinate-level and are frozen
now (Level 1). The measurement *instrument* is generated reproducibly *from* the frozen codebook and
committed before data (Level 2); because the frozen predictions are per-coordinate signs (§5.0)
independent of any specific scenario, generating stimuli after Level 1 cannot bias them.

- **Level 1 (this freeze).** Bundle = this protocol (final), `codebook-v1.md`, the §5.0 sign table,
  the §14 verified dataset registry, and the §9.1 power protocol + `power/` bootstrap script. All
  `[AUTHOR TODO]`/`[MODEL]` placeholders are resolved; `[VERIFY]` is resolved in §14.
- **Level 2 (before Phase 0 data).** Generate the 200-scenario corpus from `codebook-v1.md`, the
  frozen encoder prompts, and the fold seeds; commit as `bundle-L2/` referencing the Level-1 hash.
  The pre-freeze checklist in §14 (open the two Econometrica zips; confirm the two substitute deposits;
  fix the WVS index; resolver-check two DOIs) is cleared as part of Level 2.

**Procedure.**
1. Confirm Level-1 completeness (above); author signs off on the §5.0 signs and `codebook-v1.md`.
2. Compute `sha256` over the Level-1 bundle files; write `prereg-dimensions-v1.sha256`.
3. **Signed git tag `prereg-dimensions-v1`** in the repository (independent Merkle-ordered timestamp),
   and **OSF registration** (author step: creates a frozen, DOI-bearing copy) — record both here.
4. Only then acquire/lock held-out data; do Level 2; begin Phase 0.

**Sequencing.** Phase 0 → D3 (pipeline control) → D4, D7 (best data among dormant/semi-dormant) → D5, D8, D6, D9 → D2 last → Phase 2 → Phase 3 → Phase 4. Phases 0–1 are analysis of existing public data and can proceed immediately after freeze; Phase 2 reuses the existing panel harness; Phase 4 is gated on the post-revision coordinate set.

---

## 13. Reporting commitments

All modules are reported regardless of outcome, including failed activations, unstable prices, and encoder failures, in the same scorecard format as Part II Table "prereg-sigma-v1." The graveyard convention applies: rejected structural claims are tabulated so they are not re-walked.

---

## 14. Verified dataset registry (resolves every §5 `[VERIFY]`)

Verified 2026-07-06. **Primary = the dataset a module uses; where the primary has no reusable public
data, the pre-registered substitute (per §11) is promoted to primary and the original is retained only
as a paper-level reference.** DOIs marked ‡ were confirmed via resolver/API; † via cross-source
listing (high confidence, not resolver-run — re-check at execution).

| coord | dataset (role) | DOI / URL | data public | access |
|---|---|---|:--:|---|
| d3 | Engel 2011 dictator meta (primary) | article `10.1007/s10683-011-9283-7`†; data **osf.io/xc73h** | yes | open OSF |
| d3 | Bruhin–Fehr–Schunk 2019 (primary) | `10.1093/jeea/jvy018`‡ (corr. `…/jvz042`) | yes | open (JEEA pkg) |
| d3 | Oosterbeek 2004 ultimatum meta | `10.1023/B:EXEC.0000026978.14316.74` | **no data** | paper only → hand-code WP appendix, or use Henrich cross-cultural UG |
| d4 | Owens–Grossman–Fackler 2014 (primary) | data `10.3886/E114422V1`‡ (openICPSR 114422) | yes | open |
| d4 | Fehr–Herz–Wilkening 2013 (primary) | data `10.3886/E112646V1`‡ | yes | open |
| d4 | Bartling–Fehr–Herz 2014 | supp. under `10.3982/ECTA11573`‡ | yes* | open — *open zip pre-freeze to confirm raw data; else Feltovich 2023 JEBO |
| d7 | Abeler–Nosenzo–Raymond 2019 (primary) | supp. under `10.3982/ECTA14673`‡ | yes* | open — *open zip pre-freeze to confirm ~90-study meta-data |
| d5a | Johnson–Mislin 2011 trust meta | `10.1016/j.joep.2011.05.007`† | **no open data** | → **substitute** van den Akker 2020 trust-game meta (verify its OSF at execution) |
| d5b | Acquisti–John–Loewenstein 2013 | `10.1086/671754`‡ | **no data** | → **substitute** Benndorf–Normann 2018 `10.1111/sjoe.12247` (verify deposit) |
| d8 | Baldassarri–Grossman 2011 | `10.1073/pnas.1105456108`‡ | **no microdata** | → **substitute** Dal Bó–Foster–Putterman 2010 AER 100(5), open AEA data |
| d8 | Moral Machine (secondary, large-N) | `10.1038/s41586-018-0637-6`‡; data **osf.io/3hvt2** | yes (full ~40M) | open OSF (geo withheld) |
| d2 | WVS/EVS liberties battery | worldvaluessurvey.org (register); GESIS EVS | yes | WVS free-register / EVS open — **no single named "liberties-vs-security" item**; use a constructed index from the post-materialist battery (E001–E003 / Y002) + obedience A042, defined in the codebook before freeze |
| d2 | Moral Machine (secondary) | as above | yes | open OSF |
| d6 | DellaVigna–List–Malmendier 2012 (primary) | data `10.7910/DVN/QNVCAY`‡ (Harvard Dataverse, CC0) | yes | open |
| d9 | Good Judgment Project (primary) | `10.7910/DVN/BPCDH5`‡ (Dataverse, CC0) | yes | open |
| d9 | Metaculus (secondary) | api2 (metaculus.com/api2) | yes (API) | open read — **ToS forbids using content to train/develop AI/ML**; Phase-1 use here is descriptive pricing only, which is permitted; if any panel/model use touches Metaculus content, obtain written permission first |

**Pre-freeze checklist items surfaced by verification (must clear before §12 hashing):**
1. Open the Bartling 2014 and Abeler 2019 Econometrica supplement zips once and confirm the raw/meta
   filenames (both are high-confidence but were not eyeballed).
2. Confirm the van den Akker (2020) trust-meta OSF deposit and the Benndorf–Normann (2018) data
   deposit exist, before promoting them to primary for d5a / d5b.
3. Freeze the exact WVS variable list / constructed-index formula for d2 in the codebook (no named
   single item exists).
4. Re-run `10.1016/j.joep…` and `10.1093/qje/qjr050` through the DOI resolver (listed, not resolved).
