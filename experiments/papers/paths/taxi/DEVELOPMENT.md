# Taxi: development record

Development cabs only, by the rule of `DESIGN.md` Section 4. The held-out files are unreadable
and unopened. Nothing here is registered. Drafted by Claude.

## Split of the first batch, 2026-11-12

The download is slow. After 17 hours the portal had given 16 verified months of the 84 wanted
(January to November 2013, January, February and May 2014, January and February 2017). Two months
failed and are to be retried. The design said the whole file would be downloaded once and then
split. That was changed on 2026-11-12: months are split as they are verified, by the same rule,
which reads only the taxi identifier and the year. The rule is per row, so splitting in batches
gives the same two halves as splitting once.

`split_rows.py` on the 16 months, `results/split_counts_batch1.json`.

| | Trips |
|---|---|
| Rows read | 36,899,029 |
| Development | 18,050,664 |
| Held out, made unreadable when the split ended | 18,847,200 |
| Dropped, identifier not hexadecimal | 1,165 |

**One slip, recorded.** While checking the column names, the first data row of the unsplit
January 2013 file was printed, cut off partway through its start time. Its taxi identifier begins
with 5, so it is a development cab. No held-out row was seen. Column names are to be read from
the header line alone from here on.

## Pass 1. What a shift looks like

`describe_shifts.py`, `results/shifts_dev_batch1.json`. 18,048,582 trips by 3,875 cabs. A shift
is a run of a cab's trips with no pause over six hours, the rule of Thakral and Tô. That gives
932,061 shifts.

- **Six hours is a natural place to cut.** Pauses between a cab's trips are fewest at six to
  eight hours (0.7% of pauses), with 1.2% at four to six and 1.4% at eight to twelve.
- **Shifts are too long to be one driver's.** The median is 9.5 hours, a quarter run past 13.5
  and a tenth past 17.5. 13% of shifts run past 16 hours and they hold 40% of all trips. 6% run
  past 24 hours. This is the limit the design named: the identifier is the cab, and two drivers
  back to back look like one shift.
- 0.6% of trips start more than 15 minutes before the cab's last trip ended, which one car
  cannot do. Times are rounded to 15 minutes, so shorter overlaps mean nothing.
- 3.2% of trips have no length in seconds. 131 have no fare.
- The share of trips that end a shift rises from 2.4% in the second hour to 11.9% in hours 14 to
  16. At 8 to 9 hours it is 6.7% to 7.6%, about half the 13.2% the published paper gives for New
  York at 8.5 hours, as it would be if many of these shifts are two drivers' joined.

## Pass 2. Cabs that look like one driver

`single_driver_cabs.py`, `results/single_driver_dev_batch1.json`. For each of the 3,389 cabs with
50 shifts or more, the share of its shifts longer than 14 hours.

- **There is no clean divide.** The share runs from under 2% (a tenth of cabs) through a median
  of 19% to over 45% (a tenth). Cabs do not fall into two groups.
- A bar on that share keeps these:

  | Share of shifts over 14 hours | Cabs | Shifts | Trips | Median shift | Stopping at 8 to 9 hours |
  |---|---|---|---|---|---|
  | at most 2% | 386 | 79,925 | 814,204 | 6.75 h | 14.6% |
  | at most 5% | 627 | 146,282 | 1,534,794 | 7.0 h | 13.2% |
  | at most 10% | 1,002 | 255,758 | 2,795,453 | 7.25 h | 11.8% |

- **At a bar of 5% the shifts look like the published ones.** One shift on a working day
  (median 1.04), a median of 7 hours, nine in ten under 11.75 hours, and a stopping rate of 13.2%
  in the ninth hour, the same as New York's 13.2% at 8.5 hours.
- The cost is 8.5% of the trips. With all 84 months that would be roughly 750,000 shifts on the
  development side, against 5.8 million in the published paper. That is an extrapolation from 16
  months.
- **The bar selects on the length of shifts, which is the outcome.** It is set per cab over all
  its shifts and not per shift, so no single stopping decision decides whether it is kept. It
  still keeps cabs whose drivers stop early. Any registered test has to say so.
- The figure for hours on shift per calendar day in the result file is not usable. The months
  are not contiguous, so the span from a cab's first trip to its last holds months not downloaded.

## Pass 3. Earnings by how long ago they came, and a confound

`stop_timing.py`, `results/stop_timing_dev_batch1.json` and
`results/stop_timing_apart_dev_batch1.json`. A decision is the end of a trip 6 to 10 hours into
its shift. The outcome is whether that trip was the last of the shift. A linear probability model
on the fares of the shift so far, split by when the trip that earned them ended, with a constant
for each cab, date, hour of the week and quarter hour into the shift. Standard errors clustered
by cab. Coefficients are the change in the probability of stopping for ten more dollars.

**First form, as in the prediction carried in.** Cabs at the 5% bar, 626 cabs, 408,998
decisions, stopping rate 11.9%.

| Ten dollars earned | Change in the probability of stopping |
|---|---|
| in the last hour | +0.0099 (+0.0082 to +0.0117) |
| one to two hours before | −0.0008 (−0.0019 to +0.0004) |
| two to four hours before | −0.0005 (−0.0014 to +0.0004) |
| more than four hours before | −0.0009 (−0.0016 to −0.0002) |
| last hour minus more than four hours before | +0.0108 (+0.0089 to +0.0127) |

This is the published shape. Recent money raises stopping and early money does not. At the 10%
bar the difference is +0.0077 (+0.0065 to +0.0090).

**Second form, with the last hour split in two.** The fare of the trip just ended, and the other
fares of the last hour.

| Ten dollars earned | 5% bar | 10% bar |
|---|---|---|
| on the trip just ended | +0.0312 (+0.0284 to +0.0339) | +0.0253 (+0.0234 to +0.0272) |
| in the rest of the last hour | −0.0022 (−0.0036 to −0.0008) | −0.0034 (−0.0042 to −0.0026) |
| one to two hours before | −0.0013 (−0.0025 to −0.0002) | −0.0018 (−0.0025 to −0.0011) |
| two to four hours before | −0.0003 (−0.0011 to +0.0005) | −0.0007 (−0.0012 to −0.0001) |
| more than four hours before | −0.0007 (−0.0014 to −0.0000) | −0.0010 (−0.0014 to −0.0005) |
| rest of the last hour minus more than four hours before | −0.0014 (−0.0029 to +0.0000) | −0.0025 (−0.0033 to −0.0016) |

- **The whole effect of the last hour is the fare of the trip just ended.** Take that trip out and
  money earned in the rest of the last hour lowers stopping a little, like money earned at any
  earlier time. It does not raise it.
- **A large last fare has a plain other reading.** The last trip of a shift may be a long run
  toward home or the garage, or to an airport at the edge of the city. Then the shift ends after
  a large fare because of where the trip went, and not because of what it paid. This file cannot
  tell the two apart. So the first table is not evidence for the claim.
- **Money earned earlier lowers stopping slightly at every distance.** That is the sign a good
  day would give: a driver who is earning well stays out. It is the opposite of a daily income
  target, and it is small, a tenth of a point in a hundred for ten dollars.
- So on these 16 months the prediction carried in is not supported once the trip just ended is
  set apart. It is supported only in a form that a long last run would also produce.

**What is not known.**

- Whether the published paper's result for New York has the same sensitivity. Its pages 2417 to
  2432 were read and the treatment of the final trip was not looked for. It has exact times and
  driver identifiers, a ten-minute window and weather, none of which this file has.
- Where the last trip goes. The file has pickup and dropoff community areas. A check: whether
  the last trip of a shift ends in the same few areas for a given cab, and whether the effect of
  the trip just ended survives a constant for the dropoff area.
- Whether the effect of the trip just ended is the fare or the time. A long trip takes long, and
  the constants for quarter hours into the shift do not hold the length of the last trip fixed.

**All cabs with 50 shifts, no bar.** 3,388 cabs, 3,369,285 decisions, stopping rate 6.3%. The
first form gives +0.0005 for last hour minus more than four hours before. This sample is not
used. Its shifts are the joined ones of pass 1, and the last hour's fares have a spread of 141
dollars there against 16 at the 5% bar, which has not been looked into.

## Pass 4. Where the trip just ended went, and how long it took

`stop_where.py`, `results/stop_where_dev_batch1.json`. The second form of pass 3 again (A), then
with a constant for each pair of cab and dropoff community area of the trip just ended (B), then
with the minutes of that trip added (C). Ten dollars on the trip just ended:

| | 5% bar | 10% bar |
|---|---|---|
| A, as pass 3 | +0.0312 (+0.0284 to +0.0339) | +0.0253 (+0.0234 to +0.0272) |
| B, same cab and same dropoff area | +0.0224 (+0.0198 to +0.0249) | +0.0181 (+0.0164 to +0.0198) |
| C, and the minutes of the trip | +0.0243 (+0.0215 to +0.0272) | +0.0193 (+0.0174 to +0.0211) |

- **Place and length take away about a quarter and leave the rest.** Among one cab's trips to one
  community area, a larger fare on the trip just ended still goes with stopping.
- In B and C money in the rest of the last hour is at zero (−0.0000 and −0.0005 at the 5% bar)
  and money earned earlier is at zero or just above (+0.0004 to +0.0013).
- The last trip of a shift pays 17.13 dollars on average against 11.80 for other trips in the
  window, 45% more, and takes 13.9 minutes against 12.3, 13% more. So it is a faster, longer
  run and not a slower one.
- A cab's most common place to end a shift is not a home. Last trips end there less often
  (15%) than other trips do (22%), so that area is simply where the cab works most. The file
  gives no dropoff area for 23% of these trips. A community area is also large. A constant for
  it does not hold the distance toward a garage fixed.

## Pass 5. A tip is money that does not depend on the trip

`stop_tip.py`, `results/stop_tip_dev_batch1.json`. Given a trip's fare, place and length, the tip
is the passenger's choice and the driver learns it when the trip is over. If money just received
moves stopping, a larger tip should raise it. If the fare effect is about the kind of trip, the
tip should do nothing. Tips are recorded for card payments only, so the decisions are trip ends
paid by credit card (144,638 at the 5% bar, 267,289 at the 10% bar). The mean tip is 3.35
dollars, the median tip is 21% of the fare and 9% of card trips have no tip. Constants as in B
of pass 4, with the fare, the minutes and the earlier fares in the fit.

| | 5% bar | 10% bar |
|---|---|---|
| Ten dollars of tip on the trip just ended | +0.0079 (−0.0036 to +0.0194) | +0.0026 (−0.0048 to +0.0101) |
| Ten dollars of fare on the trip just ended, same fit | +0.0232 (+0.0196 to +0.0269) | +0.0191 (+0.0167 to +0.0214) |
| Tip over 20% of the fare, against no tip | −0.0083 (−0.0179 to +0.0012) | −0.0077 (−0.0141 to −0.0013) |
| Tip up to 20% of the fare, against no tip | −0.0034 (−0.0138 to +0.0069) | −0.0044 (−0.0113 to +0.0024) |

- **A tip does not act like a fare.** In dollars its effect is not told from zero. At the 10% bar
  the top of its interval (+0.0101) is below the bottom of the fare's (+0.0167). As a share of
  the fare a generous tip goes, if anything, with less stopping.
- So money that arrives with the trip just ended, and is not tied to what kind of trip it was,
  does not raise stopping. The fare does. The plainest reading is that the fare effect is about
  the trip and not about the money: a shift tends to end on a long run.
- The 5% bar alone cannot rule out a tip effect a third the size of the fare's.
- Earlier tips in the shift go with more stopping, +0.0055 (+0.0024 to +0.0086) for ten dollars
  at the 5% bar and +0.0063 at the 10% bar, where earlier fares do nothing. This was not looked
  for. Recorded tips also count how many earlier trips were paid by card, so it may be a trait
  of the shift. It is not read as an income target.
- What the tip test cannot rule out: passengers on some kinds of trip tip more, in ways the
  fare, the area and the minutes do not capture.

## Where the taxi arena stands

On 16 months of development cabs the prediction carried in, that recent earnings raise stopping
more than early ones, holds only through the fare of the trip just ended. The rest of the last
hour does nothing, and a tip on that same trip does nothing. That is not support for the claim
that the timing of earnings matters. It is closer to a finding about how shifts end.

This is not a failed replication of the published paper. The data differ (the cab and not the
driver, times to 15 minutes, a selected set of cabs, no weather) and the model here is simpler.
Whether the published result would survive the same split of the last hour is not known.

## Next

1. Read the rest of the published paper for how it treats the final trip. If it does not, a
   short note to its authors may be worth more than a registration here. The owner's call.
2. Decide whether taxi goes to a registration at all. As it stands there is no development
   effect of the kind the campaign is after to register.
3. The retry of the failed months continues. Each new batch is split as it is verified.
