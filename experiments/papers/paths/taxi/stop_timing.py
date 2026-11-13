"""Development pass 3: does money earned in the last hour move stopping more than money earned earlier?

    python stop_timing.py dev_2013_2019.csv.gz out.json [apart] [allcabs]

A first, plain form of the test of Thakral and To (2021), on development cabs.
Nothing here is registered.

Shifts as in pass 1 (no pause over six hours). Cabs as in pass 2: 50 shifts or
more, and a share of shifts over 14 hours at or under a bar. Run for bars of
5% and 10%, and with `allcabs` for all cabs with 50 shifts as well. That last
sample mixes shared cabs in, takes far longer and is not used (pass 3).

A decision is the end of a trip that falls 6 to 10 hours into its shift. The
outcome is 1 if that trip was the last of the shift. The fares of the shift up
to that moment are split by when the trip that earned them ended:

    e_0_1     in the last hour, the trip just ended included
    e_1_2     one to two hours before
    e_2_4     two to four hours before
    e_4plus   more than four hours before

A linear probability model of stopping on the four, in tens of dollars, with a
constant for each cab, each date, each hour of the week and each quarter hour
into the shift. The constants are removed by least squares on a sparse matrix
and the four coefficients fit on what is left. Standard errors are clustered
by cab.

The prediction carried in (DESIGN.md Section 5) is that e_0_1 raises stopping
more than e_4plus. The quantity is the first coefficient minus the last.

With `apart` the last hour is split in two: the fare of the trip just ended
(e_now) and the other fares of the last hour (e_0_1_rest). A long last run,
to an airport or toward home, would put a large fare on the last trip of a
shift for a reason that has nothing to do with money earned. If the effect of
the last hour sits only in e_now it cannot be told from that.

A shift in which more than eight trips end at one rounded time is left out
whole. One car cannot do that (added 2026-11-13, DEVELOPMENT.md pass 7).

Fares are cut to the range 0 to 200 dollars. Tips are not counted, as in the
published paper. What this does not control: a busy hour raises the last
hour's fares and also the reason to stay out, beyond what date and hour of the
week take up. There is no weather.
"""
import json
import sys

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.linalg import lsqr

GAP_HOURS = 6.0
LONG_HOURS = 14.0
MIN_SHIFTS = 50
WINDOW = (6.0, 10.0)
NAMES = ("e_0_1", "e_1_2", "e_2_4", "e_4plus")
BIG = 10 ** 11
CROWD = 8


def crowded(key):
    """True for every trip of a shift in which more than CROWD trips end at one rounded time.

    One car cannot do that. Such a shift belongs to an identifier that stands for
    more than one car, and its sums of fares run to thousands of dollars an hour
    (check_last_hour_tail.py). `key` is shift * BIG + end time, sorted.
    """
    _, inv, cnt = np.unique(key, return_inverse=True, return_counts=True)
    sh = key // BIG
    bad = np.zeros(int(sh.max()) + 1, dtype=bool)
    bad[sh[cnt[inv] > CROWD]] = True
    return bad[sh]


def fit(y, X, groups, cluster):
    cols, n = [], len(y)
    offset = 0
    for g in groups:
        _, inv = np.unique(g, return_inverse=True)
        cols.append(inv + offset)
        offset += inv.max() + 1
    D = sparse.csr_matrix((np.ones(n * len(groups)), (np.tile(np.arange(n), len(groups)), np.concatenate(cols))),
                          shape=(n, offset))

    def resid(v):
        return v - D @ lsqr(D, v, atol=1e-10, btol=1e-10, iter_lim=5000)[0]

    yr = resid(y - y.mean())
    Xr = np.column_stack([resid(X[:, j] - X[:, j].mean()) for j in range(X.shape[1])])
    bread = np.linalg.inv(Xr.T @ Xr)
    beta = bread @ (Xr.T @ yr)
    u = yr - Xr @ beta
    _, cl = np.unique(cluster, return_inverse=True)
    S = np.zeros((cl.max() + 1, X.shape[1]))
    for j in range(X.shape[1]):
        S[:, j] = np.bincount(cl, Xr[:, j] * u)
    G = cl.max() + 1
    V = bread @ (S.T @ S) @ bread * G / (G - 1)
    return beta, V, offset


def main(src, out, apart=False, all_cabs=False):
    d = pd.read_csv(src, usecols=["taxi_id", "trip_start_timestamp", "trip_end_timestamp", "fare"],
                    dtype={"taxi_id": "category"})
    for c in ("trip_start_timestamp", "trip_end_timestamp"):
        d[c] = pd.to_datetime(d[c], errors="coerce")
    d = d.dropna(subset=["trip_start_timestamp", "trip_end_timestamp"])
    d["cab"] = d["taxi_id"].cat.codes
    d = d.sort_values(["cab", "trip_start_timestamp", "trip_end_timestamp"], kind="stable").reset_index(drop=True)
    start = d["trip_start_timestamp"].values.astype("datetime64[s]").astype(np.int64)
    end = d["trip_end_timestamp"].values.astype("datetime64[s]").astype(np.int64)
    cab = d["cab"].values.astype(np.int64)
    raw_fare = d["fare"].fillna(0).values
    fare = np.clip(raw_fare, 0, 200)
    res = {"trips": int(len(d)), "share_of_fares_cut": float((raw_fare != fare).mean()), "crowd_limit": CROWD}
    del d
    first = np.r_[True, cab[1:] != cab[:-1]]
    prev_end = pd.Series(end).groupby(cab).cummax().shift(1).values
    pause = (start - prev_end) / 3600.0
    pause[first] = np.nan
    new = first | (pause > GAP_HOURS)
    shift = np.cumsum(new) - 1
    s_start = pd.Series(start).groupby(shift).min().values
    s_end = pd.Series(end).groupby(shift).max().values
    length = (s_end - s_start) / 3600.0
    s_cab = cab[new]
    ncab = int(cab.max()) + 1
    n_sh = np.bincount(s_cab, minlength=ncab)
    share_long = np.bincount(s_cab, length > LONG_HOURS, minlength=ncab) / np.maximum(n_sh, 1)

    # order trips inside a shift by end time, for the sums of earlier fares
    order = np.lexsort((end, shift))
    shift, end, fare, cab = shift[order], end[order], fare[order], cab[order]
    last = np.r_[shift[1:] != shift[:-1], True]
    cum = np.cumsum(fare)
    idx0 = np.r_[0, np.flatnonzero(shift[1:] != shift[:-1]) + 1]      # first row of each shift
    base = np.r_[0.0, cum][idx0]                                      # sum of fares before each shift
    key = shift * BIG + (end - end.min())
    hours_in = (end - s_start[shift]) / 3600.0

    def upto(lookback):
        j = np.searchsorted(key, key - lookback, side="right") - 1
        inside = j >= idx0[shift]
        return np.where(inside, cum[np.maximum(j, 0)] - base[shift], 0.0)

    total = cum - base[shift]
    b1, b2, b4 = upto(3600), upto(7200), upto(14400)
    X_all = np.column_stack([total - b1, b1 - b2, b2 - b4, b4]) / 10.0
    names = NAMES
    if apart:
        X_all = np.column_stack([fare / 10.0, X_all[:, 0] - fare / 10.0, X_all[:, 1:]])
        names = ("e_now", "e_0_1_rest") + NAMES[1:]
    in_window = (hours_in >= WINDOW[0]) & (hours_in < WINDOW[1]) & ~crowded(key)
    t = pd.to_datetime(end, unit="s")
    how = (t.dayofweek.values * 24 + t.hour.values)
    date = end // 86400
    qbin = np.floor(hours_in * 4).astype(int)

    res["samples"] = {}
    for label, bar in (("long_share_at_most_0.05", 0.05), ("long_share_at_most_0.10", 0.10)) + ((("all_cabs_with_50_shifts", 1.0),) if all_cabs else ()):
        keep_cab = (n_sh >= MIN_SHIFTS) & (share_long <= bar)
        m = in_window & keep_cab[cab]
        y = last[m].astype(float)
        X = X_all[m]
        beta, V, nfe = fit(y, X, [cab[m], date[m], how[m], qbin[m]], cab[m])
        se = np.sqrt(np.diag(V))
        c = np.zeros(len(names))
        c[1 if apart else 0], c[-1] = 1.0, -1.0
        diff, diff_se = float(c @ beta), float(np.sqrt(c @ V @ c))
        s = {"cabs": int(keep_cab[np.unique(cab[m])].sum()), "decisions": int(m.sum()), "stop_rate": float(y.mean()),
             "constants_removed": int(nfe),
             "mean_dollars": {n: float(X[:, j].mean() * 10) for j, n in enumerate(names)},
             "sd_dollars": {n: float(X[:, j].std() * 10) for j, n in enumerate(names)},
             "per_10_dollars": {n: {"coef": float(beta[j]), "se": float(se[j]),
                                    "ci95": [float(beta[j] - 1.96 * se[j]), float(beta[j] + 1.96 * se[j])]}
                                for j, n in enumerate(names)},
             ("rest_of_last_hour_minus_over_four_hours_back" if apart else "last_hour_minus_over_four_hours_back"): {"difference": diff, "se": diff_se,
                                                      "ci95": [diff - 1.96 * diff_se, diff + 1.96 * diff_se]}}
        if apart:
            c2 = np.zeros(len(names))
            c2[0], c2[-1] = 1.0, -1.0
            s["trip_just_ended_minus_over_four_hours_back"] = {"difference": float(c2 @ beta), "se": float(np.sqrt(c2 @ V @ c2))}
        res["samples"][label] = s
        print(label, json.dumps(s), flush=True)
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "apart" in sys.argv[3:], "allcabs" in sys.argv[3:])
