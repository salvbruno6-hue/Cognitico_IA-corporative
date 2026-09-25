# ELO Symbiont — Idempotent Resume Contract

## Purpose

The Symbiont must continue governed execution without relying on a conversational `Continue`. This contract provides durable operational state, deterministic operation identity, lease protection, reconciliation and bounded retry.

It does not create a new Supervisor, Orchestrator, Memory authority, Evolution Gate or promotion authority. Execution supervision remains owned by the ELO Cognitivo.

## Invariants

1. `execution_id` remains stable for one governed execution.
2. `operation_key` is deterministic for `(execution_id, iteration, stage, operation_type)`.
3. A completed operation is never executed again.
4. An `IN_PROGRESS` operation is reconciled before retry.
5. Ambiguous external effects require human escalation.
6. Retry budgets cannot increase silently.
7. State advances only after the operation result is persisted.
8. A new attempt is represented by a new iteration; historical iterations are not overwritten.
9. Production, promotion, canonicalization and authority changes remain governed boundaries.
10. Operational state is distinct from cognitive memory, evidence, experience and canonical knowledge.

## Resume protocol

```text
LOAD STATE
  ↓
ACQUIRE LEASE
  ↓
TERMINAL?
  ├─ yes → RETURN
  └─ no
      ↓
VALIDATE NEXT_ACTION
      ↓
DERIVE operation_key
      ↓
LOAD OPERATION
      ↓
COMPLETED? ── yes → reuse result
      │
      no
      ↓
IN_PROGRESS? ── yes → RECONCILE
      │                  ├─ found → persist completion
      │                  ├─ ambiguous → HUMAN_APPROVAL_REQUIRED
      │                  └─ absent → retry if budget allows
      ↓
EXECUTE IDEMPOTENTLY
      ↓
PERSIST RESULT + EVIDENCE
      ↓
ADVANCE STATE
      ↓
CONTINUE OR GOVERNANCE BOUNDARY
```

## Deterministic identity

```text
operation_key = hash(execution_id + iteration + stage + operation_type)
effect_key = hash(operation_key + input_fingerprint + environment + tool_version)
```

The keys are identities, not evidence of success. Success still requires a verified result and corresponding evidence.

## Operational state versus knowledge

```text
Operational State → where execution is
Evidence          → what was observed
Experience        → what was learned from execution
Canonical Knowledge → what ELO has formally promoted
```

The resume mechanism may reference evidence and experience, but it does not promote them.

## Human boundary

Automatic continuation stops only when a declared boundary requires authority, including:

- production authorization;
- promotion;
- canonicalization;
- authority change;
- ambiguous external effect;
- exhausted retry/correction budget;
- unresolved contradictory evidence.

A technical failure with a deterministic, bounded correction path remains inside the autonomous loop.

## Acceptance property

```text
RESUME(RESUME(RESUME(state))) == RESUME(state)
```

Equality is evaluated over logical state, operation effects, evidence identity and authority boundaries.

## Reference implementation

`src/elo/cognitive/symbiont_execution.py`

## Reference tests

`tests/cognitive/test_symbiont_execution.py`