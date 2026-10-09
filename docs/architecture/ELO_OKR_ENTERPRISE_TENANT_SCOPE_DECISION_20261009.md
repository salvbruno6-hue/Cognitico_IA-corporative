# ELO OKR — Enterprise Scope as Strategic Tenant Boundary

Status: PREPARED / NOT LIVE
Date: 2026-10-09

## Finding

The canonical Supabase authorization model already contains an active scope:

- `scope_type = ENTERPRISE`
- `scope_key = MULTITEINER`

Other active scope types include `DOMAIN`, `REPOSITORY` and `SYSTEM`.

The strategic OKR domain must not reinterpret any of those other scope types as tenant authority.

## Decision

Reuse the existing `ENTERPRISE` scope type as the candidate canonical corporate tenant boundary for strategic OKR authorization.

For the current Multiteiner corporate context, a strategic write grant may use:

```text
tenant_id = MULTITEINER
```

only when `elo-authz` proves that the authenticated ELO identity is linked through `elo_identity_scopes` to an active `elo_scopes` row where:

```text
scope_type = ENTERPRISE
scope_key  = MULTITEINER
active     = true
```

No new tenant table is introduced by this decision.

## Explicit non-equivalences

The following are NOT tenant authority:

- `elo_identity_registry.enterprise_context`;
- `DOMAIN` scope;
- department/sector names;
- PCP/Planning identity;
- `area_code` used by `authorize_area`;
- `REPOSITORY` scope;
- GitHub operator binding;
- role name;
- user metadata/JWT user metadata.

`enterprise_context` currently contains descriptive/operator context and must not be used as a tenant identifier.

## Current live gap

The read-only live audit confirmed the active `ENTERPRISE/MULTITEINER` scope exists, but the active identity observed in the audit is linked only to repository scopes and is not currently linked to `ENTERPRISE/MULTITEINER`.

Therefore strategic write authorization must remain fail-closed live.

This branch MUST NOT create or alter `elo_identity_scopes` assignments without a separate explicit authorization and validation of the intended identity-to-enterprise membership model.

## Required elo-authz behavior

A future `authorize_strategic_write` path inside the existing `elo-authz` authority must:

1. require an active ELO identity/session;
2. accept only a known strategic action;
3. map the action to an existing capability (`PROPOSE`, `REVIEW`, `APPROVE`, `CANONICAL_WRITE`);
4. require an explicit `tenant_id` and `resource_ref`;
5. resolve identity scopes from canonical tables;
6. require an active `ENTERPRISE` scope whose `scope_key` equals `tenant_id`;
7. require the mapped capability on an active role;
8. audit ALLOW/DENY through the existing authorization audit owner;
9. emit a short-lived receipt bound to identity, session, tenant, action, capability and resource;
10. preserve an `evidence_ref`/`grant_ref` that the strategic writer stores as `authorization_ref`.

## Resource binding

Receipts must be resource-specific, e.g.:

```text
strategic_okr:objective:<objective_id>
strategic_okr:key_result:<key_result_id>
strategic_okr:binding:<key_result_id>:<snapshot_id>
```

A receipt for one resource must not authorize another resource.

## No new authority

This decision does not create:

- a tenant registry parallel to `elo_scopes`;
- an OKR authorization service;
- an `OKR_WRITE` capability;
- a new role;
- a new authentication flow.

The owner remains `elo-authz` plus the existing identity/scope/capability tables.

## Live state

No scope assignment, Edge Function deployment, DDL, OKR data or permission mutation has been applied live by this decision.
