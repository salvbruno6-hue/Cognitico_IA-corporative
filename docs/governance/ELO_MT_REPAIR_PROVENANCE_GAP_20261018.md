# ELO MT repair provenance gap — 2026-10-18

## Authority

- GitHub remains the canonical authority for migration history, rules and governed implementation.
- Supabase remains the authority for persisted operational state.
- Project/Library artifacts may provide historical evidence, but do not become a third operational authority.
- A conflict between sources is a GAP to reconcile, never permission to infer missing business ownership.

## Reconstructed migration history

Production migration `20260924142122` (`adequar_mt_ordens_reparo_controle_reparos_modulos`) is present in `supabase_migrations.schema_migrations` and was missing from the GitHub migration tree at the start of this audit.

The audit restored that migration to GitHub from the exact SQL recorded by Supabase. It is historical reconciliation only and must not be reapplied to production as a new migration.

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
- 0 matching rows in `mt_proveniencia_registros`;
- 128/133 rows preserve a literal `Status fonte:` marker in `observacoes`;
- 5/133 rows have no observation;
- the preserved source-status values are concentrated in operational states for pátio and produção.

The embedded `Status fonte:` markers are evidence that most rows were loaded from or reconciled against an external operational source. They improve source-family reconstruction but are not a substitute for record-level provenance because they do not identify the exact file, revision, row, author or import transaction.

No canonical GitHub script or migration was found that loads these repair records.

## Partial source reconstruction

Project/Library evidence preserves a derived presentation named `Relatorio_Manutencao_Containers_5_Slides_70pct_Visual(1).pptx`. The presentation explicitly says it is based exclusively on records from a spreadsheet and describes an initial cohort of 13 repair records:

- 8 repair starts in August 2026;
- 5 repair starts in September 2026;
- the only start dates shown are 21/08, 24/08, 26/08, 03/09 and 10/09;
- module composition is reported as 6 Escritório Suíte, 4 Sanitário 7 Vasos and 3 Amplo;
- it records a specific configuration-change observation for container `MLTM 020189`.

The live Supabase table contains exactly 13 repair rows across those same five initial dates. Their current module composition is 5 Escritório Suíte, 5 Sanitário 7 Vasos and 3 Amplo. This is strong evidence that the initial Supabase cohort descends from the same Quality/maintenance spreadsheet family, while also proving that the persisted data has since diverged from the preserved report.

The source spreadsheet itself was not located in the connected Google Drive, Dropbox, Project files or Library index. Searches by representative container identifiers and by the `MLTM` prefix did not locate an original row-level source file.

Therefore provenance is now classified as **PARTIALLY_RECONSTRUCTED**, not unknown and not fully reconciled:

- source family: Quality / container-maintenance spreadsheet — strongly supported;
- external-source loading/reconciliation: strongly supported by `Status fonte:` in 128/133 rows;
- initial cohort relationship: supported by date/count/type correlation;
- exact original spreadsheet file: unresolved;
- row-level lineage for the 133 current rows: unresolved;
- later changes/reclassifications after the initial cohort: unresolved;
- tenant/business ownership: unresolved.

This evidence must not be used to manufacture `mt_proveniencia_registros` rows retroactively. Historical provenance requires a verifiable row-level source or a separately governed reconciliation process.

## Conceptual Quality model boundary

A Project/Library Quality-specialist artifact also describes entities named `controle_ordens_reparo`, `eventos_reparo`, `unidades_modulares` and `retornos` and expresses useful conceptual rules for separating repair orders, events, units and returns.

Those object names are **not live schema authority**: on 2026-10-18 none of those four tables exists in the live `public` schema, and no matching canonical GitHub implementation was found. They must therefore be treated as conceptual/historical evidence only.

Do not create those tables merely to conform production to the Library artifact. Any future schema evolution must first reconcile the concepts with the existing `mt_*` model, prove a non-duplicate gap, and pass normal architecture/evolution governance.

## Existing canonical rule

The PCP integration documentation from 2026-10-03 establishes that the Quality spreadsheet is an operational reconciliation source. It requires reconciliation of module identity, model/taxonomy, duplicates, dates and status before a governed load. Container number may support reconciliation but does not replace `unidade_modular_id` when physical identity is available.

The Quality specialist evidence independently reinforces the same boundary: a spreadsheet must be decomposed into the correct entities, physical module identity must remain recoverable, configuration changes belong to repair events, and a `PLANILHA != BANCO` divergence must be investigated instead of silently choosing one side. Its conceptual table names do not override the live/canonical schema.

Therefore, the current repair rows must not be promoted to tenant ownership, production coverage or authenticated MT authority solely from `numero_container`, `Status fonte:` or from the partial source reconstruction.

## Current classification

The schema-history GAP for migration `20260924142122` is reconciled by restoring the exact migration file in GitHub.

The **data provenance GAP remains open but partially reconstructed**: the source family, embedded source-status traces and initial 13-row cohort are supported by preserved evidence, but the 133 current persisted rows still have no canonical load script, record-level provenance or physical-unit reconciliation.

The only proven consumption path remains the governed Forge/backend read path with extraction mode `registro_para_experiencia`.

The 133 rows are **operational evidence with partially reconstructed provenance**, not tenant-ready data.

## Exit criteria

`AUTHZ_MT_REPAIR_PROVENANCE_GAP` can clear only when persisted repair rows are reconciled with sufficient row-level source provenance and/or physical unit identity for the intended governed use. A derived report, aggregate cohort match or embedded source-status text is not sufficient to backfill provenance automatically.

Clearing this gap does not itself authorize tenant assignment or RLS changes; those remain separate governance decisions.
