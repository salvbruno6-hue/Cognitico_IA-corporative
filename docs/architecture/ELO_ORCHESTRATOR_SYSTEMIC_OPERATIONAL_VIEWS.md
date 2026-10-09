# ELO Orchestrator — systemic and operational views

## Decision

The ELO orchestrator has two read-side presentation surfaces and must not become a monolithic authority.

### 1. Systemic view — ADM / developer

Purpose: explain the ELO system itself in a humanized, actionable way.

It may combine explicit governed evidence about:

- architecture and canonical boundaries;
- authorization/governance health;
- capability visibility and wiring;
- skill health and missing runtime proof;
- routing/execution evidence;
- DecisionLifecycle / CRL integration status;
- Symbiont observations;
- Evolution Gate state;
- operational impact observed in Forge.

Expected questions include:

- Which capabilities need improvement?
- Which skills are not functioning well or are still unproven?
- What positive capability would become available if a gap were fixed?
- Which architectural/gov boundaries are blocking a flow?
- Which operational impacts are caused by a systemic gap?
- Where does evidence stop and inference begin?

The output should be humanized and may include chart-ready datasets. Charts are presentation projections of observed states, not new authority or inferred KPI.

Systemic visibility is restricted to an audience already resolved as ELO administrator/developer by the canonical identity/authorization boundary. The orchestrator does not interpret bearer tokens or self-assign this audience.

### 2. Operational view — ELO Web / corporate interfaces

Purpose: expose governed business analysis without exposing unnecessary internal system-governance detail.

The operational surface consumes Forge/read-model evidence for domains such as:

- budget/solicitation analysis;
- reasons to proceed, revise, block or decline a solicitation when evidence exists;
- demand and demand composition;
- fabrication need;
- stock/coverage;
- capacity/load;
- materials and resources;
- repairs and return-to-stock implications;
- external operations;
- missing data/gates;
- operational indicators and formal KPI state.

Typical flow:

`Corporate interface -> CognitiveCore/Orchestrator -> governed Forge context -> operational read surface -> humanized response / chart-ready data`

The Forge remains the operational knowledge/data source. The orchestrator does not take ownership of Forge tables, business rules or operational decisions.

## Authority boundaries

| Concern | Canonical owner |
|---|---|
| identity / permission | `elo-authz` + identity contracts |
| cognitive cycle | CRL |
| application composition | `GovernedOrchestrator` |
| capability inventory | `CapabilityRegistry` |
| capability selection | `CapabilitySelector` |
| operational knowledge | Forge governed catalog/read-models |
| evidence | `EvidenceRepository` / evidence contracts |
| route selection | `ExecutionRouter` |
| governed execution | `ExecutionBoundary` |
| decision state | `DecisionLifecycle` |
| learning assessment | Symbiont / governed learning contracts |
| promotion/evolution | Evolution Gate |
| presentation of systemic/operational views | `GovernedOrchestratorReadSurface` + `OrchestrationViewComposer` |

No read surface can authorize execution, mutate canonical data, promote learning, register capabilities, change routes or pass the Evolution Gate.

## Relationship with CRL

CRL is the orchestrator of the cognitive cycle. It answers: **where is this cognition/decision in the governed lifecycle?**

`GovernedOrchestrator` is the composition coordinator. It answers: **which canonical authorities/capabilities/evidence are required to satisfy this stage?**

`GovernedOrchestratorReadSurface` is the presentation boundary. It answers: **how should the resulting governed state be explained to this audience?**

Therefore:

`CognitiveCore -> CRL -> GovernedOrchestrator -> canonical authorities -> CRL/outcome -> audience-aware read surface`

This is a target integration direction; it does not grant the orchestrator ownership of CRL stages.

## Humanization rules

A systemic diagnosis should, whenever the evidence supports it:

1. identify the observed signal;
2. explain what it means in the ELO architecture;
3. identify what is not yet proven;
4. explain the operational consequence;
5. state why closing the gap is useful;
6. recommend the next governed action;
7. cite/preserve evidence references;
8. provide chart-ready data when useful.

An operational diagnosis should, whenever the evidence supports it:

1. identify the business demand/event;
2. relate demand to model/resources/materials/capacity/coverage;
3. explain risks and gaps;
4. identify missing information and the canonical source to research;
5. explain allowed decisions versus blocked decisions;
6. preserve the distinction between observed indicator and formal KPI;
7. never invent quantities, relations or causal attributions.

## Chart contract

Charts are presentation artifacts. A chart may display, for example:

- number of capabilities by governance state;
- number of skills requiring investigation;
- evidence coverage by operational domain;
- demand/capacity/coverage values when the governed read-model actually provides those values.

A zero record count is not automatically a zero business metric. Missing/empty sources must remain `NO_RECORD`, `SEM_DADO_OPERACIONAL`, `INDETERMINADO` or another explicit fail-closed state.

## Examples

### Systemic/admin

> The budget-analysis skill is implemented but its runtime evidence is partial. This limits the ELO's ability to explain, with traceability, why a solicitation should proceed, be revised or be declined. Connect the skill to the governed runtime evidence before treating that behavior as canonical. Operational impact: budget decisions remain more dependent on manual interpretation.

### Operational

> Commercial demand is observed, but comparable history is missing. Current coverage cannot be projected safely. Ask for the historical comparable demand from the authorized source before recommending additional fabrication or a staffing impact.

Both examples are explanations of governed state, not new authorities or autonomous decisions.
