# Hermes P0 adaptations: Domain Intelligence + Autonomous Agents

## Purpose

This pair converts two Hermes capability families into reusable ELO boundaries:

1. **Domain Intelligence**: passive, evidence-bearing domain observations with explicit confidence and limitations.
2. **Autonomous AI Agents**: bounded autonomous execution experience with objective, planned actions, constraints, outcome and evidence.

Both are sources of experience, not authorities.

## Canonical flow

```text
Hermes capability
    -> evidence-bearing observation
    -> existing SymbiontPatternIntake
    -> Evolution Gate
    -> LAB_CANDIDATE / REUSE / BLOCK
    -> laboratory validation
    -> regression + governance
    -> only then possible canonical promotion
```

## Domain Intelligence adaptation

The ELO adapter preserves target, provenance, evidence, confidence, observations and limitations. It rejects incomplete evidence and credential-shaped metadata. It does not perform network reconnaissance itself; an authorized Hermes execution remains the acquisition boundary.

## Autonomous Agents adaptation

The ELO adapter treats autonomy as a bounded execution capability. It requires explicit planned actions, constraints, outcome, evidence and limitations. The adapter never executes the actions, grants permissions, writes canonical state or bypasses Evolution Gate.

## Reuse and authority

The implementation reuses `SymbiontPatternIntake` and `EvolutionGate`; it does not create a second candidate registry or evolution engine. Hermes remains an external execution/evidence source.

## Validation status

Unit tests validate the contracts and candidate-only routing. CI must provide the repository's normal behavioral, baseline, maintenance, Pages and Evolution Gate validation. A real provider execution remains a separate authorized integration test and must preserve immutable provenance and evidence lineage.

## Source lineage

Audited Hermes repository: `salvbruno6-hue/ELO-Hermes-Agent`.

Relevant capability families include `optional-skills/research/domain-intel/SKILL.md` and the bundled/optional autonomous-agent skill documentation. The ELO adaptation intentionally consumes behavior through evidence contracts rather than copying provider authority into Core.
