# ELO — Hermes-derived Flow Complementarity Adapter

**Status:** experimental implementation candidate.

## Why this exists

The Hermes scan did not reveal a ready-made generic flow-composition registry. It did reveal reusable mechanisms for evidence-linked learning relations, bounded delegation and result return, context composition, explicit capability selection, lifecycle/scheduling boundaries, checkpoints and provenance-preserving candidate intake.

ELO already owns the canonical flow, capability, governance and authorization contracts. This adapter combines those existing contracts into one bounded complementarity decision surface.

## Reuse rule

No second registry, scheduler, memory authority, Core, Evolution Gate, or execution authority is created.

The adapter consumes existing ELO capability selection, cross-domain relation contracts, workflow/cadence, Hermes candidate/evidence boundaries, and implementation/Evolution Gate readiness.

## Hermes-derived contribution

Hermes contributes experience patterns, not authority.

| Hermes mechanism | Reused for complementarity |
|---|---|
| learning graph / curator | evidence-linked candidate relations |
| context references | explicit input/context resolution |
| multi-agent result/evidence | bounded handoff and result return |
| cron lifecycle | future trigger/condition composition |
| checkpoint/recovery | safe re-entry after failed transitions |
| routing boundaries | capability selection under policy |
| profile isolation | tenant/scope checks |
| batch evaluation | repeatable relation evidence |

## Decision

`FLOW_A → RESULT → RELATION → CONTRACT CHECK → EVIDENCE CHECK → PREREQUISITE CHECK → AUTHORITY CHECK → SECURITY CHECK → CADENCE → ELIGIBLE`

Unknown relations remain `REVIEW_REQUIRED`.

Insufficient prerequisites remain `WAITING`.

The adapter never executes the target flow and never promotes a relation to canonical authority.

## Future integration

The next controlled step is wiring this adapter into the common ELO cognitive routing boundary so specialist flows stop hard-coding their own next-flow decisions. The target remains the existing ELO orchestrator, not a new orchestrator.