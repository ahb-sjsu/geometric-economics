#!/usr/bin/env python3
"""Parse Gluth, Spektor and Rieskamp 2018 (eLife 7:e39659; OSF 8r4fh), held back for the sealed menus
test. Writes covariates and outcomes to SEPARATE files, so every check before the seal reads stimuli
only. Personal header fields (age, sex, major) are not read into any output.

Each row is one trial: a high-value option HV and a low-value option LV, both choosable, and on
distractor trials a third option D that is shown but cannot be chosen. Magnitude in CHF, probability
as recorded. Files under `incomplete/` are excluded (the authors' own folder for aborted sessions).

Response codes (`rsp`), established before the seal without reading any preference statistic:
    0 = HV, 1 = LV   on every row with code 0 the reward equals HV's drawn outcome, with code 1 LV's
    2 = D            occurs only on rows where D is shown; pays nothing
    9, 10            occur with and without D; pay nothing: an empty quadrant or no response
Block 0 is training (variable length, to criterion); block 1 is the experiment: 412 rows per
participant in Experiments 1-3 and 300 in Experiment 4, as the paper states.

Buckets, which must sum to the data rows read:
    kept               block 1, response 0, 1 or 2
    training           block 0
    non_choice         block 1, response 9 or 10
    unparsed           block 1, stimulus fields missing or not numeric, or another response code

    python gluth_rows.py SEALED_DIR OUT_DIR     # on Atlas
"""
from __future__ import annotations

import collections
import io
import json
import os
import sys
import zipfile

import numpy as np
import pandas as pd

EXPS = {"exp1": "exp1_data.zip", "exp2": "exp2_data.zip", "exp3": "exp3_data.zip", "exp4": "exp4_data.zip"}
STIM = ["hv_mag", "hv_prob", "lv_mag", "lv_prob", "d_mag", "d_prob", "hv_pos", "lv_pos", "d_pos"]
CODES = {0: "HV", 1: "LV", 2: "D"}


def num(x) -> float:
    """A numeric field, or NaN when it is empty or not a number (binary trials have no D)."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return np.nan


def read_xpd(raw: bytes) -> pd.DataFrame:
    text = raw.decode("cp1252")
    body = "\n".join(l for l in text.splitlines() if not l.startswith("#"))
    return pd.read_csv(io.StringIO(body))


def parse(sealed, out):
    cov, outc, acc = collections.defaultdict(list), collections.defaultdict(list), {}
    for exp, zname in EXPS.items():
        z = zipfile.ZipFile(os.path.join(sealed, zname))
        names = [n for n in z.namelist() if n.endswith(".xpd") and "/incomplete/" not in n]
        b = collections.Counter()
        n_rows = 0
        for n in sorted(names):
            d = read_xpd(z.read(n))
            n_rows += len(d)
            for r in d.itertuples(index=False):
                if num(r.block) == 0:
                    b["training"] += 1
                    continue
                s = [num(getattr(r, c)) for c in STIM]
                rsp = num(r.rsp)
                if any(np.isnan(s[i]) for i in (0, 1, 2, 3, 6, 7)) or rsp not in CODES and rsp not in (9, 10):
                    b["unparsed"] += 1
                    continue
                if rsp in (9, 10):
                    b["non_choice"] += 1
                    continue
                if s[8] == -99:                                   # no D on this trial
                    s[4] = s[5] = s[8] = np.nan
                hit = [CODES[rsp]]
                b["kept"] += 1
                cov["exp"].append(exp)
                cov["subject"].append(f"{exp}-{r.subject_id}")
                cov["trial_type"].append(str(r.trial_type))
                cov["group"].append(str(r.between))
                for c, v in zip(STIM, s):
                    cov[c].append(v)
                outc["choice"].append(hit[0])
                outc["rt"].append(float(r.rt))
        assert sum(b.values()) == n_rows, (exp, dict(b), n_rows)
        acc[exp] = {"files": len(names), "rows": n_rows, "buckets": dict(b)}
    os.makedirs(out, exist_ok=True)
    np.savez_compressed(os.path.join(out, "gluth_covariates.npz"), **{k: np.array(v) for k, v in cov.items()})
    np.savez_compressed(os.path.join(out, "gluth_outcome.npz"), **{k: np.array(v) for k, v in outc.items()})
    json.dump(acc, open(os.path.join(out, "gluth_accounting.json"), "w"), indent=1)
    print(json.dumps(acc, indent=1))


if __name__ == "__main__":
    parse(sys.argv[1], sys.argv[2])
