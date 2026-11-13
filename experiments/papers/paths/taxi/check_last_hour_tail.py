"""Development check: where do very large last-hour fares come from?

    python check_last_hour_tail.py dev_2013_2019.csv.gz out.json

On batches 1 and 2 the fares of the last hour apart from the trip just ended
have a spread of 44 dollars at the 10% bar against 14 at the 5% bar. One car
with one driver cannot earn hundreds of dollars in an hour of city fares. This
file counts, with no model, the decisions of stop_timing.py whose last-hour
fares pass 150 dollars, how many cabs and shifts they come from, and how many
trips of a shift end at one rounded time. No identifier is written.
"""
import json
import sys

import numpy as np
import pandas as pd

from stop_timing import BIG, GAP_HOURS, LONG_HOURS, MIN_SHIFTS, WINDOW

LIMIT = 150.0


def main(src, out):
    d = pd.read_csv(src, usecols=["taxi_id", "trip_start_timestamp", "trip_end_timestamp", "fare"], dtype={"taxi_id": "category"})
    for c in ("trip_start_timestamp", "trip_end_timestamp"):
        d[c] = pd.to_datetime(d[c], errors="coerce")
    d = d.dropna(subset=["trip_start_timestamp", "trip_end_timestamp"])
    d["cab"] = d["taxi_id"].cat.codes
    d = d.sort_values(["cab", "trip_start_timestamp", "trip_end_timestamp"], kind="stable").reset_index(drop=True)
    start = d["trip_start_timestamp"].values.astype("datetime64[s]").astype(np.int64)
    end = d["trip_end_timestamp"].values.astype("datetime64[s]").astype(np.int64)
    cab = d["cab"].values.astype(np.int64)
    fare = np.clip(d["fare"].fillna(0).values, 0, 200)
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
    shift, end, fare, cab = shift[order], end[order], fare[order], cab[order]
    cum = np.cumsum(fare)
    idx0 = np.r_[0, np.flatnonzero(shift[1:] != shift[:-1]) + 1]
    base = np.r_[0.0, cum][idx0]
    key = shift * BIG + (end - end.min())
    hours_in = (end - s_start[shift]) / 3600.0
    j = np.searchsorted(key, key - 3600, side="right") - 1
    b1 = np.where(j >= idx0[shift], cum[np.maximum(j, 0)] - base[shift], 0.0)
    rest = cum - base[shift] - b1 - fare
    # trips of the shift that end at the same rounded time as this one
    same = pd.Series(np.ones(len(key))).groupby(key).transform("sum").values
    # trips and fares of a whole shift per hour of its length
    n_trips = np.bincount(shift)
    per_hour = n_trips / np.maximum(length, 0.25)
    in_window = (hours_in >= WINDOW[0]) & (hours_in < WINDOW[1])
    res = {"limit_dollars": LIMIT, "samples": {}}
    for label, bar in (("long_share_at_most_0.05", 0.05), ("long_share_at_most_0.10", 0.10)):
        keep_cab = (n_sh >= MIN_SHIFTS) & (share_long <= bar)
        m = in_window & keep_cab[cab]
        big = m & (rest > LIMIT)
        cabs_big = np.bincount(cab[big], minlength=ncab)
        cabs_all = np.bincount(cab[m], minlength=ncab)
        top = np.sort(cabs_big)[::-1]
        share_of_cab = cabs_big[cabs_big > 0] / cabs_all[cabs_big > 0]
        s = {"decisions": int(m.sum()), "over_limit": int(big.sum()),
             "rest_dollars_percentiles": {str(p): float(np.percentile(rest[m], p)) for p in (50, 90, 99, 99.9, 99.99, 100)},
             "cabs_in_sample": int((cabs_all > 0).sum()), "cabs_with_any_over_limit": int((cabs_big > 0).sum()),
             "over_limit_from_top_cabs": {"1": int(top[:1].sum()), "5": int(top[:5].sum()), "20": int(top[:20].sum())},
             "cabs_with_over_1_percent_of_decisions_over_limit": int((share_of_cab > 0.01).sum()),
             "shifts_with_any_over_limit": int(len(np.unique(shift[big]))),
             "trips_ending_at_same_time_percentiles": {str(p): float(np.percentile(same[m], p)) for p in (50, 99, 99.9, 100)},
             "trips_ending_at_same_time_when_over_limit_median": float(np.median(same[big])) if big.any() else None,
             "shift_trips_per_hour_percentiles": {str(p): float(np.percentile(per_hour[shift[m]], p)) for p in (50, 99, 99.9, 100)},
             "shift_trips_per_hour_when_over_limit_median": float(np.median(per_hour[shift[big]])) if big.any() else None}
        res["samples"][label] = s
        print(label, json.dumps(s), flush=True)
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
