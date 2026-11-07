#!/usr/bin/env python3
"""The instrument's saved files into the pilot export that split_pilot.py reads (PILOT.md, "Data and provenance").

    python export_pilot.py review RAW_DIR --prolific IDS.txt --out DIR [--mode pilot|main]
    python export_pilot.py export RAW_DIR --prolific IDS.txt --paid PAID.json --out EXPORT.json --source human
                                  [--exclude-problems]

RAW_DIR holds the files the instrument saved (instrument/task.js), as downloaded from the study's storage: one file
per checkpoint, each the whole session record so far. IDS.txt lists every participant ID that Prolific shows for the
study, whatever the submission's status, one per line. Files from anyone else (a test run, a stray post to the
storage) are left out and counted.

review   For each Prolific participant, the session that counts and its status (finished, quiz failed, or where it
         stopped), for approving submissions; DIR/bonuses.csv, one "<participant ID>,<dollars>" line per bonus, for
         Prolific's bulk bonus; DIR/donations.json, the total owed to each charity; DIR/review.csv; DIR/problems.json.
export   The export: one record per Prolific participant, in split_pilot.py's format, with "bonus_ok" and
         "donation_ok" from PAID.json, which the owner writes after paying (instrument/README.md, "After the
         study"): {"bonuses_csv": the bonuses file as paid, "donations": {charity: {"dollars": ..., "date": ...,
         "receipt": ...}}}. Paths in it are relative to it.

The session that counts is a participant's first: the earliest start, whatever its status. A second session in
another browser has seen the trials before, so its choices are not counted. Payment follows the first finished
session, since the participant finished it.

Every session is checked against stimuli.py: its stimulus and display hashes, its order against presentation(seed),
each trial's position and id, the paid trial and its amounts recomputed from the choice and the coin, and the
quiz against its answers. export refuses a session that fails a check unless --exclude-problems leaves it out, and
the report names it. None of these files enters the public repository.
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_instrument  # noqa: E402
import split_pilot  # noqa: E402
import stimuli  # noqa: E402

RECORD_FORMAT = "correlation-session/1"
CENTS = 5                              # per point (instrument/task.js, PARAMS.cents)
QUIZ_KEY = [0, 1, 2, 3]                # instrument/text.js, TEXT.quiz; the round trip checks the two agree
QUIZ_TRIES = 2
CHARITIES = ("American Red Cross", "Doctors Without Borders USA", "Feeding America",
             "St. Jude Children's Research Hospital", "World Wildlife Fund")     # text.js, TEXT.charities

TRIALS = stimuli.build()
EXTRAS = stimuli.pilot_extras(TRIALS)
OPTIONS = {t["id"]: t["options"] for t in TRIALS + EXTRAS}
DIGEST = stimuli.digest(TRIALS, EXTRAS)
DISPLAY = build_instrument.stimuli_doc()["display_sha256"]


def load_records(raw_dir):
    """Every session record under RAW_DIR, and the files that are not one."""
    records, foreign = [], []
    for path in sorted(glob.glob(os.path.join(raw_dir, "**", "*.json"), recursive=True)):
        try:
            with open(path, encoding="utf-8") as f:
                r = json.load(f)
        except (OSError, ValueError):
            foreign.append(os.path.relpath(path, raw_dir))
            continue
        if isinstance(r, dict) and r.get("format") == RECORD_FORMAT:
            records.append(r)
        else:
            foreign.append(os.path.relpath(path, raw_dir))
    return records, foreign


def latest(records):
    """The last checkpoint of each session, by (participant, session)."""
    out = {}
    for r in records:
        k = (r.get("platform_id"), r.get("sid"))
        if k not in out or r.get("seq", -1) > out[k].get("seq", -1):
            out[k] = r
    return out


def owed(r):
    """The paid trial's points and cents, recomputed from the record's own choice and coin, or None."""
    p = r.get("payment")
    if not p:
        return None
    k = p.get("pos")
    if not isinstance(k, int) or not 0 <= k < len(r["trials"]):
        return None
    t = r["trials"][k]
    option = OPTIONS[t["id"]][t["choice"]]
    face = {"heads": 0, "tails": 1}.get(p.get("coin"))
    if (len(option) == 2) != (face is not None):
        return None
    _, a, b = option[face or 0]
    self_pts, charity_pts = int(round(100 - a)), int(round(100 - b))
    return {"trial": t["id"], "choice": t["choice"], "self_points": self_pts, "charity_points": charity_pts,
            "bonus_cents": self_pts * CENTS, "donation_cents": charity_pts * CENTS}


def problems(r, mode):
    """What is wrong with one session's last record, as a list of sentences."""
    bad = []
    if r.get("mode") != mode:
        return [f"mode {r.get('mode')!r}, not {mode!r}"]
    if r.get("stimuli_sha256") != DIGEST:
        bad.append(f"stimulus hash {r.get('stimuli_sha256')} is not stimuli.py's {DIGEST}")
    if r.get("display_sha256") != DISPLAY:
        bad.append(f"display hash {r.get('display_sha256')} is not build_instrument.py's {DISPLAY}")
    seed = r.get("order_seed")
    expect = stimuli.presentation(seed, TRIALS, EXTRAS if mode == "pilot" else []) if isinstance(seed, int) else None
    if r.get("order") != expect:
        bad.append("order is not stimuli.presentation(order_seed)")
        expect = r.get("order") or []
    trials = r.get("trials") or []
    for k, t in enumerate(trials):
        if set(t) != set(split_pilot.TRIAL_KEYS):
            bad.append(f"trial at position {k} has fields {sorted(t)}")
            break
        if t["pos"] != k or k >= len(expect) or t["id"] != expect[k]:
            bad.append(f"trial at position {k} is id {t['id']} at pos {t['pos']}, the order says {expect[k] if k < len(expect) else None}")
            break
        if t["choice"] not in (0, 1) or not isinstance(t["rt_ms"], int) or t["rt_ms"] < 0:
            bad.append(f"trial {t['id']}: choice {t['choice']!r}, rt_ms {t['rt_ms']!r}")
            break
    q = r.get("quiz") or {}
    answers = q.get("answers") or []
    if len(answers) != q.get("attempts") or q.get("attempts", 0) > QUIZ_TRIES:
        bad.append(f"quiz: {q.get('attempts')} attempts with {len(answers)} answer sets")
    elif bool(q.get("passed")) != bool(answers and answers[-1] == QUIZ_KEY) or any(a == QUIZ_KEY for a in answers[:-1]):
        bad.append(f"quiz: passed {q.get('passed')} does not follow from the answers {answers}")
    if trials and not q.get("passed"):
        bad.append("trials without a passed quiz")
    if r.get("finished"):
        if len(trials) != len(expect):
            bad.append(f"finished with {len(trials)} of {len(expect)} trials")
        if mode == "pilot" and not r.get("debrief"):
            bad.append("finished without the debrief")
        o, p = owed(r), r.get("payment") or {}
        if o is None:
            bad.append(f"the payment {p} does not follow from a trial and its coin")
        elif any(p.get(k) != o[k] for k in ("trial", "choice", "bonus_cents", "donation_cents")):
            bad.append(f"the payment {p} is not what the paid trial gives, {o}")
        if not (r.get("t_start") and r.get("t_end") and (r.get("t_main_end") or mode == "main")):
            bad.append("finished without its times")
    elif r.get("payment"):
        bad.append("a payment without a finished session")
    if r.get("charity") is not None and r.get("charity") not in CHARITIES:
        bad.append(f"charity {r.get('charity')!r} is not on the list")
    if trials and r.get("charity") is None:
        bad.append("trials without a charity")
    return bad


def read_ids(path):
    with open(path, encoding="utf-8") as f:
        return {s.strip() for s in f if s.strip() and not s.lstrip().startswith("#")}


def sessions(raw_dir, ids_path, mode):
    """The sessions of the participants on Prolific's list, grouped by participant, earliest first, and what was
    left out."""
    records, foreign = load_records(raw_dir)
    ids = read_ids(ids_path)
    by_pid, outsiders = {}, set()
    for (pid, _), r in latest(records).items():
        if pid not in ids:
            outsiders.add(pid)
            continue
        by_pid.setdefault(pid, []).append(r)
    for rs in by_pid.values():
        rs.sort(key=lambda r: (r.get("t_start") or 0, r.get("sid") or ""))
    left = {"files_not_records": len(foreign), "participants_not_on_list": len(outsiders),
            "prolific_ids_without_data": len(ids - set(by_pid))}
    bad = {f"{r['platform_id']}/{r['sid']}": problems(r, mode) for rs in by_pid.values() for r in rs}
    return by_pid, bad, left


def status(r):
    if r.get("finished"):
        return "finished"
    if (r.get("quiz") or {}).get("attempts") == QUIZ_TRIES and not r["quiz"].get("passed"):
        return "quiz failed"
    return f"stopped at {r.get('stage')}, {len(r.get('trials') or [])} of {len(r.get('order') or [])} choices"


def paid_session(rs):
    """The first finished session, which payment follows."""
    return next((r for r in rs if r.get("finished")), None)


def review(raw_dir, ids_path, out_dir, mode="pilot"):
    by_pid, bad, left = sessions(raw_dir, ids_path, mode)
    os.makedirs(out_dir, exist_ok=True)
    rows, bonuses, donations = [], [], {}
    for pid in sorted(by_pid):
        rs = by_pid[pid]
        pay = paid_session(rs)
        for k, r in enumerate(rs):
            key = f"{pid}/{r['sid']}"
            minutes = (r["t_end"] - r["t_start"]) / 60 if r.get("t_end") and r.get("t_start") else None
            rows.append({"participant": pid, "prolific_session": r.get("prolific_session"), "sid": r["sid"],
                         "counts": "yes" if k == 0 else "no: a later session", "paid": "yes" if r is pay else "",
                         "status": status(r), "minutes": f"{minutes:.1f}" if minutes is not None else "",
                         "charity": r.get("charity") or "", "problems": "; ".join(bad[key])})
        if pay is not None and not bad[f"{pid}/{pay['sid']}"]:
            o = owed(pay)
            if o["bonus_cents"] > 0:
                bonuses.append((pid, o["bonus_cents"]))
            d = donations.setdefault(pay["charity"], {"people": 0, "cents": 0})
            d["people"] += 1
            d["cents"] += o["donation_cents"]
    with open(os.path.join(out_dir, "review.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["participant"])
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(out_dir, "bonuses.csv"), "w", newline="", encoding="utf-8") as f:
        f.write("".join(f"{pid},{c / 100:.2f}\n" for pid, c in bonuses))
    for d in donations.values():
        d["dollars"] = f"{d['cents'] / 100:.2f}"
    split_pilot.write(os.path.join(out_dir, "donations.json"), donations)
    split_pilot.write(os.path.join(out_dir, "problems.json"), {k: v for k, v in bad.items() if v})
    summary = {"participants": len(by_pid), "sessions": len(rows), "finished": sum(r["status"] == "finished" for r in rows),
               "bonuses": len(bonuses), "bonus_dollars": f"{sum(c for _, c in bonuses) / 100:.2f}",
               "donation_dollars": {k: v["dollars"] for k, v in donations.items()},
               "sessions_with_problems": sum(bool(v) for v in bad.values()), **left}
    split_pilot.write(os.path.join(out_dir, "review_summary.json"), summary)
    return summary


def read_paid(path):
    with open(path, encoding="utf-8") as f:
        paid = json.load(f)
    base = os.path.dirname(os.path.abspath(path))
    bonus = {}
    with open(os.path.join(base, paid["bonuses_csv"]), encoding="utf-8") as f:
        for line in f:
            if line.strip():
                pid, amount = line.strip().split(",")
                bonus[pid] = bonus.get(pid, 0) + int(round(float(amount) * 100))
    donated = {name: int(round(float(d["dollars"]) * 100)) for name, d in (paid.get("donations") or {}).items()}
    return bonus, donated


def export(raw_dir, ids_path, paid_path, out, source, exclude_problems=False):
    if source not in split_pilot.SOURCES:
        raise SystemExit(f"refusing: the source must be one of {split_pilot.SOURCES}, not {source!r}")
    by_pid, bad, left = sessions(raw_dir, ids_path, "pilot")
    failing = {pid: v for pid, v in bad.items() if v}
    first_bad = {pid for pid, rs in by_pid.items() if bad[f"{pid}/{rs[0]['sid']}"]}
    if failing and not exclude_problems:
        raise SystemExit(f"refusing: {len(failing)} session(s) fail a check, among them {sorted(failing)[:3]}; "
                         f"see `review`, and pass --exclude-problems to leave them out")
    bonus_paid, donated = read_paid(paid_path)
    owed_charity = {}
    for pid, rs in by_pid.items():
        pay = paid_session(rs)
        if pay is not None and not bad[f"{pid}/{pay['sid']}"]:
            owed_charity[pay["charity"]] = owed_charity.get(pay["charity"], 0) + owed(pay)["donation_cents"]
    people = []
    for pid, rs in by_pid.items():
        if pid in first_bad:
            continue
        r = rs[0]
        pay = paid_session(rs)
        o = owed(pay) if pay is not None and not bad[f"{pid}/{pay['sid']}"] else None
        payment = {"trial": None, "bonus": 0.0, "donation": 0.0, "bonus_ok": True, "donation_ok": True}
        if o is not None:
            payment = {"trial": o["trial"] if pay is r else None, "bonus": o["bonus_cents"] / 100,
                       "donation": o["donation_cents"] / 100,
                       "bonus_ok": bonus_paid.get(pid, 0) == o["bonus_cents"],
                       "donation_ok": donated.get(pay["charity"], 0) >= owed_charity[pay["charity"]]}
        d = r.get("debrief")
        people.append({"platform_id": pid, "order_seed": r["order_seed"], "charity": r.get("charity"),
                       "quiz": {"attempts": r["quiz"]["attempts"], "passed": bool(r["quiz"]["passed"])},
                       "finished": bool(r.get("finished")), "t_start": r.get("t_start"),
                       "t_main_end": r.get("t_main_end"), "t_end": r.get("t_end") if r.get("finished") else None,
                       "debrief": {k: d[k] for k in ("belief", "payment_rule_correct", "difficulty", "strategy")} if d else None,
                       "payment": payment,
                       "trials": [{k: t[k] for k in split_pilot.TRIAL_KEYS} for t in r["trials"]]})
    people.sort(key=lambda p: (p["t_start"] or 0, p["platform_id"]))
    doc = {"format": split_pilot.EXPORT_FORMAT, "source": source, "stimuli_sha256": DIGEST, "participants": people}
    split_pilot.write(out, doc)
    report = {"export_sha256": split_pilot.sha256(out), "participants": len(people),
              "excluded_with_problems": sorted(failing), "later_sessions_not_counted":
              sum(len(rs) - 1 for rs in by_pid.values()), **left,
              "export_pilot_sha256": split_pilot.sha256(os.path.abspath(__file__))}
    split_pilot.write(os.path.splitext(out)[0] + ".report.json", report)
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("review")
    a.add_argument("raw")
    a.add_argument("--prolific", required=True)
    a.add_argument("--out", required=True)
    a.add_argument("--mode", choices=("pilot", "main"), default="pilot")
    a = sub.add_parser("export")
    a.add_argument("raw")
    a.add_argument("--prolific", required=True)
    a.add_argument("--paid", required=True)
    a.add_argument("--out", required=True)
    a.add_argument("--source", required=True, choices=split_pilot.SOURCES)
    a.add_argument("--exclude-problems", action="store_true")
    args = ap.parse_args()
    if args.cmd == "review":
        print(json.dumps(review(args.raw, args.prolific, args.out, args.mode), indent=1))
    else:
        print(json.dumps(export(args.raw, args.prolific, args.paid, args.out, args.source, args.exclude_problems),
                         indent=1))


if __name__ == "__main__":
    main()
