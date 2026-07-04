#!/usr/bin/env python3
"""Pre-registered projection-gap contrast families.

Each contrast is a matched pair (lo pole, hi pole) that is IDENTICAL under every
scalar projection (same monetary payoffs / same lottery {(x_i,p_i)}), differing
only in the framing of ONE active coordinate d in {6,7,9}. Scalar theories are
therefore forced to predict Delta = P(A|hi) - P(A|lo) = 0; the frozen geometric
model predicts a signed Delta (see predict.py).

Encoding convention (pre-committed, transparent, bipolar => sign is invariant to
any monotone re-encoding of the coordinate):
  - Option A is the coordinate-aligned choice; option B is the alternative.
  - lo pole: the coordinate is not salient -> both options frictionless on d
    (active displacement 0) -> model P(A)=0.5.
  - hi pole: choosing the MISaligned option B incurs a displacement `m` on
    coordinate d (acting against the now-salient value is costly) -> c_B up ->
    P(A) up -> Delta > 0.
  - loss-domain d9 flip (manuscript): epistemic clarity is aversive under losses,
    so the d9 displacement lands on A instead of B -> Delta < 0 (sign reversal).
  - placebo: coordinate NOT engaged at either pole (m applied to an INACTIVE dim,
    or no displacement) -> model Delta = 0. Internal falsifier.
  - dose: `m` scales across levels -> monotone Delta (H4).

`m` is the pre-registered "moral-friction unit" on the coordinate. Sign(Delta) is
independent of m>0 (the adversary-proof primary prediction); |Delta| depends on m
and sigma_d (the magnitude / structural predictions).
"""
from __future__ import annotations

from dataclasses import dataclass, field

# Pre-registered displacement unit on the manipulated coordinate at the hi pole.
M_UNIT = 1.0


@dataclass(frozen=True)
class Contrast:
    id: str
    family: str
    domain: str          # "game" | "lottery"
    coord: int           # manipulated coordinate (6,7,9) or an inactive dim for placebo
    kind: str            # "real" | "placebo" | "dose"
    prompt_lo: str       # forced-choice prompt, low pole of the coordinate
    prompt_hi: str       # same money/lottery, high pole of the coordinate
    # option displacements as {dim: value}; A is coordinate-aligned option.
    a_lo: dict = field(default_factory=dict)
    b_lo: dict = field(default_factory=dict)
    a_hi: dict = field(default_factory=dict)
    b_hi: dict = field(default_factory=dict)
    note: str = ""


def _pair(coord: int, m: float, *, flip: bool = False) -> dict:
    """Build the four option-displacement dicts for a standard contrast.

    lo: A,B both 0 on coord. hi: displacement m on the misaligned option (B),
    unless `flip` (loss-domain), in which case it lands on the aligned option (A).
    """
    a_lo, b_lo = {}, {}
    if flip:
        a_hi, b_hi = {coord: m}, {}
    else:
        a_hi, b_hi = {}, {coord: m}
    return {"a_lo": a_lo, "b_lo": b_lo, "a_hi": a_hi, "b_hi": b_hi}


# Fixed forced-choice answer protocol appended to every prompt (output-only, no CoT).
ANSWER = ("\nAnswer with ONLY this line: FINAL CHOICE=<A or B>")


def _c(cid, family, domain, coord, kind, lo_text, hi_text, m=M_UNIT, flip=False, note=""):
    d = _pair(coord if kind != "placebo" else 1, m if kind != "placebo" else 0.0, flip=flip)
    return Contrast(
        id=cid, family=family, domain=domain, coord=coord, kind=kind,
        prompt_lo=lo_text + ANSWER, prompt_hi=hi_text + ANSWER, note=note, **d,
    )


# ----------------------------------------------------------------------------
# GAME DOMAIN (falsifies Nash / EU / Fehr-Schmidt: monetary payoff matrix fixed)
# ----------------------------------------------------------------------------
GAME = [
    # A1 -- Social Impact (d6). Identical money split; recipient's social externality varies.
    _c("A1.1", "A1_social_impact", "game", 6, "real",
       "You can keep $6 and give $4 to the other person. Option A: give the $4. "
       "Option B: keep all $10. The other person is a stranger you will never meet.",
       "You can keep $6 and give $4 to the other person. Option A: give the $4. "
       "Option B: keep all $10. The $4 you give funds meals at a community shelter that "
       "will feed a dozen people; the money you keep goes to your private account.",
       note="Ultimatum/dictator; payoff split identical ($6/$4), only recipient externality (d6) differs."),
    _c("A1.2", "A1_social_impact", "game", 6, "real",
       "Split $20 with a group. Option A: contribute $8 to the common pool. Option B: "
       "contribute $0. Contributions are anonymous and the pool is dissolved immediately.",
       "Split $20 with a group. Option A: contribute $8 to the common pool. Option B: "
       "contribute $0. Contributions are anonymous, but the pool funds a shared well the "
       "whole village will drink from for years.",
       note="Public-goods; contribution amounts identical, only community effect (d6) differs."),
    # A2 -- Virtue/Identity (d7). Identical payoffs; role-consistency framing varies.
    _c("A2.1", "A2_virtue_identity", "game", 7, "real",
       "In a one-off transaction you can under-report to gain $15 or report honestly for $5. "
       "Option A: report honestly ($5). Option B: under-report ($15). No one will ever check.",
       "As the certified auditor whose entire professional identity rests on integrity, you can "
       "under-report to gain $15 or report honestly for $5. Option A: report honestly ($5). "
       "Option B: under-report ($15). No one will ever check.",
       note="Payoffs identical ($5 vs $15); only role/identity salience (d7) differs."),
    # A3 -- Epistemic Status (d9). Identical monetary trust game; info clarity varies.
    _c("A3.1", "A3_epistemic", "game", 9, "real",
       "Trust game: send $10 (tripled to $30) hoping the partner returns half. Option A: send. "
       "Option B: keep $10. You have heard an unverified rumor the partner sometimes returns nothing.",
       "Trust game: send $10 (tripled to $30) hoping the partner returns half. Option A: send. "
       "Option B: keep $10. A verified, audited record shows the partner returns half every time.",
       note="Monetary structure identical; only informational clarity about intent (d9) differs."),
]

# ----------------------------------------------------------------------------
# LOTTERY DOMAIN (falsifies CPT / EU: outcomes & probabilities held numerically fixed)
# ----------------------------------------------------------------------------
LOTTERY = [
    # B1 -- Epistemic Status (d9), GAIN domain. Identical (x_i,p_i); source vagueness varies.
    _c("B1.1", "B1_epistemic_gain", "lottery", 9, "real",
       "Choose: Option A: a sure $40. Option B: a 50% chance of $100 (else $0). "
       "The 50% is a precisely known, machine-verified probability.",
       "Choose: Option A: a sure $40. Option B: a 50% chance of $100 (else $0). "
       "The '50%' is a vague guess from an unreliable source; the true odds are unknown.",
       note="Outcomes/probabilities numerically identical; only epistemic clarity of the source (d9) differs."),
    # B1L -- d9 in the LOSS domain: clarity is aversive -> pre-registered SIGN REVERSAL.
    _c("B1L.1", "B1L_epistemic_loss", "lottery", 9, "real",
       "Choose: Option A: a sure LOSS of $40. Option B: a 50% chance of losing $100 (else $0). "
       "The 50% is a precisely known, machine-verified probability.",
       "Choose: Option A: a sure LOSS of $40. Option B: a 50% chance of losing $100 (else $0). "
       "The '50%' is a vague guess from an unreliable source; the true odds are unknown.",
       flip=True,
       note="LOSS-domain d9 flip: epistemic clarity is aversive -> Delta sign reverses vs B1."),
    # B2 -- Social Impact (d6), lottery. Identical lottery; self-only vs community outcome.
    _c("B2.1", "B2_social_impact", "lottery", 6, "real",
       "Choose: Option A: a sure $30. Option B: a 40% chance of $80 (else $0). "
       "The payoff affects only you.",
       "Choose: Option A: a sure $30. Option B: a 40% chance of $80 (else $0). "
       "Whatever you receive is shared with your whole community.",
       note="Lottery (x_i,p_i) identical; only social scope of the outcome (d6) differs."),
]

# ----------------------------------------------------------------------------
# PLACEBOS (coordinate NOT engaged -> model Delta=0; internal falsifier)
# ----------------------------------------------------------------------------
PLACEBO = [
    _c("P.A1", "placebo", "game", 6, "placebo",
       "You can keep $6 and give $4. Option A: give the $4. Option B: keep all $10. "
       "The other person is a stranger.",
       "You may keep six dollars and give four dollars. Choice A: give the four dollars. "
       "Choice B: retain the entire ten dollars. The counterpart is a stranger.",
       note="Only surface wording (synonyms) changes; coordinate held fixed -> Delta=0 expected."),
    _c("P.B1", "placebo", "lottery", 9, "placebo",
       "Choose: Option A: a sure $40. Option B: a 50% chance of $100 (else $0). "
       "The probability is precisely known.",
       "Select: Choice A: a guaranteed $40. Choice B: a one-in-two shot at $100 (otherwise $0). "
       "The probability is precisely known.",
       note="Paraphrase only; epistemic status identical -> Delta=0 expected."),
]

# ----------------------------------------------------------------------------
# DOSE-RESPONSE (d9): m straddles the temperature-induced peak.
# The frozen T(Δ)=max(0.5, 0.24 Δ^2.13) has exponent 2.13>1, so gap/T peaks at
# cost-gap ~= 1.4 (below it T=T_floor and effect rises with m; above it T rises
# super-linearly and washes the effect out). For d9 (sigma=0.114) that peak is at
# m ~= 1.4*sigma ~= 0.16. => the model predicts a PEAKED (non-monotone) dose curve
# with the maximum at level 2. A monotone-increasing observed curve falsifies the
# temperature architecture specifically. No scalar theory predicts any dose effect.
# ----------------------------------------------------------------------------
_DOSE_M = [0.06, 0.16, 0.30, 0.60]  # gaps ~ 0.53, 1.40 (peak), 2.63, 5.26 on d9
DOSE = [
    _c(f"D9.{i}", "dose_d9", "lottery", 9, "dose",
       "Choose: Option A: a sure $40. Option B: a 50% chance of $100 (else $0). "
       "The probability source is fully reliable.",
       "Choose: Option A: a sure $40. Option B: a 50% chance of $100 (else $0). "
       f"The probability source reliability is graded at level {i} of 4 (higher = vaguer).",
       m=mval,
       note=f"Dose level {i}: displacement m={mval:.2f} on d9 (cost-gap {mval/0.114:.2f}).")
    for i, mval in enumerate(_DOSE_M, start=1)
]

ALL_CONTRASTS: list[Contrast] = GAME + LOTTERY + PLACEBO + DOSE


def as_records() -> list[dict]:
    """Serializable view of the frozen contrast set (for hashing / the panel)."""
    out = []
    for c in ALL_CONTRASTS:
        out.append({
            "id": c.id, "family": c.family, "domain": c.domain, "coord": c.coord,
            "kind": c.kind, "prompt_lo": c.prompt_lo, "prompt_hi": c.prompt_hi,
            "a_lo": c.a_lo, "b_lo": c.b_lo, "a_hi": c.a_hi, "b_hi": c.b_hi, "note": c.note,
        })
    return out


if __name__ == "__main__":
    from collections import Counter
    kinds = Counter(c.kind for c in ALL_CONTRASTS)
    fams = Counter(c.family for c in ALL_CONTRASTS)
    print(f"{len(ALL_CONTRASTS)} contrasts: {dict(kinds)}")
    for f, n in fams.items():
        print(f"  {f}: {n}")
