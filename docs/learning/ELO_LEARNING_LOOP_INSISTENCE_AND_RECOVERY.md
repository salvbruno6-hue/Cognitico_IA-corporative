# ELO — Learning Loop, Insistence and Recovery

**Status:** Learning baseline / governed design
**Scope:** Cognitive-to-operational loop, execution recovery, evidence feedback and learning
**Authority:** Existing ELO Core, DecisionRecord, OutcomeFeedback and Evolution Gate

## 1. Purpose

Define how ELO should continue a task when the first attempt does not close the objective, without turning persistence into uncontrolled repetition.

The loop must distinguish:

- persistence with the same valid method;
- recovery with a different method;
- re-planning after evidence of insufficient progress;
- escalation when authority, evidence or governance is missing;
- termination when continued attempts are not justified.

Persistence is therefore **governed insistence**, not blind retry.

## 2. Current canonical architecture found in the repository

The existing `CoreLoopEngine` is explicitly a coordinator for **Context → Evidence → Diagnosis → Handoff** and has `can_execute = False`. It does not execute enterprise actions or mutate canonical evidence.

`DecisionRecord` stores the decision, rationale, evidence linkage, impact and optional outcome linkage. `OutcomeFeedback` stores expected versus observed outcome, assessment and evidence linkage.

The existing agentic layer uses `IntentSpec` as the semantic input and `KnowledgeOrchestrator` to plan bounded knowledge requirements and retrieve/curate governed knowledge. The repository does **not** establish an existing canonical mapping from `IntentSpec`/diagnosis directly to the eight operational conditions used by the conditional pointer laboratory.

**Therefore this document does not create or silently assign that missing mapping.** The capability-condition relationship remains governed by the existing pointer matrix until an authoritative Core contract is established.

## 3. Canonical closed loop

```text
REQUEST
  ↓
INTENT / CONTEXT
  ↓
EVIDENCE RESOLUTION
  ↓
DIAGNOSIS
  ↓
DECISION / HANDOFF
  ↓
GOVERNED CAPABILITY RESOLUTION
  ↓
OPERATIONAL EXECUTION
  ↓
OBSERVED OUTCOME
  ↓
OUTCOME FEEDBACK
  ↓
LEARNING ASSESSMENT
  ↓
EVOLUTION GATE (when canonical change is proposed)
  ↺
NEXT ATTEMPT / CLOSE
```

The loop must preserve the identity of the original task, decision, evidence, attempt and outcome.

## 4. Attempt state machine

Recommended states:

- `READY` — enough context/evidence exists to begin.
- `ATTEMPTING` — an authorized operational attempt is in progress.
- `PROGRESS` — observable progress occurred.
- `SUCCESS` — objective closed and evidence supports closure.
- `PARTIAL` — useful progress occurred but objective remains open.
- `NO_PROGRESS` — attempt produced no meaningful progress.
- `BLOCKED` — evidence, authority, dependency or governance prevents continuation.
- `REPLAN_REQUIRED` — current method should not simply be repeated.
- `ESCALATE` — human/superior authority is required.
- `STOPPED` — continuation is not justified or permitted.

`NO_PROGRESS` must not automatically mean failure of the objective. It means failure of the current attempt to advance it.

## 5. Governed insistence variants

### Variant I — Same-method retry

Use only when:

- the method remains valid;
- no contradiction appeared;
- the failure is transient or operational;
- the retry has a bounded attempt count;
- the previous evidence does not invalidate the method.

```text
attempt → no_progress → validate method → retry
```

Do not retry indefinitely.

### Variant II — Evidence refresh

Use when the method is valid but the information basis may be stale or incomplete.

```text
attempt → insufficient evidence → refresh authorized sources → reassess → attempt
```

The refreshed evidence must remain traceable.

### Variant III — Replan

Use when repeated attempts show that the current path is not producing progress.

```text
attempt → NO_PROGRESS → fingerprint problem → replan → new bounded attempt
```

A replan changes the method/path, not the canonical truth.

### Variant IV — Alternate governed path

Use when the first capability/path is unavailable or incompatible, but another already-authorized path exists.

```text
attempt → blocked/unavailable → resolve existing alternative → attempt
```

No new capability is invented during recovery.

### Variant V — Escalation

Use when:

- evidence conflicts;
- authority is insufficient;
- a required relation is ambiguous;
- governance approval is required;
- repeated replanning cannot close the issue.

```text
attempt/replan → unresolved governance or ambiguity → HANDOFF → human decision
```

### Variant VI — Controlled stop

Use when continuation would become repetitive, unsafe, unjustified or outside authority.

```text
attempt → no_progress / blocked → stop condition → STOPPED
```

The stop itself must be explainable through evidence and state.

## 6. Problem fingerprint

Each non-successful attempt should produce a compact fingerprint containing:

- task/request identity;
- intent identity;
- current method/capability identity, when already resolved by Core;
- relevant evidence IDs;
- observed result;
- failure/block reason;
- attempt number;
- previous attempt relation;
- whether the method changed;
- whether evidence changed;
- whether authority/governance changed.

The fingerprint exists to prevent ELO from confusing repeated symptoms with new problems.

## 7. Insistence policy

The default progression is:

```text
1. Validate the current state.
2. Retry only if the same method remains justified.
3. If evidence is the problem, refresh evidence.
4. If the method is the problem, replan.
5. If an existing alternative is available, use it.
6. If authority/ambiguity remains unresolved, hand off.
7. If continuation is no longer justified, stop.
```

A successful attempt closes the operational loop. A failed attempt feeds the recovery loop.

## 8. Anti-loop controls

ELO must detect:

- identical method + identical evidence + identical result;
- repeated `NO_PROGRESS` without method or evidence change;
- oscillation between two methods without new evidence;
- increasing attempts without increasing information or progress;
- unresolved ambiguity being repeatedly re-presented as a new task.

These conditions should trigger `REPLAN_REQUIRED`, `ESCALATE` or `STOPPED`, according to the governing evidence.

## 9. Learning rule

ELO does **not** learn merely because an attempt happened.

Learning requires an outcome relationship:

```text
DecisionRecord → OutcomeFeedback → assessment → learning candidate
```

A useful learning record should preserve:

- what was decided;
- why it was decided;
- which evidence supported it;
- what actually happened;
- what differed from expectation;
- which method was used;
- which recovery variant was used, if any;
- whether the lesson concerns the problem or the method;
- whether the lesson is merely contextual or proposes canonical evolution.

Canonical evolution remains subject to the existing Evolution Gate.

## 10. Problem Learning × Method Learning

### Problem Learning

Answers: **what kind of problem was encountered?**

Examples of signals:

- missing evidence;
- conflicting evidence;
- dependency unavailable;
- governance block;
- invalid requirement;
- unresolved context.

### Method Learning

Answers: **which approach worked or failed under those conditions?**

Examples:

- same-method retry succeeded;
- evidence refresh resolved the issue;
- replan closed the task;
- alternate governed path succeeded;
- repeated method produced no progress.

These two learning streams must remain distinguishable so ELO does not convert a temporary execution failure into a false statement about the underlying problem.

## 11. Promotion boundary

Operational success is evidence of successful execution, not automatic canonical learning.

The progression is:

```text
candidate
  ↓
validated
  ↓
active operational
  ↓
outcome observed
  ↓
learning candidate
  ↓
Evolution Gate
  ↓
canonical evolution (only if approved)
```

No self-promotion and no silent canonical mutation.

## 12. What this document intentionally does not define

This learning baseline does **not** define a new authoritative `IntentSpec → condition → capability_id` classifier.

Repository inspection found the semantic `IntentSpec`, the Core diagnostic loop, and the deterministic conditional-pointer matrix, but no existing canonical contract proving that mapping. Creating such a mapping would therefore be an architectural decision rather than a neutral implementation detail.

Until that relation is arbitrated, the operational loop must consume only an already-governed Core capability decision.

## 13. Operational invariant

> ELO insists on the objective, not on the method.

If the objective remains valid, ELO may continue through bounded recovery variants. If the method stops producing progress, ELO changes method or escalates. If evidence or authority is insufficient, ELO stops at the appropriate governance boundary.

## 14. Learning memory statement

This document is the repository-level learning baseline for governed persistence, recovery and outcome learning. Future implementations should treat it as a reference for loop behavior while preserving the existing Core, evidence, decision, outcome and Evolution Gate authorities.
