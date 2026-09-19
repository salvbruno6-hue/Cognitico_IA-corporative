# ADR-0013 — Cognitive Runtime Loop (CRL)

## Status

PROPOSED — implementation begins with consolidation over existing authorities.

## Context

ELO already contains the canonical Decision Outcome Loop (DecisionLifecycle), authorization boundary, Symbiont/Hermes execution boundary, Learning Governance, Evolution Gate, Calibration, PrecedentIndex, workflow automation and observability contracts.

The repository must not gain a second decision engine, memory authority, Evolution Gate, dispatcher, event bus or execution orchestrator merely to implement the Cognitive Runtime Loop.

The CRL is therefore an integration contract over existing owners.

## Decision

The canonical CRL is:

EVENT/TRIGGER → CONTEXT → DECISION → MANDATE/AUTHORIZATION → ACTION → OBSERVATION → OUTCOME → ATTRIBUTION → LEARNING CANDIDATE → CALIBRATION/PRECEDENT → NEW CONTEXT

Ownership remains:

| Concern | Canonical owner |
|---|---|
| Entry/context | ELO Cognitive / existing entry and context contracts |
| Decision lifecycle | DecisionLifecycle in ELO Core |
| Durable decision audit | existing elo_audit_log, exposed through a Decision Ledger projection/adapter |
| Authorization | elo-authz / existing authorization contracts |
| Action execution | existing governed Agent Runtime / Orchestrator / Symbiont-Hermes boundaries |
| Outcome/attribution/learning | existing DecisionLifecycle + learning contracts |
| Learning promotion | Learning Governance + Evolution Gate + explicit approval |
| Calibration | existing ConfidenceCalibration |
| Precedent | existing PrecedentIndex |
| Events/triggers | existing automation/event contracts; no parallel bus |
| Observability | existing ELO Observability |
| External MCP | existing elo-mcp boundary |

## Decision Ledger boundary

The Decision Ledger is a durable/auditable projection of DecisionLifecycle transitions. It is not a second lifecycle and does not decide transitions.

The first persistence target is the existing elo_audit_log. A dedicated decision table must not be created unless evidence later proves that the existing audit contract cannot satisfy the required decision trace.

Each ledger record must preserve at least:

- decision_id;
- correlation/request identity when available;
- from_state;
- to_state;
- occurred_at;
- evidence references;
- actor;
- source/contract version.

## MCP boundary

The decision_ledger interface is a read interface over the canonical ledger. It is not a write authority, decision authority or learning authority.

## Non-goals

- Create another decision engine.
- Create another memory ledger.
- Create another event bus.
- Create another dispatcher/orchestrator.
- Let MCP authorize or promote.
- Persist canonical knowledge from a decision trace.
- Bypass existing authorization.

## Implementation order

1. Define the Decision Ledger projection over DecisionLifecycle.
2. Add the decision_ledger read tool to the existing elo-mcp boundary.
3. Add tests proving lifecycle/ledger correspondence and fail-closed filtering.
4. Integrate event/trigger ownership without introducing a second runtime.
5. Close the end-to-end CRL with observability and real outcome evidence.

## Acceptance criteria

- One canonical DecisionLifecycle remains.
- Every persisted ledger transition corresponds to a real lifecycle transition.
- Ledger reads do not mutate decisions.
- MCP remains read-only.
- Authorization remains exclusively under the existing authorization authority.
- No duplicate Core, memory, Evolution Gate, dispatcher or event authority is introduced.
