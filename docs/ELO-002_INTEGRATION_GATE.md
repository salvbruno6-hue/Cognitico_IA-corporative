# ELO-002 — Integration Verification Gate

## Gate 7 — Integration Service

`ContextualMemoryService` is the application boundary for ELO-002 intake. It resolves context and persists Evidence, Knowledge and Memory while remaining independent from the Cognitive Core.

## Gate 8 — Cognitive integration

The next integration must connect the service to the existing Cognitive API without replacing `CognitiveRequest`, `CognitiveResponse`, `ErrorContract`, `SessionManager` or `CognitiveCore`.

Required flow:

```text
CognitiveRequest
  -> Context resolution
  -> contextual intake/retrieval
  -> CognitiveCore
  -> CognitiveResponse
```

The Core must consume contextual information through an explicit dependency/interface, not import storage implementations directly.

## Gate 9 — Verification

Before merge:

- existing ELO-001 tests pass;
- ELO-002 unit tests pass;
- tenant isolation passes;
- context conflicts fail closed;
- provenance survives the complete intake chain;
- an agent observation remains `UNVERIFIED` until validation;
- no second Cognitive Core exists;
- no production persistence is claimed by the in-memory adapters;
- local execution and test commands are documented.
