"""Development pass 4: is the effect of the trip just ended about where it went and how long it took?

    python stop_where.py dev_2013_2019.csv.gz out.json

Pass 3 found that the whole effect of the last hour's earnings on stopping sits
in the fare of the trip just ended. A long last run toward home would give
that with no effect of money. This file holds the place and the length of that
trip fixed and looks again. Same shifts, cabs, decisions and other constants
as stop_timing.py with `apart`.

    A   as pass 3, to check this file reproduces it
    B   and a constant for each pair of cab and dropoff community area of the
        trip just ended, so a trip is compared with the same cab's other trips
        to the same area
    C   B and the minutes the trip just ended took, in tens

Also written, with no model: for each cab the dropoff area where its shifts
most often end (its home area, so called here), the share of last trips that
end there, the share of other trips in the window that end there, and the mean
fare and minutes of last trips against other trips.
"""
import json
import sys

import numpy as np
import pandas as pd

from stop_timing import BIG, GAP_HOURS, LONG_HOURS, MIN_SHIFTS, WINDOW, fit

NAMES = ("e_now", "e_0_1_rest", "e_1_2", "e_2_4", "e_4plus")


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
    area = d["dropoff_community_area"].fillna(0).values.astype(np.int64)      # 0 stands for not given
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
    shift, end, start, fare, cab, area = shift[order], end[order], start[order], fare[order], cab[order], area[order]
    minutes = np.clip((end - start) / 60.0, 0, 240)
    last = np.r_[shift[1:] != shift[:-1], True]
    cum = np.cumsum(fare)
    idx0 = np.r_[0, np.flatnonzero(shift[1:] != shift[:-1]) + 1]
    base = np.r_[0.0, cum][idx0]
    key = shift * BIG + (end - end.min())
    hours_in = (end - s_start[shift]) / 3600.0

    def upto(lookback):
        j = np.searchsorted(key, key - lookback, side="right") - 1
        inside = j >= idx0[shift]
        return np.where(inside, cum[np.maximum(j, 0)] - base[shift], 0.0)

    total = cum - base[shift]
    b1, b2, b4 = upto(3600), upto(7200), upto(14400)
    X_all = np.column_stack([fare, total - b1 - fare, b1 - b2, b2 - b4, b4]) / 10.0
    in_window = (hours_in >= WINDOW[0]) & (hours_in < WINDOW[1])
    t = pd.to_datetime(end, unit="s")
    how = t.dayofweek.values * 24 + t.hour.values
    date = end // 86400
    qbin = np.floor(hours_in * 4).astype(int)
    pair = cab * 100 + area

    res = {"samples": {}}
    for label, bar in (("long_share_at_most_0.05", 0.05), ("long_share_at_most_0.10", 0.10)):
        keep_cab = (n_sh >= MIN_SHIFTS) & (share_long <= bar)
        m = in_window & keep_cab[cab]
        y = last[m].astype(float)
        s = {"decisions": int(m.sum()), "stop_rate": float(y.mean()), "share_dropoff_area_not_given": float((area[m] == 0).mean())}

        # where shifts end, with no model. Home area: the cab's most common dropoff area over last trips of all its shifts.
        lt = pd.DataFrame({"cab": cab[last & keep_cab[cab]], "area": area[last & keep_cab[cab]]})
        lt = lt[lt["area"] > 0]
        home = lt.groupby("cab")["area"].agg(lambda v: v.value_counts().index[0])
        home_of = np.zeros(ncab, dtype=np.int64)
        home_of[home.index.values] = home.values
        at_home = (area[m] == home_of[cab[m]]) & (area[m] > 0)
        s["home_area"] = {"share_of_last_trips_ending_there": float(at_home[y == 1].mean()),
                          "share_of_other_trips_ending_there": float(at_home[y == 0].mean())}
        s["trip_just_ended"] = {"mean_fare_last": float(fare[m][y == 1].mean()), "mean_fare_other": float(fare[m][y == 0].mean()),
                                "mean_minutes_last": float(minutes[m][y == 1].mean()),
                                "mean_minutes_other": float(minutes[m][y == 0].mean()),
                                "stop_rate_when_ending_in_home_area": float(y[at_home].mean()),
                                "stop_rate_elsewhere": float(y[~at_home].mean())}

        groups = [cab[m], date[m], how[m], qbin[m]]
        for name, g, X, names in (
                ("A", groups, X_all[m], NAMES),
                ("B", groups + [pair[m]], X_all[m], NAMES),
                ("C", groups + [pair[m]], np.column_stack([X_all[m], minutes[m] / 10.0]), NAMES + ("ten_minutes_of_trip_just_ended",))):
            beta, V, nfe = fit(y, X, g, cab[m])
            se = np.sqrt(np.diag(V))
            s[name] = {"constants_removed": int(nfe),
                       "coef": {n: {"coef": float(beta[j]), "se": float(se[j]),
                                    "ci95": [float(beta[j] - 1.96 * se[j]), float(beta[j] + 1.96 * se[j])]}
                                for j, n in enumerate(names)}}
            print(label, name, json.dumps({n: [round(v["coef"], 4), round(v["ci95"][0], 4), round(v["ci95"][1], 4)]
                                           for n, v in s[name]["coef"].items()}), flush=True)
        print(label, json.dumps({k: s[k] for k in ("decisions", "stop_rate", "share_dropoff_area_not_given", "home_area", "trip_just_ended")}), flush=True)
        res["samples"][label] = s
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
