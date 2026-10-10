# ELO — OKR ↔ GovernedOrchestrator integration status

## Canonical decision

`GovernedOrchestrator` remains above the OKR domain. OKR is a strategic capability consumed by the orchestrator; it is not an orchestration authority.

```text
GovernedOrchestrator
  -> strategic_okr capability
      -> Objective
      -> KeyResult
      -> formal KPI / Metric
      -> Measurement
      -> evaluation
      -> diagnosis
      -> canonical DecisionLifecycle / Action / Outcome
      -> Symbiont laboratory observation
```

No `OkrOrchestrator`, `OKRRouter`, `OkrEvidenceRepository`, `OkrDecisionLifecycle`, `OkrLearningEngine`, or `OkrSymbiont` was introduced.

## Phase status

| Phase | State | Evidence/result |
|---|---|---|
| O1 | COMPROVADO | canonical runtime/owner audit completed |
| O2 | COMPROVADO | reconciliation matrix completed |
| O3 | IMPLEMENTADO/TESTADO | Objective, KeyResult and Measurement contracts |
| O4 | IMPLEMENTADO/TESTADO | tenant-safe Objective/KR read capability |
| O5 | IMPLEMENTADO/TESTADO | KR references existing formal KPI authority; latest valid Measurement derives current |
| O6 | IMPLEMENTADO/TESTADO | canonical EvidenceRepository reused; no OKR evidence store |
| O7 | IMPLEMENTADO/TESTADO | progress/trend/forecast/deviation/status separated; Objective Health fail-closed without policy |
| O8 | IMPLEMENTADO/TESTADO | existing CausalAssessment, DecisionRecord and DecisionLifecycle reused |
| O9 | IMPLEMENTADO/TESTADO | existing OrchestrationResponseComposer renders strategic state with evidence/uncertainty |
| O10 | IMPLEMENTADO/TESTADO | attributed decision/outcome can become existing SymbiontLabObservation; no learning promotion |
| O11 | IMPLEMENTADO/TESTADO | focused unit tests cover contracts, tenant isolation, KPI authority, evidence, evaluation, decision and observation |
| O12 | PARCIAL/TESTADO | existing CapabilityRegistry/Selector selects `strategic_okr`; generic natural-language → CapabilityRequirement resolver remains unproven |
| O13 | COMPROVADO | AST-based structural guard forbids parallel OKR owners |
| O14 | COMPROVADO NO HEAD ANTERIOR | seven workflows green; persistence-preparation head must rerun gates |
| O15 | DRAFT PR #961 | no merge authorization granted |
| O16 | OWNER PERSISTENTE APROVADO | Option A approved for migration preparation only |
| O17 | SQL CANDIDATO PREPARADO | Objective/KR tenant-scoped, backend-only; live DDL not applied |

## Persistence audit and approved decision

Read-only inspection of live Supabase found no existing Objective/KeyResult/OKR entity owner in `public` or `elo_core`.

The user explicitly approved on 2026-10-09:

`Option A → dedicated tenant-scoped Objective/KeyResult persistence → prepare migration only`.

Approved owners:

- `public.elo_strategic_objectives`;
- `public.elo_strategic_key_results`.

The decision is recorded in:

`docs/architecture/ELO_OKR_PERSISTENCE_BOUNDARY_DECISION_20261009.md`.

## Tenant/access boundary selected for the prepared schema

Because the current authorization baseline does not provide a general tenant-membership table/FK suitable for direct client RLS, the prepared schema uses the safest compatible mode:

**BACKEND-ONLY / SERVICE-BOUND.**

Rules:

- RLS enabled on both tables;
- all table privileges revoked from `anon` and `authenticated`;
- no permissive authenticated policy;
- explicit `service_role` table privileges only;
- tenant authorization remains upstream in the canonical ELO authorization boundary;
- sector/department is not tenant identity;
- user-editable JWT metadata is not used for tenant authorization.

This preserves fail-closed behavior while a future tenant-membership model remains undecided.

## Tenant-safe Objective ↔ KeyResult relation

The approved persistent identity model is composite:

- Objective PK: `(tenant_id, objective_id)`;
- KeyResult PK: `(tenant_id, key_result_id)`;
- KeyResult → Objective FK: `(tenant_id, objective_id)`.

This prevents a KeyResult from referencing an Objective from another tenant at the database constraint layer.

## KPI and Evidence boundaries preserved

`KeyResult.metric_code` reuses:

`mt_definicoes_kpi.codigo_kpi`.

No second KPI registry is created.

The prepared SQL does not alter or populate:

- `mt_definicoes_kpi`;
- `mt_snapshots_kpi`.

Evidence persistence contains reference identities only:

- Objective `evidence_refs`;
- KR `baseline_evidence_refs`;
- KR `target_evidence_refs`.

`EvidenceRepository` remains the evidence authority.

Checks preserve the application contract:

- non-null baseline requires baseline evidence refs;
- non-null target requires target evidence refs;
- `APPROVED` target requires non-empty `target_approval_ref`;
- `weight > 0`;
- direction restricted to `INCREASE`, `DECREASE`, `MAINTAIN`.

## Migration preparation state

Prepared SQL candidate:

`docs/implementation/sql/ELO_OKR_STRATEGIC_PERSISTENCE_CANDIDATE.sql`

Structural regression test:

`tests/integration/test_okr_strategic_persistence_candidate.py`

The SQL candidate creates only the approved Objective/KR owners and their indexes/security constraints.

### Official migration filename

The official `supabase/migrations/<timestamp>_...sql` file has **not** been fabricated.

The Supabase skill requires `supabase migration new <name>` to generate the migration filename. The current environment had no installed Supabase CLI, and `npx supabase ...` did not complete within the execution environment. Therefore the reviewed SQL remains a candidate artifact until a working official migration-generation path is available.

No DDL has been applied to live Supabase.

## Measurement boundary remains unchanged

`mt_definicoes_kpi` remains the formal KPI registry.

`mt_snapshots_kpi` remains the existing snapshot owner, but still has no tenant/KR binding sufficient to prove persistence for the application `Measurement` contract.

No M1/M2/M3 option was selected by the Objective/KR approval. No Measurement table or binding migration was created.

## Acceptance matrix

| Criterion | State | Note |
|---|---|---|
| GovernedOrchestrator recognizes OKR as a capability | PARCIAL/TESTADO | capability registry/selector + hierarchy proven; generic NLP capability resolution separate |
| no parallel OkrOrchestrator | COMPROVADO | structural guard |
| Objective contract | COMPROVADO | application contract exists |
| KeyResult contract | COMPROVADO | application contract exists |
| Objective persistent owner | PREPARADO | approved SQL candidate; not live |
| KeyResult persistent owner | PREPARADO | approved SQL candidate; not live |
| tenant-safe KR→Objective relation | PREPARADO | composite FK in SQL candidate |
| KPI relation | COMPROVADO/PREPARADO | existing formal KPI registry reused by `metric_code` |
| Measurement persistence | BLOQUEADO POR DECISAO | no tenant/KR snapshot binding chosen |
| baseline/target evidence constraints | PREPARADO | DB checks present |
| target approval constraint | PREPARADO | APPROVED requires approval ref |
| backend-only security | PREPARADO | RLS + revoke client roles + service_role grant |
| EvidenceRepository authority | PRESERVADO | refs only |
| DecisionLifecycle authority | PRESERVADO | no duplicate lifecycle |
| Symbiont boundary | PRESERVADO | no automatic learning |
| live Supabase DDL | NÃO APLICADO | outside current authorization |
| merge | NÃO AUTORIZADO | PR remains draft |

## Remaining real gaps / gates

1. generate the official migration filename through a working Supabase CLI/migration workflow and place the reviewed candidate SQL there;
2. rerun repository gates on the final migration head;
3. separately decide M1/M2/M3 for persistent Measurement binding;
4. generic natural-language → CapabilityRequirement resolution remains a separate existing gap;
5. Objective Health policy remains `INDETERMINADO` until governed;
6. production operational proof requires real persisted Objective/KR data after separately authorized live migration.

## Architectural outcome

```text
ELO / GovernedOrchestrator
        ↓
CapabilityRegistry / CapabilitySelector
        ↓
strategic_okr
        ↓
Objective / KeyResult domain semantics
        ↓
elo_strategic_objectives / elo_strategic_key_results   [prepared, not live]
        ↓
existing KPI + Evidence + Decision + Symbiont owners
```

No hypothesis, missing value, target, achievement, completed decision, or positive outcome is promoted automatically to canonical learning.
