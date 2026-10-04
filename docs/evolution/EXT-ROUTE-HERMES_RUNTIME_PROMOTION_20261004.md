# EXT-ROUTE-HERMES — Runtime Promotion — 2026-10-04

## Scope

Promote the existing Hermes routing behavior over the canonical
`IntelligenceRouter.route_and_execute` / `ExecutionRouter` path.

## Controls

- `ExecutionRouter` remains the canonical routing authority.
- Hermes cannot create routing authority or bypass governance.
- `provenance_verified` and explicit policy remain mandatory.
- fallback providers are bounded by `max_fallbacks` (0..3).
- a signal is rejected when the declared fallback set exceeds the bound.
- runtime evidence is emitted only for the governed Hermes route path.
- production proof remains pending.

## Evidence boundary

This promotion establishes governed runtime integration and repeatable runtime
evidence. It does not establish production outcome.

`FUNCTIONAL_CONTROLLED_GAIN → GOVERNED_HANDOFF → runtime integration → operational observation → OPERATIONAL_OUTCOME`
