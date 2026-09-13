# The stratification thesis

*A claim document for the Geometric Decision Theory campaign. Companion to
`nobel-program.md`, which sets the strategy, and to `nobel-roadmap.txt`, which
sets the theorem package. Written 2026-09-12, corrected the same day.*

---

## 0. What this file is, after a correction

The first version of this file opened by asserting that the thesis below existed
in no file anywhere, and made that the reason for writing it down. **That was
wrong.** The search behind it timed out at 110 seconds and returned nothing, and
an empty result from a killed process was read as an absence. The framework is
established across the corpus, in four places at least.

| Where | What is there |
|---|---|
| `geometric-ethics`, Chapter 8 | The full formal treatment. Definition 8.1 stratification with the frontier condition and local finiteness, **Definition 8.2 Whitney condition (A)**, Definition 8.3 Whitney condition (B), attributed to Whitney 1965, followed by a taxonomy of boundary types and a worked consent example |
| `erisml-lib`, `Geometric_Ethics_Foundational_Paper.tex` | The space of ethically relevant configurations modelled as a Whitney stratified space, with rights violations as the discontinuities. Whitney stratification is a listed keyword |
| `sqnd-probe`, `Non_Abelian_SQND_Bond_2026_v4_1.md` | Stratified Quantum Normative Dynamics. D₄ lattice gauge fields on a stratified lattice, stratified phase transitions, a boundary Higgs mechanism |
| `geometric-economics`, `ch01` and `front_matter` | Geometric economics already described as using stratified spaces, on a nine-dimensional stratified moral manifold with a D₄ × U(1) symmetry group |

So the thesis is not unrecorded and this file does not introduce it. What follows
is narrower and is, I think, the thing actually missing.

## 1. What is actually missing

**The framework and the campaign are not connected.** Chapter 8 develops the
stratified structure in full and the GDT experiments were designed, run, and
recorded without reference to it. The consequence is visible in the record.

- The **D₄ rotation test** in this repository found that the fourfold `d·q` term
  dominates on the Kahneman and Tversky corners at B = 0.80 and vanishes in the
  CPC18 interior at +0.003, and filed it as a clean negative, "rectangle not
  square, no continuous rotation". Meanwhile `sqnd-probe` builds D₄ lattice gauge
  fields **on a stratified lattice**. These two results are about the same group
  on the same kind of space and neither cites the other.
- The **V₄ held-out test** failed 0 of 3 and concluded that V₄ is specific to the
  curated problem set rather than to risky choice in general. Under Chapter 8 that
  sentence describes a symmetry carried by one stratum, which is what a stratified
  space predicts and not a defect.
- The **gain to loss transfer failure** at 0 percent, against about 99 percent
  within domain, is a stratum boundary with the rank local to each side.
- `prereg-boundary-v1` was written to locate a wall and does not use the word.

The claim of this file is therefore not that decisions are path finding on a
Whitney stratified space. Chapter 8 says that already. The claim is that **the
campaign has been measuring stratification for a year without naming it, and that
naming it turns three recorded negatives into a positive prediction that can be
registered.**

## 2. The thesis as it applies to decisions

Chapter 8 states the structure for moral space. The extension asserted here is
that it governs decision space generally, so that the GDT consequence space is
not a single smooth manifold carrying one shared metric.

> **Stratification thesis, decision form.** The space on which a decision is made
> is a Whitney stratified space in the sense of Definitions 8.1 to 8.3. A decision
> is the selection of a least-cost path through it under the evaluator's metric.
> Which stratum the problem sits on governs behaviour, the effective rank of the
> metric is a property of the stratum rather than of the space, and least-cost
> paths need not vary smoothly with their endpoints because a minimiser can be
> pinned to a lower-dimensional stratum over an open set of conditions.

Two consequences separate this from the campaign's current framing, in which one
shared low-rank metric covers everything.

**Effective dimension is local.** A programme that fits one rank to everything is
averaging over pieces with different ones. A rank that transfers within a region
and fails across a boundary is what that looks like from outside, and the campaign
has measured exactly that.

**Behaviour is flat and then jumps.** On a smooth manifold the minimising path is
a geodesic and moves smoothly with its endpoints. On a stratified space it can be
pinned, in the way a shortest path on a polyhedron runs along an edge, and can
change stratum discontinuously under a smooth change of the problem.

## 3. What none of the existing results can do

Four results read naturally under the thesis and that is the reason to take it
seriously. It is also the reason none of them is evidence for it. They are the
discovery set. The campaign's standing lesson is that held-out tests keep killing
the attractive readings and that the survivors are the pillars, and presenting the
D₄ and V₄ negatives as confirmations is the fastest way to make this the next
casualty. A registered prediction is needed.

## 4. The prediction, which is Definition 8.2 made behavioural

Stratification alone is weak, since any space can be cut into pieces after the
fact. The content is in the regularity condition, because it constrains the
fitted metric near a boundary before the boundary is crossed. Chapter 8 states it.

> **Definition 8.2, Whitney condition (A).** For strata `S_α ⊂ closure(S_β)` and a
> sequence in `S_β` converging to `x ∈ S_α`, if the tangent spaces converge to a
> limit `τ`, then `T_x S_α ⊂ τ`.

The behavioural translation is the new part of this file and is testable with the
campaign's existing instruments.

> **Prediction W.** Fit the local metric at a sequence of decreasing distances from
> a located boundary, from the interior side. As the distance falls the leading
> eigendirections converge, and the limiting span contains the directions along the
> boundary. Under a decomposition that is not Whitney regular the limiting span
> need not contain them, and under a single smooth metric there is no distinguished
> limit at all because the metric does not vary with position.

**What refutes it.** Convergence to a span that does not contain the boundary
directions refutes Whitney regularity and the thesis with it. No convergence at all
refutes the stratified reading outright. A fitted metric constant in position, with
rank unchanged either side of a located boundary, refutes the thesis in favour of
the campaign's current single-metric framing.

**What makes it vacuous rather than false.** A limiting span of full rank satisfies
the containment trivially. The registration must fix a rank strictly below the
ambient dimension in advance or the test proves nothing.

**Where to run it.** Two boundaries are located independently of the prediction.
The gain to loss boundary, with transfer already measured at 0 percent, and the
stake boundary, which `prereg-boundary-v1` has now put on the responder side.

## 5. The objection that will be made first

This will be read as catastrophe theory returning, and the reading is not unfair,
since singularity theory applied to economic behaviour is what Thom and Zeeman
proposed in the nineteen seventies. That programme collapsed. It was attacked for
classifying qualitatively after the fact, for fitting pictures rather than
predicting numbers, and for treating a topological possibility as an empirical
finding.

The answer is not that this is different mathematics, because it is a close
relative. The answer is the thing that programme lacked and this campaign has.
Predictions fixed in advance, graded by code written before the data are read,
with the failures kept. Prediction W is a number with a sign and a bar. If the
programme cannot produce results in that form it deserves the same fate, and
saying so first is cheaper than having a referee say it.

An external literature check on 2026-09-12 found no application of Whitney
stratification to choice behaviour outside this corpus. The nearest external
neighbours are catastrophe theory in economics, above, and low-dimensional
manifold models of decision dynamics in neuroscience, which assume smoothness
rather than test it. Any novelty claim in a paper should be stated at that width
and no wider, and should cite Chapter 8 as the prior statement within the corpus.

## 6. Next steps, in order

1. Reconcile the D₄ results. `sqnd-probe` has D₄ on a stratified lattice and this
   repository has a D₄ rotation test that failed. Determine whether they disagree
   or whether the rotation test refutes D₄ on the interior while the lattice work
   concerns the corners, which the stratified reading would predict.
2. Choose the boundary for Prediction W. The gain to loss boundary is available
   now. The stake boundary is now located on the responder side.
3. Write the estimator for the local metric at a distance from a boundary, with
   the limiting-span rank fixed in advance, and a grader that reads convergence and
   containment separately.
4. Pilot to fix tolerances. Pilots do not test the claim.
5. Register, seal, run on held-out data, keep the verdict.

## 7. Record of the correction

The first version of this file, and the commit message that introduced it
(`afd2f2e`), both assert that the thesis was written down nowhere. Both are
wrong, for the reason in Section 0. The commit is pushed and is not being
rewritten, so the error stands in the history and this section is the correction.
