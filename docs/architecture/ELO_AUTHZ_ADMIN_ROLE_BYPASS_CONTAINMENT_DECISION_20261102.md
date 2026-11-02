# ELO Authz — containment of administrative role/capability drift

Status: PREPARED / NOT LIVE
Date: 2026-11-02
Related: #1143, ADR-0017, `ELO_AUTHORITY_SEPARATION_DECISION_20261009.md`
Owner: `elo-authz` / ELO Governance

## Finding

GitHub and the live Supabase authorization model diverge.

The canonical migration `20260919220406_elo_access_tiers.sql` defines `elo_private.has_capability(p_code)` as a strict persisted relation:

```text
identity -> active role -> elo_role_capabilities -> active capability
```

The live project currently contains a later database migration that is not present in the GitHub canon and makes `elo_private.has_capability(p_code)` return `true` for an active `ELO_ADMIN` or `CANONICAL_ADMIN` role before resolving `p_code` through the capability catalog.

This creates an implicit "administrative role means every capability" semantic in RLS while `elo-authz` correctly requires explicit capabilities.

## Additional evidence

The live RLS graph currently references `PCP_ADMIN` in 38 policies across 14 tables, with 50 expression occurrences, plus `public.lista_mae_guard()`. `PCP_ADMIN` is not an active capability in `public.elo_capabilities`.

ADR-0017 explicitly records `PCP_ADMIN` as technical debt and states that capabilities were not changed when the admin editing path was introduced. Therefore the missing capability is not authority to create it automatically.

The canonical `AUTHZ_CAPABILITY_REFERENCE_INTEGRITY` probe also classifies a referenced capability missing from the catalog as `REVIEW`, never as permission to create or assign it.

Current live aggregate evidence shows the active identity carrying `CANONICAL_ADMIN` also carries `ELO_ADMIN`; `ELO_ADMIN` has explicit `READ`, `PORTAL_READ` and `PCP_READ`. No individual identity data is required by this decision.

## Decision — bounded containment

Until the `PCP_ADMIN` debt is resolved by a separate governed decision, the least-authority reconciliation candidate is:

1. restore the normal meaning of `elo_private.has_capability(p_code)` for every catalog capability: it must resolve through `elo_role_capabilities` and `elo_capabilities`;
2. preserve one explicit compatibility branch only when `p_code = 'PCP_ADMIN'`;
3. that compatibility branch may recognize only active `ELO_ADMIN` or `CANONICAL_ADMIN` roles on an active canonical identity;
4. an admin role must **not** imply any other arbitrary capability code;
5. do not insert `PCP_ADMIN` into `elo_capabilities`;
6. do not assign `PROPOSE`, `REVIEW`, `APPROVE`, `ADMIN`, `CANONICAL_WRITE` or any other capability as part of containment;
7. do not modify strategic authorization semantics in `elo-authz`;
8. keep the capability-reference health finding in `REVIEW` until the 38 policies and `lista_mae_guard` no longer depend on the orphan symbol or a later governed decision explicitly creates a real capability.

This is containment, not final resolution.

## Why this is safer than the live bypass

With the current live helper, an admin role can make `has_capability('ANY_CODE')` true even if that capability is absent or was never assigned. That allows an RLS policy typo, future capability name, or stale reference to silently become an administrative permission.

The candidate narrows this behavior to the single historical debt already acknowledged by ADR-0017. All other capability checks remain material and auditable through role-capability assignments.

## Why `PCP_ADMIN` is not created here

Creating a new capability would be a governance change, not a drift correction. The existing health contract explicitly treats the orphan reference as a `REVIEW` finding, and ADR-0017 preserved it as debt rather than defining a capability contract.

A later decision must determine whether the 38 policies should:

- use one or more existing PCP capabilities;
- use a dedicated administrative-role predicate rather than capability vocabulary; or
- introduce a governed `PCP_ADMIN` capability with explicit scope, consumers, assignments and tests.

## Production boundary

The SQL under `docs/implementation/sql/ELO_AUTHZ_ADMIN_ROLE_BYPASS_CONTAINMENT_CANDIDATE.sql` is a candidate only.

Merging it does **not** authorize:

- remote DDL;
- role/capability mutation;
- Edge Function deployment;
- strategic Objective creation;
- Objective Continuity checkpoint creation.

Promotion to an official migration and application to `fxbpevjrkwhbicpmecow` require a separate authorized DDL step and post-apply negative/positive probes.

## Acceptance for later live promotion

A promoted migration must prove at minimum:

1. an identity with only an ordinary role cannot satisfy an unassigned capability;
2. `ELO_ADMIN`/`CANONICAL_ADMIN` cannot satisfy an arbitrary unknown capability;
3. the bounded legacy `PCP_ADMIN` path continues to authorize the intended administrative workflow during the transition;
4. explicit `PCP_READ`/`PORTAL_READ` behavior is unchanged;
5. `AUTHZ_CAPABILITY_REFERENCE_INTEGRITY` still reports `PCP_ADMIN` as `REVIEW` until its debt is separately resolved;
6. no strategic capability is created or assigned;
7. no current operational data row is mutated by the migration.
