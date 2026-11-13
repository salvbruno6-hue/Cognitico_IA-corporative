# ELO — Successful Operational Activation of the 8 Candidates

The eight Hermes capability candidates now use `success` as the successful promotion state.
`ACTIVE_OPERATIONAL` remains a compatibility alias for that state.

## Effective operational activation

A green native functional proof, intact provenance and complete governance are required.
After those checks pass, `activate_operational_capabilities()` registers the eight native
mechanisms in ELO's existing provider-neutral `CapabilityRegistry`.

The registry is the existing runtime authority for capability availability. Each mechanism
is registered as `elo-native`, health-probed through its native implementation, and carries
non-secret metadata indicating `promotion_state=success`.

The eight active mechanisms are:

- `HERMES-MEMORY`
- `HERMES-SKILLS`
- `HERMES-TOOLSETS`
- `HERMES-CONTEXT`
- `HERMES-DELEGATION`
- `HERMES-AUTOMATION`
- `HERMES-MCP`
- `HERMES-CHECKPOINT`

## Core remains protected

Operational success does not mutate Core. Canonization still requires explicit Core-pillar
relevance and Evolution Gate approval. The promotion layer does not silently mutate canonical
knowledge.

## Validation target

The test suite validates both layers:

1. all eight candidates reach `success`;
2. `ACTIVE_OPERATIONAL` remains an alias for `success`;
3. all eight mechanisms are available through the existing ELO capability registry;
4. Core canonization remains blocked unless its explicit gates are supplied.
