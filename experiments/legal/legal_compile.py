#!/usr/bin/env python3
"""ErisML compile handler for the legal-reversal Stage-4 NATS-bursting job (post-freeze).

Per opinion: run the ErisML compiler -> MoralTensorV3 (the k-dim moral vector, GDT coordinates) +
deontic gate failures. These are the raw per-opinion features; the pathology score S (which needs the
train-fit low-rank manifold for the off-manifold residual) is assembled in aggregate afterward.

  compile_opinion(text, extractor) -> {"moral_vector":[...k], "gate_failures":int, "deme":str, "ok":bool}

Modes:
  python3 legal_compile.py --smoke N [--extractor mock|llm]   # compile N opinions from the frozen
                                                              # district window on Atlas Postgres
The worker entrypoint (legal_compile_worker.py) imports compile_opinion and registers it with
run_worker(handlers={"compile": ...}).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _moral_vector(ir):
    """Extract the k-dim global moral vector from the IR's MoralTensorV3 (rank-1 (k,) or mean of
    rank-2 (k,n)). Returns (vector_list, note)."""
    tv = getattr(ir, "moral_tensor_v3", None)
    if tv is None:
        return None, "no moral_tensor_v3"
    import numpy as np
    arr = None
    for attr in ("data", "tensor", "values", "array"):
        v = getattr(tv, attr, None)
        if v is not None:
            arr = np.asarray(v, dtype=float)
            break
    if arr is None and hasattr(tv, "__array__"):
        arr = np.asarray(tv, dtype=float)
    if arr is None:
        return None, f"MoralTensorV3 has no array (attrs: {[a for a in dir(tv) if not a.startswith('_')][:8]})"
    if arr.ndim == 2:               # (k, n) per-stakeholder -> mean over stakeholders
        arr = arr.mean(axis=1)
    return arr.ravel().tolist(), f"rank{arr.ndim if arr.ndim else 1} k={arr.size}"


def _gate_failures(ir, text):
    """Count failed Kantian deontic gates. Try the IR's deontic projection; fall back to running
    DeonticProjection directly."""
    try:
        from erisml_compiler.projections.deontic import DeonticProjection
        res = DeonticProjection().evaluate(ir) if hasattr(DeonticProjection(), "evaluate") else None
        if res is not None:
            findings = getattr(res, "findings", None) or getattr(res, "gates", None) or []
            fails = sum(1 for f in findings if str(getattr(f, "status", getattr(f, "verdict", ""))).lower()
                        in ("fail", "failed", "forbidden", "violated"))
            return fails, f"{len(findings)} gates"
    except Exception as e:
        return None, f"deontic error: {type(e).__name__}: {str(e)[:80]}"
    return None, "no deontic findings"


_OPTS_CACHE = {}


def _make_options(extractor):
    import inspect
    from erisml_compiler.pipeline.orchestrator import CompileOptions
    from erisml_compiler.tiers import CompilerTier
    params = set(inspect.signature(CompileOptions).parameters)
    tiers = list(CompilerTier)
    if extractor == "llm":        # real run: LLM text extraction (needs the NRP endpoint)
        tier = next((t for t in tiers if t.value == "llm"), tiers[-1])
    else:                         # smoke: 'rule' extractor = rule/SRL text extraction, no LLM
        tier = next((t for t in tiers if t.value == "rules"), tiers[0])
    kw = {}
    if "tier" in params:
        kw["tier"] = tier
    if "extractor" in params:
        kw["extractor"] = extractor
    if not _OPTS_CACHE:
        _OPTS_CACHE["done"] = True
        print(f"   [CompileOptions params: {sorted(params)}; tiers: {[t.value for t in tiers]}; using tier={tier.value}]")
    return CompileOptions(**kw)


def compile_opinion(text, extractor="mock"):
    import os
    import tempfile
    from erisml_compiler.pipeline.orchestrator import compile_document
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(text)
        path = f.name
    try:
        ir = compile_document(path, _make_options(extractor))   # takes a file path, not raw text
    finally:
        os.unlink(path)
    vec, vnote = _moral_vector(ir)
    fails, gnote = _gate_failures(ir, text)
    return {"moral_vector": vec, "gate_failures": fails, "deme": str(getattr(ir, "deme_verdict", None)),
            "ok": vec is not None, "_vnote": vnote, "_gnote": gnote}


def _opinions(n):
    """Pull N opinions from the frozen district window on the Atlas replica."""
    sql = ("SELECT o.id, coalesce(nullif(o.plain_text,''), o.html_with_citations) "
           "FROM search_opinion o JOIN search_opinioncluster c ON c.id=o.cluster_id "
           "JOIN search_docket d ON d.id=c.docket_id JOIN search_court ct ON ct.id=d.court_id "
           "AND ct.jurisdiction='FD' "
           "WHERE c.date_filed BETWEEN '1990-01-01' AND '2015-12-31' "
           "AND length(o.plain_text) BETWEEN 1500 AND 12000 LIMIT %d;" % n)
    r = subprocess.run(["sudo", "-u", "postgres", "psql", "-d", "courtlistener", "-tAF", "\x01", "-c", sql],
                       capture_output=True, text=True, timeout=120)
    out = []
    for ln in r.stdout.strip().split("\n"):
        if "\x01" in ln:
            i, t = ln.split("\x01", 1)
            out.append((i, t))
    return out


def smoke(n, extractor):
    print(f"== Stage-4 compile smoke: {n} district opinions, extractor={extractor} ==")
    for oid, text in _opinions(n):
        res = compile_opinion(text, extractor=extractor)
        v = res["moral_vector"]
        print(f"opinion {oid}: ok={res['ok']} vec={('k=%d %s' % (len(v), [round(x,2) for x in v[:5]])) if v else None} "
              f"gate_failures={res['gate_failures']} deme={res['deme']}")
        print(f"   notes: {res['_vnote']} | {res['_gnote']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", type=int, default=0)
    ap.add_argument("--extractor", default="mock")
    a = ap.parse_args()
    if a.smoke:
        smoke(a.smoke, a.extractor)


if __name__ == "__main__":
    main()
