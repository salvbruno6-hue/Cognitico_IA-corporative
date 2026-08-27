# ELO Virtual Lab — Audit of Test Cycles and Check-in

## Purpose

Maintain a durable audit trail for cognitive, integration and capability test cycles. This record distinguishes implementation from verified execution evidence.

## Cycle protocol

```text
ISSUE
  -> SCOPE
  -> IMPLEMENTATION
  -> VIRTUAL LAB
  -> CI EXECUTION
  -> EVIDENCE
  -> AUDIT
  -> DECISION
  -> CHECK-IN
  -> MERGE
```

## Check-in states

- `PLANNED`: scope defined, no execution yet.
- `IMPLEMENTED`: tests/code exist, execution evidence pending.
- `PASS`: workflow execution produced reproducible evidence for the defined scope.
- `BLOCKED`: evidence or a required dependency is missing.
- `REJECTED`: behavior violates an architectural or safety gate.
- `MERGED`: validated change incorporated into the canonical branch.

## Mandatory evidence

Each completed cycle records: issue/PR, commit, test scope, environment, workflow run, job result, relevant artifacts/logs, failures, remediation, and final decision.

## Current baseline evidence

| Cycle | Scope | Evidence | State |
|---|---|---|---|
| #304 / #315 | Adaptive performance evidence, tenant/context provenance | GitHub Actions run `33040743770` | PASS / MERGED |
| #316 | Baseline + canonical boundary tests | GitHub Actions run `33040743770` | PASS / PR cycle |
| #317 | Cognitive budget/cross-source scenarios | Commit `fd69c6ad918857109bf50549f1c8fa9a09e17345` | IMPLEMENTED; execution evidence pending |

## Check-in rule

No cycle is marked `PASS` from code inspection alone. A check-in may claim `PASS` only when the workflow has actually executed the intended tests and the evidence is attributable to the tested commit.

## Architectural rule

The audit record belongs to the existing Virtual Lab. Do not create parallel audit engines, duplicate test registries, or tenant-specific audit structures when an existing owner can be extended.

## Next required cycle

Execute the scenario-level battery for #317 and append the workflow run, job results, and failure/remediation evidence before promoting the cycle to `PASS` and considering merge.
