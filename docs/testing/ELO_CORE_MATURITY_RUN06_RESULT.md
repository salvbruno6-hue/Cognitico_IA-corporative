# ELO Core Maturity — RUN-06

## Criterion

Timeout/retry/degradation/recovery behavior is proven end-to-end without creating a second execution authority.

## Evidence rule

Documentation is not PASS evidence. PASS requires a GitHub Actions execution tied to the tested commit, with the RUN-06 integration test and canonical validation succeeding.

## Operational path

The test now uses a **real localhost HTTP transport harness** on the GitHub Actions runner. It deliberately produces transport-level outcomes and records each attempt before composing the canonical ELO Core loop:

`localhost HTTP event → bounded retry state → historical/provenance evidence → Core context/evidence → governed reasoning → recommendation/handoff`

The harness is test-only: it introduces no production provider, credential, external server, second executor, persistence authority or Core authority.

## Required cases

1. `TIMEOUT → SUCCESS` uses a real socket timeout followed by a real HTTP success, with attempts 1 and 2 preserved.
2. `UNAVAILABLE → UNAVAILABLE → UNAVAILABLE` uses real HTTP `503` responses, reaches the retry bound, and remains `DEGRADED`.
3. `TIMEOUT → UNAVAILABLE → SUCCESS` combines real transport timeout and HTTP failure before real recovery on attempt 3.
4. Repeating the same local sequence produces the same evidence status, attempt sequence, provenance and historical identity.

## Current status

`EXECUTION_REQUESTED — awaiting GitHub Actions evidence for the real transport harness`

## Required published evidence

- tested commit SHA;
- GitHub Actions workflow/run identifier;
- exact command or test target;
- environment;
- observed transport results and attempt counts;
- canonical/full-suite result;
- residual risk.

Only after those fields are backed by completed GitHub Actions results may RUN-06 be reclassified from `DEFINED` to `PASS`.

## Residual boundary

This closes the evidence gap between an internally simulated retry sequence and an actual transport event on the CI runner. It does **not** claim live external-provider or production health; that remains a separate maturity criterion.
