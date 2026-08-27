# ELO Virtual Lab — Audit of Test Cycles and Check-in

## Purpose

Maintain the durable audit trail for cognitive, integration and capability cycles. A check-in is a controlled state transition, not a commit counter. Implementation, execution evidence, audit decision and merge remain distinct.

## Cadenced cycle

```text
T0  ISSUE / INTENT
 ↓
T1  SCOPE + OWNER + NON-DUPLICITY
 ↓
T2  IMPLEMENTATION
 ↓
T3  VIRTUAL LAB TEST
 ↓
T4  CI EXECUTION ON EXACT COMMIT
 ↓
T5  EVIDENCE CAPTURE
 ↓
T6  AUDIT / REGRESSION / ARCHITECTURE
 ↓
T7  DECISION CHECK-IN
 ↓
T8  PR REVIEW
 ↓
T9  MERGE
 ↓
T10 POST-MERGE REGRESSION + BASELINE UPDATE
```

The cycle advances one gate at a time. A later gate cannot be used as evidence for an earlier missing gate.

## Check-in contract

Each check-in records:

- cycle ID and issue/PR;
- exact commit SHA under test;
- semantic owner and impacted capability;
- test scope and laboratory scenario;
- workflow run/job;
- executed test result;
- artifacts/logs or explicit absence;
- failures and remediation;
- regression result;
- architectural decision;
- next state.

## States

- `PLANNED`: intent and scope defined.
- `SCOPED`: owner and non-duplication gate passed.
- `IMPLEMENTED`: code/tests exist; execution evidence pending.
- `LAB_PASS`: virtual scenario behavior passed.
- `CI_PASS`: intended workflow executed against the exact commit and passed.
- `AUDITED`: architecture, regression, provenance and tenant boundaries reviewed.
- `CHECKED_IN`: cycle evidence is recorded and accepted for PR progression.
- `MERGED`: validated change incorporated into canonical branch.
- `POST_MERGE_PASS`: canonical branch regression passed.
- `BLOCKED`: required evidence/dependency is missing.
- `REJECTED`: behavior violates a required gate.

## Promotion rules

```text
PLANNED
  -> SCOPED
  -> IMPLEMENTED
  -> LAB_PASS
  -> CI_PASS
  -> AUDITED
  -> CHECKED_IN
  -> MERGED
  -> POST_MERGE_PASS
```

A cycle cannot skip `LAB_PASS`, `CI_PASS`, or `AUDITED` when those gates are in scope. `PASS` is never inferred from code review alone.

## Cadence policy

- Every implementation cycle gets one check-in record.
- Every check-in is tied to one exact commit.
- Every material change after CI invalidates the prior `CI_PASS` for the changed commit and requires a new execution.
- Repeated tests without code changes may reuse the same commit evidence only when the workflow/run identity and scope remain identical.
- A merge creates a new post-merge verification point; PR evidence does not automatically become post-merge evidence.
- Failed cycles remain recorded; remediation creates a new state transition rather than erasing history.

## Current cycle ledger

| Cycle | Scope | Commit | State | Evidence |
|---|---|---|---|---|
| #304 / #315 | Adaptive performance evidence, tenant/context provenance | merged history | POST_MERGE_PASS | GitHub Actions run `33040743770` |
| #316 | Baseline + canonical boundary tests | prior tested commit | CI_PASS / PR cycle | GitHub Actions run `33040743770` |
| #317 | Cognitive budget/cross-source scenarios | `fd69c6ad918857109bf50549f1c8fa9a09e17345` | IMPLEMENTED / BLOCKED at CI evidence | No check-runs for exact commit |

## Check-in for #317

The scenario battery is implemented and includes budget calculation, source crossing, provenance preservation, UNKNOWN handling, tenant isolation and non-fabrication. The exact commit has no associated check-runs, so the cycle remains `BLOCKED` at `CI_PASS` and must not be promoted or merged on the strength of the earlier baseline run.

## Architectural rule

The audit record belongs to the existing Virtual Lab. Do not create parallel audit engines, duplicate test registries, or tenant-specific audit structures when an existing owner can be extended.

## Definition of done

A cycle is complete only when the exact tested commit has reproducible laboratory/CI evidence, the result has been audited, the check-in is recorded, the PR is reviewed/merged, and post-merge regression establishes the new canonical baseline.