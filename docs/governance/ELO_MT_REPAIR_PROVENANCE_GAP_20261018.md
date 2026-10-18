# ELO MT repair provenance gap — 2026-10-18

## Authority

- GitHub remains the canonical authority for migration history, rules and governed implementation.
- Supabase remains the authority for persisted operational state.
- A conflict between the two is a GAP to reconcile, never permission to infer missing business ownership.

## Reconstructed migration history

Production migration `20260924142122` (`adequar_mt_ordens_reparo_controle_reparos_modulos`) is present in `supabase_migrations.schema_migrations` and was missing from the GitHub migration tree at the start of this audit.

This change restores that migration to GitHub from the exact SQL recorded by Supabase. It is historical reconciliation only and must not be reapplied to production as a new migration.

The migration did only schema work:

- dropped `NOT NULL` from `mt_ordens_reparo.tenant_id`;
- added `numero_container`, `tipo_modulo`, `observacoes`, `data_final_reparo`;
- added indexes for `data_final_reparo` and `numero_container`.

It did **not** insert the 133 repair rows.

## Persisted state

Live Supabase evidence on 2026-10-18:

- 133 rows in `mt_ordens_reparo`;
- 124 distinct `numero_container` values;
- 133/133 rows with a container identifier;
- 133/133 with `tenant_id IS NULL`;
- 133/133 with `unidade_modular_id IS NULL`;
- 0 matching rows in `mt_proveniencia_registros`.

No canonical GitHub script or migration was found that loads these repair records.

## Existing canonical rule

The PCP integration documentation from 2026-10-03 establishes that the Quality spreadsheet is an operational reconciliation source. It requires reconciliation of module identity, model/taxonomy, duplicates, dates and status before a governed load. Container number may support reconciliation but does not replace `unidade_modular_id` when physical identity is available.

Therefore, the current repair rows must not be promoted to tenant ownership, production coverage or authenticated MT authority solely from `numero_container`.

## Current classification

The schema-history GAP for migration `20260924142122` is reconciled by restoring the exact migration file in GitHub.

The **data provenance GAP remains open**: the 133 persisted rows still have no canonical load script, record-level provenance or physical-unit reconciliation.

The only proven consumption path remains the governed Forge/backend read path with extraction mode `registro_para_experiencia`.

The 133 rows are **operational evidence with unresolved load provenance**, not tenant-ready data.

## Exit criteria

`AUTHZ_MT_REPAIR_PROVENANCE_GAP` can clear only when persisted repair rows are reconciled with sufficient record provenance and/or physical unit identity for the intended governed use. Clearing this gap does not itself authorize tenant assignment or RLS changes; those remain separate governance decisions.
