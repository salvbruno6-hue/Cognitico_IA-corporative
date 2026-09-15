# ELO Core Maturity — RUN-06

## Criterion

Timeout/retry/degradation/recovery behavior is proven end-to-end without creating a second execution authority.

## Evidence rule

Documentation is not PASS evidence. PASS requires a GitHub Actions execution tied to the tested commit, with the RUN-06 integration test and canonical validation succeeding.

## Operational path

The test composes the existing provider-independent bounded retry simulation with the canonical ELO Core loop:

`provider event → bounded retry state → historical/provenance evidence → Core context/evidence → governed reasoning → recommendation/handoff`

The implementation deliberately does not claim live provider, credential, network or production health.

## Required cases

1. `TIMEOUT → TIMEOUT → TIMEOUT` remains bounded and degraded.
2. `TIMEOUT → SUCCESS` recovers on the bounded retry without rewriting history.
3. `UNAVAILABLE` becomes `HANDOFF`, never synthetic success.
4. Repeated identical input produces identical evidence, attempt sequence, provenance and historical identity.

## Current status

`EXECUTION_REQUESTED — awaiting GitHub Actions evidence`

## Required published evidence

- tested commit SHA;
- GitHub Actions workflow/run identifier;
- exact command or test target;
- environment;
- observed result;
- canonical/full-suite result;
- residual risk.

Only after those fields are backed by completed GitHub Actions results may RUN-06 be reclassified from `DEFINED` to `PASS`.
