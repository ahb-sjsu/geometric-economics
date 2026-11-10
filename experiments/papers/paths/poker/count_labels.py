"""Are the player labels in the HandHQ hands stable across hands?

Reads the PHH archive without extracting it and looks only at the header lines
`players`, `table`, `day` and `venue` of each hand. It reads no action, no card
and no amount, so it can be run before any poker test is designed or sealed.

    python count_labels.py poker-hand-histories-v2.zip out.json

For each site and stake folder it reports the number of hands, the number of
distinct player labels, how many hands a label appears in, and how many labels
appear on more than one day, at more than one table, and in more than one folder.
A label seen on many days at many tables is a stable identity. Labels that each
appear in one hand, or at one table only, are not.
"""
import ast
import json
import sys
import zipfile
from collections import defaultdict

import numpy as np


def main(path, out):
    days = defaultdict(set)       # label -> days seen
    tables = defaultdict(set)     # label -> tables seen (hashed to save memory)
    folders = defaultdict(set)    # label -> folders seen
    hands = defaultdict(int)      # label -> hands
    per_folder = defaultdict(lambda: {"hands": 0, "files": 0})
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if "handhq" in n.lower() and n.endswith(".phhs")]
        print("handhq files", len(names), flush=True)
        for i, name in enumerate(names):
            parts = name.split("/")
            k = [j for j, p in enumerate(parts) if p.lower() == "handhq"][0]
            folder = parts[k + 1]
            per_folder[folder]["files"] += 1
            players = table = day = None
            with z.open(name) as f:
                for raw in f:
                    line = raw.decode("utf-8", "replace")
                    if line.startswith("["):
                        players = table = day = None
                    elif line.startswith("players = "):
                        players = ast.literal_eval(line[len("players = "):].strip())
                    elif line.startswith("table = "):
                        table = hash(line[len("table = "):].strip())
                    elif line.startswith("day = "):
                        day = int(line[len("day = "):])
                    if players is not None and table is not None and day is not None:
                        per_folder[folder]["hands"] += 1
                        for p in players:
                            hands[p] += 1
                            days[p].add(day)
                            if len(tables[p]) < 50:
                                tables[p].add(table)
                            folders[p].add(folder)
                        players = table = day = None
            if i % 2000 == 0:
                print(i, len(hands), flush=True)
    n = np.array(list(hands.values()))
    res = {
        "folders": dict(per_folder),
        "hands_total": int(sum(v["hands"] for v in per_folder.values())),
        "labels": int(len(n)),
        "hands_per_label": {q: float(np.percentile(n, q)) for q in (10, 50, 90, 99)},
        "labels_in_one_hand": int((n == 1).sum()),
        "labels_on_2plus_days": int(sum(len(v) > 1 for v in days.values())),
        "labels_on_10plus_days": int(sum(len(v) >= 10 for v in days.values())),
        "labels_at_2plus_tables": int(sum(len(v) > 1 for v in tables.values())),
        "labels_in_2plus_folders": int(sum(len(v) > 1 for v in folders.values())),
        "share_of_seat_hands_from_labels_with_100plus_hands": float(n[n >= 100].sum() / n.sum()),
    }
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "folders"}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
