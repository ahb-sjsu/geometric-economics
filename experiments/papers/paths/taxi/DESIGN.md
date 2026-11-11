# Taxi: does the timing of earnings within a shift change the decision to stop?

**Status: design, 2026-11-11. Nothing downloaded when this was written. No registration drafted.**
Opened on the owner's word ("go with your recommendation, taxi first"). It is the first arena in
this line that is economic, with money, at scale.

## 1. Why this arena

Chess fixed the state and had no money. Poker had money and a small effect. A cab driver ending a
shift decides, after each fare, whether to stop or go on. The present state is hours worked and
money earned so far. The path is when in the shift the money came. If only the state mattered, a
dollar earned in the first hour and a dollar earned in the last would move the decision alike.

## 2. This is a replication and extension, and is to be described as one

Thakral and Tô, "Daily Labor Supply and Adaptive Reference Points", American Economic Review
111(8):2417–2443, 2021. Read 2026-11-11 from the authors' copy, pages 2417 to 2432.

- **Data.** Every fare of New York medallion cabs in 2013, with anonymised identifiers for driver
  and car and exact start and end times. About 41,000 drivers, 14,000 cabs and 173 million trips.
  After cleaning, over 5.8 million shifts by over 37,000 drivers.
- **Shift.** Consecutive trips not more than six hours apart.
- **Model.** After each trip the driver stops or continues. The probability of stopping is fit by
  local linear regression in a ten-minute window around a given time in the shift, with fare
  earnings split by the hour of the shift in which they came, minutes worked, driver effects, hour
  of day by day of week, day of year, neighbourhood and weather. Errors clustered by driver.
- **Result.** At 8.5 hours, with a baseline stopping probability of 13.2%, 10% more earnings
  overall raise the probability of stopping by 3.1%. If the extra comes in the eighth hour the rise
  is 10.2%. Earnings from the first four hours have little or no effect. The fitted reference
  point takes in about 40% of a surprise within an hour and about 90% within four.

So the claim "recent earnings move the stopping decision more than earlier earnings" is published,
for one city and one year. What this line can add is a second city over other years, a sealed
prediction, and the same lag curve read beside chess and poker.

## 3. The data

**Chicago "Taxi Trips (2013-2023)"**, City of Chicago data portal, dataset `wrvz-psew`. Read from
the portal's metadata on 2026-11-11, with no trip row fetched.

| | |
|---|---|
| Trips | 211,670,894 |
| Distinct taxi identifiers | 9,806 |
| Columns | trip id, taxi id, start and end time, seconds, miles, pickup and dropoff tract and community area, fare, tips, tolls, extras, total, payment type, company, centroids |
| Licence | "See Terms of Use". The terms page refused automated reading, so the terms are **not verified** |

**Three limits that the New York data did not have, stated by the city.**

- **The identifier is the cab, not the driver.** "The Taxi ID is consistent for any given taxi
  medallion number." Two drivers who share a cab are one identifier. A run of trips with no long
  gap may be two people's shifts joined. Development has to find a way to tell, or to bound the
  damage, before anything is registered. If it cannot, the study is not sealed.
- **Times are rounded to the nearest 15 minutes.** Trip length in seconds is exact. Hours into a
  shift are known to about a quarter of an hour, which is fine for earnings by hour and too coarse
  for a ten-minute window.
- **"Not all trips are reported but the City believes that most are."** A missing last trip makes
  a shift look as if it stopped early.

There is no weather in the file. Location is a community area or a census tract.

## 4. Split, fixed before download

The unit is the cab. **A cab is development if the first character of its taxi identifier is one of
`0` to `7`, and held out if it is `8` to `f`.** The identifiers are hexadecimal hashes by the
metadata, so this is about half each. An identifier that does not start with a hexadecimal digit
is dropped. The split is by cab so that no cab's habits are on both sides.

Trips from 2020 on are kept apart in both halves and are not part of a first registered test, since
the pandemic changed the trade.

The whole file is downloaded once. A program that reads only the taxi identifier and the year
routes each row to one of the files, and the held-out files are then made unreadable. No other
column of a held-out row is used by any program before a seal.

## 5. Prediction carried in, written before any trip is read

From Thakral and Tô, and in line with chess and poker. With hours worked held fixed, earnings in
the most recent hour of the shift raise the probability of stopping more than the same earnings
four or more hours earlier. No size is predicted for Chicago. The form of the test, the handling of
shared cabs and the bars come from development and are then sealed.

## 6. What a result would and would not show

A pass would say the recency of earnings replicates in a second city. It would support "history
matters beyond the present state" in an economic setting with money. It would not single out this
line's thesis, since an adaptive reference point is the published explanation and predicts the
same thing. Telling the two apart needs a place where they disagree, which has not been found yet.
