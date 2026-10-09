---
id: ELO-OKR-ORCH-001
name: Governed Orchestrator OKR Integration
type: contract
layer: cognitive
owner: GovernedOrchestrator + strategic-objective-domain
status: draft
authority: implementation
version: 0.1
related:
  - GovernedOrchestrator
  - CapabilityRegistry
  - EvidenceRepository
  - DecisionLifecycle
  - Symbiont
depends_on:
  - mt_definicoes_kpi
  - mt_snapshots_kpi
---

# GovernedOrchestrator ↔ OKR integration

## Canonical hierarchy

`GovernedOrchestrator` is above the OKR domain. OKR serves the orchestrator as a strategic capability; it does not orchestrate ELO.

```text
GovernedOrchestrator
  -> strategic/OKR capability
      -> Objective
      -> KeyResult
      -> formal KPI/Metric
      -> Measurement
      -> evaluation
      -> diagnosis
      -> DecisionLifecycle / Action / Outcome
  -> EvidenceRepository
  -> Response Composer / Humanizer
  -> Symbiont observation
```

## Reused owners

- Orchestration: `GovernedOrchestrator`.
- Capability inventory/selection: existing `CapabilityRegistry` / `CapabilitySelector`.
- Formal KPI authority: `mt_definicoes_kpi`.
- KPI observations: `mt_snapshots_kpi`.
- Evidence: `EvidenceRepository`.
- Causal diagnosis: `CausalAssessment`.
- Decision/action/outcome lifecycle: `DecisionRecord`, `DecisionLifecycle`, `OutcomeFeedback`.
- Execution: existing Router / `ExecutionBoundary`.
- Human response: existing `OrchestrationResponseComposer` / `Humanizer`.
- Learning observation: existing Symbiont / Learning Governance / Evolution Gate.

No `OkrOrchestrator`, `OKRRouter`, OKR evidence store, OKR decision lifecycle, OKR learning engine, or OKR Symbiont is permitted.

## Phase state

| Phase | State | Result |
|---|---|---|
| O1 | COMPROVADO | runtime/owner audit completed |
| O2 | COMPROVADO | reconciliation matrix completed |
| O3 | IMPLEMENTADO | minimal `Objective`, `KeyResult`, `Measurement` contracts |
| O4 | IMPLEMENTADO | tenant-scoped Objective/KR read capability |
| O5 | IMPLEMENTADO | KR metric resolution through formal KPI authority; latest valid Measurement = current |
| O6 | IMPLEMENTADO | evidence resolution through canonical `EvidenceRepository` |
| O7 | IMPLEMENTADO | progress/trend/deviation separated; status stays indeterminate without policy; Objective Health requires governed policy |
| O8 | IMPLEMENTADO | KR deviation bridges to existing `CausalAssessment` and `DecisionLifecycle` |
| O9 | PENDENTE | Response Composer / Humanizer |
| O10 | PENDENTE | Symbiont observation |
| O11+ | PENDENTE | tests/orchestrator/non-regression/gates/PR completion |

## Guardrails already enforced

- baseline requires evidence;
- target requires evidence;
- approved target requires explicit approval reference;
- draft target is not consumed as approved target;
- Measurement requires evidence and timezone-aware timestamp;
- tenant boundaries fail closed;
- KR metric identity must match its Measurement metric identity;
- absent formal KPI remains `SEM_KPI_FORMAL_REGISTRADO`;
- absent Measurement does not become zero;
- `progress != trend != forecast != status`;
- progress alone never produces `ON_TRACK`;
- Objective Health is not a simple average and remains `INDETERMINADO` without governed policy;
- diagnosis/action requires evidence already present in the KR evaluation;
- action proposals enter the existing `DecisionLifecycle` as `PROPOSED` and do not create outcome or learning automatically.
