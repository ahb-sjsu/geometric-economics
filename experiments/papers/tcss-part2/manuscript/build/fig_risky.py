"""Figure 1 of the Part II manuscript.

Reads the two graded records as executed and plots, for each of the six test
corpora, each model's test log-loss per choice minus CPT's on the same test
half. Nothing is fit here.

Run from this folder:  python fig_risky.py
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ARCH = os.path.join(HERE, "..", "..", "..", "..", "papers-archive")
psy = json.load(open(os.path.join(ARCH, "psych101", "results", "grade_real.json")))["numbers"]["test_nll"]
strata = json.load(open(os.path.join(ARCH, "strata", "results", "graded_strata_real.json")))["numbers"]
coding = strata["cpt_coding"]
nll = strata["test_nll"]

rows = [("Wulff 2018", {"EV": psy["EV_native"], "GDT2": psy["GDT_transfer"],
                               "GDTS": None, "CPT": psy["CPT_transfer"]})]
names = {"gp2012": "Glöckner 2012", "pachur2017": "Pachur 2017",
         "pachur2018": "Pachur 2018", "zilker2020": "Zilker 2020",
         "babula2018": "Babula 2018"}
for key, label in names.items():
    r = nll[key]
    rows.append((label, {"EV": r["EV"], "GDT2": r["GDT2"], "GDTS": r["GDTS"], "CPT": r[coding[key]]}))

plt.rcParams.update({"font.family": "serif", "font.size": 8})
fig, ax = plt.subplots(figsize=(3.45, 2.5))
style = {"EV": ("s", "Expected value", "0.55"),
         "GDT2": ("o", "GDT, two numbers", "black"),
         "GDTS": ("^", "GDT, stratified", "black")}
for i, (label, r) in enumerate(rows):
    y = len(rows) - 1 - i
    for j, (m, (marker, _, colour)) in enumerate(style.items()):
        if r[m] is None:
            continue
        ax.plot(r[m] - r["CPT"], y + (j - 1) * 0.18, marker, color=colour,
                markerfacecolor="white" if m == "GDTS" else colour, markersize=4.5)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows][::-1])
ax.set_ylim(-0.6, len(rows) - 0.4)
ax.set_xlabel("Test log-loss per choice minus CPT's (nats)")
handles = [plt.Line2D([], [], marker=mk, linestyle="", color=c,
                      markerfacecolor="white" if k == "GDTS" else c, markersize=4.5, label=lab)
           for k, (mk, lab, c) in style.items()]
fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False, fontsize=6.5, handletextpad=0.1, columnspacing=0.8)
ax.set_xlim(-0.004, 0.068)
fig.tight_layout(pad=0.3, rect=(0, 0, 1, 0.92))
fig.savefig(os.path.join(HERE, "fig_risky.pdf"))
fig.savefig(os.path.join(HERE, "fig_risky.png"), dpi=300)
for label, r in rows:
    print(label, {k: (None if v is None else round(v - r["CPT"], 4)) for k, v in r.items()})
