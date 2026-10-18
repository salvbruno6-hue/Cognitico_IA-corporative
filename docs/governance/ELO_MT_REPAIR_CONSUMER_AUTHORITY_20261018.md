# ELO — MT repair consumer authority — 2026-10-18

Status: `EVIDENCE_CLASSIFIED / TENANT OWNERSHIP UNRESOLVED`

## Decision

The currently proven ELO consumption path for `public.mt_ordens_reparo` is a governed Forge read path for cognitive experience extraction. This classifies current consumption authority; it does **not** assign business tenant ownership to the underlying 133 repair rows.

No tenant, `tenant_id`, identity scope, role, capability, grant, RLS policy or writer permission is created or changed by this decision.

## Canonical GitHub evidence

`supabase/migrations/20261005080000_extend_elo_forge_governed_external_repair_sources.sql` explicitly states that the registered operational sources are used only through the governed Forge read path and create no new authority. It registers:

- `public.mt_unidades_modulares` under domain `reparos_modulares`;
- `public.mt_ordens_reparo` under domain `reparos_modulares`;
- `mt_ordens_reparo` extraction mode as `registro_para_experiencia`;
- provenance preservation in the extraction rule.

The canonical Forge adapter consumes these sources server-side/read-only using the governed backend path. Existing tests exercise the repair source as a Forge demand-impact source.

## Live Supabase evidence

As of 2026-10-18:

- `mt_ordens_reparo`: 133 rows;
- 124 distinct `numero_container` values;
- all 133 rows have `numero_container`;
- all 133 rows have `tenant_id IS NULL`;
- all 133 rows have `unidade_modular_id IS NULL`;
- all 133 rows have `nao_conformidade_id IS NULL`;
- all 133 rows have `aprovado_por IS NULL`;
- `mt_tenants`: zero rows;
- no non-system trigger is attached to `mt_ordens_reparo`;
- no non-system SQL routine currently references `mt_ordens_reparo`;
- dependent repair views previously inspected are `security_invoker=true` and do not provide direct `anon`/`authenticated` SELECT access;
- the inspected request-log window had no direct REST request to the table.

The container identifiers share one observed structural format/prefix family, which is consistent with a concentrated source, but that is not sufficient evidence to infer a single business tenant.

## Classification

| Dimension | Current classification |
|---|---|
| Proven ELO consumer | Governed Forge/backend read path |
| Cognitive role | Operational source -> experience evidence |
| Direct authenticated human writer | Not proven |
| Direct authenticated human reader | Not proven |
| Business tenant ownership | Unresolved |
| Safe automatic tenant backfill | No |
| Safe automatic ENTERPRISE assignment | No |
| Safe automatic RLS tenant rewrite | No |

## Governance consequence

Until business ownership provenance is proven, `mt_ordens_reparo` must be treated as **backend/reference-read current consumption with unresolved tenant ownership**.

This means:

1. Forge may continue its already-governed read-only consumption;
2. no direct authenticated access may be justified from the Forge registration itself;
3. `numero_container` format or shared prefix must not be converted into tenant identity;
4. repository scope, Google identity, role, successful login or `ENTERPRISE/MULTITEINER` existence must not be used as tenant backfill evidence;
5. a future writer or direct client reader requires its own domain/scope/capability contract;
6. a future tenant-aware policy requires an explicit mapping source establishing row ownership before any backfill or policy replacement.

## Next safe work

The remaining technical work is provenance discovery, not authorization mutation:

- trace the source that loaded the 133 repair rows or the upstream container registry;
- locate any authoritative mapping from `numero_container` to enterprise/customer/tenant;
- if no such source exists, retain the rows as untenantized Forge evidence and keep human/direct-client access fail-closed rather than inventing ownership.
