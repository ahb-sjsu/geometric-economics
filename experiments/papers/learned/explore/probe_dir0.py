import re, sys
import numpy as np
lab = np.load(sys.argv[1], allow_pickle=True)
texts, E = lab["texts"].tolist(), lab["vecs"]
U = np.load(sys.argv[2])["U"]
v = np.linalg.svd(U, full_matrices=False)[2][0]
s = E @ v
kin = re.compile(r"\b(mom|mother|dad|father|parents?|sister|brother|grandma|grandpa|family|wife|husband|son|daughter)\b", re.I)
if np.corrcoef(s, [bool(kin.search(t)) for t in texts])[0, 1] > 0:
    s = -s                                   # same orientation as before: harm to close others at the LOW end
pct = s.argsort().argsort() / (len(s) - 1)
groups = {
    "impersonal grave: steal/theft/fraud/scam/shoplift": r"\b(steal\w*|stole|theft|fraud|scam\w*|shoplift\w*|embezzl\w*)\b",
    "violence: hit/punch/assault/beat/kill": r"\b(hit|hitting|punch\w*|assault\w*|beat\w*|kill\w*|stab\w*)\b",
    "strangers/customers/coworkers": r"\b(stranger\w*|customer\w*|coworker\w*|co-worker\w*|landlord|neighbou?r\w*|boss)\b",
    "close non-kin: friend/girlfriend/boyfriend/partner/roommate": r"\b(friend\w*|girlfriend|boyfriend|partner|roommate\w*|flatmate\w*|bf|gf)\b",
    "kin": kin.pattern,
    "lying/cheating": r"\b(lie|lying|lied|cheat\w*)\b",
}
for name, pat in groups.items():
    m = np.array([bool(re.search(pat, t, re.I)) for t in texts])
    ex = [texts[j] for j in np.where(m)[0][np.argsort(pct[m])][[0, m.sum() // 2, -1]]] if m.sum() > 2 else []
    print(f"{name}: n={m.sum()} median percentile={np.median(pct[m]):.2f} IQR=({np.percentile(pct[m],25):.2f},{np.percentile(pct[m],75):.2f})")
    for t in ex:
        print("     ", t[:100])
