"""Development: the last outcome among trials matched on the running total.

    python analyze_matched.py dev.pkl out.json [lead]

Pass 4 removed a mean within each play and could not hold the total fixed. The
check with the next trial as reference failed whenever the total was in the
fit. This file removes no mean. Trials whose reference trial was a taken gamble
are put in cells, and inside a cell the rate of gambling after a won reference
gamble is compared with the rate after a lost one. Cells are weighted by
n_won * n_lost / (n_won + n_lost), all participants pooled.

Cells, each containing the one before:

    M0   kind of the present trial, position in the play (five bins of six trials)
    M1   and the points gained or lost so far in the play before the present
         choice, in bins of 25 points
    M2   and the share of the other trials of the play on which the player
         gambled, in five bins

M2 is there because two players at the same total after a win and after a loss
came from different totals, and so may be different kinds of player. The share
of gambles over the rest of the play stands in for the kind of player.

Each is run with the last trial as reference (lag 1) and with the next trial
as reference (lead 1), where the difference must be zero. Intervals are from
1,000 resamples of participants.

For lag 1 the three are also run apart for each kind of the reference trial
(after_gain, after_mixed, after_loss) and each kind of the present trial
(now_gain, now_mixed, now_loss), the splits of pass 3.

With `lead` as third argument only the next-trial check is run, with the same
splits. There after_gain means the next trial, the reference, is a gain trial.
Each must be zero.
"""
import json
import pickle
import sys

import numpy as np

from analyze_last import SEED, plays


def main(src, out, lead_only=False):
    recs = pickle.load(open(src, "rb"))["subjData"]
    rng = np.random.default_rng(SEED)
    rows = {"lag1": [], "lead1": []}
    for i, rec in enumerate(recs):
        for p in plays(rec):
            safe, win = p[:, 2], p[:, 3]
            gam = p[:, 6] == 1
            won = gam & (p[:, 7] == win)
            got = np.where(gam, p[:, 7], safe)
            total = np.concatenate(([0.0], np.cumsum(got)[:-1]))
            n = len(p)
            if n < 3:
                continue
            rest = (gam.sum() - gam) / (n - 1)
            kind = np.where(safe > 0, 0, np.where(safe < 0, 2, 1))
            for name, step in (("lag1", -1), ("lead1", 1)):
                t = np.arange(n)
                r = t + step
                ok = (r >= 0) & (r < n)
                t, r = t[ok], r[ok]
                keep = gam[r]
                t, r = t[keep], r[keep]
                if len(t):
                    rows[name].append(np.c_[np.full(len(t), i), gam[t], won[r], kind[t], np.minimum(t // 6, 4),
                                            np.floor(total[t] / 25), np.minimum((rest[t] * 5).astype(int), 4), kind[r]])
    res = {}
    for name, parts in rows.items():
        if lead_only and name != "lead1":
            continue
        a = np.concatenate(parts)
        pid, g, w = a[:, 0].astype(int), a[:, 1], a[:, 2]
        base = a[:, 3] * 5 + a[:, 4]
        tb = a[:, 5] - a[:, 5].min()
        cells = {"M0": base, "M1": base + 15 * tb, "M2": base + 15 * tb + 15 * (tb.max() + 1) * a[:, 6]}
        upid, pidx = np.unique(pid, return_inverse=True)
        res[name] = {"rows": int(len(g)), "participants": int(len(upid))}
        subsets = {"": np.ones(len(g))}
        if name == "lag1" or lead_only:
            for i, kn in enumerate(("gain", "mixed", "loss")):
                subsets["_after_" + kn] = (a[:, 7] == i).astype(float)
                subsets["_now_" + kn] = (a[:, 3] == i).astype(float)
        draws = [np.bincount(rng.integers(0, len(upid), len(upid)), minlength=len(upid)) for _ in range(1000)]

        def est(wt, c, k):
            n1 = np.bincount(c, wt * w, k)
            n0 = np.bincount(c, wt * (1 - w), k)
            s1 = np.bincount(c, wt * w * g, k)
            s0 = np.bincount(c, wt * (1 - w) * g, k)
            use = (n1 > 0) & (n0 > 0)
            wgt = n1[use] * n0[use] / (n1[use] + n0[use])
            return float((wgt * (s1[use] / n1[use] - s0[use] / n0[use])).sum() / wgt.sum()), int(use.sum())

        for m0, c0 in cells.items():
            _, c = np.unique(c0, return_inverse=True)
            k = c.max() + 1
            for sub, mask in subsets.items():
                m = m0 + sub
                point, used = est(mask, c, k)
                boots = [est(mask * d[pidx], c, k)[0] for d in draws]
                res[name][m] = {"difference": point, "cells_used": used,
                                "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}
                print("%-6s %-14s %+.4f (%+.4f to %+.4f) cells %d" % (name, m, point, *res[name][m]["ci95"], used), flush=True)
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], len(sys.argv) > 3 and sys.argv[3] == "lead")
