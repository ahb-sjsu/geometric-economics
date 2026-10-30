# Theory paper: statements and proofs (working core)

Started 2026-10-30. Supersedes the theorem list of `../paper_00_theory.md`. Plan and the
statement-to-test map are in `../COMPANION-PLAN.md`. Prose is not written here. This file holds
the mathematics, so it serves either drafting route if the venue restricts AI-written text.

## Setup

Options are points `x` in `R^n`. A reference `r` fixes the status quo and `Delta(x) = x - r`.
`P` is a symmetric positive-semidefinite precision matrix. Cost `C(x) = sqrt(Delta(x)' P Delta(x))`.
Choice from a finite menu `X` is logit in minus cost,

    Pr(x; X) = exp(-C(x)/T) / sum_{y in X} exp(-C(y)/T),   T > 0.          (1)

A **projection model** reads an option only through a statistic `pi : R^n -> R^m`: its choice
probabilities satisfy `Pr(x; X) = G(pi(x), {pi(y) : y in X})` for some `G`. Expected utility, Nash
or payoff models, inequality aversion and CPT over stated outcomes and probabilities are projection
models, each with its own `pi`. A coordinate `z` is **discarded** by `pi` if `z` is not a function of
`pi` on the option set.

## Remark (scalarity is not the issue)

The injection theorem (`lean/ScalarIrrecoverability.lean`) says no continuous map from a real normed
space of rank above one into `R` is injective. It is true and machine checked. It does not imply that
scalar utility fails for multi-attribute choice. Debreu (1954) gives every continuous complete
preorder on a connected separable space a continuous utility, and (1) itself contracts each option to
the scalar `C(x)` before choosing. What a scalar model can get wrong is which coordinates its scalar
depends on. The paper's target is a projection that omits a coordinate behavior responds to.

## Proposition 1 (limiting correspondence)

Encode the monetary coordinate as payoff loss, `Delta_1(s_i) = K - u_i(s_i, s_-i)`, with every other
coordinate inactive. Then (1) is logit response in payoffs at scale `T` times `sqrt(P_11)`, its fixed
points are logit quantal response equilibria (McKelvey and Palfrey 1995), and as `T -> 0` their limit
points are Nash equilibria.

*Proof.* With one active coordinate and `Delta_1 >= 0`, `C(s_i) = sqrt(P_11) (K - u_i)`, so
`-C/T = (sqrt(P_11)/T) u_i - const`, which is the logit response with precision `sqrt(P_11)/T`. The
rest is McKelvey and Palfrey's limit result. []

Containment only. This proposition carries no evidence that the larger model is true.

## Theorem 1 (matched designs test projections, singly and jointly)

(a) A model's choice probabilities factor through `pi` if and only if every pair of menus that agree
under `pi` element by element yields equal choice probabilities.

(b) Let `pi_1, ..., pi_m` be the statistics of several projection models. A pair of options that every
one of them treats as identical, but that differs on a coordinate `z`, exists if and only if `z` is
not a function of `(pi_1, ..., pi_m)` on the option set. On any such pair every one of the `m` models
predicts equal choice probabilities.

*Proof.* (a) If `Pr = G o pi`, equal statistics give equal probabilities. Conversely, if equal
statistics always give equal probabilities, define `G` on the image of `pi` by
`G(pi(x)) = Pr(x)`, which is well defined. (b) `z` fails to be a function of `Pi = (pi_1..pi_m)` iff
some fiber of `Pi` contains two points with different `z`, and those two points are the pair. On it
each `pi_i` agrees, so each model predicts equality by (a). []

Part (a) unpacks a definition and is stated for reference. Part (b) is the design rule. It says which
manipulations force the whole incumbent set to the same null at once. It also bounds the design: a
null on finitely many pairs fails to refute `pi`-sufficiency and does not certify it.

## Theorem 2 (sign identification, any menu size, any direction)

Fix a menu and an alternative `A` with displacement `delta` in the low menu. The high menu changes only
`A`, moving its displacement to `delta + t v` for a direction `v` and a step `t > 0`. Write
`<x, y>_P = x' P y`. If

    <v, delta>_P >= 0   and   <v, v>_P > 0,                                  (2)

then `C_A(X_hi) > C_A(X_lo)` and `Pr(A; X_hi) < Pr(A; X_lo)` for every `T > 0`, whatever the number
of alternatives in the menu.

*Proof.* `C_A^2(t) = <delta + t v, delta + t v>_P = C_A^2(0) + 2t <v, delta>_P + t^2 <v, v>_P`, which
exceeds `C_A^2(0)` under (2). Writing `Pr(A) = [1 + sum_{B != A} exp((C_A - C_B)/T)]^{-1}` with every
`C_B` unchanged, `Pr(A)` falls. []

Condition (2) says the manipulation points away from the reference in the metric's own inner product.
It is checkable on any estimated `P`, in hand-specified or learned coordinates.

**Coordinate case.** For `v = e_d` and `delta_d > 0`, (2) reads `P_dd delta_d + c >= 0` with
`c = sum_{j != d} P_dj delta_j`, the cross-term. With no cross-term it holds whenever `A` moves further
from the reference on `d`. This is weaker than the bound `|c| <= P_dd delta_lo` of the first draft of
this file, which it replaces.

**Corollary (re-encoding).** Let `g` be any strictly increasing map applied to coordinate `d`, with
displacements recomputed as `g(a) - g(r_d)`. The hypothesis "the high menu moves `A` further from the
reference on the same side" holds under `g` whenever it holds before, because a strictly increasing
map preserves the sign and the order of differences from `g(r_d)`. So the predicted sign is the same
in every encoding in which (2) holds. With no cross-term on `d` (`c = 0`), (2) holds in every encoding
and the sign is fully encoding invariant. With cross-terms, (2) must be checked in the encoding the
metric is estimated in, and it is not itself invariant.

**Learned coordinates.** Nothing above uses the meaning of the coordinates. For any encoder
`phi` from descriptions to `R^n`, set `Delta(x) = phi(x) - phi(r)` and every statement holds as
written. In a learned chart a manipulation is the displacement `v = phi(x_hi) - phi(x_lo)` of `A`'s
description, and (2) is computed from the fitted `P`. Two things change. A full `P` on hundreds of
dimensions cannot be estimated from choice data, so a rank restriction becomes a requirement rather
than a hypothesis. And by Proposition 2 only the direction of `P` is identified, so a learned metric
is compared across data sets by its row space, not its entries.

Two corrections to earlier drafts follow. Part II's revised draft restricted the sign argument to
binary menus. The restriction is unnecessary, because `Pr(A)` falls in `C_A` for any menu. The
flagship's Theorem 3 assumed no cross-term. Condition (2) replaces that assumption with a checkable
inequality, which matters because Part II reports that the metric has off-diagonal structure.

Magnitude is not invariant under `g`. Only the sign is.

**Distinguish from Bond and Lang (2019, JPE 127(4)).** They show that comparing group means on an
ordinal response scale can be reversed by a monotone transformation unless the latent distributions
are stochastically ordered. That concerns a coded OUTCOME. Theorem 2 concerns a coded STIMULUS
attribute, and the outcome is a choice frequency with natural units, so their reversal does not
apply. The paper must say this in one sentence, because a referee will raise it.

## Proposition 2 (what the data identify: shape, not scale)

Choice probabilities under (1) depend on `(P, T)` only through `P / T^2`. For any `s > 0`, `(P, T)`
and `(s^2 P, s T)` give identical choice probabilities on every menu.

*Proof.* `C/T = sqrt(Delta' P Delta)/T = sqrt(Delta' (P/T^2) Delta)`. []

**Corollary.** The direction of `P` in the space of precision matrices, for example the ratio
`sigma_ev : sigma_sd` that Part II calls the aversion angle, is identified. Its magnitude is
identified only relative to `T`. Two domains measured in different payoff units can share a shape
while their magnitudes are incomparable. Transferring the shape and recalibrating one scale per
domain transfers exactly the identified quantity. This is the scale normalization familiar from
logit models (Train 2009), applied to the metric.

## Proposition 3 (stake enters only through the monetary encoding)

Let the stake `Lambda` enter the encoding only through the monetary coordinate.
(a) If money is encoded as a share of the stake, every displacement is independent of `Lambda`, and
choice probabilities are invariant to `Lambda` for every `P` and `T`.
(b) If money is encoded in income units, `s_1 = (Lambda / Y) q(x)`, choice probabilities depend on
`Lambda` and `Y` only through `Lambda / Y`.

*Proof.* (a) Nothing in (1) depends on `Lambda`. (b) `Lambda` and `Y` enter only through `s_1`, and
`s_1` depends on them only through the ratio. []

Part I's stake-invariance corollary is (a). It holds for every monetary variance, so the Andersen
rejection refutes the encoding and the metric together, as Part I says. (b) is Part I Section VII.A's
construction, tested in `../boundary/` (`prereg-boundary-v1`). Its level prediction, that equal
`Lambda/Y` gives equal offers, was already false in the pre-freeze descriptives and was recorded as
falsified before registration. The registered responder-side predictions are what the run tested.

## Proposition 4 (direction differences identify boundary penalties)

Let the cost of moving from state `a` to state `b` be
`w(a -> b) = sqrt((b - a)' P (b - a)) + sum_k beta_k 1[boundary k crossed going a -> b]`
(geometric-methods Chapter 6, Definition 6.1). Then

    w(a -> b) - w(b -> a) = sum_k beta_k (1[k crossed a -> b] - 1[k crossed b -> a]).

*Proof.* The Mahalanobis term is symmetric in `a` and `b`. []

The metric cancels exactly, so no `P` has to be estimated and every symmetric confound subtracts out.
This is the identification behind `../d4transition/` (`prereg-d4transition-v1`, sealed, no data).

## Proposition 5 (fixed information price)

In Matejka and McKay (2015), an agent paying information cost `lambda` per nat chooses `i` with
probability `P0(i) exp(v_i / lambda) / sum_j P0(j) exp(v_j / lambda)`, where `P0` is the
unconditional choice distribution. When `P0` is uniform over the menu, this is (1) with `v_i = -C_i`
and `T = lambda`. A fixed `T` is then a fixed price of information, constant across problems.

*Proof.* Substitution. []

Caveat to state in the paper. `P0` is the endogenous unconditional choice distribution, not the
prior. Matejka and McKay's Proposition 1 gives the standard logit with temperature `lambda` when the
actions are a priori homogeneous (exchangeable prior). State it that way, not as "uniform prior".
