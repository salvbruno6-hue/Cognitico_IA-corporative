# ELO Domain Faculty Lifecycle

## Purpose

Define how the ELO learns the essential logical mechanics of a specialist member without making the member a second cognitive core and without coupling the ELO's canonical faculty to a local implementation.

## Lifecycle

```text
MEMBER FLOW
  -> LOGIC EXTRACTION
  -> SEMANTIC NORMALIZATION
  -> FACULTY COMPARISON
  -> GOVERNANCE CLASSIFICATION
  -> PROMOTE | OVERLAY | PRESERVE_ALTERNATIVE | REJECT
  -> EVIDENCE RECORD
  -> MATURITY UPDATE
```

## Faculty

`DomainFaculty` represents reusable domain logic: objective, logical steps and invariants. It is owned by the ELO's governed knowledge lifecycle, not by the member that supplied it.

## Overlay

`DomainOverlay` represents a contextual variation or complement supplied by a member. It is versioned, source-attributed and explicitly removable. Removing an overlay must not mutate or corrupt the canonical faculty.

## Comparison

A candidate flow is classified as:

- `COMPATIBLE`: same logical cycle;
- `VARIATION`: shared structure with changed/removed/added mechanics;
- `COMPLEMENT`: new mechanics added without removing canonical mechanics;
- `CONFLICT`: incompatible domain boundary or future canonical conflict;
- `NEW`: reserved for a genuinely novel capability pending governance.

## Knowledge promotion

A mechanic may become part of the ELO faculty only through evidence-backed governance. A promotion record preserves source member/version, domain, evidence, reason and validity. A member can later be detached without deleting promoted knowledge.

## Detachment invariant

```text
member attached -> member teaches -> knowledge evaluated -> knowledge promoted
member detached -> ELO retains promoted knowledge and provenance
```

An overlay or local member detail is not automatically promoted. If a later specialist proposes a different mechanic, the ELO compares it with the current faculty rather than replacing it silently.

## Corporate example

For Commercial A, the ELO may learn:

`intake -> qualification -> proposal -> result`

Commercial B may add a risk check. The ELO keeps the faculty and represents the risk check as a complement/overlay until evidence and governance justify promotion.

Commercial C may replace qualification with a different mechanism. The ELO reports the variation/conflict and preserves the existing faculty; it does not silently erase the previous logic.

## Architectural boundary

This capability does not create a second Cognitive Core, scheduler, provider registry, parallel memory store or operational executor. It consumes the existing ELO evidence, provenance, memory and Evolution Gate contracts.
