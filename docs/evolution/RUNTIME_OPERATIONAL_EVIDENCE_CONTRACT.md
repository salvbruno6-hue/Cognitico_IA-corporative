# Runtime Operational Evidence

## Purpose

This contract records evidence emitted by an actual runtime boundary for a governed ELO mechanism.

It is an evidence layer, not a new authority, Evolution Gate, learning store, or promotion mechanism.

## Required evidence

A record requires:
- execution_id generated when the runtime execution starts;
- candidate_id;
- existing canonical owner;
- exact runtime_entrypoint;
- timestamp;
- action_observed=true from the runtime;
- operational metric and observed value;
- candidate attribution;
- source commit;
- runtime trace identifier;
- repeatability across at least two executions;
- explicit regression state;
- deterministic evidence hash.

## What this proves

A valid record proves that the runtime supplied evidence of an observed action and its measured result.

It does not authorize implementation, approve an Evolution Gate, mutate canonical state, prove long-term production impact, or replace ELO review.

## Anti-false-positive rules

The producer must not set action_observed=true merely because a unit test passed, a controlled evaluator passed, a candidate exists, a handoff exists, or an implementation branch exists.

The runtime must supply the observation. Candidate attribution is required; owner-level behavior cannot be relabeled as candidate behavior.

## Relationship to the existing loop

FUNCTIONAL_CONTROLLED_GAIN -> ELO_REVIEW -> EVOLUTION_GATE -> IMPLEMENTATION_AUTHORIZED -> RUNTIME_INTEGRATION -> RUNTIME_OPERATIONAL_EVIDENCE -> OPERATIONAL_OUTCOME -> LEARNING / SYMBIONT

This layer closes the evidence gap identified by the Hermes runtime integration audit without introducing another governance authority.

## Repeated-execution collection

Runtime observations may be accumulated by an observational collector, but the
collector is not a persistence authority, learning authority, or promotion
gate. It must reuse the configured evidence sink and the canonical operational
outcome adapter.

Repeatability requires distinct `execution_id` values for the same candidate,
canonical owner, metric, metric direction, and exact runtime entrypoint.
Duplicate execution identifiers must be rejected and observations from
different runtime entrypoints must not be combined into one operational proof.

A single observation remains controlled evidence. Only the existing operational
outcome adapter may classify compatible repeated observations as
`OPERATIONAL_OUTCOME`; the resulting evidence then returns to the existing
Simbiont / Governed Learning path and remains subject to ELO governance.
