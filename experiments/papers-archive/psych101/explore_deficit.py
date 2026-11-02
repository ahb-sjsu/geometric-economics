#!/usr/bin/env python3
"""EXPLORATORY, unregistered, run after the graded result. Where does frozen GDT lose to frozen CPT?

Reuses fit_psych101's split, unit, frame and kappa refit exactly, then breaks the test-half
loss difference (GDT minus CPT, nats per choice, positive = CPT better) down by problem type.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fit_psych101 as F  # noqa: E402

frozen = json.load(open(os.path.join(HERE, "frozen_cpc18.json")))["models"]
th = {k: frozen[F.FAMILY[k]]["theta"] for k in F.FAMILY}
cov = np.load(os.path.join(HERE, "rows_covariates.npz"))
A, B, prob = cov["A"], cov["B"], cov["problem"]
y = np.load(os.path.join(HERE, "rows_outcome.npz"))["chose_B"].astype(int)
unit = F.payoff_unit(A, B, prob)
A, B = A / [unit, 1, unit], B / [unit, 1, unit]
rng = np.random.default_rng(F.SEED)
perm = rng.permutation(np.unique(prob))
cal_set = set(perm[: int(len(perm) * F.CAL_FRAC)].tolist())
cal = np.array([q in cal_set for q in prob])
d = F.frame(A, B, y)
dc, dt, yc, yt = d[cal].reset_index(drop=True), d[~cal].reset_index(drop=True), y[cal], y[~cal]
L = {}
for name in ("GDT", "CPT", "EV"):
    fn = F.fn_of(name)
    k = F.fit_kappa(F.raw_logit(fn, th[name], dc), yc)
    L[name] = F.row_loss(F._sig(k * F.raw_logit(fn, th[name], dt)), yt)
diff = L["GDT"] - L["CPT"]
At, Bt = A[~cal], B[~cal]


def has(O, f):
    return f(O)


sure = lambda O: O[:, 1] >= 1.0
rare = lambda O: (O[:, 1] < 1) & ((O[:, 1] <= 0.2) | (O[:, 1] >= 0.8))
neg = lambda O: (O[:, [0, 2]] < 0).any(1)
pos = lambda O: (O[:, [0, 2]] > 0).any(1)
groups = {
    "one option sure": sure(At) ^ sure(Bt),
    "neither sure": ~sure(At) & ~sure(Bt),
    "a rare branch (p<=.2 or >=.8)": rare(At) | rare(Bt),
    "no rare branch": ~(rare(At) | rare(Bt)),
    "gains only": ~neg(At) & ~neg(Bt),
    "losses only": ~pos(At) & ~pos(Bt),
    "mixed": (neg(At) | neg(Bt)) & (pos(At) | pos(Bt)),
}
# risky option = higher SD; does the chooser take risk more than GDT predicts?
riskyB = dt["sdB"].to_numpy() > dt["sdA"].to_numpy()
pt = F._sig(F.fit_kappa(F.raw_logit(F.fn_of("GDT"), th["GDT"], dc), yc) * F.raw_logit(F.fn_of("GDT"), th["GDT"], dt))
pc = F._sig(F.fit_kappa(F.raw_logit(F.fn_of("CPT"), th["CPT"], dc), yc) * F.raw_logit(F.fn_of("CPT"), th["CPT"], dt))
take_risky = np.where(riskyB, yt, 1 - yt)
pred_g = np.where(riskyB, pt, 1 - pt)
pred_c = np.where(riskyB, pc, 1 - pc)
out = {"all": {"n": int(len(diff)), "gdt_minus_cpt": float(diff.mean())}}
for g, m in groups.items():
    out[g] = {"n": int(m.sum()), "gdt_minus_cpt": float(diff[m].mean()),
              "observed_risky_rate": float(take_risky[m].mean()),
              "gdt_pred_risky": float(pred_g[m].mean()), "cpt_pred_risky": float(pred_c[m].mean())}
print(json.dumps(out, indent=1))

# Payoff magnitude: GDT's logit is linear in payoff scale, CPT's grows like scale**alpha.
mag = np.maximum(np.abs(At[:, [0, 2]]).max(1), np.abs(Bt[:, [0, 2]]).max(1)) * unit   # in points
q = np.quantile(mag, [0.2, 0.4, 0.6, 0.8])
bins = np.digitize(mag, q)
zg = F.raw_logit(F.fn_of("GDT"), th["GDT"], dt) * F.fit_kappa(F.raw_logit(F.fn_of("GDT"), th["GDT"], dc), yc)
zc = F.raw_logit(F.fn_of("CPT"), th["CPT"], dt) * F.fit_kappa(F.raw_logit(F.fn_of("CPT"), th["CPT"], dc), yc)
print("magnitude quintiles (max |outcome| in points):", [round(float(x), 1) for x in q])
for b in range(5):
    m = bins == b
    # observed sharpness: per-problem |choice rate - 0.5|, averaged over problems in the bin
    pb = np.unique(prob[~cal][m])
    obs = np.mean([abs(yt[m][prob[~cal][m] == p].mean() - 0.5) for p in pb])
    print(f"Q{b+1} n={int(m.sum()):5d} gdt-cpt={diff[m].mean():+.4f}  "
          f"mean|logit| GDT={np.abs(zg[m]).mean():.2f} CPT={np.abs(zc[m]).mean():.2f}  "
          f"observed mean|rate-.5| per problem={obs:.3f}  "
          f"GDT mean|p-.5|={np.abs(pt[m]-.5).mean():.3f} CPT={np.abs(pc[m]-.5).mean():.3f}")
