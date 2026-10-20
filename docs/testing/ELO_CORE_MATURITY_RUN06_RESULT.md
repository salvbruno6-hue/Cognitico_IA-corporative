# ELO Core Maturity — RUN-06

## Criterion

Timeout/retry/degradation/recovery behavior is proven end-to-end without creating a second execution authority.

## Operational implementation

RUN-06 uses a **real localhost HTTP transport harness** on the GitHub Actions runner. It deliberately produces a socket-level timeout, HTTP `503` unavailability and successful recovery, while preserving each attempt's provenance and historical identity before composing the canonical ELO Core loop.

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

The PR was merged by squash as `79ed019903179cf9d4e03f2b7ff4c4f67bda3a80`, and `main` now points exactly to that SHA.

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

## Status

`PASS — REAL / MERGED / ON_MAIN / POST_MERGE_REGRESSION_PASS`

## Residual boundary

This evidence closes the gap between an internally simulated retry sequence and actual transport behavior on the CI runner. It does **not** claim live external-provider or production health; that remains a separate maturity criterion (OPS-03).
