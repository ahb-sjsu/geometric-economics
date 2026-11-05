#!/usr/bin/env python3
"""The pilot's analysis (PILOT.md): statistics, references, gates, the row and the sample-size rule.

    python pilot_analysis.py reference OUT.json [--pilots 400] [--people 10000] [--pilot-n N]
    python pilot_analysis.py analyse READABLE.json --reference REF.json --table TABLE.json --out DIR
    python pilot_analysis.py size DIR --table TABLE.json
    python pilot_analysis.py self-test DIR [--hier] [--pilot-n N]
    python pilot_analysis.py rehearse TRUTH PILOTS OUT.json --reference REF.json --table TABLE.json [--seed K] [--pilot-n N]
    python pilot_analysis.py summarise OUT.json REHEARSE.json... --reference REF.json --table TABLE.json [--pilot-n N]

--pilot-n runs the rehearsal's tools at another pilot size than PILOT_N, to choose the size (PILOT.md, "Pilot size").
analyse and size take no such option: the real pilot is read at the sealed size only.

reference  Simulated pilots of PILOT_N included people from the rehearsal's truths (the version 4 truths and the
           table's GEO rows) through the same 160 trials, every statistic computed as for the real pilot. Also,
           per row, how often the self-only rules flag simulated rank-one people (tpr) and people who trade
           the two off (fpr): the pilot's rule and the main study's.
analyse    A readable file from split_pilot.py: inclusion, gates, statistics, targeting rules, and what the
           sample-size rule reads: the posterior draws of the population kappa, the pilot's agreement and the
           upper limit of the self-only share. Writes DIR/pilot_estimates.json when the file declares
           "source": "human", and DIR/rehearsal_pilot_estimates.json otherwise. Aggregates only.
size       The sample-size rule, on DIR/pilot_estimates.json and the sealed power table (power_table.py).
self-test  Every guard driven to refuse, each checked to refuse for its own reason, a round trip through
           split_pilot.py including a broken split that must fail it, and the kappa rule on made-up tables.
rehearse   The pilot rehearsal (PILOT.md, sequence step 4): simulated pilots through split and analysis, and the
           n the rule would choose for each.
summarise  The pilot rehearsal's checks, from its outputs.

The rule (version 6, decided 2026-11-03 before any data; PILOT.md, "Reading the pilot"). For each kappa row of the
table, power is read at the pilot's noise and self-only share: linearly between the two noise rows whose
simulated median agreement brackets the pilot's 20th percentile, and linearly between the tabulated shares at
that row's upper limit for the share. Each draw of kappa takes the lower power of the two rows around it, a
draw above the table takes 0, and n is the smallest of 120 to 240 whose 20th percentile of power over the draws
reaches 0.80. When power falls as kappa rises this reads power at kappa's 80% upper limit, as version 5's rule
did. Version 6 found that power does not always fall. The draws come from kappa's confidence distribution:
the lottery-choice rate at the ideal, read against the reference's simulated pilots (`kappa_belt`). The first
pilot rehearsal took them from hier.py's posterior, which at pilot size sat 0.1 to 0.2 below the truth
(revised 2026-11-03; hier.py's kappa is still reported, as DESIGN.md's secondary analysis).

Guards. The analysis refuses (exit 2, naming the reason) a file that carries a trial of the test or secondary
set, or a field the readable file does not have; an undeclared source; a stimulus hash that is not
stimuli.py's; a reference computed on other stimuli or other rules. The sample-size rule reads
DIR/pilot_estimates.json and nothing else. It refuses estimates not marked human, kappa draws that did not come
from the sealed belt, a failed gate, a fired targeting rule, and estimates read against another table.

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
REF_FORMAT = "correlation-pilot-reference/3"
EST_FORMAT = "correlation-pilot-estimates/3"
KAPPA_SOURCE = "lottery-rate belt/1"     # what the rule's kappa draws must come from (kappa_belt)
BELT_GRID = 500
TABLE_FORMAT = "correlation-power-table/2"
# Which people the main tests count. "unflagged": the people the main study's self-only flag does not catch, the
# owner's decision of 2026-11-04 (DESIGN.md, Inclusion; PILOT.md). "all", every included person, was the registered
# form before it. The table carries both.
MAIN_POPULATION = "unflagged"
KAPPA_Q = 0.2                        # the 20th percentile of power over the kappa posterior
# the analysis's own list of readable roles, kept apart from split_pilot.py's so that a broken split
# cannot pass through both
READABLE_ROLES = frozenset({"calib", "check", "pilot"})
TOP_KEYS = {"format", "source", "stimuli_sha256", "split", "participants"}
PERSON_KEYS = {"pid", "order_seed", "charity", "quiz", "finished", "t_start", "t_main_end", "t_end", "debrief",
               "payment_ok", "trials"}
TRIAL_KEYS = {"id", "pos", "choice", "rt_ms"}
PILOT_N = 120                        # 40 until 2026-11-04, when the owner chose a larger pilot (PILOT.md, "Pilot size")
# The pilot rehearsal may run other sizes (`--pilot-n` on reference, rehearse, summarise and self-test, never on
# analyse or size), so everything below reads PILOT_N when it runs, not when the module loads.
MAIN_NS = (120, 160, 200, 240)       # never below 120 (PILOT.md)
TARGET_POWER = 0.80
FLAG_MIN = 18                        # of the 24 high-ratio riskless pairs
ATT_MAX = 2                          # attention-check failures allowed by the inclusion rule
TARGET_SHARE = 0.15                  # a targeting rule also needs at least this share of the pilot (18 of 120; 6 of 40)
Z80 = 0.8416212335729143             # one-sided 80%
BOOT = 2000
V4_TRUTHS = ("GEO1", "GEO2", "EARLY", "RDU", "CAG", "ADD", "IA")
GATES = {"quiz": ">= 0.80", "finish": ">= 0.85", "inclusion_failures": "<= 0.15", "belief": ">= 0.75",
         "fast_choices": "<= 0.10", "main_minutes": "<= 45", "payments": "all", "included": ">= PILOT_N"}


def target_min():
    return int(np.ceil(TARGET_SHARE * PILOT_N - 1e-9))


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
HI_R_IDS = ids(lambda t: t["cell"] in ("R_ratio2", "R_ratio3"))       # the main study's flag reads these only
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


def cell(kappa, target, share=0.0):
    return f"G{round(kappa * 100):03d}T{round(target * 10):02d}" + (f"S{round(share * 100):02d}" if share else "")


def table_rows():
    """The GEO rows of the version 6 table: kappa by noise target, nobody of rank one, the usual lapse."""
    return [t for t in R.TABLE_V6 if R.spec(t)["base"] == "GEO" and not R.spec(t)["share"] and R.spec(t)["lapse"] == 0.06]


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

    return {"self_R": took(R_IDS, SELFOPT), "self_hi": took(HI_IDS, SELFOPT), "self_hi_R": took(HI_R_IDS, SELFOPT),
            "self_pw6": took(PW6_IDS, SELFOPT),
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
            # the rule's kappa statistic (revised 2026-11-03): the same rate over the people not flagged as self only,
            # whom the table's rows do not contain
            "lottery_rate_unflagged": float(np.mean(((g("lot_cal_self") + g("lot_cal_charity")) / n_cal)[~flag]))
            if (~flag).any() else float("nan"),
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


def recruit(truth, rng, n=None):
    """Simulated people until n (by default PILOT_N) pass the attention rule, as recruitment does. Returns
    (included, excluded)."""
    n = n or PILOT_N
    inc, exc = [], []
    while len(inc) < n:
        ch, shape = sim_choices(truth, rng)
        (inc if person(ch)["att_fail"] <= ATT_MAX else exc).append((ch, shape))
    return inc, exc


def simulated_export(truth, rng, n=None):
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
           "main_flag_min": R.MAIN_FLAG_MIN, "truths": {}, "rows": {}, "fits": {}}
    t0 = time.time()
    bins = (("r below -0.2", -9, -0.2), ("r -0.2 to 0.2", -0.2, 0.2), ("r above 0.2", 0.2, 9))
    for truth in V4_TRUTHS + tuple(rows):
        rng = np.random.default_rng([R.SEED, 8, zlib.crc32(truth.encode())])
        sims, excl, by_r = [], [], {b: [0, 0] for b, _, _ in bins}
        for _ in range(pilots):
            inc, exc = recruit(truth, rng)
            sims.append(pilot_stats([person(ch) for ch, _ in inc]))
            excl.append(len(exc) / (len(exc) + len(inc)))
            for dropped, group in ((1, exc), (0, inc)):
                for _, shape in group:
                    for b, lo, hi in bins:
                        if "r" in shape and lo <= shape["r"] < hi:
                            by_r[b][0] += dropped
                            by_r[b][1] += 1
        ref["truths"][truth] = {**{k: quantiles([s[k] for s in sims]) for k in sims[0]}, "excluded": quantiles(excl)}
        if truth in rows:
            # every simulated pilot's rate, which the kappa rule reads its pilot against (kappa_belt)
            ref["truths"][truth]["lottery_rate_unflagged_draws"] = sorted(round(s["lottery_rate_unflagged"], 6) for s in sims)
        if any(n for _, n in by_r.values()):
            # the attention checks must not select on the metric (PILOT.md, inclusion rule)
            ref["truths"][truth]["excluded_by_r"] = {b: k / n if n else None for b, (k, n) in by_r.items()}
        if truth in V4_TRUTHS and fit_pilots:
            chs = [ch for _ in range(fit_pilots) for ch, _ in recruit(truth, rng)[0]]
            ref["fits"][truth] = geo_fits(chs, rng)
        print(truth, f"{time.time() - t0:.0f}s", flush=True)
    for row in rows:
        rng = np.random.default_rng([R.SEED, 9, zlib.crc32(row.encode())])
        # [flagged by the pilot's rule, flagged by the main study's rule, people]
        counts = {"trader": [0, 0, 0], "rank_one": [0, 0, 0]}
        while min(c[2] for c in counts.values()) < people:
            ch, shape = sim_choices(row + "S50", rng)      # half of them of rank one, the rest as in the row
            st = person(ch)
            if st["att_fail"] > ATT_MAX:
                continue
            c = counts["rank_one" if shape.get("rank_one") else "trader"]
            if c[2] < people:
                c[0] += st["self_hi"] >= FLAG_MIN
                c[1] += st["self_hi_R"] >= R.MAIN_FLAG_MIN
                c[2] += 1
        sp = R.spec(row)
        ref["rows"][row] = {"kappa": sp["kappa"], "target": sp["target"], "tpr": counts["rank_one"][0] / people,
                            "fpr": counts["trader"][0] / people, "tpr_main": counts["rank_one"][1] / people,
                            "fpr_main": counts["trader"][1] / people, "people": people}
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
    rules = {"pilot_n": PILOT_N, "flag_min": FLAG_MIN, "att_max": ATT_MAX, "main_flag_min": R.MAIN_FLAG_MIN}
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

def kappa_belt(rate, rows, ref, kappas, targets, grid=BELT_GRID):
    """The kappa the rule reads (revised 2026-11-03, PILOT.md): a confidence distribution from the lottery-choice
    rate at the ideal, over the pilot's unflagged people, read against the reference's simulated pilots.

    For each kappa row, G is the share of the row's simulated pilots whose rate is at or below the pilot's (ties
    count half), mixed between the two noise rows the pilot's agreement falls between, as power is. Higher kappa
    means fewer lotteries taken, so G rises with kappa. Its inverse at evenly spaced levels gives the draws: the
    draw at level 0.8 is an 80% upper limit for kappa by construction, with the rehearsal's own bias and spread
    in it. A level below G's lowest row lands just under the table, one above its highest just over it.
    The first pilot rehearsal read kappa from hier.py's posterior, which at pilot size sat 0.1 to 0.2 too low."""
    G = []
    for k in kappas:
        row = rows[str(k)]

        def F(t):
            d = ref["truths"][cell(k, t)].get("lottery_rate_unflagged_draws")
            if not d:
                raise Refusal("rules", f"the reference has no simulated lottery rates for row {cell(k, t)}")
            d = np.asarray(d)
            return float((np.sum(d < rate) + 0.5 * np.sum(d == rate)) / len(d))

        if row.get("targets"):
            (t0, t1), w = row["targets"], row["weight"]
            G.append((1 - w) * F(t0) + w * F(t1))
        else:
            G.append(F(targets[0]))           # noisier than every row: the rule stops before reading kappa
    # G must rise with kappa; the reference's sampling noise can break that where G is near 0 or 1
    G = np.maximum.accumulate(np.asarray(G))
    u = (np.arange(grid) + 0.5) / grid
    # a hair of slope through any flat stretch, so the inverse is defined there
    draws = np.interp(u, G + 1e-9 * np.arange(len(G)), kappas, left=kappas[0] - 0.01, right=kappas[-1] + 0.01)
    return [round(float(x), 4) for x in draws], [float(g) for g in G]


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
    bars = {**GATES, "included": f">= {PILOT_N}"}
    gates = {g: {"value": value[g], "bar": bars[g], "pass": bool(ok[g])} for g in GATES}

    st = pilot_stats(pp)
    flag = np.array([s["self_hi"] >= FLAG_MIN for s in pp])
    keep = [p for p, f in zip(included, flag) if not f]
    ag = np.array([s["agree"] for s, f in zip(pp, flag) if not f])
    brng = np.random.default_rng([R.SEED, 6, seed])
    boot = np.array([ag[brng.integers(0, len(ag), len(ag))].mean() for _ in range(BOOT)]) if len(ag) else np.array([np.nan])
    a20 = float(np.quantile(boot, 0.2))
    if len(keep) >= 2:
        kf = kappa_fit(np.stack([1 - choices(p)[CALIB_IDS] for p in keep]).astype(float), seed)
    else:
        kf = {"kappa_median": float("nan"), "q80": float("nan"), "fit": "none: fewer than two unflagged people"}
    # hier.py's population kappa is reported, as DESIGN.md's secondary analysis; the rule reads kappa_belt instead
    kf.pop("draws", None)
    kf.pop("draws_mean", None)

    # What the sample-size rule reads (PILOT.md, "Reading the pilot"). Per kappa row: where the pilot's 20th
    # percentile of agreement falls between the noise rows' simulated medians, and the upper limit of the self-only
    # share, converted with that row's flag rates at the same point.
    s = {"flagged": int(flag.sum()), "n": n, "share": frac(int(flag.sum()), n),
         "q_upper": wilson_upper(int(flag.sum()), n) if n else float("nan")}
    rows = {}
    for k in kappas:
        med = [ref["truths"][cell(k, t)]["agreement"]["q50"] for t in targets]
        if any(m1 >= m2 for m1, m2 in zip(med, med[1:])):
            raise Refusal("rules", f"the reference's agreement at kappa {k} does not rise as the rows get less noisy: {med}")
        rr = [ref["rows"][cell(k, t)] for t in targets]
        row = {"sim_agreement_median": dict(zip(map(str, targets), med)), "targets": None,
               "flag_rates": {str(t): [r["tpr"], r["fpr"]] for t, r in zip(targets, rr)}}
        if np.isfinite(a20) and a20 >= med[0]:
            i = max(j for j in range(len(targets) - 1) if med[j] <= a20)
            w = min(1.0, (a20 - med[i]) / (med[i + 1] - med[i]))      # at or above the least noisy row: that row
            tpr, fpr = ((1 - w) * rr[i][x] + w * rr[i + 1][x] for x in ("tpr", "fpr"))
            row.update(targets=[targets[i], targets[i + 1]], weight=float(w), tpr=float(tpr), fpr=float(fpr),
                       s_upper=float(np.clip((s["q_upper"] - fpr) / (tpr - fpr), 0, 1)))
        rows[str(k)] = row
    rate = st["lottery_rate_unflagged"]
    if np.isfinite(rate):
        draws, G = kappa_belt(rate, rows, ref, kappas, targets)
    else:
        draws, G = [], []
    rule = {"kappa_source": KAPPA_SOURCE, "kappa_draws": draws, "lottery_rate": rate,
            "belt": dict(zip(map(str, kappas), G)), "a20": a20, "q_upper": s["q_upper"], "rows": rows,
            # for the joint form (choose_n_joint): the agreement's bootstrap mean and spread, and the flagged count
            "a_mean": float(np.mean(boot)), "a_sd": float(np.std(boot)), "flagged": [s["flagged"], n]}

    targeting = {}
    for name in ("target_self", "target_charity", "target_risk_self", "target_risk_charity"):
        bar = max(ref["truths"][t][name]["q975"] for t in V4_TRUTHS)
        count = int(round(st[name] * n))
        targeting[name] = {"share": st[name], "count": count, "reference_q975_max": bar,
                           "fired": bool(st[name] > bar and count >= target_min())}

    # reported, not used by the rule: the lottery-choice rate at the ideal against the rows, at the noise row
    # nearest the pilot's and compared with the row nearest hier.py's posterior median
    k_hier = min(kappas, key=lambda k: abs(k - kf["kappa_median"])) if np.isfinite(kf["kappa_median"]) else None
    rh = rows[str(k_hier)] if k_hier is not None else {}
    t_row = (rh["targets"][int(round(rh["weight"]))] if rh.get("targets") else 1.5)
    lot = {k: ref["truths"][cell(k, t_row)]["lottery_rate"]["q50"] for k in kappas}
    lot_k = min(kappas, key=lambda k: abs(lot[k] - st["lottery_rate"]))
    reported = {"lottery_rate": st["lottery_rate"], "lottery_rate_by_row": {str(k): v for k, v in lot.items()},
                "lottery_kappa_row": lot_k, "hier_kappa_row": k_hier, "lottery_noise_row": t_row,
                "lottery_row_two_or_more_steps_from_hier": bool(k_hier is not None and
                                                                abs(kappas.index(lot_k) - kappas.index(k_hier)) >= 2),
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
           "kappa": kf, "rule": rule, "s": s, "targeting": targeting, "reported": reported,
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
    if (est.get("rule") or {}).get("kappa_source") != KAPPA_SOURCE:
        raise Refusal("kappa", f"{path}: the rule's kappa draws came from {(est.get('rule') or {}).get('kappa_source')!r}, "
                               f"not {KAPPA_SOURCE!r}")
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
    out = {"table_sha256": sha256(table_path), "estimates_sha256": sha256(path), **choose_n(est["rule"], tab)}
    dump(out, os.path.join(est_dir, "sample_size.json"))
    return out


def row_power(tab, kappa, row, n, population=MAIN_POPULATION):
    """Power at one kappa row and n: linear between the two noise rows the pilot's agreement falls between, and,
    within each, linear between the tabulated shares around the row's upper limit for the share. A share above
    the largest tabulated one, or a share cell the table lacks, counts as power 0: the table has shares only at
    rows that reached 0.80 by n = 240 with nobody of rank one (PILOT.md)."""
    key = "power" if population == "all" else "power_unflagged"
    shares, s = sorted(tab["shares"]), row["s_upper"]

    def at(t, sh):
        c = tab["cells"].get(cell(kappa, t, sh))
        if c is None:
            if not sh:
                raise Refusal("rules", f"the table lacks its row {cell(kappa, t)}")
            return 0.0
        return c[key][str(n)]

    def at_target(t):
        if s > shares[-1] + 1e-12:
            return 0.0
        j = max(i for i in range(len(shares)) if shares[i] <= s + 1e-12)
        if j == len(shares) - 1 or s <= shares[j] + 1e-12:
            return at(t, shares[j])
        w = (s - shares[j]) / (shares[j + 1] - shares[j])
        return (1 - w) * at(t, shares[j]) + w * at(t, shares[j + 1])

    (t0, t1), w = row["targets"], row["weight"]
    return (1 - w) * at_target(t0) + w * at_target(t1)


def choose_n(rule, tab, population=MAIN_POPULATION):
    """The sample-size rule (PILOT.md, "The sample size"), on what the pilot measured: for each n, the 20th
    percentile over the kappa posterior of the power at n, each draw taking the lower power of the two rows around
    it (above the table, 0; below it, the lowest row). n is the smallest whose percentile reaches 0.80."""
    kappas = sorted(tab["kappas"])
    out = {"population": population}
    if any(rule["rows"][str(k)].get("targets") is None for k in kappas):
        out["decision"] = "the pilot is noisier than every row, or has no agreement: extend the table with the same code"
        return out
    draws = np.asarray(rule["kappa_draws"], float)
    if not len(draws) or not np.all(np.isfinite(draws)):
        out["decision"] = "no kappa posterior: kappa could not be fitted"
        return out
    P = {k: np.array([row_power(tab, k, rule["rows"][str(k)], m, population) for m in MAIN_NS]) for k in kappas}
    idx = np.searchsorted(kappas, draws, side="right")          # kappas[i - 1] <= draw < kappas[i]
    per_draw = np.array([np.zeros(len(MAIN_NS)) if d > kappas[-1] + 1e-9 else P[kappas[0]] if i == 0 else
                         P[kappas[-1]] if i == len(kappas) else np.minimum(P[kappas[i - 1]], P[kappas[i]])
                         for d, i in zip(draws, idx)])
    q = np.quantile(per_draw, KAPPA_Q, axis=0, method="lower")
    out.update(curve=[(m, float(v)) for m, v in zip(MAIN_NS, q)],
               row_power={str(k): dict(zip(map(str, MAIN_NS), map(float, P[k]))) for k in kappas},
               draws_above_table=float(np.mean(draws > kappas[-1] + 1e-9)),
               draws_below_table=float(np.mean(draws < kappas[0])))
    out["n"] = next((m for m, v in out["curve"] if v >= TARGET_POWER), None)
    out["decision"] = (f"n = {out['n']}" if out["n"] else
                       "no n up to 240 reaches 0.80: the owner decides between 240, power stated, and stopping")
    return out


JOINT_DRAWS = 4000


def choose_n_joint(rule, tab, population=MAIN_POPULATION, draws=JOINT_DRAWS, seed=0):
    """EVALUATED 2026-11-04 AND NOT ADOPTED: the rule is `choose_n`. Kept so that the comparison can be rerun.
    In the third pilot rehearsal this form stopped only a few points less often than `choose_n` and chose an n
    without the power more often under one truth (PILOT.md, sequence step 4).

    The sample-size rule in a joint form: kappa, the noise and the self-only
    share are drawn together from their confidence distributions, and n is the smallest of 120 to 240 whose 20th
    percentile of power over the joint draws reaches 0.80. That is the probability statement the rule aims at.
    `choose_n` instead puts each of the three at its own one-sided 80% limit, which compounds.

    kappa: the belt's draws. Noise: the pilot's bootstrap distribution of mean agreement, normal with its mean and
    spread, placed between the noise rows at each kappa row as in `analyse`; a draw noisier than every row takes
    power 0. Share: the flagged share from a Jeffreys Beta on the flagged count, converted with the row's flag rates
    at the same point. Each draw takes the lower power of the two kappa rows around it, as in `choose_n`."""
    kappas, targets = sorted(tab["kappas"]), sorted(tab["targets"])
    shares = np.array(sorted(tab["shares"]))
    key = "power" if population == "all" else "power_unflagged"
    out = {"population": population, "form": "joint"}
    kd = np.asarray(rule["kappa_draws"], float)
    if not len(kd) or not np.isfinite(rule.get("a_mean", np.nan)):
        out["decision"] = "no kappa draws or no agreement: the rule cannot be applied"
        return out
    rng = np.random.default_rng([R.SEED, 12, seed])
    K = rng.choice(kd, draws)
    A = rng.normal(rule["a_mean"], rule["a_sd"], draws)
    F, n = rule["flagged"]
    Q = rng.beta(F + 0.5, n - F + 0.5, draws)
    by_row = {}
    for k in kappas:
        row = rule["rows"][str(k)]
        med = np.array([row["sim_agreement_median"][str(t)] for t in targets])
        fr = np.array([row["flag_rates"][str(t)] for t in targets])
        i = np.clip(np.searchsorted(med, A, side="right") - 1, 0, len(targets) - 2)
        w = np.clip((A - med[i]) / (med[i + 1] - med[i]), 0.0, 1.0)
        tpr = (1 - w) * fr[i, 0] + w * fr[i + 1, 0]
        fpr = (1 - w) * fr[i, 1] + w * fr[i + 1, 1]
        S = np.clip((Q - fpr) / (tpr - fpr), 0.0, 1.0)
        # power[t][share][n]; a missing share cell is 0, a missing share-0 row a refusal, as in row_power
        P = np.zeros((len(targets), len(shares), len(MAIN_NS)))
        for a, t in enumerate(targets):
            for b, sh in enumerate(shares):
                c = tab["cells"].get(cell(k, t, sh))
                if c is None and not sh:
                    raise Refusal("rules", f"the table lacks its row {cell(k, t)}")
                if c is not None:
                    P[a, b] = [c[key][str(m)] for m in MAIN_NS]
        at = np.zeros((draws, len(MAIN_NS)))
        cols = np.arange(draws)
        for m in range(len(MAIN_NS)):
            Pt = np.stack([np.interp(S, shares, P[a, :, m]) for a in range(len(targets))])
            at[:, m] = (1 - w) * Pt[i, cols] + w * Pt[i + 1, cols]
        at[S > shares[-1] + 1e-12] = 0.0
        at[A < med[0]] = 0.0
        by_row[k] = at
    # each draw: the lower power of the two kappa rows around it; below the table the lowest row, above it 0
    stack = np.stack([by_row[k] for k in kappas])
    idx = np.searchsorted(kappas, K, side="right")
    lo, hi, cols = np.clip(idx - 1, 0, len(kappas) - 1), np.clip(idx, 0, len(kappas) - 1), np.arange(draws)
    per = np.minimum(stack[lo, cols], stack[hi, cols])
    per[K > kappas[-1] + 1e-9] = 0.0
    q = np.quantile(per, KAPPA_Q, axis=0, method="lower")
    out["curve"] = [(m, float(v)) for m, v in zip(MAIN_NS, q)]
    out["n"] = next((m for m, v in out["curve"] if v >= TARGET_POWER), None)
    out["decision"] = (f"n = {out['n']}" if out["n"] else
                       "no n up to 240 reaches 0.80: the owner decides between 240, power stated, and stopping")
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


def synthetic_table(path, power=None):
    """A table with the real one's shape and made-up power, for the self-test only: power(kappa, target, share, n),
    by default falling with kappa and with the share, and less with the share over unflagged people."""
    ns, shares = list(R.NS5), [0.0, 0.2, 0.4, 0.6]
    power = power or (lambda k, t, s, m, pop: float(1 - np.exp(-m * (1 - s) ** (2 if pop == "all" else 1)
                                                                   * t / 1.5 / (40.0 * k ** 3))))
    cells = {}
    for row in table_rows():
        sp = R.spec(row)
        for s in shares:
            cells[cell(sp["kappa"], sp["target"], s)] = {
                "spec": {**sp, "share": s},
                **{key: {str(m): power(sp["kappa"], sp["target"], s, m, pop) for m in ns}
                   for key, pop in (("power", "all"), ("power_unflagged", "unflagged"))}}
    dump({"format": TABLE_FORMAT, "source": "synthetic, for the self-test only", "ns": ns, "shares": shares,
          "kappas": sorted({c["spec"]["kappa"] for c in cells.values()}),
          "targets": sorted({c["spec"]["target"] for c in cells.values()}), "cells": cells}, path)


def self_test(d, use_hier=False):
    os.makedirs(d, exist_ok=True)
    stub = lambda Y, seed: {"kappa_median": 1.1, "lo": 0.9, "hi": 1.3, "q80": 1.2, "fit": "stub (self-test)",  # noqa: E731
                            "draws": [float(x) for x in np.linspace(0.95, 1.25, 500)], "people": int(Y.shape[0])}
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
    check(f"simulated pilot: {PILOT_N} included, recruited until they qualify", est["counts"]["included"] == PILOT_N,
          f"counts {est['counts']}, gates failed {[g for g, v in est['gates'].items() if not v['pass']]}, "
          f"agreement q20 {est['rule']['a20']:.3f}, s {est['s']}")

    # the kappa rule on made-up rows: the pilot at the target-1.5 rows, nobody of rank one
    flat = {"kappa_draws": [float(x) for x in np.linspace(0.9, 1.3, 500)], "a20": 0.7, "q_upper": 0.0,
            "rows": {str(k): {"targets": [1.0, 1.5], "weight": 1.0, "s_upper": 0.0} for k in load(tab)["kappas"]}}
    t_syn = load(tab)

    def old_rule(rule, t):
        """Version 5's rule: the row above the posterior's 80th percentile, nobody of rank one."""
        k = next(k for k in sorted(t["kappas"]) if k >= np.quantile(rule["kappa_draws"], 0.8) - 1e-9)
        return next((m for m in MAIN_NS if t["cells"][cell(k, 1.5)]["power"][str(m)] >= TARGET_POWER), None)

    new, old = choose_n(flat, t_syn)["n"], old_rule(flat, t_syn)
    check("kappa rule: equals rounding the 80th percentile up when power falls with kappa", new == old and new is not None,
          f"n {new} against {old}")
    bumped = os.path.join(d, "table_bumped.json")
    synthetic_table(bumped, power=lambda k, t, s, m, pop: float(1 - np.exp(-m / (40.0 * (1.25 if k == 2.0 else k) ** 3))))
    t_b = load(bumped)
    high = {**flat, "kappa_draws": [float(x) for x in np.linspace(1.80, 1.99, 500)]}
    new, old = choose_n(high, t_b)["n"], old_rule(high, t_b)
    check("kappa rule: stays cautious when power rises again at kappa 2 (rounding up would not)",
          old is not None and (new is None or new > old), f"n {new} against rounding up's {old}")
    mid = {**flat, "rows": {k: {**v, "s_upper": 0.3} for k, v in flat["rows"].items()}}
    p3 = row_power(t_syn, 1.0, mid["rows"]["1.0"], 120, "all")
    p2, p4 = (t_syn["cells"][cell(1.0, 1.5, sh)]["power"]["120"] for sh in (0.2, 0.4))
    check("share: power at a share of 0.3 lies between the 0.2 and 0.4 cells", p4 < p3 < p2, f"{p4:.3f} < {p3:.3f} < {p2:.3f}")
    # the belt: a pilot whose rate is the kappa = 1 row's median, read at the target-1.5 rows
    rref = load(ref)
    med1 = float(np.median(rref["truths"][cell(1.0, 1.5)]["lottery_rate_unflagged_draws"]))
    at15 = {str(k): {"targets": [1.0, 1.5], "weight": 1.0} for k in t_syn["kappas"]}
    bd, _ = kappa_belt(med1, at15, rref, sorted(t_syn["kappas"]), sorted(t_syn["targets"]))
    check("belt: at the kappa = 1 row's median rate, kappa's confidence distribution is centred near 1",
          abs(float(np.median(bd)) - 1.0) <= 0.15, f"median {np.median(bd):.3f}, 80th percentile {np.quantile(bd, 0.8):.3f}")
    refused("size: no estimates at all", "missing", lambda: size(est_dir, tab))
    shutil.copy(written, os.path.join(est_dir, "pilot_estimates.json"))
    refused("size: a simulated file exactly where the rule looks is refused for provenance", "provenance",
            lambda: size(est_dir, tab))

    def forged(**changes):
        """The simulated estimates relabelled as human with every gate passed and no rule fired, then one change,
        so that each refusal below can only come from the guard it tests."""
        e = load(written)
        e.update(source="human", gates={g: {**v, "pass": True} for g, v in e["gates"].items()},
                 targeting={k: {**v, "fired": False} for k, v in e["targeting"].items()})
        for k, v in changes.items():
            e[k] = v(e)
        dump(e, os.path.join(est_dir, "pilot_estimates.json"))

    forged(rule=lambda e: {**e["rule"], "kappa_source": "hier.py posterior"})
    refused("size: kappa draws not from the sealed belt are refused", "kappa", lambda: size(est_dir, tab))
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


def no_hier(Y, seed):
    """The rehearsal's stand-in for hier.py, whose kappa the rule no longer reads (kappa_belt): reported as absent."""
    return {"kappa_median": float("nan"), "q80": float("nan"), "fit": "skipped in the rehearsal", "people": int(Y.shape[0])}


def rehearse(truth, pilots, ref_path, table_path, out, seed=0, kappa_fit=hier_kappa):
    """Simulated pilots under one truth through export, split and analysis (with hier.py). Per pilot: what was
    planted, and what the rule reads, as the estimates file holds it (the kappa draws, the agreement, the share's
    upper limits). `summarise` applies the rule with the power table, as `size` does with human estimates, which
    `size` itself refuses for simulated ones. The table given here serves only analyse's check that the
    reference covers its rows, so the pilots can run before the table is finished."""
    rng = np.random.default_rng([R.SEED, 7, zlib.crc32(truth.encode()), seed])
    rows, t0 = [], time.time()
    for k in range(pilots):
        with tempfile.TemporaryDirectory() as d:
            export, info = simulated_export(truth, rng)
            dump(export, os.path.join(d, "export.json"))
            split_pilot.split(os.path.join(d, "export.json"), os.path.join(d, "split"))
            est, _ = analyse(os.path.join(d, "split", "readable.json"), ref_path, table_path, os.path.join(d, "est"),
                             kappa_fit=kappa_fit, seed=seed * 100003 + k)
        rule = est["rule"]
        rows.append({"planted": info, "kappa": est["kappa"], "s": est["s"], "agreement": est["agreement"],
                     "rule": {**rule, "kappa_draws": [round(x, 4) for x in rule["kappa_draws"]]},
                     "gates_pass": est["gates_pass"], "targeting": {n: v["fired"] for n, v in est["targeting"].items()}})
        limit = float(np.quantile(rule["kappa_draws"], 0.8)) if rule["kappa_draws"] else float("nan")
        print(k, round(limit, 3), round(rule["a20"], 3), round(rule["q_upper"], 3), f"{time.time() - t0:.0f}s", flush=True)
    dump({"truth": truth, "spec": R.spec(truth), "seed": seed, "pilots": rows, "code_sha256": code_hashes(),
          "reference_sha256": sha256(ref_path), "shape_table_sha256": sha256(table_path), "seconds": time.time() - t0}, out)


# Bars for the pilot rehearsal (PILOT.md, sequence step 4), set 2026-11-03 before it ran. Each quantity enters the rule
# at a one-sided 80% limit, so each limit should hold in about 80% of pilots; the bar allows sampling error over 100.
COVER_MIN = 0.70
POWER_OK_MIN = 0.80          # of the pilots that choose an n, the share whose n has true power of at least 0.80
# Restated 2026-11-04, before the fourth run: of ALL pilots, at most this share may choose an n at which the truth's
# power is below 0.80. The conditional form above counts any choice under a truth no n reaches as a total failure,
# however rarely the rule makes it (run 3: 2 pilots of 100 chose an n under such a truth, and 98 stopped).
BAD_CHOICE_MAX = 0.20


def true_power(tab, truth, n, population):
    """The table's power for a truth's own cell at n, linear between the tabulated shares at its row. A row the table
    has no share cells for gives its power with nobody of rank one, an upper bound, and says so."""
    sp = R.spec(truth)
    key = "power" if population == "all" else "power_unflagged"
    have = sorted(sh for sh in tab["shares"] if cell(sp["kappa"], sp["target"], sh) in tab["cells"])
    pw = lambda sh: tab["cells"][cell(sp["kappa"], sp["target"], sh)][key][str(n)]  # noqa: E731
    s = sp["share"]
    if len(have) == 1 or s > have[-1]:
        return (pw(have[0]) if len(have) == 1 else 0.0), len(have) == 1
    return float(np.interp(s, have, [pw(sh) for sh in have])), False


def summarise(out, paths, ref_path, table_path):
    ref, tab = load_reference(ref_path), load_table(table_path)
    by, seen = {}, set()
    for p in paths:
        r = load(p)
        if r["reference_sha256"] != sha256(ref_path):
            raise Refusal("rules", f"{p} was run against another reference")
        if (r["truth"], r["seed"]) in seen:
            raise Refusal("format", f"{p} repeats truth {r['truth']} seed {r['seed']}")
        seen.add((r["truth"], r["seed"]))
        by.setdefault(r["truth"], []).extend(r["pilots"])
    kappas, targets = sorted(tab["kappas"]), sorted(tab["targets"])

    def joint_inputs(q):
        """The joint form's inputs, for a pilot analysed before `analyse` stored them: the agreement's spread from
        its mean and 20th percentile, the flagged count, and the rows' flag rates from the reference."""
        rule = dict(q["rule"])
        if "a_mean" not in rule:
            a = q["agreement"]
            rule.update(a_mean=a["mean"], a_sd=max(1e-6, (a["mean"] - a["q20"]) / Z80),
                        flagged=[q["s"]["flagged"], q["s"]["n"]])
        rule["rows"] = {str(k): {**rule["rows"][str(k)],
                                 "sim_agreement_median": {str(t): ref["truths"][cell(k, t)]["agreement"]["q50"] for t in targets},
                                 "flag_rates": {str(t): [ref["rows"][cell(k, t)]["tpr"], ref["rows"][cell(k, t)]["fpr"]]
                                                for t in targets}} for k in kappas}
        return rule

    for pp in by.values():          # the rule, with the table, as `size` applies it to human estimates
        for j, q in enumerate(pp):
            q["choice"] = {pop: choose_n(q["rule"], tab, pop) for pop in ("all", "unflagged")}
            jr = joint_inputs(q)
            q["choice_joint"] = {pop: choose_n_joint(jr, tab, pop, seed=j) for pop in ("all", "unflagged")}
    res = {"table_sha256": sha256(table_path), "reference_sha256": sha256(ref_path), "runs": len(paths), "bars": {
        "cover_min": COVER_MIN, "power_ok_min": POWER_OK_MIN}, "truths": {}}
    for truth, pp in sorted(by.items()):
        sp = R.spec(truth)
        k, t, s = sp["kappa"], sp["target"], sp["share"]
        med = ref["truths"][cell(k, t)]["agreement"]["q50"]
        limit = [float(np.quantile(q["rule"]["kappa_draws"], 0.8)) if q["rule"]["kappa_draws"] else float("nan") for q in pp]
        hq = [q["kappa"].get("q80", float("nan")) for q in pp]
        r = {"pilots": len(pp), "kappa": k, "target": t, "share": s,
             # the 80% upper limit the rule reads for kappa (the belt's draw at level 0.8)
             "kappa_limit_covers": float(np.mean([x >= k for x in limit])),
             "kappa_limit_median": float(np.nanmedian(limit)),
             "hier_q80_covers": float(np.mean([x >= k for x in hq])) if np.isfinite(hq).any() else None,
             "agreement_q20_at_or_below_truth": float(np.mean([q["rule"]["a20"] <= med for q in pp])),
             "s_upper_covers": float(np.mean([(q["rule"]["rows"][str(k)].get("s_upper") or 0) >= s for q in pp])),
             "gates_pass": float(np.mean([q["gates_pass"] for q in pp])),
             "targeting_fired": float(np.mean([any(q["targeting"].values()) for q in pp]))}
        for pop in ("all", "unflagged"):
            tp = {m: true_power(tab, truth, m, pop) for m in MAIN_NS}
            first = next((m for m in MAIN_NS if tp[m][0] >= TARGET_POWER), None)    # the n the truth needs
            for form, ck in (("", "choice"), ("_joint", "choice_joint")):
                ns = [q[ck][pop].get("n") for q in pp]
                chosen = [m for m in ns if m]
                x = {"true_power": {str(m): v for m, (v, _) in tp.items()}, "true_power_is_upper_bound": tp[240][1],
                     "truth_needs": first, "n": {str(m): ns.count(m) for m in MAIN_NS} | {"none": ns.count(None)},
                     "chosen_power_ok": float(np.mean([tp[m][0] >= TARGET_POWER for m in chosen])) if chosen else None,
                     # the cost of caution: how often the rule stops although some n up to 240 has the power
                     "stops_when_powered": float(np.mean([m is None for m in ns])) if first else None,
                     # the restated bar: pilots that choose an n without the power, out of all pilots
                     "bad_choice_rate": float(np.mean([m is not None and tp[m][0] < TARGET_POWER for m in ns]))}
                x["pass_conditional"] = x["chosen_power_ok"] is None or x["chosen_power_ok"] >= POWER_OK_MIN
                x["pass"] = x["bad_choice_rate"] <= BAD_CHOICE_MAX
                r[pop + form] = x
        r["covers_pass"] = all(r[x] >= COVER_MIN for x in ("kappa_limit_covers", "agreement_q20_at_or_below_truth"))
        if s:
            r["covers_pass"] = r["covers_pass"] and r["s_upper_covers"] >= COVER_MIN
        res["truths"][truth] = r
        print(truth, json.dumps({x: r[x] for x in ("kappa_limit_covers", "agreement_q20_at_or_below_truth",
                                                   "s_upper_covers", "covers_pass")}), flush=True)
        for key in ("all", "unflagged", "all_joint", "unflagged_joint"):
            x = r[key]
            print(f"   {key:16s} truth needs n {x['truth_needs']}; chosen {x['n']}; chosen n powered "
                  f"{x['chosen_power_ok']}; stops when powered {x['stops_when_powered']}; bad choices "
                  f"{x['bad_choice_rate']:.2f}; pass {x['pass']} (conditional form {x['pass_conditional']})", flush=True)
    dump(res, out)
    return res


def main():
    global PILOT_N
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
    a.add_argument("--no-hier", action="store_true", help="skip hier.py, whose kappa the rule no longer reads")
    a = sub.add_parser("summarise")
    a.add_argument("out")
    a.add_argument("runs", nargs="+")
    a.add_argument("--reference", required=True)
    a.add_argument("--table", required=True)
    for name in ("reference", "self-test", "rehearse", "summarise"):
        sub.choices[name].add_argument("--pilot-n", type=int, default=None,
                                       help=f"simulated pilots of this many included people instead of {PILOT_N}")
    args = ap.parse_args()
    if getattr(args, "pilot_n", None):
        PILOT_N = args.pilot_n
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
        elif args.cmd == "summarise":
            summarise(args.out, args.runs, args.reference, args.table)
        else:
            rehearse(args.truth, args.pilots, args.reference, args.table, args.out, args.seed,
                     kappa_fit=no_hier if args.no_hier else hier_kappa)
    except Refusal as e:
        print(f"REFUSED ({e.kind}): {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
