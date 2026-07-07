#!/usr/bin/env python3
"""Generate the self-contained student notebook `coupling_study.ipynb` from the frozen Level-2 menus.

The notebook embeds the menus + all analysis inline so it runs on Colab/Jupyter with no external files
and no access to the private repo. It is a voluntary, not-for-credit METHOD lab (fit your own decision
geometry) with an optional, anonymous, opt-in research contribution — the split that keeps any
student-subject use ethical (voluntary + anonymous + no grade removes the coercion concern; the
instructor still supplies an IRB protocol number in the Consent cell before collecting data).

  python make_coupling_notebook.py    # writes coupling_study.ipynb
"""
from __future__ import annotations

import json

import nbformat as nbf


def compact_menus():
    m = json.load(open("coupling_menus.json", encoding="utf-8"))["menus"]
    out = {}
    for block, rows in m.items():
        out[block] = [[r["text"].split("|")[0].replace("A:", "").strip(),
                       r["text"].split("|")[1].replace("B:", "").strip(),
                       r["encoded_A"], r["encoded_B"]] for r in rows]
    return out


MENUS = compact_menus()

SETUP = f'''\
import numpy as np, json, hashlib
try:
    import ipywidgets as W
    from IPython.display import display
    HAVE_WIDGETS = True
except Exception:
    HAVE_WIDGETS = False

# ---- the frozen choice menus (embedded; each: [text_A, text_B, encoded_A(d1,d2), encoded_B(d1,d2)]) ----
MENUS = {json.dumps(MENUS)}
BLOCKS = ["risk_gain","risk_loss","social_adv","social_dis","patience"]
T = 0.20                                   # choice temperature (fixed, from the theory)
GRID = np.linspace(0.05, np.pi/2-0.05, 61) # candidate tradeoff angles

def _cost(theta, d):                       # geometric cost of an option with shortfalls d=(d1,d2)
    return np.cos(theta)*d[0] + np.sin(theta)*d[1]

def fit_angle(choices, menu):
    """Grid-MLE of one person's tradeoff angle from their A/B choices in a block.
    choices: list of 1(=A)/0(=B); menu: the block's rows. Returns the best-fit angle (radians)."""
    y = np.array(choices, float)
    best_ll, best = -1e9, GRID[len(GRID)//2]
    for th in GRID:
        pA = 1/(1+np.exp(-(np.array([_cost(th,r[3])-_cost(th,r[2]) for r in menu]))/T))
        pA = np.clip(pA, 1e-6, 1-1e-6)
        ll = float(np.sum(y*np.log(pA)+(1-y)*np.log(1-pA)))
        if ll > best_ll: best_ll, best = ll, th
    return float(best)
print("setup ok — widgets:", HAVE_WIDGETS)'''

COLLECT = '''\
# Make your choices. For each row pick the option you would actually prefer (real money framing).
# If ipywidgets renders below, click A/B and then run the next cell. Otherwise, edit `responses`
# manually (1 = you prefer A, 0 = you prefer B), one list per block.
responses = {}
_widgets = {}
if HAVE_WIDGETS:
    boxes = []
    for b in BLOCKS:
        rows = []
        for i,(ta,tb,_,_) in enumerate(MENUS[b]):
            w = W.ToggleButtons(options=[("A: "+ta,1),("B: "+tb,0)], value=1,
                                style={"button_width":"initial"})
            _widgets.setdefault(b,[]).append(w); rows.append(w)
        boxes.append(W.VBox([W.HTML(f"<b>{b}</b>")]+rows))
    display(W.VBox(boxes))
    print("Pick your choices above, then run the next cell.")
else:
    # fallback: a placeholder set of choices so the notebook runs end-to-end. REPLACE with your own.
    rng = np.random.default_rng(0)
    responses = {b: list(rng.integers(0,2,len(MENUS[b]))) for b in BLOCKS}
    print("ipywidgets not available — using placeholder choices. Edit `responses` with your real picks.")'''

HARVEST = '''\
# collect the widget choices (run after picking above)
if HAVE_WIDGETS and _widgets:
    responses = {b: [w.value for w in _widgets[b]] for b in BLOCKS}
print({b: f"{sum(responses[b])}/{len(responses[b])} chose A" for b in BLOCKS})'''

FIT = '''\
# Fit YOUR decision geometry: one tradeoff angle per sub-block, then your aversion parameters.
theta = {b: fit_angle(responses[b], MENUS[b]) for b in BLOCKS}
a_risk   = theta["risk_gain"]  - theta["risk_loss"]   # your loss-aversion parameter (risk reflection)
a_social = theta["social_adv"] - theta["social_dis"]  # your inequality-aversion parameter (social reflection)
print("your sub-angles (rad):", {k: round(v,3) for k,v in theta.items()})
print(f"your loss-aversion  a_risk   = {a_risk:+.3f}")
print(f"your inequality-av. a_social = {a_social:+.3f}")'''

EXPORT = '''\
# OPTIONAL, ANONYMOUS research contribution. This writes ONLY your angles + aversion parameters
# (no name, no raw identity). Submitting is voluntary and not part of your grade. To opt in, set
# CONTRIBUTE = True, run, and upload the printed file to the course dropbox.
CONTRIBUTE = False
record = {"a_risk": a_risk, "a_social": a_social,
          "theta": {k: round(v,4) for k,v in theta.items()},
          "id": hashlib.sha256(str(sorted(responses.items())).encode()).hexdigest()[:12]}
if CONTRIBUTE:
    fn = f"coupling_response_{record['id']}.json"
    json.dump(record, open(fn,"w"), indent=2)
    print("wrote", fn, "-> upload this file (anonymous).")
else:
    print("Not contributing (CONTRIBUTE=False). Your record would be:", record)'''

INSTRUCTOR = '''\
# INSTRUCTOR / class-level analysis. After collecting the anonymous JSONs into ./responses/, this
# runs the pre-registered PRIMARY test: does each student's loss-aversion couple with their
# inequality-aversion? (the aversion contrast, prereg-coupling-angle-v1). Needs ~200 for full power.
import glob
recs = [json.load(open(f)) for f in glob.glob("responses/*.json")]
if len(recs) < 10:
    print(f"only {len(recs)} responses — collect more (target ~200 for full power).")
else:
    ar = np.array([r["a_risk"] for r in recs]); as_ = np.array([r["a_social"] for r in recs])
    r = float(np.corrcoef(ar, as_)[0,1])
    boots = np.array([np.corrcoef(*np.array([[ar[i],as_[i]] for i in
             np.random.default_rng(k).integers(0,len(ar),len(ar))]).T)[0,1] for k in range(2000)])
    lo, hi = np.percentile(boots,[2.5,97.5])
    print(f"N={len(recs)}  aversion coupling r = {r:+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]")
    print("PASS (Level-B supported at the aversion rank)" if lo>0.10 else
          "not yet decisive (CI includes 0.10) — collect more or report as inconclusive.")'''


def build():
    nb = nbf.v4.new_notebook()
    md = nbf.v4.new_markdown_cell
    co = nbf.v4.new_code_cell
    nb.cells = [
        md("# Geometric Decision Lab — does *one* geometry govern your choices?\n\n"
           "You'll make a series of choices about **money gambles**, **splitting money with another "
           "person**, and **waiting for a larger reward**. Then you'll fit *your own* decision "
           "geometry — the tradeoff **angles** a model of choice assigns you — and test a real, open "
           "research question: do the *same* people who are more **loss-averse** in risky choice also "
           "show more **inequality-aversion** in fairness choices? (i.e., is there one shared decision "
           "metric across domains?)\n\n"
           "**Voluntary, not for credit.** This is a live pre-registered study "
           "(`prereg-coupling-angle-v1`); the honest answer is unknown, and volunteers help decide it."),
        md("## Consent (read first)\n\n"
           "- Participation is **entirely voluntary and not for credit** — no grade is attached, and "
           "choosing not to take part, or stopping at any point, has **no consequence** whatsoever.\n"
           "- Your results are **anonymous**: no name or identity is stored — only your fitted angles, "
           "and only if you opt in (`CONTRIBUTE = True` at the end).\n"
           "- You can do the whole notebook just to see *your own* decision geometry and share nothing.\n"
           "- *Instructor: this cell is a placeholder for your IRB protocol number and approved consent "
           "language before any data is collected.*"),
        co(SETUP),
        md("## Part 1 — Make your choices\nImagine each amount is real. Pick the option you'd truly take."),
        co(COLLECT),
        co(HARVEST),
        md("## Part 2 — Fit your decision geometry\nA tradeoff **angle** per block; the **difference** "
           "between the two reflection sub-blocks (gain vs loss, advantageous vs disadvantageous) is "
           "your **aversion parameter** in that domain."),
        co(FIT),
        md("## Part 3 — Contribute (optional, anonymous)"),
        co(EXPORT),
        md("## Part 4 — The class result (instructor / after collection)\n"
           "The pre-registered PRIMARY test: correlate every student's loss-aversion with their "
           "inequality-aversion. A shared decision metric predicts a **positive** coupling."),
        co(INSTRUCTOR),
        md("## Optional exercises (to go deeper)\n"
           "1. Explain why fitting **one angle** per domain and correlating misses the coupling, but "
           "the **gain−loss difference** finds it. (Hint: what does averaging over the reflection do to "
           "a factor that flips sign across it?)\n"
           "2. Modify `fit_angle` to return a bootstrap confidence interval for *your* angle.\n"
           "3. The class `r` has a wide CI at N≈100. How many students are needed for the CI to exclude "
           "0.10? Simulate it.\n"
           "4. What would it mean for decision theory if the coupling is **zero**? Argue both sides."),
    ]
    nb.metadata = {"kernelspec": {"name": "python3", "display_name": "Python 3"},
                   "language_info": {"name": "python"}}
    nbf.write(nb, "coupling_study.ipynb")
    print("wrote coupling_study.ipynb  (%d cells)" % len(nb.cells))


if __name__ == "__main__":
    build()
