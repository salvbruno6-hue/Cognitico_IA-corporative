# Hermes 13 — Governed Implementation Loop

## Purpose

Unify the 13 original Hermes candidates in one execution sequence using the
existing ELO/Symbiont implementation handoff.

This is orchestration, not a new governance authority.

## Sequence

`candidate → bounded adaptation → functional evidence → regression/repeatability → Evolution Gate / ELO Review → explicit implementation authorization`

The canonical execution order is the order already recorded in
`HERMES_CANDIDATE_EVALUATION_MATRIX.md`:

1. EXT-CONTEXT-PLUGIN-HERMES
2. EXT-WORKTREE-HERMES
3. EXT-MULTIAGENT-HERMES
4. EXT-CRON-HERMES
5. EXT-MEMPROVIDER-HERMES
6. EXT-ROUTE-HERMES
7. EXT-PROFILE-HERMES
8. EXT-BATCH-HERMES
9. EXT-LEARN-HERMES
10. EXT-LEARNING-GRAPH-HERMES
11. EXT-CONTEXTREF-HERMES
12. EXT-CHECKPOINT-HERMES
13. EXT-HOOK-HERMES

## Governance boundary

The orchestrator:

- reuses the candidate-specific functional probes;
- reuses `advance_to_implementation()`;
- produces the existing START/END governance views through the shared handoff;
- supplies no Evolution Gate approval flag;
- supplies no implementation authorization flag;
- rejects any result reporting `canonical_mutation=True`;
- does not execute Hermes production workloads;
- does not deploy or activate candidates;
- does not create a second Evolution Gate, registry, scheduler, memory store, or promotion authority.

Therefore a technically eligible candidate reaches the existing
`READY_FOR_ELO_REVIEW / ELO_REVIEW` boundary and remains there until the
existing explicit governance decision is supplied.

## Checkpoint exception

`EXT-CHECKPOINT-HERMES` historically returns its probe tuple as
`(evidence, implementation)`. The orchestrator normalizes that tuple without
changing the checkpoint adapter.

## Result semantics

The report records, for every candidate:

- candidate ID;
- governed-loop result;
- next governance state;
- canonical-mutation flag;
- presence of implementation evidence.

The report is evidence of loop traversal, not evidence of production outcome
or authorization.

## Next gate

The next action for candidates at `ELO_REVIEW` is the existing human
Evolution Gate / implementation authorization. No automatic transition is
performed by this orchestrator.
