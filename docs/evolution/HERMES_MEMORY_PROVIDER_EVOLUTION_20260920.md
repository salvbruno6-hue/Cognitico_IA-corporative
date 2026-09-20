# Hermes External Memory Providers -> ELO Boundary - 2026-09-20

## Current Hermes mechanism

Hermes supports external memory-provider plugins; only one external provider is active at a time alongside built-in memory. Provider context can be injected into the agent working context. Profiles isolate memory and state. External providers are integration mechanisms, not independent ELO authority.

## ELO adaptation

EXT-MEMPROVIDER-HERMES belongs to ELO Memory and is adapter-only.

The provider may supply retrieval/context evidence, but:
- ELO remains the canonical memory authority;
- provider responses require provenance;
- provider output enters the governed temporal/evidence path;
- useful content is not automatically promoted to Evolution Memory;
- provider configuration cannot grant canonical write authority.

## Intake contract

Required:
- provider identity;
- tenant scope;
- operation;
- source references;
- evidence digest;
- verified provenance;
- explicit activation.

CANDIDATE means the adapter contract is sufficiently evidenced for Evolution Gate review. It does not activate the provider in production.

Discovery without explicit activation -> OBSERVATION.
Missing identity/scope/provenance -> REJECTED.
Any canonical write or autonomous promotion attempt -> REJECTED.

## Non-goals

- no provider activation;
- no memory writes;
- no promotion;
- no credential mutation;
- no replacement of ELO temporal/evolution memory;
- no second memory authority.
