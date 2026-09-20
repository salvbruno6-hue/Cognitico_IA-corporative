# Hermes Profile / Bot Mode — ELO Evolution Boundary

## Source observation

Hermes profiles isolate configuration, credentials, memory, sessions, skills, and
gateway state. Bot Mode presents profiles as named agents with persistent
conversations and configurable capabilities.

## ELO adaptation

Candidate ID: `EXT-PROFILE-HERMES`

The ELO adaptation treats a Hermes profile as an **isolated agent-context
candidate**, not as a new cognitive authority.

A profile may carry identity, scoped configuration, skills, and local state.
It must not gain authority to mutate canonical ELO memory, approve promotion,
govern Git merges, or bypass tenant/scope controls.

## Boundary rules

1. Missing identity, tenant scope, or provenance is rejected.
2. Authority transfer from ELO Core to a profile is rejected.
3. Shared canonical memory is observation-only until a separate governed memory
   contract proves the boundary safe.
4. Isolation and explicit activation are required before a profile becomes a
   candidate.
5. Assessment never creates, activates, executes, or promotes a profile.
6. `canonical_authority`, `execution_permitted`, and
   `promotion_permitted` remain false.

## Relation to existing ELO mechanisms

This is an intake/evaluation boundary around Hermes profile semantics. It does
not replace ELO delegation, context resolution, memory governance, or the
Evolution Gate.

## Test intent

Controlled tests cover valid candidate admission, missing provenance,
authority-transfer rejection, shared-memory containment, and missing
activation/isolation.

No production activation is performed by this change.
