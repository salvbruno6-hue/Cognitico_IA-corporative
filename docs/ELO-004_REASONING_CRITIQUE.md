# ELO-004 — Reasoning + Critique

## Objective

Turn ELO from a system that can receive contextual information into a system that can evaluate claims against explicit evidence, expose uncertainty, identify contradictions, formulate hypotheses and critique its own conclusions before decision support.

## Canonical flow

```text
CognitiveRequest
    ↓
Context
    ↓
Knowledge / Evidence / Memory
    ↓
ReasoningService
    ↓
Evidence evaluation
    ↓
Finding
    ↓
Self-critique
    ↓
Confidence adjustment
    ↓
Unresolved questions
    ↓
Cognitive Core / Decision Support
```

## Non-goals

- autonomous business execution;
- silent modification of memory;
- treating model output as verified fact;
- causal certainty without evidence;
- replacing the Cognitive Core;
- model training;
- production RAG infrastructure.

## Finding taxonomy

- `FACT`: explicitly established by governed evidence;
- `INFERENCE`: conclusion derived from evidence;
- `HYPOTHESIS`: plausible explanation requiring validation;
- `RISK`: evidence-grounded adverse possibility;
- `OPPORTUNITY`: evidence-grounded beneficial possibility;
- `UNKNOWN`: insufficient basis for a conclusion.

## Claim status

- `SUPPORTED` — supporting evidence exists;
- `PARTIALLY_SUPPORTED` — support exists but relevant contradiction/uncertainty remains;
- `UNVERIFIED` — evidence is insufficient;
- `CONTRADICTED` — contrary evidence dominates.

## Critique requirements

Every reasoning result should expose, when applicable:

1. supporting evidence;
2. contradictory evidence;
3. assumptions;
4. missing evidence;
5. alternative hypotheses;
6. confidence;
7. unresolved questions;
8. recommended next validation step.

## Evidence rule

Confidence does not create evidence. Evidence references must remain traceable to the ELO-002 evidence boundary.

## Self-critique rule

The system must actively attempt to falsify or weaken its own finding. A successful critique does not mean the finding is wrong; it means uncertainty has been made explicit.

## Decision boundary

ELO-004 produces analysis and critique. It does not execute a business decision. Decision support and human dialogue are subsequent capabilities.

## Security

Reasoning must preserve tenant, domain, principal and provenance boundaries. Evidence from another tenant cannot be introduced into a reasoning context.

## Acceptance criteria

- [ ] typed reasoning contracts exist;
- [ ] evidence-grounded reasoning exists;
- [ ] contradictions are represented;
- [ ] insufficient evidence produces `UNKNOWN/UNVERIFIED`;
- [ ] critique produces alternative hypotheses;
- [ ] confidence is bounded 0..1;
- [ ] high confidence requires evidence references;
- [ ] reasoning cannot execute business tools;
- [ ] provenance is preserved;
- [ ] tests cover supported, contradictory and missing evidence;
- [ ] ELO-001/ELO-002 contracts remain untouched;
- [ ] no second cognitive core exists.

## Definition of Done

ELO-004 is ready for merge only when implementation, tests, documentation and repository comparison are complete. CI evidence must be reported separately from code presence; a test file is not evidence that the tests passed.
