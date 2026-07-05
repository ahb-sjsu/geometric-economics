#!/usr/bin/env python3
"""Score the frozen cross-domain-coupling prereg (prereg-coupling-v1) on GPS data.

Falk, Becker, Dohmen, Enke, Huffman, Sunde (2018 QJE), "Global Evidence on Economic Preferences."
Global Preferences Survey: risk, patience, positive/negative reciprocity, altruism, trust for ~80,000
people in 76 countries. Data are registration-gated (briq merged into IZA in 2024) at
https://gps.iza.org/downloads (mirror https://gps.econ.uni-bonn.de/downloads) -- NOT redistributed
here. Unzip the GPS package anywhere under `raw_gps/` and run; this script globs for the .dta with the
six preference columns (country-level preferred; individual-level also works).

The prereg (PREREG_cross_domain_coupling.md, sha256 1eac580f...) predicts, from GDT's one-metric claim:
  P1 (sign)  the RISK angle and the SOCIAL (other-regard) angle are POSITIVELY coupled.
             Proxy here: corr(risktaking, altruism/trust/posrecip). Incumbents (separate CPT +
             inequality-aversion) predict ZERO coupling.
  P2 (rank)  the coupling is RANK-1: one latent metric factor explains it.
             Proxy: eigenvalue spectrum of the 6-preference correlation matrix (rank-1 => lambda_1
             dominates; rank-2 => two bundles => the STRONG rank-1 prereg fails but the broader
             low-rank claim, at rank 2, survives -- the Ruggeri "rank-2 sweet spot").

HONEST: GPS measures are survey/experimental preference *scores*, not the choice-fit geometric angles of
the paper's own risk/social encodings. This is therefore a PROXY test of the prereg, not the exact
same-subject angle-to-angle test; the individual-level choice-fit test remains the gold standard. Falk
et al. already report two bundles (risk+patience; altruism+posrecip+trust), so P1/P2 may well be
falsified -- reported either way, against a hash frozen before these data were opened.

    python gps_coupling.py
"""
from __future__ import annotations

import os
import sys
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PREFS = ["risktaking", "patience", "posrecip", "negrecip", "altruism", "trust"]
SOCIAL = ["altruism", "trust", "posrecip"]  # the other-regarding coordinate(s)


def find_data():
    """Glob any .dta under raw_gps/ and return the ones containing the 6 preference columns,
    country-level (fewer rows) preferred over individual-level."""
    import glob
    import pandas as pd
    root = os.path.join(HERE, "raw_gps")
    hits = []
    for f in glob.glob(os.path.join(root, "**", "*.dta"), recursive=True):
        try:
            cols = [c.lower() for c in pd.read_stata(f, chunksize=1).__next__().columns]
        except Exception:
            try:
                cols = [c.lower() for c in pd.read_stata(f).columns]
            except Exception:
                continue
        if all(p in cols for p in PREFS):
            # prefer country-level (folder/filename hint), else individual
            is_country = "country" in f.lower() and "individual" not in f.lower()
            hits.append((0 if is_country else 1, f))
    hits.sort()
    return hits[0][1] if hits else None


def main():
    import pandas as pd
    from scipy import stats

    path = find_data()
    if path is None:
        print("GPS data (.dta with the 6 preference columns) not found under raw_gps/.")
        print("Get the GPS package from https://gps.iza.org/downloads")
        print("  (mirror https://gps.econ.uni-bonn.de/downloads; briq merged into IZA in 2024),")
        print("  or the community country-level mirror github.com/scerioli/Global-Preferences-Survey.")
        print("Unzip anywhere under experiments/datasets/raw_gps/ and re-run.")
        print("(The Harvard Dataverse zip ships only the Stata do-files, not the data.)")
        return

    level = "country" if "Country" in path else "individual"
    df = pd.read_stata(path)
    df.columns = [c.lower() for c in df.columns]
    miss = [p for p in PREFS if p not in df.columns]
    if miss:
        print(f"Missing expected preference columns: {miss}\nHave: {list(df.columns)[:30]}")
        return
    X = df[PREFS].apply(pd.to_numeric, errors="coerce").dropna()
    n = len(X)
    print(f"== GPS {level}-level: {n} rows x {len(PREFS)} preferences ==\n")

    # ---- correlation matrix (Spearman, matching the do-files) ----
    R = np.zeros((6, 6)); P = np.zeros((6, 6))
    for i in range(6):
        for j in range(6):
            R[i, j], P[i, j] = stats.spearmanr(X.iloc[:, i], X.iloc[:, j])
    print("Spearman correlation matrix (rows/cols = " + ", ".join(PREFS) + "):")
    for i, p in enumerate(PREFS):
        print("  " + p.ljust(10) + " " + " ".join(f"{R[i,j]:+.2f}" for j in range(6)))

    # ---- P1: risk <-> social coupling (sign) ----
    ri = PREFS.index("risktaking")
    print("\n== P1 (sign): risk <-> social coupling ==")
    p1_vals = []
    for s in SOCIAL:
        j = PREFS.index(s)
        r, pv = R[ri, j], P[ri, j]
        p1_vals.append(r)
        star = "***" if pv < 0.001 else "**" if pv < 0.01 else "*" if pv < 0.05 else "ns"
        print(f"  corr(risktaking, {s:<9}) = {r:+.3f}  (p={pv:.3g}, {star})")
    mean_soc = float(np.mean(p1_vals))
    # contrast: within-social block coherence (should be high if 'social' is one coordinate)
    soc_idx = [PREFS.index(s) for s in SOCIAL]
    within = [R[a, b] for k, a in enumerate(soc_idx) for b in soc_idx[k + 1:]]
    print(f"  mean risk-social corr = {mean_soc:+.3f}   |   mean within-social corr = {np.mean(within):+.3f}")

    # ---- P2: rank of the 6x6 correlation matrix ----
    evals = np.sort(np.linalg.eigvalsh(R))[::-1]
    ev = evals / evals.sum()
    print("\n== P2 (rank): eigenvalue spectrum of the 6-preference correlation matrix ==")
    print("  variance share: " + " ".join(f"PC{i+1}={ev[i]*100:.0f}%" for i in range(6)))
    print(f"  PC1 alone = {ev[0]*100:.0f}%   PC1+PC2 = {(ev[0]+ev[1])*100:.0f}%   lambda1/lambda2 = {evals[0]/evals[1]:.2f}")

    # ---- verdict against the frozen prereg ----
    print("\n== Verdict vs prereg-coupling-v1 (frozen before these data) ==")
    p1_pass = mean_soc > 0.10 and all(v > 0 for v in p1_vals)
    rank1 = ev[0] > 0.60 and evals[0] / evals[1] > 3.0
    rank2 = (ev[0] + ev[1]) > 0.70 and not rank1
    print(f"  P1 (risk<->social POSITIVE): {'PASS' if p1_pass else 'FAIL'} "
          f"(mean risk-social corr {mean_soc:+.3f}).")
    if rank1:
        print(f"  P2 (RANK-1 coupling): PASS (PC1={ev[0]*100:.0f}%, l1/l2={evals[0]/evals[1]:.1f}).")
    elif rank2:
        print(f"  P2 (RANK-1): FAIL, but structure is RANK-2 (PC1+PC2={(ev[0]+ev[1])*100:.0f}%) -- "
              f"the strong rank-1 prereg is falsified; the broader low-rank claim survives at rank 2 "
              f"(the two bundles Falk et al. report; echoes the Ruggeri rank-2 sweet spot).")
    else:
        print(f"  P2: FAIL -- structure is not low-rank (PC1+PC2={(ev[0]+ev[1])*100:.0f}%).")
    print("\nHONEST: proxy test (survey scores, not choice-fit angles); the same-subject angle-to-angle "
          "test remains the gold standard. Reported against a hash frozen before the data were opened.")


if __name__ == "__main__":
    main()
