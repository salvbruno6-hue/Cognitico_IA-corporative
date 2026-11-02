# ELO Authz — resolution of the orphan `PCP_ADMIN` authorization symbol

Status: PREPARED / NOT LIVE
Date: 2026-11-02
Related: #1143, #1145, ADR-0017
Owner: `elo-authz` / ELO Governance

## Context

`PCP_ADMIN` is referenced by production RLS but is not an active capability in `public.elo_capabilities`.

ADR-0017 explicitly recorded `PCP_ADMIN` as technical debt and did not create a capability contract for it. The canonical capability-integrity probe classifies a referenced-but-missing capability as `REVIEW`, not as authority to create or assign it.

The live authorization drift introduced by `20260928200819_governanca_elo_admin_acesso_todas_camadas` attempted to compensate by making `ELO_ADMIN`/`CANONICAL_ADMIN` satisfy **every** string passed to `elo_private.has_capability(p_code)`. That conflates role membership with capability possession and diverges from `elo-authz`, which requires explicit capabilities.

A read-only live audit on 2026-11-02 found:

- 38 RLS policies across 14 tables reference `PCP_ADMIN`;
- 50 policy-expression occurrences exist because UPDATE policies use both `USING` and `WITH CHECK`;
- there are only two expression shapes:
  - 30 occurrences: `JWT app_metadata.role = admin OR has_capability('PCP_ADMIN')`;
  - 20 occurrences: `has_capability('PCP_ADMIN')` only;
- every affected policy is `PERMISSIVE` and targets `{authenticated}`;
- `public.lista_mae_guard()` is the only function body that also references `PCP_ADMIN`;
- the same live-only migration added `current_user IN ('postgres','service_role')` inside that `SECURITY DEFINER` trigger function;
- the function owner is `postgres`, so `current_user` is not a safe caller-identity proof in this context.

## Decision

Resolve the debt without creating a new capability.

### 1. Administrative role predicate

Introduce one internal RLS helper:

```text
elo_private.has_admin_role()
```

It answers one question only: does `auth.uid()` resolve to an active canonical identity with an active role whose code is `ELO_ADMIN` or `CANONICAL_ADMIN`?

It does not accept arbitrary capability codes and is not an authorization service parallel to `elo-authz`.

### 2. Capability resolver returns to strict semantics

`elo_private.has_capability(p_code)` returns `true` only through:

```text
active identity
  -> active role
  -> elo_role_capabilities
  -> active elo_capabilities
  -> c.code = p_code
```

No role code bypasses capability materialization.

### 3. Remove `PCP_ADMIN` from RLS vocabulary

The 38 existing admin-write policies keep their current role/JWT semantics, but every `has_capability('PCP_ADMIN')` term is replaced by `has_admin_role()`.

The migration candidate is deliberately fail-closed and now embeds the **exact audited snapshot** observed live. Before the first `ALTER POLICY`, it validates for every one of the 38 policies:

- `schemaname`;
- `tablename`;
- `policyname`;
- command (`INSERT`, `UPDATE` or `DELETE`);
- permissiveness (`PERMISSIVE`);
- target roles (`{authenticated}`);
- exact `USING` predicate;
- exact `WITH CHECK` predicate.

The two accepted legacy predicate shapes are materialized explicitly. The candidate aborts if a policy is missing, if an unaudited `PCP_ADMIN` consumer appears, or if any definition changes even while the aggregate totals remain 38 policies / 50 occurrences. Same-count drift is therefore not accepted as evidence of equivalence.

After the rewrite, the candidate also aborts if any `PCP_ADMIN` reference remains in `pg_policies`.

### 4. Correct `lista_mae_guard`

`public.lista_mae_guard()` keeps the accepted ADR-0017 authorization sources:

- explicit gateway GUC `app.lista_mae_aprovada = 'SIM'`;
- canonical administrative role through `has_admin_role()`;
- authenticated JWT `app_metadata.role = 'admin'`.

The live-only `current_user IN ('postgres','service_role')` branch is removed. A `SECURITY DEFINER` function must not interpret `current_user` as caller identity.

Audit insertion into `lista_mae_alteracoes` is preserved.

### 5. No implicit strategic authority

This resolution does **not** grant `PROPOSE`, `REVIEW`, `APPROVE`, `ADMIN`, `CANONICAL_WRITE`, or any other strategic/system capability.

`elo-authz` remains the authorization authority for strategic and executable operations. RLS role membership remains a database enforcement fact, not an authorization receipt.

## Why not create `PCP_ADMIN`

No accepted contract defines its scope, consumers, delegation rules or assignment semantics. ADR-0017 explicitly left it as debt. Creating it merely because policies reference it would convert drift into new authority.

The admin-write policies are already semantically named and bounded as administrative operations, so a role predicate expresses the actual intent more accurately than a fictitious capability.

## Production boundary

The companion SQL is stored as:

`docs/implementation/sql/ELO_AUTHZ_PCP_ADMIN_DEBT_RESOLUTION_CANDIDATE.sql`

It is **not** an official migration and is **not** authorized for remote execution.

Merge means only that the canonical remediation is prepared. Promotion to `supabase/migrations` and application to `fxbpevjrkwhbicpmecow` require a separately authorized DDL step.

## Required pre-apply evidence

Before promotion to an official migration:

1. re-read the live helper definitions and the complete `PCP_ADMIN` policy graph;
2. require exact equality with the embedded 38-policy snapshot, including identities, commands, permissiveness, roles and `USING/WITH CHECK` definitions; any difference requires re-analysis;
3. require the observed aggregate of 38 policies / 50 occurrences and exactly one function-body consumer;
4. confirm `ELO_ADMIN` and `CANONICAL_ADMIN` are still the intended administrative role codes;
5. confirm no new `PCP_ADMIN` consumer appeared after this decision;
6. obtain explicit canonical DDL authorization.

## Required post-apply evidence

After authorized application:

1. `pg_policies` contains zero `PCP_ADMIN` references;
2. function bodies contain zero `PCP_ADMIN` authorization references;
3. `has_capability('unknown-code')` is never granted merely by an admin role;
4. `has_admin_role()` is true only for active canonical administrative identities;
5. explicit capabilities such as `PCP_READ` remain governed by `elo_role_capabilities`;
6. Lista-Mãe admin writes and audit trail still work under authorized paths;
7. unauthorized authenticated writes remain denied;
8. the `AUTHZ_CAPABILITY_REFERENCE_INTEGRITY` finding for `PCP_ADMIN` disappears because the orphan reference no longer exists, not because a capability was fabricated;
9. no Objective, checkpoint, grant or operational data row is created by the schema correction itself.
