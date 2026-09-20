# Hermes Curator → ELO Lifecycle Boundary — 2026-09-20

## Purpose
Hermes Curator is treated as a maintenance-signal source, not as an ELO knowledge lifecycle authority.

Hermes currently tracks curator-managed skills through active → stale → archived, protects pinned skills, keeps archives recoverable, and distinguishes agent-created skills from user-directed /learn skills. ELO preserves those distinctions while keeping canonical knowledge under ELO governance.

## Contract
- EXT-CURATOR-HERMES is candidate-only.
- Every signal requires tenant scope, skill identity, and provenance.
- stale produces REVIEW_REQUIRED.
- archived produces RETIREMENT_CANDIDATE.
- pinned, user-directed, or unmanaged skills remain observations.
- no signal grants canonical authority.
- no signal permits mutation, deletion, archival, or consolidation of ELO canonical knowledge.
- retirement/consolidation decisions require existing ELO evidence, conflict, learning-governance, human-approval and Evolution Gate controls.

## Architectural relation
Hermes Curator supplies evidence for validity/obsolescence management. It does not replace the ELO Learning Laboratory or Evolution Gate.

Hermes recoverable archive semantics do not authorize ELO to archive or delete canonical knowledge. A curator signal may open a review candidate; ELO must then compare dependencies and provenance and decide whether a governed retirement/consolidation package is warranted.

User-directed /learn skills are intentionally not curator-managed by Hermes. This boundary therefore keeps them as observations unless a separate governed process admits them.

## Controlled validation
The test module covers stale review, archived retirement candidacy, pin protection, user-directed learning, and missing provenance.

## Non-goals
- no filesystem mutation;
- no skill deletion;
- no automatic consolidation;
- no direct Hermes modification;
- no promotion into ELO Core.