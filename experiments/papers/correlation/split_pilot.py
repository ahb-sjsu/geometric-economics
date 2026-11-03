#!/usr/bin/env python3
"""Split the pilot instrument's export into a readable and a sealed file (PILOT.md, "What it must not do").

    python split_pilot.py EXPORT.json OUTDIR

  readable.json      calibration trials (block R, block S at the ideal), attention checks (A) and the
                     pilot-only trials, each with its response time, and the participant record without
                     the payment details
  sealed.json        the test trials (block S off the ideal, X) and the secondary ones (XC, SC) with their
                     response times, and the payment record, which can name a sealed trial and its outcome
  id_map.json        platform identifier to p001, p002, ... Private: it bars pilot participants from the
                     main study, and it is the only output that holds platform identifiers
  split_record.json  sha256 of the export, of every output and of this script

The export is one JSON object, written by the instrument:
  {"format": "correlation-pilot-export/1", "source": "human" or "simulated", "stimuli_sha256": ...,
   "participants": [{"platform_id", "order_seed", "charity", "quiz": {"attempts", "passed"}, "finished",
                     "t_start", "t_main_end", "t_end" (epoch seconds), "debrief": {"belief",
                     "payment_rule_correct", "difficulty", "strategy"}, "payment": {"trial", "bonus",
                     "donation", "bonus_ok", "donation_ok"}, "trials": [{"id", "pos", "choice", "rt_ms"}]}]}
`choice` is the option chosen, 0 for the left one (stimuli.py shows option 0 on the left). Participants are
numbered in order of start time. None of these files enters the public repository.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stimuli  # noqa: E402

EXPORT_FORMAT = "correlation-pilot-export/1"
READABLE_FORMAT = "correlation-pilot-readable/1"
SEALED_FORMAT = "correlation-pilot-sealed/1"
READABLE_ROLES = {"calib", "check", "pilot"}
SOURCES = ("human", "simulated")
RECORD_KEYS = ("order_seed", "charity", "quiz", "finished", "t_start", "t_main_end", "t_end", "debrief")
TRIAL_KEYS = ("id", "pos", "choice", "rt_ms")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def write(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True)


def split(export_path, out_dir):
    with open(export_path) as f:
        ex = json.load(f)
    trials = stimuli.build()
    extras = stimuli.pilot_extras(trials)
    role = {t["id"]: t["role"] for t in trials + extras}
    digest = stimuli.digest(trials, extras)
    if ex.get("format") != EXPORT_FORMAT:
        raise SystemExit(f"refusing: {export_path} is not a pilot export (format {ex.get('format')!r})")
    if ex.get("source") not in SOURCES:
        raise SystemExit(f"refusing: the export must declare its source as one of {SOURCES}, not {ex.get('source')!r}")
    if ex.get("stimuli_sha256") != digest:
        raise SystemExit(f"refusing: the export's stimulus hash {ex.get('stimuli_sha256')} is not stimuli.py's {digest}")
    people = ex["participants"]
    pids = [p.get("platform_id") for p in people]
    if not all(pids) or len(set(pids)) != len(pids):
        raise SystemExit("refusing: every participant needs a platform_id, and no two the same")
    for p in people:
        ids = [t["id"] for t in p["trials"]]
        if len(set(ids)) != len(ids) or not set(ids) <= set(role):
            raise SystemExit(f"refusing: participant {p['platform_id']} has repeated or unknown trial ids")
        if any(t["choice"] not in (0, 1) for t in p["trials"]):
            raise SystemExit(f"refusing: participant {p['platform_id']} has a choice that is not 0 or 1")
        if p["finished"] and set(ids) != set(role):
            raise SystemExit(f"refusing: participant {p['platform_id']} finished but lacks {len(set(role) - set(ids))} trials")
    readable, sealed, id_map = [], [], {}
    for k, p in enumerate(sorted(people, key=lambda p: (p["t_start"], p["platform_id"])), 1):
        pid = f"p{k:03d}"
        id_map[pid] = p["platform_id"]
        pay = p.get("payment") or {}
        keep = lambda ts: [{key: t[key] for key in TRIAL_KEYS} for t in ts]  # noqa: E731
        readable.append({"pid": pid, **{key: p.get(key) for key in RECORD_KEYS},
                         "payment_ok": {"bonus": bool(pay.get("bonus_ok")), "donation": bool(pay.get("donation_ok"))},
                         "trials": keep(t for t in p["trials"] if role[t["id"]] in READABLE_ROLES)})
        sealed.append({"pid": pid, "payment": pay,
                       "trials": keep(t for t in p["trials"] if role[t["id"]] not in READABLE_ROLES)})
    os.makedirs(out_dir, exist_ok=True)
    out = {name: os.path.join(out_dir, f"{name}.json") for name in ("readable", "sealed", "id_map")}
    head = {"source": ex["source"], "stimuli_sha256": digest, "split": {"export_sha256": sha256(export_path),
                                                                       "split_pilot_sha256": sha256(__file__)}}
    write(out["readable"], {"format": READABLE_FORMAT, **head, "participants": readable})
    write(out["sealed"], {"format": SEALED_FORMAT, **head, "participants": sealed})
    write(out["id_map"], id_map)
    record = {"export_sha256": head["split"]["export_sha256"], "split_pilot_sha256": head["split"]["split_pilot_sha256"],
              "stimuli_sha256": digest, "source": ex["source"], "participants": len(people),
              "readable_trials": sum(len(p["trials"]) for p in readable),
              "sealed_trials": sum(len(p["trials"]) for p in sealed),
              **{f"{name}_sha256": sha256(path) for name, path in out.items()},
              "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    write(os.path.join(out_dir, "split_record.json"), record)
    return record


if __name__ == "__main__":
    rec = split(*sys.argv[1:3])
    print(json.dumps(rec, indent=1))
