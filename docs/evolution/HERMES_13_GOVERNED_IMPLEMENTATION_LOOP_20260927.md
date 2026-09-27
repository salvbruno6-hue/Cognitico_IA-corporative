# Hermes 13 — Governed Implementation Loop

The 13 original Hermes candidates are orchestrated through their existing
candidate-specific functional probes and the canonical Symbiont/ELO governed
handoff.

## Sequence

`candidate → bounded adaptation → functional evidence → regression/repeatability → Evolution Gate / ELO Review → explicit implementation authorization`

Order: Context Plugin, Worktree, Multiagent, Cron, Memory Provider, Route,
Profile, Batch, Learn, Learning Graph, ContextRef, Checkpoint, Hook.

## Governance boundary

The orchestrator reuses `advance_to_implementation()`, supplies no approval
flags, does not execute production workloads, does not deploy or activate
candidates, and does not mutate canonical state. Any `canonical_mutation=True`
result fails closed.

Technically eligible candidates stop at `READY_FOR_ELO_REVIEW / ELO_REVIEW`
until the existing explicit governance decision is supplied.

Checkpoint's historical `(evidence, implementation)` return ordering is
normalized by the orchestrator without changing its adapter.

This report is loop-traversal evidence, not production outcome or promotion
evidence.
