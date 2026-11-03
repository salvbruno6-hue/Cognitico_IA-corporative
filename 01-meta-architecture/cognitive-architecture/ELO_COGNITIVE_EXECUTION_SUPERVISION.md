# ELO Cognitive Execution Supervision

## Purpose

Define execution supervision as a native capability of the ELO Cognitivo. This does not introduce a separate Supervisor, Orchestrator authority, or fourth cognitive core.

The ELO Cognitivo maintains task state, execution context, evidence, planning, specialist coordination, cycle control, continuation, correction, replanning, escalation, promotion decisions, post-merge verification and learning. ELO Core and ELO Forge execute within canonical authority and contracts.

## Canonical principle

> The ELO Cognitivo supervises execution cognitively; ELO Core materializes capabilities; ELO Forge constructs and tests changes; Validation/Governance verifies compliance.

## Questions the Cognitivo must always answer

For every active governed task:

1. Who is doing what?
2. What is the current task state?
3. What is the objective and acceptance criteria?
4. What is the next best action?
5. What evidence already exists?
6. Which specialists have participated?
7. Which specialist or capability is still missing?
8. Which execution/correction cycle is active?
9. Why has the task not finished?
10. Can execution safely continue?
11. Should the task be corrected or replanned?
12. Is an architectural decision required?
13. Should the task be escalated?
14. Is the change eligible for promotion/merge?
15. What was learned after completion?

If these questions cannot be answered from task state and evidence, the task is not fully supervised.

## State model

```text
CREATED → UNDERSTANDING → PLANNING → EXECUTING → VALIDATING
→ SPECIALIST_REVIEW → ELO_ARCHITECTURAL_REVIEW
→ CORRECTING → REVALIDATING → APPROVED → MERGING
→ POST_MERGE_VERIFY → COMPLETED
```

Alternative transitions include `REPLANNING`, `BLOCKED`, `ESCALATED`, `FAILED` and `ROLLED_BACK`. A non-terminal task must always have a next action, retry budget or escalation condition.

## Execution context

The Cognitivo must maintain or reconstruct, as applicable:

```text
task_id, objective, scope, acceptance_criteria, current_state,
current_cycle, max_cycles, actor, active_executor, active_branch,
active_specialists, next_action, last_action, last_result,
evidence_refs, decision_refs, contract_refs, change_refs,
test_refs, risk_refs, open_findings, blocking_findings,
elapsed_time, cost_budget, scope_budget, retry_count,
escalation_reason, learning_refs
```

This is execution state, not a replacement for canonical knowledge or memory.

## Responsibilities

### ELO Cognitivo

Owns objective interpretation, task state, planning, replanning, next-action selection, evidence assessment, specialist coordination, divergence interpretation, continuation, correction, escalation, architectural decisions, promotion/merge recommendation, post-merge verification and learning extraction.

### ELO Core

Provides executable cognitive/runtime capabilities through canonical contracts. It is not an independent task authority.

### ELO Forge

Constructs, experiments, tests and corrects implementation changes on governed branches. Forge reports results and evidence and cannot silently redefine canonical architecture.

### Validation/Governance

Checks tests, security, policy, contracts, evidence and repository protection. It can reject promotion but does not become a competing cognitive authority.

## Next-action policy

The Cognitivo chooses the next action from objective, state, evidence, acceptance criteria, canonical contracts, specialist findings, risk, remaining budget and previous attempts.

Choose the smallest safe action with a credible path to completion. Do not repeat a failed action without a changed hypothesis, expand scope without justification, create duplicate capabilities, change architecture for convenience, continue after exhausted budgets, or hide uncertainty.

## Pre-action coherence and efficiency authority

Before delegating or executing an action, ELO Cognitivo has the authority and responsibility to proactively investigate the existing state and select the most coherent and efficient governed path. This is a native orchestration responsibility, not a new autonomous Orchestrator, Supervisor, Core, or persistence authority.

The pre-action evaluation must, proportionate to scope and risk:

1. Recover task objective, acceptance criteria, current state and relevant prior decisions; inspect canonical GitHub contracts/implementation and applicable structured Supabase evidence.
2. Verify consistency between canonical owner, contract, implementation, consumers, current SO/evidence, specialists and governance; distinguish facts, hypotheses, historical precedents and pending decisions.
3. Check for existing capabilities, duplicated work, conflicting instructions, unnecessary steps and avoidable cost, latency or complexity.
4. Compare credible next actions and prefer the smallest safe, reusable and testable path to the objective: REUSE → CONNECT → RECONCILE → CORRECT → EXTEND → CREATE only when justified.
5. Record material GAPs, decision rationale, provenance, risk, selected executor and required validation; escalate canonical conflicts that cannot be resolved within assigned authority.
6. Execute only within approved scope, permissions, risk and autonomy budgets; persistent/high-impact or irreversible changes remain subject to applicable authorization, required gates and repository protections.

Read-only discovery, comparison, diagnosis, planning and choice of next action are part of the Orchestrator's proactive mandate; they do not require an additional case-by-case approval where already permitted. The permission to investigate or recommend does not, by itself, grant permission to mutate operational or cognitive authority.

Pre-action check outcome must be explicit: COHERENT / GAP / BLOCKED, with a next action or an escalation condition. This check complements — and does not bypass — existing VALIDATING, ELO_ARCHITECTURAL_REVIEW, Evolution Gate, merge and post-merge verification.

## Evidence supervision

Evidence remains traceable and distinguishable as requirement, contract, implementation evidence, test evidence, specialist finding, architectural decision, runtime result, post-merge result and learning. Facts/evidence must not be conflated with inference, hypothesis, recommendation or decision.

## Specialist coordination

For each specialist interaction retain specialist, question, input evidence, finding, confidence, blocking status and required follow-up. Specialists provide evidence and domain judgment; they do not independently redefine canonical ELO architecture.

## Cycle control

Every correction/review cycle must preserve its reason and result. A cycle counter alone is insufficient.

```text
Cycle 1 → implementation defect → Forge correction
Cycle 2 → contract mismatch → implementation adapted
Cycle 3 → architecture passes → approve
```

## Continue / Correct / Replan / Escalate

**CONTINUE:** next action is within scope, policy and budget and evidence supports continuation.

**CORRECT:** objective remains valid and the defect is local or contract-level.

**REPLAN:** current approach is unlikely to satisfy the objective but an alternative remains within scope.

**ESCALATE:** canonical contracts conflict; new security boundary is required; evidence is materially insufficient; authority is unavailable; risk exceeds autonomy level; correction budget is exhausted; an unspecified persistent model is required; repository protection blocks execution; or an irreversible high-impact decision is required.

Escalation must include reason, evidence, alternatives considered and the exact decision required.

## Autonomy budget

Tasks should have explicit or inherited limits for correction cycles, execution time, cost, scope/files, external calls, agent count, retries and destructive operations. The Cognitivo decides whether to continue within those limits and must not silently expand them.

## Merge supervision

`APPROVE_MERGE` requires declared acceptance criteria, required tests, specialist reviews, architectural conformity, security/policy checks, no blocking findings, scope compliance and repository protections. Merge remains a governed repository operation.

## Post-merge supervision

A task is not complete at merge:

```text
MERGE → MAIN STATE → POST-MERGE VALIDATION → EXPECTED BEHAVIOR
→ REGRESSION CHECK → LEARNING → COMPLETED
```

Material regressions trigger correction, rollback or escalation according to policy.

## Learning

For completed tasks extract reusable learning from successful plans, failed hypotheses, corrections, specialist findings, architectural conflicts, repeated failure patterns, effective tool/model choices and validation results. Do not automatically promote every event to durable knowledge.

## Authority boundary

```text
ELO COGNITIVO (decides/supervises)
        ↓
ELO CORE (executes canonical capabilities)
        ↓
ELO FORGE (constructs implementation)
        ↓
VALIDATION/GOVERNANCE (verifies)
        ↓
MAIN (canonical state)
        ↓
ELO COGNITIVO (verifies/learns)
```

The cycle is closed by the Cognitivo. This is supervision, not a separate supervisor component.

## Design constraint

Do not create `ExecutionSupervisor`, `SupervisorCore`, `CognitiveSupervisor` or another parallel authority. These responsibilities belong to the ELO Cognitivo and should use existing context, memory, reasoning, agent and governance mechanisms.

## Maturity criterion

Execution supervision is mature when the ELO can demonstrate that it can accept an objective, establish state and scope, plan, delegate to Core/Forge/agents, track evidence and specialists, detect failure/divergence, correct/replan, decide continuation/escalation, approve governed promotion, verify post-merge outcome, record learning and reach a terminal state without manual intervention at every intermediate step.

The goal is bounded autonomous completion with traceable decisions and safe escalation, not unrestricted autonomy.
