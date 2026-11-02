#!/usr/bin/env python3
"""Download the candidate corpora of prereg-strata-v1 into raw/<corpus>/. Reads nothing.

Files over MAX_MB are listed and skipped. Each corpus goes in its own directory.
"""
import json
import os
import sys
import urllib.request

MAX_MB = 120
OSF = {"gp2012": "7khwj", "pachur2017": "35pf6", "pachur2018": "5semf",
       "zilker2020": "nzwx4", "baselberlin": "rce7g"}
ROOT = sys.argv[1] if len(sys.argv) > 1 else "raw"


def get(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def osf_tree(url, dest):
    while url:
        d = json.loads(get(url))
        for f in d["data"]:
            a = f["attributes"]
            if a["kind"] == "folder":
                osf_tree(f["relationships"]["files"]["links"]["related"]["href"], os.path.join(dest, a["name"]))
                continue
            mb = (a.get("size") or 0) / 1e6
            path = os.path.join(dest, a["name"])
            if mb > MAX_MB:
                print(f"SKIP {mb:7.1f} MB {path}")
                continue
            os.makedirs(dest, exist_ok=True)
            if not os.path.exists(path):
                open(path, "wb").write(get(f["links"]["download"]))
            print(f"got  {mb:7.2f} MB {path}")
        url = d["links"].get("next")


def zenodo(rec, dest):
    d = json.loads(get(f"https://zenodo.org/api/records/{rec}"))
    os.makedirs(dest, exist_ok=True)
    for f in d["files"]:
        mb = f["size"] / 1e6
        path = os.path.join(dest, f["key"])
        if mb > MAX_MB:
            print(f"SKIP {mb:7.1f} MB {path}")
            continue
        if not os.path.exists(path):
            open(path, "wb").write(get(f["links"]["self"]))
        print(f"got  {mb:7.2f} MB {path}")


for name, node in OSF.items():
    try:
        osf_tree(f"https://api.osf.io/v2/nodes/{node}/files/osfstorage/", os.path.join(ROOT, name))
    except Exception as e:
        print("FAIL", name, e)
try:
    zenodo("7770917", os.path.join(ROOT, "babula2018"))
except Exception as e:
    print("FAIL babula2018", e)
