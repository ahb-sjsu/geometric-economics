"""Drive every bar of grade_gbe.py to fail, starting from the development files.

    python selftest_grade.py dev_matched.json dev_matched_lead.json dev_onesided.json

Development must grade as all PASS. Then one number at a time is moved across
its bar and the line it belongs to must change, and no other prediction's value.
"""
import copy
import json
import sys

from grade_gbe import grade

BASE = [json.load(open(a)) for a in sys.argv[1:4]]


def run(edit=None, heldout=False):
    m, ld, o = copy.deepcopy(BASE)
    if edit:
        edit(m, ld, o)
    return grade(m, ld, o, heldout=heldout)


def setv(d, diff=None, ci=None, key="difference"):
    if diff is not None:
        d[key] = diff
    if ci is not None:
        d["ci95"] = list(ci)


CASES = [
    ("H1", lambda m, ld, o: setv(m["lag1"]["M0"], ci=(-0.012, 0.001)), "FAIL"),
    ("H2", lambda m, ld, o: setv(m["lag1"]["M0"], diff=-0.019), "FAIL"),
    ("H3", lambda m, ld, o: setv(m["lag1"]["M2"], ci=(-0.009, -0.001)), "FAIL"),
    ("H4", lambda m, ld, o: setv(m["lag1"]["M1_after_loss"], ci=(-0.001, 0.02)), "FAIL"),
    ("H5", lambda m, ld, o: setv(o["C1"]["lag_lost"], ci=(-0.001, 0.03)), "FAIL"),
    ("H6", lambda m, ld, o: setv(o["C1"]["lag_lost_minus_won"], ci=(-0.001, 0.03)), "FAIL"),
    ("K1", lambda m, ld, o: setv(ld["lead1"]["M1"], diff=0.0041), "NOT TRUSTED"),
    ("K2", lambda m, ld, o: setv(ld["lead1"]["M1_after_gain"], diff=-0.0051), "NOT TRUSTED"),
    ("K3", lambda m, ld, o: setv(o["C1"]["lead_lost"], diff=0.011, key="slope_per_100_points"), "NOT TRUSTED"),
]
GUARDED = {"K1": ("H1", "H2", "H3"), "K2": ("H4",), "K3": ("H5",)}

bad = 0


def check(label, ok):
    global bad
    bad += not ok
    print("%-4s %s" % ("ok" if ok else "BAD", label))


g = run()
check("development grades", g["verdict"] == "GRADED")
check("development all PASS", all(v == "PASS" for part in ("checks", "predictions", "overall") for v in g[part].values()))
for name, edit, want in CASES:
    r = run(edit)
    hit = GUARDED.get(name, (name,))
    for k, v in r["predictions"].items():
        if k[:2] in hit:
            check("%s moved: %s is %s" % (name, k[:2], want), v.startswith(want))
        else:
            check("%s moved: %s unchanged" % (name, k[:2]), v == "PASS")
    if name in GUARDED:
        check("%s moved: the check itself is FAIL" % name,
              [v for k, v in r["checks"].items() if k.startswith(name)] == ["FAIL"])
r = run(lambda m, ld, o: setv(m["lag1"]["M0"], ci=(-0.012, 0.001)))
check("H1 fails: part 1 FAIL, part 2 PASS", list(r["overall"].values()) == ["FAIL", "PASS"])
r = run(lambda m, ld, o: setv(o["C1"]["lag_lost_minus_won"], ci=(-0.001, 0.03)))
check("H6 fails: part 1 PASS, part 2 FAIL", list(r["overall"].values()) == ["PASS", "FAIL"])
check("V1 fires on the development count", run(heldout=True)["verdict"] == "VOID")
check("V2 fires on too few rows", run(lambda m, ld, o: m["lag1"].update(rows=599999))["verdict"] == "VOID")
print("SELFTEST", "FAILED %d" % bad if bad else "PASSED")
sys.exit(1 if bad else 0)
