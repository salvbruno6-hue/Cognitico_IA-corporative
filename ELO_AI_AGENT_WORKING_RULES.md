# ELO — AI Agent Working Rules

## 1. Scope

This protocol governs work performed by ChatGPT, Codex, IDE agents, repository agents, automation agents, and other AI systems against the ELO repository.

The objective is continuity: different AI systems must be able to enter the repository and understand what is authoritative, what is proposed, what is implemented, what is tested, and what remains blocked.

## 2. First action: establish state

Before changing anything, report:

- repository;
- branch;
- HEAD SHA;
- working-tree state when available;
- target task/issue;
- current ELO phase;
- dependency phase;
- relevant existing files;
- tests available;
- blockers.

Never infer that a phase is complete solely because its documents or directories exist.

## 3. Search before creation

For every requested concept, search for:

1. exact term;
2. synonyms;
3. existing interface/contract;
4. existing class/schema;
5. existing test;
6. existing ADR;
7. existing roadmap entry;
8. related implementation.

Then classify the work as:

- reuse;
- extend;
- correct;
- consolidate;
- deprecate;
- create new.

`create new` requires justification.

## 4. Context hierarchy

Use this reading order when resolving architectural meaning:

1. `AGENTS.md`;
2. repository navigation rules;
3. enterprise/constitutional manifest;
4. architecture baseline;
5. relevant ADRs;
6. governance/policy;
7. canonical contracts;
8. implementation;
9. tests;
10. roadmap/proposals.

Lower-level code must not silently redefine higher-level architecture.

## 5. Planning rule

Before a substantial change, write a short execution plan:

- objective;
- files expected to change;
- contracts reused;
- tests to add/update;
- risks;
- non-goals.

If the plan reveals an architectural conflict, stop and request an ADR rather than improvising.

## 6. Implementation rule

Prefer:

small boundary-preserving change
→ test
→ review
→ next change

Avoid:

large rewrite
→ many coupled changes
→ unclear test coverage.

Do not rename or relocate broad directory trees during a feature task unless the task explicitly concerns consolidation.

## 7. Contract-first behavior

When a canonical contract exists:

- reuse it;
- extend it deliberately;
- preserve compatibility where required;
- add migration when breaking change is approved.

Do not create `RequestV2`, `NewContext`, `BetterMemory`, or similar parallel contracts merely to avoid understanding the existing contract.

## 8. Cognitive architecture rule

The ELO Cognitive Core is an orchestration boundary, not a dumping ground.

Use specialized boundaries for:

- context assembly;
- knowledge retrieval;
- memory access;
- evidence handling;
- reasoning;
- scenario analysis;
- decision support;
- provenance;
- agent orchestration.

The Core may coordinate these capabilities without owning all their implementation details.

## 9. Consulting Mode rule

The emerging ELO Cognitive Consulting capability must not be implemented as an unrestricted autonomous consultant.

The intended pattern is:

Observe
→ Detect
→ Contextualize
→ Identify information gaps
→ Ask
→ Retrieve relevant knowledge
→ Compare experience
→ Form hypotheses
→ Gather evidence
→ Reason
→ Model scenarios
→ Recommend
→ Human decision
→ Observe outcome
→ Governed learning

The system must distinguish:

- fact;
- observation;
- hypothesis;
- external reference;
- internal experience;
- recommendation;
- human decision;
- outcome.

## 10. Organizational learning rule

A previous solution is not automatically a reusable solution.

The agent must consider:

- context similarity;
- constraints;
- evidence quality;
- applicability conditions;
- non-applicability conditions;
- outcome quality;
- unintended consequences.

The intended behavior is:

"This experience is partially analogous under conditions X/Y, but differs in Z."

not:

"This worked before, therefore repeat it."

## 11. External knowledge rule

External web/AI/scientific knowledge may inform a hypothesis, but must not silently become organizational truth.

Record where applicable:

- source;
- date;
- author/provider;
- scope;
- evidence quality;
- applicability;
- limitations;
- provenance.

## 12. Organizational health rule

The ELO should identify operational signals and capability gaps, not automatically label people.

Use distinctions such as:

anomaly ≠ error
error ≠ negligence
negligence ≠ incompetence

Repeated operational problems must first be evaluated against:

- process quality;
- system quality;
- training;
- tooling;
- workload;
- supervision;
- policy;
- environmental conditions;
- capability.

Only then should a human-governed capability assessment be considered.

## 13. Sensitive information rule

Never use a broad organizational data set merely because it exists.

For each investigation define a relevance scope:

problem
→ related entities
→ related processes
→ relevant systems
→ permitted sources
→ required evidence

Apply tenant, domain, principal, policy, and need-to-know boundaries.

## 14. Provenance rule

For important cognitive outputs, preserve the ability to answer:

- What triggered this?
- Which request?
- Which tenant/domain?
- Who/what supplied the information?
- Which evidence was used?
- Which external knowledge was consulted?
- Which model/provider was used, when applicable?
- What reasoning/validation occurred?
- What recommendation was produced?
- What human decision followed?
- What outcome occurred?

## 15. Testing rule

Every implementation task must specify tests before declaring completion.

Minimum categories when applicable:

- happy path;
- invalid input;
- authorization failure;
- tenant isolation;
- domain handling;
- dependency failure;
- timeout;
- malformed external response;
- provenance;
- correlation/request IDs;
- security/privacy behavior.

A zero-test collection is not a passing gate.

## 16. Review rule

For a pull request, report:

### What changed
Concise list.

### Why
Requirement and architectural rationale.

### Contracts
Existing contracts reused or changed.

### Tests
Commands, number collected, passed/failed/skipped.

### Risks
Known limitations.

### Debt
Known follow-up work.

### Architecture decisions
Any decision that requires explicit approval.

## 17. Git rule

Use a dedicated branch for substantive work.

Do not merge automatically for:

- architecture;
- security;
- data model;
- tenant boundary;
- identity;
- decision authority;
- autonomous behavior.

Documentation-only low-risk changes may still use PR review as the default project convention.

## 18. Handoff rule

At the end of every task, leave enough information for another AI to continue:

- current phase;
- completed criteria;
- failed criteria;
- current branch;
- latest SHA;
- files changed;
- tests run;
- unresolved questions;
- next exact action.

Never rely on the previous conversation as the only source of state.

## 19. Stop words

The following statements require evidence before use:

- complete;
- production-ready;
- secure;
- compliant;
- autonomous;
- validated;
- scalable;
- enterprise-ready.

Replace unsupported claims with measurable status.

## 20. Final principle

The AI agent is an implementation and reasoning assistant operating under ELO governance.

It is not the authority that defines the ELO architecture by itself.
