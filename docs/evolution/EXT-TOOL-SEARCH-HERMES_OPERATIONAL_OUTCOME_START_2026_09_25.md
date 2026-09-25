# START — EXT-TOOL-SEARCH-HERMES operational outcome evidence

- candidate_id: EXT-TOOL-SEARCH-HERMES
- capability: Progressive Tool Schema Disclosure
- authorization_ref: Issue #740
- owner: ELO Model / Tool Routing
- branch: evo/hermes-operational-outcome-evidence-20260925
- stage: OPERATIONAL_OUTCOME_EVIDENCE
- canonical_authority: ExecutionRouter
- evidence_authority: existing PerformanceEvidence contract
- canonical_mutation: false
- core_promotion: false
- tool_execution: not performed by this adapter

## Objective

Capture the first measured operational outcome without creating a second
measurement, learning, routing, memory, or promotion authority.

## Reuse

- canonical ExecutionRouter
- canonical progressive schema disclosure
- existing PerformanceEvidence
- existing aggregate
- existing Evolution Gate for any later promotion decision

## Required evidence

Only measurements produced by an actual authorized runtime observation may be
supplied: quality, reliability, latency, cost and provenance.

No value is synthesized by the adapter.

## Boundary

This loop records evidence. It does not persist learning, mutate Core/Soul,
approve promotion, deploy Hermes, or create a new governance gate.
