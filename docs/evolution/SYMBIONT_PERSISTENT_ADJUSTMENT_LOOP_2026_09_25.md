# Simbiont Persistent Adjustment Loop — 2026-09-25

## Rule

When a candidate already has **strong evidence of gain** and **strong evidence of evolutionary impact**, absence of its own production execution does not stop the Symbiont's improvement work.

The existing capability-evolution review now exposes a governed planning signal:

- `persistent_adjustment_required=true`
- `production_pending=true`

The signal means the candidate remains in an adjustment cycle until an authorized production observation is obtained.

## Cycle

`analyze → correct → Lab retest → repeat → seek authorized production → production evidence → existing Evolution Gate`

## Boundaries

- Reuses the existing `CapabilityEvolutionReview`.
- No new Evolution Gate, Registry, Memory or promotion authority.
- Lab/indirect evidence is never relabeled as production evidence.
- No automatic Core/Soul mutation.
- No automatic promotion.
- The mechanism plans and maintains the work state; the existing governed runtime/deployment boundary remains responsible for actual production execution.

## Completion

The loop is considered to have reached its production objective only when the candidate has its own governed production observation. Until then, the Symbiont continues identifying the next justified correction and retest.
