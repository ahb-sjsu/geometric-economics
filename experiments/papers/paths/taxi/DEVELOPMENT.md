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

## Pass 6. The test in the form the published paper used

Read 2026-11-12 from the authors' posted copies of the paper (pages 2426 to 2431) and its
appendix (Sections D.1 and E.5, Tables A7 to A9).

- **Their form.** Trips that end within ten minutes of 8.5 hours into the shift. Fares split by
  the hour of the shift in which they were earned, hour 1 to hour 8. Constants for driver, time,
  195 neighbourhoods and weather.
- **Their effect falls off gradually.** Table 2, last column, percent change in stopping for 1%
  more daily earnings arriving in hours 1 to 8: 0.01, 0.04, −0.04, 0.10, 0.36, 0.49, 0.79, 1.02.
  The table came through text extraction with its columns out of line. This reading of the last
  column agrees with the text, which gives 10.2% for the eighth hour.
- **The trip just ended is not taken apart** in what was read. A trip that ends at 8.5 hours
  ends in the ninth hour, and no term for the ninth hour is in the table. Where its fare sits
  is not stated in the pages read.
- **What they did check** (appendix D.1): adding distance, tips, airport fares and the number
  of trips as controls does not change the estimate, the effect holds on trips inside
  Manhattan, and a constant for each pair of driver and neighbourhood strengthens it. Earnings
  instrumented by other drivers' speed give 1.91 (standard error 0.93) for hour 8.

`stop_clockhour.py`, `results/stop_clockhour_dev_batch1.json` put the Chicago development cabs
through that form. Constants for cab, date, hour of the week and dropoff area. Change in the
probability of stopping for ten dollars, with 95% intervals:

| Ten dollars earned in | 10 minutes, 5% bar | 30 minutes, 10% bar |
|---|---|---|
| hour 5 | −0.0010 (−0.0038 to +0.0017) | −0.0005 (−0.0015 to +0.0004) |
| hour 6 | +0.0000 (−0.0028 to +0.0029) | +0.0013 (+0.0003 to +0.0023) |
| hour 7 | +0.0001 (−0.0027 to +0.0029) | +0.0005 (−0.0005 to +0.0014) |
| hour 8 | +0.0015 (−0.0012 to +0.0043) | −0.0010 (−0.0021 to +0.0001) |
| after 8 hours, the trip just ended included | +0.0154 (+0.0105 to +0.0202) | +0.0072 (+0.0051 to +0.0093) |
| after 8 hours, apart from the trip just ended | +0.0023 (−0.0026 to +0.0073) | −0.0029 (−0.0042 to −0.0016) |
| the trip just ended | +0.0334 (+0.0271 to +0.0396) | +0.0249 (+0.0207 to +0.0292) |
| decisions | 23,946 | 213,104 |

The first five rows are from the fit as published. The last two are from a second fit with the
trip just ended taken apart, where hours 5 to 8 read the same. The other two samples (10 minutes at the 10% bar, 30 minutes at the 5% bar) read the same way
and are in the result file.

- **Chicago shows no gradual fall-off.** Fares from hours 5 to 8 do nothing in any of the four
  samples. Only the trip just ended moves stopping.
- **Against the published sizes.** Their 1.35 points for 26 dollars in hour 8 is +0.0052 for ten
  dollars, and by the same scaling hour 7 is +0.0040 and hour 6 is +0.0025. The Chicago
  intervals for hours 7 and 8 lie below those in all four samples. The scaling is rough: other
  city, other fares, linear probability against their elasticities.
- **A fault found on the way.** The city rounds trip times to 15 minutes, so every decision
  within ten minutes of 8.5 hours sits at exactly 8.5 hours. A covariate for hours into the
  shift was constant there and the fit failed. It was replaced by a constant for each quarter
  hour. The rounding also moves a fare into a neighbouring hour now and then. That would smear
  a gradient across hours and would not remove one.
- **What this is.** In the published form the Chicago development cabs do not show the
  published pattern. The differences stand: the cab and not the driver, a selected set of cabs,
  times to 15 minutes, no weather, and a fall of the published effect onto the last trip has
  not been tested on New York data. Their replication files are public (openICPSR 125682) and
  have not been fetched.

## Pass 7. A second batch of months, and identifiers that are not one car

**Batch 2, split 2026-11-13.** 26 more verified months (July 2014 to July 2017, with breaks),
70,143,293 trips. By the rule of `DESIGN.md` Section 4, 34,024,129 went to development and
36,112,714 were held out and made unreadable when the split ended. 6,450 were dropped for an
identifier that does not start with a hexadecimal digit (`results/split_counts_batch2.json`).
The development halves of both batches were joined into one file of 42 months. The same cabs
are in both batches, so the new months are more data on the development cabs and not a fresh
sample of cabs.

**Pass 6 again on 42 months** (`results/stop_clockhour_dev_batch12.json`). It reads as before.

| Ten dollars earned in | 10 minutes, 5% bar | 30 minutes, 10% bar |
|---|---|---|
| hour 5 | +0.0014 (−0.0004 to +0.0032) | −0.0000 (−0.0007 to +0.0007) |
| hour 6 | +0.0009 (−0.0009 to +0.0028) | +0.0009 (+0.0001 to +0.0016) |
| hour 7 | +0.0021 (−0.0001 to +0.0043) | +0.0003 (−0.0005 to +0.0011) |
| hour 8 | +0.0008 (−0.0016 to +0.0032) | −0.0017 (−0.0025 to −0.0008) |
| the trip just ended | +0.0315 (+0.0268 to +0.0363) | +0.0245 (+0.0222 to +0.0269) |
| decisions | 62,515 | 585,986 |

- In the 10 minute sample at the 5% bar the interval for hour 7 now reaches +0.0043, above the
  scaled New York size of +0.0040. The statement of pass 6 that hours 7 and 8 lie below the
  published sizes in all four samples holds for three of the four on 42 months.
- Hour 1 is positive in all four samples, +0.0038 to +0.0047 with intervals clear of zero. This
  was not looked for and is not explained.

**Identifiers that are not one car.** The last-hour fit of pass 3 on 42 months gave the same
reading (trip just ended +0.0338 at the 5% bar and +0.0281 at the 10% bar, other fares of the
last hour −0.0016 and −0.0006). But the other fares of the last hour had a spread of 44 dollars
at the 10% bar against 14 at the 5% bar. `check_last_hour_tail.py`,
`results/last_hour_tail_dev_batch12.json` counted why, with no model.

- At the 10% bar 961 of 1,979,999 decisions have over 150 dollars of other fares in the last
  hour. 425 of them come from one identifier. The largest value is 4,908 dollars.
- Up to 436 trips of one shift end at the same rounded time. The 99.9th percentile is 5.
- So a few identifiers stand for more than one car. They are 0.05% of decisions and sit far out
  on the regressor.

**Change made.** A shift in which more than eight trips end at one rounded time is left out
whole, in `stop_timing.py`, `stop_where.py`, `stop_tip.py` and `stop_clockhour.py` (function
`crowded`). Eight was chosen from the percentiles above and not tuned on any coefficient. The
result files of passes 3 to 6 on batch 1 were made before this change and are kept as they
were. The all-cabs sample of `stop_timing.py`, which pass 3 judged not usable, is now run only
on request. The four fits are being rerun on 42 months with the change
(`results/*_dev_batch12c.json`), and those are the figures a registration would be set on.

`grade_taxi.py` is a first draft of a grader for such a registration. Its bars are provisional,
there is no registration text yet, and nothing is sealed.

## Where the taxi arena stands

On 16 months of development cabs, and again on 42, the prediction carried in, that recent earnings raise stopping
more than early ones, holds only through the fare of the trip just ended. The rest of the last
hour does nothing, a tip on that same trip does nothing, and in the published paper's own form
fares from hours 5 to 8 do nothing. That is not support for the claim that the timing of
earnings matters. It is closer to a finding about how shifts end.

The published paper reports a gradual fall-off over hours 5 to 8 that a last-trip effect alone
would not give. Chicago does not show it. Whether that is the city, the cab standing in for the
driver, or the selection of cabs is not known.

## Next

1. The owner decides between three courses. Stop the taxi line. Register on the held-out half
   the two things development shows (no effect of fares before the trip just ended, and an
   effect of that trip's fare), as a record that the published pattern is absent in Chicago. Or
   fetch the authors' public replication files, with the owner's word, and take the trip just
   ended apart on the New York data.
2. The retry of the failed months continues (44 verified on 2026-11-13, 42 of them split).
   Each new batch is split as it is verified.
