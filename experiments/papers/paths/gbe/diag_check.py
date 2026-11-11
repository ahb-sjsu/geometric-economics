"""Development: why is the lead-1 check of analyze_last.py not zero?

    python diag_check.py dev.pkl out.json

The first pass gave -0.0044 for a difference that must be zero if the spinner
is independent of the player, and 50.5% of taken gambles won. This script looks
for the cause on the development half. Nothing here is a test of the thesis.

Written out:
  share of gambles won by design version, by third of the play, by play number,
  and by the player's choice latency on that trial (fast or slow half);
  the share won given the previous taken gamble was won or lost;
  lag 1, lag 2, lead 1 and lead 2 pooled over all trials (no per-participant step),
  and per participant, each for design versions 1 to 2 and 3 to 5 apart.
"""
import json
import pickle
import sys
from collections import defaultdict

import numpy as np

from analyze_last import SEED, estimate, plays


def main(src, out):
    recs = pickle.load(open(src, "rb"))["subjData"]
    rng = np.random.default_rng(SEED)
    share = defaultdict(lambda: [0, 0])
    pooled = defaultdict(lambda: [[0, 0], [0, 0]])
    per = defaultdict(lambda: defaultdict(lambda: [[0, 0], [0, 0]]))
    lat = []
    for rec in recs:
        pid = int(rec["id"])
        ps = plays(rec)
        vers = np.atleast_1d(rec["designVersion"])
        for i, p in enumerate(ps):
            ver = int(vers[i]) if i < len(vers) else -1
            grp = "v1_2" if ver in (1, 2) else "v3_5"
            gam = p[:, 6] == 1
            won = gam & (p[:, 7] == p[:, 3])
            last = None
            for t in range(len(p)):
                if gam[t]:
                    for k in ("version_%d" % ver, "third_%d" % (3 * t // len(p) + 1), "play_%s" % (i + 1 if i < 3 else "4_or_later")):
                        share[k][0] += int(won[t])
                        share[k][1] += 1
                    lat.append((float(p[t, 8]), int(won[t])))
                    if last is not None:
                        k = "after_previous_gamble_" + ("won" if last else "lost")
                        share[k][0] += int(won[t])
                        share[k][1] += 1
                    last = bool(won[t])
                for name, r in (("lag1", t - 1), ("lag2", t - 2), ("lead1", t + 1), ("lead2", t + 2)):
                    if not 0 <= r < len(p) or not gam[r]:
                        continue
                    for k in (name, name + "_" + grp):
                        j = 0 if won[r] else 1
                        pooled[k][j][0] += int(gam[t])
                        pooled[k][j][1] += 1
                        c = per[k][pid][j]
                        c[0] += int(gam[t])
                        c[1] += 1
    lat = np.array(lat)
    ok = np.isfinite(lat[:, 0])
    med = float(np.median(lat[ok, 0]))
    res = {"share_won": {k: {"share": v[0] / v[1], "n": v[1]} for k, v in sorted(share.items())},
           "share_won_by_latency": {"median_seconds": med,
                                    "fast": float(lat[ok & (lat[:, 0] <= med), 1].mean()),
                                    "slow": float(lat[ok & (lat[:, 0] > med), 1].mean())},
           "pooled": {k: {"after_win": v[0][0] / v[0][1], "after_loss": v[1][0] / v[1][1],
                          "difference": v[0][0] / v[0][1] - v[1][0] / v[1][1], "n": v[0][1] + v[1][1]}
                      for k, v in sorted(pooled.items())},
           "per_participant": {k: estimate(per[k], rng) for k in sorted(per)}}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
