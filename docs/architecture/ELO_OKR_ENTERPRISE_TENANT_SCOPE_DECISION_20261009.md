# ELO OKR — Enterprise Scope as Strategic Tenant Boundary

Status: PREPARED / NOT LIVE
Date: 2026-10-09

## Finding

The canonical Supabase authorization model already contains an active scope:

- `scope_type = ENTERPRISE`
- `scope_key = MULTITEINER`

Other active scope types include `DOMAIN`, `REPOSITORY` and `SYSTEM`.

The strategic OKR domain must not reinterpret any of those other scope types as tenant authority.

A read-only live audit also confirmed that strategic authorization eligibility must be constrained to identities already registered in `elo_identity_registry` through the Google authentication flow.

## Decision

Reuse the existing `ENTERPRISE` scope type as the candidate canonical corporate tenant boundary for strategic OKR authorization.

For the current Multiteiner corporate context, a strategic write grant may use:

```text
tenant_id = MULTITEINER
```

only when `elo-authz` proves BOTH identity eligibility and tenant membership.

### Identity eligibility

The authenticated caller is eligible for strategic authorization only when the canonical identity record satisfies all of the following:

```text
elo_identity_registry.active = true
elo_identity_registry.provider = google
elo_identity_registry.auth_user_id is present
elo_identity_registry.authorized_email = authenticated Google email
```

The authenticated email is resolved from Supabase Auth/Google and compared case-insensitively with `authorized_email`.

No email is auto-registered by domain, role, department, request payload or successful Google login alone. A Google-authenticated email that is not already present and active in the canonical identity registry remains unauthorized.

### Tenant membership

After identity eligibility is proven, `elo-authz` must prove that the same ELO identity is linked through `elo_identity_scopes` to an active `elo_scopes` row where:

```text
scope_type = ENTERPRISE
scope_key  = MULTITEINER
active     = true
```

No new tenant table is introduced by this decision.

## Explicit non-equivalences

The following are NOT tenant authority or strategic authorization eligibility:

- `elo_identity_registry.enterprise_context`;
- `DOMAIN` scope;
- department/sector names;
- PCP/Planning identity;
- `area_code` used by `authorize_area`;
- `REPOSITORY` scope;
- GitHub operator binding;
- role name;
- email domain;
- caller-supplied email;
- successful Google authentication without a matching canonical identity record;
- user metadata/JWT user metadata.

`enterprise_context` currently contains descriptive/operator context and must not be used as a tenant identifier.

## Current live state

The read-only live audit confirmed:

- `ENTERPRISE/MULTITEINER` exists and is active;
- there is currently one active identity satisfying the exact Google-bound eligibility predicate (`provider=google`, active, `auth_user_id` present);
- the active identity observed is linked only to repository scopes and is not currently linked to `ENTERPRISE/MULTITEINER`.

Therefore strategic write authorization must remain fail-closed live.

This branch MUST NOT create or alter `elo_identity_scopes` assignments without a separate explicit authorization and validation of the intended identity-to-enterprise membership model.

## Required elo-authz behavior

A future `authorize_strategic_write` path inside the existing `elo-authz` authority must:

1. authenticate through Supabase Auth and obtain the Google-authenticated email;
2. resolve an active canonical identity in `elo_identity_registry`;
3. require `provider=google`, matching `authorized_email`, and a bound `auth_user_id`;
4. require an active ELO session;
5. accept only a known strategic action;
6. map the action to an existing capability (`PROPOSE`, `REVIEW`, `APPROVE`, `CANONICAL_WRITE`);
7. require an explicit `tenant_id` and `resource_ref`;
8. resolve identity scopes from canonical tables;
9. require an active `ENTERPRISE` scope whose `scope_key` equals `tenant_id`;
10. require the mapped capability on an active role;
11. audit ALLOW/DENY through the existing authorization audit owner;
12. emit a short-lived receipt bound to identity, session, tenant, action, capability and resource;
13. preserve an `evidence_ref`/`grant_ref` that the strategic writer stores as `authorization_ref`.

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
- a new authentication flow;
- an email allowlist outside the canonical identity registry.

The owner remains `elo-authz` plus the existing Supabase Auth identity, identity registry, scope and capability tables.

## Live state

No scope assignment, Edge Function deployment, DDL, OKR data, identity registration or permission mutation has been applied live by this decision.
