#!/usr/bin/env python3
"""What one paid trial pays, in points, to size the point rate (PILOT.md, "The open items"; DESIGN.md, "Payment").

    python payout.py

One trial of the session is drawn and paid: self points to the participant and charity points to the charity, at
one rate per point. For the main study's 140 trials and the pilot's 160, this prints the expected points of a trial
drawn at random under three ways of choosing (at random, always the option worth more self points, always the one
worth more charity points) and the largest outcome on each scale. A lottery counts at its expected value.
"""
import numpy as np

import stimuli as S


def ev(option):
    """Expected self and charity points of one option."""
    return (sum(p * (100 - a) for p, a, b in option), sum(p * (100 - b) for p, a, b in option))


def main():
    T = S.build()
    X = S.pilot_extras(T)
    for name, tt in ((f"main study, {len(T)} trials", T), (f"pilot, {len(T) + len(X)} trials", T + X)):
        e = np.array([[ev(o) for o in t["options"]] for t in tt])     # trial x option x (self, charity)
        idx = np.arange(len(tt))
        rand = e.mean(axis=1).mean(axis=0)
        sel = e[idx, e[:, :, 0].argmax(axis=1)].mean(axis=0)
        cha = e[idx, e[:, :, 1].argmax(axis=1)].mean(axis=0)
        top_s = max(100 - a for t in tt for o in t["options"] for p, a, b in o)
        top_c = max(100 - b for t in tt for o in t["options"] for p, a, b in o)
        print(f"{name}: random choice self {rand[0]:.1f} charity {rand[1]:.1f} | self-maximiser self {sel[0]:.1f} "
              f"charity {sel[1]:.1f} | charity-maximiser self {cha[0]:.1f} charity {cha[1]:.1f} | highest outcome "
              f"self {top_s:.0f} charity {top_c:.0f}")


if __name__ == "__main__":
    main()
