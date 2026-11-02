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
  * Self-contained: rehearsal.py, models.py and stimuli.py ride in as base64, each checked by sha256
    in the pod. Versions pinned to Atlas's.
  * Self-terminating, no sleep in the pod, backoff_limit=0; the result is printed gzip+base64 between
    markers and collected from the log.
  * Submitted via nats-bursting, a fresh name per attempt, creationTimestamp checked. Finished Jobs
    are deleted after their log is saved. At most 2 attempts per truth.

    python submit_nrp.py --i-have-checked-nrp-policy --src DIR --out DIR [--truths GEO1 ...]
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
PINS = "numpy==2.2.6 scipy==1.17.1 jax==0.12.0.1 numpyro==0.22.0"   # the versions tested on Atlas
TRUTHS = ["GEO1", "GEO2", "EARLY", "RDU", "CAG", "ADD"]
FILES = ["rehearsal.py", "models.py", "stimuli.py", "hier.py"]
MAX_TRIES = 2
POLL_S = 60


def sh(*cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def command(src: Path, truth: str) -> str:
    lines = ["set -euo pipefail", "export PYTHONUNBUFFERED=1 PIP_ROOT_USER_ACTION=ignore", "mkdir -p /work"]
    for name in FILES:
        raw = (src / name).read_bytes()
        lines.append(f"echo '{base64.b64encode(raw).decode()}' | base64 -d > /work/{name}")
        lines.append(f'echo "{hashlib.sha256(raw).hexdigest()}  /work/{name}" | sha256sum -c - || exit 3')
    lines += [f"pip install -q {PINS} 2>&1 | tail -1",
              f"cd /work && OMP_NUM_THREADS=1 python -u rehearsal.py {truth} /work/out.json > /work/run.log",
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


def collect(name, out: Path, truth: str) -> bool:
    log = sh("kubectl", "-n", NS, "logs", f"job/{name}")
    (out / "logs").mkdir(parents=True, exist_ok=True)
    (out / "logs" / f"{name}.log").write_text(log)
    if "----BEGIN result----" not in log:
        return False
    blob = log.split("----BEGIN result----", 1)[1].split("----END result----", 1)[0]
    (out / f"rehearsal_{truth}.json").write_bytes(gzip.decompress(base64.b64decode(blob.strip())))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack")
    ap.add_argument("--src", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--truths", nargs="*", default=TRUTHS)
    ap.add_argument("--tag", default="gecr")
    ap.add_argument("--nats-url", default="nats://localhost:4222")
    a = ap.parse_args()
    if not a.ack:
        sys.exit("refusing without --i-have-checked-nrp-policy")
    a.out.mkdir(parents=True, exist_ok=True)
    client = Client(nats_url=a.nats_url)
    state = {t: {"attempt": 0, "done": False} for t in a.truths}
    stamp = datetime.now().strftime("%m%d%H%M")
    while not all(s["done"] for s in state.values()):
        for t, s in state.items():
            if s["done"]:
                continue
            name = f"{a.tag}-{t.lower()}-{stamp}-a{s['attempt']}" if s["attempt"] else ""
            st = job_state(name)[0] if name else "missing"
            if st == "active":
                continue
            if st in ("complete", "failed"):
                ok = collect(name, a.out, t)
                subprocess.run(["kubectl", "-n", NS, "delete", "job", name], capture_output=True)
                if ok:
                    s["done"] = True
                    print(f"{t}: done ({name})", flush=True)
                    continue
                print(f"{t}: {name} {st} without a result", flush=True)
            elif name:
                print(f"{t}: {name} disappeared", flush=True)
            if s["attempt"] >= MAX_TRIES:
                s["done"] = s["parked"] = True
                print(f"{t}: PARKED after {MAX_TRIES} attempts", flush=True)
                continue
            s["attempt"] += 1
            d = JobDescriptor(name=f"{a.tag}-{t.lower()}-{stamp}-a{s['attempt']}", image=IMAGE,
                              command=["/bin/bash", "-lc", command(a.src, t)],
                              resources=Resources(cpu="1", memory="2Gi", gpu=0, ephemeral_storage="2Gi"),
                              labels={"atlas.io/batch": BATCH, "atlas.io/role": t.lower()}, backoff_limit=0)
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
