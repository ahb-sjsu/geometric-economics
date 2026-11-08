#!/usr/bin/env python3
"""The seal of sequence step 10 (PILOT.md): the n the pilot chose, recorded under a second signed tag before
recruitment (DESIGN.md, "Stages", 4), and with it the main study's analysis (MAIN.md).

    python seal_main.py                                  # verify the recorded seal
    python seal_main.py --write --estimates DIR [--publish-estimates] [--owner-n 240 --owner-said TEXT]

--write is for step 10, after the pilot has been split and analysed (step 9), and with the owner's OK. It writes
prereg-correlation-v1-main.sha256 in the format of prereg-correlation-v1.sha256, and refuses unless
  - the design's seal, prereg-correlation-v1, is intact (seal_correlation.py);
  - pilot_analysis.size takes DIR/pilot_estimates.json against the sealed table: estimates from people, every gate
    passed, no targeting rule fired, kappa from the sealed belt and the agreement read at the sealed percentile. It
    writes DIR/sample_size.json, the row and n;
  - the rule gives an n, or, when no n reaches 0.80, the owner has decided to run at 240 with the power stated
    (PILOT.md, "The sample size"): --owner-n 240, with the owner's words, which the seal records;
  - results/main_selftest.json passed every check on this main_analysis.py and the code it reads, and
    results/main_rehearsal.json passed its bars on the same analysis code.
It copies DIR/sample_size.json into results/. pilot_estimates.json goes in too with --publish-estimates, which needs the
owner's OK (PILOT.md, "Data and provenance"); either way its hash is recorded, as step 10 asks.

main_analysis.py reads this seal before it grades human data, and refuses unless the seal names it and both seals are
intact (verify_record). The tool itself, like seal_correlation.py, is not in the bundle.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import seal_correlation as design_seal  # noqa: E402

SEAL = os.path.join(HERE, "prereg-correlation-v1-main.sha256")
PREREG = "prereg-correlation-v1-main"
TABLE = "results/power_table_v6b.json"            # the sealed table, which pilot_analysis.size reads
SELFTEST = "results/main_selftest.json"
REHEARSAL = "results/main_rehearsal.json"
SAMPLE_SIZE = "results/sample_size.json"
ESTIMATES = "results/pilot_estimates.json"
BUNDLE = [
    "MAIN.md",                  # the main study's analysis: who counts, the fits, the tests, the guards
    "main_analysis.py",         # the runner: export, grade
    SELFTEST,                   # its self-test, on this code
    REHEARSAL,                  # its rehearsal: how often the claim passes through it, against bars set before
    SAMPLE_SIZE,                # the row and n, from pilot_analysis.size
]
# the files main_analysis.py's rehearsal runs (its record must name these as they are now)
REHEARSAL_CODE = ("main_analysis.py", "rehearsal.py", "models.py", "stimuli.py", "pilot_analysis.py", "export_pilot.py",
                  "split_pilot.py", "build_instrument.py")
META = {
    "title": design_seal.META["title"],
    "author": design_seal.META["author"],
    "step": "PILOT.md, sequence step 10: the row and n by the sealed rule, recorded under a signed tag with the hash of "
            "pilot_estimates.json; with them the main study's analysis, main_analysis.py (MAIN.md).",
    "data": "The pilot only, through split_pilot.py and pilot_analysis.py: its readable file read, its sealed file "
            "unopened. The main study NOT STARTED: nobody recruited to it.",
    "hash_note": design_seal.META["hash_note"],
}
digest = design_seal.digest


def load(rel):
    with open(os.path.join(HERE, rel), encoding="utf-8") as f:
        return json.load(f)


def raw_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def combined(files, bundle):
    return hashlib.sha256("".join(files.get(r, "") for r in bundle).encode("ascii")).hexdigest()


def design_state():
    """The design's seal, and what in it no longer holds (an empty list when it is intact)."""
    rec = design_seal.load(os.path.basename(design_seal.SEAL))
    try:
        cur = design_seal.compute(rec["frozen_at"])
    except SystemExit as e:
        return rec, [str(e)]
    bad = [rel for rel in design_seal.BUNDLE if rec["files"].get(rel) != cur["files"][rel]]
    if rec["bundle_files"] != design_seal.BUNDLE:
        bad.append("its bundle list")
    if rec["combined_sha256"] != cur["combined_sha256"]:
        bad.append("its combined hash")
    bad += [name for name, ok in design_seal.checks(cur["files"]) if not ok]
    return rec, bad


def stale(record, names):
    """The files a test record names whose hashes are not those it ran with."""
    rec = record.get("code_sha256") or {}
    out = []
    for name in names:
        try:
            if rec.get(name) != digest(name):
                out.append(name)
        except SystemExit:
            out.append(name)
    return out


def tested_state():
    """Whether the self-test and the rehearsal passed on the code as it is now: a list of what fails."""
    bad = []
    for rel in (SELFTEST, REHEARSAL):
        if not os.path.exists(os.path.join(HERE, rel)):
            bad.append(f"{rel} is missing")
    if bad:
        return bad
    st, rh = load(SELFTEST), load(REHEARSAL)
    if st.get("pass") is not True:
        bad.append(f"{SELFTEST} did not pass")
    bad += [f"{SELFTEST} ran another {name}" for name in stale(st, sorted(st.get("code_sha256") or {}))]
    if "main_analysis.py" not in (st.get("code_sha256") or {}):
        bad.append(f"{SELFTEST} does not name main_analysis.py")
    if rh.get("pass") is not True:
        bad.append(f"{REHEARSAL} did not pass its bars")
    bad += [f"{REHEARSAL} ran another {name}" for name in stale(rh, REHEARSAL_CODE)]
    return bad


def make_record(n, decision, pilot, bundle=None, frozen_at=None):
    bundle = list(BUNDLE if bundle is None else bundle)
    files = {rel: digest(rel) for rel in bundle}
    drec = design_seal.load(os.path.basename(design_seal.SEAL))
    return {"prereg": PREREG, **META,
            "base": {"prereg": drec["prereg"], "seal_file": os.path.basename(design_seal.SEAL),
                     "combined_sha256": drec["combined_sha256"]},
            "n": n, "decision": decision, "population": "unflagged", "pilot": pilot,
            "frozen_at": frozen_at or datetime.date.today().isoformat(), "bundle_files": bundle, "files": files,
            "combined_sha256": combined(files, bundle)}


def verify_record(rec):
    """What main_analysis.py checks before it grades human data: every file the record names is as recorded, its
    combined hash is theirs, it names the design's seal, and that seal is intact."""
    files = {}
    for rel in rec.get("bundle_files") or []:
        try:
            files[rel] = digest(rel) == (rec.get("files") or {}).get(rel)
        except SystemExit:
            files[rel] = False
    broken = [rel for rel, ok in files.items() if not ok]
    if combined(rec.get("files") or {}, rec.get("bundle_files") or []) != rec.get("combined_sha256"):
        broken.append("the record's combined hash")
    drec, bad = design_state()
    if (rec.get("base") or {}).get("combined_sha256") != drec["combined_sha256"]:
        broken.append("the design seal it names")
    broken += [f"the design's seal: {b}" for b in bad]
    return {"files": files, "broken": broken, "intact": not broken}


def write(args):
    _, bad = design_state()
    if bad:
        raise SystemExit("not written: the design's seal is broken: " + "; ".join(bad))
    bad = tested_state()
    if bad:
        raise SystemExit("not written: " + "; ".join(bad))
    import pilot_analysis as PA  # noqa: PLC0415  (numpy)
    try:
        out = PA.size(args.estimates, os.path.join(HERE, TABLE))
    except PA.Refusal as e:
        raise SystemExit(f"not written: pilot_analysis.size refused ({e.kind}): {e}")
    n = out.get("n")
    if n is None:
        if args.owner_n != 240 or not args.owner_said:
            raise SystemExit(f"not written: the rule chose no n ({out['decision']}). PILOT.md: the owner decides between "
                             f"240, with the power stated, and stopping. For 240, pass --owner-n 240 and the owner's words "
                             f"(--owner-said)")
        n, decision = 240, f"the owner's decision, since the rule chose none ({out['decision']}): {args.owner_said}"
    elif args.owner_n is not None:
        raise SystemExit(f"not written: the rule chose n = {n}; --owner-n is for when it chooses none")
    else:
        decision = out["decision"]
    est_path, size_path = (os.path.join(args.estimates, name) for name in ("pilot_estimates.json", "sample_size.json"))
    shutil.copy(size_path, os.path.join(HERE, SAMPLE_SIZE))
    bundle = list(BUNDLE)
    if args.publish_estimates:
        shutil.copy(est_path, os.path.join(HERE, ESTIMATES))
        bundle.append(ESTIMATES)
    pilot = {"estimates_sha256": raw_sha256(est_path), "estimates_published": bool(args.publish_estimates),
             "sample_size_sha256": raw_sha256(size_path), "table_sha256": out["table_sha256"],
             "rule_decision": out["decision"], "curve": out.get("curve")}
    frozen = datetime.date.today().isoformat()
    if os.path.exists(SEAL):
        frozen = load(os.path.basename(SEAL)).get("frozen_at", frozen)
        print("seal exists, keeping frozen_at", frozen)
    rec = make_record(n, decision, pilot, bundle, frozen)
    with open(SEAL, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rec, f, indent=2)
        f.write("\n")
    print("written", os.path.basename(SEAL), f"n = {n}:", decision)
    print("  combined sha256", rec["combined_sha256"])
    for rel in bundle:
        print(f"    {rel:<36} {rec['files'][rel][:16]}")
    return 0


def verify():
    if not os.path.exists(SEAL):
        print("no seal of step 10 recorded. It is written at step 10, after the pilot (MAIN.md)")
        return 1
    rec = load(os.path.basename(SEAL))
    state = verify_record(rec)
    print(f"SEAL CHECK, {rec['prereg']}, frozen {rec['frozen_at']}: n = {rec['n']} ({rec['decision']})")
    ok = state["intact"] and rec["bundle_files"] in (BUNDLE, BUNDLE + [ESTIMATES])
    if rec["bundle_files"] not in (BUNDLE, BUNDLE + [ESTIMATES]):
        print("  the bundle's list differs from this script's")
    for rel, same in state["files"].items():
        print(f"    {rel:<36} {'ok' if same else 'CHANGED SINCE THE SEAL'}")
    size = load(SAMPLE_SIZE)
    for name, good in (("the record's n is the rule's, or the owner's 240 when the rule chose none",
                        rec["n"] == size.get("n") or (size.get("n") is None and rec["n"] == 240)),
                       ("sample_size.json read the estimates whose hash the record holds",
                        size.get("estimates_sha256") == rec["pilot"]["estimates_sha256"]),
                       ("the design's seal is intact, and the record names it",
                        not [b for b in state["broken"] if b.startswith("the design")])):
        ok &= good
        print(f"  {'ok' if good else 'FAILED'}: {name}")
    for b in tested_state():
        ok = False
        print(f"  FAILED: {b}")
    print("  SEAL INTACT" if ok else "  SEAL BROKEN")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--estimates", help="the folder holding the pilot's pilot_estimates.json (step 9)")
    ap.add_argument("--publish-estimates", action="store_true", help="copy pilot_estimates.json into results/ (owner's OK)")
    ap.add_argument("--owner-n", type=int, default=None)
    ap.add_argument("--owner-said", default=None)
    args = ap.parse_args()
    if args.write:
        if not args.estimates:
            ap.error("--write needs --estimates DIR")
        return write(args)
    return verify()


if __name__ == "__main__":
    raise SystemExit(main())
