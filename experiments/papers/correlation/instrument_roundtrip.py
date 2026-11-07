#!/usr/bin/env python3
"""The instrument's round trip (PILOT.md, sequence step 3): simulated participants through the real page in a
headless browser, their saved files through export_pilot.py, split_pilot.py and pilot_analysis.py, and every
recorded choice checked against the click that made it.

    python instrument_roundtrip.py OUT_DIR [--people 24] [--parallel 6] [--seeds 2000] [--result results/X.json]

Needs Playwright with Chromium (run on Atlas, not on the laptop). A local server serves the page, with a test copy
of config.js, and stands in for DataPipe's API: POST /api/data/ stores each file once and answers 201, or 400 with
FILE_EXISTS for a name already stored, as DataPipe does (instrument/README.md). Nothing leaves the machine.

The checks:
  build        stimuli.js and MANIFEST.json are what build_instrument.py gives from the sources now;
  order        the page's order (order.js) is stimuli.presentation(seed) for every seed tried, in both modes;
  page         the page's trials, hashes, quiz key, charities, point rate and trial count are stimuli.py's and
               export_pilot.py's;
  clicks       in every counted session, each trial's id, position and choice are those of the click, and its
               response time is at least the driver's wait before the click;
  records      quiz tries, the charity, the debrief, finished, and the paid amounts are those the page showed;
  sessions     a participant who declines leaves no file; one who stops leaves the last checkpoint; a reload
               resumes; a second session is not counted; saves that fail at first arrive; a stray file and a
               participant not on Prolific's list are left out;
  split        split_pilot.py takes the export, pilot_analysis.roundtrip finds every trial where its role says and
               no Prolific ID outside id_map.json, and the analysis reads the readable file and counts what was
               planted;
  main         two participants in the main study's mode: 140 trials, no debrief, its own order.
Controls, each of which must make a check fail: a page that records the other side (swap), a shuffle that stops one
step short (order), a payment at 6 cents a point (pay), and an unpaid bonus (unpaid).
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import http.server
import json
import os
import random
import re
import shutil
import sys
import threading
import time
import urllib.parse
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_instrument  # noqa: E402
import export_pilot  # noqa: E402
import pilot_analysis as PA  # noqa: E402
import split_pilot  # noqa: E402
import stimuli  # noqa: E402

WEB = build_instrument.WEB
FILES = build_instrument.SOURCES + ("config.js", "MANIFEST.json")
MIME = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css",
        ".json": "application/json"}
TRIALS, EXTRAS = PA.TRIALS, PA.EXTRAS
CODES = {"finished": "RTDONE", "quiz_failed": "RTQUIZ"}
# Each control's change to the page. Each must occur exactly once in its file.
MUTATIONS = {
    "swap": ("task.js", "S.trials.push({id, pos, choice: side, rt_ms: rt});",
             "S.trials.push({id, pos, choice: 1 - side, rt_ms: rt});"),
    "order": ("order.js", "for (let i = a.length - 1; i >= 1; i--) {", "for (let i = a.length - 1; i >= 2; i--) {"),
    "pay": ("task.js", "bonus_cents: self * PARAMS.cents,", "bonus_cents: self * (PARAMS.cents + 1),"),
}
TITLES = {"consent": "Consent to take part in a research study", "intro": "How the study works",
          "charity": "Choose your charity", "rules": "Two kinds of option", "quiz": "Four questions about the rules",
          "retry": "Not all of your answers were right", "thanks": "Thank you", "ready": "The choices",
          "debrief": "Four last questions", "payment": "Your paid choice"}
WRONG = [1, 0, 0, 0]                   # a quiz answer set with three wrong answers


# ---- the server: the page, and DataPipe's API --------------------------------------------------------------------

class Store:
    def __init__(self, raw):
        self.raw, self.lock, self.flaky, self.tries, self.refused = raw, threading.Lock(), set(), {}, 0


def handler(store, roots):
    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def send(self, code, body, kind="application/json"):
            body = body if isinstance(body, bytes) else json.dumps(body).encode()
            self.send_response(code)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = urllib.parse.urlparse(self.path).path
            if path == "/complete":
                return self.send(200, b"<!doctype html><title>complete</title><p>complete</p>", MIME[".html"])
            parts = path.strip("/").split("/")
            if len(parts) == 3 and parts[0] == "v" and parts[1] in roots and parts[2] in FILES:
                with open(os.path.join(roots[parts[1]], parts[2]), "rb") as f:
                    return self.send(200, f.read(), MIME[os.path.splitext(parts[2])[1]])
            self.send(404, {"error": "not found"})

        def do_POST(self):
            if urllib.parse.urlparse(self.path).path != "/api/data/":
                return self.send(404, {"error": "not found"})
            try:
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                exp, name, data = body["experimentID"], body["filename"], body["data"]
            except (KeyError, ValueError, TypeError):
                return self.send(400, {"message": "bad request", "error": "INVALID_DATA"})
            if exp not in roots:
                return self.send(400, {"message": "no such experiment", "error": "DATA_COLLECTION_NOT_ACTIVE"})
            if not re.fullmatch(r"[A-Za-z0-9_.-]{1,200}", name):
                return self.send(400, {"message": "bad filename", "error": "UPLOAD_ERROR"})
            try:
                json.loads(data)
            except ValueError:
                return self.send(400, {"message": "not JSON", "error": "INVALID_DATA"})
            with store.lock:
                if name.split("_")[0] in store.flaky and store.tries.get(name, 0) < 2:
                    store.tries[name] = store.tries.get(name, 0) + 1
                    store.refused += 1
                    return self.send(503, {"message": "try later", "error": None})
                path = os.path.join(store.raw, exp, name)
                if os.path.exists(path):
                    return self.send(400, {"message": "exists", "error": "FILE_EXISTS"})
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(data)
            self.send(201, {"message": "Success"})
    return H


def test_config(variant, mode):
    return ("\"use strict\";\nconst CONFIG = " + json.dumps({
        "mode": mode, "datapipe_url": "/api/data/", "experiment_id": variant, "completion_url": "/complete?cc=",
        "completion": CODES, "receipts_url": "https://example.org/receipts",
        "contact": {"pi": "Round-trip test", "email": "test@example.org", "irb": "test board", "protocol": "TEST"},
        "consent_draft": True}, indent=1) + ";\n")


def webroots(out):
    roots = {}
    for variant, mode in (("base", "pilot"), ("main", "main"), ("swap", "pilot"), ("order", "pilot"), ("pay", "pilot")):
        d = os.path.join(out, "web", variant)
        os.makedirs(d, exist_ok=True)
        for name in FILES:
            if name != "config.js":
                shutil.copy(os.path.join(WEB, name), os.path.join(d, name))
        with open(os.path.join(d, "config.js"), "w", encoding="utf-8") as f:
            f.write(test_config(variant, mode))
        if variant in MUTATIONS:
            name, old, new = MUTATIONS[variant]
            with open(os.path.join(d, name), encoding="utf-8") as f:
                text = f.read()
            if text.count(old) != 1:
                raise SystemExit(f"control {variant}: the text to change occurs {text.count(old)} times in {name}")
            with open(os.path.join(d, name), "w", encoding="utf-8") as f:
                f.write(text.replace(old, new))
        roots[variant] = d
    return roots


# ---- the participants ----------------------------------------------------------------------------------------------

def plan(people, rng):
    """Who does what. Index 0 declines, 1 fails the quiz twice, 2 passes on the second try, 3 stops after 70
    choices, 4 reloads mid-trials and at the debrief, 5 meets a store that refuses every file twice, 6 finishes and
    starts again in another browser, 7 stops after 30 and finishes in another browser; the rest finish. The last two
    run the main study's mode. One more participant per control."""
    truths = ("GEO1", "GEO2", "RDU", "IA")
    full = {"quiz": [export_pilot.QUIZ_KEY]}
    specs = []
    for k in range(people + len(MUTATIONS)):
        control = list(MUTATIONS)[k - people] if k >= people else None
        main = people - 2 <= k < people
        s = {"k": k, "pid": f"{rng.getrandbits(96):024x}", "truth": truths[k % len(truths)], "charity": k % 5,
             "variant": control or ("main" if main else "base"), "mode": "main" if main else "pilot",
             "debrief": {"belief": 1 + k % 5, "rule": (0, 1, 1, 1)[k % 4], "difficulty": 1 + (k * 3) % 5,
                         "strategy": f"round trip {k}"}, "sessions": [dict(full)]}
        if control is None:
            if k == 0:
                s["sessions"] = [{"decline": True}]
            elif k == 1:
                s["sessions"] = [{"quiz": [WRONG, [0, 1, 2, 2]]}]
            elif k == 2:
                s["sessions"] = [{"quiz": [WRONG, export_pilot.QUIZ_KEY]}]
            elif k == 3:
                s["sessions"] = [{**full, "stop_at": 69}]
            elif k == 4:
                s["sessions"] = [{**full, "reload_at": 49, "reload_debrief": True}]
            elif k == 5:
                s["flaky"] = True
            elif k == 6:
                s["sessions"] = [dict(full), {**full, "stop_at": 24}]
            elif k == 7:
                s["sessions"] = [{**full, "stop_at": 29}, dict(full)]
        specs.append(s)
    return specs


async def title(page, key):
    await page.wait_for_function(
        "t => { const h = document.querySelector('h1'); return !!h && h.textContent.trim() === t; }", arg=TITLES[key])


def money(text, what):
    m = re.search(rf"{what} of \$(\d+\.\d\d)", text)
    return float(m.group(1)) if m else None


async def run_session(browser, base, spec, sess, n_session, choices, rng):
    rec = {"clicks": [], "outcome": None}
    ctx = await browser.new_context(viewport={"width": 1280, "height": 800})
    page = await ctx.new_page()
    page.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    q = urllib.parse.urlencode({"PROLIFIC_PID": spec["pid"], "STUDY_ID": "RTSTUDY",
                                "SESSION_ID": f"RT{spec['k']:03d}{n_session}"})
    await page.goto(f"{base}/v/{spec['variant']}/index.html?{q}")
    await title(page, "consent")
    if sess.get("decline"):
        await page.click("#decline")
        await title(page, "thanks")
        rec["outcome"] = "declined"
        await ctx.close()
        return rec
    await page.click("#agree")
    await title(page, "intro")
    await page.click("#next")
    await title(page, "charity")
    await page.check(f"input[name=charity][value='{spec['charity']}']")
    await page.click("#next")
    await title(page, "rules")
    await page.click("#next")
    for attempt, answers in enumerate(sess["quiz"]):
        await title(page, "quiz")
        if attempt:
            await page.wait_for_selector("text=Second try")
        for i, a in enumerate(answers):
            await page.check(f"input[name=q{i}][value='{a}']")
        await page.click("#submit")
        if answers == export_pilot.QUIZ_KEY:
            break
        if attempt == 0:
            await title(page, "retry")
            await page.click("#next")
    else:
        await title(page, "thanks")
        await page.wait_for_selector("body[data-saved='1']")
        await page.click("#finish")
        await page.wait_for_url(f"**/complete?cc={CODES['quiz_failed']}")
        rec["outcome"] = "quiz failed"
        await ctx.close()
        return rec
    await title(page, "ready")
    await page.click("#next")
    n = len(TRIALS) + (len(EXTRAS) if spec["mode"] == "pilot" else 0)
    for k in range(n):
        await page.wait_for_selector(f"#pair[data-pos='{k}'][data-live='1']")
        tid = int(await page.get_attribute("#pair", "data-trial-id"))
        side = int(choices[tid])
        wait = rng.uniform(0.03, 0.12)
        await asyncio.sleep(wait)
        await page.click(f"#pair button.choose[data-side='{side}']")
        rec["clicks"].append([tid, k, side, int(wait * 1000)])
        if k == sess.get("reload_at"):
            await page.reload()
        if k == sess.get("stop_at"):
            await asyncio.sleep(1.5)       # let the last checkpoint's save finish, as a slow closer's would
            rec["outcome"] = "stopped"
            await ctx.close()
            return rec
    if spec["mode"] == "pilot":
        await title(page, "debrief")
        if sess.get("reload_debrief"):
            await page.reload()
            await title(page, "debrief")
        d = spec["debrief"]
        await page.check(f"input[name=belief][value='{d['belief']}']")
        await page.check(f"input[name=rule][value='{d['rule']}']")
        await page.check(f"input[name=difficulty][value='{d['difficulty']}']")
        await page.fill("textarea[name=strategy]", d["strategy"])
        await page.click("#submit")
    await title(page, "payment")
    await page.wait_for_selector("body[data-saved='1']", timeout=60000)
    text = await page.inner_text("#app")
    rec["shown"] = {"bonus": money(text, "bonus"), "donation": money(text, "donation")}
    await page.click("#finish")
    await page.wait_for_url(f"**/complete?cc={CODES['finished']}")
    rec["outcome"] = "finished"
    await ctx.close()
    return rec


async def run_person(browser, base, spec, sem, store):
    rng = random.Random(spec["k"])
    choices, _ = PA.sim_choices(spec["truth"], np.random.default_rng([20261106, spec["k"]]))
    spec["choices"] = [int(c) for c in choices]
    if spec.get("flaky"):
        store.flaky.add(spec["pid"])
    async with sem:
        spec["runs"] = []
        for i, sess in enumerate(spec["sessions"]):
            spec["runs"].append(await run_session(browser, base, spec, sess, i, choices, rng))
            await asyncio.sleep(0.2)       # the second session starts later than the first


async def drive(base, specs, parallel, store, seeds, roots):
    from playwright.async_api import async_playwright  # noqa: PLC0415  (Atlas only)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"{base}/v/base/index.html")
        await page.wait_for_selector("h1")
        seen = await page.evaluate("""() => ({sha256: STIMULI.sha256, display: STIMULI.display_sha256,
            seed: STIMULI.seed, trials: STIMULI.trials, parts: STIMULI.parts,
            quiz: TEXT.quiz({cents: 5, charity: "x"}).map(q => q.key), rule: TEXT.debrief({charity: "x"}).rule.key,
            charities: Object.keys(TEXT.charities), short: Object.keys(PARAMS.short), cents: PARAMS.cents,
            main_trials: PARAMS.main_trials, tries: PARAMS.quiz_tries, title: document.querySelector("h1").textContent})""")
        orders = {}
        for variant in ("base", "order"):
            await page.goto(f"{base}/v/{variant}/index.html")
            got = []
            for i in range(0, len(seeds), 250):
                got += await page.evaluate(
                    "ss => ss.map(s => [ORDER.presentation(s, STIMULI.parts.pilot), ORDER.presentation(s, STIMULI.parts.main)])",
                    seeds[i:i + 250])
            orders[variant] = got
        await page.close()
        sem = asyncio.Semaphore(parallel)
        await asyncio.gather(*(run_person(browser, base, s, sem, store) for s in specs))
        await browser.close()
    return seen, orders


# ---- the checks ----------------------------------------------------------------------------------------------------

def expected_trials(run):
    """The trials the last checkpoint of a session holds: every click if it finished, else those up to the last
    multiple of 20 (task.js, PARAMS.checkpoint_every)."""
    clicks = run["clicks"]
    if run["outcome"] == "finished":
        return clicks
    return clicks[:len(clicks) // 20 * 20]


def compare_clicks(people, specs):
    """Mismatches between each counted session's trials and the clicks that made them."""
    bad = []
    for s in specs:
        p = people.get(s["pid"])
        if p is None:
            continue
        exp = expected_trials(s["runs"][0])
        got = p["trials"]
        if len(got) != len(exp):
            bad.append(f"{s['k']}: {len(got)} trials recorded, {len(exp)} clicked and saved")
            continue
        for t, (tid, k, side, wait_ms) in zip(got, exp):
            if (t["id"], t["pos"], t["choice"]) != (tid, k, side):
                bad.append(f"{s['k']}: position {k} recorded as id {t['id']} choice {t['choice']}, clicked id {tid} side {side}")
            elif t["rt_ms"] < wait_ms - 2:
                bad.append(f"{s['k']}: trial {tid} timed {t['rt_ms']} ms, the driver waited {wait_ms} ms")
    return bad


def check(results, name, ok, detail=""):
    results[name] = {"pass": bool(ok), "detail": detail}
    print(("PASS " if ok else "FAIL ") + name + (f": {detail}" if detail else ""), flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("out")
    ap.add_argument("--people", type=int, default=24)
    ap.add_argument("--parallel", type=int, default=6)
    ap.add_argument("--seeds", type=int, default=2000)
    ap.add_argument("--result", default=None, help="also write the summary here (no raw data, no IDs)")
    args = ap.parse_args()
    t0 = time.time()
    out = os.path.abspath(args.out)
    if os.path.exists(out):
        raise SystemExit(f"refusing: {out} exists; the round trip writes a fresh folder")
    os.makedirs(out)
    R = {}
    check(R, "build", not build_instrument.stale(), f"stale {build_instrument.stale()}")
    roots = webroots(out)
    store = Store(os.path.join(out, "raw"))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler(store, roots))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"

    specs = plan(args.people, random.Random(20261106))
    rng = np.random.default_rng(20261106)
    seeds = [0, 1, 2, 3, 2 ** 31 - 2, 2 ** 31 - 1] + [int(x) for x in rng.integers(0, 2 ** 31, args.seeds)]
    seen, orders = asyncio.run(drive(base, specs, args.parallel, store, seeds, roots))

    # junk a participant would not send: a record from someone not on Prolific's list, and a file that is not one
    def post(name, data):
        req = urllib.request.Request(f"{base}/api/data/", json.dumps(
            {"experimentID": "base", "filename": name, "data": data}).encode(), {"Content-Type": "application/json"})
        urllib.request.urlopen(req).read()
    post("outsider_0000000000000000_001.json", json.dumps({"format": export_pilot.RECORD_FORMAT,
                                                           "platform_id": "outsider", "sid": "0" * 16, "seq": 1}))
    post("stray.json", json.dumps([1, 2, 3]))
    server.shutdown()

    # the page against stimuli.py and export_pilot.py
    shown = {int(k): v for k, v in seen["trials"].items()}
    want = {t["id"]: t["options"] for t in TRIALS + EXTRAS}
    check(R, "page: trials", shown == want, f"{len(shown)} trials")
    check(R, "page: hashes", seen["sha256"] == PA.DIGEST and seen["display"] == export_pilot.DISPLAY,
          f"{seen['sha256'][:12]} display {seen['display'][:12]}")
    check(R, "page: quiz key, charities, rate, trial count",
          seen["quiz"] == export_pilot.QUIZ_KEY and seen["tries"] == export_pilot.QUIZ_TRIES
          and seen["charities"] == list(export_pilot.CHARITIES) and seen["short"] == list(export_pilot.CHARITIES)
          and seen["cents"] == export_pilot.CENTS and seen["main_trials"] == len(TRIALS),
          f"quiz {seen['quiz']}, rule key {seen['rule']}, {seen['cents']} cents, {seen['main_trials']} main trials")
    check(R, "page: without a Prolific ID it records nothing", seen["title"] == "This link is missing your Prolific ID")

    def order_mismatch(got):
        return sum((pl != stimuli.presentation(s, TRIALS, EXTRAS)) + (mn != stimuli.presentation(s, TRIALS, []))
                   for s, (pl, mn) in zip(seeds, got))
    check(R, "order: the page's order is stimuli.presentation(seed), both modes",
          order_mismatch(orders["base"]) == 0, f"{len(seeds)} seeds, {order_mismatch(orders['base'])} mismatches")

    # the pilot's files through review, export, split and analysis
    raw = os.path.join(out, "raw", "base")
    base_specs = [s for s in specs if s["variant"] == "base"]
    ids = os.path.join(out, "prolific_ids.txt")
    with open(ids, "w") as f:
        f.write("".join(s["pid"] + "\n" for s in base_specs))
    rev = export_pilot.review(raw, ids, os.path.join(out, "review"))
    shutil.copy(os.path.join(out, "review", "bonuses.csv"), os.path.join(out, "bonuses_paid.csv"))
    with open(os.path.join(out, "review", "donations.json")) as f:
        owed = json.load(f)
    paid = {"bonuses_csv": "bonuses_paid.csv", "bonuses_paid_utc": "round trip",
            "donations": {c: {"dollars": d["dollars"], "date": "round trip", "receipt": "none"} for c, d in owed.items()}}
    split_pilot.write(os.path.join(out, "PAID.json"), paid)
    export = os.path.join(out, "export.json")
    rep = export_pilot.export(raw, ids, os.path.join(out, "PAID.json"), export, "simulated")
    with open(export) as f:
        ex = json.load(f)
    people = {p["platform_id"]: p for p in ex["participants"]}
    by = {s["k"]: s for s in specs}

    bad = compare_clicks(people, base_specs)
    check(R, "clicks: every counted trial is the click that made it, timed at least as long as the wait",
          not bad, f"{sum(len(p['trials']) for p in people.values())} trials; {bad[:3]}")

    def rec_ok(s):
        p = people.get(s["pid"])
        run = s["runs"][0]
        if run["outcome"] == "declined":
            return p is None
        quiz = s["sessions"][0]["quiz"]
        ok = (p["quiz"] == {"attempts": len(quiz) if quiz[-1] == export_pilot.QUIZ_KEY else 2,
                            "passed": quiz[-1] == export_pilot.QUIZ_KEY}
              and p["charity"] == export_pilot.CHARITIES[s["charity"]] and p["finished"] == (run["outcome"] == "finished"))
        if run["outcome"] == "finished":
            d = s["debrief"]
            ok &= p["debrief"] == {"belief": d["belief"], "payment_rule_correct": d["rule"] == seen["rule"],
                                   "difficulty": d["difficulty"], "strategy": d["strategy"]}
            ok &= (p["payment"]["bonus"], p["payment"]["donation"]) == (run["shown"]["bonus"], run["shown"]["donation"])
            ok &= p["payment"]["bonus_ok"] and p["payment"]["donation_ok"] and p["payment"]["trial"] in {t["id"] for t in p["trials"]}
            ok &= p["t_start"] < p["t_main_end"] <= p["t_end"]
        return bool(ok)
    wrong = [s["k"] for s in base_specs if not rec_ok(s)]
    check(R, "records: quiz, charity, debrief, finished and payment as the page showed them", not wrong, f"wrong {wrong}")

    raw_files = os.listdir(raw)
    second = by[7]["runs"][1]
    p7 = people[by[7]["pid"]]
    sess_ok = {
        "decliner left no file": not any(f.startswith(by[0]["pid"]) for f in raw_files),
        "stopper's last checkpoint (60 of 70)": len(people[by[3]["pid"]]["trials"]) == 60,
        "reloaded participant finished": people[by[4]["pid"]]["finished"],
        "refused saves arrived": store.refused > 0 and people[by[5]["pid"]]["finished"],
        "second session not counted": rep["later_sessions_not_counted"] == 2 and people[by[6]["pid"]]["finished"],
        "first session counts, payment follows the finished one":
            not p7["finished"] and len(p7["trials"]) == 20 and p7["payment"]["trial"] is None
            and p7["payment"]["bonus"] == second["shown"]["bonus"],
        "stray file and outsider left out": rep["files_not_records"] == 1 and rep["participants_not_on_list"] == 1,
        "decliner is on Prolific's list without data": rep["prolific_ids_without_data"] == 1,
        "nothing failed a check": not rep["excluded_with_problems"] and not rev["sessions_with_problems"],
    }
    check(R, "sessions", all(sess_ok.values()), "; ".join(f"{k}: {v}" for k, v in sess_ok.items()))
    raws = [export_pilot.latest(export_pilot.load_records(raw)[0])]
    reloads = [r.get("reloads") for r in raws[0].values() if r["platform_id"] == by[4]["pid"]]
    check(R, "sessions: the reload resumed the same session", reloads == [2], f"reloads {reloads}")

    split_dir = os.path.join(out, "split")
    srec = split_pilot.split(export, split_dir)
    problems = PA.roundtrip(export, split_dir)
    check(R, "split: every trial where its role says, no Prolific ID outside id_map.json", not problems,
          f"{srec['readable_trials']} readable, {srec['sealed_trials']} sealed; {problems[:3]}")
    PA.load_readable(os.path.join(split_dir, "readable.json"))
    est, _ = PA.analyse(os.path.join(split_dir, "readable.json"), os.path.join(HERE, "results", "pilot_reference_n120_self.json"),
                        os.path.join(HERE, "results", "power_table_v6b.json"), os.path.join(out, "est"), kappa_fit=PA.no_hier)
    finishers = [s for s in base_specs if s["runs"][0]["outcome"] == "finished"]
    included = sum(PA.person(np.array(s["choices"]))["att_fail"] <= PA.ATT_MAX for s in finishers)
    want_counts = {"participants": len(base_specs) - 1, "quiz_passed": len(base_specs) - 2,
                   "finished": len(finishers), "included": included}
    got_counts = {k: est["counts"][k] for k in want_counts}
    check(R, "analysis: reads the readable file and counts what was planted", got_counts == want_counts
          and est["gates"]["payments"]["pass"], f"counts {got_counts}, planted {want_counts}; payments gate "
          f"{est['gates']['payments']['pass']}; the robot's sub-second clicks fail the fast-choice gate, as they should: "
          f"{est['gates']['fast_choices']['pass'] is False}")

    # the main study's mode
    main_specs = [s for s in specs if s["variant"] == "main"]
    with open(os.path.join(out, "prolific_ids_main.txt"), "w") as f:
        f.write("".join(s["pid"] + "\n" for s in main_specs))
    rev_m = export_pilot.review(os.path.join(out, "raw", "main"), os.path.join(out, "prolific_ids_main.txt"),
                                os.path.join(out, "review_main"), mode="main")
    recs_m = {r["platform_id"]: r for r in export_pilot.latest(export_pilot.load_records(os.path.join(out, "raw", "main"))[0]).values()}
    bad_m = compare_clicks(recs_m, main_specs)
    check(R, "main: 140 trials in its own order, no debrief, paid, every click recorded",
          not bad_m and rev_m["finished"] == len(main_specs) and not rev_m["sessions_with_problems"]
          and all(len(r["trials"]) == len(TRIALS) and r["debrief"] is None for r in recs_m.values()),
          f"{rev_m}; {bad_m[:2]}")

    # the controls: each must be caught
    C = {}
    for variant in MUTATIONS:
        sp = [s for s in specs if s["variant"] == variant]
        d = os.path.join(out, "raw", variant)
        with open(os.path.join(out, f"prolific_ids_{variant}.txt"), "w") as f:
            f.write("".join(s["pid"] + "\n" for s in sp))
        rv = export_pilot.review(d, os.path.join(out, f"prolific_ids_{variant}.txt"), os.path.join(out, f"review_{variant}"))
        recs = {r["platform_id"]: r for r in export_pilot.latest(export_pilot.load_records(d)[0]).values()}
        caught = {"clicks": bool(compare_clicks(recs, sp)), "problems": rv["sessions_with_problems"] > 0}
        if variant == "order":
            caught["order"] = order_mismatch(orders["order"]) > 0
        C[variant] = caught
    check(R, "control swap: the click check catches a page that records the other side", C["swap"]["clicks"], str(C["swap"]))
    check(R, "control order: the order check and export_pilot.py catch a short shuffle",
          C["order"]["order"] and C["order"]["problems"], str(C["order"]))
    check(R, "control pay: export_pilot.py catches a payment the paid trial does not give", C["pay"]["problems"], str(C["pay"]))
    with open(os.path.join(out, "bonuses_paid.csv")) as f:
        lines = f.readlines()
    with open(os.path.join(out, "bonuses_short.csv"), "w") as f:
        f.writelines(lines[1:])
    split_pilot.write(os.path.join(out, "PAID_short.json"), {**paid, "bonuses_csv": "bonuses_short.csv"})
    export_pilot.export(raw, ids, os.path.join(out, "PAID_short.json"), os.path.join(out, "export_short.json"), "simulated")
    split_pilot.split(os.path.join(out, "export_short.json"), os.path.join(out, "split_short"))
    est_s, _ = PA.analyse(os.path.join(out, "split_short", "readable.json"),
                          os.path.join(HERE, "results", "pilot_reference_n120_self.json"),
                          os.path.join(HERE, "results", "power_table_v6b.json"), os.path.join(out, "est_short"),
                          kappa_fit=PA.no_hier)
    check(R, "control unpaid: one bonus left unpaid fails the payments gate", not est_s["gates"]["payments"]["pass"])

    code = {n: split_pilot.sha256(os.path.join(HERE, n)) for n in
            ("instrument_roundtrip.py", "export_pilot.py", "build_instrument.py", "split_pilot.py", "pilot_analysis.py", "stimuli.py")}
    with open(os.path.join(WEB, "MANIFEST.json")) as f:
        manifest = json.load(f)
    summary = {"format": "correlation-instrument-roundtrip/1", "pass": all(v["pass"] for v in R.values()), "checks": R,
               "controls": C, "people": len(specs), "seeds": len(seeds), "build": manifest["build"],
               "stimuli_sha256": PA.DIGEST, "code_sha256": code, "seconds": round(time.time() - t0),
               "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    split_pilot.write(os.path.join(out, "instrument_roundtrip.json"), summary)
    if args.result:
        split_pilot.write(args.result, summary)
    print(f"{'ALL PASS' if summary['pass'] else 'FAILED'}: {sum(v['pass'] for v in R.values())} of {len(R)} checks, "
          f"{summary['seconds']} s", flush=True)
    sys.exit(0 if summary["pass"] else 1)


if __name__ == "__main__":
    main()
