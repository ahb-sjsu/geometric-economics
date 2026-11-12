"""Development: is the effect of the last gamble one-sided, and does it outlast the points held.

    python analyze_onesided.py dev.pkl out.json [first]

With `first` only each participant's first play is used, where the share of
gambles won is nearest one half (pass 2).

Pass 5 found, with Theory Radar scored by area under the curve, the form
`(base - prev_out) max base`: a last trial that paid less than average raises
gambling and one that paid more does nothing. Pass 6 found that matching on the
points held removes most of the difference between after a win and after a
loss. This file sets the two against each other.

Rows are trials whose reference trial was a taken gamble. Let s be half the
distance between the two outcomes of that gamble, in hundreds of points. If it
was won the player got s more than the gamble's mean, if lost s less. Inside
cells, least squares of the present choice on

    won * s     how the rate of gambling moves with the size of a good surprise
    lost * s    how it moves with the size of a bad surprise

with one constant per cell and one for won against lost, so the two slopes are
read from the size of the surprise and not from winning itself. Cells:

    C0   kind of the present trial, kind of the reference trial, position in
         the play (five bins), the player's share of gambles on the rest of the
         play (five bins)
    C1   and the points gained or lost so far in the play before the present
         choice, in bins of 25

A player who takes a wide gamble differs from one who takes a narrow one, so
neither slope is clean by itself. The same fit with the next trial as
reference (lead 1) has the same selection and no effect of the outcome, so the
quantity read is the lag slope minus the lead slope. One-sided as in pass 5
would be a positive value for lost and about zero for won.

The outcome of the next gamble is chance, so the lead slope should be the same
for won and lost. lead_won_minus_lost tests that. If it holds, the mean of the
two lead slopes is the better estimate of the selection, and the lag slopes
minus that mean are given too. lag_lost_minus_won needs no lead at all, since
a selection common to won and lost cancels in it. Intervals from
1,000 resamples of participants, the same resamples for lag and lead.
"""
import json
import pickle
import sys

import numpy as np

from analyze_last import SEED, plays


def main(src, out, first_only=False):
    recs = pickle.load(open(src, "rb"))["subjData"]
    rng = np.random.default_rng(SEED)
    rows = {"lag1": [], "lead1": []}
    for i, rec in enumerate(recs):
        for p in plays(rec)[:1] if first_only else plays(rec):
            safe, win, lose = p[:, 2], p[:, 3], p[:, 4]
            gam = p[:, 6] == 1
            won = gam & (p[:, 7] == win)
            got = np.where(gam, p[:, 7], safe)
            total = np.concatenate(([0.0], np.cumsum(got)[:-1]))
            n = len(p)
            if n < 3:
                continue
            rest = (gam.sum() - gam) / (n - 1)
            kind = np.where(safe > 0, 0, np.where(safe < 0, 2, 1))
            half = (win - lose) / 200.0
            for name, step in (("lag1", -1), ("lead1", 1)):
                t = np.arange(n)
                r = t + step
                ok = (r >= 0) & (r < n)
                t, r = t[ok], r[ok]
                keep = gam[r]
                t, r = t[keep], r[keep]
                if len(t):
                    rows[name].append(np.c_[np.full(len(t), i), gam[t], won[r], half[r], kind[t], kind[r],
                                            np.minimum(t // 6, 4), np.minimum((rest[t] * 5).astype(int), 4),
                                            np.floor(total[t] / 25)])
    npart = len(recs)
    draws = [np.bincount(rng.integers(0, npart, npart), minlength=npart).astype(float) for _ in range(1000)]
    fits = {}
    res = {}
    for name, parts in rows.items():
        a = np.concatenate(parts)
        pid, g, w, s = a[:, 0].astype(int), a[:, 1], a[:, 2], a[:, 3]
        c0 = ((a[:, 4] * 3 + a[:, 5]) * 5 + a[:, 6]) * 5 + a[:, 7]
        tb = a[:, 8] - a[:, 8].min()
        wide = s > np.median(s)
        res[name] = {"rows": int(len(g)), "mean_half_spread_hundreds": float(s.mean()),
                     "share_won": float(w.mean()), "share_won_narrow": float(w[~wide].mean()),
                     "share_won_wide": float(w[wide].mean())}
        print(name, res[name], flush=True)
        for cname, cell in (("C0", c0), ("C1", c0 + 225 * tb)):
            _, c = np.unique(cell * 2 + w, return_inverse=True)     # a constant per cell and per won or lost
            k = c.max() + 1
            X = np.c_[w * s, (1 - w) * s]

            def fit(wt):
                sw = np.bincount(c, wt, k)
                use = sw > 0
                A = np.zeros((2, 2))
                b = np.zeros(2)
                mx = [np.bincount(c, wt * X[:, j], k) for j in range(2)]
                my = np.bincount(c, wt * g, k)
                for j in range(2):
                    b[j] = (wt * X[:, j] * g).sum() - (mx[j][use] * my[use] / sw[use]).sum()
                    for l in range(2):
                        A[j, l] = (wt * X[:, j] * X[:, l]).sum() - (mx[j][use] * mx[l][use] / sw[use]).sum()
                return np.linalg.solve(A, b)

            fits[(name, cname)] = np.array([fit(np.ones(len(g)))] + [fit(d[pid]) for d in draws])
            print(name, cname, "won*s %+.4f lost*s %+.4f" % tuple(fits[(name, cname)][0]), flush=True)
    for cname in ("C0", "C1"):
        lag, lead = fits[("lag1", cname)], fits[("lead1", cname)]
        e = {}
        for label, v in (("lag_won", lag[:, 0]), ("lag_lost", lag[:, 1]), ("lead_won", lead[:, 0]), ("lead_lost", lead[:, 1]),
                         ("won_lag_minus_lead", lag[:, 0] - lead[:, 0]), ("lost_lag_minus_lead", lag[:, 1] - lead[:, 1]),
                         ("lost_minus_won_net", (lag[:, 1] - lead[:, 1]) - (lag[:, 0] - lead[:, 0])),
                         ("lead_won_minus_lost", lead[:, 0] - lead[:, 1]),
                         ("lag_lost_minus_won", lag[:, 1] - lag[:, 0]),
                         ("lead_mean", lead.mean(1)),
                         ("won_lag_minus_lead_mean", lag[:, 0] - lead.mean(1)),
                         ("lost_lag_minus_lead_mean", lag[:, 1] - lead.mean(1))):
            e[label] = {"slope_per_100_points": float(v[0]),
                        "ci95": [float(np.percentile(v[1:], 2.5)), float(np.percentile(v[1:], 97.5))]}
            print("%s %-22s %+.4f (%+.4f to %+.4f)" % (cname, label, v[0], *e[label]["ci95"]), flush=True)
        res[cname] = e
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], len(sys.argv) > 3 and sys.argv[3] == "first")
