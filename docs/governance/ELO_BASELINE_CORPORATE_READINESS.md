# ELO — Baseline Corporate Readiness

## 1. Purpose

This document defines the engineering-control interpretation of the ELO baseline after recovery of the post-Diagnostic Scenario Engine integration defects.

It separates four states that must not be conflated:

1. **Code is executable** — the repository installs, compiles, and tests run.
2. **Baseline is behaviorally stable** — the current regression suite is green.
3. **Architecture is sufficiently evidenced** — the declared architectural scenarios have executable evidence.
4. **Enterprise production readiness** — operational, security, governance, resilience, observability, ownership, and rollback controls are evidenced.

A green unit/regression suite proves only the first two states. It does not automatically prove the latter two.

## 2. Current evidence boundary

As of the current `main` baseline:

- the behavioral-validation workflow is configured for Python 3.14;
- package installation and compilation are validated;
- the repository test suite is executed by CI;
- the latest recorded successful run reported 77 passing tests;
- contextual observation normalization is treated as a canonical-contract boundary;
- Conversation/Evolution Memory, ChatBridge, SourceDiscovery, ContextualMemory, canonical identity, evolution memory, and knowledge admission have executable tests.

The repository test matrix separately defines 44 architectural scenarios. A scenario marked `DEFINED` is not evidence of implementation merely because the scenario is documented.

## 3. Engineering state model

### State A — GREEN BASELINE

Required:

- CI passes from a clean environment;
- no known baseline-breaking defect remains open;
- canonical contracts are preserved;
- tenant/domain/provenance/correlation boundaries remain intact;
- no test is weakened merely to obtain green status.

This is the current working state.

### State B — EVIDENCED BASELINE

Required in addition to State A:

- every critical architectural scenario has executable evidence;
- positive cases and negative cases are represented;
- adversarial cases are represented;
- tenant isolation is tested across positive and negative paths;
- provenance survives each relevant boundary;
- authorization failures are explicit;
- provider unavailability cannot become fabricated evidence;
- incomplete flows cannot be reported as complete;
- uncertainty remains explicit;
- deterministic precedence rules are tested;
- evidence is linked to a commit and reproducible test execution.

This is the target before formal Baseline v1.0 freeze.

### State C — ENTERPRISE PILOT READY

Required in addition to State B:

- production-like configuration is tested;
- secrets are externalized;
- authorization and tenant controls are exercised through the real integration boundary;
- audit/provenance records are inspectable;
- structured logs and correlation IDs exist;
- health/readiness behavior is defined;
- failure and timeout behavior is bounded;
- rollback procedure is tested;
- operational owner is identified;
- support/incident path is defined;
- data retention and deletion behavior is defined where applicable;
- cost and provider failure modes are measurable.

### State D — PRODUCTION READY

Required in addition to State C:

- service-level objectives are defined and measured;
- capacity and concurrency limits are known;
- resilience behavior is validated;
- security review is complete for the deployment scope;
- change-management and release controls are operational;
- monitoring produces actionable alerts rather than only logs;
- disaster/recovery assumptions are documented and tested where required;
- business ownership and technical ownership are explicit;
- evidence can be reproduced independently of the developer who implemented the feature.

## 4. Corporate reality model

The main corporate risk is not a single failing test. It is **false confidence**.

A system can be green in CI while still being unsafe to promote because:

- the tested path is narrower than the operational path;
- authorization is mocked rather than enforced at the real boundary;
- tenant isolation is assumed rather than adversarially tested;
- external providers fail differently from local mocks;
- provenance is dropped between adapters;
- a timeout creates an ambiguous state;
- memory promotion becomes implicit;
- a recommendation is interpreted as a decision;
- an experimental component is mistaken for a canonical component;
- rollback restores binaries but not state;
- operators cannot determine why a decision was produced.

Therefore ELO must treat **evidence integrity** as a first-class engineering property.

## 5. Required test progression

### Gate 1 — Baseline regression

Current objective:

```text
install
→ compile
→ complete repository pytest suite
→ artifact evidence
→ green CI
```

Failure interpretation:

- any regression in a canonical contract blocks promotion;
- test collection failure is a failure;
- missing tests are not equivalent to passing tests;
- undocumented manual validation is not equivalent to automated evidence.

### Gate 2 — Architectural coverage

Convert the remaining `DEFINED` scenarios in the executable matrix into real tests.

Priority order:

1. Context
2. Discovery
3. Handoff
4. Diagnostic
5. Production-flow invariants
6. Memory
7. Adversarial
8. Governance

The priority is intentional: context and provenance errors propagate into every downstream layer.

### Gate 3 — Boundary and adversarial testing

For each security- or governance-relevant boundary, test at least:

- valid input;
- missing required context;
- wrong tenant;
- wrong domain;
- wrong principal;
- conflicting source;
- insufficient evidence;
- unauthorized provider;
- unavailable provider;
- malformed payload;
- duplicated request/correlation;
- incomplete workflow;
- low-confidence result;
- attempted architectural bypass.

### Gate 4 — Operational simulation

Introduce production-like tests for:

- timeout;
- retry;
- partial dependency failure;
- provider degradation;
- malformed external response;
- concurrent requests;
- repeated request;
- state recovery;
- restart;
- rollback;
- observability correlation.

## 6. Corporate projections

These are engineering projections, not claims about current production capability.

### Projection P0 — current

**Condition:** green repository regression suite.

Expected capability:

- safe continuation of baseline engineering;
- controlled implementation of missing tests;
- no automatic production promotion.

Primary risk:

- confusing regression stability with architectural completeness.

### Projection P1 — evidenced baseline

**Condition:** all critical matrix scenarios have executable evidence and the complete suite remains green.

Expected capability:

- formal Baseline v1.0 review becomes reasonable;
- architecture can be frozen as a controlled reference point;
- future changes can be measured against a known behavioral contract.

Primary risk:

- hidden operational assumptions outside the repository.

### Projection P2 — controlled enterprise pilot

**Condition:** P1 plus operational/security/observability controls.

Expected capability:

- limited tenant/pilot deployment;
- real adapter/provider integration under controlled conditions;
- measurable operational behavior;
- incident and rollback exercises.

Primary risk:

- scale exposes cost, latency, concurrency, provider, and organizational bottlenecks not visible in unit tests.

### Projection P3 — production candidate

**Condition:** P2 plus SLOs, capacity evidence, security review, operational ownership, and repeatable release controls.

Expected capability:

- production-readiness review;
- controlled expansion of enterprise integrations;
- governed evolution of the cognitive core.

Primary risk:

- organizational process becomes the limiting factor rather than code.

## 7. What must not happen

Until State B is reached:

- do not freeze Baseline v1.0;
- do not declare the Diagnostic Scenario Engine production-ready solely from unit-test success;
- do not promote new memory behavior to canonical status without explicit evidence;
- do not treat GPT/provider output as ELO source of truth;
- do not replace missing tests with documentation;
- do not weaken contracts to preserve green CI;
- do not merge unrelated architectural capabilities into the baseline recovery work.

Until State C is reached:

- do not describe the system as enterprise-pilot ready;
- do not assume mock-based provider tests represent provider production behavior;
- do not rely on developer knowledge as the operational runbook.

Until State D is reached:

- do not describe the system as production-ready.

## 8. Baseline freeze criteria

Baseline v1.0 may be proposed only when all of the following are true:

- [ ] current CI suite is green;
- [ ] architectural matrix is fully evidenced for critical scenarios;
- [ ] no open critical baseline defect exists;
- [ ] tenant isolation tests are green;
- [ ] provenance preservation tests are green;
- [ ] authorization-negative tests are green;
- [ ] provider-failure tests are green;
- [ ] incomplete-flow tests are green;
- [ ] deterministic precedence tests are green;
- [ ] adversarial tests are green;
- [ ] evidence is linked to a reproducible commit;
- [ ] known limitations are documented;
- [ ] formal architecture review approves the freeze.

## 9. Definition of done for the current track

The current baseline-integrity track is complete only when:

```text
#61 resolved
    ↓
#57 baseline regression restored
    ↓
repository suite green
    ↓
architectural matrix executed
    ↓
adversarial/boundary suite green
    ↓
reproducible evidence package
    ↓
Baseline v1.0 freeze review
```

The green state is a gate, not the destination.

## 10. Decision principle

When evidence conflicts with architectural expectation, the evidence wins as the description of current behavior; the architecture wins as the normative target. The difference must become an explicit defect, decision, or migration task.
