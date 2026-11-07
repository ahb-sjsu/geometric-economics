#!/usr/bin/env python3
"""Every screen of the instrument as a picture, for the ethics application and for checking the layout
(PILOT.md, "The open items", 3).

    python instrument_screens.py OUT_DIR [--mode pilot|main]

Needs Playwright with Chromium (run on Atlas). Serves the page as instrument_roundtrip.py does, with its test
settings, and walks one participant through it: the consent, the rules, the quiz and its second try, the first
trial of each kind (two sure options, a coin flip against a sure option, two coin flips), the debrief, the paid
choice, and the screens for a quiz failed twice, a window too small and a link without a Prolific ID. The pictures
are 1280 pixels wide.
"""
from __future__ import annotations

import argparse
import asyncio
import http.server
import os
import sys
import threading
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import export_pilot  # noqa: E402
import instrument_roundtrip as RT  # noqa: E402

KINDS = {(1, 1): "trial_sure_sure", (2, 1): "trial_coin_sure", (1, 2): "trial_coin_sure", (2, 2): "trial_coin_coin"}


async def shoot(base, out, mode):
    from playwright.async_api import async_playwright  # noqa: PLC0415  (Atlas only)
    variant = "base" if mode == "pilot" else "main"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        async def fresh(pid, width=1280, height=800):
            ctx = await browser.new_context(viewport={"width": width, "height": height})
            page = await ctx.new_page()
            page.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            q = urllib.parse.urlencode({"PROLIFIC_PID": pid, "STUDY_ID": "SCREENS", "SESSION_ID": "SCREENS"})
            await page.goto(f"{base}/v/{variant}/index.html?{q}" if pid else f"{base}/v/{variant}/index.html")
            await page.wait_for_selector("h1")
            return ctx, page

        async def snap(page, name):
            await page.screenshot(path=os.path.join(out, f"{name}.png"), full_page=True)
            print("wrote", name, flush=True)

        ctx, page = await fresh(None)
        await snap(page, "00_no_prolific_id")
        await ctx.close()
        ctx, page = await fresh("screens000000000000small", 900, 600)
        await snap(page, "01_window_too_small")
        await ctx.close()

        ctx, page = await fresh("screens00000000000000001")
        await snap(page, "02_consent")
        await page.click("#agree")
        await RT.title(page, "intro")
        await snap(page, "03_how_it_works")
        await page.click("#next")
        await RT.title(page, "charity")
        await page.check("input[name=charity][value='2']")
        await snap(page, "04_charity")
        await page.click("#next")
        await RT.title(page, "rules")
        await snap(page, "05_rules")
        await page.click("#next")
        await RT.title(page, "quiz")
        for i, a in enumerate(RT.WRONG):
            await page.check(f"input[name=q{i}][value='{a}']")
        await snap(page, "06_quiz")
        await page.click("#submit")
        await RT.title(page, "retry")
        await snap(page, "07_quiz_second_try")
        await page.click("#next")
        await RT.title(page, "quiz")
        for i, a in enumerate(export_pilot.QUIZ_KEY):
            await page.check(f"input[name=q{i}][value='{a}']")
        await page.click("#submit")
        await RT.title(page, "ready")
        await snap(page, "08_ready")
        await page.click("#next")
        n = len(RT.TRIALS) + (len(RT.EXTRAS) if mode == "pilot" else 0)
        seen = set()
        for k in range(n):
            await page.wait_for_selector(f"#pair[data-pos='{k}'][data-live='1']")
            tid = await page.get_attribute("#pair", "data-trial-id")
            kind = KINDS[tuple(await page.evaluate(f"() => STIMULI.trials['{tid}'].map(o => o.length)"))]
            if kind not in seen:
                seen.add(kind)
                await snap(page, f"09_{kind}")
            await page.click("#pair button.choose[data-side='0']")
        if mode == "pilot":
            await RT.title(page, "debrief")
            await page.check("input[name=belief][value='4']")
            await page.check("input[name=rule][value='1']")
            await page.check("input[name=difficulty][value='3']")
            await page.fill("textarea[name=strategy]", "I weighed my points against the charity's.")
            await snap(page, "10_debrief")
            await page.click("#submit")
        await RT.title(page, "payment")
        await page.wait_for_selector("body[data-saved='1']")
        await snap(page, "11_paid_choice")
        await ctx.close()

        ctx, page = await fresh("screens00000000000000002")
        await page.click("#agree")
        for key in ("intro", "charity", "rules"):
            await RT.title(page, key)
            if key == "charity":
                await page.check("input[name=charity][value='0']")
            await page.click("#next")
        for attempt in range(2):
            await RT.title(page, "quiz")
            if attempt:
                await page.wait_for_selector("text=Second try")
            for i, a in enumerate(RT.WRONG):
                await page.check(f"input[name=q{i}][value='{a}']")
            await page.click("#submit")
            if not attempt:
                await RT.title(page, "retry")
                await page.click("#next")
        await RT.title(page, "thanks")
        await page.wait_for_selector("body[data-saved='1']")
        await snap(page, "12_quiz_failed")
        await ctx.close()
        await browser.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("out")
    ap.add_argument("--mode", choices=("pilot", "main"), default="pilot")
    args = ap.parse_args()
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    roots = RT.webroots(os.path.join(out, "_serve"))
    store = RT.Store(os.path.join(out, "_serve", "raw"))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), RT.handler(store, roots))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    asyncio.run(shoot(f"http://127.0.0.1:{server.server_address[1]}", out, args.mode))
    server.shutdown()


if __name__ == "__main__":
    main()
