"""Grader for prereg-poker-recency-v1. The bars live here and nowhere else.

    python grade_recency.py recency_result.json [graded.json]

Reads the output of `analyze_recency.py HANDS OUT 10 0 SITE` (threshold 10 big
blinds, the coarse stack bins, one site) and returns a verdict for each
prediction from the contrasts for raising after a large pot of either result.
"""
import json
import sys

ZERO_BAND = 0.015                 # an interval inside +-ZERO_BAND counts as no difference (widened from 0.01 before the seal)
H3_BAND = (-0.022, -0.005)        # the development range -0.010 to -0.014, widened by about 0.007
MIN_PLAYERS = 3000


def grade(res):
    c = res["contrasts"]["raised"]
    first, second = c["any_lag1_minus_lag2"], c["any_lag2_minus_lag3"]
    if first.get("players", 0) < MIN_PLAYERS or "ci95" not in second:
        return {"verdict": "VOID", "reason": "fewer than %d players in the first contrast" % MIN_PLAYERS}
    win, loss = c["win_lag1_minus_lag2"], c["loss_lag1_minus_lag2"]
    out = {
        "H1 raising dips in the hand straight after a large pot":
            "PASS" if first["ci95"][1] < 0 else "FAIL",
        "H2 the dip lasts one hand":
            "PASS" if -ZERO_BAND < second["ci95"][0] and second["ci95"][1] < ZERO_BAND else "FAIL",
        "H3 the size replicates":
            "PASS" if H3_BAND[0] <= first["difference"] <= H3_BAND[1] else "FAIL",
        "H4 the dip follows wins and losses alike":
            "PASS" if win.get("difference", 1) < 0 and loss.get("difference", 1) < 0 else "FAIL",
    }
    keep = ("any_lag1_minus_lag2", "any_lag2_minus_lag3", "any_lag3_minus_lag4",
            "win_lag1_minus_lag2", "loss_lag1_minus_lag2")
    return {"verdict": "GRADED", "site": res.get("site"), "predictions": out,
            "numbers": {k: c[k] for k in keep}}


if __name__ == "__main__":
    g = grade(json.load(open(sys.argv[1])))
    if len(sys.argv) > 2:
        json.dump(g, open(sys.argv[2], "w"), indent=1)
    print(json.dumps(g.get("predictions", g), indent=1))
