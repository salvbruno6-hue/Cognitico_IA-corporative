# ELO external-AI contract reconciliation

This note records the implementation adjustment made before any operational validation of external-AI/data-source execution.

## Reuse

The Symbiont already had the underlying controls:

- tenant scope and authorized capabilities;
- evidence requirements and provenance;
- read-only-first execution;
- candidate-only learning boundaries;
- Evolution Gate and Governed Learning;
- human escalation and confidence primitives;
- no canonical mutation by external providers.

## Consolidation

The new `src/elo/cognitive/governed_external_ai_contract.py` consolidates the missing contract-level pieces without introducing a second authority:

- `ExternalAIMandateAck` makes mandate acknowledgement explicit;
- `GovernedExternalAIEnvelope` binds the acknowledged mandate to tenant scope, capabilities and evidence requirements;\n- `authorization_decision_id` is mandatory provenance: capabilities are treated as ELO-issued authorization output, not as self-asserted authority from the external AI;
- `DecisionBrief` standardizes the consultative output and its audit metadata;
- confidence below `0.70` requires explicit `LOW_CONFIDENCE` escalation;
- other escalation reasons are explicit and closed-set;
- canonical mutation cannot be granted by this external-AI envelope;\n- empty capabilities and missing authorization provenance are rejected before runtime execution.

## Authority rule

This module is a contract boundary only. It does not authorize identities, choose tools, persist canonical knowledge, create a second decision ledger, or promote candidates. Existing ELO authorization, routing, Evolution Gate, Decision Outcome Loop where applicable, and Learning Governance remain the owners of those responsibilities.

## Validation boundary

No external connector, external database, MCP server, or production migration is validated merely because these contracts instantiate successfully. Runtime validation remains a separate gate requiring authorization, tenant isolation, credential resolution, provenance, audit integrity and fail-closed behavior.

## Additional pre-validation guards

The contract boundary now also rejects:

- decision briefs without alternatives or trade-offs;
- secret-bearing audit metadata such as passwords, tokens, API keys or database URLs;
- audit request/tenant identifiers that disagree with the brief;
- explicit unmasked PII exposure by an external-AI envelope;
- financial impact above a declared limit unless FINANCIAL_LIMIT escalation is present.

These checks are preconditions only. They do not replace elo-authz, the canonical risk/financial governance, or the Evolution Gate.

## Consolidation correction

A pre-validation audit found that `symbiont_governance_contract.py` and `governed_external_ai_contract.py` had overlapping mandate and decision-brief definitions. The duplicate definitions were removed from the Symbiont governance module; it now acts as a compatibility facade over the canonical external-AI contract. This prevents two competing Symbiont mandate/decision-brief authorities.
