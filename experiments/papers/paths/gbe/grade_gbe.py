"""Grader for prereg-gbe-last-outcome-v1. The bars live here and nowhere else.

    python grade_gbe.py matched.json matched_lead.json onesided.json [graded.json]

Reads the outputs of `analyze_matched.py DATA OUT`, `analyze_matched.py DATA OUT lead`
and `analyze_onesided.py DATA OUT` and returns each prediction and each check of
Section 5 as PASS or FAIL. A prediction whose check fails is returned as
NOT TRUSTED whatever its value.

As a self-test, on the three development files every line must be PASS, since
the bars were set there.
"""
import json
import sys

H2_BAND = (-0.018, -0.004)        # development -0.0105
H3_BAND = 0.008                   # both ends of the M1 and M2 intervals inside +-this
K1_LIMIT = 0.004                  # pooled next-trial checks, development +0.0017, +0.0018, +0.0001
K2_LIMIT = 0.005                  # next-trial checks by kind with points matched, development +0.0013, +0.0017
K3_LIMIT = 0.010                  # next-trial slope for lost gambles, development +0.0001
HELDOUT_PARTICIPANTS = 23478
MIN_ROWS = 600000


def below(e):
    return e["ci95"][1] < 0


def above(e):
    return e["ci95"][0] > 0


def word(ok):
    return "PASS" if ok else "FAIL"


def grade(matched, lead, onesided, heldout=True):
    lag = matched["lag1"]
    ld = lead["lead1"]
    c1 = onesided["C1"]
    if lag["rows"] < MIN_ROWS:
        return {"verdict": "VOID", "reason": "V2: %d choices follow a taken gamble, fewer than %d" % (lag["rows"], MIN_ROWS)}
    if heldout and lag["participants"] > HELDOUT_PARTICIPANTS:
        return {"verdict": "VOID", "reason": "V1: %d participants, more than the held-out file holds" % lag["participants"]}
    checks = {
        "K1 pooled next-trial checks within %.3f" % K1_LIMIT:
            all(abs(ld[m]["difference"]) <= K1_LIMIT for m in ("M0", "M1", "M2")),
        "K2 next-trial checks after gain and loss trials within %.3f" % K2_LIMIT:
            all(abs(ld[m]["difference"]) <= K2_LIMIT for m in ("M1_after_gain", "M1_after_loss")),
        "K3 next-trial slope for lost gambles within %.3f" % K3_LIMIT:
            abs(c1["lead_lost"]["slope_per_100_points"]) <= K3_LIMIT,
    }
    k1, k2, k3 = checks.values()
    raw = [
        ("H1 gambling dips after a win", below(lag["M0"]), k1),
        ("H2 the size replicates", H2_BAND[0] <= lag["M0"]["difference"] <= H2_BAND[1], k1),
        ("H3 the points held carry the pooled dip",
         all(-H3_BAND < lag[m]["ci95"][0] and lag[m]["ci95"][1] < H3_BAND for m in ("M1", "M2")), k1),
        ("H4 the sign turns with the kind of trial just played",
         below(lag["M1_after_gain"]) and above(lag["M1_after_loss"]), k2),
        ("H5 a larger loss is followed by more gambling", above(c1["lag_lost"]), k3),
        ("H6 the loss slope is larger than the win slope", above(c1["lag_lost_minus_won"]), True),
    ]
    preds = {name: (word(ok) if guard else "NOT TRUSTED, its check failed (value alone would be %s)" % word(ok))
             for name, ok, guard in raw}
    ok = {name[:2]: v == "PASS" for name, v in preds.items()}
    overall = {
        "part 1, the pooled dip and the points held (H1, H3, K1)": word(ok["H1"] and ok["H3"] and k1),
        "part 2, structure inside the null (H4 with K2, H6)": word(ok["H4"] and k2 and ok["H6"]),
    }
    numbers = {"lag1 " + m: lag[m] for m in ("M0", "M1", "M2", "M1_after_gain", "M1_after_loss",
                                             "M2_after_gain", "M2_after_loss")}
    numbers.update({"lead1 " + m: ld[m] for m in ("M0", "M1", "M2", "M1_after_gain", "M1_after_loss")})
    numbers.update({"C1 " + m: c1[m] for m in ("lag_won", "lag_lost", "lead_won", "lead_lost", "lag_lost_minus_won")})
    return {"verdict": "GRADED", "rows": lag["rows"], "participants": lag["participants"],
            "checks": {k: word(v) for k, v in checks.items()}, "predictions": preds, "overall": overall,
            "numbers": numbers}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--development"]
    g = grade(*(json.load(open(a)) for a in args[:3]), heldout="--development" not in sys.argv)
    if len(args) > 3:
        json.dump(g, open(args[3], "w"), indent=1)
    print(json.dumps({k: g[k] for k in ("verdict", "reason", "checks", "predictions", "overall") if k in g}, indent=1))
