# Hermes Research → ELO adaptation

## Purpose

This boundary adapts evidence produced by an authorized Hermes Research skill into the existing ELO Symbiont evolution intake. It does **not** create a second research authority.

The audited Hermes source currently includes the `domain-intel` skill at `optional-skills/research/domain-intel/SKILL.md`. Its documented mechanisms include passive domain reconnaissance, structured JSON output, and explicit limitations around WHOIS/network availability and heuristic availability checks.

## ELO contract

```text
Hermes Research Skill
        ↓
HermesResearchObservation
        ↓
SymbiontPatternIntake
        ↓
Evolution Gate
        ↓
LAB_CANDIDATE / REUSE / BLOCK
```

Research findings must carry:

- tenant identity;
- Hermes skill identity;
- source repository and immutable source commit;
- evidence identifiers;
- question and findings;
- limitations/uncertainty;
- risk and source kind.

The adapter rejects observations without evidence or limitations and rejects credential-shaped metadata.

## Non-goals

This implementation does not:

- call Hermes or the network;
- persist research findings;
- promote knowledge into Core;
- bypass Evolution Gate;
- grant provider authority;
- introduce credentials into the browser or ELO source tree.

## Candidate status

The implementation is a **laboratory adaptation**, not a canonical Research capability. Promotion requires the normal ELO sequence: authorized real execution → evidence → laboratory validation → regression → security/governance validation → Evolution Gate.

## Next real test

Execute one authorized Hermes `domain-intel` run against a controlled domain, capture its structured output and provenance, feed the observation through this adapter, and verify that ELO produces a candidate-only decision while preserving limitations and evidence lineage.
