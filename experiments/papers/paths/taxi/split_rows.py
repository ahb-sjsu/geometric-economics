"""Route each row of the Chicago taxi file to development or held out, reading two columns.

    python split_rows.py Taxi_Trips_2013-2023.csv out_dir

The rule is DESIGN.md Section 4, fixed before the download. A cab is development
if the first character of its taxi identifier is 0 to 7 and held out if it is
8 to f. Other identifiers are dropped. Trips from 2020 on go to separate files.
Only the taxi identifier and the year of the start time are parsed. Every other
column is copied as text and is not looked at. The line is written unchanged.

Writes dev_2013_2019.csv.gz, dev_2020_on.csv.gz, heldout_2013_2019.csv.gz,
heldout_2020_on.csv.gz and counts.json. The caller makes the held-out files
unreadable.
"""
import csv
import gzip
import io
import json
import os
import re
import sys

YEAR = re.compile(r"(\d{4})")
DEV = set("01234567")
HELD = set("89abcdef")


def main(src, out):
    os.makedirs(out, exist_ok=True)
    names = ("dev_2013_2019", "dev_2020_on", "heldout_2013_2019", "heldout_2020_on")
    files = {n: gzip.open(os.path.join(out, n + ".csv.gz"), "wt", compresslevel=3, newline="") for n in names}
    counts = {n: 0 for n in names}
    counts.update({"dropped_identifier": 0, "dropped_year": 0, "rows": 0})
    with open(src, newline="", encoding="utf-8", errors="replace") as f:
        header = f.readline()
        cols = next(csv.reader(io.StringIO(header)))
        i_taxi = cols.index("Taxi ID")
        i_start = cols.index("Trip Start Timestamp")
        for w in files.values():
            w.write(header)
        for line in f:
            counts["rows"] += 1
            row = next(csv.reader(io.StringIO(line)))
            taxi = row[i_taxi].strip().lower()
            if not taxi or (taxi[0] not in DEV and taxi[0] not in HELD):
                counts["dropped_identifier"] += 1
                continue
            m = YEAR.search(row[i_start])
            if not m or not 2013 <= int(m.group(1)) <= 2023:
                counts["dropped_year"] += 1
                continue
            name = ("dev" if taxi[0] in DEV else "heldout") + ("_2013_2019" if int(m.group(1)) <= 2019 else "_2020_on")
            files[name].write(line)
            counts[name] += 1
            if counts["rows"] % 10000000 == 0:
                print(counts, flush=True)
    for w in files.values():
        w.close()
    json.dump(counts, open(os.path.join(out, "counts.json"), "w"), indent=1)
    print("DONE", counts, flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
