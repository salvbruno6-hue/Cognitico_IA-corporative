# ELO OKR — Measurement Binding Boundary Decision

Date: 2026-10-09
Status: PREPARED / NOT APPLIED LIVE
Scope: strategic OKR read capability

## Decision

Adopt **M2** for persistent Measurement attribution:

- keep `public.mt_snapshots_kpi` unchanged as the canonical owner of KPI snapshot values;
- keep `public.mt_definicoes_kpi` unchanged as the canonical formal KPI registry;
- keep `public.elo_strategic_key_results` as the tenant-scoped KR owner;
- introduce a separate tenant-scoped binding owner:
  `public.elo_strategic_kr_snapshot_bindings`.

The binding does not copy KPI values, formulas, dates, status, progress, decisions, or learning state. It only records that one governed KPI snapshot is admissible as an OKR-domain Measurement for a specific tenant/KR, with explicit evidence references.

## Why M2

Live schema inspection confirms that `mt_snapshots_kpi` is global KPI snapshot storage with:

- `id` UUID primary key;
- `kpi_id` FK to `mt_definicoes_kpi.id`;
- `data_referencia`;
- `valor`;
- `numerador` / `denominador`;
- `contexto`;
- `calculado_em`;
- unique `(kpi_id, data_referencia)`.

It does not own `tenant_id` or `key_result_id`. Adding those columns directly would change the meaning of the existing KPI snapshot authority and could break existing consumers.

## Authority boundaries

### `mt_definicoes_kpi`
Owns formal KPI identity and definition.

### `mt_snapshots_kpi`
Owns the observed KPI snapshot value and reference date.

### `elo_strategic_key_results`
Owns tenant-scoped KR identity and the expected `metric_code`.

### `elo_strategic_kr_snapshot_bindings`
Owns only the attribution:

`tenant + KR -> existing snapshot + evidence refs`.

### Evidence
`EvidenceRepository` remains the cognitive evidence authority. The binding stores identities/references only.

## Read invariant

A binding may become a `Measurement` only when all conditions hold:

1. the requested tenant matches the binding tenant;
2. the requested KR matches the binding KR;
3. the KR exists in the same tenant;
4. the snapshot exists;
5. the snapshot points to an active formal KPI definition;
6. that definition's `codigo_kpi` equals the KR `metric_code`;
7. the snapshot has a non-null `valor`;
8. the binding has at least one evidence reference.

Any mismatch fails closed. A snapshot must never be inferred as a KR Measurement merely because its KPI code matches.

## Measurement projection

The read adapter materializes the domain `Measurement` without creating a second value authority:

- `measurement_id` <- binding `binding_id`;
- `tenant_id` <- binding/KR tenant;
- `key_result_id` <- binding/KR;
- `metric_code` <- formal KPI definition, validated against KR;
- `value` <- `mt_snapshots_kpi.valor`;
- `measured_at` <- `data_referencia` represented as UTC start-of-day for the domain datetime contract;
- `evidence_refs` <- binding evidence refs;
- `source_ref` <- deterministic `mt_snapshots_kpi:<snapshot_id>`.

`calculado_em` remains snapshot computation metadata and is not used to reorder business reference dates.

## Security

The binding remains backend/service-bound:

- RLS enabled;
- no permissive client-side policy;
- `anon` and `authenticated` have no table privileges;
- explicit backend `service_role` privileges only;
- tenant authorization stays outside the repository, in the canonical ELO authorization boundary;
- every read still includes and revalidates `tenant_id`.

## Non-goals

This decision does not:

- modify `mt_snapshots_kpi`;
- modify or populate `mt_definicoes_kpi`;
- calculate KPI values;
- automatically bind snapshots to KRs;
- approve targets;
- calculate Objective Health policy;
- authorize tenants;
- write learning;
- execute decisions;
- apply DDL to live Supabase.

## Migration state

A SQL candidate may be prepared for review, but no live DDL and no invented migration timestamp are authorized by this document.
