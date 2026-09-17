# ELO — Outcome Feedback Boundary

## Purpose

Define the non-destructive boundary between operational outcome feedback and systemic interpretation.

## Architecture

```text
DecisionRecord
    |
    v
Execution / Experience
    |
    v
Outcome
    |
    v
Operational OutcomeFeedback
    |
    |  preserve decision_id, outcome identity, expected, observed, assessment, evidence
    v
Systemic Interpretation
    |
    +--> variance
    +--> causal assessment
    +--> temporal validity
    +--> uncertainty
    +--> scenarios / systemic relations
    |
    v
Learning Candidate
    |
    v
Evolution Gate
    |
    +--> reject / retain as evidence
    +--> promote when governed
    |
    v
Canonical ELO
```

## Responsibilities

### Operational feedback

The operational feedback contract is optimized for fast, immutable recording of what happened after a decision. It must not require systemic analysis to be recorded.

Minimum semantic content:

- decision identity;
- outcome identity;
- expected result;
- observed result;
- assessment;
- evidence references.

### Systemic interpretation

The systemic layer interprets already-observed outcomes. It can add:

- variance between expected and observed;
- temporal information;
- causal assessment;
- uncertainty and limitations;
- scenario implications;
- evidence-backed systemic relations.

It must preserve provenance back to the operational outcome and must not overwrite the operational record.

## Governance rules

1. Operational feedback is evidence, not automatically canonical knowledge.
2. Systemic interpretation is derived knowledge, not a replacement for the original outcome.
3. Missing systemic fields do not invalidate a valid operational outcome.
4. Causal claims require explicit evidence and bounded confidence.
5. Learning candidates do not become canonical ELO knowledge without the existing Evolution Gate.
6. The boundary must remain provider-neutral and must not authorize execution.
7. The runtime may remain lightweight; systemic enrichment can occur asynchronously or in a later cognitive cycle.
8. The two existing `OutcomeFeedback` classes must not be silently renamed, merged, or deleted until compatibility and ownership are explicitly tested.

## Compatibility direction

The preferred evolution path is additive:

```text
existing operational record
        |
        +----> systemic interpretation reference
                         |
                         +----> systemic primitives
```

The first implementation should therefore introduce an explicit adapter/translation boundary rather than making either existing contract depend directly on the other.

## Why this model is mature

This separation provides:

- low-latency operational recording;
- richer systemic reasoning when evidence permits;
- independent evolution of runtime and cognition;
- traceability from learning back to the original outcome;
- controlled promotion through Evolution Gate;
- reduced coupling between execution and systemic intelligence.

## Non-goals

This document does not decide the final public name of either contract, does not delete either implementation, and does not define an `IntentSpec -> condition -> capability_id` classifier.
