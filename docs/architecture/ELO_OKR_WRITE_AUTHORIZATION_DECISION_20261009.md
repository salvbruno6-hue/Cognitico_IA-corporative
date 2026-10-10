# ELO OKR — Strategic Write Authorization Boundary

Status: PREPARED / NOT LIVE
Date: 2026-10-09

## Decision

Strategic OKR writes remain below the `GovernedOrchestrator` and are never authorized by the OKR domain, repository adapter, Supabase service role, UI or caller-provided role.

The canonical authority remains `elo-authz`.

## Reused capabilities

No new capability code is introduced.

| Strategic action | Existing capability |
|---|---|
| `strategic_okr_propose` | `PROPOSE` |
| `strategic_okr_review` | `REVIEW` |
| `strategic_okr_approve` | `APPROVE` |
| `strategic_okr_write` | `CANONICAL_WRITE` |

These capability codes already exist in the canonical capability registry. The writer must not substitute `PCP_UPDATE`, because strategic Objectives/KRs can span PCP, Commercial, Production, Stock, Repairs and other domains.

## Write ownership

`GovernedOkrWriter` coordinates writes after authorization.

It does not:

- authenticate;
- resolve roles;
- grant capabilities;
- authorize tenant access;
- create KPI definitions;
- create KPI snapshots;
- create evidence authority;
- approve its own target;
- create DecisionLifecycle or learning state.

The Supabase writer adapter is transport/persistence only. `service_role` is not an authorization decision.

## Required flow

```text
identity/session
  -> elo-authz
  -> explicit strategic action + canonical capability
  -> explicit tenant scope verification
  -> auditable, bounded authorization receipt/grant
  -> normalized StrategicWriteGrant
  -> GovernedOkrWriter
  -> SupabaseOkrWriteRepository
  -> approved strategic owner table
```

Every write must preserve an `authorization_ref` originating from `elo-authz`.

## Operation semantics

### PROPOSE

Allowed for:

- creating/updating an Objective proposal backed by evidence;
- creating/updating a KeyResult whose target remains `DRAFT`.

It cannot write an `APPROVED` target.

### REVIEW

Allowed for:

- creating/updating an explicit KR <-> KPI snapshot binding after evidence-backed review.

It does not alter the snapshot or KPI definition.

### APPROVE

Allowed for:

- persisting a KeyResult whose target is explicitly `APPROVED` and contains `target_approval_ref`.

Approval remains external to the writer; the writer only validates the received state and authorization.

### CANONICAL_WRITE

Reserved for governed maintenance of consolidated strategic records. It is not a shortcut around PROPOSE/REVIEW/APPROVE and is not automatically used by normal proposal flows.

## Tenant boundary

The grant tenant must exactly match the entity/binding tenant. Cross-tenant writes fail closed before persistence.

The persistence layer remains backend-only and service-bound until a canonical tenant membership model exists for client-side RLS.

Repository scope and area scope are not interchangeable with tenant scope. `elo-authz` must verify an explicit tenant scope before emitting a strategic write authorization.

## Evidence and provenance

- Objective proposal requires evidence refs.
- KeyResult baseline/target continue to require evidence refs according to the domain contract.
- Snapshot binding requires evidence refs.
- Every persisted strategic write records `authorization_ref`.
- `EvidenceRepository` remains the evidence authority; tables store references only.

## Current activation blockers

The current `elo-authz` implementation is not yet sufficient for live strategic writes for three independent reasons:

1. **Action mapping** — the four strategic actions are not yet present in `ACTION_CAPABILITY`.
2. **Tenant scope** — generic authorization currently validates repository scope, while `authorize_area` validates area scope. Neither is a canonical tenant authorization contract for OKR writes.
3. **Bounded authorization receipt** — the generic action response contains identity/session/action/capability/request information, but it does not currently provide the tenant-bound, auditable, expirability semantics expected by `StrategicWriteGrant`.

Therefore the writer is intentionally fail-closed and MUST NOT be activated live until `elo-authz` is extended to satisfy all three conditions using its existing identity/session/capability/audit authorities.

The extension should preserve existing owners rather than repurpose GitHub execution/commit/merge grants for corporate data writes.

Do not bypass these blockers by:

- reading a role directly in the writer;
- accepting caller-supplied capability names;
- interpreting `service_role` as authorization;
- reusing `operation="execute"`;
- treating repository scope or area scope as tenant scope;
- reusing GitHub operator bindings as corporate tenant authority;
- using `PCP_UPDATE` as a generic strategic write capability;
- creating `OKR_WRITE` or another duplicate capability.

## Live state

No strategic OKR persistence table, authz extension or writer flow has been activated in the live Supabase project as part of this decision.
