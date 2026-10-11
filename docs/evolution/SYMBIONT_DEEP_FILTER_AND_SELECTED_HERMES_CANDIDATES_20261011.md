# Symbiont deep evolution filter + selected Hermes candidates

## Decision

Hermes mechanisms are not admitted because they exist or because they are technically compatible.
A candidate advances only when it deepens an existing ELO mechanism without creating a parallel owner, duplicate capability, authority transfer, or objective drift, and when a repeatable candidate-attributed functional gain is demonstrated.

## Mandatory filter

A candidate must satisfy all conditions:

1. reuse the existing canonical owner;
2. preserve the owner's architectural objective;
3. create no new or parallel authority;
4. duplicate no capability already supplied by that owner;
5. introduce no adaptation that changes the owner's purpose merely to fit Hermes;
6. demonstrate repeatable net functional gain attributable to the candidate;
7. preserve provenance and report controlled evidence separately from production proof.

Failure of 1-5 is `REJECT`. Failure of 6-7 is `RETEST`. Only candidates satisfying all conditions are `ACCEPT` for subsequent ELO review. Acceptance is not automatic Core promotion.

## Candidates admitted by this cycle

### EXT-WIRE-CONTRACT-HERMES

Owner: `ELO Interface`.

Evolution: deterministic versioned fingerprints over the existing `CognitiveRequest`, `CognitiveResponse`, and `ErrorContract` schemas. The registry is observational and creates no transport, endpoint, router, authorization path, or execution authority.

Objective deepened: make changes to the existing interface contract observable and compatibility-reviewable.

### EXT-SESSION-SEARCH-BOUNDS-HERMES

Owner: `ELO Context`.

Evolution: explicit `after`/`before` temporal bounds and an explicit relaxed-recall retry mode that preserves those same temporal bounds. The policy creates no memory store, retrieval engine, provider, persistence path, or secondary context authority.

Objective deepened: improve relevance and retrieval precision while preserving the existing context boundary.

## Controlled evidence

The integration includes deterministic synthetic fixtures only. They execute no business operation and do not invoke or modify Hermes.

- Wire contract: deterministic contract fingerprint capability compared with a baseline lacking that capability.
- Bounded context: out-of-window context admission compared with an unbounded baseline fixture.

These fixtures may establish `FUNCTIONAL_CONTROLLED_GAIN`; they do not establish production effectiveness.

## Automation

`ELO Evolution Gate` now contains a `Symbiont deep capability evolution filter` job. It runs after canonical validation and before the ELO decision handoff. A failure blocks readiness for ELO review. The automation never promotes a candidate, deploys it, or mutates canonical business state.
