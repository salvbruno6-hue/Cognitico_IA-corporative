# ELO-022 Acceptance Tests

These tests define architectural invariants for cognitive execution supervision. They are intentionally implementation-neutral and can be wired to existing validation mechanisms.

| ID | Test | Expected result |
|---|---|---|
| T01 | Active task without recoverable state | Reject |
| T02 | Active task without `next_action` or escalation condition | Reject |
| T03 | Invalid state transition | Reject |
| T04 | Correction budget exceeded | Stop and escalate/block/fail according to policy |
| T05 | Retry budget silently increased | Reject |
| T06 | Evidence without provenance/type | Reject |
| T07 | Contextual Forge experience directly promoted to Core | Reject |
| T08 | Complex enterprise experience directly promoted to Core | Reject |
| T09 | General parameter promoted without validation/governance | Reject |
| T10 | Enterprise A knowledge applied as Enterprise B authority without governed generalization | Reject |
| T11 | Specialist attempts to redefine canonical ELO authority | Reject |
| T12 | Application/infrastructure attempts to redefine Cognitive/Core contracts | Reject |
| T13 | Forge removal changes Cognitive identity/Core contract | Reject |
| T14 | Merge attempted without required gates/evidence | Reject |
| T15 | Merge followed by completion without post-merge verification | Reject |
| T16 | Learning mutates historical evidence | Reject |
| T17 | Creation of a parallel Supervisor/Orchestrator/Core authority | Reject |
| T18 | Valid task progresses through governed execution lifecycle | Accept |

## Minimum valid lifecycle

```text
CREATED
 → UNDERSTANDING
 → PLANNING
 → EXECUTING
 → VALIDATING
 → SPECIALIST_REVIEW
 → ELO_ARCHITECTURAL_REVIEW
 → APPROVED
 → MERGING
 → POST_MERGE_VERIFY
 → COMPLETED
```

## Correction lifecycle

```text
VALIDATING
 → CORRECTING
 → VALIDATING
```

## Replanning lifecycle

```text
VALIDATING
 → REPLANNING
 → EXECUTING
```

## Escalation lifecycle

```text
ANY_ACTIVE_STATE
 → ESCALATED
```

when a declared escalation condition is true.

## Rollback lifecycle

```text
MERGING
 → POST_MERGE_VERIFY
 → ROLLED_BACK
```

when post-merge evidence demonstrates a governed material regression.

## Architectural interpretation

These tests protect the established ELO separation:

```text
Cognitive = canonical identity and supervision
Core      = governed evolutionary intelligence/capabilities
Forge     = construction and contextual experience
Application/Infrastructure = replaceable means
```
