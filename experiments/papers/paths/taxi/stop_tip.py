"""Development pass 5: does a tip on the trip just ended move stopping?

    python stop_tip.py dev_2013_2019.csv.gz out.json

Passes 3 and 4 found that a larger fare on the trip just ended goes with
stopping, and that the place and length of the trip do not remove it. A fare
is still tied to the trip: a driver heading home may take a long run on
purpose. A tip is not. Given the fare, the place and the length of a trip, the
tip is the passenger's choice, and the driver learns it only when the trip is
over. If money just received moves the decision to stop, a larger tip should
raise stopping. If the fare effect is about the kind of trip, the tip should
do nothing.

Tips are recorded only for trips paid by card, so the decisions used are trip
ends, 6 to 10 hours into the shift, whose trip was paid by credit card. Same
shifts and cabs as stop_timing.py.

Linear probability of stopping on

    tip_now        the tip on the trip just ended, tens of dollars
    e_now          its fare
    e_0_1_rest, e_1_2, e_2_4, e_4plus     fares earlier in the shift, as before
    tips_before    recorded tips earlier in the shift
    ten_minutes    length of the trip just ended

with a constant for each cab, date, hour of the week, quarter hour into the
shift, and pair of cab and dropoff area. Clustered by cab.

A second fit replaces tip_now by the tip as a share of the fare, in three
levels (none, up to 20%, over 20%), since a tip in dollars grows with the fare.

What this cannot rule out: passengers on some kinds of trip tip more, in ways
the fare, place and length do not capture.
"""
import json
import sys

import numpy as np
import pandas as pd

from stop_timing import BIG, GAP_HOURS, LONG_HOURS, MIN_SHIFTS, WINDOW, crowded, fit


def main(src, out):
    d = pd.read_csv(src, usecols=["taxi_id", "trip_start_timestamp", "trip_end_timestamp", "fare", "tips", "payment_type",
                                  "dropoff_community_area"], dtype={"taxi_id": "category", "payment_type": "category"})
    for c in ("trip_start_timestamp", "trip_end_timestamp"):
        d[c] = pd.to_datetime(d[c], errors="coerce")
    d = d.dropna(subset=["trip_start_timestamp", "trip_end_timestamp"])
    res = {"payment_types": {str(k): int(v) for k, v in d["payment_type"].value_counts().items()}}
    d["cab"] = d["taxi_id"].cat.codes
    d = d.sort_values(["cab", "trip_start_timestamp", "trip_end_timestamp"], kind="stable").reset_index(drop=True)
    start = d["trip_start_timestamp"].values.astype("datetime64[s]").astype(np.int64)
    end = d["trip_end_timestamp"].values.astype("datetime64[s]").astype(np.int64)
    cab = d["cab"].values.astype(np.int64)
    fare = np.clip(d["fare"].fillna(0).values, 0, 200)
    tip = np.clip(d["tips"].fillna(0).values, 0, 100)
    card = (d["payment_type"].astype(str).str.lower() == "credit card").values
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
    shift, end, start, fare, tip, card, cab, area = (v[order] for v in (shift, end, start, fare, tip, card, cab, area))
    minutes = np.clip((end - start) / 60.0, 0, 240)
    last = np.r_[shift[1:] != shift[:-1], True]
    cum = np.cumsum(fare)
    cumtip = np.cumsum(tip)
    idx0 = np.r_[0, np.flatnonzero(shift[1:] != shift[:-1]) + 1]
    base = np.r_[0.0, cum][idx0]
    basetip = np.r_[0.0, cumtip][idx0]
    key = shift * BIG + (end - end.min())
    hours_in = (end - s_start[shift]) / 3600.0

    def upto(lookback):
        j = np.searchsorted(key, key - lookback, side="right") - 1
        inside = j >= idx0[shift]
        return np.where(inside, cum[np.maximum(j, 0)] - base[shift], 0.0)

    total = cum - base[shift]
    b1, b2, b4 = upto(3600), upto(7200), upto(14400)
    tips_before = cumtip - basetip[shift] - tip
    common = np.column_stack([fare, total - b1 - fare, b1 - b2, b2 - b4, b4, tips_before]) / 10.0
    common_names = ("e_now", "e_0_1_rest", "e_1_2", "e_2_4", "e_4plus", "tips_before")
    in_window = (hours_in >= WINDOW[0]) & (hours_in < WINDOW[1]) & ~crowded(key)
    t = pd.to_datetime(end, unit="s")
    how = t.dayofweek.values * 24 + t.hour.values
    date = end // 86400
    qbin = np.floor(hours_in * 4).astype(int)
    pair = cab * 100 + area
    share = np.where(fare > 0, tip / np.maximum(fare, 0.01), 0.0)

    res["samples"] = {}
    for label, bar in (("long_share_at_most_0.05", 0.05), ("long_share_at_most_0.10", 0.10)):
        keep_cab = (n_sh >= MIN_SHIFTS) & (share_long <= bar)
        w = in_window & keep_cab[cab]
        m = w & card & (fare > 0)
        y = last[m].astype(float)
        s = {"decisions_in_window": int(w.sum()), "of_which_paid_by_card": int(m.sum()), "stop_rate": float(y.mean()),
             "stop_rate_all_payment": float(last[w].mean()),
             "tip_dollars": {"mean": float(tip[m].mean()), "sd": float(tip[m].std()), "share_zero": float((tip[m] == 0).mean())},
             "tip_share_of_fare": {k: float(np.percentile(share[m], p)) for k, p in (("p10", 10), ("median", 50), ("p90", 90))},
             "stop_rate_by_tip_share": {"none": float(y[share[m] == 0].mean()),
                                        "up_to_20_percent": float(y[(share[m] > 0) & (share[m] <= 0.2)].mean()),
                                        "over_20_percent": float(y[share[m] > 0.2].mean())}}
        groups = [cab[m], date[m], how[m], qbin[m], pair[m]]
        mins = minutes[m] / 10.0
        fits = (("dollars", np.column_stack([tip[m] / 10.0, common[m], mins]), ("tip_now",) + common_names + ("ten_minutes",)),
                ("share", np.column_stack([(share[m] > 0) & (share[m] <= 0.2), share[m] > 0.2, common[m], mins]).astype(float),
                 ("tip_up_to_20_percent", "tip_over_20_percent") + common_names + ("ten_minutes",)))
        for name, X, names in fits:
            beta, V, nfe = fit(y, X, groups, cab[m])
            se = np.sqrt(np.diag(V))
            s[name] = {"constants_removed": int(nfe),
                       "coef": {n: {"coef": float(beta[j]), "se": float(se[j]),
                                    "ci95": [float(beta[j] - 1.96 * se[j]), float(beta[j] + 1.96 * se[j])]}
                                for j, n in enumerate(names)}}
            print(label, name, json.dumps({n: [round(v["coef"], 4), round(v["ci95"][0], 4), round(v["ci95"][1], 4)]
                                           for n, v in s[name]["coef"].items()}), flush=True)
        print(label, json.dumps({k: v for k, v in s.items() if k not in ("dollars", "share")}), flush=True)
        res["samples"][label] = s
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
