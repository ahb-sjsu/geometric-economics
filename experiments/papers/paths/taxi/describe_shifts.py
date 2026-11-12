"""Development pass 1: what a shift looks like in the Chicago file, before any test.

    python describe_shifts.py dev_2013_2019.csv.gz out.json

Development cabs only. Reads the taxi identifier, the two times, seconds, fare
and total of each trip. Trips of a cab are ordered by start time. The pause
before a trip is its start minus the latest end among the cab's earlier trips.
A shift is a run of trips with no pause longer than six hours, the rule of
Thakral and To (2021).

Written out, with no test of anything:

    coverage         trips by month, cabs, rows dropped for a missing time
    pauses           how the pauses between a cab's trips are spread, to see
                     whether six hours is a natural place to cut
    overlaps         trips that start more than 15 minutes before the cab's
                     last trip ended. Times are rounded to 15 minutes, so
                     shorter overlaps are expected. Longer ones cannot be one car.
    shifts           how many, their length and number of trips, and the share
                     longer than 12, 16 and 24 hours. The identifier is the cab
                     and not the driver, so a very long shift is likely two
                     drivers' shifts joined.
    stopping         by hour into the shift, the share of trips that were the
                     last of their shift
"""
import json
import sys

import numpy as np
import pandas as pd

GAP_HOURS = 6.0
PAUSE_EDGES = [-1e9, -0.2501, 0.0, 0.2501, 1, 2, 4, 6, 8, 12, 24, 1e9]
PAUSE_NAMES = ["overlap over 15 min", "overlap up to 15 min", "0 to 15 min", "15 min to 1 h", "1 to 2 h", "2 to 4 h",
               "4 to 6 h", "6 to 8 h", "8 to 12 h", "12 to 24 h", "over 24 h"]


def q(v):
    return {k: float(np.percentile(v, p)) for k, p in (("p10", 10), ("p25", 25), ("median", 50), ("p75", 75),
                                                       ("p90", 90), ("p99", 99))}


def main(src, out):
    cols = ["taxi_id", "trip_start_timestamp", "trip_end_timestamp", "trip_seconds", "fare", "trip_total"]
    d = pd.read_csv(src, usecols=cols, dtype={"taxi_id": "category"})
    res = {"rows": int(len(d))}
    for c in ("trip_start_timestamp", "trip_end_timestamp"):
        d[c] = pd.to_datetime(d[c], errors="coerce")
    bad = d["trip_start_timestamp"].isna() | d["trip_end_timestamp"].isna()
    res["dropped_missing_time"] = int(bad.sum())
    d = d[~bad]
    d["cab"] = d["taxi_id"].cat.codes
    d = d.sort_values(["cab", "trip_start_timestamp", "trip_end_timestamp"], kind="stable").reset_index(drop=True)
    res["cabs"] = int(d["cab"].nunique())
    res["trips"] = int(len(d))
    res["trips_by_month"] = {str(k): int(v) for k, v in d["trip_start_timestamp"].dt.to_period("M").value_counts().sort_index().items()}
    res["missing_fare"] = int(d["fare"].isna().sum())
    res["missing_seconds"] = int(d["trip_seconds"].isna().sum())

    start = d["trip_start_timestamp"].values.astype("datetime64[s]").astype(np.int64)
    end = d["trip_end_timestamp"].values.astype("datetime64[s]").astype(np.int64)
    cab = d["cab"].values
    first = np.r_[True, cab[1:] != cab[:-1]]
    # latest end among the cab's earlier trips
    prev_end = pd.Series(end).groupby(cab).cummax().shift(1).values
    pause = (start - prev_end) / 3600.0
    pause[first] = np.nan
    ok = ~first
    h = np.histogram(pause[ok], bins=PAUSE_EDGES)[0]
    res["pauses"] = {n: {"n": int(c), "share": float(c / ok.sum())} for n, c in zip(PAUSE_NAMES, h)}
    res["overlaps_over_15_min_share"] = float((pause[ok] < -0.2501).mean())

    new = first | (pause > GAP_HOURS)
    shift = np.cumsum(new) - 1
    n_shift = int(shift[-1] + 1)
    s_start = pd.Series(start).groupby(shift).min().values
    s_end = pd.Series(end).groupby(shift).max().values
    s_trips = np.bincount(shift)
    length = (s_end - s_start) / 3600.0
    fare = d["fare"].fillna(0).values
    s_fare = np.bincount(shift, fare)
    res["shifts"] = {"n": n_shift, "hours": q(length), "trips": q(s_trips), "fare_dollars": q(s_fare),
                     "share_one_trip": float((s_trips == 1).mean()),
                     "share_over_12_h": float((length > 12).mean()), "share_over_16_h": float((length > 16).mean()),
                     "share_over_24_h": float((length > 24).mean()),
                     "share_of_trips_in_shifts_over_16_h": float(s_trips[length > 16].sum() / len(d))}
    res["shifts_per_cab"] = q(np.bincount(cab[new]))

    last = np.r_[new[1:], True]
    hour = np.floor((end - s_start[shift]) / 3600.0).astype(int)
    stop = {}
    for k in range(0, 25):
        m = hour == k
        if m.sum():
            stop[str(k)] = {"trips": int(m.sum()), "share_last_of_shift": float(last[m].mean())}
    res["stopping_by_hour_into_shift"] = stop
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
