# ELO — AI Agent Operating Rules

## 1. Purpose

This file is the operational contract for AI coding agents, reviewers, assistants, and automation working inside the ELO repository.

The repository is the official operational source of the ELO ecosystem. The current README identifies the repository as the base for the ELO Enterprise Integration Platform and identifies `src/elo/` as the implementation core.

These rules complement, but do not replace, the canonical architecture, ADRs, governance documents, contracts, tests, and repository-specific instructions.

## 2. Non-negotiable operating principles

1. Inspect before editing.
2. Reuse existing contracts before creating new contracts.
3. Never create a second implementation of an existing ELO capability merely because the existing implementation is incomplete.
4. Do not use folder names as proof of architectural authority; use the authority map and canonical documents.
5. Do not promote roadmap concepts to implemented capabilities without an explicit implementation task.
6. Do not silently change normative architecture to make code easier to write.
7. Keep tenant, domain, principal, policy, provenance, and correlation boundaries explicit where applicable.
8. Do not use `department` as the primary security boundary.
9. Do not expose internal exceptions, secrets, private data, or unnecessary operational details.
10. Prefer small, testable changes over broad refactors.
11. Every executable change must have an evidence path: requirement → contract → implementation → test.
12. Do not bypass branch protection, required checks, or repository governance.
13. Automatic merge is permitted only through the governed ELO agent loop and only when every declared merge gate passes.
14. The Forge constructor plane is an execution/building area inside the canonical repository; it is not a second Core, second governance authority, or shadow main.
15. Forge branches must build against the canonical `main`, compare results with canonical contracts, and promote changes only through the governed PR path.
16. Operational SQL, migrations, runtime configuration, generated artifacts, dashboards, and other implementation artifacts are evidence sources during Forge review, not canonical architecture by default.
17. **ELO is the canonical cognitive orchestrator. Supabase, Forge, GitHub and automations are specialized members of the architecture and must not autonomously assume ELO cognitive authority.**
18. **For `ELO APRENDER`, Supabase is consultative memory: it supplies existing knowledge/evidence to ELO; it does not independently admit, promote or persist learning.**
19. **No governed learning commit may occur before explicit ELO cognitive MERGE approval.**
20. **Architecture evolution must follow INSPECT → REUSE → EXTEND → RELATE → REFACTOR/MIGRATE → CREATE ONLY IF INDISPENSABLE.**

## 3. Required inspection sequence

Before any implementation task:

1. Read this file.
2. Read `ELO_REPOSITORY_NAVIGATION_RULES.md`.
3. Read `ELO_ARTIFACT_METADATA_STANDARD.md` when adding or relocating artifacts.
4. Inspect the target directory.
5. Search for an existing concept, contract, class, schema, test, ADR, or document.
6. Identify the canonical owner of the concept.
7. Check the current implementation state and tests.
8. Check relevant ADRs and governance constraints.
9. Define the smallest change that satisfies the task.

## 4. Change classification

Every proposed change must be classified as one of:

- DOCUMENTATION
- NORMATIVE ARCHITECTURE
- CONTRACT
- IMPLEMENTATION
- TEST
- GOVERNANCE
- DATA/MIGRATION
- OBSERVABILITY
- ROADMAP
- EXPERIMENTAL

Do not mix these classifications in one change unless the task explicitly requires it.

## 5. ELO execution gates

The implementation sequence is governed by explicit gates. Current roadmap sequence remains authoritative.

A later phase must not be implemented as if an earlier phase were complete unless the relevant gate has been explicitly approved.

## 6. Architecture boundaries

The ELO architecture must preserve conceptual separation between:

- Context
- Knowledge
- Memory
- Evidence
- Reasoning
- Recommendation
- Decision
- Policy
- Provenance
- Agents
- AI Gateway
- Integration
- Forge Constructor Plane

The Forge Constructor Plane constructs and validates implementations but does not become an ungoverned parallel Reasoning Engine, Cognitive Core, Memory system, or governance authority.

## 7. Cognitive orchestration boundary

ELO is the cognitive authority and orchestrator.

Canonical relationship:

`ELO decides/orchestrates → specialized member provides evidence or executes → ELO verifies`

Supabase is a consultative memory member. It may retrieve, relate and return structured memory, but it must not independently interpret, promote or commit learning.

Forge is the execution/versioning member. It may build, test, commit and prepare PRs only after the ELO gates authorize the operation.

GitHub Issue/PR is the durable decision and versioning ledger. It records evidence and approvals; it does not replace ELO cognitive judgment.

Automations are deterministic process adapters. A technical trigger must never outrun ELO governance.

## 8. ELO APRENDER canonical sequence

`ELO APRENDER → ELO ANALYSIS → SUPABASE MEMORY CONSULT → ELO CONSOLIDATION → COGNITIVE MERGE → GOVERNANCE → ISSUE DOSSIER → MERGED APPROVED? → COMMIT → COMMIT VERIFY → ISSUE UPDATE → PR → GIT MERGE → MAIN/ELO`

**Cognitive MERGE** means ELO consolidates experiences and concepts into governed knowledge.

**Git MERGE** means the approved PR is integrated into `main`.

They are distinct operations.

No commit may precede the cognitive MERGE approval for a governed learning change.

## 9. Learning and memory admission

A valuable experience does not automatically become architecture or a rule.

ELO must distinguish, as applicable:

- CASE
- PRECEDENT
- LEARNING_CANDIDATE
- VALIDATED_LEARNING
- CONCEPTUAL_KNOWLEDGE
- INSTRUCTIONAL_KNOWLEDGE
- RULE

Existing `VALIDATED_LEARNING` should be reused and enriched with relevant evidence rather than duplicated.

A precedent must not be promoted to a rule automatically.

## 10. Multi-tenancy and identity

Where a governed operation is involved, preserve tenant_id, domain, principal_id, session_id, request_id and correlation_id where applicable.

## 11. Evidence and provenance

Do not conflate AuditEvent, ProvenanceRecord and Evidence. Knowledge sources must remain distinguishable from hypotheses, recommendations, decisions and organizational experience.

## 12. Testing requirements

For implementation work:

- add or update tests with the change;
- run the project test suite relevant to the changed area;
- run compile/type/lint checks when configured;
- record failures honestly;
- never report a phase as READY when required tests are absent or failing.

## 13. Git discipline

Preferred flow for governed learning and architecture changes:

`issue/task → ELO analysis → cognitive MERGE approval → dedicated branch → commit → verification → PR → Git merge → final verification`

Do not write directly to `main` during task execution.

Do not commit a governed learning change before ELO cognitive MERGE approval.

## 14. Autonomous ELO execution loop

When a task objective is explicit, executable and within policy, ELO should continue through the complete governed workflow:

`OBJECTIVE → DECOMPOSE → EXECUTE → VALIDATE → SPECIALIST_REVIEW → ELO_REVIEW → CORRECT/REPLAN → REVALIDATE → COGNITIVE_MERGE → APPROVE → COMMIT → VERIFY → PR → GIT_MERGE → VERIFY → LEARN → REPORT`

Automatic merge is allowed only when ELO emits `APPROVE_MERGE`, required specialist/CI/acceptance/scope/protection gates pass, no blocking finding remains, and no governed learning commit occurred before cognitive approval.

## 15. Stop conditions

Stop and request an architectural decision when two canonical contracts conflict, a change would break a public contract without migration, a new persistent data model is required but unspecified, a component would bypass an established governance boundary, evidence is insufficient, required capabilities are unavailable, or correction cycles are exhausted.

## 16. Definition of done for AI work

DONE requires:

- scope satisfied;
- canonical contracts reused;
- no known duplicate implementation introduced;
- tests/evidence produced when applicable;
- documentation updated when behavior or contract changed;
- git status clean except for intentional changes;
- commit/PR information reported;
- unresolved risks explicitly listed;
- final verification completed after merge.
