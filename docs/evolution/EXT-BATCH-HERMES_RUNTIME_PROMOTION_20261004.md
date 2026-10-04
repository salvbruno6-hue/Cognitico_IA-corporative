# EXT-BATCH-HERMES — Runtime Promotion — 2026-10-04

## Scope

Promote the existing Hermes batch behavior over the canonical
`NativeMLOpsEvaluation` runtime path.

## Controls

- the existing batch boundary remains the admission authority;
- Hermes cannot create a canonical mutation or promotion authority;
- explicit authorization and bounded intake remain mandatory;
- `max_items` is bounded to 1..1000 and the batch is rejected when the declared item count exceeds the bound;
- runtime evidence is emitted from the existing `NativeMLOpsEvaluation.evaluate` path;
- repeatable runtime evidence is retained by the existing operational evidence collector.

## Evidence boundary

This promotion establishes governed runtime integration and repeatable runtime
evidence. It does not establish production outcome.

`FUNCTIONAL_CONTROLLED_GAIN → GOVERNED_HANDOFF → runtime integration → operational observation → OPERATIONAL_OUTCOME`

`production_proven` remains false until an actual attributable operational
environment supplies valid production evidence.
