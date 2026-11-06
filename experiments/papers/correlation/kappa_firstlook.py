"""First look at the kappa limit's shortfall at kappa = 2, on the pilots runs 5 and 6 already simulated at 120 people
(PILOT.md, "The limit for kappa"). Run on Atlas, where those pilots and their reference are kept; it computes nothing
new, and its output is results/kappa_firstlook.txt.

    python kappa_firstlook.py

The pilot's lottery rate is read against the reference's simulated pilots at the truth's OWN row (its kappa and noise
target, nobody of rank one), with no noise mixing. If the pilots differ from the reference only by their rank-one
share, the share of pilots whose rate sits at or below the reference's 80th percentile (the own-row coverage of an
80% upper limit) is 80% when the share does not matter. Printed per truth, with the rate's shift from the
reference's median in units of the reference's spread, and its relation to how many rank-one people the flag left in.
The rate is the one the rule read until 2026-11-05: both attributes' calibration lotteries, over unflagged people.
"""
import glob
import json

import numpy as np

C = "/archive/experiments/correlation"
ref = json.load(open(f"{C}/ref_v7/pilot_reference_n120.json"))


def cell(k, t):
    return f"G{round(k * 100):03d}T{round(t * 10):02d}"


by = {}
for run in ("pilot_reh_v7_n120", "pilot_reh_v8"):
    for path in sorted(glob.glob(f"{C}/{run}/rehearse_*.json")):
        r = json.load(open(path))
        by.setdefault(r["truth"], []).extend((run, q) for q in r["pilots"])

for truth, pp in sorted(by.items()):
    sp = pp[0][1]
    k, t = int(truth[1:4]) / 100, int(truth[5:7]) / 10
    row = cell(k, t)
    d = np.asarray(ref["truths"][row]["lottery_rate_unflagged_draws"])
    med, sd = float(np.median(d)), float(np.std(d))
    rate = np.array([q["rule"]["lottery_rate"] for _, q in pp])
    pit = np.array([(np.sum(d < x) + 0.5 * np.sum(d == x)) / len(d) for x in rate])
    lim = np.array([np.quantile(q["rule"]["kappa_draws"], 0.8) for _, q in pp])
    flagged = np.array([q["s"]["flagged"] for _, q in pp])
    n = np.array([q["s"]["n"] for _, q in pp])
    r1 = np.array([q["planted"]["rank_one_included"] for _, q in pp])
    left = (r1 - flagged) / (n - flagged)            # rank-one people left among the unflagged, roughly (flagged traders count against it)
    z = (rate - med) / sd
    slope = np.polyfit(left, rate - med, 1)
    print(f"{truth} pilots {len(pp)} own row {row}: ref median {med:.4f} sd {sd:.4f}")
    print(f"   own-row coverage {np.mean(pit <= 0.8):.3f}  (run 5 {np.mean(pit[[r == 'pilot_reh_v7_n120' for r, _ in pp]] <= 0.8):.3f}, "
          f"run 6 {np.mean(pit[[r == 'pilot_reh_v8' for r, _ in pp]] <= 0.8):.3f});  as run, limit >= kappa {np.mean(lim >= k - 1e-9):.3f}")
    print(f"   rate minus ref median: mean {np.mean(rate - med):+.4f} = {np.mean(z):+.2f} ref sd;  PIT mean {pit.mean():.3f} "
          f"(0.5 if no shift)")
    print(f"   rank-one included {r1.mean():.1f}, flagged {flagged.mean():.1f}, unflagged {np.mean(n - flagged):.1f}; "
          f"proxy share left {left.mean():+.3f}; corr(rate shift, proxy) {np.corrcoef(left, rate - med)[0, 1]:+.3f}, "
          f"slope {slope[0]:+.4f} per unit share left, intercept {slope[1]:+.4f}")
