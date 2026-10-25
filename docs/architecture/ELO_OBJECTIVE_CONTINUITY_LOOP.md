# ELO Objective Continuity Loop

## Purpose

Keep ELO persistent on a governed objective across repeated executions, chat/process restarts and repetitive workstreams without creating a second objective authority, supervisor, scheduler or execution engine.

## Existing owners reused

- Strategic objective identity and approved targets: existing OKR contracts/repository.
- Execution persistence, idempotency and recovery: `SymbiontExecutionStore`.
- Cognitive supervision and next-action policy: ELO Cognitivo.
- Replanning: existing ELO-010 semantics / governed decision path.
- Learning: Symbiont + Evolution Gate + Governed Learning.
- Scheduling/wakeup: external ChatGPT automation or future canonical scheduler; scheduling does not become objective authority.

## Stable binding

Each workstream gets a deterministic execution identity from:

```text
tenant_id + objective_id + workstream_id
```

The same objective/workstream therefore resumes the same durable execution after a new chat, process restart or scheduled wakeup.

## Loop

```text
OBJECTIVE
  -> WORKSTREAM
  -> CHECKPOINT
  -> EXECUTE ONE BOUNDED CYCLE
  -> RECORD EVIDENCE + PROGRESS TOKEN
  -> COMPARE WITH PRIOR CHECKPOINT
  -> CONTINUE | CORRECT | REPLAN | ESCALATE | COMPLETE
  -> PERSIST CHECKPOINT
  -> NEXT WAKEUP / NEW CHAT / SAME CHAT
```

## Progress discipline

A cycle must provide an objective-relevant `progress_token` and evidence. Repeating the same token means the method did not create measurable progress.

Default behavior:

| repeated no-progress streak | decision |
|---:|---|
| 0 | `CONTINUE` |
| 1 | `CORRECT` |
| 2-3 | `REPLAN` |
| 4+ | `ESCALATE` |

Progress resets the streak to zero. High/critical risk, missing authority, scope expansion or exhausted autonomy budget also escalate.

## Idempotency

Every cycle is bound to the persistent `state_version`. A stale checkpoint cannot be replayed after the state advances. Operation keys remain deterministic inside the canonical Symbiont runtime.

Therefore repeated wakeups must not repeat a logically completed cycle.

## Repetitive flows

A repetitive flow is valid only when each repetition advances an objective-relevant marker, for example:

```text
batch:1 -> batch:2 -> batch:3
validated_items:10 -> 20 -> 30
remaining_gaps:7 -> 5 -> 2 -> 0
```

Repeating `batch:1 -> batch:1 -> batch:1` is not treated as persistence; it is treated as stagnation and forces correction/replanning/escalation.

## ChatGPT automation boundary

ChatGPT automation may wake the objective loop periodically. It must:

1. resolve the current governed objective/workstream;
2. load the latest checkpoint;
3. perform only the next bounded safe cycle;
4. record evidence/progress;
5. persist the next checkpoint;
6. stop notifying when there is no material change;
7. escalate when the loop requires authority or a root-objective change.

Automation may adapt operational method, priority, decomposition and next action within approved scope. It may not autonomously change ELO purpose, identity, governance boundaries, human-approved strategic target or action authority.

## Test acceptance criteria

The implementation is accepted only if tests prove:

- checkpoint survives closing and reopening the persistent store;
- no-progress streak survives restart;
- stagnation transitions through correction/replanning and eventually escalation;
- objective-relevant progress resets stagnation;
- repetitive flow reaches completion;
- stale checkpoint replay is blocked;
- two workstreams under the same objective remain isolated;
- a multi-cycle flow can restart the process after every cycle and still reach completion.
