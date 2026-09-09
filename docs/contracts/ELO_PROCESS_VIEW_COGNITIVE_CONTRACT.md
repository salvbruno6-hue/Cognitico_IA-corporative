# ELO ProcessView — Cognitive Contract

Status: PROPOSED / GOVERNED GAP
Owner: ELO Cognitive

## Purpose

Define the canonical server-side boundary that supplies process views to the ELO Web experience layer.

The browser may request a view, but it must not become an authority for process topology, governance, canonical knowledge, operational state, evidence, or Hermes execution.

## Authority

- Process structure: existing canonical ELO process knowledge.
- Current operational state: ELO Cognitive, only when backed by governed evidence.
- Evidence/provenance: existing ELO evidence and persistence contracts.
- Execution: governed ELO → Hermes boundary.
- Learning: existing governed learning and Evolution Gate contracts.

No second process registry, process engine, memory, authorization engine, or evolution gate is introduced.

## Request

```text
ProcessViewRequest
- view_id
- process_id
- tenant_scope
- requested_by
```

The request is an application boundary object. Authentication and authorization remain owned by the existing ELO security boundary.

## Response

```text
ProcessViewResponse
- view_id
- process_id
- source
- authority: reference | canonical
- generated_at
- nodes: node_id -> state
- evidence_available
- operational_state_available
- gaps[]
```

Node state is constrained to:

```text
REFERENCE | CURRENT | DEVIATION | UNKNOWN
```

`CURRENT` or `DEVIATION` MUST NOT be emitted merely because the process is documented. They require governed operational evidence.

## Reference fallback

Until the Cognitive provider is implemented, the web layer may render the existing reference projection. That projection MUST remain explicitly `REFERENCE`, MUST expose its gaps, and MUST NOT claim current telemetry.

## Multi-tenant boundary

The provider must preserve `tenant_scope` and reject cross-tenant reads. The browser must never be trusted to select or override the authoritative tenant boundary.

## Hermes boundary

ProcessView is observational/presentational. It does not execute Hermes. A user mission that requires execution must continue through the already-established ELO authorization → Cognitive decision → governed Hermes execution path.

## Learning boundary

A ProcessView response is not a learning event. Any learning candidate must use the existing evidence/outcome/governed-learning flow and Evolution Gate. No frontend observation can directly mutate canonical knowledge.

## Implementation gate

Before this contract is wired to live data:

1. Reuse the existing Cognitive ownership and data contracts.
2. Prove the tenant/auth boundary.
3. Prove reference/current/deviation/unknown invariants.
4. Prove evidence linkage for non-reference states.
5. Add integration tests against a deterministic provider.
6. Validate CI and deploy preview through the existing Vercel project.
7. Only then replace the reference adapter in `apps/elo-web`.

## Current GAP

The repository currently has the frontend `ProcessView` presentation contract and a reference adapter, but no verified live Cognitive provider endpoint. This document records that boundary without fabricating one.
