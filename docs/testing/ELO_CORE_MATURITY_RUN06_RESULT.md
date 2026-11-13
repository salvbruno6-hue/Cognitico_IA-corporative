# ELO Core Maturity — RUN-06

## Criterion

Timeout/retry/degradation/recovery behavior is proven end-to-end without creating a second execution authority.

## Operational implementation

RUN-06 uses a **real localhost HTTP transport harness** on the GitHub Actions runner. It deliberately produces a socket-level timeout, HTTP `503` unavailability and successful recovery. The original PR #520 demonstrated this **transport-only** behavior; it did **not** pass its retry evidence into the Core (Codex P1 at #523). This PR extends the existing integration test so every observed HTTP attempt, including provenance, historical identity and status, is attached as `ContextSource` and `ContextEvidence` before the canonical `CoreLoopEngine` executes.

`localhost HTTP event → bounded retry state → historical/provenance evidence → Core context/evidence → governed reasoning → recommendation/handoff`

The harness is test-only. It introduces no production provider, credential, external server, second executor, persistence authority or Core authority.

## Published GitHub evidence

Tested commit: `6bc26fa4f0065a634ad6bf2682d6036aa0986b69`

PR: `#520`

PR validation:

- ELO Behavioral Validation run `34920488550`: PASS; compile, tests and evidence upload completed.
- ELO PR1 Validation run `34920488515`: PASS; compile and tests completed.
- ELO Evolution Gate run `34920488523`: PASS; canonical validation, full suite, external access contract and decision handoff completed successfully.
- ELO Maintenance Coordinator run `34920488520`: PASS.

The PR was merged by squash as `79ed019903179cf9d4e03f2b7ff4c4f67bda3a80`. At the time of its post-merge verification, `main` pointed to that SHA; subsequent `main` commits do not invalidate the historical ON_MAIN evidence.

## Required cases and observed behavior

1. `TIMEOUT → SUCCESS`: real socket timeout followed by real HTTP success; attempts `[1, 2]` preserved.
2. `UNAVAILABLE → UNAVAILABLE → UNAVAILABLE`: real HTTP `503` on three attempts; retry bound reached; final state `DEGRADED`, never synthetic success.
3. `TIMEOUT → UNAVAILABLE → SUCCESS`: real timeout, real `503`, then real HTTP success on attempt 3.
4. Repeated identical local sequence: identical status sequence, attempt sequence, provenance and historical identity.

## Post-merge regression evidence

Main SHA: `79ed019903179cf9d4e03f2b7ff4c4f67bda3a80`

- ELO Behavioral Validation push run `34920608456`: PASS; compile, tests and test-evidence upload completed successfully.
- ELO PR1 Validation push run `34920608475`: PASS; compile and tests completed successfully.
- ELO Evolution Gate push run `34920608466`: PASS; canonical validation/full suite, external access contract and decision handoff completed successfully.
- ELO GitHub Pages push run `34920608431`: PASS; frontend build, artifact upload and deployment completed successfully.

## End-to-end Core evidence added in PR #523 (13 November 2026)

The new `tests/integration/test_core_critical_run06.py` paths reuse the **existing** `ContextResolutionEngine`, `DiagnosticScenario` and `CoreLoopEngine`. They attach one scoped source and context evidence per observed HTTP attempt, using the real attempt number, status, historical identity and transport provenance. The diagnostic observation comes from the **actual final attempt**, not from an unrelated synthetic capacity record.

- `TIMEOUT → SUCCESS`: Core receives both attempts and returns `RECOMMENDATION`, no handoff and no execution permission.
- `503 → 503 → 503`: Core receives all three failures, returns `HANDOFF`, retains a retry-exhausted GAP and does not propose an executable action.
- `TIMEOUT → 503 → SUCCESS`: Core receives all three attempts and reproducibly returns a governed recommendation; historical IDs stay attached to each attempt.
- Empty evidence is rejected rather than promoted to Core.

## Status and promotion gate

**Historical PR #520:** `PARTIAL — REAL_HTTP_TRANSPORT_PASS / ON_MAIN / POST_MERGE_CI_PASS`. The earlier GitHub runs are real and remain valid **for their original transport-only scope**, but they are insufficient to assert the full RUN-06 end-to-end criterion.

**Current PR #523:** `END_TO_END_CANDIDATE — REQUIRES_CURRENT_HEAD_CI / EVOLUTION_GATE / REVIEW / AUTHORIZATION / MERGE`. Do not record RUN-06=`PASS` in the canonical maturity matrix or claim `ON_MAIN` for this new evidence before the current-head validation and governed promotion. An approved test-only completion does not imply production capability.

## Residual boundary

The localhost runner is a **test fixture**, not a live external provider. This work does not claim production provider health, production incident recovery, or permission to execute operational actions. OPS-03 remains separate.
