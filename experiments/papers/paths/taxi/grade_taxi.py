"""Grader for prereg-taxi-last-trip-v1. The bars live here and nowhere else.

DRAFT of 2026-11-13. The registration text is not written, the bars below are
provisional and nothing is sealed.

    python grade_taxi.py clockhour.json timing_apart.json tip.json [graded.json] [--development]

Reads the outputs of `stop_clockhour.py DATA OUT`, `stop_timing.py DATA OUT apart`
and `stop_tip.py DATA OUT` and returns each prediction of Section 5 as PASS or
FAIL.

As a self-test, on the development files every line must be PASS, since the
bars were set there.
"""
import json
import sys

S1 = "within_30_minutes.long_share_at_most_0.10"       # the larger sample
S2 = "within_10_minutes.long_share_at_most_0.05"       # the published window, the stricter cabs
BAR10 = "long_share_at_most_0.10"
T2_BAND = (0.012, 0.036)          # fare of the trip just ended, S1, per ten dollars
T3_LIMIT = 0.0025                 # hours 5 to 8, S1, each point estimate within +-this
NEW_YORK = {"h7": 0.0040, "h8": 0.0052}   # published sizes scaled to ten dollars, DEVELOPMENT.md pass 6
T4_LIMIT = 0.004                  # other fares of the last hour, point estimate within +-this
MIN_DECISIONS = {S1: 250000, S2: 25000}


def word(ok):
    return "PASS" if ok else "FAIL"


def grade(clock, timing, tip):
    s1, s2 = clock["samples"][S1], clock["samples"][S2]
    for k, s in ((S1, s1), (S2, s2)):
        if s["decisions"] < MIN_DECISIONS[k]:
            return {"verdict": "VOID", "reason": "V1: %d decisions in %s, fewer than %d" % (s["decisions"], k, MIN_DECISIONS[k])}
    a1, a2 = s1["trip_just_ended_apart"]["coef"], s2["trip_just_ended_apart"]["coef"]
    p1 = s1["as_published"]["coef"]
    lh = timing["samples"][BAR10]["per_10_dollars"]
    tp = tip["samples"][BAR10]["dollars"]["coef"]
    preds = {
        "T1 a larger fare on the trip just ended goes with stopping":
            a1["e_now"]["ci95"][0] > 0 and a2["e_now"]["ci95"][0] > 0,
        "T2 the size replicates":
            T2_BAND[0] <= a1["e_now"]["coef"] <= T2_BAND[1],
        "T3 fares from hours 5 to 8 do nothing":
            all(abs(p1[h]["coef"]) <= T3_LIMIT for h in ("h5", "h6", "h7", "h8")),
        "T4 hours 7 and 8 lie below the published sizes":
            all(p1[h]["ci95"][1] < v for h, v in NEW_YORK.items()),
        "T5 the other fares of the last hour do nothing":
            abs(lh["e_0_1_rest"]["coef"]) <= T4_LIMIT and lh["e_0_1_rest"]["ci95"][1] < lh["e_now"]["ci95"][0],
        "T6 a tip on the trip just ended moves stopping less than its fare":
            tp["tip_now"]["ci95"][1] < tp["e_now"]["ci95"][0],
    }
    ok = {k[:2]: v for k, v in preds.items()}
    overall = {
        "part 1, shifts end on a larger fare (T1, T2)": word(ok["T1"] and ok["T2"]),
        "part 2, no effect of earlier fares, the published fall-off is absent (T3, T4, T5)":
            word(ok["T3"] and ok["T4"] and ok["T5"]),
        "part 3, the fare effect is about the trip and not the money (T6)": word(ok["T6"]),
    }
    numbers = {"S1 apart " + n: a1[n] for n in ("h5", "h6", "h7", "h8", "after8_rest", "e_now")}
    numbers.update({"S1 as published " + n: p1[n] for n in ("h5", "h6", "h7", "h8", "after8")})
    numbers.update({"S2 apart " + n: a2[n] for n in ("h5", "h6", "h7", "h8", "after8_rest", "e_now")})
    numbers.update({"window 6 to 10 hours " + n: lh[n] for n in ("e_now", "e_0_1_rest", "e_1_2", "e_2_4", "e_4plus")})
    numbers.update({"card trips " + n: tp[n] for n in ("tip_now", "e_now", "tips_before")})
    return {"verdict": "GRADED", "decisions": {S1: s1["decisions"], S2: s2["decisions"]},
            "predictions": {k: word(v) for k, v in preds.items()}, "overall": overall, "numbers": numbers}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--development"]
    g = grade(*(json.load(open(a)) for a in args[:3]))
    if len(args) > 3:
        json.dump(g, open(args[3], "w"), indent=1)
    print(json.dumps({k: g[k] for k in ("verdict", "reason", "decisions", "predictions", "overall") if k in g}, indent=1))
