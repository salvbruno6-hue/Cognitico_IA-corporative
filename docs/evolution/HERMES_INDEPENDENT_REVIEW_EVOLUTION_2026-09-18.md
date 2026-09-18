# Hermes → ELO: Independent Review Evidence — 2026-09-18

## Discovery

Current Hermes main exposes an independent /review path that dispatches a
reviewer subagent on the delegation rail. The reviewer receives relevant
working context and can inherit named skills and the normal subagent toolset.
Hermes also documents a software-development skill whose core principle is
that an agent should not verify its own work.

This is an external mechanism reference, not ELO authority.

## ELO candidate

Candidate: HERMES-DELEGATION-REVIEW

Owner: ELO Worker/Delegation + existing Validation/Evolution Gate boundaries.

Purpose: represent independent review as explicit, immutable evidence with
reviewer identity, subject identity, bounded scope, context snapshot, inherited
skills/tools, verdict, findings, evidence references and provenance.

Not introduced: automatic reviewer execution, automatic merge, automatic
promotion, new Core authority, new memory authority, or a second Evolution Gate.

## Relationship to existing ELO architecture

The candidate refines HERMES-DELEGATION and the existing ELO workflow:

EXECUTE → VALIDATE → SPECIALIST_REVIEW → ELO_REVIEW → CORRECT/REPLAN → REVALIDATE

It does not replace EvolutionGate, SourceResolver, ContextResolutionEngine,
KnowledgeOrchestrator, or ELOContextAssembler.

The review contract records evidence; existing governance decides what that
evidence permits.

## Controlled implementation

Implemented:

- src/elo/agent_intake/independent_review.py
- tests/agent_intake/test_independent_review.py

The contract is side-effect free. It rejects reviewer/owner identity reuse,
missing context snapshots, missing evidence, unbounded verdict values and
missing provenance.

The object is immutable and contains no promotion or merge permission field.

## Validation status

The implementation is a validated ELO refinement candidate, not a promoted
canonical policy.

Validation requires:

1. unit tests pass;
2. no mutation of Hermes;
3. no business operation;
4. CI evidence is green;
5. repository review remains separate from review evidence itself.

## Hermes evidence

Current Hermes main inspected at commit
01382698fc32ec7740b6a204d9b7a6abeac74d33.

Relevant surfaces:

- agent/review_engine.py
- gateway/slash_commands_goals.py
- website/docs/user-guide/features/delegation.md
- skills/software-development/requesting-code-review/SKILL.md

## Decision

Do not create a ninth root capability. Treat this as a bounded refinement of
Delegation + Validation. Promotion beyond candidate/refinement status remains
subject to the existing Evolution Gate and repository governance.
