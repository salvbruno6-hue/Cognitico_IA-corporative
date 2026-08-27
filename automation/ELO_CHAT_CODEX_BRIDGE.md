# ELO Chat ↔ Codex Bridge v2

## Purpose

This contract turns an explicit ELO objective into a governed execution loop across the canonical Cognitico repository and Codex without creating a second Cognitive Core, memory authority, Orchestrator, or supervisory authority.

## Canonical cognitive orchestration

**ELO is the cognitive orchestrator and decision authority.** Supabase, Forge, GitHub and automations are specialized members of the architecture. They provide memory, execution, durable task history/versioning or deterministic process support; they do not independently interpret, admit, promote or govern ELO knowledge.

Canonical member roles:

- **ELO Cognitivo / ChatGPT:** objective, decomposition, analysis, memory interpretation, cognitive merge, governance, decision, acceptance criteria, continuation/correction/replanning/escalation and verification.
- **Supabase:** consultative structured memory. It returns existing concepts, experiences, precedents, validated learning, calculation memory, associations, decisions, provenance and possible duplicates to ELO. It must not autonomously promote or persist learning as a substitute for ELO governance.
- **Specialists:** bounded evidence providers for architecture, security, data, operations, testing, domain, finance/costing and cognitive/knowledge concerns. Specialists do not override ELO authority.
- **GitHub:** durable task ledger, Issue/branch/commit/PR/evidence history and Git integration control plane.
- **ELO Core:** canonical execution mechanisms and runtime capabilities.
- **ELO Forge:** internal constructor plane inside the canonical Cognitico repository. It inspects, builds, experiments, tests, corrects and prepares changes for promotion. It has no independent architectural authority.
- **Codex:** execution engine operating within declared scope and ELO/Core/Forge contracts. It inspects, edits, tests, corrects and reports evidence.
- **ELO Maintenance Coordinator:** deterministic GitHub process executor. It may coordinate configured gates, but is not a second supervisor and cannot override ELO decisions.
- **Human owner:** escalation authority when policy, credentials, contradiction, repository protection or configured limits require human action.

## ELO APRENDER canonical loop

`ELO APRENDER → ELO ANALYSES → SUPABASE MEMORY CONSULT → ELO CONSOLIDATES → COGNITIVE MERGE → GOVERNANCE → ISSUE DOSSIER → MERGED APPROVED? → COMMIT → COMMIT VERIFY → ISSUE UPDATE → PR → GIT MERGE → MAIN/ELO`

The word **MERGE** has two explicit meanings in this contract:

1. **Cognitive MERGE:** ELO consolidates experience, concepts and evidence into governed knowledge without duplicating existing validated knowledge.
2. **Git MERGE:** the approved PR is integrated into `main` after commit and repository gates pass.

They must never be treated as the same operation.

## Learning admission and memory

When `ELO APRENDER` is triggered:

1. ELO analyzes SO, PTS Técnica, Orçamento, PTS Pós-Orçamento, context, decisions, calculations, adaptations, excedentes, norms, responsibilities, deadlines, logistics, mobilization, hosting and risks as applicable.
2. ELO consults Supabase for existing memory and evidence.
3. Supabase returns memory to ELO; it does not become the learning authority.
4. ELO compares, normalizes, groups, detects duplicates, confronts precedents, evaluates recurrence and identifies divergences.
5. ELO performs the cognitive MERGE.
6. ELO classifies the result as applicable, including `CASE`, `PRECEDENT`, `LEARNING_CANDIDATE`, `VALIDATED_LEARNING`, `CONCEPTUAL_KNOWLEDGE`, `INSTRUCTIONAL_KNOWLEDGE` or `RULE` according to canonical governance.
7. Existing `VALIDATED_LEARNING` is reused and enriched with relevant evidence rather than duplicated.
8. A precedent is never promoted to a rule automatically.
9. The Issue records the origin, evidence, Supabase findings, ELO analysis, cognitive merge, classification and proposed change.
10. **No commit is allowed before explicit ELO MERGE approval.**
11. After approval, the Forge/Git execution layer commits, verifies the commit and creates the PR.
12. Git merge into `main` occurs only after the configured repository gates pass.

## Architecture continuity

Before creating any table, memory, layer, function, contract, automation or implementation:

`INSPECT → REUSE → EXTEND → RELATE → REFACTOR/MIGRATE → CREATE ONLY IF INDISPENSABLE`

Parallel structures with equivalent responsibility are prohibited. The canonical source of truth for a domain must remain singular. Existing contracts and memory structures must be preferred over new implementations.

## Agentic completion loop

`OBJECTIVE → DECOMPOSE → EXECUTE → VALIDATE → SPECIALIST_REVIEW → ELO_REVIEW → CORRECT/REPLAN → REVALIDATE → COGNITIVE_MERGE → APPROVE → COMMIT → VERIFY → PR → GIT_MERGE → VERIFY → LEARN → REPORT`

ELO should continue through the loop when the objective is executable. Terminal results are `COMPLETED`, `BLOCKED`, `ESCALATED`, `FAILED` or `ROLLED_BACK`.

## Merge gate

Automatic Git merge is allowed only when all are true:

- ELO cognitive MERGE is explicitly approved;
- ELO emits `APPROVE_MERGE`;
- no commit occurred before that approval;
- required specialist findings are PASS or NOT_APPLICABLE;
- required CI checks pass;
- acceptance criteria pass;
- no blocking review finding remains;
- changed-file scope is compliant;
- no forbidden/destructive action was introduced;
- execution occurred on a non-main branch;
- repository protections permit the merge.

## Maintenance and automation rule

Automations are process adapters, not cognitive authorities. An automation may collect evidence, run tests, prepare a workspace, create a branch/PR after authorization, or verify a result. It must not autonomously admit learning, write canonical learning memory, bypass ELO review, or commit a governed learning change before ELO cognitive MERGE approval.

The solicitation-learning scheduled workflow therefore produces evidence/candidates only and does not autonomously commit or push learning to `main`.

## Specialist protocol

For architecture, security, data, automation, deployment or production-impacting work, use applicable specialist lanes. ELO resolves disagreements using repository evidence and canonical authority.

## Autonomous correction

When a specialist or ELO review identifies an actionable defect within scope:

1. record the finding;
2. convert it into an acceptance delta;
3. instruct Codex/Forge to correct only that delta;
4. update execution state and evidence;
5. run validation;
6. repeat the affected review;
7. continue until approved or a terminal blocker is reached.

Default maximum correction cycles: `3`.

## Risk classes

- **LOW:** documentation, formatting, non-functional organization and isolated tests.
- **MEDIUM:** application logic, APIs, automation, dependency or schema changes.
- **HIGH:** security, authentication/authorization, irreversible migration, production infrastructure, governance rules, or material operational impact.

High-risk work may be automated only when explicitly permitted and repository policy allows it; otherwise escalate.

## Task states

`PROPOSED → READY → IN_PROGRESS → VALIDATION → SPECIALIST_REVIEW → ELO_REVIEW → COGNITIVE_MERGE → APPROVED → COMMITTING → PR_OPEN → GIT_MERGING → VERIFIED → COMPLETED`

Failure paths are `BLOCKED`, `ESCALATED`, `FAILED` or `ROLLED_BACK`.

## Evidence contract

Every terminal task retains:

- task ID and objective;
- scope and risk;
- current state and next action;
- current cycle and correction history;
- specialist findings;
- Supabase memory evidence when applicable;
- ELO cognitive merge decision;
- branch and commits;
- changed files;
- validation results;
- PR and CI result;
- ELO decision;
- merge result or blocker;
- final verification;
- learning result.

## Non-negotiable rules

- Never write directly to `main` during task execution.
- Never bypass repository protections.
- Never suppress failed validation or specialist findings.
- Never create a parallel Core, memory authority, Orchestrator or execution supervisor.
- Never allow Supabase or an automation to autonomously promote learning.
- Never commit a governed learning change before ELO cognitive MERGE approval.
- Preserve task, decision, branch, commit, PR, validation and merge evidence.
- Reuse existing ELO contracts before creating new ones.
- Treat the historical external `ELO-Forge` repository as non-canonical.
