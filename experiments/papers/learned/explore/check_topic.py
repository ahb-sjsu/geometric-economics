#!/usr/bin/env python3
"""DEVELOPMENT. Is discovered direction 0 moral gravity, or a family-versus-errands topic axis?

Its extremes were family estrangement or cruelty (low) against chores and transactions (high). A topic
reading predicts that a kinship-word indicator explains most of it, and that among actions that mention
no kin the direction loses its spread and its ordering. A gravity reading predicts that the direction
still orders non-kin actions from grave to trivial.

Reports: R^2 of direction 0 from the kin indicator; its spread within and outside kin texts; and the
extreme exemplars among non-kin texts, for reading.

    python check_topic.py EMB_DIR OUT_DIR OUT.json
"""
import json
import os
import re
import sys

import numpy as np

KIN = re.compile(r"\b(mom|mother|mum|dad|father|parents?|sister|brother|siblings?|grandma|grandmother|grandpa|"
                 r"grandfather|grandparents?|aunt|uncle|cousin|son|daughter|kids?|children|child|wife|husband|"
                 r"fianc\w*|in-law|in law|niece|nephew|family|stepmom|stepdad|stepmother|stepfather|baby)\b", re.I)


def main(emb_dir, out_dir, out):
    lab = np.load(os.path.join(emb_dir, "labse.npz"), allow_pickle=True)
    texts, E = lab["texts"].tolist(), lab["vecs"]
    U = np.load(os.path.join(out_dir, "gdt_labse.npz"))["U"]
    _, _, Vt = np.linalg.svd(U, full_matrices=False)
    kin = np.array([bool(KIN.search(t)) for t in texts])
    res = {"texts": len(texts), "kin_share": float(kin.mean()), "directions": []}
    for i in range(3):
        s = E @ Vt[i]
        if np.corrcoef(s, kin)[0, 1] > 0:      # orient so that kin texts sit at the low end, as in discover_dims
            s = -s
        r = float(np.corrcoef(s, kin)[0, 1])
        nk = s[~kin]
        order = np.argsort(nk)
        nk_texts = [texts[j] for j in np.where(~kin)[0]]
        res["directions"].append({
            "index": i, "r_with_kin": r, "R2_from_kin": r * r,
            "sd_all": float(s.std()), "sd_kin": float(s[kin].std()), "sd_nonkin": float(nk.std()),
            "mean_kin_minus_nonkin_in_sd": float((s[kin].mean() - nk.mean()) / s.std()),
            "nonkin_low_end": [nk_texts[j] for j in order[:10]],
            "nonkin_high_end": [nk_texts[j] for j in order[-10:]]})
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
