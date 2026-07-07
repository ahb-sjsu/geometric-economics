# codebook-v1 — The Nine Coordinates of the Economic Decision Manifold

**Bundle component of `prereg-dimensions-v1`.** Frozen with the protocol; part of the hashed content.

## Encoding convention (shared by all coordinates; identical to `projection-gap/contrasts.py`)

Each coordinate d_k is **bipolar** with a pre-committed orientation:

- The **aligned pole** ("+"): the option *honors* the value named by d_k.
- The **violating pole** ("−"): the option *acts against* that value.
- A scenario's Δ**a** places each option on d_k by how far it sits toward the violating pole when the
  coordinate is made salient. In a projection-gap pair, **option A is the coordinate-aligned option**
  and option B is the alternative; at the low pole neither option engages d_k (Δ ≈ 0), at the high
  pole the violating option B carries the moral-friction cost.

**Sign invariance.** Because the coordinate is bipolar and the metric enters as a squared cost,
Part II Theorem 2 guarantees the *sign* of every prediction is invariant to any monotone re-encoding
of d_k; only the orientation (which pole is "aligned") is a modeling choice, and it is fixed here,
once, per coordinate, by the anchors. The unit interval [0, 1] is the displacement between the two
anchor scenarios below (the "moral-friction unit" m of `contrasts.py`).

The **model's predicted sign** follows mechanically from this orientation (see the sign table in
`prereg-dimensions-v1.md` §5): making the value salient raises the cost of the *violating* option, so
the aligned option gains probability (projection-gap Δ > 0) and a move toward the violating pole must
be compensated by money (marginal price p_k > 0). The single registered exception is d9 under losses.

---

## d1 — Money (numeraire)
- **Construct.** Own monetary payoff. The unit of account against which all other coordinates are priced.
- **Orientation.** Aligned = more money to self. No activation test; calibration only.
- **Anchors.** 0 = the menu's lowest own-payoff option; 1 = a +\$1 move (per-dataset rescaled).
- **Non-examples.** Not "social impact of money" (that is d6); not "fairness of the split" (d3).

## d2 — Rights
- **Construct.** Whether an option *upholds vs. violates a basic entitlement or protected liberty of a
  person* (bodily integrity, due process, a promised entitlement, a civil liberty), independent of the
  material payoff.
- **Orientation.** Aligned = the option that respects the right; violating = the option that infringes
  it for private gain.
- **Anchors.** 0 = an action with no rights content (a neutral market trade); 1 = the same trade whose
  execution requires overriding one identified person's explicit protected entitlement.
- **Non-examples.** Not mere *unfairness of division* (that is d3 — a right can be violated in a
  perfectly equal split); not *loss of one's own choice* (that is d4). Rights concern a **third party's
  protected claim**, not the allocation ratio and not the agent's own agency.
- **Lexicographic contingency (see §5 D2, §9).** May refuse a finite price; the priced branch orients
  as above.

## d3 — Fairness
- **Construct.** The distance of an allocation from the procedurally/ distributively fair benchmark for
  the parties (equal split, equity by contribution, or the paradigm's fair reference).
- **Orientation.** Aligned = the fair(er) allocation; violating = the unfair(er) allocation that favors
  self at others' expense.
- **Anchors.** 0 = equal (or equity-fair) split; 1 = the maximally self-favoring split the menu allows.
- **Non-examples.** Not *total social welfare* (that is d6 — a fair split can have low aggregate
  impact); not *a rights violation* (d2 — an unfair split need not breach an entitlement).

## d4 — Autonomy
- **Construct.** Whether an option *preserves vs. surrenders the decision-maker's own control / decision
  rights* over a consequential choice, beyond its expected-value consequences.
- **Orientation.** Aligned = retain one's own decision rights; violating = delegate/cede control (even
  when delegation has weakly higher expected value — the *control-premium* design).
- **Anchors.** 0 = a choice made by the agent directly; 1 = the identical expected-value choice made by
  an external party on the agent's behalf without recourse.
- **Non-examples.** Not *a third party's rights* (d2 — autonomy is the agent's OWN agency); not
  *legitimacy of the authority* one defers to (d8 — one can lose autonomy to a perfectly legitimate
  authority).

## d5 — Privacy / Trust (pre-registered as possibly two coordinates)
- **Construct (5a, trust).** Whether an option *honors vs. betrays* trust placed by/in a counterpart
  (reciprocating vs. defecting on entrusted resources).
- **Construct (5b, privacy).** Whether an option *protects vs. discloses* a person's private
  information.
- **Orientation.** Aligned = honor trust (5a) / protect privacy (5b); violating = betray (5a) /
  disclose (5b).
- **Anchors (5a).** 0 = no trust extended; 1 = maximal entrusted amount fully appropriated.
  **(5b).** 0 = no private information at stake; 1 = full disclosure of an identified private fact.
- **Non-examples.** Trust ≠ *fairness of the returned amount* (d3); privacy ≠ *a legal right to privacy*
  (d2 — 5b is the felt cost of disclosure, tested for whether it separates from trust).

## d6 — Social impact  *(active; panel-confirmed, `prereg-v1`)*
- **Construct.** The magnitude/direction of an option's externality on parties beyond the
  decision-maker (a recipient, a community, the public).
- **Orientation.** Aligned = the option with the better social externality; violating = the option that
  imposes a worse externality for the same own-payoff.
- **Anchors.** 0 = identical own-payoff options with no differential externality; 1 = one option imposes
  a defined harm on an identified other at no change to own payoff.
- **Non-examples.** Not *fairness to the counterpart in the split* (d3 — impact can fall on
  non-transacting third parties); not *virtue of the actor* (d7).

## d7 — Virtue / identity  *(active; panel-confirmed, `prereg-v1`)*
- **Construct.** Consistency of an option with the agent's moral self-image / role identity (honesty,
  role duty), independent of payoff.
- **Orientation.** Aligned = the identity-consistent act (e.g., an honest report); violating = the
  self-serving act that contradicts the identity (a dishonest report for money).
- **Anchors.** 0 = an act with no identity content; 1 = the payoff-maximizing act that requires an
  explicit dishonesty/role-breach.
- **Non-examples.** Not *harm to others* (d6 — one can lie with no external victim); not *fairness*
  (d3). d7 is about the **actor's own** integrity.

## d8 — Legitimacy
- **Construct.** Whether the authority/procedure that an option complies with (or defies) is legitimate
  — lawfully constituted, consented-to, or duly elected — holding the material incentive fixed.
- **Orientation.** Aligned = comply with a *legitimate* directive / defy an *illegitimate* one;
  violating = comply with an *illegitimate* directive (or defy a legitimate one) for private gain.
- **Anchors.** 0 = an incentive with no authority framing; 1 = the identical incentive issued by an
  explicitly illegitimate (unelected/unlawful/coercive) source.
- **Non-examples.** Not *the agent's own autonomy* (d4 — legitimacy is a property of the external
  authority); not *a rights violation by that authority* (d2, though they can co-occur — the codebook
  requires the legitimacy manipulation to hold rights content fixed).

## d9 — Epistemic status  *(active; panel-confirmed, `prereg-v1`; loss-domain sign reversal registered)*
- **Construct.** The clarity/quality of the information on which an option rests (source reliability,
  evidence quality, ambiguity of probabilities), holding the monetary structure identical.
- **Orientation (gain domain).** Aligned = the epistemically clearer option; violating = the vaguer one.
  **Loss domain: reversed** — clarity is aversive under losses, so the displacement lands on the clear
  option (the registered sign flip; see §5 D9 and `contrasts.py` B1L).
- **Anchors.** 0 = numerically identical outcomes/probabilities with equal clarity; 1 = the same
  outcomes with one option's source made explicitly vague/ambiguous.
- **Non-examples.** Not *trust in a person* (d5a — d9 is about evidence quality, not a counterpart's
  trustworthiness); not *risk magnitude* (the money/lottery structure is held identical).
