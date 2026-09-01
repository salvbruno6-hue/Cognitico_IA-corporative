# ELO Workflow + Automation Contract

## Purpose

Define one governed workflow boundary for scheduled, event-driven and human-triggered ELO processes.

## Canonical lifecycle

`TRIGGER → CONTEXT → ANALYZE → DECIDE → AUTHORIZE → EXECUTE → OBSERVE → RECORD OUTCOME → LEARN`

## Trigger types

- scheduled;
- event-driven;
- user-requested;
- follow-up/condition watch.

## Governance

Automation invokes existing ELO capabilities. It does not become a source of truth or authority.

Consequential writes/actions require an explicit authorization result appropriate to the operation.

## Idempotency and traceability

A workflow execution should have:

- `workflow_id`;
- `run_id`;
- `tenant_id`;
- `request_id`/correlation id;
- trigger metadata;
- capability/action identifiers;
- authorization result;
- input/output evidence references;
- timestamps;
- outcome;
- retry/recovery state.

Retries must be safe or explicitly blocked when idempotency cannot be guaranteed.

## Failure states

`BLOCKED`, `FAILED`, `PARTIAL`, `COMPLETED`, `REQUIRES_HUMAN_REVIEW`.

A failed workflow is not represented as successful merely because a later retry is scheduled.

## Integration boundary

External orchestrators may be adapters behind this contract. They are evaluated by the ELO integration gate and do not become canonical ELO architecture by installation alone.
