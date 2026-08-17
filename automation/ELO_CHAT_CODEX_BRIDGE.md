# ELO Chat ↔ Codex Bridge v1

## Purpose

This contract turns an explicit ELO objective into a governed execution loop across the canonical Cognitico repository and Codex without creating a second Cognitive Core, memory authority, Orchestrator, or supervisory authority.

## Roles

- **ELO Cognitivo / ChatGPT:** objective, decomposition, task state, execution context, architectural authority, specialist questions, next-action selection, acceptance criteria, continuation/correction/replanning/escalation decisions, risk decision and terminal decision.
- **Specialists:** bounded evidence providers for architecture, security, data, operations, testing and domain concerns. Specialists do not override ELO authority.
- **GitHub:** durable task ledger, branch/commit/PR/evidence history and merge control plane.
- **ELO Core:** canonical execution mechanisms and runtime capabilities.
- **ELO Forge:** internal constructor plane inside the canonical Cognitico repository. It inspects, builds, experiments, tests, corrects and prepares changes for promotion. It has no independent architectural authority.
- **Codex:** execution engine operating within the declared task scope and the ELO/Core/Forge contracts. It inspects, edits, tests, corrects and reports evidence.
- **Human owner:** escalation authority when policy, credentials, contradiction, repository protection or other configured limits require human action.

## Agentic completion loop

`OBJECTIVE → DECOMPOSE → EXECUTE → VALIDATE → SPECIALIST_REVIEW → ELO_REVIEW → CORRECT/REPLAN → REVALIDATE → APPROVE → MERGE → VERIFY → LEARN → REPORT`

ELO should continue through the loop when the objective is executable. It should return to the user with a terminal result: `COMPLETED`, `BLOCKED`, `ESCALATED`, `FAILED`, or `ROLLED_BACK`.

## Cognitive execution supervision

The ELO Cognitivo is the native supervisor of the task. It must be able to determine:

- who is doing what;
- current state;
- objective and acceptance criteria;
- next best action;
- evidence already available;
- specialists involved and missing;
- current cycle;
- why the task has not finished;
- whether execution may safely continue;
- whether to correct, replan or escalate;
- whether promotion/merge is justified.

Do not create an `ExecutionSupervisor`, `SupervisorCore`, `CognitiveSupervisor` or equivalent parallel authority.

## Specialist protocol

For architecture, security, data, automation, deployment or production-impacting work, use applicable specialist lanes:

1. Architecture — boundaries, coupling, contracts and compatibility.
2. Security — secrets, authorization, supply chain and attack surface.
3. Data — schemas, migrations, provenance and tenant isolation.
4. Operations — deployment, reliability, rollback and observability.
5. Testing — acceptance coverage, regression and evidence quality.
6. Domain — business/process correctness when applicable.

ELO resolves disagreements using repository evidence and canonical authority.

## Autonomous correction

When a specialist or ELO review identifies an actionable defect within scope:

1. record the finding;
2. convert it into an acceptance delta;
3. instruct Codex/Forge to correct only that delta;
4. update execution state and evidence;
5. run validation;
6. repeat the affected review;
7. continue until approved or a terminal blocker is reached.

Default maximum correction cycles: `3`, unless the task explicitly defines a lower bound or another governed limit.

## Merge gate

Automatic merge is allowed only when all are true:

- task state is `APPROVED`;
- ELO emits `APPROVE_MERGE`;
- required specialist findings are PASS or NOT_APPLICABLE;
- required CI checks pass;
- acceptance criteria pass;
- no blocking review finding remains;
- changed-file scope is compliant;
- no forbidden/destructive action was introduced;
- execution occurred on a non-main branch;
- repository protections permit the merge.

Never bypass branch protection or required checks.

## Risk classes

- **LOW:** documentation, formatting, non-functional organization and isolated tests.
- **MEDIUM:** application logic, APIs, automation, dependency or schema changes.
- **HIGH:** security, authentication/authorization, irreversible migration, production infrastructure, governance rules, or material operational impact.

High-risk work may be automated only when the task explicitly permits it and repository policy does not require human approval. Otherwise the terminal state is `ESCALATED`.

## Task states

`PROPOSED → READY → IN_PROGRESS → VALIDATION → SPECIALIST_REVIEW → ELO_REVIEW → CORRECTING/REPLANNING → APPROVED → MERGING → VERIFIED → COMPLETED`

Failure paths are `BLOCKED`, `ESCALATED`, `FAILED`, or `ROLLED_BACK`.

## Non-negotiable rules

- Never write directly to `main` during task execution.
- Never bypass repository protections.
- Never silently expand scope.
- Never suppress failed validation or specialist findings.
- Preserve task, decision, branch, commit, PR, validation and merge evidence.
- Reuse existing ELO contracts before creating new ones.
- Do not create a parallel Core, memory authority, Orchestrator or execution supervisor.
- Treat the historical external `ELO-Forge` repository as non-canonical. It may be inspected for evidence or historical assets, but the active Forge constructor is inside `Cognitico_IA-corporative`.
- Do not promote historical Forge SQL, migrations, runtime configuration, dashboards or implementation artifacts merely because they exist. Promote only reconciled output that adds value and conforms to canonical ELO contracts.

## Evidence contract

Every terminal task retains:

- task ID and objective;
- scope and risk;
- current state and next action;
- current cycle and correction history;
- specialist findings;
- evidence references;
- branch and commits;
- changed files;
- validation results;
- PR and CI result;
- ELO decision;
- merge result or blocker;
- final verification;
- learning result.

## Forge relationship

The active Forge is an internal constructor plane of the canonical Cognitico repository. Its workflow is:

`TASK → forge/<task> → BUILD → TEST → CORRECT → VALIDATE → PR → ELO REVIEW → MERGE`

The historical external `ELO-Forge` repository is not a canonical runtime or governance authority. Its contents may be used as evidence and candidates through:

`OBSERVE → CLASSIFY → COMPARE → EVIDENCE → PROMOTE/REUSE/EXTEND/REJECT/ROADMAP → TRACE`

No historical Forge artifact becomes canonical merely because it exists in the external repository.
