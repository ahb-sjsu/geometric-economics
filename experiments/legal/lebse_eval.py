#!/usr/bin/env python3
"""Rigorous, HELD-OUT comparison of LeBSE vs base LaBSE on legal-semantic geometry.

Runs ON ATLAS, GPU-1. Evaluates on opinions the SimCSE fine-tune never saw (id beyond the
training window), so any gain is generalization, not memorization. Nothing here uses labels the
model was trained on -- the positive signal is the CourtListener citation graph.

Metrics (each reported for BOTH models; honest -- LeBSE can lose):
  1. anisotropy          mean cosine of RANDOM opinion pairs. LaBSE embeddings are famously
                         anisotropic (cone-shaped); SimCSE should DROP this toward 0 (more isotropic,
                         more usable geometry). Lower = better.
  2. cite_auroc          AUROC of cosine separating CITATION-LINKED opinion pairs (positive) from
                         random pairs (negative). Citation = legal-topical relatedness, so a better
                         legal encoder ranks linked pairs higher. Higher = better. This is the headline.
  3. cocite_auroc        same, but positives = pairs that both cite a COMMON third opinion
                         (co-citation ~ same doctrine). Independent structural signal. Higher = better.
  4. align / uniform     Wang-Isola (2020) intrinsic diagnostics on normalized embeddings:
                         alignment = E||x_a - x_b||^2 over linked pairs (lower=closer positives);
                         uniformity = log E exp(-2||x_i-x_j||^2) over random (lower=more spread).
  5. dAUROC 95% CI       paired bootstrap on cite_auroc (LeBSE - LaBSE). CI excluding 0 => the
                         legal adaptation moved retrieval by a real margin, not noise.

  python3 lebse_eval.py --n 4000 --pairs 3000 --train-n 6000 --lebse /archive/courtlistener/lebse
"""
import argparse, subprocess, sys
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


MIN_SNIP = 500   # min snippet chars (length filtered in Python, NOT SQL, to avoid full TOAST detoast)
# planner hints so it uses the big page cache (128MB shared_buffers but ~200GB OS cache) and index scans
_SET = "SET effective_cache_size='200GB'; SET work_mem='512MB'; SET jit=off; "


def psql(sql, timeout=600):
    r = subprocess.run(["sudo", "-u", "postgres", "psql", "-d", "courtlistener",
                        "-v", "ON_ERROR_STOP=1", "-tAF", "\x01", "-c", _SET + sql],
                       capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:800])
    return [ln for ln in r.stdout.split("\n") if ln.strip()]


def heldout_threshold(train_n):
    """Max opinion id used by SimCSE training (ORDER BY id LIMIT train_n in the length filter).
    Everything with a larger id is genuinely held out. Uses length() -> full detoast, so slow;
    pass --thr to skip (the value is printed once and stable)."""
    rows = psql("SELECT max(id) FROM (SELECT id FROM search_opinion "
                "WHERE length(plain_text) BETWEEN 1500 AND 25000 ORDER BY id LIMIT %d) t;" % train_n,
                timeout=1200)
    return int(rows[0])


def snippet(col):
    # PARTIAL detoast: left() reads only the first TOAST chunks, then collapse whitespace. Avoids
    # decompressing whole opinions. length() in SQL would force a FULL detoast (100GB) -> do it in Python.
    # NOTE: standard string '\s+' (NOT E'\s+' -- E'' mis-parses \s as literal 's' and leaves newlines,
    # which truncates snippets on the Python split). standard_conforming_strings=on passes \s+ verbatim.
    return r"regexp_replace(left(%s, 3000), '\s+', ' ', 'g')" % col


def fetch_snips(ids):
    """Batch-fetch snippets for a set of opinion ids via indexed PK lookups (id = ANY(array)).
    Partial detoast only for these ids; NO giant join, NO full-table scan."""
    ids = sorted(set(int(i) for i in ids))
    if not ids:
        return {}
    arr = "{" + ",".join(str(i) for i in ids) + "}"
    rows = psql("SELECT id, %s FROM search_opinion WHERE id = ANY('%s'::int[]);"
                % (snippet("plain_text"), arr), timeout=600)
    d = {}
    for ln in rows:
        if "\x01" in ln:
            i, t = ln.split("\x01", 1)
            d[int(i)] = t
    return d


def load_pool(thr, n):
    # ORDER BY id DESC = NEWEST held-out opinions (best plain_text; oldest ids are scanned/short).
    rows = psql("SELECT id, %s FROM search_opinion WHERE id > %d ORDER BY id DESC LIMIT %d;"
                % (snippet("plain_text"), thr, n * 2))   # over-fetch; Python length filter trims
    ids, texts = [], []
    for ln in rows:
        if "\x01" in ln:
            i, t = ln.split("\x01", 1)
            if len(t) >= MIN_SNIP:
                ids.append(int(i)); texts.append(t)
    return ids[:n], texts[:n]


def _edge_ids_to_pairs(edge_rows):
    """edge_rows: lines 'a_id\\x01b_id'. Fetch snippets once for all ids, build (id,snip) pairs."""
    edges = []
    for ln in edge_rows:
        p = ln.split("\x01")
        if len(p) == 2:
            edges.append((int(p[0]), int(p[1])))
    snips = fetch_snips([i for e in edges for i in e])
    A, B = [], []
    for a, b in edges:
        sa, sb = snips.get(a), snips.get(b)
        if sa and sb and len(sa) >= MIN_SNIP and len(sb) >= MIN_SNIP:
            A.append((a, sa)); B.append((b, sb))
    return A, B


def citation_pairs(thr, k):
    """Held-out citation edges (both endpoints past the training id cut). Phase 1: pick edge id pairs
    (int-only, indexed on the PK -> fast). Phase 2: batch-fetch snippets. Avoids the 3-way join."""
    rows = psql("SELECT citing_opinion_id, cited_opinion_id FROM search_opinionscited "
                "WHERE citing_opinion_id > %d AND cited_opinion_id > %d ORDER BY id DESC LIMIT %d;"
                % (thr, thr, k * 2), timeout=600)
    return _edge_ids_to_pairs(rows)


def cocitation_pairs(thr, k):
    """Pairs (x,y) that both cite a common opinion z -> same-doctrine proxy. Phase 1: self-join on
    cited_opinion_id for id pairs only (no text). Phase 2: batch-fetch snippets."""
    rows = psql("SELECT o1.citing_opinion_id, o2.citing_opinion_id FROM search_opinionscited o1 "
                "JOIN search_opinionscited o2 ON o2.cited_opinion_id=o1.cited_opinion_id "
                " AND o2.citing_opinion_id > o1.citing_opinion_id "
                "WHERE o1.citing_opinion_id > %d AND o2.citing_opinion_id > %d "
                "ORDER BY o1.id DESC LIMIT %d;"
                % (thr, thr, k * 2), timeout=600)
    return _edge_ids_to_pairs(rows)


def encode(model, texts, bs=128):
    return model.encode(texts, batch_size=bs, convert_to_numpy=True,
                        normalize_embeddings=True, show_progress_bar=False)


def auroc(pos, neg):
    from sklearn.metrics import roc_auc_score
    y = np.r_[np.ones(len(pos)), np.zeros(len(neg))]
    return roc_auc_score(y, np.r_[pos, neg])


def eval_model(name, st_model, pool_texts, posA, posB, coA, coB, rng):
    E = encode(st_model, pool_texts)                       # normalized pool embeddings
    n = len(E)
    # random-pair cosine (anisotropy + negatives + uniformity)
    ri, rj = rng.integers(0, n, 20000), rng.integers(0, n, 20000)
    m = ri != rj; ri, rj = ri[m], rj[m]
    rand_cos = np.sum(E[ri] * E[rj], axis=1)
    anisotropy = float(rand_cos.mean())
    # positive citation pairs
    pa = encode(st_model, [t for _, t in posA]); pb = encode(st_model, [t for _, t in posB])
    pos_cos = np.sum(pa * pb, axis=1)
    neg_cos = rand_cos[: len(pos_cos)]
    cite = auroc(pos_cos, neg_cos)
    # co-citation pairs (secondary; may be empty -> report NaN, don't crash)
    if coA:
        ca = encode(st_model, [t for _, t in coA]); cb = encode(st_model, [t for _, t in coB])
        coc = np.sum(ca * cb, axis=1)
        cocite = auroc(coc, rand_cos[: len(coc)])
    else:
        cocite = float("nan")
    # Wang-Isola
    align = float(np.mean(np.sum((pa - pb) ** 2, axis=1)))
    d2 = np.sum((E[ri] - E[rj]) ** 2, axis=1)
    uniform = float(np.log(np.mean(np.exp(-2.0 * d2))))
    print(f"\n[{name}]  anisotropy={anisotropy:+.4f}  cite_auroc={cite:.4f}  "
          f"cocite_auroc={cocite:.4f}  align={align:.4f}  uniform={uniform:.4f}")
    return {"name": name, "anisotropy": anisotropy, "cite_auroc": cite, "cocite_auroc": cocite,
            "align": align, "uniform": uniform, "pos_cos": pos_cos, "neg_cos": neg_cos}


def bootstrap_dauroc(a, b, rng, B=2000):
    """Paired bootstrap CI on cite_auroc(LeBSE) - cite_auroc(LaBSE). Resample the SAME pair indices
    for both models so the comparison is paired."""
    from sklearn.metrics import roc_auc_score
    npos, nneg = len(a["pos_cos"]), len(a["neg_cos"])
    diffs = []
    for _ in range(B):
        pi = rng.integers(0, npos, npos); ni = rng.integers(0, nneg, nneg)
        y = np.r_[np.ones(npos), np.zeros(nneg)]
        da = roc_auc_score(y, np.r_[a["pos_cos"][pi], a["neg_cos"][ni]])
        db = roc_auc_score(y, np.r_[b["pos_cos"][pi], b["neg_cos"][ni]])
        diffs.append(da - db)
    diffs = np.array(diffs)
    return float(diffs.mean()), float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=4000, help="held-out pool size")
    ap.add_argument("--pairs", type=int, default=3000, help="citation / co-citation positive pairs")
    ap.add_argument("--train-n", type=int, default=6000, help="opinions used by SimCSE (for held-out cut)")
    ap.add_argument("--thr", type=int, default=0, help="held-out id cut (skip the slow length()-based compute; prior run printed 9400)")
    ap.add_argument("--lebse", default="/archive/courtlistener/lebse")
    ap.add_argument("--base", default="sentence-transformers/LaBSE")
    a = ap.parse_args()

    import torch
    from sentence_transformers import SentenceTransformer
    print(f"[eval] cuda={torch.cuda.is_available()} dev="
          f"{torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu'}")
    rng = np.random.default_rng(0)

    thr = a.thr or heldout_threshold(a.train_n)
    print(f"[eval] held-out cut: opinion id > {thr} (train used first {a.train_n} by id)")
    ids, pool = load_pool(thr, a.n)
    posA, posB = citation_pairs(thr, a.pairs)
    coA, coB = cocitation_pairs(thr, a.pairs)
    print(f"[eval] pool={len(pool)}  citation_pairs={len(posA)}  cocitation_pairs={len(coA)}")
    if len(posA) < 200:
        print("[eval] WARNING: few held-out citation pairs; widen --train-n cut or --pairs")

    base = SentenceTransformer(a.base, device="cuda")
    lebse = SentenceTransformer(a.lebse, device="cuda")
    rb = eval_model("LaBSE", base, pool, posA, posB, coA, coB, np.random.default_rng(1))
    rl = eval_model("LeBSE", lebse, pool, posA, posB, coA, coB, np.random.default_rng(1))

    md, lo, hi = bootstrap_dauroc(rl, rb, np.random.default_rng(7))
    print("\n==================== VERDICT ====================")
    print(f"  cite_auroc   LaBSE {rb['cite_auroc']:.4f}  ->  LeBSE {rl['cite_auroc']:.4f}")
    print(f"  cocite_auroc LaBSE {rb['cocite_auroc']:.4f}  ->  LeBSE {rl['cocite_auroc']:.4f}")
    print(f"  anisotropy   LaBSE {rb['anisotropy']:+.4f}  ->  LeBSE {rl['anisotropy']:+.4f}  (lower=better)")
    print(f"  d(cite_auroc) = {md:+.4f}   95% CI [{lo:+.4f}, {hi:+.4f}]   "
          f"{'SIGNIFICANT (CI excludes 0)' if (lo > 0 or hi < 0) else 'not significant'}")
    better = md > 0 and lo > 0
    print(f"  => LeBSE {'IMPROVES' if better else 'does NOT clearly improve'} held-out legal retrieval.")
    print("=================================================")


if __name__ == "__main__":
    main()
