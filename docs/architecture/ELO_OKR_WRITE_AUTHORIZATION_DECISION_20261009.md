# ELO OKR — Strategic Write Authorization Boundary

Status: IMPLEMENTED IN CANON / NOT LIVE
Date: 2026-10-09
Last reconciled: 2026-11-02

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

These capability codes exist in the capability registry. The writer must not substitute `PCP_UPDATE`, because strategic Objectives/KRs can span PCP, Commercial, Production, Stock, Repairs and other domains.

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

## Canonical implementation state — reconciled 2026-11-02

The three implementation blockers recorded on 2026-10-09 are resolved in the GitHub canon:

1. **Action mapping** — `strategic_okr_propose/review/approve/write` map to `PROPOSE/REVIEW/APPROVE/CANONICAL_WRITE` in the canonical `elo-authz` source.
2. **Tenant scope** — `authorize_strategic_write` validates explicit `ENTERPRISE/<tenant>` scope and action/resource binding.
3. **Bounded receipt** — the canonical extension emits short-lived, auditable strategic authorization evidence.

These statements describe the GitHub implementation, not the current production deployment.

## Current live activation blockers — 2026-11-02

The live Supabase project is intentionally still fail-closed:

1. **`elo-authz` runtime drift** — live Edge Function version 15 predates `authorize_strategic_write` and the later continuation tenant/resource hardening. Canonical source must be deployed through the governed deployment path before strategic authorization can be considered live.
2. **administrative capability drift** — live `CANONICAL_ADMIN` has zero material role-capability assignments, while the canonical baseline materially assigns its baseline capabilities. Recovery is prepared separately and must not be performed by ad-hoc SQL.
3. **strategic owner absent** — `elo_strategic_objectives`, `elo_strategic_key_results` and `elo_strategic_kr_snapshot_bindings` are not live. #1137 governs their promotion.
4. **delegated strategic assignment not selected** — `PROPOSE/REVIEW/APPROVE` must be explicitly assigned through governance to appropriate operator roles/identities; no document or bootstrap path may choose recipients automatically.

The complete activation order is defined in:

`docs/architecture/ELO_OBJECTIVE_CONTINUITY_ACTIVATION_SEQUENCE_20261102.md`

Do not bypass these blockers by:

- reading a role directly in the writer;
- accepting caller-supplied capability names;
- interpreting `service_role` as authorization;
- reusing `operation="execute"`;
- treating repository scope or area scope as tenant scope;
- reusing GitHub operator bindings as corporate tenant authority;
- using `PCP_UPDATE` as a generic strategic write capability;
- creating `OKR_WRITE` or another duplicate capability;
- fabricating an Objective Continuity checkpoint before the strategic Objective exists;
- treating technical ability to deploy/apply a migration as governance approval.

## Live state

No strategic Objective/KR owner table, role-capability repair, delegated strategic permission, Objective or ACTIVE checkpoint is activated merely by this decision.
