# Symbiont Skill Pre-Intake

## Purpose

The Symbiont must determine whether a proposed specialist skill is justified by existing reusable components before a new skill is created or absorbed.

This is a **pre-intake assessment**, not a skill creator and not a new authority.

## Canonical flow

```text
SKILL PROPOSAL
      |
      v
SPECIALIST SKILL PRE-INTAKE
      |
      +--> existing governed skill?
      |        |
      |       YES --> REUSE_EXISTING
      |
      +--> inspect required components
               |
               +--> all FOUND --> READY_FOR_INTAKE
               |
               +--> PARTIAL/MISSING --> DEVELOP_FIRST
                                      |
                                      v
                               build missing base
                                      |
                                      v
                               run pre-intake again
                                      |
                                      v
                              SYMBIONT LAB INTAKE
                                      |
                                      v
                                  VALIDATION
                                      |
                                      v
                               EVOLUTION GATE
```

## Decision contract

Each required component is classified as:

- `FOUND`: reusable and explicitly evidenced;
- `PARTIAL`: a related mechanism exists but requires development or reconciliation;
- `MISSING`: no reusable mechanism was evidenced.

The pre-intake result exposes:

- `readiness_score`;
- component status and evidence path;
- `DEVELOP_FIRST` when any required component is not `FOUND`;
- `REUSE_EXISTING` when an existing governed skill matches the proposed domain;
- `READY_FOR_INTAKE` only when all required components are `FOUND` and no governed duplicate was resolved.

## Authority boundaries

- Forge Specialist Skill Registry remains the canonical skill registry.
- Core `SpecialistSkillResolver` provides deterministic resolution and the read-only pre-intake assessment.
- `SymbiontSkillRuntime` exposes the pre-intake operation without becoming a second registry or Evolution Gate.
- Pre-intake does not create skills, mutate Core, grant authorization, persist learning, or promote candidates.
- Evolution Gate remains the promotion authority.

## Anti-duplication rule

The resolver checks for an existing governed skill before accepting a new proposal. A matching existing skill produces `REUSE_EXISTING` rather than a second skill identity.

## Relationship to existing Symbiont flow

The pre-intake sits before the existing:

`SOURCE → EVIDENCE → FORGE SKILL → TEST → EMPIRICAL VALIDATION → CONTEXTUAL EXPERIENCE → GENERALIZATION → EVOLUTION GATE`

It answers one additional question before that flow:

> Is the base already present enough to justify entering skill intake?

It does not replace the existing Symbiont Laboratory or capability absorption mechanisms.
