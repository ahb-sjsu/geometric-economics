# FREEZE_PROTOCOL — how every frozen prediction in this program is anchored

*One protocol for all pre-registrations ([[prereg-sigma-v1]], [[prereg-coupling-v1]],
[[prereg-legal-reversal-v1]], and future ones). The credibility of the whole program rests on these
freezes holding up to a skeptical third party, so the anchoring is layered and cryptographic, not
"trust the registry."*

## What a freeze must guarantee (four layers)

| Guarantee | Mechanism | Independent of |
|---|---|---|
| **Authorship** — who froze it | GPG-signed tag (key `0C7E…4456`) | — |
| **Content integrity** — text unaltered | `sha256sum` recorded in-file **and** as a `.sha256` sidecar | git's SHA-1 DAG (second, stronger leg) |
| **Relative ordering** — prediction precedes data | git Merkle DAG: a commit SHA commits to its entire ancestry; the prereg is an ancestor of every data/results commit | commit timestamps (which are forgeable) |
| **Absolute time** — existed before real-world date T | OpenTimestamps (Bitcoin anchor) + GitHub push receive-time | any trusted party (OTS is decentralized) |

Commit timestamps alone prove **nothing** (author-set, backdatable). The Merkle DAG proves *ordering*
to yourself; OTS/GitHub proves *pre-existence* to anyone.

## The sequence (do not reorder)

**Freeze the FINAL artifacts — no placeholders, no TODO fields.** A timestamp on a draft scope anchors
nothing binding.

```bash
# 0. finalize: every parameter fixed (scope JSON has no TODO_*), analysis plan complete.
# 1. content hash (SHA-256, independent of git):
sha256sum PREREG_<name>.md <name>_scope.json > prereg-<name>-v1.sha256

# 2. commit + SIGNED tag (authorship + DAG position):
git add PREREG_<name>.md <name>_scope.json prereg-<name>-v1.sha256
git commit -S -m "Freeze prereg-<name>-v1"
git tag -s prereg-<name>-v1 -m "frozen; sha256 in sidecar"

# 3. absolute-time anchor (private-safe: stamps the HASH, not the content):
ots stamp prereg-<name>-v1.sha256          # -> prereg-<name>-v1.sha256.ots  (commit it too)

# 4. push (GitHub receive-time anchor; also off-machine backup):
git push origin main --tags

# 5. ONLY NOW pull the data / link labels / run the model.
```

If OTS is not installed: `pip install opentimestamps-client` (the `ots` CLI). If the repo stays
private and unpushed, step 3 (OTS) is what carries the third-party proof — it does not require
revealing the content, only the hash. Step 4 to GitHub is the backup/redundant anchor.

## Ordering rule (the thing that must never be violated)

> **Data pull and label linkage commits must be DESCENDANTS of the freeze tag, never ancestors.**

Because each commit hashes its parents, once the freeze is an ancestor of the results, the prediction
cannot be silently edited after seeing outcomes without invalidating every downstream SHA, the signed
tag, the sidecar sha256, and the OTS proof simultaneously. That conjunction is what makes it credible.

## Verification (what a reviewer runs)

```bash
git verify-tag prereg-<name>-v1                 # GPG authorship
sha256sum -c prereg-<name>-v1.sha256            # content unaltered
ots verify prereg-<name>-v1.sha256.ots          # existed before a Bitcoin block time
git merge-base --is-ancestor prereg-<name>-v1 HEAD && echo "prediction precedes results"
```

## What this does NOT prove (state it honestly)

- **That the outcome data was not consulted before writing the prediction.** No hash chain can
  establish that — it is a conduct claim. Mitigation: freeze *before* the corpus is pulled, and prefer
  designs whose labels are **external / not-yet-materialized** at freeze time (e.g., future appellate
  reversals, forward-prediction registries), so there is nothing to peek at.
- **That the frozen artifacts are the *complete* analysis plan.** Anything not in the frozen files is
  exploratory by definition and must be reported as such.

## Program freeze registry

| Tag | Predicts | Status |
|---|---|---|
| `prereg-sigma-v1` | low-rank Σ (H1–H4) | frozen; scored (survived) |
| `prereg-v1` / `prereg-v2` | projection-gap signs | frozen; scored / redesigned |
| `prereg-coupling-v1` | cross-domain angle coupling | frozen; awaiting GPS data |
| `prereg-legal-reversal-v1` | geometric pathology → reversal | **DRAFT** — finalize `legal_reversal_scope.json`, then run this protocol |
