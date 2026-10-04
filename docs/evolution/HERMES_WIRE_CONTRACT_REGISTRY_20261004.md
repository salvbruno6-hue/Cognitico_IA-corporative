# Hermes Wire Contract Registry → ELO

## Decision

The Hermes wire-contract mechanism is introduced as an **ELO-side contract-evidence refinement**, not as a new transport or routing authority.

## Existing canonical owner

The existing ELO interface owner is:

- `src/elo/interface/contracts.py`
- `src/elo/interface/api.py`
- Pydantic models: `CognitiveRequest`, `CognitiveResponse`, `ErrorContract`

The refinement adds:

- deterministic registry metadata;
- semantic registry version;
- transport declaration matching the current ELO interface (`HTTP/JSON`);
- SHA-256 schema evidence generated from the existing Pydantic models.

## Explicitly not imported from Hermes

- no JSON-RPC runtime;
- no OpenRPC endpoint;
- no second interface router;
- no generated client authority;
- no new execution path;
- no authorization mechanism;
- no memory or learning mutation.

## Governance boundary

The registry is observational. It identifies and fingerprints existing interface contracts so compatibility changes become reviewable evidence.

It does not authorize execution, mutate canonical state, promote learning, or replace the existing API.

## Validation

The controlled tests require:

1. the three canonical interface contracts are present;
2. contract names are unique;
3. registry version is explicit;
4. transport remains the existing HTTP/JSON boundary;
5. schema fingerprints are deterministic;
6. the registry does not introduce a JSON-RPC execution surface.

## Candidate classification

`HERMES-WIRE-CONTRACT-REGISTRY` is classified as an **implemented refinement of the existing ELO Interface owner**, pending repository CI and Evolution Gate validation.

Functional production benefit is not claimed by this change alone.
