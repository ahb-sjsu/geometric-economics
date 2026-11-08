#!/usr/bin/env python3
"""The main study's analysis (DESIGN.md, "Analysis"; MAIN.md): who counts, the fits, and every registered test.

    python main_analysis.py export RAW_DIR --prolific IDS.txt --pilot-ids PILOT_ID_MAP.json --out DIR --source human
                                   [--exclude-problems]
    python main_analysis.py grade DIR/main_data.json --out OUT_DIR [--record SEAL.sha256]
    python main_analysis.py self-test DIR [--hier]
    python main_analysis.py rehearse TRUTH STUDIES OUT.json [--n 120] [--seed 0]
    python main_analysis.py summarise OUT.json REHEARSE.json...

export     The files the instrument saved in the main study's mode (instrument/config.js, mode "main"), as downloaded
           from the storage, into DIR/main_data.json: one record per participant on Prolific's list, their first
           session only, as export_pilot.py counts it, numbered m0001 on in order of start time. Pilot participants,
           whose Prolific IDs are in the pilot's id_map.json, are left out, since the pilot bars them (PILOT.md).
           DIR/main_id_map.json is the only output with Prolific IDs, and DIR/main_problems.json names the sessions that
           fail a check. DIR/export_record.json holds the hashes and the counts, among them how many qualify so far,
           which says when recruitment can stop. Only the record may enter the public repository.
grade      Who counts, the fits and the tests: OUT_DIR/main_results.json (aggregates) and OUT_DIR/main_people.json (a
           row per person; private). Human data are graded only at the n that the seal of sequence step 10 records
           (seal_main.py), only while that seal and the design's are intact, and only by the main_analysis.py it names.
           Simulated data take --n and write rehearsal_main_results.json and rehearsal_main_people.json instead.
self-test  Simulated sessions through export and grade: every choice where the simulation put it, the people counted
           and every number equal to a second computation from the simulation itself, the planted cases, two controls
           that must fail, and every guard driven to refuse for its own reason. Writes DIR/main_selftest.json.
rehearse   Simulated main studies of one truth through the saved files, export and grade, without hier.py: how often
           the claim and the secondary claim pass (MAIN.md, "The rehearsal").
summarise  The rehearsal's runs into one record, with the bars MAIN.md set before they ran.

Who counts (DESIGN.md, "Inclusion"; PILOT.md, "Participants and instrument"): finished the session, passed the quiz
within two tries, chose the dominated option in at most 2 of the 8 attention checks (pilot_analysis.person), and not
flagged as self only (rehearsal.flagged: the self-favouring option in at least 15 of block R's 20 pairs at ratios 2
and 3). The registered tests count the first n of them in order of start time, as the rehearsal counted the first n
unflagged people it recruited. Flagged people and anyone qualifying after the first n enter no registered test: the
flagged are reported apart, by the model-free statistics, and the rest are counted.

The fits are rehearsal.main's, unchanged (DESIGN.md, "Fitting"; models.py). Every model is fitted to each person's
calibration trials with fixed weak priors, then again with an empirical-Bayes prior, the median and MAD of the first
pass over the first PRIOR_N people included, flagged or not, as rehearsal.main took them from the first ns[0] people
it recruited. The tests are rehearsal.evaluate and rehearsal.tests themselves: H1 to H3 at the registered margin and
their conjunction, the claim; H4; MF1 and MF2; SH1 and SH2 and their conjunction, the secondary claim; SH1r and SH3,
reported. The population kappa is hier.py's, on the people counted. Each person's fits draw their random second start
from their own stream, numbered by their place in the export, so a person's fits do not depend on anyone else's.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
import zlib

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import export_pilot  # noqa: E402
import models as M  # noqa: E402
import pilot_analysis as PA  # noqa: E402
import rehearsal as R  # noqa: E402
import split_pilot  # noqa: E402
import stimuli  # noqa: E402

DATA_FORMAT = "correlation-main-data/1"
RECORD_FORMAT = "correlation-main-export-record/1"
RESULTS_FORMAT = "correlation-main-results/1"
SELFTEST_FORMAT = "correlation-main-self-test/1"
REHEARSE_FORMAT = "correlation-main-rehearsal/1"
MODE = "main"                        # instrument/config.js: 140 trials, no debrief
MARGIN = 0.005                       # DESIGN.md: nats per trial, set by the owner on 2026-11-02
J = R.MARGINS.index(MARGIN)          # rehearsal.tests records a pass at each of R.MARGINS
PRIOR_N = R.NS[0]                    # rehearsal.main: the empirical-Bayes prior from the first ns[0] people, 60
FIT_STREAM = 20                      # each person's fits: np.random.default_rng([SEED, FIT_STREAM, number])
SIM_STREAM = 21                      # the simulated sessions of the self-test and the rehearsal
POPULATION = PA.MAIN_POPULATION      # "unflagged", the owner's decision of 2026-11-04
SEAL_MAIN = os.path.join(HERE, "prereg-correlation-v1-main.sha256")
TRIALS = R.TRIALS                    # the main set, 140 trials; the main study shows no pilot-only trial
N_MAIN = len(TRIALS)
MAIN_IDS = frozenset(range(N_MAIN))
TOP_KEYS = {"format", "source", "stimuli_sha256", "export", "participants"}
PERSON_KEYS = {"pid", "order_seed", "charity", "quiz", "finished", "t_start", "t_main_end", "t_end", "trials"}
TRIAL_KEYS = frozenset(split_pilot.TRIAL_KEYS)
# the code a run depends on, hashed with CRLF normalized to LF as the seals hash it
CODE = ("main_analysis.py", "rehearsal.py", "models.py", "stimuli.py", "hier.py", "pilot_analysis.py",
        "export_pilot.py", "split_pilot.py", "build_instrument.py", "seal_main.py", "seal_correlation.py")
Refusal = PA.Refusal


def lf_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read().replace(b"\r\n", b"\n")).hexdigest()


def code_hashes():
    return {name: lf_sha256(os.path.join(HERE, name)) for name in CODE}


def coded(ch):
    """rehearsal.py's coding of one person's choices: 1 where the left option, option 0, was chosen. `ch` holds the
    option chosen on each trial id, as the instrument records it."""
    return (1 - np.asarray(ch[:N_MAIN])).astype(float)


def flagged(y):
    """The main study's self-only flag, rehearsal.flagged (DESIGN.md, Inclusion)."""
    return R.flagged(y)


# ---- export ---------------------------------------------------------------------------------------------------

def export(raw_dir, ids_path, pilot_ids_path, out_dir, source, exclude_problems=False):
    if source not in split_pilot.SOURCES:
        raise Refusal("provenance", f"the source must be one of {split_pilot.SOURCES}, not {source!r}")
    if pilot_ids_path:
        barred = set(PA.load(pilot_ids_path).values())   # the pilot's id_map.json: p001 -> Prolific ID
    elif source == "human":
        raise Refusal("pilot", "a human export needs the pilot's id_map.json (--pilot-ids): pilot participants are "
                               "barred from the main study (PILOT.md, \"What it must not do\")")
    else:
        barred = set()
    by_pid, bad, left = export_pilot.sessions(raw_dir, ids_path, MODE)
    pilot_people = sorted(set(by_pid) & barred)
    for pid in pilot_people:
        del by_pid[pid]
    failing = {key: v for key, v in bad.items() if v and key.split("/")[0] in by_pid}
    first_bad = {pid for pid, rs in by_pid.items() if bad[f"{pid}/{rs[0]['sid']}"]}
    if failing and not exclude_problems:
        raise Refusal("problems", f"{len(failing)} session(s) fail a check (export_pilot.problems); see "
                                  f"`export_pilot.py review --mode main`, and pass --exclude-problems to leave them out")
    people = []
    for pid, rs in by_pid.items():
        if pid in first_bad:
            continue
        r = rs[0]
        people.append({"platform_id": pid, "order_seed": r["order_seed"], "charity": r.get("charity"),
                       "quiz": {"attempts": r["quiz"]["attempts"], "passed": bool(r["quiz"]["passed"])},
                       "finished": bool(r.get("finished")), "t_start": r.get("t_start"),
                       "t_main_end": r.get("t_main_end"), "t_end": r.get("t_end") if r.get("finished") else None,
                       "trials": [{k: t[k] for k in split_pilot.TRIAL_KEYS} for t in r["trials"]]})
    people.sort(key=lambda p: (p["t_start"] or 0, p["platform_id"]))
    id_map = {}
    for k, p in enumerate(people, 1):
        id_map[f"m{k:04d}"] = p.pop("platform_id")
        p["pid"] = f"m{k:04d}"
    os.makedirs(out_dir, exist_ok=True)
    paths = {name: os.path.join(out_dir, f"{name}.json") for name in ("main_data", "main_id_map", "main_problems")}
    doc = {"format": DATA_FORMAT, "source": source, "stimuli_sha256": export_pilot.DIGEST,
           "export": {"pilot_id_map_sha256": split_pilot.sha256(pilot_ids_path) if pilot_ids_path else None,
                      "left_out": {**left, "pilot_participants": len(pilot_people),
                                   "later_sessions_not_counted": sum(len(rs) - 1 for rs in by_pid.values()),
                                   "excluded_with_problems": len(first_bad)}},
           "participants": [{key: p[key] for key in ("pid", *sorted(PERSON_KEYS - {"pid"}))} for p in people]}
    split_pilot.write(paths["main_data"], doc)
    split_pilot.write(paths["main_id_map"], id_map)
    split_pilot.write(paths["main_problems"], failing)
    w = who_counts(doc["participants"])
    record = {"format": RECORD_FORMAT, "source": source,
              **{f"{name}_sha256": split_pilot.sha256(path) for name, path in paths.items()},
              "pilot_id_map_sha256": doc["export"]["pilot_id_map_sha256"], "code_sha256": code_hashes(),
              "counts": counts(doc["participants"], w), "left_out": doc["export"]["left_out"],
              "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    split_pilot.write(os.path.join(out_dir, "export_record.json"), record)
    return record


# ---- who counts -----------------------------------------------------------------------------------------------

def load_data(path):
    doc = PA.load(path)
    if doc.get("format") != DATA_FORMAT:
        raise Refusal("format", f"{path} is not the main study's data (format {doc.get('format')!r}); run export first")
    if doc.get("source") not in split_pilot.SOURCES:
        raise Refusal("provenance", f"{path} does not declare its source as human or simulated ({doc.get('source')!r})")
    if doc.get("stimuli_sha256") != export_pilot.DIGEST:
        raise Refusal("hash", f"{path} names stimulus hash {doc.get('stimuli_sha256')}, not stimuli.py's {export_pilot.DIGEST}")
    if set(doc) - TOP_KEYS:
        raise Refusal("field", f"{path} has fields the main study's data do not have: {sorted(set(doc) - TOP_KEYS)}")
    people = doc["participants"]
    if [p.get("pid") for p in people] != [f"m{k:04d}" for k in range(1, len(people) + 1)]:
        raise Refusal("format", f"{path}: participants are not numbered m0001 on in the export's order")
    for p in people:
        if set(p) != PERSON_KEYS:
            raise Refusal("field", f"participant {p.get('pid')} has fields {sorted(set(p) ^ PERSON_KEYS)} beyond or short "
                                   f"of the main study's")
        seen = set()
        for t in p["trials"]:
            if set(t) != TRIAL_KEYS:
                raise Refusal("field", f"participant {p['pid']}, trial {t.get('id')}: fields {sorted(t)}")
            if t["id"] not in MAIN_IDS or t["id"] in seen or t["choice"] not in (0, 1):
                raise Refusal("format", f"participant {p['pid']}: trial {t['id']} is repeated, has an invalid choice, or "
                                        f"is not one of the main set's {N_MAIN} (the main study shows no pilot-only trial)")
            seen.add(t["id"])
        if p["finished"] and seen != MAIN_IDS:
            raise Refusal("format", f"participant {p['pid']} finished with {len(seen)} of the {N_MAIN} trials")
    return doc


def who_counts(people):
    """DESIGN.md, "Inclusion", over the export's people in its order, which is the order of start time. Returns the
    pids passing each step, in that order, and each finished person's choices in rehearsal.py's coding."""
    quiz_ok = [p for p in people if p["quiz"]["passed"] and p["quiz"]["attempts"] <= export_pilot.QUIZ_TRIES]
    finished = [p for p in quiz_ok if p["finished"]]
    ch = {p["pid"]: PA.choices(p) for p in finished}
    y = {pid: coded(c) for pid, c in ch.items()}
    att = {pid: PA.person(c)["att_fail"] for pid, c in ch.items()}
    included = [p["pid"] for p in finished if att[p["pid"]] <= PA.ATT_MAX]
    flag = {pid: flagged(y[pid]) for pid in included}
    return {"quiz_ok": [p["pid"] for p in quiz_ok], "finished": [p["pid"] for p in finished], "included": included,
            "flagged": [pid for pid in included if flag[pid]], "unflagged": [pid for pid in included if not flag[pid]],
            "att_fail": att, "y": y}


def counts(people, w):
    return {"participants": len(people), "quiz_passed": len(w["quiz_ok"]), "finished": len(w["finished"]),
            "included": len(w["included"]), "flagged": len(w["flagged"]), "unflagged": len(w["unflagged"]),
            "qualify": len(w["unflagged"])}


# ---- the fits and the tests -----------------------------------------------------------------------------------

def number(pid):
    return int(pid[1:])


def first_pass(pid, y):
    rng = np.random.default_rng([R.SEED, FIT_STREAM, number(pid)])
    d, yc = R.SUB["calib"], y[R.IDX["calib"]]
    return {k: M.fit(M.MODELS[k], d, yc, rng) for k in R.FIT}


def second_pass(pid, y, f1, priors):
    # one start from the first pass's estimate, so the random stream is not drawn (models.fit)
    rng = np.random.default_rng([R.SEED, FIT_STREAM, number(pid), 2])
    d, yc = R.SUB["calib"], y[R.IDX["calib"]]
    return {k: M.fit(M.MODELS[k], d, yc, rng, starts=1, prior=priors[k], x0=f1[k]) for k in R.FIT}


def fit_all(y, prior_pids, counted):
    """rehearsal.main's two passes: the first for the prior's people and the people counted, the empirical-Bayes prior
    from the prior's people, the second for the people counted."""
    f1 = {pid: first_pass(pid, y[pid]) for pid in dict.fromkeys(prior_pids + counted)}
    priors = {k: M.eb_prior(M.MODELS[k], [f1[pid][k] for pid in prior_pids]) for k in R.FIT}
    f2 = {pid: second_pass(pid, y[pid], f1[pid], priors) for pid in counted}
    return f1, priors, f2


def hier_kappa(Y):
    import hier  # noqa: PLC0415  (jax is needed only here)
    return {**hier.fit(R.SUB["calib"], Y, seed=0), "fit": "hier.py", "people": int(Y.shape[0])}


def no_hier(Y):
    return {"kappa_median": None, "lo": None, "hi": None, "fit": "skipped (simulated data only)", "people": int(Y.shape[0])}


def model_free(ys):
    """MF1's and MF2's per-person statistics (rehearsal.evaluate's obs_corr and bg) over a group, with their interval
    over people, for people no model is fitted to."""
    if len(ys) < 2:
        return {"people": len(ys)}
    obs = [float(np.where(R.CORR == 0, y[R.IDX["X"]], 1 - y[R.IDX["X"]]).mean() - 0.5) for y in ys]
    bg = [0.5 * (R.lottery_rates(y, "self", 0) + R.lottery_rates(y, "charity", 0)) for y in ys]
    return {"people": len(ys), **{name: dict(zip(("est", "lo", "hi"), R.ci(v))) for name, v in (("MF1", obs), ("MF2", bg))}}


def load_record(path):
    """The seal of sequence step 10 (seal_main.py): refuses unless it exists, names this main_analysis.py, and it and
    the design's seal are intact."""
    if not os.path.exists(path):
        raise Refusal("missing", f"no seal of sequence step 10 at {path}: human data are graded only after that seal records "
                                 f"n and this script (PILOT.md, step 10; MAIN.md)")
    import seal_main  # noqa: PLC0415
    rec = PA.load(path)
    state = seal_main.verify_record(rec)
    if state["files"].get("main_analysis.py") is not True:
        raise Refusal("runner", f"the seal {os.path.basename(path)} does not name this main_analysis.py "
                                f"({lf_sha256(os.path.join(HERE, 'main_analysis.py'))[:16]})")
    if not state["intact"]:
        raise Refusal("seal", f"the seal {os.path.basename(path)} or the design's is broken: {state['broken']}")
    if rec.get("n") not in PA.MAIN_NS:
        raise Refusal("n", f"the seal {os.path.basename(path)} records n = {rec.get('n')!r}, not one of {PA.MAIN_NS}")
    return rec


def grade(data_path, out_dir, record_path=None, n=None, kappa_fit=None):
    doc = load_data(data_path)
    human = doc["source"] == "human"
    rec = None
    if human:
        if n is not None:
            raise Refusal("n", "human data are graded at the n the seal of step 10 records, never at one given by hand")
        if not doc["export"].get("pilot_id_map_sha256"):
            raise Refusal("pilot", f"{data_path} was exported without the pilot's id_map.json, so pilot participants "
                                   f"were not left out")
        rec = load_record(record_path or SEAL_MAIN)
        n = rec["n"]
        kappa_fit = kappa_fit or hier_kappa
    elif n is None:
        raise Refusal("n", "simulated data are graded at an n given by hand (--n)")
    kappa_fit = kappa_fit or no_hier
    people = doc["participants"]
    w = who_counts(people)
    if len(w["unflagged"]) < n:
        raise Refusal("short", f"{len(w['unflagged'])} people qualify, fewer than n = {n}: recruitment continues until n "
                               f"qualify (DESIGN.md, Inclusion)")
    counted = w["unflagged"][:n]
    prior_pids = w["included"][:PRIOR_N]
    y = w["y"]
    t0 = time.time()
    f1, priors, f2 = fit_all(y, prior_pids, counted)
    ps = [R.evaluate({"y": y[pid], "pl": y[pid], "shape": {}}, f2[pid], f1[pid]) for pid in counted]
    res = R.tests(ps)
    kappa = kappa_fit(np.stack([y[pid][R.IDX["calib"]] for pid in counted]))
    seconds = time.time() - t0
    by_pid = {p["pid"]: p for p in people}

    hyp = {}
    for name, k in (("H1", "EARLY"), ("H2", "RDU"), ("H3", "CAG")):
        h = res[f"H_vs_{k}"]
        hyp[name] = {"against": k, "est": h["est"], "lo": h["lo"], "hi": h["hi"], "pass": h["pass"][J],
                     "pass_by_margin": dict(zip(map(str, R.MARGINS), h["pass"])), "est_S": h["est_S"], "est_X": h["est_X"]}
    claim = all(h["pass"] for h in hyp.values())
    sec = res["secondary"]
    secondary = {"pass": bool(sec["SH1_IA_beats_GEO"]["pass"] and sec["SH2_straddle_beyond_GEO"]["pass"]),
                 "SH1": sec["SH1_IA_beats_GEO"], "SH2": sec["SH2_straddle_beyond_GEO"],
                 "reported": {k: sec[k] for k in ("SH1r_GEO_beats_IA", "SH3_equal_splits_beyond_GEO", "SH3_did",
                                                  "straddle_raw")}}
    mf = {"MF1": res["MF1"], "MF2": res["MF2"], "both_null": not (res["MF1"]["pass"] or res["MF2"]["pass"])}
    kap = {k: v for k, v in kappa.items() if k != "draws"}
    if kappa.get("lo") is not None:
        kap.update(interval_excludes_1=bool(kappa["lo"] > 1 or kappa["hi"] < 1),
                   interval_excludes_2=bool(kappa["lo"] > 2 or kappa["hi"] < 2), draws=kappa.get("draws"))
    # the readings DESIGN.md registers for these outcomes, quoted when their condition holds
    readings = []
    if mf["both_null"]:
        readings.append("DESIGN.md, model-free checks: both are null, so additive value wins and the metric is not "
                        "detected for these attributes.")
    if not claim and kap.get("interval_excludes_1"):
        readings.append("DESIGN.md, the population kappa: a null on the claim with the interval excluding 1 means cost "
                        "is not distance-like, and the design had little power.")
    if not claim and kap.get("interval_excludes_2"):
        readings.append("DESIGN.md, the population kappa: a null on the claim with the interval excluding 2 counts "
                        "against the metric.")
    beyond = w["unflagged"][n:]
    minutes = [(by_pid[pid]["t_main_end"] - by_pid[pid]["t_start"]) / 60 for pid in counted
               if by_pid[pid]["t_main_end"] and by_pid[pid]["t_start"]]
    rts = [t["rt_ms"] for pid in counted for t in by_pid[pid]["trials"]]
    charities = {}
    for pid in counted:
        charities[by_pid[pid]["charity"]] = charities.get(by_pid[pid]["charity"], 0) + 1
    out = {"format": RESULTS_FORMAT, "source": doc["source"],
           "inputs": {"data_sha256": split_pilot.sha256(data_path), "stimuli_sha256": export_pilot.DIGEST,
                      "code_sha256": code_hashes(), "export": doc["export"],
                      "record": None if rec is None else {"prereg": rec["prereg"], "file": os.path.basename(record_path or SEAL_MAIN),
                                                          "sha256": split_pilot.sha256(record_path or SEAL_MAIN),
                                                          "combined_sha256": rec["combined_sha256"], "n": rec["n"]}},
           "n": n, "population": POPULATION, "margin": MARGIN,
           "counts": {**counts(people, w), "counted": len(counted), "unflagged_beyond_n": len(beyond),
                      "prior_people": len(prior_pids), "prior_flagged": len(set(prior_pids) & set(w["flagged"]))},
           "model_free": mf,
           "claim": {"pass": claim, **hyp},
           "H4": res["H4"],
           "population_kappa": {**kap, "note": "DESIGN.md: it means something only if GEO is the right model"},
           "secondary": secondary,
           "readings": readings,
           "mean_ll": res["mean_ll"], "mean_ll_pass1": res["mean_ll_pass1"],
           "priors": {k: {"median": [float(x) for x in mu], "sd": [float(x) for x in sd]} for k, (mu, sd) in priors.items()},
           "reported_apart": {"flagged": model_free([y[pid] for pid in w["flagged"]]),
                              "unflagged_beyond_n": len(beyond)},
           "descriptives": {"main_minutes_median": float(np.median(minutes)) if minutes else None,
                            "choices_under_1s": float(np.mean(np.array(rts) < 1000)) if rts else None,
                            "left_rate": float(np.mean([y[pid].mean() for pid in counted])),
                            "charities": dict(sorted(charities.items(), key=lambda kv: str(kv[0])))},
           "seconds": seconds, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    rows = [{"pid": pid, "att_fail": w["att_fail"][pid], "fit1": {k: [float(x) for x in v] for k, v in f1[pid].items()},
             "fit2": {k: [float(x) for x in v] for k, v in f2[pid].items()},
             **{k: v for k, v in p.items() if k not in ("true_corr", "rank_one")}} for pid, p in zip(counted, ps)]
    rows += [{"pid": pid, "flagged": True, "att_fail": w["att_fail"][pid]} for pid in w["flagged"]]
    os.makedirs(out_dir, exist_ok=True)
    stem = "main" if human else "rehearsal_main"
    paths = (os.path.join(out_dir, f"{stem}_results.json"), os.path.join(out_dir, f"{stem}_people.json"))
    PA.dump(out, paths[0])
    PA.dump({"format": RESULTS_FORMAT + "/people", "source": doc["source"], "people": rows}, paths[1])
    return out, paths[0]


# ---- simulated sessions ---------------------------------------------------------------------------------------

BUILD = PA.load(os.path.join(HERE, "instrument", "MANIFEST.json"))["build"]


def session(pid, ch, rng, t_start, *, k=None, answers=None, sid=None, seq=11, mode=MODE):
    """One session as instrument/task.js saves it at a checkpoint (the fields of the round trip's main-mode records),
    choosing ch[i] on trial i. k: the choices made so far (all of them, by default, and the session finished);
    answers: the quiz's tries (one right one by default)."""
    seed = int(rng.integers(2 ** 31))
    order = stimuli.presentation(seed, TRIALS, [])
    answers = [list(export_pilot.QUIZ_KEY)] if answers is None else answers
    passed = answers[-1] == export_pilot.QUIZ_KEY
    k = (len(order) if k is None else k) if passed else 0
    finished = passed and k == len(order)
    rt = np.exp(rng.normal(np.log(3500.0), 0.5, len(order))).astype(int)
    t_main = t_start + 240.0 + float(rt[:k].sum()) / 1000
    r = {"format": export_pilot.RECORD_FORMAT, "build": BUILD, "mode": mode, "platform_id": pid, "study_id": "SIMSTUDY",
         "prolific_session": f"SIM{int(rng.integers(16 ** 6)):06x}",
         "sid": sid or f"{int(rng.integers(16 ** 8)):08x}{int(rng.integers(16 ** 8)):08x}",
         "stimuli_sha256": export_pilot.DIGEST, "display_sha256": export_pilot.DISPLAY, "order_seed": seed,
         "order": order, "t_start": t_start, "t_main_end": t_main if finished else None,
         "t_end": t_main + 0.5 if finished else None,
         "stage": "payment" if finished else ("trials" if passed else "quiz_failed"),
         "charity": export_pilot.CHARITIES[int(rng.integers(len(export_pilot.CHARITIES)))],
         "quiz": {"attempts": len(answers), "passed": passed, "answers": answers}, "debrief": None, "payment": None,
         "finished": finished, "seq": seq, "reloads": 0, "hidden": 0, "save_errors": [], "viewport": [1280, 800],
         "kind": "final" if finished else "checkpoint", "saved_utc": "2026-11-07T00:00:00.000Z",
         "trials": [{"id": int(i), "pos": pos, "choice": int(ch[i]), "rt_ms": int(rt[pos])} for pos, i in enumerate(order[:k])]}
    if finished:
        pos = int(rng.integers(len(order)))
        t, c = order[pos], int(ch[order[pos]])
        option = export_pilot.OPTIONS[t][c]
        coin = ("heads", "tails")[int(rng.integers(2))] if len(option) == 2 else None
        _, a, b = option[{"heads": 0, "tails": 1}.get(coin, 0)]
        sp, cp = int(round(100 - a)), int(round(100 - b))
        r["payment"] = {"trial": int(t), "pos": pos, "choice": c, "coin": coin, "self_points": sp, "charity_points": cp,
                        "bonus_cents": sp * export_pilot.CENTS, "donation_cents": cp * export_pilot.CENTS,
                        "bonus": sp * export_pilot.CENTS / 100, "donation": cp * export_pilot.CENTS / 100}
    return r


def checkpoint(r, k, seq):
    """An earlier checkpoint of the same session: its first k choices, before it finished."""
    c = json.loads(json.dumps(r))
    c.update(trials=c["trials"][:k], finished=False, payment=None, t_main_end=None, t_end=None, stage="trials",
             kind="checkpoint", seq=seq)
    return c


def save(raw_dir, r):
    os.makedirs(raw_dir, exist_ok=True)
    split_pilot.write(os.path.join(raw_dir, f"{r['platform_id']}_{r['sid']}_{r['seq']:03d}.json"), r)


def prolific_id(rng):
    return f"{int(rng.integers(16 ** 12)):012x}{int(rng.integers(16 ** 12)):012x}"


def simulated_study(truth, rng, n, raw_dir, beyond=2):
    """Simulated people from a truth (rehearsal.simulate, main set only) through saved session files, recruited until
    n + beyond qualify by the simulation's own reckoning. Returns each person's truth, in order of start."""
    good = {t["id"]: t["good_option"] for t in TRIALS if t["block"] == "A"}
    hi = {t["id"]: stimuli.self_option(t) for t in TRIALS if t["cell"] in ("R_ratio2", "R_ratio3")}
    people, qualify, t = [], 0, 1.8e9
    while qualify < n + beyond:
        sim = R.simulate(truth, rng)
        ch = (1 - sim["y"]).astype(int)
        pid, t = prolific_id(rng), t + float(rng.uniform(30, 300))
        r = session(pid, ch, rng, t)
        save(raw_dir, r)
        att = sum(ch[i] != g for i, g in good.items())
        flag = sum(ch[i] == s for i, s in hi.items()) >= R.MAIN_FLAG_MIN
        people.append({"platform_id": pid, "t_start": t, "ch": ch, "included": att <= PA.ATT_MAX, "flagged": flag,
                       "rank_one": bool(sim["shape"].get("rank_one")), "record": r})
        qualify += att <= PA.ATT_MAX and not flag
    return people


# ---- the self-test --------------------------------------------------------------------------------------------

def self_test(d, use_hier=False, truth="G100T15S30", n=120):
    """Simulated sessions (MAIN.md, "The self-test")."""
    global coded, flagged      # the two controls below swap these for broken versions, then put them back
    os.makedirs(d, exist_ok=True)
    t_begin = time.time()
    stub = lambda Y: {"kappa_median": 1.0, "lo": 0.8, "hi": 1.2, "fit": "stub (self-test)", "people": int(Y.shape[0])}  # noqa: E731
    kfit = hier_kappa if use_hier else stub
    results = []

    def check(name, ok, detail=""):
        results.append({"check": name, "pass": bool(ok), "detail": detail})
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}", flush=True)

    def refused(name, kind, fn):
        try:
            fn()
        except Refusal as e:
            check(name, e.kind == kind, f"refused ({e.kind}): {e}")
            return
        check(name, False, "did not refuse")

    rng = np.random.default_rng([R.SEED, SIM_STREAM, 0])
    raw, ids, pilot_ids = os.path.join(d, "raw"), os.path.join(d, "prolific_ids.txt"), os.path.join(d, "pilot_id_map.json")
    for sub in ("raw", "export", "grade"):
        shutil.rmtree(os.path.join(d, sub), ignore_errors=True)
    sims = simulated_study(truth, rng, n, raw)
    # Planted people, each starting among the first 60, where the prior's people come from. They choose as the first
    # simulated person after the first who qualifies by the attention checks.
    t0 = sims[0]["t_start"]
    base = next(p for p in sims[1:] if p["included"])
    any_ch = base["ch"].copy()

    def plant(name, offset, **kw):
        pid = prolific_id(rng)
        r = session(pid, any_ch, rng, t0 + offset, **kw)
        save(raw, r)
        return {"name": name, "platform_id": pid, "record": r}

    att_ch = any_ch.copy()
    for i in [t["id"] for t in TRIALS if t["block"] == "A"][:3]:
        att_ch[i] = 1 - TRIALS[i]["good_option"]
    planted = [plant("quiz failed twice", 11.0, answers=[[0, 1, 2, 0], [1, 1, 2, 3]]),
               plant("quiz passed at the second try", 12.0, answers=[[0, 0, 2, 3], list(export_pilot.QUIZ_KEY)]),
               plant("stopped after 70 choices", 13.0, k=70, seq=5)]
    pid = prolific_id(rng)
    r = session(pid, att_ch, rng, t0 + 14.0)
    save(raw, r)
    planted.append({"name": "three attention checks failed", "platform_id": pid, "record": r})
    pid = prolific_id(rng)
    first, again = session(pid, any_ch, rng, t0 + 15.0, k=40, seq=3), session(pid, any_ch, rng, t0 + 900.0)
    save(raw, first)
    save(raw, again)
    planted.append({"name": "a first session stopped, a second finished", "platform_id": pid, "record": first})
    planted.append(plant("a pilot participant", 16.0))
    planted.append(plant("not on Prolific's list", 17.0))
    split_pilot.write(os.path.join(raw, "notes.json"), {"note": "not a session record"})
    # an earlier checkpoint of a simulated person's session, which its last one replaces
    save(raw, checkpoint(sims[2]["record"], 20, 2))
    by_name = {p["name"]: p for p in planted}
    listed = [p["platform_id"] for p in sims] + [p["platform_id"] for p in planted if p["name"] != "not on Prolific's list"]
    with open(ids, "w") as f:
        f.write("".join(pid + "\n" for pid in listed + [prolific_id(rng)]))     # one listed ID with no data
    split_pilot.write(pilot_ids, {"p001": by_name["a pilot participant"]["platform_id"], "p002": prolific_id(rng)})

    # ---- export
    ex_dir = os.path.join(d, "export")
    rec = export(raw, ids, pilot_ids, ex_dir, "simulated")
    data_path = os.path.join(ex_dir, "main_data.json")
    doc = PA.load(data_path)
    id_map = PA.load(os.path.join(ex_dir, "main_id_map.json"))
    back = {v: k for k, v in id_map.items()}
    truth_of = {p["platform_id"]: p for p in sims}
    # who should be exported, in which order: everyone on the list with data, but the pilot participant
    expect = sorted([(p["t_start"], p["platform_id"]) for p in sims]
                    + [(p["record"]["t_start"], p["platform_id"]) for p in planted
                       if p["name"] not in ("a pilot participant", "not on Prolific's list")])
    ok_order = [id_map[p["pid"]] for p in doc["participants"]] == [pid for _, pid in expect]
    wrong = []
    for p in doc["participants"]:
        pid = id_map[p["pid"]]
        want = truth_of[pid]["ch"] if pid in truth_of else any_ch
        if pid == by_name["three attention checks failed"]["platform_id"]:
            want = att_ch
        if any(t["choice"] != int(want[t["id"]]) for t in p["trials"]):
            wrong.append(p["pid"])
    check("export: everyone on the list is exported once, in order of start, and every choice is the simulated one",
          ok_order and not wrong and len(doc["participants"]) == len(expect),
          f"{len(doc['participants'])} exported of {len(expect)} expected, {len(wrong)} with a wrong choice")
    lo = rec["left_out"]
    check("export: left out as planted: the pilot participant, the one not on the list, the stray file, the later session",
          lo["pilot_participants"] == 1 and lo["participants_not_on_list"] == 1 and lo["files_not_records"] == 1
          and lo["later_sessions_not_counted"] == 1 and lo["prolific_ids_without_data"] == 1 and lo["excluded_with_problems"] == 0,
          json.dumps(lo))
    leaked = []
    for name in ("main_data.json", "export_record.json"):
        with open(os.path.join(ex_dir, name)) as f:
            text = f.read()
        leaked += [pid for pid in id_map.values() if pid in text]
    check("export: no Prolific ID outside main_id_map.json and main_problems.json", not leaked, f"{len(leaked)} found")

    # ---- the people who count, from the simulation itself
    numbered = {pid: back[pid] for pid in back}
    inc = [numbered[pid] for _, pid in expect if pid in truth_of and truth_of[pid]["included"]]
    second_try = by_name["quiz passed at the second try"]["platform_id"]
    # the planted second-try person chose as `base`, who qualifies by the attention checks, so they are included, and
    # flagged if `base` is
    inc = sorted(inc + [numbered[second_try]])
    flag_of = {numbered[pid]: p["flagged"] for pid, p in truth_of.items()}
    flag_of[numbered[second_try]] = base["flagged"]
    want_unflagged = [pid for pid in inc if not flag_of[pid]]
    want_counted, want_prior = want_unflagged[:n], inc[:PRIOR_N]
    w = who_counts(doc["participants"])
    check(f"grade: the people counted are the first {n} who qualify, in order of start, and the prior's are the first "
          f"{PRIOR_N} included, flagged or not",
          w["unflagged"][:n] == want_counted and w["included"][:PRIOR_N] == want_prior and w["included"] == inc,
          f"included {len(w['included'])} (expected {len(inc)}), flagged {len(w['flagged'])}, counted "
          f"{len(w['unflagged'][:n])}, prior {len(w['included'][:PRIOR_N])} with "
          f"{len(set(w['included'][:PRIOR_N]) & set(w['flagged']))} flagged")
    out_pids = {numbered[by_name[k]["platform_id"]] for k in ("quiz failed twice", "stopped after 70 choices",
                                                              "three attention checks failed",
                                                              "a first session stopped, a second finished")}
    check("grade: the planted people who do not qualify are neither counted nor in the prior; the second-try quiz counts",
          not out_pids & set(w["included"]) and numbered[second_try] in w["included"],
          f"{sorted(out_pids)} left out; {numbered[second_try]} included")

    # ---- grade, and the same numbers computed again from the simulation
    g_dir = os.path.join(d, "grade")
    res, written = grade(data_path, g_dir, n=n, kappa_fit=kfit)     # the one grade that fits hier.py with --hier
    check("grade: a simulated input writes rehearsal_main_results.json only",
          os.path.basename(written) == "rehearsal_main_results.json" and not os.path.exists(os.path.join(g_dir, "main_results.json")))
    y_sim = {numbered[pid]: coded(p["ch"]) for pid, p in truth_of.items()}
    y_sim[numbered[second_try]] = coded(any_ch)
    f1, priors, f2 = fit_all(y_sim, want_prior, want_counted)
    ps = [R.evaluate({"y": y_sim[pid], "pl": y_sim[pid], "shape": {}}, f2[pid], f1[pid]) for pid in want_counted]
    again = R.tests(ps)

    def same(res, again):
        keys = [("claim", "H1", "H_vs_EARLY"), ("claim", "H2", "H_vs_RDU"), ("claim", "H3", "H_vs_CAG")]
        diffs = [h for top, h, k in keys if (res[top][h]["est"], res[top][h]["hi"]) != (again[k]["est"], again[k]["hi"])]
        diffs += [k for k in ("H4", "MF1", "MF2") if (res["H4"] if k == "H4" else res["model_free"][k]) != again[k]]
        diffs += [k for k in ("SH1_IA_beats_GEO", "SH2_straddle_beyond_GEO") if
                  res["secondary"]["SH1" if k.startswith("SH1") else "SH2"] != again["secondary"][k]]
        diffs += [] if res["mean_ll"] == again["mean_ll"] else ["mean_ll"]
        return diffs

    diffs = same(res, again)
    check("grade: every registered number equals rehearsal.tests on the simulated choices of the expected people",
          not diffs, f"differ: {diffs}; claim {res['claim']['pass']}, H1 {res['claim']['H1']['hi']:+.4f}, "
                     f"H2 {res['claim']['H2']['hi']:+.4f}, H3 {res['claim']['H3']['hi']:+.4f}, H4 {res['H4']['pass']}, "
                     f"secondary {res['secondary']['pass']}")
    k_ok = (res["population_kappa"].get("kappa_median") is not None and np.isfinite(res["population_kappa"]["kappa_median"])
            and res["population_kappa"]["lo"] < res["population_kappa"]["kappa_median"] < res["population_kappa"]["hi"])
    check(f"grade: the population kappa from {'hier.py' if use_hier else 'a stub'} on the {n} people counted",
          k_ok and res["population_kappa"]["people"] == n,
          f"median {res['population_kappa'].get('kappa_median')}, interval [{res['population_kappa'].get('lo')}, "
          f"{res['population_kappa'].get('hi')}], divergences {res['population_kappa'].get('divergences')}")

    # ---- two controls: each must make a check above fail
    saved = coded, flagged
    try:
        # The choices read the other way round. The flag then catches people who favour the charity, and fewer may
        # qualify than n, so this runner is graded at the n it can reach and compared with the right computation there.
        coded = lambda ch: np.asarray(ch[:N_MAIN]).astype(float)  # noqa: E731
        n_c = min(n, len(who_counts(doc["participants"])["unflagged"]))
        res_c, _ = grade(data_path, os.path.join(d, "grade_swap"), n=n_c, kappa_fit=stub)
        coded, flagged = saved[0], (lambda y: False)
        w_c = who_counts(doc["participants"])
    finally:
        coded, flagged = saved
    if n_c == n:
        again_c = again
    else:
        f1c, _, f2c = fit_all(y_sim, want_prior, want_unflagged[:n_c])
        again_c = R.tests([R.evaluate({"y": y_sim[pid], "pl": y_sim[pid], "shape": {}}, f2c[pid], f1c[pid])
                           for pid in want_unflagged[:n_c]])
    check("control: a runner that reads the choices the other way round fails the comparison", bool(same(res_c, again_c)),
          f"at n = {n_c}, differ: {same(res_c, again_c)}")
    check("control: a runner that ignores the self-only flag counts other people", w_c["unflagged"][:n] != want_counted,
          f"{len(set(w_c['unflagged'][:n]) - set(want_counted))} of the {n} counted are flagged people")

    # ---- the guards
    def variant(name, fn, base=data_path):
        v = PA.load(base)
        fn(v)
        path = os.path.join(d, f"main_data_{name}.json")
        PA.dump(v, path)
        return path

    import seal_main  # noqa: PLC0415
    rec_dir = os.path.join(d, "records")
    os.makedirs(rec_dir, exist_ok=True)

    def record(name, **changes):
        r = seal_main.make_record(n=n, decision=f"n = {n} (self-test)", pilot=None, bundle=["main_analysis.py"],
                                  frozen_at="self-test")
        for k, fn in changes.items():
            r[k] = fn(r)
        path = os.path.join(rec_dir, f"{name}.sha256")
        PA.dump(r, path)
        return path

    human = variant("human", lambda v: v.update(source="human"))
    refused("grade: human data without the seal of step 10 are refused", "missing",
            lambda: grade(human, g_dir, record_path=os.path.join(rec_dir, "absent.sha256"), kappa_fit=stub))
    good = record("good")
    refused("grade: human data at an n given by hand are refused", "n",
            lambda: grade(human, g_dir, record_path=good, n=n, kappa_fit=stub))
    refused("grade: a seal that names another main_analysis.py is refused", "runner",
            lambda: grade(human, g_dir, record_path=record("runner", files=lambda r: {**r["files"], "main_analysis.py": "0" * 64}),
                          kappa_fit=stub))
    refused("grade: a seal that names another design seal is refused", "seal",
            lambda: grade(human, g_dir, record_path=record("base", base=lambda r: {**r["base"], "combined_sha256": "0" * 64}),
                          kappa_fit=stub))
    refused("grade: a seal recording an n outside 120 to 240 is refused", "n",
            lambda: grade(human, g_dir, record_path=record("n100", n=lambda r: 100), kappa_fit=stub))
    no_pilot = variant("nopilot", lambda v: v["export"].update(pilot_id_map_sha256=None), base=human)
    refused("grade: human data exported without the pilot's id map are refused", "pilot",
            lambda: grade(no_pilot, g_dir, record_path=good, kappa_fit=stub))
    refused("grade: another stimulus hash is refused", "hash",
            lambda: grade(variant("hash", lambda v: v.update(stimuli_sha256="0" * 64)), g_dir, n=n, kappa_fit=stub))
    refused("grade: an undeclared source is refused", "provenance",
            lambda: grade(variant("source", lambda v: v.update(source="unknown")), g_dir, n=n, kappa_fit=stub))
    refused("grade: a participant field the export does not write (a Prolific ID) is refused", "field",
            lambda: grade(variant("field", lambda v: v["participants"][0].update(platform_id="X")), g_dir, n=n, kappa_fit=stub))
    pilot_trial = {"id": N_MAIN, "pos": 140, "choice": 0, "rt_ms": 1000}
    refused("grade: a pilot-only trial is refused", "format",
            lambda: grade(variant("trial", lambda v: v["participants"][0]["trials"].append(pilot_trial)), g_dir, n=n,
                          kappa_fit=stub))
    refused("grade: fewer people qualifying than n is refused", "short",
            lambda: grade(data_path, g_dir, n=len(w["unflagged"]) + 1, kappa_fit=stub))
    res_h, written_h = grade(human, os.path.join(d, "grade_human"), record_path=good, kappa_fit=stub)
    check("grade: human data under an intact seal of step 10 are graded at its n into main_results.json",
          os.path.basename(written_h) == "main_results.json" and res_h["n"] == n and res_h["inputs"]["record"]["n"] == n
          and res_h["claim"] == res["claim"], f"n {res_h['n']}, claim {res_h['claim']['pass']}")
    refused("export: a human export without the pilot's id map is refused", "pilot",
            lambda: export(raw, ids, None, os.path.join(d, "export_nopilot"), "human"))
    raw_bad = os.path.join(d, "raw_bad")
    shutil.rmtree(raw_bad, ignore_errors=True)
    shutil.copytree(raw, raw_bad)
    victim = sims[3]
    path = next(os.path.join(raw_bad, f) for f in sorted(os.listdir(raw_bad)) if f.startswith(victim["platform_id"]))
    r = PA.load(path)
    r["payment"]["bonus_cents"] += 5
    PA.dump(r, path)
    refused("export: a session whose payment does not follow from its choice is refused", "problems",
            lambda: export(raw_bad, ids, pilot_ids, os.path.join(d, "export_bad"), "simulated"))
    rec_x = export(raw_bad, ids, pilot_ids, os.path.join(d, "export_bad"), "simulated", exclude_problems=True)
    check("export: with --exclude-problems that session is left out and counted",
          rec_x["left_out"]["excluded_with_problems"] == 1 and rec_x["counts"]["participants"] == rec["counts"]["participants"] - 1,
          json.dumps(rec_x["left_out"]))
    raw_mode = os.path.join(d, "raw_mode")
    shutil.rmtree(raw_mode, ignore_errors=True)
    shutil.copytree(raw, raw_mode)
    r = session(sims[4]["platform_id"], sims[4]["ch"], rng, sims[4]["t_start"] - 1.0, mode="pilot")
    save(raw_mode, r)
    refused("export: a session saved in the pilot's mode is refused", "problems",
            lambda: export(raw_mode, ids, pilot_ids, os.path.join(d, "export_mode"), "simulated"))

    failed = [r for r in results if not r["pass"]]
    print(f"self-test: {len(results) - len(failed)} of {len(results)} checks passed", flush=True)
    summary = {k: res[k] for k in ("n", "counts", "claim", "H4", "model_free", "population_kappa", "secondary")}
    summary["population_kappa"] = {k: v for k, v in summary["population_kappa"].items() if k != "draws"}
    PA.dump({"format": SELFTEST_FORMAT, "pass": not failed, "passed": len(results) - len(failed), "checks": results,
             "truth": truth, "n": n, "hier": use_hier, "code_sha256": code_hashes(), "stimuli_sha256": export_pilot.DIGEST,
             "simulated_study": summary, "seconds": time.time() - t_begin,
             "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, os.path.join(d, "main_selftest.json"))
    return not failed


# ---- the rehearsal --------------------------------------------------------------------------------------------

def rehearse(truth, studies, out, n=120, seed=0):
    """Simulated main studies of one truth through the saved files, export and grade (MAIN.md, "The rehearsal")."""
    R.spec(truth)       # an unknown truth fails here, before anything runs
    rows, t0 = [], time.time()
    for s in range(studies):
        rng = np.random.default_rng([R.SEED, SIM_STREAM, zlib.crc32(truth.encode()), seed, s])
        with tempfile.TemporaryDirectory() as d:
            sims = simulated_study(truth, rng, n, os.path.join(d, "raw"))
            with open(os.path.join(d, "ids.txt"), "w") as f:
                f.write("".join(p["platform_id"] + "\n" for p in sims))
            export(os.path.join(d, "raw"), os.path.join(d, "ids.txt"), None, os.path.join(d, "export"), "simulated")
            res, _ = grade(os.path.join(d, "export", "main_data.json"), os.path.join(d, "grade"), n=n, kappa_fit=no_hier)
        rows.append({"study": s, "claim": res["claim"]["pass"],
                     **{h: {k: res["claim"][h][k] for k in ("est", "hi", "pass")} for h in ("H1", "H2", "H3")},
                     "H4": res["H4"]["pass"], "MF1": res["model_free"]["MF1"]["pass"], "MF2": res["model_free"]["MF2"]["pass"],
                     "secondary": res["secondary"]["pass"], "SH1": res["secondary"]["SH1"]["pass"],
                     "SH2": res["secondary"]["SH2"]["pass"], "counts": res["counts"],
                     "rank_one_recruited": sum(p["rank_one"] for p in sims), "recruited": len(sims)})
        print(s, f"{time.time() - t0:.0f}s", f"claim {rows[-1]['claim']} secondary {rows[-1]['secondary']}", flush=True)
    doc = {"format": REHEARSE_FORMAT, "truth": truth, "n": n, "seed": seed, "studies": rows, "code_sha256": code_hashes(),
           "stimuli_sha256": export_pilot.DIGEST, "seconds": time.time() - t0}
    PA.dump(doc, out)
    return doc


# The bars, set in MAIN.md ("The rehearsal") before the runs, from the sealed table and rehearsal version 4.
POWERED = {"G100T15S30": 16}               # claim passes in at least this many of 20 studies
NULLS = ("EARLY", "RDU", "CAG", "ADD", "IA")
NULL_MAX = 1                               # claim passes in at most this many of 20 under a truth without the metric
IA_SECONDARY_MIN = 18                      # the secondary claim passes in at least this many of 20 under IA
SECONDARY_MAX = 1                          # and in at most this many under every other truth


def summarise(out, paths):
    by = {}
    for path in paths:
        doc = PA.load(path)
        by.setdefault(doc["truth"], []).append(doc)
    table, bars = {}, []
    codes = {json.dumps(doc["code_sha256"], sort_keys=True) for docs in by.values() for doc in docs}
    for truth, docs in sorted(by.items()):
        rows = [r for doc in docs for r in doc["studies"]]
        table[truth] = {"studies": len(rows), "n": sorted({doc["n"] for doc in docs}),
                        "seeds": sorted({doc["seed"] for doc in docs}),
                        **{k: sum(bool(r[k]) for r in rows) for k in ("claim", "secondary", "H4", "MF1", "MF2", "SH1", "SH2")},
                        **{h: sum(bool(r[h]["pass"]) for r in rows) for h in ("H1", "H2", "H3")},
                        "flagged_share": float(np.mean([r["counts"]["flagged"] / r["counts"]["included"] for r in rows])),
                        "rank_one_share": float(np.mean([r["rank_one_recruited"] / r["recruited"] for r in rows]))}
        t = table[truth]
        if truth in POWERED:
            bars.append((f"{truth}: the claim passes in at least {POWERED[truth]} of {t['studies']}", t["claim"] >= POWERED[truth]))
        if truth in NULLS:
            bars.append((f"{truth}: the claim passes in at most {NULL_MAX} of {t['studies']}", t["claim"] <= NULL_MAX))
        if truth == "IA":
            bars.append((f"IA: the secondary claim passes in at least {IA_SECONDARY_MIN} of {t['studies']}",
                         t["secondary"] >= IA_SECONDARY_MIN))
        else:
            bars.append((f"{truth}: the secondary claim passes in at most {SECONDARY_MAX} of {t['studies']}",
                         t["secondary"] <= SECONDARY_MAX))
    bars.append(("every run used the same code", len(codes) == 1))
    doc = {"format": REHEARSE_FORMAT + "/summary", "table": table, "bars": [{"bar": b, "pass": ok} for b, ok in bars],
           "pass": all(ok for _, ok in bars), "code_sha256": json.loads(next(iter(codes))) if len(codes) == 1 else None,
           "runs": [os.path.basename(p) for p in paths], "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    PA.dump(doc, out)
    for b, ok in bars:
        print(f"{'PASS' if ok else 'FAIL'}  {b}")
    return doc


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("export")
    a.add_argument("raw")
    a.add_argument("--prolific", required=True)
    a.add_argument("--pilot-ids", default=None, help="the pilot's id_map.json; required for human data")
    a.add_argument("--out", required=True)
    a.add_argument("--source", required=True, choices=split_pilot.SOURCES)
    a.add_argument("--exclude-problems", action="store_true")
    a = sub.add_parser("grade")
    a.add_argument("data")
    a.add_argument("--out", required=True)
    a.add_argument("--record", default=None, help=f"the seal of step 10 (default {os.path.basename(SEAL_MAIN)})")
    a.add_argument("--n", type=int, default=None, help="simulated data only")
    a = sub.add_parser("self-test")
    a.add_argument("dir")
    a.add_argument("--hier", action="store_true", help="fit the population kappa with hier.py instead of a stub (needs jax)")
    a = sub.add_parser("rehearse")
    a.add_argument("truth")
    a.add_argument("studies", type=int)
    a.add_argument("out")
    a.add_argument("--n", type=int, default=120)
    a.add_argument("--seed", type=int, default=0)
    a = sub.add_parser("summarise")
    a.add_argument("out")
    a.add_argument("runs", nargs="+")
    args = ap.parse_args()
    np.seterr(all="ignore")
    try:
        if args.cmd == "export":
            rec = export(args.raw, args.prolific, args.pilot_ids, args.out, args.source, args.exclude_problems)
            print(json.dumps({k: rec[k] for k in ("counts", "left_out")}, indent=1))
        elif args.cmd == "grade":
            res, path = grade(args.data, args.out, args.record, args.n)
            print(path, json.dumps({"n": res["n"], "claim": res["claim"]["pass"], "secondary": res["secondary"]["pass"],
                                    "H4": res["H4"]["pass"], "MF1": res["model_free"]["MF1"]["pass"],
                                    "MF2": res["model_free"]["MF2"]["pass"]}, indent=1))
        elif args.cmd == "self-test":
            sys.exit(0 if self_test(args.dir, args.hier) else 1)
        elif args.cmd == "rehearse":
            rehearse(args.truth, args.studies, args.out, args.n, args.seed)
        else:
            sys.exit(0 if summarise(args.out, args.runs)["pass"] else 1)
    except Refusal as e:
        print(f"REFUSED ({e.kind}): {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
