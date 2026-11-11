"""Development: does the outcome of the last gamble change the next choice?

    python analyze_last.py dev.pkl out.json

Reads the development half written by split_gbe.py and nothing else.

A play is 30 trials in the order shown. Column 7 is 1 if the player gambled,
column 8 the outcome, column 4 the value on the winning side of the spinner,
column 3 the safe value (above zero in a gain trial, zero in a mixed trial,
below zero in a loss trial). A gamble is won if the outcome equals the winning
side's value.

Trial order was random and the spinner decided the outcome. So among choices
that follow a taken gamble, those after a win and those after a loss differ only
by chance, and the offer on the present trial does not depend on either.

For each participant: the rate of gambling on trials whose reference trial was
a won gamble, minus the rate on trials whose reference trial was a lost gamble.
The reported number is the mean over participants who have both, with a 95%
interval from 2,000 resamples of participants.

Reference trials:
    lag 1    the trial before (the question)
    lag 2    two trials before
    lead 1   the trial AFTER. Its outcome is not yet known when the present
             choice is made, so this difference must be zero. It is the check
             that the comparison itself is sound.

Also written: the share of taken gambles that were won, overall and by kind of
trial, as a check on the spinner. Splits of lag 1 by the kind of the present
trial and by the kind of the reference trial.
"""
import json
import pickle
import sys
from collections import defaultdict

import numpy as np

SEED = 20261111
KIND = {1: "gain", 0: "mixed", -1: "loss"}


def plays(rec):
    d = rec["data"]
    if isinstance(d, np.ndarray) and d.dtype != object and d.ndim == 2:
        return [d]
    return [p for p in np.atleast_1d(d) if isinstance(p, np.ndarray) and p.ndim == 2 and p.shape[0] >= 2]


def estimate(acc, rng):
    v = np.array([w[0] / w[1] - l[0] / l[1] for w, l in acc.values() if w[1] and l[1]])
    if len(v) < 30:
        return {"participants": int(len(v))}
    boots = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(2000)]
    return {"participants": int(len(v)), "difference": float(v.mean()),
            "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}


def main(src, out):
    recs = pickle.load(open(src, "rb"))["subjData"]
    rng = np.random.default_rng(SEED)
    new = lambda: defaultdict(lambda: [[0, 0], [0, 0]])       # participant -> [after win, after loss] -> [gambled, n]
    acc = defaultdict(new)
    spinner = defaultdict(lambda: [0, 0])
    n_plays = n_trials = 0
    for rec in recs:
        pid = int(rec["id"])
        for p in plays(rec):
            n_plays += 1
            n_trials += len(p)
            gam = p[:, 6] == 1
            won = gam & (p[:, 7] == p[:, 3])
            kind = [KIND[int(np.sign(x))] for x in p[:, 2]]
            for t in range(len(p)):
                if gam[t]:
                    for k in ("all", kind[t]):
                        spinner[k][0] += int(won[t])
                        spinner[k][1] += 1
                for name, r in (("lag1", t - 1), ("lag2", t - 2), ("lead1", t + 1)):
                    if not 0 <= r < len(p) or not gam[r]:
                        continue
                    keys = [name]
                    if name == "lag1":
                        keys += ["lag1_now_" + kind[t], "lag1_after_" + kind[r]]
                    for k in keys:
                        c = acc[k][pid][0 if won[r] else 1]
                        c[0] += int(gam[t])
                        c[1] += 1
    res = {"participants": len(recs), "plays": n_plays, "trials": n_trials,
           "share_of_gambles_won": {k: {"share": v[0] / v[1], "n": v[1]} for k, v in sorted(spinner.items())},
           "gamble_rate_after_win_minus_after_loss": {k: estimate(acc[k], rng) for k in sorted(acc)}}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
