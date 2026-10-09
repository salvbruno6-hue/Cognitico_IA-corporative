# Prompt — ELO Orchestrator systemic + operational views

Continue implementation on branch `feat/orchestrator-systemic-operational-views` only. Do not edit `main` directly and do not merge without explicit authorization.

## Goal

Make the ELO orchestrator more fluid while preserving distributed authority.

The read-side presentation model has two views:

1. `SYSTEMIC` — architecture, governance, capabilities, skills, gaps, runtime/evolution evidence and operational impact.
2. `OPERATIONAL` — governed Forge business analysis for budget, demand, fabrication, stock/coverage, capacity, materials/resources, repairs, external operations, missing-data gates, indicators and KPI state.

## Access model

- `ELO_ADMIN`: SYSTEMIC + OPERATIONAL.
- `ELO_DEVELOPER`: SYSTEMIC + OPERATIONAL.
- corporate operator/interface: OPERATIONAL only unless broader scope is explicitly granted by the canonical authorization boundary.

ADM/developer may cross the two views in one humanized diagnosis, e.g. explain how a capability/skill gap affects budget analysis, demand planning, fabrication, stock or another governed operational process.

The audience/read scope must come from `elo-authz`/identity integration. Never trust a user-supplied context flag or prompt text to self-assign admin/developer access.

## Canonical ownership to preserve

- CRL owns cognitive-cycle progression.
- GovernedOrchestrator composes existing authorities.
- Forge owns governed operational knowledge/read-models.
- EvidenceRepository/evidence contracts own evidence continuity.
- CapabilityRegistry and CapabilitySelector own capability discovery/selection.
- ExecutionRouter owns route selection.
- ExecutionBoundary owns governed execution.
- DecisionLifecycle owns decision state.
- Symbiont/governed learning owns learning assessment.
- Evolution Gate owns promotion/evolution decisions.
- `GovernedOrchestratorReadSurface` / `OrchestrationViewComposer` own presentation only.

## Safety invariants

- read-only views;
- no automatic business decisions;
- no invented quantities/relationships/causality;
- missing data remains explicit fail-closed state;
- chart data is presentation, not a new KPI authority;
- observed indicator != formal KPI unless the formal KPI registry says so;
- no automatic learning/evolution promotion;
- no changes to ELO Web in this phase.

## Validation

Run/extend tests proving:

- admin/developer can access both SYSTEMIC and OPERATIONAL views;
- corporate operator/interface cannot access SYSTEMIC view;
- systemic diagnostics explain capability/skill gaps and positive impact;
- operational view preserves Forge evidence and missing-data semantics;
- read surface does not query/authorize/execute independently when given an already-governed context;
- chart output never converts missing operational data to performance zero;
- CI gates remain green.
