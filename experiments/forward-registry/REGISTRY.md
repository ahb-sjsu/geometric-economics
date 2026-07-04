# Forward-prediction registry

Pre-registered, hashed, timestamped **sign-predictions** about future events where the geometric
model and scalar economics **provably diverge on a non-monetary coordinate**. When an event resolves,
later history verifies (or falsifies) the prediction — the scientific gold standard, and immune to the
retrodiction critique because the prediction is frozen *before* the outcome exists.

## Protocol

1. A prediction is added to `predictions.json` with a `frozen` block: the claim, the coordinate, the
   **scalar** prediction, the **geometry** prediction, the resolution criterion, and the falsifier.
2. `python registry.py` writes `registry.lock.json` — a sha256 of each frozen block. The hash +
   `registered` date are the anti-backfit proof. Commit + tag (e.g. `forward-vN`).
3. When an event resolves, append a `resolution` block to that entry (outcome + source). The `frozen`
   block and its hash **never change**; `python registry.py --verify` confirms this.

## Discipline (what keeps it credible)

- **Sign-level only.** Direction, not magnitude (magnitude is not yet calibrated).
- **Mechanism-level, not macro.** No "we predicted the recession." Each prediction names a specific
  coordinate manipulation with a concrete resolution rule.
- **A stated falsifier per prediction.** If the scalar sign is observed, the geometry loses that row.
- **Frozen before resolution.** The hash is worthless if edited after the fact; `--verify` guards it.

## Currently registered (all open)

| id | coordinate | geometry predicts (vs scalar) | resolves on |
|---|---|---|---|
| PG-2026-001 | d1→d6/d7 | incentive **backfires** in high-norm domains (vs improves) | any incentive field-experiment w/ control |
| PG-2026-002 | d8 | compliance **falls** after legitimacy shock (vs unchanged) | identified legitimacy shocks, fixed rates |
| PG-2026-003 | d7/d8 | civic-frame carbon price **more accepted** (vs identical) | frame-varying referenda/trials at equal cost |
| PG-2026-004 | d9 | epistemic-ambiguity framing **shifts** protective choice (vs identical) | risk-communication experiments, fixed stated prob |

These mirror the historical ledger's classes (crowding-out, legitimacy, framing, epistemic) — but
forward. Each is a standing bet that resolves as qualifying studies/policies appear.
