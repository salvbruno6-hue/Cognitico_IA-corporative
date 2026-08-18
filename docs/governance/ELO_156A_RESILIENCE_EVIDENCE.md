# ELO-156A — Deterministic Resilience Evidence

This artifact provides provider-independent operational simulations for ELO-156. It does not claim production resilience or external-provider availability.

## Evidence states

- `TIMEOUT`: provider did not answer within the simulated attempt.
- `UNAVAILABLE`: provider is unavailable; the ELO must hand off rather than fabricate success.
- `DEGRADED`: bounded retries were exhausted without a successful provider response.
- `RECOVERED`: a later bounded retry succeeded.
- `HANDOFF`: external execution/evidence is required and remains unresolved.

## Invariants

1. Retry count is bounded.
2. The same input produces the same simulated outcome.
3. Provenance is preserved across attempts.
4. Historical evidence is append-only; recovery does not rewrite the timeout record.
5. Provider unavailability never becomes synthetic PASS.
6. These simulations are not evidence that a real provider, credential, network or production system is healthy.

## Relationship to ELO-156

This closes the deterministic simulation portion of timeout/retry/degradation/recovery. Real external-provider evidence remains an explicit external gate and must be supplied separately.
