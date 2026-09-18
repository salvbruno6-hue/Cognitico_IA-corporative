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


## Symbiont operational contract

The executable boundary is consolidated in
`src/elo/cognitive/symbiont_operational_contract.py`. It does not replace the
existing governance mechanisms; it makes their boundary conditions explicit:

- mandate acknowledgement and ELO authorization are required;
- the default execution path is non-destructive and canonical mutation is rejected;
- governed operations are limited to metadata/read/query and explicitly named reasoning artifacts;
- write/schema-change/DML/DDL and a competing `decision_register` are blocked;
- a decision brief must carry evidence and audit references and remains advisory;
- confidence below 0.70, high risk, canon conflict, insufficient evidence, or financial impact above the owner's limit trigger human escalation;
- PII masking is required only when PII is actually present;
- infrastructure/secret fields and competing canonical ledgers are rejected at the boundary.

These checks are guards around the existing ELO authority. They do not create a
second decision ledger, memory ledger, authorization service, or Evolution Gate.
