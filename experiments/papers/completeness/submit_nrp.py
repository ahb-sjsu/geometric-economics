#!/usr/bin/env python3
"""Run score.py (or --script) on NRP, one CPU Job per corpus. Runs ON ATLAS beside the nats-bursting client, and
follows the NRP PREFLIGHT (reference_nrp_job_policies) line by line:

  * CPU-only, exempt class: cpu=1, memory=1Gi, ephemeral-storage declared. The footprint was
    measured on Atlas (CPC18, 10 folds, 3 draws): peak RSS 0.20 GiB, 99% of one CPU;
    explore_rho.py measured the same way (CPC18, 2 folds, 2 draws): 0.19 GiB.
  * Self-contained: score.py, strata_models.py and the corpus's problems file ride in as base64,
    each checked by sha256 in the pod. Versions pinned to Atlas's.
  * Self-terminating, no sleep in the pod, backoff_limit=0; the result is printed gzip+base64
    between markers and collected from the log.
  * Submitted via nats-bursting, a fresh name per attempt, creationTimestamp checked. Finished
    Jobs are deleted after their log is saved. At most 2 attempts per corpus.

    python submit_nrp.py --i-have-checked-nrp-policy --src DIR --out DIR [--folds 10 --draws 100]
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
from nats_bursting.descriptor import JobDescriptor, Resources, Volume  # noqa: E402

NS = "ssu-atlas-ai"
BATCH = "ge-completeness"
IMAGE = "python:3.12-slim"
PINS = "numpy==2.4.6 scipy==1.18.1 scikit-learn==1.8.0"
CORPORA = ["cpc18", "gp2012", "pachur2017", "pachur2018", "zilker2020", "babula2018"]
MAX_TRIES = 2
POLL_S = 60


def sh(*cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def b64(path: Path):
    raw = path.read_bytes()
    return base64.b64encode(raw).decode(), hashlib.sha256(raw).hexdigest()


def command(src: Path, corpus: str, folds: int, draws: int, script: str, extra=(), cfg="") -> str:
    files = {"score.py": src / "score.py", "strata_models.py": src / "strata_models.py", script: src / script,
             f"problems_{corpus.split('.p')[0]}.npz": src / "data" / f"problems_{corpus.split('.p')[0]}.npz", **{e: src / e for e in extra}}
    lines = ["set -euo pipefail", "export PYTHONUNBUFFERED=1 PIP_ROOT_USER_ACTION=ignore", "mkdir -p /work"]
    for name, path in files.items():
        enc, sha = b64(path)
        if cfg and name.startswith("problems_"):           # too big for an argument: from the ConfigMap
            lines.append(f"cp /cfg/{name} /work/{name}")
        else:
            lines.append(f"echo '{enc}' | base64 -d > /work/{name}")
        lines.append(f'echo "{sha}  /work/{name}" | sha256sum -c - || exit 3')
    lines += [f"pip install -q {PINS} 2>&1 | tail -1",
              f"cd /work && OMP_NUM_THREADS=1 python -u {script} /work {corpus} /work/out.json "
              f"--folds {folds} --draws {draws} > /work/score.log",
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


def collect(name, out: Path, corpus: str, prefix: str) -> bool:
    log = sh("kubectl", "-n", NS, "logs", f"job/{name}")
    (out / "logs").mkdir(parents=True, exist_ok=True)
    (out / "logs" / f"{name}.log").write_text(log)
    if "----BEGIN result----" not in log:
        return False
    blob = log.split("----BEGIN result----", 1)[1].split("----END result----", 1)[0]
    (out / f"{prefix}_{corpus}.json").write_bytes(gzip.decompress(base64.b64decode(blob.strip())))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-have-checked-nrp-policy", action="store_true", dest="ack")
    ap.add_argument("--src", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--folds", type=int, default=10)
    ap.add_argument("--draws", type=int, default=100)
    ap.add_argument("--script", default="score.py")
    ap.add_argument("--tag", default="gec")
    ap.add_argument("--extra", nargs="*", default=[])
    ap.add_argument("--corpora", nargs="*", default=CORPORA)
    ap.add_argument("--configmap", default="", help="ConfigMap holding the problems files, mounted at /cfg")
    ap.add_argument("--nats-url", default="nats://localhost:4222")
    a = ap.parse_args()
    if not a.ack:
        sys.exit("refusing without --i-have-checked-nrp-policy")
    a.out.mkdir(parents=True, exist_ok=True)
    client = Client(nats_url=a.nats_url)
    state = {c: {"attempt": 0, "done": False} for c in a.corpora}
    stamp = datetime.now().strftime("%m%d%H%M")
    while not all(s["done"] for s in state.values()):
        for c, s in state.items():
            if s["done"]:
                continue
            name = f"{a.tag}-{c.replace('_', '-').replace('.', '-')}-{stamp}-a{s['attempt']}" if s["attempt"] else ""
            st = job_state(name)[0] if name else "missing"
            if st == "active":
                continue
            if st in ("complete", "failed"):
                ok = collect(name, a.out, c, a.script.removesuffix(".py"))
                subprocess.run(["kubectl", "-n", NS, "delete", "job", name], capture_output=True)
                if ok:
                    s["done"] = True
                    print(f"{c}: done ({name})", flush=True)
                    continue
                print(f"{c}: {name} {st} without a result", flush=True)
            elif name:
                print(f"{c}: {name} disappeared", flush=True)
            if s["attempt"] >= MAX_TRIES:
                s["done"] = s["parked"] = True
                print(f"{c}: PARKED after {MAX_TRIES} attempts", flush=True)
                continue
            s["attempt"] += 1
            d = JobDescriptor(name=f"{a.tag}-{c.replace('_', '-').replace('.', '-')}-{stamp}-a{s['attempt']}", image=IMAGE,
                              command=["/bin/bash", "-lc", command(a.src, c, a.folds, a.draws, a.script, a.extra, a.configmap)],
                              resources=Resources(cpu="1", memory="1Gi", gpu=0, ephemeral_storage="2Gi"),
                              labels={"atlas.io/batch": BATCH, "atlas.io/role": c.replace(".", "-")}, backoff_limit=0,
                              volumes=[Volume(name="cfg", mount_path="/cfg", read_only=True, config_map=a.configmap)]
                              if a.configmap else [])
            t_sub = time.time()
            client.submit_and_wait(d, timeout=120)
            st2, created = job_state(d.name)
            fresh = bool(created) and datetime.fromisoformat(created.replace("Z", "+00:00")).timestamp() >= t_sub - 120
            print(f"{c}: submitted {d.name} -> {st2} created {created} fresh={fresh}", flush=True)
        json.dump(state, open(a.out / "driver-state.json", "w"), indent=1)
        if not all(s["done"] for s in state.values()):
            time.sleep(POLL_S)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
