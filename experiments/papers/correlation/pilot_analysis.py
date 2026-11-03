#!/usr/bin/env python3
"""The pilot's analysis (PILOT.md): statistics, references, gates, the row and the sample-size rule.

    python pilot_analysis.py reference OUT.json [--pilots 400] [--people 10000]
    python pilot_analysis.py analyse READABLE.json --reference REF.json --table TABLE.json --out DIR
    python pilot_analysis.py size DIR --table TABLE.json
    python pilot_analysis.py self-test DIR [--hier]
    python pilot_analysis.py rehearse TRUTH PILOTS OUT.json --reference REF.json --table TABLE.json

reference  Simulated pilots of 40 included people from the rehearsal's truths (the version 4 truths and the
           table's GEO rows) through the same 160 trials, every statistic computed as for the real pilot. Also,
           per row, how often the self-only rule flags simulated rank-one people (tpr) and people who trade
           the two off (fpr).
analyse    A readable file from split_pilot.py: inclusion, gates, statistics, targeting rules, the row.
           Writes DIR/pilot_estimates.json when the file declares "source": "human", and
           DIR/rehearsal_pilot_estimates.json otherwise. Aggregates only.
size       The sample-size rule, on DIR/pilot_estimates.json and the sealed power table (power_table.py).
self-test  Every guard driven to refuse, each checked to refuse for its own reason, and a round trip
           through split_pilot.py, including a broken split that must fail it.
rehearse   The pilot rehearsal (PILOT.md, sequence step 4): simulated pilots through split and analysis.

Guards. The analysis refuses (exit 2, naming the reason) a file that carries a trial of the test or secondary
set, or a field the readable file does not have; an undeclared source; a stimulus hash that is not
stimuli.py's; a reference computed on other stimuli or other rules. The sample-size rule reads
DIR/pilot_estimates.json and nothing else. It refuses estimates not marked human, a kappa that did not come
from hier.py, a failed gate, a fired targeting rule, and estimates read against another table.

The self-only flag (revised 2026-11-03, before any data): a person is flagged who chose the self-favouring
option in at least FLAG_MIN of the 24 high-ratio riskless pairs (block R's ratio-2 and ratio-3 pairs and
the four ratio-6 pairs). The flagged share is corrected by the row's simulated rates. The first rule, at
least 38 of 40 block R pairs and all four ratio-6 pairs, flagged 1% to 43% of simulated rank-one people
(PILOT.md).
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
import models as M  # noqa: E402
import rehearsal as R  # noqa: E402
import split_pilot  # noqa: E402
import stimuli  # noqa: E402

READABLE_FORMAT = "correlation-pilot-readable/1"
REF_FORMAT = "correlation-pilot-reference/1"
EST_FORMAT = "correlation-pilot-estimates/1"
TABLE_FORMAT = "correlation-power-table/1"
# the analysis's own list of readable roles, kept apart from split_pilot.py's so that a broken split
# cannot pass through both
READABLE_ROLES = frozenset({"calib", "check", "pilot"})
TOP_KEYS = {"format", "source", "stimuli_sha256", "split", "participants"}
PERSON_KEYS = {"pid", "order_seed", "charity", "quiz", "finished", "t_start", "t_main_end", "t_end", "debrief",
               "payment_ok", "trials"}
TRIAL_KEYS = {"id", "pos", "choice", "rt_ms"}
PILOT_N = 40
MAIN_NS = (120, 160, 200, 240)       # never below 120 (PILOT.md)
TARGET_POWER = 0.80
FLAG_MIN = 18                        # of the 24 high-ratio riskless pairs
ATT_MAX = 2                          # attention-check failures allowed by the inclusion rule
TARGET_MIN = 6                       # a targeting rule also needs at least this many of the 40
Z80 = 0.8416212335729143             # one-sided 80%
BOOT = 2000
V4_TRUTHS = ("GEO1", "GEO2", "EARLY", "RDU", "CAG", "ADD", "IA")
GATES = {"quiz": ">= 0.80", "finish": ">= 0.85", "inclusion_failures": "<= 0.15", "belief": ">= 0.75",
         "fast_choices": "<= 0.10", "main_minutes": "<= 45", "payments": "all", "included": f">= {PILOT_N}"}

TRIALS = stimuli.build()
EXTRAS = stimuli.pilot_extras(TRIALS)
DIGEST = stimuli.digest(TRIALS, EXTRAS)
T = {t["id"]: t for t in TRIALS + EXTRAS}
N_TRIALS = len(T)
DATA = tuple(np.concatenate([a, b]) for a, b in zip(R.ALL, M.arrays(EXTRAS)))


def ids(cond):
    return np.array([i for i, t in sorted(T.items()) if cond(t)], dtype=int)


R_IDS = ids(lambda t: t["block"] == "R")
HI_IDS = ids(lambda t: t["cell"] in ("R_ratio2", "R_ratio3", "PW_ratio6"))
PW6_IDS = ids(lambda t: t["cell"] == "PW_ratio6")
PW025_IDS = ids(lambda t: t["cell"] == "PW_ratio0.25")
A_IDS = ids(lambda t: t["block"] == "A")
CAL = {s: ids(lambda t, s=s: t["block"] == "S" and t["role"] == "calib" and t["side"] == s) for s in ("self", "charity")}
PS = {s: ids(lambda t, s=s: t["block"] == "PS" and t["side"] == s) for s in ("self", "charity")}
CALIB_IDS = ids(lambda t: t["role"] == "calib")
READ_IDS = ids(lambda t: t["role"] in READABLE_ROLES)
PR_PAIRS = [(t["id"], t["repeat_of"]) for t in EXTRAS if t["block"] == "PR"]
SELFOPT, LOTOPT, GOOD = (np.full(N_TRIALS, -9) for _ in range(3))
for _i, _t in T.items():
    if _t["block"] in ("R", "PR", "PW"):
        SELFOPT[_i] = stimuli.self_option(_t)
    if "lot_option" in _t:
        LOTOPT[_i] = _t["lot_option"]
    if "good_option" in _t:
        GOOD[_i] = _t["good_option"]
CODE = ("rehearsal.py", "models.py", "stimuli.py", "hier.py", "split_pilot.py", "pilot_analysis.py")


class Refusal(Exception):
    """A guard's refusal. `kind` names the reason, so a test can tell a refusal for the right reason from one
    for another (PILOT.md: a refusal for the wrong reason proves nothing)."""

    def __init__(self, kind, msg):
        super().__init__(msg)
        self.kind = kind


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def code_hashes():
    return {name: sha256(os.path.join(HERE, name)) for name in CODE}


def load(path):
    with open(path) as f:
        return json.load(f)


def dump(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=1)


def cell(kappa, target):
    return f"G{round(kappa * 100):03d}T{round(target * 10):02d}"


def table_rows():
    """The GEO rows of the version 5 table: kappa by noise target, nobody of rank one, the usual lapse."""
    return [t for t in R.TABLE_V5 if R.spec(t)["base"] == "GEO" and not R.spec(t)["share"] and R.spec(t)["lapse"] == 0.06]


def quantiles(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if not len(x):
        return {"n": 0}
    q = np.quantile(x, [0.025, 0.2, 0.5, 0.8, 0.975])
    return {"n": int(len(x)), "mean": float(x.mean()), **dict(zip(("q025", "q20", "q50", "q80", "q975"), map(float, q)))}


def wilson_upper(k, n, z=Z80):
    p = k / n
    centre = p + z * z / (2 * n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return float(min(1.0, (centre + half) / (1 + z * z / n)))


# ---- per person and per pilot ---------------------------------------------------------------------------------

def person(ch):
    """One participant's statistics from their choices: an array over the 160 trials holding the option chosen,
    and -1 where the readable file has no choice."""
    def took(idx, opt):
        return int(np.sum(ch[idx] == opt[idx]))

    return {"self_R": took(R_IDS, SELFOPT), "self_hi": took(HI_IDS, SELFOPT), "self_pw6": took(PW6_IDS, SELFOPT),
            "self_pw025": took(PW025_IDS, SELFOPT),
            # a repeat shows the original's options with the sides swapped, so the same option is the other index
            "agree": float(np.mean([ch[i] == 1 - ch[j] for i, j in PR_PAIRS])),
            "att_fail": int(np.sum(ch[A_IDS] != GOOD[A_IDS])),
            "lot_cal_self": took(CAL["self"], LOTOPT), "lot_cal_charity": took(CAL["charity"], LOTOPT),
            "lot_ps_self": took(PS["self"], LOTOPT), "lot_ps_charity": took(PS["charity"], LOTOPT),
            "left": float(np.mean(ch[READ_IDS] == 0))}


def pilot_stats(pp):
    """A pilot's statistics from its included people's per-person statistics (PILOT.md, "Reading the pilot")."""
    g = lambda k: np.array([p[k] for p in pp], float)  # noqa: E731
    flag = g("self_hi") >= FLAG_MIN
    self_r, n_r = g("self_R"), len(R_IDS)
    n_cal = len(CAL["self"]) + len(CAL["charity"])
    return {"flag_share": float(flag.mean()),
            "agreement": float(g("agree")[~flag].mean()) if (~flag).any() else float("nan"),
            "always_charity": float(np.mean(self_r == 0)), "never_charity": float(np.mean(self_r == n_r)),
            # targeting rules (PILOT.md): never toward the charity in R but toward it in 2+ of the 4 ratio-6 pairs;
            # always toward it in R but keeping their own points in 2+ of the 4 quarter-ratio pairs; the sure
            # amount in all 12 calibration lotteries of an attribute but a PS lottery of that attribute taken
            "target_self": float(np.mean((self_r == n_r) & (len(PW6_IDS) - g("self_pw6") >= 2))),
            "target_charity": float(np.mean((self_r == 0) & (g("self_pw025") >= 2))),
            "target_risk_self": float(np.mean((g("lot_cal_self") == 0) & (g("lot_ps_self") >= 1))),
            "target_risk_charity": float(np.mean((g("lot_cal_charity") == 0) & (g("lot_ps_charity") >= 1))),
            "lottery_rate": float(np.mean((g("lot_cal_self") + g("lot_cal_charity")) / n_cal)),
            "left_mean": float(g("left").mean()), "left_sd": float(g("left").std(ddof=1)) if len(pp) > 1 else 0.0}


def geo_fits(chs, rng):
    """GEO fitted per person on the calibration trials, first pass (reported only): ratio and metric correlation."""
    data = tuple(arr[CALIB_IDS] for arr in DATA)
    ratio, corr = [], []
    for ch in chs:
        th = M.fit(M.MODELS["GEO"], data, (1 - ch[CALIB_IDS]).astype(float), rng)
        P11, P12, P22 = M.metric(th)
        ratio.append(float(np.sqrt(P22 / P11)))
        corr.append(float(P12 / np.sqrt(P11 * P22)))
    return {"ratio": quantiles(ratio), "corr": quantiles(corr)}


# ---- simulation -----------------------------------------------------------------------------------------------

def sim_choices(truth, rng):
    """One simulated person through the 160 trials (rehearsal.simulate): the option chosen per trial."""
    p = R.simulate(truth, rng, data=DATA)
    return (1 - p["y"]).astype(int), p["shape"]


def recruit(truth, rng, n=PILOT_N):
    """Simulated people until n pass the attention rule, as recruitment does. Returns (included, excluded)."""
    inc, exc = [], []
    while len(inc) < n:
        ch, shape = sim_choices(truth, rng)
        (inc if person(ch)["att_fail"] <= ATT_MAX else exc).append((ch, shape))
    return inc, exc


def simulated_export(truth, rng, n=PILOT_N):
    """An instrument export of a simulated pilot, in the format split_pilot.py reads, with plausible session
    records (one quiz attempt, finished, belief 5, log-normal response times around 3.5 s)."""
    inc, exc = recruit(truth, rng, n)
    people = []
    for k, (ch, _) in enumerate(inc + exc):
        seed = int(rng.integers(2 ** 31))
        order = stimuli.presentation(seed, TRIALS, EXTRAS)
        rt = np.exp(rng.normal(np.log(3500.0), 0.5, len(order)))
        start = 1.8e9 + 900.0 * k + float(rng.uniform(0, 600))
        main_s = float(rt[:len(TRIALS)].sum()) / 1000 + 240.0
        people.append({"platform_id": f"SIM-{int(rng.integers(16 ** 8)):08x}", "order_seed": seed, "charity": "simulated",
                       "quiz": {"attempts": 1, "passed": True}, "finished": True, "t_start": start,
                       "t_main_end": start + main_s, "t_end": start + main_s + float(rt[len(TRIALS):].sum()) / 1000 + 120.0,
                       "debrief": {"belief": 5, "payment_rule_correct": True, "difficulty": 3, "strategy": ""},
                       "payment": {"trial": int(order[int(rng.integers(len(order)))]), "bonus": 0.0, "donation": 0.0,
                                   "bonus_ok": True, "donation_ok": True},
                       "trials": [{"id": int(i), "pos": pos, "choice": int(ch[i]), "rt_ms": int(rt[pos])}
                                  for pos, i in enumerate(order)]})
    order = rng.permutation(len(people))
    export = {"format": split_pilot.EXPORT_FORMAT, "source": "simulated", "stimuli_sha256": DIGEST,
              "participants": [people[int(i)] for i in order]}
    return export, {"included": len(inc), "excluded": len(exc),
                    "rank_one_included": sum(bool(s.get("rank_one")) for _, s in inc)}


def reference(out, pilots=400, people=10000, fit_pilots=5):
    rows = table_rows()
    ref = {"format": REF_FORMAT, "source": "simulated", "stimuli_sha256": DIGEST, "code_sha256": code_hashes(),
           "pilots": pilots, "people": people, "pilot_n": PILOT_N, "flag_min": FLAG_MIN, "att_max": ATT_MAX,
           "truths": {}, "rows": {}, "fits": {}}
    t0 = time.time()
    for truth in V4_TRUTHS + tuple(rows):
        rng = np.random.default_rng([R.SEED, 8, zlib.crc32(truth.encode())])
        sims, excl = [], []
        for _ in range(pilots):
            inc, exc = recruit(truth, rng)
            sims.append(pilot_stats([person(ch) for ch, _ in inc]))
            excl.append(len(exc) / (len(exc) + len(inc)))
        ref["truths"][truth] = {**{k: quantiles([s[k] for s in sims]) for k in sims[0]}, "excluded": quantiles(excl)}
        if truth in V4_TRUTHS and fit_pilots:
            chs = [ch for _ in range(fit_pilots) for ch, _ in recruit(truth, rng)[0]]
            ref["fits"][truth] = geo_fits(chs, rng)
        print(truth, f"{time.time() - t0:.0f}s", flush=True)
    for row in rows:
        rng = np.random.default_rng([R.SEED, 9, zlib.crc32(row.encode())])
        counts = {"trader": [0, 0], "rank_one": [0, 0]}
        while min(c[1] for c in counts.values()) < people:
            ch, shape = sim_choices(row + "S50", rng)      # half of them of rank one, the rest as in the row
            st = person(ch)
            if st["att_fail"] > ATT_MAX:
                continue
            c = counts["rank_one" if shape.get("rank_one") else "trader"]
            if c[1] < people:
                c[0] += st["self_hi"] >= FLAG_MIN
                c[1] += 1
        sp = R.spec(row)
        ref["rows"][row] = {"kappa": sp["kappa"], "target": sp["target"], "tpr": counts["rank_one"][0] / people,
                            "fpr": counts["trader"][0] / people, "people": people}
        print(row, ref["rows"][row], f"{time.time() - t0:.0f}s", flush=True)
    ref["seconds"] = time.time() - t0
    dump(ref, out)
    return ref


# ---- loading, with the guards ---------------------------------------------------------------------------------

def load_readable(path):
    doc = load(path)
    if doc.get("format") != READABLE_FORMAT:
        raise Refusal("format", f"{path} is not a readable pilot file (format {doc.get('format')!r}); "
                                f"run split_pilot.py on the export first")
    if doc.get("source") not in ("human", "simulated"):
        raise Refusal("provenance", f"{path} does not declare its source as human or simulated ({doc.get('source')!r})")
    if doc.get("stimuli_sha256") != DIGEST:
        raise Refusal("hash", f"{path} names stimulus hash {doc.get('stimuli_sha256')}, not stimuli.py's {DIGEST}")
    if set(doc) - TOP_KEYS:
        raise Refusal("field", f"{path} has fields a readable file does not have: {sorted(set(doc) - TOP_KEYS)}")
    for p in doc["participants"]:
        if set(p) - PERSON_KEYS:
            raise Refusal("field", f"participant {p.get('pid')} has fields a readable file does not have: "
                                   f"{sorted(set(p) - PERSON_KEYS)}")
        seen = set()
        for t in p["trials"]:
            if set(t) - TRIAL_KEYS:
                raise Refusal("field", f"participant {p['pid']}, trial {t.get('id')}: fields {sorted(set(t) - TRIAL_KEYS)}")
            tr = T.get(t["id"])
            if tr is None or t["id"] in seen or t["choice"] not in (0, 1):
                raise Refusal("format", f"participant {p['pid']}: unknown, repeated or invalid trial {t.get('id')}")
            if tr["role"] not in READABLE_ROLES:
                raise Refusal("sealed", f"participant {p['pid']} carries trial {t['id']} (block {tr['block']}, role "
                                        f"{tr['role']}), which belongs to the sealed file; the analysis reads only "
                                        f"calibration, attention-check and pilot-only trials")
            seen.add(t["id"])
    return doc


def load_reference(path):
    ref = load(path)
    if ref.get("format") != REF_FORMAT:
        raise Refusal("format", f"{path} is not a pilot reference (format {ref.get('format')!r})")
    if ref.get("stimuli_sha256") != DIGEST:
        raise Refusal("hash", f"the reference {path} was computed on stimuli {ref.get('stimuli_sha256')}, not {DIGEST}")
    rules = {"pilot_n": PILOT_N, "flag_min": FLAG_MIN, "att_max": ATT_MAX}
    if any(ref.get(k) != v for k, v in rules.items()):
        raise Refusal("rules", f"the reference {path} was computed with other rules: {[ref.get(k) for k in rules]} "
                               f"against {list(rules.values())}")
    return ref


def load_table(path):
    tab = load(path)
    if tab.get("format") != TABLE_FORMAT:
        raise Refusal("format", f"{path} is not a power table (format {tab.get('format')!r})")
    return tab


def choices(p):
    ch = np.full(N_TRIALS, -1)
    for t in p["trials"]:
        ch[t["id"]] = t["choice"]
    return ch


def hier_kappa(Y, seed):
    import hier  # noqa: PLC0415  (jax is needed only here)
    return {**hier.fit(tuple(arr[CALIB_IDS] for arr in DATA), Y, seed=seed), "fit": "hier.py", "people": int(Y.shape[0])}


# ---- the analysis ---------------------------------------------------------------------------------------------

def analyse(path, ref_path, table_path, out_dir, kappa_fit=hier_kappa, seed=0):
    doc = load_readable(path)
    ref = load_reference(ref_path)
    tab = load_table(table_path)
    kappas, targets = sorted(tab["kappas"]), sorted(tab["targets"])
    uncovered = [cell(k, t) for k in kappas for t in targets if cell(k, t) not in ref["truths"] or cell(k, t) not in ref["rows"]]
    if uncovered:
        raise Refusal("rules", f"the reference {ref_path} lacks table rows {uncovered}; recompute it for this table")
    everyone = doc["participants"]
    quiz_ok = [p for p in everyone if (p.get("quiz") or {}).get("passed") and p["quiz"].get("attempts", 9) <= 2]
    finished = [p for p in quiz_ok if p.get("finished")]
    stats = {p["pid"]: person(choices(p)) for p in finished}
    included = [p for p in finished if stats[p["pid"]]["att_fail"] <= ATT_MAX]
    pp = [stats[p["pid"]] for p in included]
    n = len(included)

    def frac(num, den):
        return num / den if den else float("nan")

    rts = [t["rt_ms"] for p in included for t in p["trials"]]
    minutes = [(p["t_main_end"] - p["t_start"]) / 60 for p in included if p.get("t_main_end") and p.get("t_start")]
    value = {"quiz": frac(len(quiz_ok), len(everyone)), "finish": frac(len(finished), len(quiz_ok)),
             "inclusion_failures": frac(len(finished) - n, len(finished)),
             "belief": frac(sum(((p.get("debrief") or {}).get("belief") or 0) >= 4 for p in included), n),
             "fast_choices": frac(sum(rt < 1000 for rt in rts), len(rts)),
             "main_minutes": float(np.median(minutes)) if minutes else float("nan"),
             "payments": all(all((p.get("payment_ok") or {}).get(k) for k in ("bonus", "donation")) for p in everyone),
             "included": n}
    ok = {"quiz": value["quiz"] >= 0.80, "finish": value["finish"] >= 0.85, "inclusion_failures": value["inclusion_failures"] <= 0.15,
          "belief": value["belief"] >= 0.75, "fast_choices": value["fast_choices"] <= 0.10,
          "main_minutes": value["main_minutes"] <= 45, "payments": bool(value["payments"]), "included": n >= PILOT_N}
    gates = {g: {"value": value[g], "bar": GATES[g], "pass": bool(ok[g])} for g in GATES}

    st = pilot_stats(pp)
    flag = np.array([s["self_hi"] >= FLAG_MIN for s in pp])
    keep = [p for p, f in zip(included, flag) if not f]
    ag = np.array([s["agree"] for s, f in zip(pp, flag) if not f])
    brng = np.random.default_rng([R.SEED, 6, seed])
    a20 = float(np.quantile([ag[brng.integers(0, len(ag), len(ag))].mean() for _ in range(BOOT)], 0.2)) if len(ag) else float("nan")
    if len(keep) >= 2:
        kf = kappa_fit(np.stack([1 - choices(p)[CALIB_IDS] for p in keep]).astype(float), seed)
    else:
        kf = {"kappa_median": float("nan"), "q80": float("nan"), "fit": "none: fewer than two unflagged people"}

    # the smallest tabulated kappa at or above the posterior's 80th percentile (PILOT.md). When even that
    # percentile is below the table, the smallest row is used and the estimates say so: power below kappa = 1
    # was not simulated.
    row = {"kappa": None, "target": None, "cell": None, "q80_below_table": bool(kf["q80"] < kappas[0])}
    above = [k for k in kappas if k >= kf["q80"] - 1e-9]
    if above:
        row["kappa"] = above[0]
        med = {t: ref["truths"][cell(row["kappa"], t)]["agreement"]["q50"] for t in targets}
        row["sim_agreement_median"] = {str(t): v for t, v in med.items()}
        fit = [t for t in targets if med[t] <= a20]
        if fit:
            row["target"] = max(fit)
            row["cell"] = cell(row["kappa"], row["target"])
    s = {"flagged": int(flag.sum()), "n": n, "share": frac(int(flag.sum()), n), "q_upper": wilson_upper(int(flag.sum()), n) if n else float("nan")}
    if row["cell"]:
        rr = ref["rows"][row["cell"]]
        s.update(tpr=rr["tpr"], fpr=rr["fpr"], upper=float(np.clip((s["q_upper"] - rr["fpr"]) / (rr["tpr"] - rr["fpr"]), 0, 1)))

    targeting = {}
    for name in ("target_self", "target_charity", "target_risk_self", "target_risk_charity"):
        bar = max(ref["truths"][t][name]["q975"] for t in V4_TRUTHS)
        count = int(round(st[name] * n))
        targeting[name] = {"share": st[name], "count": count, "reference_q975_max": bar,
                           "fired": bool(st[name] > bar and count >= TARGET_MIN)}

    # reported, not used for the row
    t_row = row["target"] or 1.5
    lot = {k: ref["truths"][cell(k, t_row)]["lottery_rate"]["q50"] for k in kappas}
    lot_k = min(kappas, key=lambda k: abs(lot[k] - st["lottery_rate"]))
    reported = {"lottery_rate": st["lottery_rate"], "lottery_rate_by_row": {str(k): v for k, v in lot.items()},
                "lottery_kappa_row": lot_k,
                "lottery_row_two_or_more_steps_from_hier": bool(row["kappa"] is not None and
                                                                abs(kappas.index(lot_k) - kappas.index(row["kappa"])) >= 2),
                "always_charity": st["always_charity"], "never_charity": st["never_charity"],
                "left_mean": st["left_mean"], "left_sd": st["left_sd"],
                "geo_fits": geo_fits([choices(p) for p in keep], np.random.default_rng([R.SEED, 10, seed])),
                "reference_under_v4": {t: {k: ref["truths"][t][k] for k in ("always_charity", "lottery_rate", "left_mean",
                                                                          "excluded")} for t in V4_TRUTHS},
                "reference_fits_under_v4": ref.get("fits", {})}
    est = {"format": EST_FORMAT, "source": doc["source"],
           "inputs": {"readable_sha256": sha256(path), "reference_sha256": sha256(ref_path), "table_sha256": sha256(table_path),
                      "stimuli_sha256": DIGEST, "code_sha256": code_hashes(), "split": doc.get("split")},
           "counts": {"participants": len(everyone), "quiz_passed": len(quiz_ok), "finished": len(finished),
                      "included": n, "flagged": int(flag.sum())},
           "gates": gates, "gates_pass": all(g["pass"] for g in gates.values()), "statistics": st,
           "agreement": {"mean": float(ag.mean()) if len(ag) else float("nan"), "q20": a20, "people": int(len(ag))},
           "kappa": kf, "row": row, "s": s, "targeting": targeting, "reported": reported,
           "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    os.makedirs(out_dir, exist_ok=True)
    name = "pilot_estimates.json" if doc["source"] == "human" else "rehearsal_pilot_estimates.json"
    dump(est, os.path.join(out_dir, name))
    return est, os.path.join(out_dir, name)


# ---- the sample-size rule -------------------------------------------------------------------------------------

def size(est_dir, table_path):
    path = os.path.join(est_dir, "pilot_estimates.json")
    if not os.path.exists(path):
        raise Refusal("missing", f"no pilot_estimates.json in {est_dir}")
    est = load(path)
    if est.get("source") != "human":
        raise Refusal("provenance", f"{path} declares source {est.get('source')!r}; the sample-size rule takes "
                                    f"estimates from human data only")
    if (est.get("kappa") or {}).get("fit") != "hier.py":
        raise Refusal("kappa", f"{path}: kappa came from {(est.get('kappa') or {}).get('fit')!r}, not hier.py")
    failed = [g for g, v in est["gates"].items() if not v["pass"]]
    if failed:
        raise Refusal("gate", f"{path} reports failed gate(s) {failed}; the instrument is fixed and the pilot repeated")
    fired = [k for k, v in est["targeting"].items() if v["fired"]]
    if fired:
        raise Refusal("targeting", f"{path}: targeting rule(s) {fired} fired; the stimuli change, the table is "
                                   f"recomputed and resealed before n is set")
    if est["inputs"]["table_sha256"] != sha256(table_path):
        raise Refusal("table", f"{path} was read against table {est['inputs']['table_sha256']}, not {table_path}")
    tab = load_table(table_path)
    row, s = est["row"], est["s"]
    out = {"row": row, "s_upper": s.get("upper"), "table_sha256": sha256(table_path), "estimates_sha256": sha256(path)}
    if row["q80_below_table"]:
        out["note"] = "kappa's 80th percentile is below the table; its smallest row is used, and power there was not simulated"
    if row["kappa"] is None:
        out["decision"] = ("no row: kappa could not be fitted" if not np.isfinite(est["kappa"]["q80"]) else
                           "no row: kappa's 80th percentile is above the table; the study is not powered for this population")
    elif row["target"] is None:
        out["decision"] = "the pilot is noisier than every row: extend the table with the same code"
    else:
        ns = [int(k) for k in tab["ns"]]
        pw = [tab["cells"][row["cell"]]["power"][str(k)] for k in ns]
        curve = [(m, float(np.interp(m * (1 - s["upper"]), [0] + ns, [0.0] + pw))) for m in MAIN_NS]
        out["curve"] = curve
        out["n"] = next((m for m, p in curve if p >= TARGET_POWER), None)
        out["decision"] = (f"n = {out['n']}" if out["n"] else
                           "no n up to 240 reaches 0.80: the owner decides between 240, power stated, and stopping")
    dump(out, os.path.join(est_dir, "sample_size.json"))
    return out


# ---- round trip, self-test and the pilot rehearsal ------------------------------------------------------------

def roundtrip(export_path, out_dir):
    """Every trial of the export is in the file its role says and nowhere else, with its choice and time; no
    platform identifier is outside id_map.json. Checked with this module's own role list. Returns problems."""
    ex = load(export_path)
    rd, sl = load(os.path.join(out_dir, "readable.json")), load(os.path.join(out_dir, "sealed.json"))
    idm = load(os.path.join(out_dir, "id_map.json"))
    rd_by = {idm[p["pid"]]: {t["id"]: t for t in p["trials"]} for p in rd["participants"]}
    sl_by = {idm[p["pid"]]: {t["id"]: t for t in p["trials"]} for p in sl["participants"]}
    problems = []
    for p in ex["participants"]:
        pid = p["platform_id"]
        if pid not in rd_by or pid not in sl_by:
            problems.append(f"{pid} is missing from a split file")
            continue
        for t in p["trials"]:
            readable = T[t["id"]]["role"] in READABLE_ROLES
            here, there = (rd_by, sl_by) if readable else (sl_by, rd_by)
            if t["id"] in there[pid]:
                problems.append(f"{pid}: trial {t['id']} (role {T[t['id']]['role']}) is in the "
                                f"{'sealed' if readable else 'readable'} file")
            if here[pid].get(t["id"]) != {k: t[k] for k in TRIAL_KEYS}:
                problems.append(f"{pid}: trial {t['id']} did not arrive intact in the {'readable' if readable else 'sealed'} file")
        if set(rd_by[pid]) | set(sl_by[pid]) != {t["id"] for t in p["trials"]}:
            problems.append(f"{pid}: the split files hold trials the export does not")
    for name in ("readable.json", "sealed.json"):
        with open(os.path.join(out_dir, name)) as f:
            text = f.read()
        leaked = [pid for pid in idm.values() if pid in text]
        if leaked:
            problems.append(f"{name} holds platform identifiers: {leaked[:3]}")
    return problems


def synthetic_table(path):
    """A table with the real one's shape and made-up power, for the self-test only."""
    ns = list(R.NS5)
    cells = {}
    for row in table_rows():
        sp = R.spec(row)
        cells[row] = {"spec": sp, "power": {str(m): float(1 - np.exp(-m / (40.0 * sp["kappa"] ** 3))) for m in ns}}
    dump({"format": TABLE_FORMAT, "source": "synthetic, for the self-test only", "ns": ns,
          "kappas": sorted({c["spec"]["kappa"] for c in cells.values()}),
          "targets": sorted({c["spec"]["target"] for c in cells.values()}), "cells": cells}, path)


def self_test(d, use_hier=False):
    os.makedirs(d, exist_ok=True)
    stub = lambda Y, seed: {"kappa_median": 1.1, "lo": 0.9, "hi": 1.3, "q80": 1.2, "fit": "stub (self-test)",  # noqa: E731
                            "people": int(Y.shape[0])}
    kfit = hier_kappa if use_hier else stub
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}", flush=True)

    def refused(name, kind, fn):
        try:
            fn()
        except Refusal as e:
            check(name, e.kind == kind, f"refused ({e.kind}): {e}")
            return
        check(name, False, "did not refuse")

    rng = np.random.default_rng([R.SEED, 11])
    ref, tab = os.path.join(d, "reference.json"), os.path.join(d, "table.json")
    reference(ref, pilots=10, people=300, fit_pilots=1)
    synthetic_table(tab)
    export, info = simulated_export("GEO1", rng)
    exp_path, split_dir = os.path.join(d, "export.json"), os.path.join(d, "split")
    dump(export, exp_path)
    split_pilot.split(exp_path, split_dir)
    readable = os.path.join(split_dir, "readable.json")
    problems = roundtrip(exp_path, split_dir)
    check("round trip: every trial lands where its role says, nowhere else", not problems, f"{len(problems)} problems")

    est_dir = os.path.join(d, "est")
    est, written = analyse(readable, ref, tab, est_dir, kappa_fit=kfit)
    check("a simulated input writes rehearsal_pilot_estimates.json only",
          os.path.basename(written) == "rehearsal_pilot_estimates.json"
          and not os.path.exists(os.path.join(est_dir, "pilot_estimates.json")))
    check("simulated pilot: 40 included, recruited until they qualify", est["counts"]["included"] == PILOT_N,
          f"counts {est['counts']}, gates failed {[g for g, v in est['gates'].items() if not v['pass']]}, "
          f"row {est['row'].get('cell')}, s {est['s']}")
    refused("size: no estimates at all", "missing", lambda: size(est_dir, tab))
    shutil.copy(written, os.path.join(est_dir, "pilot_estimates.json"))
    refused("size: a simulated file exactly where the rule looks is refused for provenance", "provenance",
            lambda: size(est_dir, tab))

    def forged(**changes):
        """The simulated estimates relabelled as human with every gate passed and no rule fired, then one change,
        so that each refusal below can only come from the guard it tests."""
        e = load(written)
        e.update(source="human", kappa={**e["kappa"], "fit": "hier.py"},
                 gates={g: {**v, "pass": True} for g, v in e["gates"].items()},
                 targeting={k: {**v, "fired": False} for k, v in e["targeting"].items()})
        for k, v in changes.items():
            e[k] = v(e)
        dump(e, os.path.join(est_dir, "pilot_estimates.json"))

    forged(kappa=lambda e: {**e["kappa"], "fit": "stub (self-test)"})
    refused("size: a kappa not from hier.py is refused", "kappa", lambda: size(est_dir, tab))
    forged(gates=lambda e: {**e["gates"], "belief": {**e["gates"]["belief"], "pass": False}})
    refused("size: a failed gate is refused", "gate", lambda: size(est_dir, tab))
    forged(targeting=lambda e: {**e["targeting"], "target_self": {**e["targeting"]["target_self"], "fired": True}})
    refused("size: a fired targeting rule is refused", "targeting", lambda: size(est_dir, tab))
    other = os.path.join(d, "table_other.json")
    synthetic_table(other)
    t2 = load(other)
    t2["source"] += " (altered)"
    dump(t2, other)
    forged()
    refused("size: estimates read against another table are refused", "table", lambda: size(est_dir, other))
    try:
        out = size(est_dir, tab)
        check("size: estimates that pass every guard give a decision (synthetic table, forged source)",
              "decision" in out, out["decision"])
    except Refusal as e:
        check("size: estimates that pass every guard give a decision", False, f"refused ({e.kind}): {e}")

    doc = load(readable)
    sealed_doc = load(os.path.join(split_dir, "sealed.json"))

    def variant(name, fn):
        v = json.loads(json.dumps(doc))
        fn(v)
        path = os.path.join(d, f"readable_{name}.json")
        dump(v, path)
        return path

    leak = sealed_doc["participants"][0]["trials"][0]
    p_leak = variant("leak", lambda v: v["participants"][0]["trials"].append(leak))
    refused(f"analyse: a readable file carrying a sealed trial ({T[leak['id']]['block']}) is refused", "sealed",
            lambda: analyse(p_leak, ref, tab, est_dir, kappa_fit=kfit))
    p_field = variant("field", lambda v: v["participants"][0].update(payment={"trial": 1}))
    refused("analyse: a field the readable file does not have is refused", "field",
            lambda: analyse(p_field, ref, tab, est_dir, kappa_fit=kfit))
    p_src = variant("source", lambda v: v.pop("source"))
    refused("analyse: an undeclared source is refused", "provenance", lambda: analyse(p_src, ref, tab, est_dir, kappa_fit=kfit))
    p_hash = variant("hash", lambda v: v.update(stimuli_sha256="0" * 64))
    refused("analyse: another stimulus hash is refused", "hash", lambda: analyse(p_hash, ref, tab, est_dir, kappa_fit=kfit))
    r2 = load(ref)
    r2["stimuli_sha256"] = "0" * 64
    ref_bad = os.path.join(d, "reference_bad.json")
    dump(r2, ref_bad)
    refused("analyse: a reference on other stimuli is refused", "hash", lambda: analyse(readable, ref_bad, tab, est_dir, kappa_fit=kfit))

    # a deliberately broken split, which leaks the test trials into the readable file
    broken_dir = os.path.join(d, "split_broken")
    saved = split_pilot.READABLE_ROLES
    split_pilot.READABLE_ROLES = saved | {"test"}
    try:
        split_pilot.split(exp_path, broken_dir)
    finally:
        split_pilot.READABLE_ROLES = saved
    problems = roundtrip(exp_path, broken_dir)
    check("a broken split that leaks test choices fails the round trip", bool(problems),
          f"{len(problems)} problems, first: {problems[0] if problems else None}")
    refused("analyse: the broken split's readable file is refused by the analysis's own guard", "sealed",
            lambda: analyse(os.path.join(broken_dir, "readable.json"), ref, tab, est_dir, kappa_fit=kfit))
    failed = [r for r in results if not r[1]]
    print(f"self-test: {len(results) - len(failed)} of {len(results)} checks passed", flush=True)
    return not failed


def rehearse(truth, pilots, ref_path, table_path, out, seed=0):
    """Simulated pilots under one truth through export, split and analysis (with hier.py). Per pilot: the row,
    the kappa posterior, the self-only share and what was planted."""
    rng = np.random.default_rng([R.SEED, 7, zlib.crc32(truth.encode()), seed])
    rows, t0 = [], time.time()
    for k in range(pilots):
        with tempfile.TemporaryDirectory() as d:
            export, info = simulated_export(truth, rng)
            dump(export, os.path.join(d, "export.json"))
            split_pilot.split(os.path.join(d, "export.json"), os.path.join(d, "split"))
            est, _ = analyse(os.path.join(d, "split", "readable.json"), ref_path, table_path, os.path.join(d, "est"),
                             seed=seed * 100003 + k)
        rows.append({"planted": info, "row": est["row"], "kappa": est["kappa"], "s": est["s"],
                     "agreement": est["agreement"], "gates_pass": est["gates_pass"],
                     "targeting": {n: v["fired"] for n, v in est["targeting"].items()}})
        print(k, est["row"].get("cell"), round(est["kappa"]["q80"], 3), est["s"].get("upper"), f"{time.time() - t0:.0f}s", flush=True)
    dump({"truth": truth, "spec": R.spec(truth), "pilots": rows, "code_sha256": code_hashes(),
          "reference_sha256": sha256(ref_path), "table_sha256": sha256(table_path), "seconds": time.time() - t0}, out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("reference")
    a.add_argument("out")
    a.add_argument("--pilots", type=int, default=400)
    a.add_argument("--people", type=int, default=10000)
    a.add_argument("--fit-pilots", type=int, default=5)
    a = sub.add_parser("analyse")
    a.add_argument("readable")
    a.add_argument("--reference", required=True)
    a.add_argument("--table", required=True)
    a.add_argument("--out", required=True)
    a = sub.add_parser("size")
    a.add_argument("dir")
    a.add_argument("--table", required=True)
    a = sub.add_parser("self-test")
    a.add_argument("dir")
    a.add_argument("--hier", action="store_true", help="fit kappa with hier.py instead of a stub (needs jax)")
    a = sub.add_parser("rehearse")
    a.add_argument("truth")
    a.add_argument("pilots", type=int)
    a.add_argument("out")
    a.add_argument("--reference", required=True)
    a.add_argument("--table", required=True)
    a.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    np.seterr(all="ignore")
    try:
        if args.cmd == "reference":
            reference(args.out, args.pilots, args.people, args.fit_pilots)
        elif args.cmd == "analyse":
            est, path = analyse(args.readable, args.reference, args.table, args.out)
            print(path, json.dumps({k: est[k] for k in ("counts", "gates_pass", "row", "s")}, indent=1))
        elif args.cmd == "size":
            print(json.dumps(size(args.dir, args.table), indent=1))
        elif args.cmd == "self-test":
            sys.exit(0 if self_test(args.dir, args.hier) else 1)
        else:
            rehearse(args.truth, args.pilots, args.reference, args.table, args.out, args.seed)
    except Refusal as e:
        print(f"REFUSED ({e.kind}): {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
