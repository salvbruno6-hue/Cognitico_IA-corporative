# ELO Executable Core — Local Agent Rules

## Scope

`src/elo/` is the canonical executable implementation area identified by the repository README.

## Before editing

Inspect:

1. root `AGENTS.md`;
2. `ELO_REPOSITORY_NAVIGATION_RULES.md`;
3. relevant architecture documents;
4. relevant contracts;
5. existing tests;
6. existing implementation.

## Implementation rules

- Reuse existing contracts.
- Do not create parallel request/response models without an approved reason.
- Keep HTTP transport adapters separate from application boundaries where applicable.
- Keep application boundaries separate from cognitive engines.
- Preserve tenant/domain/principal/session/request/correlation context where required.
- Keep provenance and evidence traceability intact.
- Avoid provider-specific coupling outside the AI Gateway.

## ELO-001

The target vertical slice is:

ELOChat
→ HTTP/API adapter
→ CognitiveAPI
→ Session
→ CognitiveCore
→ ResponseBuilder
→ CognitiveResponse

A test suite collecting zero tests is a gate failure.

## Response contracts

Do not remove canonical response fields simply to simplify the builder. If a field is not populated in the current phase, return its canonical empty/neutral value where the contract requires it.

Confidence must be validated/normalized to its contract range when the contract defines one.

## Errors

External/API errors must use consistent contracts. Internal exceptions must not leak stack traces or sensitive implementation details.

## Testing

Every behavior change requires tests. Prefer behavior tests over implementation-detail tests.

## Scope control

Do not implement future ELO phases merely because the code structure makes them possible. Current phase gates are authoritative.
