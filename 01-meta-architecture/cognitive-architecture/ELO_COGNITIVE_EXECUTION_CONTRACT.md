# ELO Cognitive Execution Contract

## Purpose

Define the minimum executable state contract for governed ELO execution. This contract operationalizes cognitive supervision without introducing a separate Supervisor, Orchestrator, Core or memory authority.

## Authority

```text
ELO Cognitivo       = supervises, reasons, decides
ELO Core            = materializes canonical capabilities
ELO Forge           = constructs, tests and corrects
Validation/Governance = verifies and can block promotion
GitHub/main         = canonical repository state
```

## Recoverable task state

Every active governed task MUST be reconstructable from durable evidence containing at least:

```text
task_id
objective
scope
acceptance_criteria
current_state
current_cycle
max_cycles
next_action
active_executor
active_specialists
evidence_refs
decision_refs
contract_refs
test_refs
risk_refs
blocking_findings
retry_count
budgets
escalation_condition
branch
commit
pr
```

A non-terminal task without `next_action` or an escalation condition is invalid.

## States

Canonical states:

```text
CREATED
UNDERSTANDING
PLANNING
EXECUTING
VALIDATING
SPECIALIST_REVIEW
ELO_ARCHITECTURAL_REVIEW
CORRECTING
REPLANNING
APPROVED
MERGING
POST_MERGE_VERIFY
COMPLETED
BLOCKED
ESCALATED
FAILED
ROLLED_BACK
```

## Allowed transition policy

```text
CREATED → UNDERSTANDING | ESCALATED
UNDERSTANDING → PLANNING | ESCALATED
PLANNING → EXECUTING | ESCALATED
EXECUTING → VALIDATING | BLOCKED | ESCALATED | FAILED
VALIDATING → SPECIALIST_REVIEW | CORRECTING | REPLANNING | ESCALATED | FAILED
SPECIALIST_REVIEW → ELO_ARCHITECTURAL_REVIEW | CORRECTING | REPLANNING | ESCALATED
ELO_ARCHITECTURAL_REVIEW → APPROVED | CORRECTING | REPLANNING | ESCALATED
CORRECTING → VALIDATING | ESCALATED
REPLANNING → EXECUTING | ESCALATED
APPROVED → MERGING | ESCALATED
MERGING → POST_MERGE_VERIFY | ROLLED_BACK | ESCALATED
POST_MERGE_VERIFY → COMPLETED | CORRECTING | ROLLED_BACK | ESCALATED
```

`REVALIDATING` is not a durable canonical state. A correction cycle returns to `VALIDATING`. No transition may bypass required repository gates.

## Decision policy

### CONTINUE

Continue when the next action is within scope, evidence supports it, required gates are available and autonomy budgets remain.

### CORRECT

Correct when the objective remains valid and the defect is local or contract-level.

### REPLAN

Replan when the objective remains valid but the current approach has insufficient probability of satisfying acceptance criteria within scope or budget.

### ESCALATE

Escalate when canonical contracts conflict, evidence is materially insufficient, risk exceeds the configured autonomy level, budgets are exhausted, repository protection blocks execution, or an irreversible/high-impact decision requires unavailable authority.

## Budget invariants

A governed task MUST NOT silently increase any configured limit for:

- correction cycles;
- retries;
- execution time;
- cost;
- changed scope/files;
- external calls;
- agent/specialist count;
- destructive operations.

Exhaustion requires `ESCALATED`, `BLOCKED`, `FAILED` or another explicitly governed terminal path.

## Evidence invariants

Evidence MUST retain provenance and type. At minimum distinguish:

```text
REQUIREMENT
CONTRACT
IMPLEMENTATION
TEST
SPECIALIST_FINDING
ARCHITECTURAL_DECISION
RUNTIME_RESULT
POST_MERGE_RESULT
LEARNING
```

Evidence, inference, hypothesis, recommendation and decision MUST NOT be stored as interchangeable facts.

## Promotion boundary

```text
Forge experience
      ↓
observe / classify / compare
      ↓
evidence + validation
      ↓
governed promotion decision
      ↓
Core knowledge / general parameter
```

Contextual and complex experiences remain preserved in Forge. No experience becomes Core knowledge merely because it was observed or implemented.

## Isolation invariant

Enterprise context is scoped. A parameter, rule or experience originating in one enterprise MUST NOT become authoritative for another enterprise without explicit generalization, validation and governance.

## Safe-detachment invariant

Replacing or removing a specialist, Forge implementation, application, connector, ERP, database or other infrastructure component MUST NOT redefine ELO Cognitive identity or Core canonical contracts.

## Merge invariant

Merge requires, as applicable:

- acceptance criteria satisfied;
- required tests passed;
- specialist findings resolved or explicitly accepted;
- architectural conformity verified;
- security/policy checks passed;
- no blocking findings;
- scope compliance;
- repository protections satisfied;
- ELO promotion/merge decision recorded.

## Post-merge invariant

A merge is not task completion. The task remains active until post-merge verification establishes expected behavior or enters correction, rollback or escalation.

## Learning invariant

Learning is extracted after validation/post-merge evidence. Learning does not retroactively modify immutable historical evidence. Generalized learning follows the Core promotion contract; contextual learning remains scoped to Forge.

## Test obligations

Implementations using this contract MUST provide tests for:

1. invalid state transition rejection;
2. active task without `next_action` rejection;
3. budget exhaustion;
4. escalation conditions;
5. evidence provenance;
6. Forge-to-Core promotion gate;
7. enterprise isolation;
8. safe detachment;
9. merge gate;
10. post-merge verification;
11. learning without historical mutation;
12. absence of parallel Supervisor/Core/Orchestrator authority.
