# START — EXT-TOOL-SEARCH-HERMES indirect capability evidence

- candidate_id: EXT-TOOL-SEARCH-HERMES
- capability: Progressive Tool Schema Disclosure
- stage: INDIRECT_CAPABILITY_EVIDENCE
- owner: ELO Model / Tool Routing
- canonical_authority: ExecutionRouter
- evidence_authority: existing PerformanceEvidence
- observer: an already validated downstream capability/experience
- canonical_mutation: false
- core_promotion: false

## Objective

Allow the skill to be evaluated through the experience of another capability
that is already validated and operational, without requiring the evaluated
skill to own production traffic.

## Evidence model

The downstream capability supplies an observed result. The adapter records the
relationship between:

skill evaluated -> validated observer capability -> experience -> observed outcome

The adapter does not infer causality. The caller must provide the observer,
experience reference, expected outcome, observed outcome and relationship.

## Boundary

This is corroborating efficacy evidence, not production-readiness evidence.
It reuses PerformanceEvidence and aggregate. It does not create a second
evidence authority, execute tools, persist learning, mutate Core/Soul, or
authorize promotion.
