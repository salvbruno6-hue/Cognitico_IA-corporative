# ELO Corporate Test Execution Protocol

## Purpose

Convert the ELO architectural test matrix into reproducible evidence and establish the minimum conditions for Baseline v1.0 review.

This protocol is subordinate to the canonical architecture and Evolution Gate. It does not create a new engine, memory model, adapter, or Cognitive Core.

## Evidence rule

A documented scenario is not evidence.

A scenario becomes `PASS` only when an executable test runs successfully and the result can be tied to a reproducible commit/run.

States:

- `PASS`: executed and approved.
- `FAIL`: executed and failed.
- `UNKNOWN`: evidence is insufficient.
- `BLOCKED`: execution is prevented by a known dependency or environment condition.
- `DEFINED`: specified but not yet executed.

Infrastructure failure must not be silently classified as functional failure. Functional failure must not be hidden as infrastructure failure.

## Execution order

The order is based on error propagation and corporate impact:

1. Context
2. Source Discovery
3. GPT/provider handoff
4. Diagnostic scenarios
5. Production-flow invariants
6. Memory/admission/provenance
7. Adversarial boundaries
8. Governance
9. Operational simulation

Context and provenance are first because downstream conclusions cannot be trusted when scope is wrong.

## Required assertions by domain

### Context

Test:

- entity identification;
- tenant preservation;
- domain preservation;
- principal preservation;
- session/request/correlation propagation;
- reliable metadata completion when explicit scope is absent;
- explicit context versus source conflict;
- wrong scope denial.

### Source Discovery

Test:

- deterministic precedence;
- specific intent versus generic terms;
- authorized source selection;
- unavailable source reporting;
- no manual technical path requirement;
- provenance continuity.

### Provider/GPT Handoff

Test:

- valid context requirement;
- evidence requirement;
- unauthorized provider denial;
- provider unavailable behavior;
- malformed provider response;
- no fabricated retrieval;
- provider output remains consultative and cannot become canonical truth by itself.

### Diagnostic

Test:

- baseline;
- stress;
- failure;
- counterfactual without canonical-state mutation;
- sensitivity dependency registration;
- conflict blocking;
- explicit low confidence;
- preservation of evidence and assumptions.

### Production Flow

ProductionFlow remains experimental until explicitly promoted.

Test:

- minimum complete cycle;
- deviation detection;
- tenant isolation;
- unit isolation;
- incomplete flow cannot be declared complete;
- missing/blocked/unknown stages remain visible.

### Memory

Test the distinction:

`Observation != Evidence != Knowledge != Decision != Evolution Memory`

Verify:

- authorized observation admission;
- unauthorized observation rejection;
- explicit promotion to evolution memory;
- provenance preservation;
- tenant/domain isolation;
- no implicit permanent learning from an ordinary observation.

### Adversarial

For each relevant boundary, test:

- wrong tenant;
- wrong domain;
- wrong principal;
- wrong unit;
- conflicting source;
- insufficient evidence;
- high confidence with wrong scope;
- unauthorized provider;
- available provider without authorization;
- unavailable provider;
- malformed payload;
- duplicate request/correlation;
- incomplete workflow;
- experimental component presented as canonical;
- attempted bypass of policy/provenance/evidence.

### Governance

Test:

- UNKNOWN does not become PASS;
- merge requires applicable gates;
- final diff is compared with baseline;
- architectural change is routed through Evolution Gate;
- missing tests remain visible;
- evidence package identifies commit, environment, command and result.

## Operational simulation

After architectural coverage is evidenced, execute production-like scenarios for:

- timeout;
- retry;
- partial dependency failure;
- provider degradation;
- malformed external response;
- concurrent requests;
- repeated requests;
- restart/recovery;
- rollback;
- observability correlation.

Operational tests must distinguish state loss, state recovery and stale state.

## Corporate analysis layer

For business scenarios, the test harness should preserve the distinction:

`observed data != calculation != inference != hypothesis != recommendation != decision`

When multiple sources or datasets are involved, validate:

- row/record counts;
- nulls;
- duplicate keys;
- domain violations;
- temporal consistency;
- granularity;
- cardinality;
- join duplication risk;
- source coverage;
- additive versus non-additive measures.

A KPI cannot be treated as a management fact until its data quality and semantic definition are established.

## Projection discipline

A projection must include:

- observed baseline;
- hypothesis;
- validity conditions;
- confirmation signals;
- deterioration signals;
- follow-up action.

A projection must never be reported as current fact.

## Baseline v1.0 freeze gate

Freeze review is allowed only when:

- current CI is green;
- critical architectural scenarios are executable;
- no critical baseline defect remains open;
- tenant isolation is green;
- provenance continuity is green;
- authorization-negative paths are green;
- provider failure paths are green;
- incomplete-flow paths are green;
- deterministic precedence is green;
- adversarial tests are green;
- evidence is reproducible from a clean environment;
- known limitations are documented;
- architecture review approves the freeze.

A green regression suite is a necessary condition, not sufficient evidence for the freeze.

## Completion artifact

Every completed execution cycle must produce:

```text
ELO TEST EVIDENCE RECORD

Commit:
Environment:
Python/runtime:
Install command:
Focused test commands:
Full-suite command:
Static checks:

PASS:
FAIL:
UNKNOWN:
BLOCKED:
DEFINED:

Coverage executed:
Positive execution rate:

Changed contracts:
Preserved invariants:
New risks:
Known limitations:
Decision:
```

## Non-negotiable rules

- Do not weaken a test to preserve green CI.
- Do not create duplicate architectural components to satisfy a scenario.
- Do not promote experimental components by documentation alone.
- Do not treat provider output as canonical truth.
- Do not infer authorization from department alone.
- Do not mix corporate and unit scope without explicit evidence.
- Do not convert missing evidence into confidence.
- Do not merge unrelated architectural changes into baseline recovery.
