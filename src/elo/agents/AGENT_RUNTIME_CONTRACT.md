# ELO Agent Runtime Contract

## Purpose

Provide one governed execution boundary for specialist agents. This is not a second Core, supervisor, memory authority or policy authority.

## Execution

`REQUEST → CONTEXT → CAPABILITY SELECTION → EVIDENCE → REASONING → ACTION PLAN → AUTHORIZATION → EXECUTION → OUTCOME → MEMORY/EXPERIENCE`

## Agent responsibilities

Agents may:
- decompose tasks;
- request existing Core capabilities;
- use authorized tools;
- maintain task-local state;
- produce evidence-backed recommendations;
- report outcomes and failures.

Agents may not:
- redefine canonical ELO identity;
- create a parallel memory authority;
- bypass provenance or tenant isolation;
- silently promote experience to Core knowledge;
- execute consequential actions without required authorization.

## Required execution metadata

Every run should carry:

- `run_id`;
- `tenant_id`;
- `principal_id`;
- `request_id`;
- `agent_id`;
- capability identifiers;
- source/evidence references;
- policy/authorization result;
- provider/model metadata when applicable;
- timestamps;
- outcome status;
- provenance.

## Failure behavior

If required evidence, authorization, capability or governance is unavailable, the runtime returns an explicit blocked/gap state instead of fabricating completion.

## Promotion boundary

Agent experience remains contextual until validated through the existing Evolution Gate.
