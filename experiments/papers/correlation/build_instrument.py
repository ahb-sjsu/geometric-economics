#!/usr/bin/env python3
"""Write the instrument's stimulus file and manifest from stimuli.py (PILOT.md, sequence step 3).

    python build_instrument.py          write instrument/stimuli.js and instrument/MANIFEST.json
    python build_instrument.py --check  exit 1 if either is not what stimuli.py and the instrument's files give now

stimuli.js carries only what the page shows: each trial's id and its two options as [p, a, b] outcomes (shortfalls,
as in stimuli.py; the page shows 100 minus each), the three parts that presentation(seed) shuffles, stimuli.SEED,
and stimuli.digest(), the hash the export declares. Roles, blocks and cells stay out of the page. MANIFEST.json lists
the sha256 of every file the participant's browser loads except config.js, which holds the deployment's settings
(instrument/README.md), and a build hash over them, which each session record carries. Hashes are taken with line
endings as LF, so a Windows checkout gives the same ones.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stimuli  # noqa: E402

WEB = os.path.join(HERE, "instrument")
# the files the page loads, in index.html's order; stimuli.js is written here, the rest by hand
SOURCES = ("index.html", "style.css", "stimuli.js", "order.js", "text.js", "task.js")
MANIFEST_FORMAT = "correlation-instrument-manifest/1"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def lf(data):
    return data.replace(b"\r\n", b"\n")


def stimuli_doc():
    """What stimuli.js holds: the trials as shown, the parts presentation(seed) shuffles, and the hashes."""
    trials = stimuli.build()
    extras = stimuli.pilot_extras(trials)
    for t in trials + extras:
        for option in t["options"]:
            ps = [o[0] for o in option]
            assert ps in ([1.0], [0.5, 0.5]), (t["id"], ps)
    shown = {str(t["id"]): t["options"] for t in trials + extras}
    canon = json.dumps(shown, sort_keys=True, separators=(",", ":"))
    main = [[t["id"] for t in trials if t["block"] == "R"], [t["id"] for t in trials if t["block"] != "R"]]
    return {"seed": stimuli.SEED, "sha256": stimuli.digest(trials, extras), "display_sha256": sha256(canon.encode()),
            "parts": {"pilot": main + [[t["id"] for t in extras]], "main": main + [[]]}, "trials": shown}


def stimuli_js():
    return ("// Written by build_instrument.py from stimuli.py. Do not edit: run `python build_instrument.py`.\n"
            "// Each option is a list of [p, a, b] outcomes, a and b the self and charity shortfalls.\n"
            f"const STIMULI = {json.dumps(stimuli_doc(), sort_keys=True, separators=(',', ':'))};\n")


def file_hashes(js, web=WEB):
    files = {}
    for name in SOURCES:
        if name == "stimuli.js" and js is not None:
            files[name] = sha256(lf(js.encode()))
        else:
            with open(os.path.join(web, name), "rb") as f:
                files[name] = sha256(lf(f.read()))
    return files


def manifest(js, web=WEB):
    files = file_hashes(js, web)
    build = sha256("".join(f"{n}:{files[n]}\n" for n in SOURCES).encode())
    return {"format": MANIFEST_FORMAT, "files": files, "build": build, "stimuli_sha256": stimuli.digest()}


def outputs():
    js = stimuli_js()
    return {"stimuli.js": js, "MANIFEST.json": json.dumps(manifest(js), indent=1, sort_keys=True) + "\n"}


def stale(web=WEB):
    """The generated files that differ from what the sources give now."""
    out = []
    for name, text in outputs().items():
        try:
            with open(os.path.join(web, name), "rb") as f:
                if lf(f.read()) != text.encode():
                    out.append(name)
        except FileNotFoundError:
            out.append(name)
    return out


def main():
    paths = outputs()
    build = json.loads(paths["MANIFEST.json"])["build"]
    if "--check" in sys.argv:
        if stale():
            raise SystemExit(f"stale: {stale()}; run python build_instrument.py")
        print("instrument files up to date, build", build)
        return
    for name, text in paths.items():
        with open(os.path.join(WEB, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    print("wrote", ", ".join(paths), "build", build)


if __name__ == "__main__":
    main()
