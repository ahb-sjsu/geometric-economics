"""Grader for H5 of prereg-chess-memory-v1. Its bars live here and nowhere else.

    python grade_pull.py pull_time_result.json [graded.json]

Reads the output of analyze_pull_time.py. H5 is graded in bullet, blitz and
rapid separately: the pull among zero-second moves has an interval below zero,
and the pull among moves of two seconds or more has an interval above zero.
H5 passes if both hold in all three speeds.
"""
import json
import sys

SPEEDS = ("bullet", "blitz", "rapid")
MIN_PLAYERS = 1000


def grade(res):
    out, numbers = {}, {}
    for sp in SPEEDS:
        e = res["pull"].get(sp, {})
        zero, slow = e.get("zero", {}), e.get("slow", {})
        numbers[sp] = {"zero": zero, "slow": slow, "slow_minus_zero": e.get("slow_minus_zero", {})}
        if min(zero.get("players", 0), slow.get("players", 0)) < MIN_PLAYERS or "ci95" not in zero or "ci95" not in slow:
            out[sp] = "VOID"
            continue
        out[sp] = "PASS" if zero["ci95"][1] < 0 and slow["ci95"][0] > 0 else "FAIL"
    if "VOID" in out.values():
        verdict = "VOID"
    else:
        verdict = "PASS" if all(v == "PASS" for v in out.values()) else "FAIL"
    return {"H5 a move played in no time is drawn to the earlier move, a slower one to the last": verdict,
            "by_speed": out, "numbers": numbers}


if __name__ == "__main__":
    g = grade(json.load(open(sys.argv[1])))
    if len(sys.argv) > 2:
        json.dump(g, open(sys.argv[2], "w"), indent=1)
    print(json.dumps({k: g[k] for k in list(g)[:2]}, indent=1))
