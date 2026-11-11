"""Route each participant of the Great Brain Experiment file to development or held out.

    python split_gbe.py Rutledge_GBE_risk_data_TOD.mat out_dir

The rule is DESIGN.md Section 4, fixed on 2026-11-11 before the archive was
downloaded. For a participant with identifier `id` (the sequential number the
archive stores, as decimal text), take SHA-256 of "gbe-split-2026-11-11:" + id.
First hexadecimal character 0 to 7 is development, 8 to f is held out. All of a
participant's plays go with the participant. The depression subset (depData)
carries the same identifiers and is routed by the same rule.

The Matlab file has to be loaded whole. This script looks at the `id` field and
at nothing else. Every other field is copied as loaded. It prints counts of
participants and no value from the data.

Writes dev.pkl, heldout.pkl (each a dict with lists `subjData` and `depData` of
per-participant dicts) and counts.json. The caller makes heldout.pkl unreadable.
"""
import hashlib
import json
import os
import pickle
import sys

import scipy.io

SALT = "gbe-split-2026-11-11:"


def side(pid):
    h = hashlib.sha256((SALT + str(int(pid))).encode()).hexdigest()
    return "dev" if h[0] in "01234567" else "heldout"


def main(src, out):
    os.makedirs(out, exist_ok=True)
    m = scipy.io.loadmat(src, struct_as_record=False, squeeze_me=True)
    parts = {"dev": {"subjData": [], "depData": []}, "heldout": {"subjData": [], "depData": []}}
    counts = {}
    for name in ("subjData", "depData"):
        for rec in m[name]:
            s = side(rec.id)
            parts[s][name].append({f: getattr(rec, f) for f in rec._fieldnames})
            counts[s + "_" + name] = counts.get(s + "_" + name, 0) + 1
    for s, d in parts.items():
        with open(os.path.join(out, s + ".pkl"), "wb") as f:
            pickle.dump(d, f, protocol=4)
    json.dump(counts, open(os.path.join(out, "counts.json"), "w"), indent=1)
    print("DONE", counts, flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
