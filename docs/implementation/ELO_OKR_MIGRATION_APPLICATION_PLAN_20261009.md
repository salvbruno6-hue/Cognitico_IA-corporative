# ELO OKR — Migration Application Plan

Status: PREPARED / NOT APPLIED
Date: 2026-10-09
Branch: feat/orchestrator-okr-capability-integration
PR: #961

## 1. Scope

This plan covers only the persistence already prepared and validated in the PR:

1. `public.elo_strategic_objectives`
2. `public.elo_strategic_key_results`
3. `public.elo_strategic_kr_snapshot_bindings`

It does not create a new KPI owner, snapshot owner, Evidence owner, DecisionLifecycle, learning engine, router, or orchestrator.

## 2. Canonical owners preserved

- `GovernedOrchestrator` — orchestration authority above `strategic_okr`.
- `mt_definicoes_kpi` — formal KPI definition authority.
- `mt_snapshots_kpi` — KPI snapshot value/date authority.
- `EvidenceRepository` — evidence authority.
- `DecisionLifecycle` — decision/outcome lifecycle authority.
- Symbiont / Learning Governance / Evolution Gate — learning/promotion authorities.

## 3. Required migration order

### Migration A — strategic Objective / KeyResult persistence

Source candidate:

`docs/implementation/sql/ELO_OKR_STRATEGIC_PERSISTENCE_CANDIDATE.sql`

Creates Objective/KR owners, indexes, RLS fail-closed Data API boundary, backend grants, and updated_at triggers reusing the existing `public.elo_cognitive_set_updated_at()` function.

Must be applied before Migration B because the binding FK depends on `(tenant_id, key_result_id)`.

### Migration B — KR / KPI snapshot binding

Source candidate:

`docs/implementation/sql/ELO_OKR_MEASUREMENT_BINDING_CANDIDATE.sql`

Creates only the tenant-scoped attribution between a KR and an existing `mt_snapshots_kpi` row.

It must not alter `mt_snapshots_kpi` or `mt_definicoes_kpi`.

## 4. Migration file generation rule

Do not invent filenames or timestamps.

When Supabase CLI is available, generate the files using the current CLI command:

```bash
supabase migration new elo_okr_strategic_persistence
supabase migration new elo_okr_measurement_binding
```

Then copy the reviewed candidate SQL into the files in that exact order.

Do not run `db push`, `migration up --linked`, or any equivalent remote DDL action without a separate explicit human authorization.

## 5. Pre-application checks

All checks must pass before any live DDL authorization is requested.

### Existing owners

Confirm:

- `public.mt_definicoes_kpi` exists;
- `public.mt_snapshots_kpi` exists;
- `mt_definicoes_kpi.codigo_kpi` is UNIQUE;
- `mt_snapshots_kpi.id` is the primary key;
- `mt_snapshots_kpi.kpi_id` references `mt_definicoes_kpi.id`.

### Existing updated_at function

Confirm:

- `public.elo_cognitive_set_updated_at()` exists;
- it is already used by existing ELO tables;
- no parallel updated_at function is introduced by this migration.

### Name collision check

Confirm the following do not already exist live before applying:

- `public.elo_strategic_objectives`;
- `public.elo_strategic_key_results`;
- `public.elo_strategic_kr_snapshot_bindings`.

### Security check

Confirm candidate SQL:

- enables RLS on every new `public` table;
- revokes `anon` and `authenticated` table privileges;
- creates no permissive client-side policy;
- grants explicit backend access only to `service_role`;
- contains no `SECURITY DEFINER` function;
- does not use user-editable JWT metadata as authorization.

## 6. Post-application verification plan

If live DDL is authorized in a future step, verify immediately after application:

1. all three tables exist;
2. all expected PK/FK/check constraints exist;
3. Objective/KR updated_at triggers point to `public.elo_cognitive_set_updated_at()`;
4. RLS is enabled on all three tables;
5. `anon` and `authenticated` have no table privileges;
6. `service_role` has the intended CRUD privileges;
7. no row exists unless explicitly inserted later under a separate data authorization;
8. existing `mt_definicoes_kpi` and `mt_snapshots_kpi` definitions/data are unchanged;
9. no new Measurement value owner exists;
10. adapter reads remain fail-closed when there are no rows/bindings.

## 7. Rollback plan

Because no productive data should exist immediately after schema application, rollback is schema-only and must execute in reverse dependency order.

```sql
begin;

drop table if exists public.elo_strategic_kr_snapshot_bindings;
drop table if exists public.elo_strategic_key_results;
drop table if exists public.elo_strategic_objectives;

commit;
```

Do not drop or alter:

- `public.mt_definicoes_kpi`;
- `public.mt_snapshots_kpi`;
- `public.elo_cognitive_set_updated_at()`;
- Evidence/Decision/Symbiont/Learning owners.

If productive Objective/KR data ever exists, this rollback is no longer sufficient and a data-preservation/recovery plan is required before any drop.

## 8. Data activation boundary

Applying the schema does not authorize creation of productive OKR data.

Separate authorization is required for:

- Objective inserts;
- KeyResult inserts;
- KR/snapshot bindings;
- writers/services that create or update those records;
- tenant membership or client-side access expansion.

## 9. Current live state

At preparation time, none of the three new OKR persistence tables has been applied to the live Supabase project.

The reviewed source files remain candidates only until generated into official migration filenames and explicitly authorized for remote application.
