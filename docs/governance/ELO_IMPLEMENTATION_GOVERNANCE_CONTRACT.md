# ELO Implementation Governance Contract

## Purpose

Every Symbiont implementation loop must expose a governance read view at its
start and at its end. The view establishes where the implementation belongs in
the canonical ELO tree and makes its relationships and governance state
observable without granting the view mutation authority.

## Mandatory identity

Each view must identify:

- implementation_id
- candidate_id
- owner
- functional_branch
- capability
- optional specialization
- source reference and source commit
- related contracts
- dependencies
- evidence references
- environment
- loop stage and result

## Ownership resolution

An implementation must resolve to one of:

CANONICAL, EXTENSION, INTEGRATION, EXISTING_BUT_UNWIRED, PARTIAL, MISSING,
DUPLICATE, CONFLICT, UNRESOLVED.

UNRESOLVED is a governance diagnostic, not approval.

The resolver must prefer an existing canonical owner. A new implementation is
not permitted to silently create a parallel branch of responsibility.

## Loop boundary

The mandatory sequence is:

START VIEW → governed implementation loop → END VIEW

The START view captures the intended ownership and evidence boundary before
technical progression. The END view captures the resulting stage, result and
governance/runtime states.

A failed, rejected or retest result still produces the END view.

## Relationship to existing governance

This contract reuses the existing:

- implementation loop;
- implementation readiness/evidence contracts;
- Evolution Gate;
- Learning Governance;
- Evolution Dashboard read model.

It does not create a second Evolution Gate, deployment authority, learning store
or dashboard authority.

## Deployment distinction

A merged implementation and a deployed implementation are different states.
The view therefore records source_commit, runtime_status and environment
separately. NOT_DEPLOYED is the default runtime state unless deployment
evidence exists.

## Authority boundary

The view is read-only:

- it cannot authorize canonical mutation;
- it cannot approve Evolution Gate;
- it cannot promote learning;
- it cannot deploy;
- it cannot alter Core/Soul.

The governance system consumes the view to determine whether the implementation
is correctly attached to the canonical ELO tree and whether the next governed
action is justified.

## Canonical flow

IMPLEMENTATION → GOVERNANCE VIEW → OWNER/BRANCH RESOLUTION → EVIDENCE →
EVOLUTION GATE → GOVERNANCE → MERGE → DEPLOY → RUNTIME EVIDENCE →
EVOLUÇÃO_DE_CAPACIDADES
