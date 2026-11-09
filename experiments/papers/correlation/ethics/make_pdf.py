"""Print screens.html, with the instrument's screenshots beside it, to instrument_screens.pdf in headless Chromium.

Run from the folder that holds screens.html and screens/.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

here = pathlib.Path.cwd()
html = here / "screens.html"
out = here / "instrument_screens.pdf"
if not html.exists():
    sys.exit(f"missing: {html}")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(html.as_uri())
    page.wait_for_load_state("networkidle")
    n = page.evaluate("document.images.length")
    broken = page.evaluate("Array.from(document.images).filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src)")
    if broken:
        sys.exit(f"images that did not load: {broken}")
    page.pdf(path=str(out), format="Letter", print_background=True,
             margin={"top": "0.75in", "bottom": "0.75in", "left": "0.75in", "right": "0.75in"})
    browser.close()
print(f"wrote {out} ({out.stat().st_size} bytes), {n} images, none broken")
