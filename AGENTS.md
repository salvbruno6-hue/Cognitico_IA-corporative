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
12. Do not merge architectural changes automatically.

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

An Agent must not become an ungoverned parallel Reasoning Engine. Reasoning must not bypass policy, evidence, provenance, or the AI Gateway when those boundaries apply.

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

## 13. Stop conditions

Stop and request an architectural decision when:

- two canonical contracts conflict;
- two folders appear to be competing authorities;
- a change would break a public contract without migration;
- a new security boundary is required;
- a new persistent data model is required but not specified;
- a roadmap capability is required to complete the current phase;
- a component would need to bypass an established governance boundary;
- evidence is insufficient to make the requested conclusion safely.

## 14. Definition of done for AI work

A task is not DONE merely because files were generated.

DONE requires:

- scope satisfied;
- canonical contracts reused;
- no known duplicate implementation introduced;
- tests/evidence produced when applicable;
- documentation updated when behavior or contract changed;
- git status clean except for intentional changes;
- commit/PR information reported;
- unresolved risks explicitly listed.
