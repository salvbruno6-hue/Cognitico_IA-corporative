# Cognitive Architecture — Implementation Guide

## Purpose

This document defines how the proposed ELO Cognitive Architecture should be analyzed and progressively implemented inside `Cognitico_IA-corporative`.

It is an implementation guide, not an approval to bypass the repository governance model.

## Authority and prerequisites

Before implementation, agents must inspect and respect:

- `AGENTS.md`
- `ELO_REPOSITORY_NAVIGATION_RULES.md`
- `ELO_ARTIFACT_METADATA_STANDARD.md`
- `ELO_AI_AGENT_WORKING_RULES.md`
- approved architecture baselines
- approved ADRs
- canonical contracts and schemas
- current implementation and tests

The repository explicitly requires inspection before editing, reuse of existing contracts, explicit architecture decisions for durable changes, and an evidence path from requirement to contract, implementation, and test.

## Implementation sequence

The architecture should be decomposed into incremental capabilities rather than implemented as one large system.

### Phase 1 — Baseline and gap analysis

Map the proposed cognitive architecture against the current ELO implementation.

Produce:

- capability matrix;
- existing/reuse/extend/new/conflict classification;
- architecture gaps;
- contract gaps;
- data gaps;
- test gaps;
- governance implications;
- ADR requirements.

No implementation should begin until duplicate concepts and authority conflicts are classified.

### Phase 2 — Context

Strengthen the context layer so the ELO can represent:

- organization;
- tenant;
- domain;
- process;
- resources;
- objectives;
- current plan;
- constraints;
- risks;
- events;
- operational state.

The context layer must preserve tenant/domain/principal/session/request/correlation boundaries where applicable.

### Phase 3 — Knowledge and evidence

Integrate curated organizational knowledge, external references, evidence, provenance, and lessons learned without conflating them.

Maintain explicit distinctions between:

- source knowledge;
- evidence;
- hypotheses;
- recommendations;
- decisions;
- organizational experience.

### Phase 4 — Governed reasoning

Build reasoning capabilities behind established governance boundaries.

The reasoning layer must use:

- context;
- evidence;
- knowledge;
- policies;
- constraints;
- provenance.

Reasoning must not bypass policy, evidence, provenance, or the AI Gateway where those boundaries apply.

### Phase 5 — Decision intelligence

Introduce structured decision support with a standard decision contract:

`context → event → problem → evidence → causes → impacts → constraints → alternatives → decision → justification → owner → deadline → indicator → result → learning`

Every recommendation must be explainable and traceable.

### Phase 6 — Scenario intelligence

Introduce scenario evaluation for:

- current state;
- demand growth;
- resource constraints;
- supplier delay;
- plan changes;
- contingencies.

Each scenario should expose assumptions, impacts, risks, constraints, KPI effects, objective effects, and recommended actions.

### Phase 7 — Adaptive replanning

Implement controlled replanning when a material event invalidates or degrades the current plan.

Required sequence:

1. detect event;
2. validate information;
3. identify affected plan/version;
4. propagate impacts;
5. identify conflicts and constraints;
6. generate alternatives;
7. compare alternatives;
8. recommend a new plan;
9. require human approval when policy requires it;
10. version the new plan;
11. communicate changes;
12. monitor execution;
13. record outcome and learning.

The system must explain why the plan changed.

### Phase 8 — Learning

Connect results back to organizational knowledge.

When expected and actual outcomes diverge, capture:

- wrong assumptions;
- omitted variables;
- underestimated dependencies;
- missed indicators;
- policy gaps;
- process lessons;
- new knowledge.

Learning must influence future recommendations through governed knowledge and memory mechanisms.

## Engineering requirements

### Modularity

Use clear boundaries between:

- context;
- knowledge;
- memory;
- evidence;
- reasoning;
- recommendation;
- decision;
- policy;
- provenance;
- agents;
- AI Gateway;
- integration.

### Contracts

Prefer small, versioned contracts over implicit coupling.

Every persistent or externally consumed contract must define:

- identity;
- version;
- owner;
- authority;
- lifecycle;
- validation rules;
- compatibility expectations.

### Data lineage

For critical outputs, retain enough lineage to answer:

- what data was used;
- what knowledge was used;
- what rules were applied;
- what model/reasoning path was used;
- what recommendation was generated;
- who approved the decision;
- what result occurred.

### Confidence and uncertainty

The ELO must distinguish:

- confirmed;
- probable;
- incomplete;
- conflicting;
- stale information.

Uncertainty must be explicit in recommendations.

### Human authority

The ELO should be a governed cognitive copilot.

It may detect, correlate, analyze, simulate, recommend, explain, and anticipate.

Human approval remains mandatory where policy or impact level requires it.

### Testing

Each capability must include:

- unit tests;
- contract tests where applicable;
- scenario tests;
- exception tests;
- regression tests;
- evidence of runtime behavior.

A feature is not considered complete merely because code exists.

## Operational acceptance criteria

A capability is ready only when:

- architectural placement is approved;
- authority is clear;
- contracts are defined;
- implementation maps to the approved capability;
- tests execute and pass as required;
- observability is available where relevant;
- provenance is preserved where relevant;
- failure behavior is defined;
- unresolved risks are documented.

Use the repository status vocabulary consistently: `PROPOSED`, `DRAFT`, `NORMATIVE`, `IMPLEMENTED`, `TESTED`, `VERIFIED`, `EXPERIMENTAL`, `DEPRECATED`, `SUPERSEDED`, `ROADMAP`, `BLOCKED`.

## First implementation task

The first concrete task should not be the adaptive replanning engine.

The first task should be an architectural gap assessment that maps this proposal against the current ELO-001 through ELO-013 roadmap and identifies exactly which capabilities already exist, which can be reused, and which require new contracts or ADRs.

The resulting gap assessment should become the basis for the implementation backlog and architecture decisions.
