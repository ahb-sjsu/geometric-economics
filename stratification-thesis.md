# The stratification thesis

*A claim document for the Geometric Decision Theory campaign. Companion to
`nobel-program.md`, which sets the strategy, and to `nobel-roadmap.txt`, which
sets the theorem package. Written 2026-09-12. Nothing here has been tested.*

---

## 0. Why this file exists

The thesis below was carried verbally for some time and was written down nowhere.
A search of every repository under `C:\source`, of the whole memory, and of every
session transcript returned no occurrence of the words Whitney or stratified in
this sense. A framing that exists only in one person's head is one forgotten
afternoon from being lost, and this campaign has already spent effort recovering
work that went missing for exactly that reason. That is the whole reason for the
file, and it is worth more than the polish of what follows.

## 1. The claim

> **Stratification thesis.** The space on which a decision is made is not a smooth
> manifold carrying one metric. It is a Whitney stratified space, a union of
> smooth pieces of differing dimension glued so that each piece lies in the
> closure of higher-dimensional ones and so that tangent planes behave regularly
> in the limit. A decision is the selection of a least-cost path through that
> space under the evaluator's metric. Choice behaviour is therefore governed by
> which stratum the problem sits on, and the phenomena that scalar theories
> record as anomalies are the signature of paths meeting a wall.

Two consequences separate this from the campaign's current framing, in which the
consequence space is a single smooth space carrying a shared low-rank metric.

**Effective dimension is local, not global.** On a stratified space the rank of
the metric is a property of the stratum. A programme that fits one rank to
everything is averaging over pieces that have different ones, and a rank that
transfers within a region and fails across a boundary is what that looks like from
the outside.

**Least-cost paths need not vary smoothly with their endpoints.** On a smooth
Riemannian manifold the minimising path is a geodesic and moves smoothly as the
endpoints move. On a stratified space it need not. The minimiser can be pinned to
a lower-dimensional stratum across an open set of endpoints, in the way a shortest
path on a polyhedron runs along an edge, and it can change stratum discontinuously
under a smooth change of the problem. Behaviour is then flat over a range of
conditions and then jumps, rather than responding in proportion throughout.

The mathematics is well posed. Riemannian structures on stratified spaces are
defined and admit a geodesic distance, so least-cost path length is a real object
here and not a metaphor.

## 2. What the campaign has already seen, and why none of it tests this

Four results in the record read naturally under the thesis. This is the reason to
take it seriously and it is also the reason none of them can be evidence for it.

| Result in the record | Reading under the thesis |
|---|---|
| D₄ rotation test. The fourfold `d·q` term dominates on the Kahneman and Tversky corners at B = 0.80 and vanishes in the CPC18 mixed-gamble interior at +0.003. Recorded as "rectangle not square, no continuous rotation" | A term that lives on the corners and not in the interior is a structure carried by a lower-dimensional stratum |
| V₄ held-out test failed 0 of 3. The pure interaction is absent on representative gambles, so V₄ is specific to the curated problem set and not to risky choice in general | The same reading. V₄ is the local symmetry of one stratum rather than of the ambient space |
| Low-rank Σ transfers at about 99 percent within domain and at 0 percent from gain to loss | A stratum boundary, with the rank a local property either side of it |
| The share-normalized model has a stake boundary, which `prereg-boundary-v1` is frozen to locate | A wall, with a measurable position |

**These four are the discovery set.** The thesis was suggested by them, so scoring
it on them would be fitting and reporting the fit. The campaign's own standing
lesson is that held-out tests keep killing the attractive overclaims and that the
survivors are the pillars, and the fastest way to make this thesis another
casualty is to present rows one and two, currently filed as clean negatives, as
though they were confirmations. They are not. They are the reason to register a
prediction.

## 3. The prediction that is specific to Whitney, and to nothing else

Stratification alone is weak. Any space can be cut into pieces after the fact, and
a decomposition chosen once the anomalies are known explains nothing. What gives
the thesis content is the regularity condition, because it constrains the
behaviour of the fitted metric near a boundary before the boundary is crossed.

Whitney's condition (a) says that if a sequence of points in an open stratum
approaches a point of a lower stratum, and the tangent planes along that sequence
converge, then the limit plane contains the tangent space of the lower stratum.

The behavioural translation is direct and is testable with the campaign's existing
instruments.

> **Prediction W.** Fit the local metric at a sequence of decreasing distances
> from a known boundary, from the interior side. As the distance falls, the
> leading eigendirections of the fitted metric converge, and the limiting span
> contains the directions along the boundary. Under any decomposition that is not
> Whitney regular, the limiting span need not contain them, and under a single
> smooth metric there is no distinguished limit at all because the metric does not
> vary with position.

This is a quantitative, signed, pre-registerable claim about a quantity nothing in
the campaign has yet computed. It uses a boundary the campaign has already located
independently, so the boundary is not chosen to make the prediction work. Two
boundaries are available now. The gain to loss boundary, where transfer is already
measured at 0 percent, and the stake boundary that `prereg-boundary-v1` is frozen
to locate on three high-stakes ultimatum datasets.

**What refutes it.** Leading directions that converge to a span not containing the
boundary directions refute Whitney regularity, and the thesis with it, leaving at
most an uninteresting decomposition. Leading directions that do not converge at
all refute the stratified reading outright. A fitted metric whose leading
directions are constant in position, with rank unchanged either side of a located
boundary, refutes the thesis in favour of the campaign's current single-metric
framing.

**What would make it vacuous rather than false.** If every direction is in the
limiting span, the containment holds trivially. The registration has to fix in
advance a rank for the limiting span that is strictly below the ambient dimension,
or the test proves nothing.

## 4. The objection that will be made first

This will be read as catastrophe theory returning, and the reading is not unfair,
since singularity theory applied to economic behaviour is exactly what Thom and
Zeeman proposed in the nineteen seventies. That programme collapsed. It was
attacked for classifying phenomena qualitatively after the fact, for fitting
pictures rather than predicting numbers, and for treating a topological
possibility as an empirical finding, and the field has not forgotten.

The answer is not that this thesis is a different piece of mathematics, because it
is a close relative. The answer is the one thing catastrophe theory in economics
did not have and this campaign does. Predictions fixed in advance, scored by a
grader written before the data are read, with the failures kept. Prediction W is
a number with a sign and a bar, not a shape that resembles a cusp. If the
programme cannot produce results in that form it deserves the same fate, and
saying so in the paper is cheaper than having a referee say it.

The literature check run on 2026-09-12 found no existing application of Whitney
stratification to choice behaviour, preference, or decision theory. The nearest
neighbours are catastrophe theory in economics, which is the cautionary case
above, and low-dimensional manifold models of decision dynamics in neuroscience,
which assume smoothness rather than test it. The framing appears unclaimed, which
is worth little on its own and is worth stating so that the claim of novelty in
any paper is narrow and survives contact with a referee.

## 5. Where this sits in the campaign

It does not displace anything. The two results that carry the programme, the
pre-registered low-rank Σ with three held-out legs and the encoding-invariant
projection-gap experiment, are
within-stratum results and stay exactly as they are. The thesis is a claim about
what lies between the regions those results describe, and it makes the campaign's
recorded failures informative rather than merely recorded, which is the same move
the boundary paper already makes for the share-normalized model.

The status is that this is a conjecture with one designed test and no data.
It earns a place in the programme if Prediction W is registered and run, and it
earns nothing at all until then.

## 6. Next steps, in order

1. Choose the boundary. The gain to loss boundary is available immediately and has
   a measured transfer failure to anchor it. The stake boundary is cleaner but
   waits on `prereg-boundary-v1` being run.
2. Write the estimator for the local metric at a distance from a boundary, with
   the limiting-span rank fixed in advance, and a grader that reads the
   containment and the convergence separately.
3. Pilot on data already used, to establish that the estimator recovers a known
   answer and to fix the tolerances. Pilots do not test the claim.
4. Register, seal, run on held-out data, and keep the verdict whichever way it
   falls.
