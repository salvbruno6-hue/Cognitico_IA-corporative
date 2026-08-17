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

The implementation sequence is governed by explicit gates. Current roadmap sequence:

ELO-001 Cognitive Interface Vertical Slice
→ ELO-002 Context Engine MVP
→ ELO-003 Knowledge Retrieval MVP
→ ELO-004 AI Gateway
→ ELO-005 Governed Reasoning MVP
→ ELO-006 Provenance
→ ELO-007 Decision Intelligence MVP
→ ELO-008 IAM/Tenant Enforcement
→ ELO-009 Governed Memory MVP
→ ELO-010 Controlled Agent Runtime
→ ELO-011 Demand Intelligence
→ ELO-012 First Enterprise Adapter
→ ELO-013 Production Readiness

A later phase must not be implemented as if an earlier phase were complete unless the relevant gate has been explicitly approved.

## 6. Current ELO-001 rule

ELO-001 is considered complete only when the real path is demonstrated and tested:

ELOChat
→ HTTP/API adapter
→ CognitiveAPI
→ Session
→ CognitiveCore
→ ResponseBuilder
→ CognitiveResponse

Required evidence includes valid request validation, mandatory tenant context, session creation/recovery, domain preservation, typed core input, canonical response, request/response correlation, processing time, consistent errors, happy-path tests, error tests, and local execution documentation.

Do not treat `compileall` alone as proof of functionality. A test suite that collects zero tests is a failure of the gate.

## 7. Architecture boundaries

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

## 8. Multi-tenancy and identity

Where a governed operation is involved, preserve:

- tenant_id
- domain
- principal_id
- session_id
- request_id
- correlation_id

`department` may exist as a business attribute, but must not be the primary security boundary.

## 9. Evidence and provenance

Do not conflate:

AuditEvent != ProvenanceRecord != Evidence

Knowledge sources must remain distinguishable from hypotheses, recommendations, decisions, and organizational experience.

Forge artifacts must retain their origin and classification when used as evidence. Inspection of an operational artifact does not constitute promotion into the canonical architecture.

## 10. AI provider boundary

Application and cognitive components must not hard-code direct provider coupling when the architecture calls for an AI Gateway.

Preferred direction:

Cognitive capability
→ AI Gateway
→ Provider contract
→ Provider

## 11. Testing requirements

For implementation work:

- add or update tests with the change;
- run the project test suite relevant to the changed area;
- run compile/type/lint checks when configured;
- record failures honestly;
- never report a phase as READY when required tests are absent or failing.

## 12. Git discipline

Preferred flow:

issue/task
→ dedicated branch
→ focused commits
→ tests
→ pull request
→ architectural review
→ merge

For Forge work, use a dedicated `forge/*` branch namespace or an explicitly named constructor branch. Do not use a long-lived Forge branch as a substitute for `main`.

Do not mix unrelated work in the same commit.

Suggested commit prefixes:

- `docs:` documentation
- `feat:` new capability
- `fix:` corrective change
- `test:` tests
- `refactor:` structural refactor without intended behavior change
- `chore:` tooling/maintenance
- `security:` security/governance correction
- `adr:` architecture decision

## 13. Autonomous ELO execution loop

When a task objective is explicit, executable, and within policy, ELO should continue through the complete governed workflow rather than stopping at a recommendation:

OBJECTIVE
→ DECOMPOSE
→ EXECUTE
→ VALIDATE
→ SPECIALIST REVIEW
→ ELO ARCHITECTURAL REVIEW
→ CORRECT
→ REVALIDATE
→ APPROVE
→ MERGE
→ VERIFY
→ REPORT

The loop may repeat correction/review cycles up to the task's configured limit. A terminal state must be one of COMPLETED, BLOCKED, ESCALATED, or FAILED.

Automatic merge is allowed only when:

- ELO decision is `APPROVE_MERGE`;
- required specialist reviews pass or are explicitly not applicable;
- required CI checks pass;
- acceptance criteria pass;
- no blocking review finding remains;
- scope is compliant;
- forbidden/destructive actions were not introduced;
- the change is not being pushed directly to `main`;
- repository protections permit the merge.

High-risk work may be automated only when the task explicitly permits it and repository policy does not require a human approval. The agent must never bypass a repository protection or invent authority.

## 14. Stop conditions

Stop and request an architectural decision when:

- two canonical contracts conflict;
- two folders appear to be competing authorities;
- a change would break a public contract without migration;
- a new security boundary is required;
- a new persistent data model is required but not specified;
- a roadmap capability is required to complete the current phase;
- a component would need to bypass an established governance boundary;
- evidence is insufficient to make the requested conclusion safely;
- required credentials/capabilities are unavailable;
- correction cycles are exhausted.

## 15. Definition of done for AI work

A task is not DONE merely because files were generated.

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
