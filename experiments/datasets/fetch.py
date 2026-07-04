#!/usr/bin/env python3
"""Probe / fetch candidate validation datasets.

By default this only PROBES each inventory URL (HTTP HEAD, then a tiny ranged GET
fallback) and reports what is actually reachable -- it asserts nothing about
access it hasn't checked. Use --download <id> to pull a specific open dataset.

    python fetch.py                 # probe all URLs, print a reachability report
    python fetch.py --download ethics socialchem   # git-clone / download open ones

Honest by construction: registration-gated sources (GPS) will report a login/redirect,
not a file -- which is the truth, and tells us which datasets need a manual step.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    return json.load(open(os.path.join(HERE, "inventory.json"), encoding="utf-8"))


def probe(url: str, timeout: int = 20) -> dict:
    import requests
    try:
        r = requests.head(url, allow_redirects=True, timeout=timeout)
        if r.status_code >= 400 or r.status_code == 405:  # some hosts reject HEAD
            r = requests.get(url, stream=True, timeout=timeout,
                             headers={"Range": "bytes=0-1023"})
        return {
            "status": r.status_code,
            "final_url": r.url,
            "content_type": r.headers.get("Content-Type", ""),
            "content_length": r.headers.get("Content-Length", ""),
            "reachable": r.status_code < 400,
        }
    except Exception as e:  # noqa: BLE001
        return {"status": None, "error": repr(e)[:120], "reachable": False}


def download(ds: dict, dest: str) -> None:
    url = ds["url"]
    os.makedirs(dest, exist_ok=True)
    if url.endswith(".git") or "github.com" in url:
        target = os.path.join(dest, ds["id"])
        if os.path.exists(target):
            print(f"  {ds['id']}: already present at {target}"); return
        print(f"  {ds['id']}: git clone {url}")
        subprocess.run(["git", "clone", "--depth", "1", url, target], check=False)
    else:
        import requests
        fn = os.path.join(dest, ds["id"] + "_" + url.split("/")[-1])
        print(f"  {ds['id']}: GET {url}")
        r = requests.get(url, stream=True, timeout=60)
        with open(fn, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
        print(f"    -> {fn} ({os.path.getsize(fn)} bytes)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", nargs="*", default=None, help="dataset ids to download")
    ap.add_argument("--dest", default=os.path.join(HERE, "raw"))
    a = ap.parse_args()
    inv = load()
    by_id = {d["id"]: d for d in inv["datasets"]}

    if a.download is not None:
        for did in a.download:
            if did in by_id:
                download(by_id[did], a.dest)
            else:
                print(f"  unknown id: {did}")
        return 0

    print(f"{'id':14} {'access':14} {'conf':7} {'reachable':9} status  url")
    for d in inv["datasets"]:
        p = probe(d["url"])
        mark = "yes" if p.get("reachable") else "NO"
        print(f"{d['id']:14} {d['access']:14} {d['confidence']:7} {mark:9} "
              f"{str(p.get('status')):6}  {d['url']}")
        if p.get("error"):
            print(f"               error: {p['error']}")
    print("\nProbe reports HTTP reachability only. 'reachable=yes' with an HTML content-type often "
          "means a landing/registration page, not the data file -- verify per dataset.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
