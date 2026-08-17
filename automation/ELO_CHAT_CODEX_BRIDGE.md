# ELO Chat ↔ Codex Bridge v1

## Purpose

This contract turns an explicit ELO objective into a governed execution loop across GitHub and Codex without creating a second Cognitive Core, memory authority, or Orchestrator.

## Roles

- **ELO / ChatGPT:** objective, decomposition, architectural authority, specialist questions, acceptance criteria, risk decision, terminal decision.
- **Specialists:** bounded evidence providers for architecture, security, data, operations, testing, and domain concerns. Specialists do not override ELO authority.
- **GitHub:** durable task ledger, branch/commit/PR/evidence history and merge control plane.
- **Codex:** execution engine. It inspects, edits, tests, corrects and reports evidence within the declared task scope.
- **Human owner:** escalation authority when policy, credentials, contradiction, or repository protection requires human action.

## Agentic completion loop

`OBJECTIVE → DECOMPOSE → EXECUTE → VALIDATE → SPECIALIST_REVIEW → ELO_REVIEW → CORRECT → REVALIDATE → APPROVE → MERGE → VERIFY → REPORT`

ELO should continue through the loop when the objective is executable. It must return to the user only with a terminal result: `COMPLETED`, `BLOCKED`, `ESCALATED`, or `FAILED`.

## Specialist protocol

For architecture, security, data, automation, deployment, or production-impacting work, use the applicable specialist lanes:

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
3. instruct Codex to correct only that delta;
4. run validation;
5. repeat the affected review;
6. continue until approved or a terminal blocker is reached.

Default maximum correction cycles: `3`.

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

`PROPOSED → READY → IN_PROGRESS → VALIDATION → SPECIALIST_REVIEW → ELO_REVIEW → CORRECTING → APPROVED → MERGING → VERIFIED → COMPLETED`

Failure paths are `BLOCKED`, `ESCALATED`, or `FAILED`.

## Non-negotiable rules

- Never write directly to `main` during task execution.
- Never bypass repository protections.
- Never silently expand scope.
- Never suppress failed validation or specialist findings.
- Preserve task, decision, branch, commit, PR, validation and merge evidence.
- Reuse existing ELO contracts before creating new ones.
- Do not create a parallel Core, memory authority, or Orchestrator.
- Treat Forge as an external knowledge source, not a canonical runtime authority.
- Promote Forge material selectively through the existing ELO knowledge-governance path.

## Evidence contract

Every terminal task retains:

- task ID and objective;
- scope and risk;
- specialist findings;
- corrections;
- branch and commits;
- changed files;
- validation results;
- PR and CI result;
- ELO decision;
- merge result or blocker;
- final verification.

## Forge relationship

Forge is a source for candidate knowledge, working assets and historical experimentation. The Cognitico repository remains the canonical operational source. Forge content enters the Cognitico only through `OBSERVE → CLASSIFY → COMPARE → EVIDENCE → PROMOTE/REUSE/EXTEND/REJECT/ROADMAP → TRACE` and must retain provenance. No Forge artifact becomes canonical merely because it exists in Forge.
