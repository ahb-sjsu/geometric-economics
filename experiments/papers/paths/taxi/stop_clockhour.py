"""Development pass 6: the test in the form the published paper used.

    python stop_clockhour.py dev_2013_2019.csv.gz out.json

Passes 3 to 5 split a shift's fares by how long before the decision they were
earned, over decisions 6 to 10 hours into the shift. Thakral and To (2021,
Table 2) do it another way. They take trips that end within ten minutes of 8.5
hours into the shift and split the fares by the hour of the shift in which
they were earned, hour 1 to hour 8. Their effect falls off gradually: money in
hours 5, 6 and 7 still raises stopping, less than money in hour 8. This file
puts the Chicago development cabs through that form, so the two can be set
side by side.

A decision is the end of a trip that falls within a half-width of 8.5 hours
into its shift. The half-width is 10 minutes as published, and 30 minutes for
more decisions. A fare belongs to the hour of the shift in which its trip
ended. Regressors, in tens of dollars:

    h1 .. h8        fares of trips that ended in hour 1 .. hour 8 of the shift
    after8          fares of trips that ended later than 8 hours in

Second fit, the trip just ended taken apart:

    h1 .. h8, after8_rest, e_now

where e_now is the fare of the trip just ended and after8_rest the other
fares after 8 hours. The published text read so far does not say in which
term the fare of the trip just ended sits.

Constants for each cab, date, hour of the week, dropoff community area (the
paper has driver, time and 195 neighbourhoods) and quarter hour into the
shift. The city rounds trip times to the nearest 15 minutes, so within ten
minutes of 8.5 hours every decision sits at exactly 8.5 hours and the last
constant does nothing there. Clustered by cab. Same shifts and cabs as stop_timing.py.
Linear probability, not the paper's elasticities, and cabs, not drivers.
Nothing here is registered.
"""
import json
import sys

import numpy as np
import pandas as pd

from stop_timing import GAP_HOURS, LONG_HOURS, MIN_SHIFTS, fit

CENTRE = 8.5
HOURS = 8


def main(src, out):
    d = pd.read_csv(src, usecols=["taxi_id", "trip_start_timestamp", "trip_end_timestamp", "fare", "dropoff_community_area"],
                    dtype={"taxi_id": "category"})
    for c in ("trip_start_timestamp", "trip_end_timestamp"):
        d[c] = pd.to_datetime(d[c], errors="coerce")
    d = d.dropna(subset=["trip_start_timestamp", "trip_end_timestamp"])
    d["cab"] = d["taxi_id"].cat.codes
    d = d.sort_values(["cab", "trip_start_timestamp", "trip_end_timestamp"], kind="stable").reset_index(drop=True)
    start = d["trip_start_timestamp"].values.astype("datetime64[s]").astype(np.int64)
    end = d["trip_end_timestamp"].values.astype("datetime64[s]").astype(np.int64)
    cab = d["cab"].values.astype(np.int64)
    fare = np.clip(d["fare"].fillna(0).values, 0, 200)
    area = d["dropoff_community_area"].fillna(0).values.astype(np.int64)
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

    order = np.lexsort((end, shift))
    shift, end, fare, cab, area = shift[order], end[order], fare[order], cab[order], area[order]
    last = np.r_[shift[1:] != shift[:-1], True]
    idx0 = np.r_[0, np.flatnonzero(shift[1:] != shift[:-1]) + 1]
    hours_in = (end - s_start[shift]) / 3600.0
    hbin = np.clip(np.floor(hours_in).astype(int), 0, HOURS)          # 0..7 are hours 1..8, 8 is after 8 hours
    cols = []
    for k in range(HOURS + 1):
        cum = np.cumsum(np.where(hbin == k, fare, 0.0))
        cols.append(cum - np.r_[0.0, cum][idx0][shift])
    H = np.column_stack(cols) / 10.0
    now = fare / 10.0
    t = pd.to_datetime(end, unit="s")
    how = t.dayofweek.values * 24 + t.hour.values
    date = end // 86400
    hnames = tuple("h%d" % (k + 1) for k in range(HOURS))

    res = {"centre_hours": CENTRE, "samples": {}}
    for half, hl in ((10, "within_10_minutes"), (30, "within_30_minutes")):
        near = np.abs(hours_in - CENTRE) <= half / 60.0
        for label, bar in (("long_share_at_most_0.05", 0.05), ("long_share_at_most_0.10", 0.10)):
            keep_cab = (n_sh >= MIN_SHIFTS) & (share_long <= bar)
            m = near & keep_cab[cab]
            y = last[m].astype(float)
            s = {"cabs": int(len(np.unique(cab[m]))), "decisions": int(m.sum()), "stop_rate": float(y.mean()),
                 "mean_dollars": {n: float(H[m, k].mean() * 10) for k, n in enumerate(hnames + ("after8",))},
                 "mean_fare_trip_just_ended": float(fare[m].mean())}
            print(hl, label, json.dumps({k: s[k] for k in ("cabs", "decisions", "stop_rate", "mean_dollars", "mean_fare_trip_just_ended")}),
                  flush=True)
            groups = [cab[m], date[m], how[m], area[m], np.round(hours_in[m] * 4).astype(int)]
            fits = (("as_published", H[m], hnames + ("after8",)),
                    ("trip_just_ended_apart", np.column_stack([H[m, :HOURS], H[m, HOURS] - now[m], now[m]]),
                     hnames + ("after8_rest", "e_now")))
            for name, X, names in fits:
                beta, V, nfe = fit(y, X, groups, cab[m])
                se = np.sqrt(np.diag(V))
                s[name] = {"constants_removed": int(nfe),
                           "coef": {n: {"coef": float(beta[j]), "se": float(se[j]),
                                        "ci95": [float(beta[j] - 1.96 * se[j]), float(beta[j] + 1.96 * se[j])]}
                                    for j, n in enumerate(names)}}
                print(hl, label, name, json.dumps({n: [round(v["coef"], 4), round(v["ci95"][0], 4), round(v["ci95"][1], 4)]
                                                   for n, v in s[name]["coef"].items()}), flush=True)
            res["samples"][hl + "." + label] = s
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
