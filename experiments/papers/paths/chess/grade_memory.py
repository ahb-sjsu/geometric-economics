"""Grader for prereg-chess-memory-v1. The bars live here and nowhere else.

    python grade_memory.py memory_result.json [graded.json]

Reads the output of `analyze_memory.py ROWS OUT 24` and returns a verdict for
each prediction from the curve over pairs where the player's own moves came in
the same order. KMAX in analyze_memory.py is 5 and with the player's own order
the same k is even, so the point "6 or more" is stored under k = 5.
"""
import json
import sys

BAND = 0.01                       # an interval inside +-BAND counts as zero
H1_FLOOR = 0.02                   # D(0) interval above this
H2_FLOOR = 0.005                  # D(2) interval above this
H3_FALL_0_2 = 0.015               # D(0) - D(2) interval above this
H4_BANDS = {"0": (0.031, 0.041), "2": (0.008, 0.017), "4": (0.003, 0.013)}
MIN_PLAYERS = {"0": 50000, "4": 5000}


def grade(res):
    c = res["own_same"]
    void = [k for k, n in MIN_PLAYERS.items() if c.get(k, {}).get("players", 0) < n]
    if void:
        return {"verdict": "VOID", "reason": "too few players at k = " + ", ".join(void)}

    def lo(k):
        return c[k]["ci95"][0]

    def hi(k):
        return c[k]["ci95"][1]

    out = {
        "H1 history matters with the position fixed":
            "PASS" if lo("0") > H1_FLOOR else ("FAIL, inside the zero band" if -BAND < lo("0") and hi("0") < BAND else "FAIL"),
        "H2 it matters beyond the last move": "PASS" if lo("2") > H2_FLOOR else "FAIL",
        "H3 the last move carries most of it":
            "PASS" if c["0_minus_2"]["ci95"][0] > H3_FALL_0_2 else "FAIL",
        "H4 the values replicate":
            "PASS" if all(a <= c[k]["D"] <= b for k, (a, b) in H4_BANDS.items()) else "FAIL",
    }
    numbers = {k: c[k] for k in ("0", "2", "4", "5", "0_minus_2", "2_minus_4")}
    return {"verdict": "GRADED", "predictions": out, "numbers": numbers}


if __name__ == "__main__":
    g = grade(json.load(open(sys.argv[1])))
    if len(sys.argv) > 2:
        json.dump(g, open(sys.argv[2], "w"), indent=1)
    print(json.dumps(g.get("predictions", g), indent=1))
