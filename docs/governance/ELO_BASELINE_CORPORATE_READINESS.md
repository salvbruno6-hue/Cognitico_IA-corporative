# ELO — Baseline Corporate Readiness

## 1. Purpose

This document defines the engineering-control interpretation of the ELO baseline. It separates four states that must not be conflated:

1. **Code is executable** — the repository installs, compiles, and tests run.
2. **Baseline is behaviorally stable** — the current regression suite is green.
3. **Architecture is sufficiently evidenced** — the declared architectural scenarios have executable evidence.
4. **Enterprise production readiness** — operational, security, governance, resilience, observability, ownership, and rollback controls are evidenced.

A green unit/regression suite proves only the first two states. It does not automatically prove the latter two.

## 2. Current evidence boundary — 2026-08-18

The current `main` contains the following merged closure waves:

- **PR #214 / merge `38f7a4d6f02bb68a40e5f7900df1e64251bf0e2c`** — authorized source-adapter → Temporal Memory → budgeting evidence integration, including provenance and unavailable-source behavior.
- **PR #215 / merge `fa5676e1164d1965e62414caacbc8d1e57669a37`** — adversarial closure for execution authority, provider degradation, scenario readiness/conflicts and budgeting retrieval provenance.
- **ELO-212 closure merge** — governed execution boundary, mandatory execution controls, deterministic blocking, provenance preservation and baseline closure criteria.

The repository therefore has executable evidence for important boundaries including source retrieval, context/provenance preservation, canonical scenario readiness, provider degradation, consultative GPT handoff, Forge promotion boundaries and governed execution controls.

This evidence does **not** by itself establish production readiness or Baseline v1.0. The distinction is intentional and remains a governance invariant.

## 3. Engineering state model

### State A — GREEN BASELINE

Required:

- CI passes from a clean environment;
- no known baseline-breaking defect remains open;
- canonical contracts are preserved;
- tenant/domain/provenance/correlation boundaries remain intact;
- no test is weakened merely to obtain green status.

The current repository is operating in this engineering state.

### State B — EVIDENCED BASELINE

Required in addition to State A:

- every critical architectural scenario has executable evidence;
- positive and negative cases are represented;
- adversarial cases are represented;
- tenant isolation is tested across positive and negative paths;
- provenance survives each relevant boundary;
- authorization failures are explicit;
- provider unavailability cannot become fabricated evidence;
- incomplete flows cannot be reported as complete;
- uncertainty remains explicit;
- deterministic precedence rules are tested;
- evidence is linked to a commit and reproducible test execution.

**State B is the target of #92/#156 and has not been declared complete merely from the merged closure waves.**

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

The main corporate risk is **false confidence**. A system can be green in CI while still being unsafe to promote because the tested path can be narrower than the operational path, authorization can be mocked rather than enforced at the real boundary, external providers can fail differently from local mocks, provenance can be dropped between adapters, or a recommendation can be mistaken for a decision.

Therefore ELO treats **evidence integrity** as a first-class engineering property.

## 5. Required test progression

### Gate 1 — Baseline regression

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

Remaining `DEFINED` scenarios in the executable matrix must be converted into real tests. The current implementation wave has materially reduced the previously documented gaps; #92/#156 remain the canonical owners of the residual matrix rather than creating new parallel test authorities.

Priority:

1. Context
2. Discovery
3. Handoff
4. Diagnostic
5. Production-flow invariants
6. Memory
7. Adversarial
8. Governance

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

Implemented closure evidence already covers several of these cases. The remaining matrix must be assessed explicitly rather than inferred from neighboring tests.

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

## 6. Current residual blockers

The previous registry described Source Resolver (#36) and Scenario Engine consolidation (#56) as active blockers. They are now **closed and implemented** and must not be treated as current blockers.

The remaining material validation tracks are:

- **#92** — reproducible baseline evidence and architectural matrix closure;
- **#156** — architecture-to-operation validation, including residual adversarial and end-to-end scenarios;
- **#137** — genuine specialist feedback not available to repository automation;
- **#125** — governed external architecture benchmark, which is comparative research rather than a prerequisite for the existing Core contracts.

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

```text
implemented closure waves
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
