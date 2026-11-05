#!/usr/bin/env python3
"""Run rehearsal.py on NRP, one CPU Job per truth. Runs ON ATLAS beside the nats-bursting client and
follows the NRP PREFLIGHT (reference_nrp_job_policies) line by line, as
../../papers-archive/completeness/submit_nrp.py did:

  * CPU-only, exempt class: cpu=1, memory=2Gi (the exempt maximum), ephemeral-storage declared.
    Footprint measured on Atlas with REHEARSAL_QUICK (30 people, GEO1 and RDU): peak RSS 0.10 GiB, 99%
    of one CPU, about 0.2 s per simulated person, so a full cell (60 studies x 200 people) runs about 40
    minutes. Version 2 fits each model twice: about 0.28 s per person, so 50 studies x 200 people run
    about 47 minutes. Version 3 adds the hierarchical fit (hier.py, JAX on one CPU), measured on Atlas
    at n = 120: 290 to 400 s per fit, peak RSS 0.57 GiB. Ten fits per truth add about an hour.
    Version 4 ran 22 to 93 minutes per truth at 200 people; a version 5 cell has 240.
  * Self-contained: rehearsal.py, models.py and stimuli.py ride in as base64, each checked by sha256
    in the pod. Versions pinned to Atlas's.
  * Self-terminating, no sleep in the pod, backoff_limit=0; the result is printed gzip+base64 between
    markers and collected from the log.
  * Submitted via nats-bursting, a fresh name per attempt, creationTimestamp checked. Finished Jobs
    are deleted after their log is saved; an active Job is never deleted. A kubectl error is retried the
    next round; a finished Job whose pod is gone counts as lost and is resubmitted. At most --max-tries
    attempts per truth (2 until version 4, 3 from version 5: a pod can be lost at any time).

    python submit_nrp.py --i-have-checked-nrp-policy --src DIR --out DIR [--truths GEO1 ...] [--max-tries 3]

The pilot rehearsal (PILOT.md, sequence step 4) runs the same way with --pilot-ref and --pilot-table: each unit
is TRUTH:SEED, one Job of --pilots-per-job simulated pilots through `pilot_analysis.py rehearse`, with the
reference and the table riding in gzipped and checked by sha256 like the code. Results land as
rehearse_<TRUTH>_s<SEED>.json. --pilot-n runs it at another pilot size, and --no-hier skips hier.py and jax.
--pilot-reference builds references instead, one Job per pilot size given as the units, landing as
pilot_reference_n<SIZE>.json (choosing the pilot's size, PILOT.md).
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, "/home/claude/step5")
from nats_bursting.client import Client  # noqa: E402
from nats_bursting.descriptor import JobDescriptor, Resources  # noqa: E402

NS = "ssu-atlas-ai"
BATCH = "ge-correlation"
IMAGE = "python:3.12-slim"
PINS = "numpy==2.2.6 scipy==1.17.1"                  # the versions tested on Atlas
PINS_HIER = "jax==0.12.0.1 numpyro==0.22.0"          # only when the hierarchical fit runs
TRUTHS = ["GEO1", "GEO2", "EARLY", "RDU", "CAG", "ADD", "IA"]
FILES = ["rehearsal.py", "models.py", "stimuli.py", "hier.py"]
PILOT_FILES = FILES + ["split_pilot.py", "pilot_analysis.py"]
POLL_S = 60


def embed(src: Path, names, gz=False):
    lines = []
    for name in names:
        raw = (src / name).read_bytes()
        if gz:
            lines.append(f"echo '{base64.b64encode(gzip.compress(raw)).decode()}' | base64 -d | gunzip > /work/{name}")
        else:
            lines.append(f"echo '{base64.b64encode(raw).decode()}' | base64 -d > /work/{name}")
        lines.append(f'echo "{hashlib.sha256(raw).hexdigest()}  /work/{name}" | sha256sum -c - || exit 3')
    return lines


# Linux caps one argument at 128 KiB (MAX_ARG_STRLEN), and the command is one argument to bash -lc. The first
# pilot-rehearsal Jobs embedded their files plain and failed at exec with "argument list too long" (2026-11-03).
MAX_COMMAND = 120_000


def pilot_command(src: Path, unit: str, ref: Path, table: Path, per_job: int, pilot_n=None, no_hier=False) -> str:
    truth, seed = unit.split(":")
    lines = ["set -euo pipefail", "export PYTHONUNBUFFERED=1 PIP_ROOT_USER_ACTION=ignore", "mkdir -p /work"]
    lines += embed(src, PILOT_FILES, gz=True)
    for path, dest in ((ref, "ref.json"), (table, "table.json")):
        raw = path.read_bytes()
        lines.append(f"echo '{base64.b64encode(gzip.compress(raw)).decode()}' | base64 -d | gunzip > /work/{dest}")
        lines.append(f'echo "{hashlib.sha256(raw).hexdigest()}  /work/{dest}" | sha256sum -c - || exit 3')
    extra = (f" --pilot-n {int(pilot_n)}" if pilot_n else "") + (" --no-hier" if no_hier else "")
    lines += [f"pip install -q {PINS}{'' if no_hier else ' ' + PINS_HIER} 2>&1 | tail -1",
              f"cd /work && OMP_NUM_THREADS=1 python -u pilot_analysis.py rehearse {truth} {per_job} /work/out.json "
              f"--reference /work/ref.json --table /work/table.json --seed {int(seed)}{extra} > /work/run.log",
              'echo "----BEGIN result----"', "gzip -c /work/out.json | base64 -w0",
              'echo; echo "----END result----"']
    return "\n".join(lines)


def reference_command(src: Path, pilot_n: int) -> str:
    """`pilot_analysis.py reference` for simulated pilots of pilot_n people (choosing the pilot's size, PILOT.md)."""
    lines = ["set -euo pipefail", "export PYTHONUNBUFFERED=1 PIP_ROOT_USER_ACTION=ignore", "mkdir -p /work"]
    lines += embed(src, PILOT_FILES, gz=True)
    lines += [f"pip install -q {PINS} 2>&1 | tail -1",
              f"cd /work && OMP_NUM_THREADS=1 python -u pilot_analysis.py reference /work/out.json --pilot-n {int(pilot_n)} "
              f"> /work/run.log",
              'echo "----BEGIN result----"', "gzip -c /work/out.json | base64 -w0",
              'echo; echo "----END result----"']
    return "\n".join(lines)


def command(src: Path, truth: str, hier_sims=None) -> str:
    lines = ["set -euo pipefail", "export PYTHONUNBUFFERED=1 PIP_ROOT_USER_ACTION=ignore", "mkdir -p /work"]
    lines += embed(src, FILES)
    env = "" if hier_sims is None else f"REHEARSAL_HIER_SIMS={hier_sims} "
    pins = PINS if hier_sims == 0 else f"{PINS} {PINS_HIER}"
    lines += [f"pip install -q {pins} 2>&1 | tail -1",
              f"cd /work && {env}OMP_NUM_THREADS=1 python -u rehearsal.py {truth} /work/out.json > /work/run.log",
              'echo "----BEGIN result----"', "gzip -c /work/out.json | base64 -w0",
              'echo; echo "----END result----"']
    return "\n".join(lines)


def job_state(name):
    p = subprocess.run(["kubectl", "-n", NS, "get", "job", name, "-o", "json"], capture_output=True, text=True)
    if p.returncode != 0:
        return "missing", ""
    j = json.loads(p.stdout)
    for c in j.get("status", {}).get("conditions") or []:
        if c.get("status") == "True" and c["type"] in ("Complete", "Failed"):
            return c["type"].lower(), j["metadata"].get("creationTimestamp", "")
    return "active", j["metadata"].get("creationTimestamp", "")


def collect(name, out: Path, result: str):
    """True: result saved. False: no result (the Job is deleted and the truth resubmitted). None: kubectl did
    not answer, or the pod is still there, so the Job is kept and collection tried again next round. Version 5's
    first driver died here on a failed `kubectl logs` for a Job whose pod was gone (2026-11-03)."""
    p = subprocess.run(["kubectl", "-n", NS, "logs", f"job/{name}"], capture_output=True, text=True)
    if p.returncode != 0:
        pods = subprocess.run(["kubectl", "-n", NS, "get", "pods", "-l", f"job-name={name}", "-o", "name"],
                              capture_output=True, text=True)
        if pods.returncode != 0 or pods.stdout.strip():
            return None
        log = f"[no pod left for {name}; kubectl logs said: {p.stderr.strip()}]"
    else:
        log = p.stdout
    (out / "logs").mkdir(parents=True, exist_ok=True)
    (out / "logs" / f"{name}.log").write_text(log)
    if "----BEGIN result----" not in log:
        return False
    blob = log.split("----BEGIN result----", 1)[1].split("----END result----", 1)[0]
    (out / result).write_bytes(gzip.decompress(base64.b64decode(blob.strip())))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack")
    ap.add_argument("--src", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--truths", nargs="*", default=TRUTHS)
    ap.add_argument("--tag", default="gecr")
    ap.add_argument("--hier-sims", type=int, default=None,
                    help="studies per truth that get the hierarchical fit (rehearsal default 10); 0 skips it and jax")
    ap.add_argument("--nats-url", default="nats://localhost:4222")
    ap.add_argument("--max-tries", type=int, default=3)
    ap.add_argument("--pilot-ref", type=Path, help="pilot rehearsal: the reference (pilot_analysis.py reference)")
    ap.add_argument("--pilot-table", type=Path, help="pilot rehearsal: the power table (power_table.py)")
    ap.add_argument("--pilots-per-job", type=int, default=10)
    ap.add_argument("--pilot-n", type=int, default=None, help="pilot rehearsal: simulated pilots of this many people")
    ap.add_argument("--no-hier", action="store_true", help="pilot rehearsal: skip hier.py, whose kappa the rule no longer reads")
    ap.add_argument("--pilot-reference", action="store_true",
                    help="build pilot references instead; each unit is a pilot size (pilot_analysis.py reference --pilot-n)")
    a = ap.parse_args()
    if not a.ack:
        sys.exit("refusing without --i-have-checked-nrp-policy")
    pilot = a.pilot_ref is not None
    if pilot != (a.pilot_table is not None) or (pilot and not all(":" in t for t in a.truths)):
        sys.exit("the pilot rehearsal needs --pilot-ref, --pilot-table and units TRUTH:SEED")
    if a.pilot_reference and (pilot or not all(t.isdigit() for t in a.truths)):
        sys.exit("--pilot-reference takes pilot sizes as units, and no --pilot-ref or --pilot-table")
    a.out.mkdir(parents=True, exist_ok=True)
    client = Client(nats_url=a.nats_url)
    state = {t: {"attempt": 0, "done": False} for t in a.truths}
    stamp = datetime.now().strftime("%m%d%H%M")
    while not all(s["done"] for s in state.values()):
        for t, s in state.items():
            if s["done"]:
                continue
            slug = f"ref{t}" if a.pilot_reference else t.lower().replace(":", "-s")
            name = f"{a.tag}-{slug}-{stamp}-a{s['attempt']}" if s["attempt"] else ""
            st = job_state(name)[0] if name else "missing"
            if st == "active":
                continue
            if st in ("complete", "failed"):
                result = (f"pilot_reference_n{t}.json" if a.pilot_reference else
                          f"rehearse_{t.replace(':', '_s')}.json" if pilot else f"rehearsal_{t}.json")
                ok = collect(name, a.out, result)
                if ok is None:
                    continue
                subprocess.run(["kubectl", "-n", NS, "delete", "job", name], capture_output=True)
                if ok:
                    s["done"] = True
                    print(f"{t}: done ({name})", flush=True)
                    continue
                print(f"{t}: {name} {st} without a result", flush=True)
            elif name:
                print(f"{t}: {name} disappeared", flush=True)
            if s["attempt"] >= a.max_tries:
                s["done"] = s["parked"] = True
                print(f"{t}: PARKED after {a.max_tries} attempts", flush=True)
                continue
            s["attempt"] += 1
            cmd = (reference_command(a.src, int(t)) if a.pilot_reference else
                   pilot_command(a.src, t, a.pilot_ref, a.pilot_table, a.pilots_per_job, a.pilot_n, a.no_hier) if pilot
                   else command(a.src, t, a.hier_sims))
            if len(cmd.encode()) > MAX_COMMAND:
                sys.exit(f"{t}: the command is {len(cmd.encode())} bytes, over {MAX_COMMAND}; "
                         f"exec would fail with 'argument list too long'")
            d = JobDescriptor(name=f"{a.tag}-{slug}-{stamp}-a{s['attempt']}", image=IMAGE,
                              command=["/bin/bash", "-lc", cmd],
                              resources=Resources(cpu="1", memory="2Gi", gpu=0, ephemeral_storage="2Gi"),
                              labels={"atlas.io/batch": BATCH, "atlas.io/role": slug}, backoff_limit=0)
            t_sub = time.time()
            client.submit_and_wait(d, timeout=120)
            st2, created = job_state(d.name)
            fresh = bool(created) and datetime.fromisoformat(created.replace("Z", "+00:00")).timestamp() >= t_sub - 120
            print(f"{t}: submitted {d.name} -> {st2} created {created} fresh={fresh}", flush=True)
        json.dump(state, open(a.out / "driver-state.json", "w"), indent=1)
        if not all(s["done"] for s in state.values()):
            time.sleep(POLL_S)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
