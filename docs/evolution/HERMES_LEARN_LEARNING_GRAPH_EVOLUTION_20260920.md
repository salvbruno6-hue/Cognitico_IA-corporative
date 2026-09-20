# Hermes Learn + Learning Graph -> ELO — 2026-09-20

## Discovery

Current Hermes exposes /learn as a normal agent turn that gathers requested
sources and asks the agent to author a reusable SKILL.md. The resulting skill
is recorded with learning provenance. Hermes also exposes a learning journey /
memory graph that relates learned skills and memory nodes; graph membership is
driven by learning signals such as a learned skill or actual use.

The Curator separately maintains selected agent-created skills by tracking use,
staleness, archival and review. User-directed /learn results are intentionally
not treated as curator-managed agent-created skills.

## ELO comparison

ELO already has a stricter learning lifecycle:
EXPERIENCE -> evidence -> LEARNING_CANDIDATE -> validation -> governed
promotion -> Evolution Gate -> VALIDATED_LEARNING.

Therefore Hermes /learn cannot become an ELO promotion shortcut.

The Learning Graph is useful as a relation/evidence surface, but it cannot
become canonical memory, a rule engine, or a promotion authority.

## Candidate introduction

EXT-LEARN-HERMES:
- owner: ELO Knowledge & Skills;
- source provenance required;
- unverified learning remains observation;
- verified learning becomes candidate-only;
- tenant scope preserved;
- no promotion authority.

EXT-LEARNING-GRAPH-HERMES:
- owner: ELO Evolution Memory;
- relations connect learning signals, evidence and skills;
- evidence references are mandatory;
- self-relations are rejected;
- graph metadata cannot change canonical authority.

## Controlled implementation

Implemented in:
- src/elo/agent_intake/hermes_learning_boundary.py
- tests/agent_intake/test_hermes_learning_boundary.py

No Hermes mutation, business operation, skill write, or canonical memory mutation
occurs in the adapter.

## Validation

The controlled suite verifies verified-learning admission, unverified observation,
provenance rejection, evidence-required graph relations, and non-authority.

Repository-wide CI remains separately governed; the unrelated missing operator
GitHub binding migration is not included.

## Governance

This validates an intake contract, not autonomous learning promotion.
Production activation remains subject to the Evolution Gate.
