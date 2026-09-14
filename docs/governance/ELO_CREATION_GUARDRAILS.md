# ELO Creation Guardrails — Universal Invariant

**Status:** NORMATIVE
**Authority:** ELO Operating Rules + ELO Constraints + AI Agent Working Rules
**Scope:** Every new or modified ELO capability, application, connector, adapter, skill, frontend, integration, test and persistent structure

## Purpose

This document makes explicit a repository-wide rule that already follows from the ELO governance framework:

> **No new implementation may bypass an existing ELO contract, boundary, authority model or canonical capability. Every creation must be governed before it is created, not corrected only after a violation occurs.**

This is a preventive control. It applies to AI agents, human contributors, Forge work, frontend work, connectors, adapters, providers and generated code.

## 1. Mandatory pre-creation sequence

Before creating or materially changing anything, execute:

```text
INSPECT
→ SEARCH exact concept
→ SEARCH synonyms / abbreviations
→ FIND existing contract/interface
→ FIND existing implementation
→ FIND existing tests
→ FIND relevant ADR / governance rule
→ IDENTIFY canonical owner
→ CLASSIFY REUSE | EXTEND | CORRECT | CONSOLIDATE | DEPRECATE | NEW
→ DEFINE smallest boundary-preserving change
→ IMPLEMENT
→ TEST
→ ELO GOVERNANCE GATE
```

`NEW` is not the default. It requires a demonstrated gap and traceability justification.

## 2. Universal architectural invariants

Every implementation MUST preserve:

- one canonical Cognitive Core;
- one canonical authority per governed concept/scenario;
- Cognitive/Core/Forge/Application/Infrastructure separation;
- tenant/domain/principal isolation where applicable;
- authorization before external access or execution;
- provenance and request/correlation lineage;
- admission and promotion governance for retained knowledge;
- replaceable Application/Infrastructure boundaries;
- existing public contracts unless an approved migration exists;
- reversible changes where practical and required;
- executable evidence for maturity claims.

## 3. No parallel capability rule

Never create a second version of an existing capability merely because the existing implementation is incomplete, inconvenient or difficult to reuse.

Forbidden patterns include:

- `RequestV2` created only to avoid an existing request contract;
- duplicate memory/reasoning/core implementations;
- a second login/authentication authority;
- a second database authority for the same canonical data;
- a frontend that calls a downstream executor directly when a governed Cognitive boundary already exists;
- copied Hermes runtime logic inside ELO Cognitive or ELO Web;
- a new connector that silently reimplements authorization;
- duplicate routes for the same governed operation without an explicit consolidation decision.

The required response is `REUSE`, `EXTEND`, `CORRECT` or `CONSOLIDATE` unless a real gap is demonstrated.

## 4. Frontend invariant

The ELO Web is an Application layer. It MUST remain replaceable and MUST NOT become a cognitive authority.

For governed AI execution, the canonical path is:

```text
User / Browser
→ ELO Web
→ authenticated server boundary
→ ELO Cognitive
→ governed Symbiont contract
→ Hermes runtime
→ Evidence / Outcome
→ ELO governed learning / Evolution Gate
```

The browser MUST NOT:

- call Hermes directly;
- construct or approve canonical authority;
- promote skills or knowledge;
- contain provider/runtime secrets;
- choose an execution capability outside the Cognitive authorization decision;
- bypass provenance, tenant, domain or principal boundaries.

## 5. Hermes integration invariant

Hermes is an external execution/orchestration runtime. It is not a second ELO Core, memory authority, governance engine or Evolution Gate.

The ELO-owned Hermes boundary MUST remain contract-first. An execution request must preserve, where applicable:

- `request_id`;
- `intent`;
- `tenant_scope`;
- `mission_class`;
- `authorized_capabilities`;
- bounded context;
- evidence requirements.

Infrastructure identifiers and secrets MUST NOT cross this boundary. Hermes-created skills remain non-canonical until ELO governance promotes them.

## 6. Error-prevention control

A recurring architectural error MUST be converted into a reusable invariant, test or validation rule rather than fixed only in the affected feature.

Therefore, when a violation is discovered:

1. correct the immediate implementation;
2. identify the missing preventive control;
3. add or strengthen a repository-level guard/test/check;
4. document the invariant when its scope is universal;
5. revalidate existing adjacent implementations for the same failure mode.

The objective is to prevent recurrence in future creations, not only repair the current file.

## 7. Mandatory implementation evidence

Every substantive implementation must leave the following evidence path:

```text
Requirement
→ Canonical rule / contract
→ Implementation
→ Executable test
→ Verification result
→ PR review record
→ Merge
```

A passing build alone is insufficient when architecture, security, authorization, provenance or integration boundaries are affected.

## 8. Minimum tests for governed integrations

When applicable, tests MUST cover:

- happy path;
- invalid input;
- unauthorized access;
- tenant/domain/principal isolation;
- dependency failure and timeout;
- malformed external response;
- request/correlation ID preservation;
- provenance;
- connector/runtime isolation;
- secrets/infrastructure-field rejection;
- canonical authority protection;
- non-canonical learning candidate handling.

## 9. PR gate requirement

Before merge, the ELO PR Governance Gate must verify that the creation followed this guardrail and that no new duplicate or authority violation was introduced.

A material change invalidates prior ELO approval and requires the full review loop again.

## 10. Operational interpretation

This document is not permission to create more governance documents for every feature. It is a reusable guardrail that points implementations back to the existing ELO authority map, contracts, tests and Evolution Gate.

The preferred behavior is:

> **Search first. Reuse the canonical owner. Extend only when justified. Put execution behind the established boundary. Add a preventive test when an error class is discovered.**
