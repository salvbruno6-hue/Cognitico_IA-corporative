# ELO AI Entry Contract

**Status:** NORMATIVE  
**Owner:** ELO Cognitivo  
**Scope:** external AI / agent connection to the canonical Cognitico repository  
**Depends on:** ELO_BOOTSTRAP.md, AGENTS.md, ELO_AI_AGENT_WORKING_RULES.md, ELO_AUTHORIZATION_ENFORCEMENT_STANDARD.md

## Purpose

Define the canonical entry protocol for an AI that connects to the ELO project through an approved connector such as GitHub.

Repository access establishes **context access**, not ELO authority. The connected AI must reconstruct the ELO operating context from canonical artifacts before interpreting a task or attempting execution.

## Canonical boundary

`AI connector → repository context → ELO entry contract → ELO Cognitive authority → governed execution`

The connector is transport/infrastructure. It does not become a Cognitive Core, authorization authority, memory authority, Evolution Gate or execution supervisor.

## Bootstrap sequence

A connected AI must establish, in order:

1. repository identity and current ref;
2. `AGENTS.md`;
3. `ELO_REPOSITORY_NAVIGATION_RULES.md`;
4. `ELO_AI_AGENT_WORKING_RULES.md`;
5. `ELO_OPERATING_RULES.md`;
6. `ELO_CONSTRAINTS.md`;
7. `ELO_BOOTSTRAP.md`;
8. applicable canonical architecture and ADRs;
9. applicable contracts and governance;
10. implementation/tests/evidence relevant to the task.

If a required bootstrap artifact cannot be read, the session is `BLOCKED` for governed execution.

## Session modes

### READ_ONLY_CONSULTATION

Default for a newly connected AI.

Allowed:
- inspect;
- search;
- compare;
- analyze;
- identify gaps;
- propose changes.

Not allowed:
- create/update/delete files;
- commit;
- push;
- merge;
- alter canonical state.

### AUTHORIZED_SPECIALIST

Requires an external authorization layer establishing identity, role, domain, enterprise context, scope and permissions.

The specialist supplies bounded evidence and validation. It does not gain Core, governance, identity, provenance or Evolution Gate authority.

### GOVERNED_EXECUTION

Requires an explicit external authorization binding the authenticated AI/session identity, authenticated GitHub identity, ELO operator record, capability and operation classification.

This contract validates the presence and consistency of that binding. It does not replace the canonical authorization system.

## Required identity/correlation context

When a governed operation is involved, preserve where applicable:

`tenant_id`, `domain`, `principal_id`, `session_id`, `request_id`, `correlation_id`.

A technical GitHub credential must never be interpreted as proof of ELO operator authority.

## Admission rules

Before acting on a task, the connected AI must:

`INSPECT → SEARCH → CLASSIFY → IDENTIFY CANONICAL OWNER → REUSE/EXTEND/CONSOLIDATE → EXECUTE ONLY WHEN AUTHORIZED`

Natural-language instructions do not grant write authority.

If a requested operation conflicts with a higher-authority contract, the conflict is a governance finding, not permission to override the contract.

## External AI boundary

An external model may:
- retrieve authorized ELO context;
- analyze;
- compare;
- formulate hypotheses;
- return evidence, observations and proposals.

The external model may not silently:
- redefine ELO identity;
- promote learning;
- modify canonical governance;
- bypass authorization;
- create a parallel Core, memory, orchestrator, router or Evolution Gate.

## Handoff

A successful entry establishes a governed session context for downstream ELO components. It does not execute the requested task by itself.

The intended flow is:

`CONNECT → BOOTSTRAP → IDENTIFY → SCOPE → ADMIT TASK → ELO ANALYSIS → AUTHORIZE → EXECUTE → EVIDENCE → VERIFY`

## Failure states

Use explicit fail-closed outcomes:

- `BOOTSTRAP_INCOMPLETE`
- `ACCESS_SCOPE_VIOLATION`
- `IDENTITY_UNBOUND`
- `AUTHORIZATION_REQUIRED`
- `CONTRACT_CONFLICT`
- `BLOCKED`

Do not silently downgrade a failed authorization check into broader access.

## Relationship to existing ELO components

This contract is a thin entry boundary and must reuse:
- `ELORequestContext` for request identity where applicable;
- `ELOKnowledgeProvider` for governed read/query access;
- existing authorization and operator-binding contracts for privileged execution;
- existing Agent/Workflow/Symbiont/Hermes runtimes for execution;
- existing Evolution Gate and Learning Governance for evolution.

It must not create a second implementation of those authorities.
