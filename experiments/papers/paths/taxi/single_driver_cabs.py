"""Development pass 2: can cabs driven by one person be told from shared cabs?

    python single_driver_cabs.py dev_2013_2019.csv.gz out.json

Pass 1 found that 13% of shifts run past 16 hours and hold 40% of trips. The
identifier is the cab, so a long shift is likely two drivers back to back. A
test of when a driver stops needs shifts that are one person's.

A cab with one driver should show three things: almost no shift past 14 hours,
about one shift on a day it works, and long pauses between shifts. For each cab
with 50 shifts or more this file computes

    share_long        share of its shifts longer than 14 hours
    shifts_per_day    shifts divided by distinct dates on which a shift began
    hours_per_day     hours on shift divided by the days from its first to its last trip

and then, for bars on share_long of 2%, 5% and 10%, how many cabs, shifts and
trips pass, their shift lengths, and the share of trips that were the last of
their shift by hour into the shift. Nothing is tested. The bar is chosen from
these counts and from nothing about earnings.
"""
import json
import sys

import numpy as np
import pandas as pd

GAP_HOURS = 6.0
LONG_HOURS = 14.0
MIN_SHIFTS = 50


def q(v):
    return {k: float(np.percentile(v, p)) for k, p in (("p10", 10), ("p25", 25), ("median", 50), ("p75", 75),
                                                       ("p90", 90), ("p99", 99))}


def main(src, out):
    d = pd.read_csv(src, usecols=["taxi_id", "trip_start_timestamp", "trip_end_timestamp"], dtype={"taxi_id": "category"})
    for c in ("trip_start_timestamp", "trip_end_timestamp"):
        d[c] = pd.to_datetime(d[c], errors="coerce")
    d = d.dropna()
    d["cab"] = d["taxi_id"].cat.codes
    d = d.sort_values(["cab", "trip_start_timestamp", "trip_end_timestamp"], kind="stable").reset_index(drop=True)
    start = d["trip_start_timestamp"].values.astype("datetime64[s]").astype(np.int64)
    end = d["trip_end_timestamp"].values.astype("datetime64[s]").astype(np.int64)
    cab = d["cab"].values
    first = np.r_[True, cab[1:] != cab[:-1]]
    prev_end = pd.Series(end).groupby(cab).cummax().shift(1).values
    pause = (start - prev_end) / 3600.0
    pause[first] = np.nan
    new = first | (pause > GAP_HOURS)
    shift = np.cumsum(new) - 1
    s_start = pd.Series(start).groupby(shift).min().values
    s_end = pd.Series(end).groupby(shift).max().values
    s_cab = cab[new]
    s_trips = np.bincount(shift)
    length = (s_end - s_start) / 3600.0

    ncab = int(cab.max()) + 1
    n_sh = np.bincount(s_cab, minlength=ncab)
    n_long = np.bincount(s_cab, length > LONG_HOURS, minlength=ncab)
    hours = np.bincount(s_cab, length, minlength=ncab)
    days = pd.Series(s_start // 86400).groupby(s_cab).nunique().reindex(range(ncab), fill_value=0).values
    span = (pd.Series(end).groupby(cab).max().values - pd.Series(start).groupby(cab).min().values) / 86400.0
    enough = n_sh >= MIN_SHIFTS
    share_long = np.where(n_sh > 0, n_long / np.maximum(n_sh, 1), np.nan)
    res = {"cabs": ncab, "cabs_with_%d_shifts_or_more" % MIN_SHIFTS: int(enough.sum()),
           "share_long_over_cabs": q(share_long[enough]),
           "shifts_per_day_over_cabs": q(n_sh[enough] / np.maximum(days[enough], 1)),
           "hours_on_shift_per_calendar_day_over_cabs": q(hours[enough] / np.maximum(span[enough], 1)),
           "histogram_share_long": {"%.1f-%.1f" % (a, a + 0.1): int(((share_long[enough] >= a) & (share_long[enough] < a + 0.1 + (a > 0.85))).sum())
                                    for a in np.arange(0, 1, 0.1)},
           "bars": {}}
    last = np.r_[new[1:], True]
    hour = np.floor((end - s_start[shift]) / 3600.0).astype(int)
    for bar in (0.02, 0.05, 0.10):
        keep_cab = enough & (share_long <= bar)
        ks = keep_cab[s_cab]
        kt = keep_cab[cab]
        b = {"cabs": int(keep_cab.sum()), "shifts": int(ks.sum()), "trips": int(kt.sum()),
             "share_of_all_trips": float(kt.mean()),
             "shift_hours": q(length[ks]), "shift_trips": q(s_trips[ks]),
             "shifts_per_day": q(n_sh[keep_cab] / np.maximum(days[keep_cab], 1)),
             "hours_on_shift_per_calendar_day": q(hours[keep_cab] / np.maximum(span[keep_cab], 1)),
             "share_last_of_shift_by_hour": {}}
        for k in range(0, 15):
            m = kt & (hour == k)
            if m.sum():
                b["share_last_of_shift_by_hour"][str(k)] = {"trips": int(m.sum()), "share": float(last[m].mean())}
        res["bars"]["%.2f" % bar] = b
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
