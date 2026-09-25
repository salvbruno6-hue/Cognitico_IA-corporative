# ELO Symbiont — External Gate Perception

## Purpose

The Symbiont can encounter an external gate that is still running, such as CI
or another governed validation process. Waiting for that gate is an execution
state, not a scheduled task and not a human approval request.

## Contract

`WAITING_FOR_EXTERNAL_GATE` means:

- the execution state is durable;
- the next action is preserved;
- repeated perception while the gate is pending is idempotent;
- no operation is repeated merely because time passed;
- completion is accepted only from a deterministic external observation;
- completion evidence is recorded in the existing execution boundary;
- the execution returns to `ACTIVE` and the existing resume contract continues it.

This mechanism does not authorize production, promotion, canonical mutation, or
authority changes.

## Boundary

The perception adapter is not a scheduler, supervisor, memory authority, or
second execution engine. It reuses `SymbiontExecutionStore` and the existing
`SymbiontResumer` contract.

## Invariant

`PERCEIVE_PENDING(state) == state` for logical execution state.

When the external gate deterministically completes:

`PERCEIVE_COMPLETED(state) -> ACTIVE(next_action)`.

Human approval remains a separate governed boundary.
