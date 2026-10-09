# ELO — OKR ↔ GovernedOrchestrator integration status

## Canonical decision

`GovernedOrchestrator` is above the OKR domain. OKR is a strategic capability consumed by the orchestrator; it is not an orchestration authority.

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
| O12 | PARCIAL/TESTADO | existing CapabilityRegistry/Selector selects `strategic_okr`; GovernedOrchestrator visibility/orientation remains above it; general natural-language → CapabilityRequirement resolver is not proven in current runtime |
| O13 | COMPROVADO | AST-based structural guard forbids parallel OKR owner classes without falsely rejecting `OkrSymbiontBridge` |
| O14 | COMPROVADO | final validated head `838b3186bcfa9b934dce2b6a60c8ffbdd5b3c545` closed all seven workflows in `success`, including Evolution Gate |
| O15 | DRAFT PR #961 | no merge authorization granted |

## Persistence audit

Read-only inspection of the live Supabase project `fxbpevjrkwhbicpmecow` found no table in `public` or `elo_core` whose name matches OKR, Objective, Objetivo, KeyResult or Resultado-Chave variants.

Classification:

- Objective persistence: `NAO_COMPROVADO`.
- KeyResult persistence: `NAO_COMPROVADO`.
- Objective ↔ KeyResult durable relation: `NAO_COMPROVADO`.
- New Objective/KR schema: **NOT CREATED**, because the persistent owner and tenant-isolation model require an explicit architectural decision.
- Draft decision contract: `docs/architecture/ELO_OKR_PERSISTENCE_BOUNDARY_DECISION_20261009.md`.

The application port `OkrReadRepository` therefore remains storage-neutral until a canonical persistent owner/schema is explicitly approved or an existing equivalent is proven.

### Existing generic relation/knowledge owners

Live inspection found:

- `elo_cognitive_relations`;
- `elo_relation_types`;
- `elo_conhecimento_itens`;
- `elo_conhecimento_vinculos`;
- `elo_conhecimento_nucleos`.

`elo_cognitive_relations` is suitable only as a **relation candidate**, not as the Objective/KR entity store. It represents `source_type/source_id → relation_type → target_type/target_id`, but has no `tenant_id`, is currently service-role-only and has no Objective/KR lifecycle semantics. Repository code search found no canonical consumer that would justify silently overloading it with entire strategic entities.

Knowledge tables remain knowledge owners and must not be repurposed as strategic commitment/entity storage.

### KPI definition versus tenant-scoped Measurement

Live inspection of the existing KPI layer established:

- `mt_definicoes_kpi`: RLS enabled, zero current rows, primary key `id`, unique `codigo_kpi`, authenticated `SELECT` policy with `USING (true)`, no `tenant_id`;
- `mt_snapshots_kpi`: RLS enabled, zero current rows, FK `kpi_id → mt_definicoes_kpi.id`, unique `(kpi_id, data_referencia)`, authenticated `SELECT` with `USING (true)` and authenticated `INSERT` with `WITH CHECK (true)`, no `tenant_id` and no `key_result_id`.

Therefore the existing KPI layer must be interpreted more precisely:

- KPI definition identity: `REUSE`, with global/corporate scope still to be explicitly confirmed;
- KPI snapshot authority: `REUSE CANDIDATE`, but tenant/subject binding is not proven;
- OKR `Measurement.tenant_id` persistence: `PARCIAL/BLOQUEADO POR MODELO DE VINCULO`.

The runtime contract may continue using `metric_code` to reference the formal KPI registry, but it must not claim that `mt_snapshots_kpi` is already a complete tenant-safe persistence implementation of `Measurement`.

### Authorization/tenant boundary

The canonical authorization baseline owns identity, session, role, capability and scope and keeps those primitives closed to ordinary client access. It does not establish a general tenant table/FK that new strategic persistence can assume automatically.

Consequently, any future Objective/KR persistence must explicitly choose and prove its tenant authority before DDL. Sector/department must not become the primary security boundary, and authenticated access with `USING (true)` is insufficient for tenant-scoped strategic data.

## Acceptance matrix

| Criterion | State | Note |
|---|---|---|
| GovernedOrchestrator recognizes OKR as a capability | PARCIAL/TESTADO | capability registry/selector + orchestrator visibility prove hierarchy; generic NLP capability resolution remains a separate existing gap |
| no parallel OkrOrchestrator | COMPROVADO | structural search/test |
| Objective accessible | COMPROVADO IN CONTRACT/FIXTURE | live persistence absent |
| KeyResult accessible | COMPROVADO IN CONTRACT/FIXTURE | live persistence absent |
| KPI related | COMPROVADO | uses formal KPI registry identity; no duplicate registry |
| Measurement accessible | COMPROVADO IN CONTRACT/FIXTURE | live tenant/KR binding to snapshot authority remains unproven |
| current derived correctly | COMPROVADO | latest valid Measurement, never silent zero |
| progress calculated by OKR owner | COMPROVADO | direction-aware domain evaluator |
| trend separate from progress | COMPROVADO | independent field/evaluation |
| forecast separate | COMPROVADO | currently `None`/SEM_DADO; no invented forecast |
| deviation identifiable | COMPROVADO | independent current-target difference when both known |
| EvidenceRepository integrated | COMPROVADO | canonical tenant-scoped repository reused |
| Objective Health governed | PARCIAL | fail-closed without explicit policy; no simple-average default |
| diagnosis traceable | COMPROVADO | CausalAssessment requires evidence from KR evaluation |
| Action/Outcome related | PARCIAL | canonical DecisionLifecycle bridge proven; durable OKR relation not persisted |
| Response Composer integrated | COMPROVADO | existing composer extended |
| Humanized business response | COMPROVADO AT COMPOSER BOUNDARY | human-facing output preserves uncertainty; no second response/humanizer authority introduced |
| multi-tenancy preserved | COMPROVADO IN APPLICATION/EVIDENCE; PERSISTENCE BLOCKED | Objective/KR runtime checks tenant; persistent tenant authority must still be approved |
| authorization preserved | COMPROVADO BY BOUNDARY DESIGN | OKR capability does not self-authorize; execution remains GovernedOrchestrator/elo-authz/ExecutionBoundary |
| Symbiont observational | COMPROVADO | observation only after ATTRIBUTED outcome |
| no automatic learning | COMPROVADO | bridge does not evaluate/promote/attach learning |
| no autoauthorization | COMPROVADO | no authorization code in OKR domain |
| no parallel owner | COMPROVADO | AST structural guard |
| full regression CI | COMPROVADO | all seven workflows green at `838b3186...` |
| Evolution Gate | COMPROVADO | workflow and internal canonical/security/Hermes jobs green |

## CI correction evidence

The first final-head run failed only because the structural anti-duplication test searched forbidden symbols by substring and interpreted the permitted class `OkrSymbiontBridge` as the forbidden authority `OkrSymbiont`. The full suite at that point reported **1717 passed / 1 failed**.

The test was corrected to inspect exact class names via AST. No architecture or implementation behavior was weakened. At head `838b3186bcfa9b934dce2b6a60c8ffbdd5b3c545`, all seven workflows passed.

## Remaining real gaps / gates

1. **Durable Objective/KeyResult persistence**: no canonical live entity owner exists. Draft proposal recommends the minimum dedicated tenant-scoped owner, but implementation is blocked until explicit architecture approval.
2. **Tenant security source for strategic persistence**: no general tenant registry/FK has been proven in the authorization baseline. Must be selected before RLS/DDL.
3. **Measurement ↔ KR persistence**: current `mt_snapshots_kpi` has neither `tenant_id` nor `key_result_id`; select a governed strengthening/association strategy before claiming persistent E2E traceability.
4. **KPI registry scope**: formal KPI definitions appear structurally global; confirm global/corporate scope explicitly before using that assumption as architecture.
5. **Generic natural-language → CapabilityRequirement resolution**: no canonical runtime owner was found. Do not create an `OKRRouter`; solve this later at the general intent/capability-resolution layer.
6. **Objective Health policy**: no approved policy exists. Health remains `INDETERMINADO` instead of using a silent arithmetic mean.
7. **Production operational proof**: fixture/unit/CI evidence is not a production OKR dataset proof.

## Architectural decision gate

Repository governance explicitly requires stopping before implementation when a new persistent data model is required but unspecified. That gate is now reached.

The draft decision contract recommends:

- dedicated tenant-scoped Objective/KR entity ownership only;
- continued reuse of `mt_definicoes_kpi` for KPI definition identity;
- no duplicate KPI snapshot registry;
- a separate explicit decision for tenant/KR binding of measurements;
- `elo_cognitive_relations` only as a relation layer if/when its tenant semantics are governed;
- no live DDL and no merge until the persistent owner and tenant authority are explicitly approved.

## Architectural outcome

The implementation has the intended dependency direction:

```text
ELO / GovernedOrchestrator
        ↓
CapabilityRegistry / CapabilitySelector
        ↓
strategic_okr
        ↓
Objective / KeyResult domain semantics
        ↓
existing KPI + Evidence + Decision + Symbiont owners
```

The inverse relation remains structurally valid when persisted evidence/bindings exist:

```text
operational event / evidence
  -> formal KPI measurement
  -> KeyResult evaluation
  -> Objective evaluation
  -> strategy reference
```

No hypothesis, missing value, achievement, completed decision, or positive outcome is promoted automatically to canonical learning.
