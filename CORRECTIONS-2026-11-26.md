# Corrections to Geometric Economics, 2026-11-26

These corrections were made on 2026-11-26 at the author's direction after a review of the series.

Each item gives where the change is, what the text said, what it says now, and how the right value was established. Figure lines and captions were not edited.

## Reconciled

1. **Chapter 3, Proposition 5 (Section 3.6).** The threshold read `beta_k > Delta d_1 / sigma_1^2`. It now reads `beta_k > (Delta d_1)^2 / sigma_1^2`. Definition 4 gives the monetary term of an edge weight as the squared change over the variance, and the ultimatum example of Chapter 7 states the same threshold in the squared form.

2. **Chapter 3, Section 3.8, option v2.** The autonomy line said "committed to three years" for a lease the same list calls a five-year term three times. It now says five years. Chapter 7 also gives a five-year guarantee.

3. **Chapter 3, Section 3.8, path to v2.** The text said the positive movements "actively reduce the Mahalanobis distance, because improvements on correlated dimensions offset the monetary cost". A quadratic form cannot be reduced by a displacement in either direction. The text now says that the movements are improvements, that the non-monetary displacements are smaller in total than on the path to v1 (sum of squares 0.85 against 1.28 from the printed vectors), and that the direction-dependent treatment of gains and losses is the Finsler metric of Section 4.10.

4. **Chapter 4, Section 4.10.** The loss-aversion coefficient is defined in Section 4.2 as a ratio of edge weights and in Section 4.10 as a ratio of Finsler lengths. One sentence now names both and says the second is the square root of the first, since an edge weight is a squared length. No number was changed. See Unresolved 3.

5. **Chapter 4, Technical Appendix, condition 2 of the Finsler metric.** The note said absolute homogeneity "allows F(x, v) != F(x, -v)". Setting alpha = -1 shows it forces equality. The note now says so, and the next sentence says condition 2 is relaxed to positive homogeneity.

6. **Chapter 4, Section 4.8.** One sentence now says the vectors of this example are posited for it and differ from the vector Section 3.8 assigns to accepting the increase, which was scored with a one-year lease and so has a positive d2. The numbers of both sections are unchanged. See Unresolved 10.

7. **Chapter 5, worked example, Path A.** The text said the margin drops "to roughly -2,020 a month (from 1,400 to -620)". 1,400 less the 3,420 a month the same sentence and the table give is -2,020, so the parenthesis now reads "from 1,400 to -2,020". See Unresolved 2 for the 19,000 figure.

8. **Chapter 5, worked example, Step 3 table.** The ranks read 4th, 3rd, 1st, Last, with no 2nd. Step 4 ranks the paths C, B, A, D, and the f column of the table orders them the same way. The ranks now read A 3rd, B 2nd, C 1st, D Last.

9. **Chapter 6, Theorem 16.** Part 2 wrote the cycle as phi(x) > phi(y) > phi(z) > phi(x), which no real-valued function satisfies. It now writes the cycle in the projected preference relation, says the projection is context-dependent, and adds that a single fixed real-valued phi gives no cycle. This is what the theorem's own proof uses.

10. **Chapter 6, GDP as tensor contraction.** The component T_k was "the total change along each dimension", which for d1 is zero in a closed economy by Corollary 9.2. It is now "the total activity along each dimension", with a pointer to Corollary 9.2 for the difference between volume and net change.

11. **Chapter 6, running example.** "Business gutted on five of nine dimensions" followed a list of four components (B3, B5, B6, B7). It now says four.

12. **Chapter 6, Projection 1.** The displayed sum was given as approximately 200,000 dollars. With the printed inputs (226,800 growing 2% a year, less 210,000, discounted at 10% over ten years) it evaluates to 212,261. The display now says approximately 212,000, and the next sentence says the appraiser's number is 200,000 in round figures. The 200,000 used in the rest of the chapter is unchanged.

13. **Chapter 7, worked example, contraction check.** The text said the contraction condition "is satisfied. The BGE is unique." The condition was assessed only qualitatively (High against Moderate), and the best-response lists name no accepting strategy for Maria at the offers of 5K and 6K. The sentence is now conditional, and one sentence says the lists do not by themselves establish uniqueness.

14. **Chapter 8, Section 8.2; Chapter 9, Sections 9.3 and the running-example box; Chapter 10, Section 10.3; Chapter 14, Section 14.9; Appendix D; index.** Fairness, d3, was placed with the transferable dimensions in some places and with the evaluative ones in others. Definition 2 of Chapter 3 argues explicitly that fairness is evaluative, and Theorems 9.1 and 9.4 and Section 6 agree. Every classification now reads transferable d1, d2, d4 and evaluative d3, d5 to d9. In Chapter 9 the sum defining V_created now runs over {3, 5, 6, 7, 8, 9}, the list of evaluative dimensions in Section 9.3 includes fairness, and the box says "zero-sum on three dimensions and able to be positive-sum on the other six" where it said "positive-sum on five". In Theorem 10.1 the quantity V_E is now described as "the evaluative value summed over d5 to d9" and its formula is unchanged.

15. **Chapter 8, worked example of Section 8.7.** "We present it under three descriptions" introduced a table of four. It now says four descriptions, a baseline and three transformations.

16. **Chapter 9, worked example, autonomy row.** Both parties had a negative entry and the sum read "balanced", against Theorem 9.1. The proof of Theorem 9.1 gives the case: the party who commits to deliver loses autonomy and the other gains guaranteed receipt. The row now reads +guaranteed delivery for Maria, -committed to delivery for Elena, sum 0.

17. **Chapter 10, Section 10.4.** A diagonal move under positive correlation was said to "cover more Mahalanobis distance" than two sequential moves. For a covariance [[1, r], [r, 1]] with r > 0 the diagonal move costs (a^2 + b^2 - 2rab)/(1 - r^2), which is less than the sum of the two single moves. The text now says "costs less", which is also what the preceding paragraph says ("lower total energy").

18. **Chapter 12, Sections 12.1 and 12.5.** "A 3,000 dollar loss is 0.002% of his annual compensation" and "100 dollars is 0.00007% of Crane's monthly discretionary income". With the chapter's 4.5 million a year and 150,000 a month both are 0.067%. Both now say 0.067%.

19. **Chapter 12, "What the Gini Misses".** The Gini of the three-person economy was given as 0.67, twice. The chapter's own formula with its three incomes (2,160, 4,500 and 375,000 a month) gives 0.651. Both now say 0.65.

20. **Chapter 12, Proposition 42.** The proposition writes G proportional to the square root of I_11, and the Technical Appendix says the two are "related to but not identical". One sentence after the proposition now says the proportionality is schematic and points to the appendix.

21. **Chapter 13, worked example.** The monetary terms were written 960/sigma_1^2 and 2,000/sigma_1^2. Definition 4 squares the change. They now read 960^2 and 2,000^2. See Unresolved 5 for the subtraction in Option B.

22. **Chapter 13, "The Conservation Laws in Maria's Trade".** The evaluative surplus was "approximately 2.3 units" from terms that add to 3.3 (0.4 + 0.4 + 0.6 + 0.6 + 0.8 + 0.5). It now says 3.3 and notes that Chapter 9's illustration of the same order uses smaller per-party gains and totals 2.4.

23. **Chapter 15, Section 15.2.** Stern's 0.1% was called his social discount rate. The Ramsey decomposition in the same section uses 0.1% as his pure time preference and gives a total of 1.4%. The opening sentence now says pure time preference, 0.1%, and gives the total. See Unresolved 8 for Nordhaus.

24. **Chapter 15, solar table.** The present value was 31,200 and the net 1,200. The table's own formula, 4,500 a year times the sum of exp(-0.03 t) for t = 1 to 8, gives 31,528. The table now says 31,500 and 1,500.

25. **Chapter 2, cross-references.** "Theorem 34", "Proposition 36" and "Theorem 37" now say "of Chapter 4", because Chapter 8 also has a Theorem 37 and a Remark 36. See Unresolved 9.

Checked and left as they are: Sofia's itemised terms in Section 12.5 add to 8.32 and the printed total of 9.1 includes "other cross terms" the text names; the ratios 22,750 and 825 follow from the printed totals. The heading of the Chapter 5 example asks about a rise to 5.00 and Path B is the alternative of 5.50, which is not a contradiction.

## Marked as illustrative or simulated

1. **Chapter 0 (preface and Key Results table), root `front_matter.md`, Chapter 3 Section 3.1, Chapter 4 Section 4.2 and Notes on Sources, Chapter 16 Sections 16.1 and 16.8, index.** The text said the framework "correctly predicts 16/16 behavioral phenomena with 2.70% mean absolute error", that the validation "confirms" the loss-aversion range, and that the framework "is empirically grounded". The record in this repository is `experiments/PART2_DRAFT.md`, which calls the result "an in-sample benchmark (16 aggregate targets, MAE 2.70%)", and `nobel-program.md`, which describes "16 aggregate targets, heterogeneous studies, plus or minus 5/10% tolerances". The passages now say 16 of 16 aggregate targets reproduced in sample, a calibration benchmark and not an out-of-sample prediction. The README's status of 2026-07-14 (posited, no economics instrument through the admission filter) is the later statement and the chapter sentences were brought to it. The code listing in Appendix B was not touched.

2. **Chapter 3, Section 3.1.** The text said the nine dimensions "were empirically validated across 20,030 texts and 11 languages". In Geometric Ethics 20,030 is the number of letters in the Dear Abby corpus, which is in English, and the cross-lingual set is 109,294 passages in 11 languages. The Ethics claim ledger (`GE-CROSSLINGUAL`) classes the cross-lingual result exploratory, with the instrument confound open. The sentence now gives both corpora and that classification.

3. **Chapter 3, Section 3.7.** "Validated by factor analysis of behavioral data" now reads as a prediction (Prediction 5 of Section 16.4), since no such analysis is recorded in the repository. "Cross-lingual validation shows that the rank of Sigma is stable at approximately 9" now reads as a posit, and one sentence reports that the repository's registered tests on choice data report a low-rank metric (`experiments/EVIDENCE.md`) and that the coupling test failed.

4. **Chapters 0 and 16, the failed registered test.** The cross-domain coupling prediction (`experiments/PREREG_cross_domain_coupling.md`) was scored on the Global Preferences Survey and failed on that proxy (`experiments/RESULTS_coupling_scorecard.md`). The preface now says so in one sentence, and Section 16.1 says it in two: the correlations were positive but below the registered threshold, the structure was not rank-one, and the same-subject test on choice-fit angles has not been run.

5. **Chapter 8, worked example of Section 8.7.** The heading now says "(hypothetical data)". The body already said the ratings were hypothetical.

## Withdrawn or updated

1. **Chapter 8, Section 8.2, "Comparison with Other Domain Gauge Groups".** The table gave D4 times U(1)_H for Ethics and D4 for Law, and listed "harm conservation". Geometric Ethics withdrew D4 for the Hohfeldian positions in version 1.25 (2026-11-08) and withdrew "conservation of harm" on 2026-06-19. A dated note now heads the subsection. The table gives V4 times U(1)_H and V4, and "harm accounting". The sentence after the table said "The ethics gauge group is discrete (D4 is finite)". It now says the Hohfeldian factor is discrete (V4 is finite), which is true as written. The comparison uses only finiteness, so nothing was withdrawn. The Law row was restated on the strength of the Ethics withdrawal. The Law volume's own text was not checked here.

2. **Chapter 1, "The Suspicious Coincidence".** The first-person account names the conservation law for harm and the D4 group. The account was left as written and a dated note after it records both withdrawals and says nothing in this volume depends on them.

3. **Experiments.** `experiments/EVIDENCE.md` already lists the D4 and V4 conjectures about risky choice as dead, with the correction of 2026-09-13. Those concern a symmetry of the (d, q) plane of gambles, not the Hohfeldian positions, and no chapter cites them. Nothing was changed.

No other withdrawn or refuted Ethics result (the SU(2) gauge prediction, hysteresis) is cited in this volume.

## Unresolved

1. **Chapter 1, Easterlin paragraph.** "Beyond a threshold of approximately 15,000 dollars per capita (in 2024 dollars, roughly 75,000)" gives two figures that no conversion in the text connects, and "Japan's real GDP per capita quadrupled between 1960 and 1990" and "tripled" for the United States carry no source. Needed: the source and the intended threshold.

2. **Chapter 5, worked example.** The 3,420 a month is 18% of 19,000, which the text calls annual bean costs. A monthly bean cost of 19,000 exceeds the total monthly costs of 17,500 given in Step 1, and Chapters 9 and 13 put the bean order at 2,000 a month. The margins of Paths B, C and D (+2,580, +600, +4,200) are consistent with their own totals but do not follow from the prices: 4,200 cups at one dollar more, less 3,420, is +780. Needed: one consistent set of inputs. Figure 5.1 prints the margins 3,980, 2,000 and 5,600.

3. **Chapter 4, the value of lambda.** Remark 35 (2.0) and the worked example of Section 4.8 (2.59) use the ratio of edge weights. The Technical Appendix (1.7 to 1.86, then 2.23) uses the square-root form. All are compared with the same 2.25. Needed: which convention is the coefficient, and the numbers under it. The normalisation step in Section 4.8 adds 1.80 standardised units to a monetary term set to 1.0, which holds only if 24,000 dollars is one standard deviation. The "Observed lambda" column of the table in Section 4.2 has no source.

4. **Chapter 3, proof of Proposition 5.** The proof says the Mahalanobis component "contributes a net decrease in distance" and concludes from a positive total weight that the action is off the minimum-cost path. Neither step holds for a quadratic form. The statement was corrected (Reconciled 1). The proof needs the comparison with the alternative of not transacting.

5. **Chapter 13, Option B, and the sign of an improvement generally.** Option B's cost is written as the monetary term minus the squared evaluative gains. Definition 4 adds every squared displacement. With the squares added, Option B's quadratic form exceeds Option A's (2,000^2 against 960^2, and 1.41 against 1.10 on the other dimensions), so the ranking B, C, A does not follow from Definition 4 as it stands. The same gap is behind Reconciled 3 and Unresolved 4. Needed: where the direction of a displacement enters the cost (the goal region, or the Finsler metric of Section 4.10).

6. **Chapters 9 and 13, the bean prices.** Chapter 9 prices commodity beans at 18 dollars a pound (a saving of 7 a pound, 560 a month). Chapter 13 prices commodity beans at 12 and direct-trade beans at 18. Maria's gains from the order also differ between the two chapters. Changing Chapter 13 would change Figure 13.1.

7. **Chapter 9, running-example box.** The box about the rent payment says the geometric economist "also sees the 2.4 units of evaluative value created". The 2.4 belongs to the bean order worked out later in the chapter.

8. **Chapter 15.** Nordhaus is given a rate of 3% at the head of Section 15.2 and in the worked example, and a pure time preference of 1.5% with a total of 5.5% in the Ramsey decomposition. The solar table counts cash flows for years 1 to 8 of a panel the text gives a 25-year life. Over 25 years the same formula gives a net present value of about 48,000, not a marginal one. The opening box gives a payback of 8 years, and 30,000 over 4,500 is 6.7. Figure 15.1 draws the Stern and Nordhaus curves at 0.1% and 3%.

9. **Duplicate numbering.** Chapter 4 uses Theorem 34, Remark 35, Proposition 36, Theorem 37, Propositions 38 and 39. Chapter 8 uses Definitions 34 and 35, Remark 36, Theorems 37 and 38, Definition 39, Theorem 40, Definition 41, Proposition 42, Definition 43, Proposition 44, Remark 45, Definition 46, Proposition 47. Chapter 11 uses Definitions 38 and 39. Chapter 12 uses Proposition 40, Definition 41, Propositions 42 and 43. Renumbering is an editorial decision and would change the captions of Figures 11.1 and others that cite these numbers.

10. **The rent-increase vector.** Section 3.8 (accept the increase), Section 4.8 (loss path) and Chapter 6 (the lease vector L) give three different nine-component vectors for the rent rising to 7,000, including opposite signs on d2 between 3.8 and 4.8. A sentence now relates the first two. Figures 3.2 and 4.1 draw them as printed.

11. **GDP notation.** GDP is written as T_1 in Chapter 6, as T_11 and as a trace in the Chapter 6 appendix, and as a double sum of T^1_ij in the Chapter 1 appendix.

12. **Results with no record in this repository.** The replication "across 6 additional languages (Thiele, 2026)", and the Appendix C results (15 societies at MAE under 5%, 4.3% out-of-sample error on public goods, 13 of 17 prospect-theory problems, a WTA/WTP ratio of 1.66) come from the eris-econ library, which is outside this repository. They were left as written. The "16/16" and the "13 of 17" stand side by side in the Key Results table.

## Cross-volume repairs (2026-11-26)

These repairs come from the survey of the series for consistency between volumes (`cross-volume-report.md`, findings E1 to E13 and the series-wide items X1, X2, X3, X6 and S1) and the author's decisions on its [AUTHOR] items (`author-decisions.md`, rules G1 to G14). Each target was checked in the cited volume as it stands. *Geometric Ethics* means its version 1.29. No figure, caption or file under `tools/`, `figures/` or `.build/` was changed.

### Applied

- **Unresolved 12, the Thiele study, now settled.** Section 3.1 said "with a reported replication across 6 additional languages (Thiele, 2026)". *Geometric Ethics* v1.29 (§17.10a) reports the study as "reported by Thiele (2026, unpublished)", in six languages, English among them. The sentence now reads "and a further study in six languages reported by Thiele (2026, unpublished; *Geometric Ethics* §17.10a)".
- **Unresolved 12, "4.3% out-of-sample", now qualified.** In the Key Results table of Chapter 0, the row "Public goods: 4.3% out-of-sample prediction error" now reads "Public goods: 4.3% prediction error, labelled out-of-sample by eris-econ (no run record here; *Geometric Ethics* §20.7 says the published calibration is not held-out prediction)". *Geometric Ethics* §20.7 says the published calibration "reports cross-domain reuse of parameters ... not held-out prediction" and that its out-of-sample test (the stake invariance of ultimatum offers) fails. Appendix C, Section C.4, already says its runs have no record here and was not changed.
- **E1 (X1), the title of Volume 1.** "*Geometric Methods in Computational Modeling*" now reads "*Geometric Methods: Computational Modeling*": the preface (Chapter 0), the closing note on sources of Chapter 1, the References of Chapters 9 and 16, Appendix A (opening), and the README (list and map).
- **E2, the 3 × 3 derivation.** Section 3.1 said the nine dimensions come from "three normative modes (consequentialist, deontological, virtue-based) ... crossed with three evaluative scopes (individual, relational, institutional) ... nine independent dimensions", and the Technical Appendix of Chapter 1 ("Dimensional Count") said "three normative modes × three scopes". *Geometric Ethics* §5.3 crosses three ethical scopes (individual, relational, collective) with three epistemic modes (what matters, who decides, what we know), and calls the nine "a canonical engineering chart ... not a discovered empirical dimensionality". Both passages now say so. Section 3.1 adds that *Geometric Ethics* treats the nine as a chart chosen for coverage.
- **E3, the rank of Σ.** Section 3.7 posited a rank of about 9 "on the strength of the cross-lingual work reported in *Geometric Ethics*". That volume reports an effective rank of 5.19 of 8 for its validated axes (§5.3). The clause is removed. The sentence that says the posit is open now begins with that result, on moral text rather than economic behavior (*Geometric Ethics* §5.3, §20.11).
- **E4, Chapter 3, Notes on Sources.** "validated empirically in Chapters 6-8 of that work" now reads that the evidence and its limits are in Chapter 17 of *Geometric Ethics* and its §5.3 (eight of nine axes pass a frozen-null gate; rights-and-duties fails). *Geometric Ethics* Chapters 6 to 8 are the tensor hierarchy, the worked case and stratification.
- **E5, the origin of the BIP.** Section 8.1 said the principle was "developed in *Geometric Reasoning* ... and applied to ethics in *Geometric Ethics*". *Geometric Ethics* (Volume 2) states it as Axiom 5.1, and *Geometric Reasoning* (Volume 3) adopts it in Chapter 8. The sentence now says that.
- **E6, the gauge violation tensor.** Section 8.7 called the tensor "a direct analogue of the object defined in *Geometric Reasoning* (Ch. 8) and applied to ethics in *Geometric Ethics* (Ch. 17)". Neither volume defines one. *Geometric Reasoning*'s nearest object is the corruption tensor (its Chapter 5, read along gauge directions in Chapter 8). The BIP experiments of *Geometric Ethics* (§17.3) were run in a multilingual embedding model, not on people (§17.7). The sentence now says so, and "In ethics, the gauge violation tensor measures" now reads "In ethics, such a tensor would measure". "Measuring the Gauge Violation Tensor" now says the protocol adapts those experiments to human subjects, where it said it "mirrors" them.
- **E7, the No Escape Theorem.** Section 16.2 said *Geometric Ethics* "(Chapter 18) proves the No Escape Theorem". That volume's Theorem 18.1 is tagged conditional on four requirements. The sentence now names them.
- **E8 [AUTHOR], rule G4: "Bond Index" for different quantities.**
  - Section 4.4 defines BI(τ) as the relative change of the heuristic under one re-description. The name is kept, and a parenthesis now says it is a different quantity from the Bond Index of *Geometric Ethics*, Chapter 18: the mean of such deviations over the tested inputs and declared re-descriptions, divided by a tolerance. The tolerance is not written τ there, because τ is this chapter's re-description.
  - Corollary 9.1 said exploitation makes "the Bond Index ... non-zero", although exploitation is not a re-description. It now names the exploitation index of Proposition 9.3, as the report proposed (G4: the report's text where given).
  - Prediction 6 (Section 16.4) spoke of "transactions with high Bond Index". It now reads "transactions on which an evaluator shows a large gauge violation (Section 4.4, the deviation under one re-description)", in the wording of G4. Its pointer "the gauge-violation measure from Chapter 8" now reads "of Section 4.4", where the index is defined.
- **E9 [AUTHOR], rule G12: prospect theory.** Chapter 1 ("The Arc of the Book") said Chapter 4 "derives prospect-theoretic phenomena". The chapter opening of Chapter 4 said it "derives loss aversion -- and every other prospect-theory phenomenon --" and that "The metric is not a parameter to be fitted." *Geometric Ethics* §20.8 calls these readings, not derivations, and reports that sealed tests favoured cumulative prospect theory. Both now say "reads". The two closing sentences of the opening are replaced by "Sealed tests of reduced-form geometric models against cumulative prospect theory have so far favored prospect theory (*Geometric Ethics*, §20.8)." This is the summary in Chapter 4 to which G12 lets *Geometric Ethics* point.
- **E10 [AUTHOR], rule G12: the sealed test on this volume's chart.** Section 3.1 ("[Empirical.]") now ends "In a sealed test on moral-judgment data, learned coordinates outperformed a nine-axis codebook built on this chart (*Geometric Ethics*, §5.3)." *Geometric Ethics* §5.3 calls that codebook "the companion economics volume's chart".
- **E11, Scalar Irrecoverability.** The Chapter 6 notes said the three-part formulation "and the application to prospect-theoretic paradoxes" are original to *Geometric Ethics* Chapter 15. That chapter's Theorem 15.1 has the three parts and is conditional on Definition 5.2. Neither Chapter 15 nor Chapter 20 has the Allais or Ellsberg paradox. The note now cites Theorem 15.1, "conditional there on its nine-dimensional chart, a modeling axiom", and says that the application to the paradoxes is new here. The definition number is not written, because the series checker would read "Definition 5.2" as a definition of this book.
- **E12 [AUTHOR], rule G3: debiasing.** Section 8.8 cited *Geometric Reasoning* Chapter 14 for "heuristic augmentation". That chapter is data augmentation, and heuristic correction is its Sections 11.3 and 11.7.1. It now cites "Chs. 11 and 14".
- **E13 [AUTHOR], rule G7: the subtitle.** The README title now gives the subtitle of the title page and the series build, "Decision Manifolds, Equilibria, and the Geometry of Markets". It had "Decision Manifolds, the Bond Geodesic Equilibrium, and the Irrecoverable Geometry of Markets", which `books.json` also carries; the portal is changed separately.
- **Keys.** "(Bond, 2026)" for *Geometric Ethics* now reads "(Bond, 2026b)", the key the preface assigns, in Sections 3.1 and 8.1, the Chapter 3 notes on sources, and the Chapter 2 and Chapter 4 notes on sources.
- **README (X2, X3, X1).** The series table now lists the fourteen volumes in series order. Ethics reads "Published (v1.29)". Economics, Communication and Medicine carry the subtitles of the series build (G7). A last row is added for *Geometric Observation*, with the status "Draft" (G8). In the map, the Methods node reads "Geometric Methods / Computational Modeling", and a node for *Geometric Observation* stands in the parent-framework subgraph, with no edge (G8).
- **S1 [AUTHOR], rule G8: the license paragraph.** It now reads "Claims in this series carry status labels, such as `[proved]`, `[posited]` or `[open]` or a volume's own tags, graded against a claim ledger where the volume keeps one".
- **Unpublished files (X6, X1, G7, G9, G12).**
  - `front_matter.md`, Series Foreword:
    - *Geometric Ethics* is Book 2 and *Geometric Reasoning* Book 3; they were numbered 3 and 2.
    - The Methods title follows X1.
    - "with its $D_4 \times U(1)_H$ symmetry group" is now history (G9): "It once gave the manifold's symmetry group as $D_4 \times U(1)_H$; it withdrew $D_4$ in version 1.25 (the group of the two demonstrated operations is $V_4$)."
    - "It predicts them, from geometry alone." now reads "It reads them as geometric properties." (G12).
  - `backmatter/bibliography.md`, The Geometric Series:
    - 2026b is now *Geometric Ethics* [Book 2] and 2026c *Geometric Reasoning* [Book 3], the keys the chapters use. The two had been swapped.
    - The Methods title follows X1.
    - *Geometric Law* and *Geometric Cognition* carry the subtitles of their title pages: "Symmetry, Invariance, and the Structure of Legal Reasoning" and "The Mathematical Structure of Human and Artificial Thought".

### Recorded, not changed

- `front_matter.md` (unpublished) still carries the Key Results row "Public goods: 4.3% out-of-sample prediction error", which is qualified in Chapter 0 above.
- The bibliography of the series volumes still stops at Book 8. No chapter cites a later volume by key.
- Chapter 1, "The Dimensional Hypothesis" ("Chapter 4 derives this prediction") is about the range of λ in this volume's own model, not prospect theory, and was left.

### Figures and captions

None is made stale. No figure draws the passages above.

## Appendices published (2026-11-26)

The appendices went online with the survey (chapters cite them). Repairs made when they were added:

- Appendix C, Section C.4, opens with a status note: its results come from runs of the framework against published data with parameters calibrated per dataset; the runs are not in this repository and the volume does not reproduce them, so the results are reported without a run record; the registered coupling test failed (Chapter 16, Section 16.1).
- Appendix B cited 'Definition 3.1' and 'Definition 4.2'; the book numbers these Definitions 3 and 4.
