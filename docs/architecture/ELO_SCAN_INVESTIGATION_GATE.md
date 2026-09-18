# ELO Scan Investigation Gate

## Purpose

Every ELO scan request must begin with a bounded investigation definition before source extraction, learning classification, or corrective action.

## Canonical order

```
REQUEST
→ OBJECTIVE
→ SCOPE + SUCCESS CRITERIA
→ HYPOTHESES / PROBABILITIES
→ RELATION / CASCADE INVESTIGATION
→ EVIDENCE
→ COHERENCE TEST
→ CONCEPT CLASSIFICATION
→ OBJECTIVE RESULT
→ LEARNING GOVERNANCE
```

## Hard Skill ownership

The investigation method is a Hard Skill. The orchestrator executes the governed runtime boundary; it does not invent a second investigation methodology.

## Mandatory fields

Each scan mission must define:

- objective
- scope
- expected_output
- success_criteria
- constraints
- prohibited_actions
- hypotheses
- relevant_source_domains

## Investigation rules

1. Objective must be explicit and testable.
2. Hypotheses are alternatives to investigate, not conclusions.
3. Probability is a prioritization signal only; evidence determines support.
4. When the objective crosses domains, investigate relationships and cascades before isolated records.
5. A foreign key or structural relationship is not by itself evidence of causality.
6. Preserve provenance, source identity, scope, and relevant timestamps/revisions.
7. Record contradictions and evidence gaps.
8. Prefer an existing ELO capability/owner over creating a duplicate mechanism.
9. A scan finding is not learning.
10. Learning candidates route through existing governed learning structures and Evolution Gate.
11. No canonical mutation or automatic learning promotion occurs during investigation.

## Concept classification

Allowed investigation outcomes:

- SUPPORTED
- PARTIALLY_SUPPORTED
- UNRESOLVED
- CONTRADICTED
- INSUFFICIENT_EVIDENCE

A solid concept is one supported by the available evidence within the declared scope and objective.

## Cascade requirement

For cross-domain objectives, the investigation should reconstruct relevant paths such as:

```
DEMANDA
├── PCP → PRODUÇÃO
├── MATERIAL → ALMOXARIFADO
├── COMPRA → FORNECEDOR → COTAÇÃO
├── RH
├── OPERAÇÃO EXTERNA
└── ORÇAMENTO
```

Only relationships supported by the actual data model and evidence may be used.

## Runtime boundary

The scan orchestrator must not execute a mission merely because a source is stale or a row exists. It first establishes the investigation objective and bounded evidence plan. Runtime observation can then determine whether the mission is CONTINUE, CORRECT, REPLAN, ESCALATE, BLOCKED, or routed to the governed learning path.

## Invariant

```
NO OBJECTIVE → NO INVESTIGATION
NO EVIDENCE → NO LEARNING
NO GOVERNANCE → NO PROMOTION
```
