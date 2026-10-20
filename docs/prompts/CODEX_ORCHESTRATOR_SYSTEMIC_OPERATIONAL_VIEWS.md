# Codex continuation — ELO Orchestrator systemic/operational views

Continue only on `feat/orchestrator-systemic-operational-views`.

## Goal

Integrate the new read surfaces into the ELO flow without creating a God Orchestrator.

## Preserve

- CRL owns cognitive-cycle progression.
- GovernedOrchestrator owns composition only.
- elo-authz owns authorization.
- Forge owns governed operational knowledge/read-models.
- CapabilityRegistry/Selector own capability discovery/selection.
- ExecutionRouter/ExecutionBoundary own route/execution boundaries.
- DecisionLifecycle owns decision state.
- Symbiont owns governed learning assessment.
- Evolution Gate owns promotion/evolution.

## New contracts

- `OrchestrationViewComposer.systemic_view()` is for already-authorized ADM/developer audiences.
- `OrchestrationViewComposer.operational_view()` is for corporate operational surfaces.
- `GovernedOrchestratorReadSurface` is presentation-only and must remain read-only.

## Follow-up integration target

When integrating into CognitiveCore/API/MCP, pass an audience/read scope already resolved by canonical identity/authz. Do not infer role from message text.

The systemic view should aggregate explicit capability/skill/governance evidence and may include Forge operational impact.
The operational view should project the same governed Forge context already used for evidence, without a second Forge read.

## Acceptance

- no duplicate Forge query for one request;
- no audience self-authorization;
- no zero-filling missing business metrics;
- no automatic KPI promotion;
- no automatic learning/evolution;
- chart data remain presentation read models;
- tests preserve existing orchestrator/CRL behavior.
