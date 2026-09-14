# Hermes P0 — Skill Authoring + Knowledge Capture

## Source mechanisms

The Hermes `hermes-agent-skill-authoring` skill was used as comparative evidence for deterministic authoring rules: compact capability descriptions, explicit metadata, platform auditing, provenance, verification and duplicate avoidance. The mechanism is generalized here; Hermes is not a runtime dependency or canonical authority.

The ELO repository already contains canonical Forge skill resolution and governed learning/memory paths. This cycle therefore adds only the missing native preparation boundaries rather than a second registry or memory store.

## Native ELO implementation

- `src/elo/forge/skill_authoring.py` prepares a validated `SkillCandidate`.
- `src/elo/cognitive/knowledge_capture.py` prepares evidence-bearing observations and deterministic fingerprints.
- Duplicate knowledge returns `DUPLICATE`; same concept with a different fingerprint returns `CONFLICT_REVIEW` rather than overwriting canonical knowledge.
- Secret-bearing provenance, missing evidence, invalid skill metadata and duplicate skill identifiers are rejected.
- No file write, Forge registry mutation, Core promotion, authorization grant, or provider-specific execution occurs in these boundaries.

## Acceptance tests

1. Valid skill candidate is deterministic and normalized.
2. Existing skill cannot be duplicated.
3. Knowledge requires evidence and provenance.
4. Duplicate fingerprint is detected without mutation.
5. Concept collision becomes explicit reconciliation work.
6. Secret-bearing provenance is rejected.

## Governance

Promotion remains downstream of the existing learning governance and Evolution Gate. Capture is not consolidation, and a candidate is not canonical knowledge until the existing governed lifecycle validates it.

## Potentialization

Skill Authoring increases ELO's ability to turn validated mechanisms into reusable Forge capabilities. Knowledge Capture increases the quality of cognitive memory admission by making provenance, evidence, deduplication and conflict explicit before consolidation.
