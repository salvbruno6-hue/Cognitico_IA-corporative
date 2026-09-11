# Symbiont → Hermes Governed Execution

## Purpose

This boundary connects ELO Cognitive to the external Hermes runtime without moving authority out of ELO.

```text
ELO Cognitive
    │
    │ already-authorized HermesExecutionRequest
    ▼
SymbiontHermesBridge
    │
    │ authorized capability only
    ▼
Hermes /elo/v1/execute
    │
    ▼
Hermes execution
    │
    ├── evidence
    ├── outcome
    └── learning_candidate
    │
    ▼
Symbiont receipt → ELO Cognitive
```

## Ownership

- **ELO Cognitive/Core:** authorization, canonical identity, governance and evolution decisions.
- **Symbiont:** connector, translation, boundary validation and receipt normalization.
- **Hermes:** external execution/orchestration runtime.
- **Evolution Gate:** sole authority for evolution classification.
- **Learning:** remains candidate-only until the existing governed promotion flow accepts it.

## Invariants

1. Symbiont cannot grant a capability that is absent from `authorized_capabilities`.
2. Hermes receives the ELO-generated request; Symbiont does not re-authorize it.
3. The `request_id` remains the correlation key across the boundary.
4. Required execution/outcome evidence must be present before a receipt is accepted.
5. Infrastructure identifiers remain rejected by the Hermes contract.
6. Hermes learning output cannot become canonical knowledge through this bridge.
7. No second Evolution Gate, memory authority, authentication authority, or canonical registry is introduced.
8. A runtime failure is evidence of execution failure, not permission to mutate Core.

## Scope

This stage establishes the executable boundary. It intentionally does not implement automatic skill creation, autonomous promotion, or direct browser-to-Hermes communication. Those concerns remain behind the existing governed architecture.
