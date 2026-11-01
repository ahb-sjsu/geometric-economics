# Part III exploration: is distance from a reference the right curvature? Development record

**This is development on the spent prereg-learned-v1 data** (Scruples Dilemmas: which of two actions
is less ethical, with 5 annotations per pair). It uses the same splits and the same held-out rule
(dev and test pairs sharing an action with train are dropped) as the registration. It addresses the
registration's own caveat: H2 showed that curvature beats a linear scalar, not that *distance from a
reference* is the right curvature.

## Models (`explore_learned.py`)

| Model | Cost of an action e |
|---|---|
| LIN | w · e (logit = b + w·(e0 − e1)) |
| GDT | ‖U (e − r)‖₂, the registered form |
| GDTq | (Σ_i \|U (e − r)\|_i^q)^(1/q), q free in (0.5, 4.5) |
| SQD | ‖U (e − r)‖₂², squared distance: a convex quadratic utility with the reference folded into its linear term |
| QUAD | w·e + Σ_j s_j (u_j·e)²: a low-rank quadratic with free-sign curvature and no reference |

Ranks are k ∈ {16, 32, 64} for the encoders and k = 9 (full) for xbse. The penalty λ ∈ {0, 1e-5,
1e-4} is chosen on dev, with two restarts. Coordinates come from three sources:

- **LaBSE** and **BGE-M3**, the registered and replication encoders;
- **xbse**: the nine graded moral axes (physical harm, fairness, autonomy, privacy,
  societal/environmental, care, legitimacy, epistemic quality, identity attack). Each is its own
  fine-tuned BGE-M3 encoder plus a valence axis. All nine passed their gates (`xbse_scores.meta.json`).
  Scores are standardised on train.

## Result (`explore_learned.json`, test log-loss per annotation)

| Coordinates | LIN | GDT | GDTq | SQD | QUAD |
|---|---|---|---|---|---|
| LaBSE | 0.6549 | **0.6410** | 0.7069 | 0.6433 | 0.6638 |
| BGE-M3 | 0.6283 | 0.6196 | 0.6280 | **0.6175** | 0.6468 |
| xbse (9 axes) | 0.6770 | 0.6731 | 0.6723 | 0.6738 | **0.6700** |

| Comparison, paired bootstrap over test pairs | LaBSE | BGE-M3 | xbse |
|---|---|---|---|
| GDT − LIN | −0.0140 [−0.0189, −0.0093] | −0.0087 [−0.0131, −0.0041] | −0.0040 [−0.0061, −0.0019] |
| GDT − SQD | −0.0023 [−0.0058, +0.0013] | +0.0021 [−0.0012, +0.0055] | −0.0008 [−0.0013, −0.0002] |
| GDT − QUAD | −0.0228 [−0.0310, −0.0142] | −0.0272 [−0.0365, −0.0187] | +0.0030 [+0.0011, +0.0049] |
| GDTq − GDT | +0.0659 [+0.0547, +0.0781] | +0.0083 [+0.0037, +0.0132] | −0.0008 [−0.0017, +0.0002] |

## Reading

1. **Curvature beats a linear scalar everywhere.** This replicates H2 in all three coordinate systems.
2. **Distance from a reference cannot be told apart from a convex quadratic utility.** In both
   encoders, GDT and SQD are within ±0.002 with intervals spanning zero. In the moral-axis space GDT
   is ahead by 0.0008, which is significant but small. The registered geometric form is not shown to
   be the right curvature; it is one of two forms the data cannot separate.
3. **The free Minkowski exponent is not usable in high dimension.** In the encoders, GDTq drives q
   below 1 (0.6 to 0.9), reaches much lower training loss, and generalises badly. In the 9-d moral-axis
   space, q runs to the top bound (4.47, close to the max-norm, where the worst axis dominates) for a
   gain of 0.0008. Neither is evidence about the true norm.
4. **The nine moral axes carry much less than the raw encoders** (LIN 0.677 against 0.628 to 0.655).
   They still beat Part III's text-codebook axes (0.6875). In their space a free-sign quadratic with no
   reference is best. Some axes are evaluated convexly, some concavely, and that differs from distance
   to a single ideal point.

## Dimension discovery from choices, steps 1–2 (`discover_dims.py`, `discover_dims.json`)

The candidate dimensions are the right singular vectors of the GDT metric U. U is k = 32, λ = 1e-5,
refit on all training pairs; its directions agree with the registered metric's at |cos| = 1.00. Each
candidate goes through the admission screens of moral-spectrum-analyzer's discovery roadmap that need
no second corpus:

- stability: the median over 20 bootstrap refits of the best |cos| (bar 0.70);
- non-redundancy: the direction's score on all 27,982 action texts against the nine xbse axes
  (max |r| < 0.35);
- importance: the rise in dev loss when the direction is projected out of the metric.

| Direction | Singular value | Dev loss if removed | Stability | Max \|r\| with xbse | R² from nine axes |
|---|---|---|---|---|---|
| 0 | 11.9 | +0.0315 | 0.93 | 0.25 (physical harm) | 0.13 |
| 1 | 9.9 | +0.0108 | 0.80 | 0.59 (privacy, −) | 0.44 |
| 2 | 9.5 | +0.0029 | 0.71 | 0.18 | 0.08 |
| 3–31 | 8.9–2.7 | ≤ 0.0018 | 0.30–0.59 | ≤ 0.31 | ≤ 0.12 |

Subspace stability (mean cos² of principal angles, median over resamples) is 0.65 for the top 4, 0.65
for the top 8, 0.68 for the top 16 and 0.73 for all 32.

- **Three directions are stable, and only two of them are also non-redundant: 0 and 2.** Past the
  third, the 32-dimensional metric is a rotating fit, not structure.
- **Direction 0 carries most of what the metric learned.** Removing it costs 0.032 nats per annotation,
  more than GDT's whole advantage over a linear scalar. Its extremes are cruelty to or estrangement from
  close family ("cutting my sick grandma out of my life", "despising my mentally handicap sister") at
  one end, and mundane acts ("asking for a refund", "changing laundry", "being polite") at the other.
  A plausible name is *moral gravity*, how serious the act is, as distinct from which value it touches.
  The nine axes explain 13% of it.
- **Direction 1 is mostly the xbse privacy and autonomy axes** (R² 0.44). It sets omitted care duties
  to family against offensive jokes and exposure.
- **Direction 2 looks like topic** (disability against weddings and family secrets) more than morality,
  and it carries little (0.003).

The names come from eight exemplars per end and are hypotheses. Before direction 0 is called a new
dimension it needs two checks:

1. whether it is moral-spectrum-analyzer's general-valence channel (its pc0 / G), which the roadmap
   already calls a moral-relevance detector;
2. cross-corpus replication (step 3).

### Direction 0 is not general valence (`check_valence.py`, `check_valence.json`)

General valence was checked in both of moral-spectrum-analyzer's forms:

- G, the trained channel `general_valence_joint`, at all three seeds (all passed their gates);
- pc0, the first principal component of the nine axis scores.

| | r with G (s0 / s1 / s2) | r with pc0 | R² nine axes | R² nine axes + G |
|---|---|---|---|---|
| Direction 0 | 0.26 / 0.18 / 0.19 | −0.25 | 0.130 | 0.144 |
| Direction 1 | 0.08 / 0.16 / 0.17 | −0.28 | 0.440 | 0.441 |
| Direction 2 | −0.09 / −0.08 / −0.06 | 0.09 | 0.084 | 0.091 |

86% of direction 0 lies outside everything moral-spectrum-analyzer measures.

### Not a family topic axis, and not pure gravity (`check_topic.py`, `probe_dir0.py`)

- A kinship-word indicator explains 7% of direction 0 (r = −0.27).
- Among actions that mention no kin, the spread is unchanged (SD 0.056 against 0.056 overall).
- The ordering holds without kin. At the low end are "killing my friend's tarantula", "cutting an
  autistic friend out of my life" and "potentially causing a girl to fail university". At the high
  end are "buying curtains" and "asking for a refund".

Median percentile on direction 0 by keyword group (0 = the low end):

| Group | n | Median | IQR |
|---|---|---|---|
| violence | 201 | 0.25 | 0.08–0.57 |
| kin | 6,122 | 0.33 | 0.15–0.55 |
| friends and partners | 10,026 | 0.41 | 0.20–0.63 |
| lying and cheating | 477 | 0.44 | 0.25–0.70 |
| theft, fraud, scams | 141 | 0.50 | 0.21–0.74 |
| strangers, customers, coworkers | 1,065 | 0.57 | 0.34–0.78 |

Violence sits low, as a gravity reading predicts. Impersonal wrongs (theft, fraud) sit mid-range and
acts toward strangers sit high, as a relational-stakes reading predicts. The best description these
data support is *harm to people the actor is close to, scaled by severity*. The keyword groups are
crude; the theft group includes "stealing my buddy's girl". A clean test needs independent ratings of
severity and of relational closeness on a sample of actions, then a regression of direction 0 on both.

### Hohfeld test: duty breached, closeness, or severity? (`hohfeld_*.py`)

**Written 2026-10-31 before any rating was collected.** The owner's question: can relationships be
decomposed into duties and obligations, so that direction 0 is a Hohfeldian dimension? Three readings
make different predictions:

- **gravity**: direction 0 tracks severity of harm, whoever is affected;
- **closeness**: it tracks how close the affected party is (and closeness × severity);
- **duty**: it tracks whether the act breaches a duty the narrator owes the affected party, in
  Hohfeld's terms (erisml `HohfeldianState`): the narrator holds O toward them and the act violates
  it. Under this reading closeness matters only through the duties it creates, so it should lose its
  share once breach is in the model.

Design:

- **Sample** (`hohfeld_sample.py`): 100 actions drawn at random from each decile of direction 0 over
  all 27,982 texts, seed 20261031. Texts and scores are in separate files; the raters read only texts,
  one at a time, in shuffled order.
- **Raters** (`hohfeld_rate.py`): two models from different families on NRP's managed LLM gateway,
  `gemma` and `qwen3-small`, at temperature 0. The served model is recorded on every row. Each labels
  the party most affected, closeness 0–6, position O or L, breach, omission and severity 0–6. The
  prompt is in the script.
- **Analysis** (`hohfeld_analyze.py`): direction 0 regressed on three blocks, S (severity), C
  (closeness and severity × closeness) and H (breach and omission). Each block's unique R² is reported
  given the other two, with bootstrap intervals over items.

Readings, fixed now:

| Reading | Holds if |
|---|---|
| covered | R²(S + C + H) ≥ 0.10; otherwise these labels do not capture direction 0 |
| duty | ΔR²(H \| S, C) ≥ 0.02, lower bound > 0, and larger than ΔR²(C \| S, H) |
| closeness | ΔR²(C \| S, H) ≥ 0.02, lower bound > 0, and larger than ΔR²(H \| S, C) |
| gravity | R²(S) ≥ 0.8 R²(S + C + H) |

A reading counts only if it holds for the raters' average and for each rater alone. Duty is
inconclusive if Cohen's κ between the raters on breach is below 0.40.

This is development, not a registration. LLM ratings are a stand-in for human ones, severity and
breach are both judgments of wrongness and will be correlated, and rater noise attenuates every R².
A positive reading here would justify putting the same labels to people.

**Result (run 2026-10-31; `hohfeld/hohfeld_analysis.json`).** All 1,000 items were rated by both
raters with no errors. The served models were `google/gemma-4-31B-it-qat-w4a16-ct` and
`Qwen/Qwen3.8-27B-FP8`.

Rater agreement:

| Label | Agreement |
|---|---|
| Closeness, Spearman | 0.81 |
| Severity, Spearman | 0.55 |
| Position, Cohen's κ | 0.68 |
| Breach, κ | 0.68, so the duty test is assessable |
| Omission, κ | 0.61 |
| Affected party, κ | 0.84 |

Variance explained in direction 0:

| | Raters' average | gemma | qwen |
|---|---|---|---|
| R²(S), severity | 0.164 | 0.169 | 0.118 |
| R²(C), closeness | 0.129 | 0.113 | 0.121 |
| R²(H), breach and omission | 0.088 | 0.078 | 0.070 |
| R²(S + C + H) | 0.253 | 0.241 | 0.212 |
| ΔR²(H \| S, C), duty's unique share | 0.002 [0.000, 0.010] | 0.001 | 0.002 |
| ΔR²(C \| S, H), closeness's unique share | 0.087 [0.062, 0.118] | 0.070 | 0.091 |
| ΔR²(S \| C, H), severity's unique share | 0.061 [0.035, 0.090] | 0.071 | 0.040 |

| Reading | Average | Each rater | Counts |
|---|---|---|---|
| covered | yes | yes | **yes** |
| duty | no | no | **no** |
| closeness | yes | yes | **yes** |
| gravity | no (R²(S) is 65% of the full model) | no | **no** |

What this says:

- **Direction 0 is closeness and severity, not duty breached.** Breach on its own explains 9% of the
  direction. Once severity and closeness are in the model it adds 0.002, and its standardised
  coefficient falls to about zero. In these labels, a duty owed to someone close adds nothing beyond
  how close they are and how much harm is done. The Hohfeldian reading, in this form, is not
  supported.
- **Closeness carries the largest unique share, and severity a real one.** Both coefficients are
  negative (standardised −0.29 and −0.39 on the average): grave acts toward close others sit at the
  low end. That matches the description from the keyword groups, "harm to people the actor is close
  to, scaled by severity".
- **Descriptives** (gemma's labels, direction 0 standardised):
  - by Hohfeldian cell: O with breach −0.45 (n = 271), O without breach 0.06 (17), L 0.17 (712);
  - by affected party: animal −0.54 (9), family −0.46 (205), friend −0.43 (153), romantic partner
    −0.03 (236), acquaintance or coworker 0.20 (180), stranger or public 0.37 (139), self only 1.06
    (76).
  
  Romantic partners sit near the middle, despite being rated as close as family. That was not
  predicted. One possibility is that the direction tracks kin and friendship ties rather than romantic
  intimacy. Another is that many partner items are breakups, which raters may not count as harm. This
  is a single descriptive and was not tested.

Caveats:

- **Severity is the noisiest label** (agreement 0.55 against 0.81 for closeness). Noise attenuates its
  share, so the closeness-over-severity ordering is partly a reliability gap. The duty result does not
  depend on this: breach is measured as reliably as position, and still adds nothing.
- **The duty test is of one operationalisation.** It asks whether the narrator owes the affected
  party a duty concerning the act. Duties that scale with the relationship (special obligations) are
  by construction confounded with closeness. If duty is what makes closeness matter, this design
  cannot see it, because the raters code both from the same text.
- **The full model leaves 75% of direction 0 unexplained.** LLM labels are stand-ins for human ones.

### Duties encoded by erisml-compiler: do relationships decompose into them? (`compile_*.py`)

**Written 2026-10-31 before any action was compiled.** The test above used ad hoc labels. The owner
pointed to erisml-compiler, which encodes a moral situation as typed structure:

- stakeholders with roles;
- commitments, among them `role_duty`, promise and vow, each with a holder, a beneficiary and a
  status;
- ethical facts with a severity and the parties they fall on;
- DEME's nine-dimension MoralVector, built from these per party.

The compiler's LLM extractor does not fill `Relation`. A relationship enters only as the duties it
creates, so the compiler builds in the owner's claim that relationships decompose into duties.

Design:

- **Compile** (`compile_actions.py`): each of the 1,000 sampled actions goes through
  `compile_document` as "I did the following: <action>." The settings are:
  - LLM tier, model `qwen3-small` on NRP's gateway at temperature 0, with thinking off;
  - default projections and default DEME weights;
  - a pinned venv on Atlas, erisml-compiler `73212db` and erisml-lib `c1f5643`.
- **Features**, with the narrator as the stakeholder whose roles include `agent`:
  - K, the commitment block: whether a `role_duty` held by the narrator is marked `violated`; whether a
    promise, vow, contract, oath or covenant held by the narrator is marked `violated`; and whether the
    narrator holds any `role_duty` at all;
  - MV, DEME's nine dimensions from `ir.moral_vectors[0]`.
- **Analysis** (`compile_analyze.py`), on the same y, S, C and H as the test above.

Rules, fixed now:

| Question | Reading |
|---|---|
| 1. Does the compiled MoralVector capture direction 0 better than the learned xbse axes? | Ten-fold cross-validated R² of direction 0 from MV, against the same from the nine xbse axes on the same items, with a paired bootstrap interval on the difference. Reported, no bar. |
| 2. Relationships decompose into duties | Holds if ΔR²(C \| S, H, K) < 0.02 and ΔR²(K \| S, C, H) ≥ 0.02 with lower bound > 0. |
| 2. Closeness survives the duties | Holds if ΔR²(C \| S, H, K) ≥ 0.02 with lower bound > 0. |
| 2. Neither | Inconclusive. |
| Void | More than 10% of actions fail to compile or have no agent. |

One extractor model is used, so there is no inter-rater check on the compiled structure.

**Amendment after a five-action smoke test, before the full compile, with nothing scored.**

What the smoke test showed:

- On one-line actions the extractor emits no commitments at all. Duties appear as ethical facts of
  kind `role_duty`, naming the narrator and the other party, with no status. The commitment features
  above would be almost all zero.
- A self-only action produced no stakeholders.
- The DEME vector cannot register a breached role duty. In `v3_facts_direct.py` a `role_duty` fact
  sets only `duty_owed`. DEME's `virtue_care` starts at 1.0 and falls only through
  `receives_compassion`, `treated_as_end` and `betrays_trust`: the first is never set false by any
  fact kind, and the other two only by deception. `rights_respect` falls only for grave coercion or
  a consent failure. Locking a grandfather's wife out of his hospital room compiled to `virtue_care`
  1.0 and `rights_respect` 1.0.

So K is redefined from the compiler's facts, with no judgment of mine added:

- **duty owed**: a `role_duty` fact names the narrator and another party;
- **harm under duty**: the largest severity magnitude, using the compiler's own map (minor 0.25,
  moderate 0.5, grave 0.75, catastrophic 1.0), among harm, coercion, deception and externality facts
  that fall on a party named in one of the narrator's `role_duty` facts; 0 if there is none;
- **commitment violated**: kept, though expected to be rare.

The other changes:

- **Void** now counts only compile errors. An action with no stakeholders or no agent is kept, with
  no duty.
- **Question 1** uses the actions that have a vector.

The rules are otherwise unchanged. Question 1 now tests a vector that is known to be blind to breach.

**Result (run 2026-10-31; `hohfeld/compile_analysis.json`).**

The run: 7 of 1,000 actions failed to compile (malformed JSON from the model), so it is not void.
Every row was served by `Qwen/Qwen3.8-27B-FP8`.

| Question 2, 993 actions | Value [95%] |
|---|---|
| ΔR²(C \| S, H), closeness before K | 0.087 [0.061, 0.119] |
| ΔR²(C \| S, H, K), closeness given the compiler's duties | **0.083** [0.058, 0.115] |
| ΔR²(K \| S, C, H), duties' unique share | 0.004 [0.001, 0.015] |
| R²(K) alone | 0.018 |
| Reading | **closeness survives the duties**; relationships decompose into duties: no |

| Question 1, the 816 actions with a vector | Cross-validated R² |
|---|---|
| DEME's nine dimensions (unfixed bridge) | 0.091 |
| The nine xbse axes | 0.121 |
| Difference | −0.029 [−0.091, +0.026] |

Four DEME dimensions barely move: rights, privacy, legitimacy and epistemic quality all have SD at most
0.036.

**This is not a fair test of the owner's hypothesis, because the compiler measured duty poorly.**

- 205 actions (21%) compiled to no stakeholders at all. "Wanting my family to stop cussing in public"
  compiled to nothing.
- Of the 204 actions gemma rated as affecting family, the compiler found a role duty in 63 (31%), and
  a commitment in 3.
- "Not letting my sister move in" and "not loaning my brother money for his car anymore" compiled
  with no duty.
- Duty owed correlates 0.13 with the raters' closeness.

A duty block that misses most relationships cannot absorb closeness, whatever the truth. The reading
"closeness survives" holds as registered. What it shows is that the compiler, on one-line actions,
does not encode relationships as duties, not that relationships are not duties.

Before the test can be fair, the extractor needs two things:

- a narrator for every first-person act;
- a role duty for every kin, partner or friend relation it names. The `Relation` schema has
  `kin_of`, but the LLM extractor never fills it.

The bridge fix (erisml-compiler PR #49) matters only once duties are extracted. Harm under a duty was
found in 3% of actions here.

### Rerun with the fixed extractor and bridge (PRs #49 and #50)

**Written 2026-10-31 before the rerun.**

- **What runs:** the same 1,000 actions, model and prompt prefix. The compiler is `main` 73212db with
  PR #49 (`breached_duties`) and PR #50 applied: narrator guard, relations pass, duties derived from
  relations, one completion pass. Output goes to `hohfeld/compiled_v2_qwen3-small.jsonl`, with full
  IRs saved.
- **K, now read from what the compiler itself produces:**
  - duty owed: the narrator holds a `role_duty` toward another party, as a commitment or as a
    `role_duty` fact naming both;
  - harm under duty: the severity magnitude of the gravest breach in `breached_duties`, 0 if none;
  - commitment violated: as before.
- **Rules and void condition:** as for the first compile.

**Caveat.** Duties now come from relations the extractor names, so K is partly a coded form of
closeness. If K absorbs closeness here, that says the duty-and-breach encoding carries what graded
closeness carries. It does not say people reason through duties. The informative quantity is
ΔR²(C | S, H, K): how much graded closeness adds beyond the compiled duties and breaches.

**Added during the run, before any analysis.** At 263 rows, 16 had failed. Every failure was the
model returning empty content on both tries of a prompt; the first compile lost 0.7% this way.
(The progress monitor first over-counted failures by grepping for "error", which also matches
saved IR text.) Failed actions are retried once, with the same settings, after the pass ends; the
script resumes and skips actions already compiled. The retry depends on whether an action
compiled, never on any score. The void rule counts the failures left after the retry, and both
counts are reported.

**Result (2026-10-31; `hohfeld/compile_v2_analysis.json`).** 58 actions failed in the pass and 29
after the retry, so the run is not void. Every row was served by `Qwen/Qwen3.8-27B-FP8`.

What the extractor now encodes, against the first compile:

| | First compile | Rerun |
|---|---|---|
| Actions with no agent | 207 | **0** |
| Narrator owes a role duty | 15% | **42%** |
| A duty breached | 3% | **12%** |
| Correlation of duty owed with the raters' closeness | 0.13 | **0.41** |

Question 2, on 971 actions:

| | First compile | Rerun [95%] |
|---|---|---|
| R²(K) alone | 0.018 | 0.096 [0.065, 0.136] |
| ΔR²(K \| S, C, H), duties' unique share | 0.004 | 0.016 [0.006, 0.033] |
| ΔR²(C \| S, H), closeness before K | 0.087 | 0.086 [0.060, 0.119] |
| ΔR²(C \| S, H, K), closeness after K | 0.083 | **0.055** [0.034, 0.081] |
| Reading | closeness survives | **closeness survives**; decompose: no |

Question 1, on 818 actions: DEME's vector has cross-validated R² 0.114, the xbse axes 0.134, a
difference of −0.020 [−0.083, +0.044]. `virtue_care` and `rights_respect` now vary (SD 0.196 and
0.202, against 0.087 and 0.036).

What this says:

- **A better encoding moves the result toward the owner's hypothesis, but not past the bar.**
  - Once duties and breaches are encoded, they take about a third of closeness's unique share
    (0.086 to 0.055).
  - The duties alone explain 10% of direction 0.
  - Their unique share, 0.016, is just under the 0.02 bar.
- **Graded closeness keeps a real share beyond the compiled duties.** A sibling and a friend both
  carry a duty here, and the duty has no strength. The raters' closeness separates them. Whether the
  remainder is the *strength* of the duty, which DUTY_RELATIONS does not grade, or something other
  than duty, this design cannot tell.
- **The repaired DEME vector now moves on breach,** and its fit to direction 0 rose from 0.091 to
  0.114. It is still level with the xbse axes.

The natural next test is graded duty strength: a weight per relation type, or per relation as the
extractor reads it. Fitting those weights on direction 0 would be selection on the target, so they
would have to be fixed beforehand, or fit on another corpus.

Together with `../../strata2/DEVELOPMENT.md` and `../../menus/DEVELOPMENT.md`: in none of the three
domains does the data prefer a Euclidean distance from a reference point over its nearest
non-geometric rival. What the data do reward is curvature, and in menus a scale set by the menu.
