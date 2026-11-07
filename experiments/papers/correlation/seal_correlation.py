#!/usr/bin/env python3
"""Hash the prereg-correlation-v1 bundle, in the format this repository already uses (PILOT.md, sequence step 6).

A file is in the bundle if changing it would change what the study concludes: the design and the protocol, the
stimuli, the models and the tests, the pilot's split, gates and sample-size rule, the table and the reference that
rule reads, and every file the participant's browser loads, with the scripts that write the page and read what it
saves. The round trip and its record are in too, so the seal shows what was tested.

Out, though in the tagged commit:
  instrument/config.js     the deployment's settings, filled in at launch (instrument/README.md)
  instrument/README.md     how to deploy the page, and what to do after the study
  instrument_screens.py    pictures of the screens, for the ethics application
  REHEARSAL.md, results/   the record the table was computed from, and the rehearsal's runs
  the diagnostics          kappa_*.py, diag_kappa.py, mf2_check.py, pilot_decompose.py, payout.py,
                           aggregate_rehearsal.py and submit_nrp.py

Two checks run with the hashes, and --write refuses to write if either fails. MANIFEST.json must give the page's
files as they are, and the round trip's record must name this build of the page, this stimulus hash and these
files' hashes. The seal cannot then cover a page or code that the round trip did not run.

    python seal_correlation.py           # verify against the recorded seal
    python seal_correlation.py --write   # write it
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEAL = os.path.join(HERE, "prereg-correlation-v1.sha256")

BUNDLE = [
    "DESIGN.md",                               # the design of record: models, tests, margin, inclusion, sample size
    "PILOT.md",                                # the protocol: the pilot's gates, the rule that reads it, the sequence
    "stimuli.py",                              # every trial, its role, and each participant's order
    "models.py",                               # every model the tests fit
    "rehearsal.py",                            # the per-person fits, the self-only flag, H1 to H4, MF1, MF2, SH1 to SH3
    "hier.py",                                 # the population kappa
    "power_table.py",                          # the power table from the rehearsal's runs
    "split_pilot.py",                          # the export into the readable and the sealed file
    "pilot_analysis.py",                       # the pilot's gates, the limit for kappa and the sample-size rule
    "results/power_table_v6b.json",            # the table the rule reads
    "results/pilot_reference_n120_self.json",  # the simulated pilots the pilot is read against
    "build_instrument.py",                     # writes stimuli.js and MANIFEST.json from stimuli.py
    "export_pilot.py",                         # the saved files into the export, the bonuses and the donations
    "instrument/index.html",                   # the page, in the order index.html loads it
    "instrument/style.css",
    "instrument/stimuli.js",
    "instrument/order.js",
    "instrument/text.js",
    "instrument/task.js",
    "instrument/MANIFEST.json",                # the page's hashes and its build
    "instrument_roundtrip.py",                 # the round trip of sequence step 3
    "results/instrument_roundtrip.json",       # its record
]
PAGE = ("index.html", "style.css", "stimuli.js", "order.js", "text.js", "task.js")  # build_instrument.SOURCES

META = {
    "prereg": "prereg-correlation-v1",
    "title": "Cross-attribute risk attitudes: a test of a full Mahalanobis metric with late contraction",
    "author": "Andrew H. Bond, San Jose State University",
    "frozen_predictions": "DESIGN.md, 'Analysis': H1, H2 and H3, whose conjunction is the claim, at a margin of "
                          "0.005 nats per trial; H4; the model-free checks; the population kappa; the secondary "
                          "claim, SH1 and SH2 together. The inclusion and sample-size rules are in DESIGN.md and "
                          "PILOT.md, and the pilot's gates and the rule that reads it in PILOT.md and "
                          "pilot_analysis.py.",
    "data": "NONE COLLECTED. Neither the pilot nor the main study has run. The design, the table and the "
            "sample-size rule are sealed BEFORE the pilot, so nothing the pilot measures can reach the margin, a "
            "model, the claim or the sample size except through a rule written in advance.",
    "outside_the_bundle": "In the tagged commit but not sealed: instrument/config.js (the deployment's settings), "
                          "instrument/README.md, instrument_screens.py, REHEARSAL.md, the rehearsal's results and "
                          "the diagnostics.",
    "hash_note": "sha256 of each file with CRLF normalized to LF; combined = sha256 over the concatenated "
                 "component hex digests in bundle_files order",
}


def digest(rel):
    path = os.path.join(HERE, rel)
    if not os.path.exists(path):
        raise SystemExit(f"bundle file missing: {rel}")
    with open(path, "rb") as f:
        return hashlib.sha256(f.read().replace(b"\r\n", b"\n")).hexdigest()


def load(rel):
    with open(os.path.join(HERE, rel), encoding="utf-8") as f:
        return json.load(f)


def compute(frozen_at):
    files = {rel: digest(rel) for rel in BUNDLE}
    combined = hashlib.sha256("".join(files[r] for r in BUNDLE).encode("ascii")).hexdigest()
    man = load("instrument/MANIFEST.json")
    return {**META, "frozen_at": frozen_at,
            "instrument": {"build": man["build"], "stimuli_sha256": man["stimuli_sha256"]},
            "bundle_files": BUNDLE, "files": files, "combined_sha256": combined}


def checks(files):
    """What the hashes alone cannot say: that the manifest is the page's, and that the round trip ran this page and
    this code. The round trip hashed its files as they were on Atlas, with LF line endings."""
    man = load("instrument/MANIFEST.json")
    rt = load("results/instrument_roundtrip.json")
    page = {n: files["instrument/" + n] for n in PAGE}
    build = hashlib.sha256("".join(f"{n}:{page[n]}\n" for n in PAGE).encode()).hexdigest()
    failed = [name for name, c in rt["checks"].items() if not c["pass"]]
    return [
        ("MANIFEST.json gives the page's files and their build", man["files"] == page and man["build"] == build),
        (f"the round trip passed {len(rt['checks']) - len(failed)} of {len(rt['checks'])} checks",
         rt["pass"] is True and not failed),
        ("the round trip ran this build of the page, on these stimuli",
         rt["build"] == man["build"] and rt["stimuli_sha256"] == man["stimuli_sha256"]),
        (f"the round trip ran these files: {', '.join(sorted(rt['code_sha256']))}",
         all(files.get(n) == h for n, h in rt["code_sha256"].items())),
    ]


def main():
    if "--write" in sys.argv:
        frozen = datetime.date.today().isoformat()
        if os.path.exists(SEAL):
            frozen = load(os.path.basename(SEAL)).get("frozen_at", frozen)
            print("seal exists, keeping frozen_at", frozen)
        cur = compute(frozen)
        bad = [name for name, ok in checks(cur["files"]) if not ok]
        if bad:
            raise SystemExit("not written: " + "; ".join(bad))
        with open(SEAL, "w", encoding="utf-8", newline="\n") as f:
            json.dump(cur, f, indent=2)
            f.write("\n")
        print("written", os.path.basename(SEAL))
        print("  combined sha256", cur["combined_sha256"])
        for rel in BUNDLE:
            print(f"    {rel:<42} {cur['files'][rel][:16]}")
        return 0

    if not os.path.exists(SEAL):
        print("no seal recorded. run with --write")
        return 1
    rec = load(os.path.basename(SEAL))
    cur = compute(rec["frozen_at"])
    print(f"SEAL CHECK, {rec['prereg']}, frozen {rec['frozen_at']}")
    print("  recorded ", rec["combined_sha256"])
    print("  computed ", cur["combined_sha256"])
    ok = rec["bundle_files"] == BUNDLE and rec["combined_sha256"] == cur["combined_sha256"]
    if rec["bundle_files"] != BUNDLE:
        print("  the bundle's list differs from the seal's")
    for rel in BUNDLE:
        same = rec["files"].get(rel) == cur["files"][rel]
        ok &= same
        print(f"    {rel:<42} {'ok' if same else 'CHANGED SINCE THE SEAL'}")
    for name, good in checks(cur["files"]):
        ok &= good
        print(f"  {'ok' if good else 'FAILED'}: {name}")
    print("  SEAL INTACT" if ok else "  SEAL BROKEN")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
