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
- 133/133 rows with a module/container identifier;
- 133/133 with `tenant_id IS NULL`;
- 133/133 with `unidade_modular_id IS NULL`;
- 0 matching rows in `mt_proveniencia_registros`;
- 128/133 rows preserve a literal `Status fonte:` marker in `observacoes`;
- 5/133 rows have no observation;
- the preserved source-status values are concentrated in operational states for pátio and produção.

The embedded `Status fonte:` markers are evidence that most rows were loaded from or reconciled against an external operational source. They improve source-family reconstruction but are not a substitute for record-level provenance because they do not identify the exact file, revision, row, author or import transaction.

No canonical GitHub script or migration was found that loads these repair records.

## Didactic identity model

The repair identifier should be interpreted as a human-readable physical-module identifier, not as an opaque tenant key.

Example:

`MLTM 010030`

can be read didactically as:

- `MLTM` — modular asset family/prefix;
- `01` — model family, corresponding to M01;
- `0030` — sequential individual identification inside that model/family.

Live validation supports the structural form but also shows why automatic classification must wait:

- all 133 current identifiers follow `MLTM` + numeric content;
- 132/133 use exactly six digits after the `MLTM` prefix;
- no current row falls outside the `MLTM` + numeric pattern;
- legacy `tipo_modulo` text is not fully consistent with the model code embedded in the identifier: code `01` currently appears with more than one module type, and code `02` also appears with more than one module type.

Therefore the identifier structure is a strong reconciliation key, while the legacy textual module classification remains evidence to reconcile, not authority to overwrite the model automatically.

This decomposition does not by itself create a database key, tenant boundary or authorization rule. Any canonical parser must validate the code against the existing model/taxonomy records and record conflicts instead of silently choosing one side.

The Google Drive PCP spreadsheet may be used as a didactic/reference source for presenting model, repair, status and flow information in a simpler form, but it is not assumed to be the row-level origin of the 133 persisted repairs.

## Partial source reconstruction

Project/Library evidence preserves a derived presentation named `Relatorio_Manutencao_Containers_5_Slides_70pct_Visual(1).pptx`. The presentation explicitly says it is based exclusively on records from a spreadsheet and describes an initial cohort of 13 repair records:

- 8 repair starts in August 2026;
- 5 repair starts in September 2026;
- the only start dates shown are 21/08, 24/08, 26/08, 03/09 and 10/09;
- module composition is reported as 6 Escritório Suíte, 4 Sanitário 7 Vasos and 3 Amplo;
- it records a specific configuration-change observation for module `MLTM 020189`.

The live Supabase table contains 13 repair rows across those same five initial dates, with a closely related current module composition. This establishes a useful **reconciliation hypothesis**, not proven row-level lineage: aggregate date/count/type correlation alone cannot prove that those exact database rows descend from that exact spreadsheet cohort.

The source spreadsheet itself was not located in the connected Google Drive, Dropbox, Project files or Library index. Searches by representative identifiers and by the `MLTM` prefix did not locate an original row-level source file.

Therefore provenance is classified as **PARTIALLY_RECONSTRUCTED**:

- repair domain/source family: Quality / module-repair control — supported by project history and preserved artifacts;
- external-source loading/reconciliation: strongly supported by `Status fonte:` in 128/133 rows;
- initial 13-row cohort relationship: plausible reconciliation hypothesis, not proven lineage;
- exact original spreadsheet file: unresolved;
- row-level lineage for the 133 current rows: unresolved;
- later changes/reclassifications: unresolved;
- tenant/business ownership: unresolved.

This evidence must not be used to manufacture `mt_proveniencia_registros` rows retroactively. Historical provenance requires a verifiable row-level source or a separately governed reconciliation process.

## Domain ownership: Quality and repairs

The functional concept of repairs belongs to the **Quality** domain flow. The intended progression is didactically:

`módulo → qualidade/inspeção → necessidade de reparo → reparo → validação/liberação`

The earlier project intent was to take repair information used by the Quality project and persist it in a Quality-related database structure, preserving the relationship between the physical module and its repair lifecycle.

This domain ownership is more important than preserving any old experimental table name. The live schema already provides the minimal reusable structure:

`mt_unidades_modulares → mt_inspecoes → mt_ordens_reparo → mt_eventos_reparo`

Verified live relationships:

- `mt_unidades_modulares` identifies the physical module through `codigo_unidade`, its `modelo_id` and `status_qualidade`;
- `mt_inspecoes.unidade_modular_id` is a foreign key to `mt_unidades_modulares.id`;
- `mt_ordens_reparo.unidade_modular_id` is a foreign key to `mt_unidades_modulares.id`;
- `mt_ordens_reparo.nao_conformidade_id` links repair to `mt_nao_conformidades` when applicable;
- `mt_eventos_reparo.ordem_reparo_id` is a foreign key to `mt_ordens_reparo.id`.

For didactic use, the model can therefore be presented simply as:

`MÓDULO → INSPEÇÃO/QUALIDADE → ORDEM DE REPARO → EVENTOS DO REPARO → APROVAÇÃO/LIBERAÇÃO`

This is the preferred direction for adapting spreadsheet information: map each spreadsheet field to an existing concept first, instead of reproducing the spreadsheet structure as new tables.

The current 133 legacy repair rows are not yet connected to that full flow because `unidade_modular_id` is null. Reconciliation should focus on linking trustworthy module identity to `mt_unidades_modulares`, not on creating a parallel repair subsystem.

## Conceptual Quality model boundary

A Project/Library Quality-specialist artifact describes entities named `controle_ordens_reparo`, `eventos_reparo`, `unidades_modulares` and `retornos` and expresses useful conceptual rules for separating repair orders, events, units and returns.

Those object names are **not live schema authority**: on 2026-10-18 none of those four exact table names exists in the live `public` schema, and no matching canonical GitHub implementation was found. Their concepts, however, substantially overlap the existing live `mt_*` entities listed above.

Do not create those tables merely to conform production to the Library artifact. Reuse the canonical `mt_*` model and extend it only when a proven non-duplicate gap remains.

## Existing canonical rule

The PCP integration documentation from 2026-10-03 establishes that a Quality spreadsheet can be an operational reconciliation source. It requires reconciliation of module identity, model/taxonomy, duplicates, dates and status before a governed load. A human-readable module identifier may support reconciliation but does not replace a canonical physical-unit relationship when one exists.

The Quality specialist evidence independently reinforces the same boundary: a spreadsheet must be decomposed into the correct entities, physical module identity must remain recoverable, configuration changes belong to repair events, and a `PLANILHA != BANCO` divergence must be investigated instead of silently choosing one side. Its conceptual table names do not override the live/canonical schema.

Therefore, the current repair rows must not be promoted to tenant ownership, production coverage or authenticated MT authority solely from `numero_container`, `Status fonte:` or from the partial source reconstruction.

## Current classification

The schema-history GAP for migration `20260924142122` is reconciled by restoring the exact migration file in GitHub.

The **data provenance GAP remains open but partially reconstructed**: Quality-domain ownership and external-source traces are supported; aggregate cohort matching remains a hypothesis; the 133 current persisted rows still have no canonical row-level provenance or physical-unit reconciliation.

The only proven consumption path remains the governed Forge/backend read path with extraction mode `registro_para_experiencia`.

The 133 rows are **operational evidence with partially reconstructed provenance**, not tenant-ready data.

## Exit criteria

`AUTHZ_MT_REPAIR_PROVENANCE_GAP` can clear only when persisted repair rows are reconciled with sufficient row-level source provenance and/or physical unit identity for the intended governed use. A derived report, aggregate cohort match, parsed identifier or embedded source-status text is not sufficient to backfill provenance automatically.

Clearing this gap does not itself authorize tenant assignment or RLS changes; those remain separate governance decisions.
