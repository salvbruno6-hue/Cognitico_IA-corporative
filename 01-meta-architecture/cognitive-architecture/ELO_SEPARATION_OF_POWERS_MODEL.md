# ELO — Separation of Powers and Canonical Operating Model

## Purpose

Define the canonical relationship between ELO Cognitivo, ELO Core, ELO Forge and Validation/Governance inside the `Cognitico_IA-corporative` repository.

## Canonical model

```text
                    ELO COGNITIVO
                 normative authority
                         |
                         | rules / contracts /
                         | architecture / decisions
                         v
                      ELO CORE
                execution of capabilities
                         |
                         | governed tasks
                         v
                   ELO FORGE
             construction / experiment /
                 testing / correction
                         |
                         v
                  VALIDATION/GOVERNANCE
               conformity / evidence /
                security / acceptance
                         |
                         v
                       MERGE
                         |
                         v
                    CANONICAL MAIN
```

## Definitions

### ELO Cognitivo

The canonical intelligence and governance layer. It owns architectural meaning, knowledge, context, memory, evidence, reasoning, policies, decisions, provenance and governed evolution.

It answers:

> What should be done, why, under which constraints and according to which canonical knowledge?

### ELO Core

The canonical executable core that materializes cognitive capabilities through contracts and runtime mechanisms.

It answers:

> How are the canonical cognitive capabilities executed?

### ELO Forge

The internal constructor plane of the canonical Cognitico repository. Forge builds, experiments, tests, corrects and prepares changes for promotion. Forge has no independent architectural authority.

It answers:

> How do we safely build and validate what the canonical ELO decided to change?

### Validation/Governance

The control layer that verifies whether implementation conforms to canonical contracts, acceptance criteria, security requirements, evidence requirements and repository policy.

It answers:

> Does this change comply with what the ELO decided and with the repository's protected rules?

## Authority rules

1. `main` is the canonical integrated state.
2. ELO Cognitivo defines normative architecture and canonical contracts.
3. ELO Core implements canonical capabilities.
4. ELO Forge is a constructor, not a second cognitive authority.
5. Forge may propose architectural changes, but cannot silently redefine the canonical architecture.
6. Validation/Governance may reject a change but does not become a parallel architecture owner.
7. A change becomes canonical only after governed promotion into `main`.
8. External repositories, including the historical `ELO-Forge` repository, are not canonical authorities.

## Branch model

Forge work occurs inside the canonical repository through task-scoped branches:

```text
main
  |
  +-- forge/<task>
  +-- forge/<experiment>
  +-- forge/<construction>
```

Feature branches may use normal `feat/*` naming when repository automation requires it, but the semantic role remains constructor work inside the canonical repository.

## Divergence protocol

When Forge detects divergence from the canonical architecture:

```text
DIVERGENCE
   |
   +-- implementation defect -> correct implementation
   +-- contract mismatch -> adapt implementation
   +-- duplicate -> consolidate
   +-- naming/location issue -> reconcile
   +-- architectural conflict -> ELO decision / ADR
   +-- insufficient evidence -> investigate
```

Forge must never change the canonical architecture merely to make construction easier.

## Promotion rule for Forge artifacts

Presence in Forge does not imply canonical status.

Every candidate must be classified as:

- CANONICAL
- CONTRACT
- KNOWLEDGE
- IMPLEMENTATION
- EXPERIMENTAL
- HISTORICAL
- REJECTED

Only the appropriate class may be promoted, and promotion requires comparison with the canonical architecture.

## Operational implementation rule

Operational SQL, migrations, runtime configuration, dashboards, generated artifacts, and other implementation-specific assets from historical Forge sources are not promoted automatically.

They may be inspected for evidence or reusable design ideas, but only reconciled output that adds value and conforms to the canonical ELO may enter the canonical architecture.

## Autonomous execution

The separation of powers must not reduce autonomy. The ELO agent loop remains:

```text
OBJECTIVE
→ DECOMPOSE
→ CORE / FORGE EXECUTION
→ VALIDATE
→ SPECIALIST REVIEW
→ ELO COGNITIVE REVIEW
→ CORRECT
→ REVALIDATE
→ APPROVE_MERGE
→ MERGE
→ VERIFY
→ REPORT
```

The user is an escalation authority, not a required operator for every intermediate step.

## Core constitutional principle

> No component should simultaneously possess unilateral authority to define, implement, validate and promote a canonical architectural change.

This separation enables autonomous engineering while preserving architectural coherence.
