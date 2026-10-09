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
| O11 | IMPLEMENTADO | focused unit tests cover contracts, tenant isolation, KPI authority, evidence, evaluation, decision and observation |
| O12 | PARCIAL | existing CapabilityRegistry/Selector selects `strategic_okr`; GovernedOrchestrator visibility/orientation remains above it; general natural-language → CapabilityRequirement resolver is not proven in current runtime |
| O13 | IMPLEMENTADO | structural test forbids parallel OKR owners; repository CI provides broader non-regression evidence |
| O14 | PENDENTE NO HEAD FINAL | Evolution Gate must be green after final branch changes |
| O15 | DRAFT PR #961 | no merge authorization granted |

## Persistence audit

Read-only inspection of the live Supabase project `fxbpevjrkwhbicpmecow` found no table in `public` or `elo_core` whose name matches OKR, Objective, Objetivo, KeyResult or Resultado-Chave variants.

Classification:

- Objective persistence: `NAO_COMPROVADO`.
- KeyResult persistence: `NAO_COMPROVADO`.
- Objective ↔ KeyResult durable relation: `NAO_COMPROVADO`.
- Measurement/KPI authority: existing `mt_definicoes_kpi` / `mt_snapshots_kpi` remains canonical for formal KPI definitions and observations.
- New Objective/KR schema: **NOT CREATED**, because no canonical persistent model was defined and repository rules require stopping rather than inventing a new persistent authority.

The application port `OkrReadRepository` therefore remains storage-neutral until a canonical persistent owner/schema is explicitly defined or an existing equivalent is proven.

## Acceptance matrix

| Criterion | State | Note |
|---|---|---|
| GovernedOrchestrator recognizes OKR as a capability | PARCIAL/TESTADO | capability registry/selector + orchestrator visibility prove hierarchy; generic NLP capability resolution remains a separate existing gap |
| no parallel OkrOrchestrator | COMPROVADO | structural search/test |
| Objective accessible | COMPROVADO IN CONTRACT/FIXTURE | live persistence absent |
| KeyResult accessible | COMPROVADO IN CONTRACT/FIXTURE | live persistence absent |
| KPI related | COMPROVADO | uses formal KPI registry port; no duplicate registry |
| Measurement accessible | COMPROVADO IN CONTRACT/FIXTURE | maps to canonical KPI observation identity; live OKR binding absent |
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
| multi-tenancy preserved | COMPROVADO IN APPLICATION/EVIDENCE | persistent RLS not applicable until Objective/KR persistence exists |
| authorization preserved | COMPROVADO BY BOUNDARY DESIGN | OKR capability does not self-authorize; execution remains GovernedOrchestrator/elo-authz/ExecutionBoundary |
| Symbiont observational | COMPROVADO | observation only after ATTRIBUTED outcome |
| no automatic learning | COMPROVADO | bridge does not evaluate/promote/attach learning |
| no autoauthorization | COMPROVADO | no authorization code in OKR domain |
| no parallel owner | COMPROVADO | structural guard |
| full regression CI | PENDENTE NO HEAD FINAL | rerun after final docs/tests |
| Evolution Gate | PENDENTE NO HEAD FINAL | rerun after final docs/tests |

## Remaining real gaps

1. **Durable Objective/KeyResult persistence**: no canonical live table/model exists. Do not invent one without an explicit persistent contract.
2. **Generic natural-language → CapabilityRequirement resolution**: no canonical runtime owner was found. Do not create an `OKRRouter`; solve this later at the general intent/capability-resolution layer.
3. **Objective Health policy**: no approved policy exists. Health remains `INDETERMINADO` instead of using a silent arithmetic mean.
4. **Production operational proof**: fixture/unit/CI evidence is not a production OKR dataset proof.

## Architectural outcome

The implementation now has the intended dependency direction:

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

The inverse relation is also structurally possible when evidence is supplied:

```text
operational event / evidence
  -> formal KPI measurement
  -> KeyResult evaluation
  -> Objective evaluation
  -> strategy reference
```

No hypothesis, missing value, achievement, completed decision, or positive outcome is promoted automatically to canonical learning.
