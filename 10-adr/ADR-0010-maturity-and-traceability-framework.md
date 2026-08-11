# ADR-0010 — ELO Maturity and Traceability Framework

- **Status:** proposed
- **Date:** 2026-08-11
- **Decision owner:** ELO Architecture & Governance
- **Related:** `ELO_BASELINE_MATURITY_AND_TRACEABILITY_FRAMEWORK.md`

## Context

The ELO repository contains architectural documentation, implementation artifacts, cognitive interface work, roadmap material and historical directories in more than one naming convention. The project also uses AI coding agents, making it necessary to distinguish proposals, contracts, implementation and verified behavior.

Without a maturity and traceability mechanism, a document can be incorrectly interpreted as evidence of implementation, and an implementation can be incorrectly interpreted as verified capability.

## Decision proposed

Adopt a controlled maturity scale:

```text
0 absent
1 conceptual
2 documented
3 contracted
4 implemented
5 tested
6 verified
7 operationally evidenced
```

and require traceability, where applicable, across:

```text
requirement → capability → contract → ADR → implementation → test → evidence
```

The framework must be evidence-based and must not promote a capability merely because documentation exists.

## Alternatives considered

### A. No centralized maturity model

Rejected because it preserves ambiguity between documentation and implementation.

### B. Percentage-only maturity score

Rejected as the sole mechanism because a high average can conceal a critical security, tenancy, provenance or governance deficiency.

### C. Centralized framework plus capability registry

Proposed because it gives the project a stable vocabulary while keeping individual capability evidence distributed in its natural owners.

## Consequences

### Positive

- Better architectural auditability.
- Easier handoff between ChatGPT, Codex and other agents.
- More reliable phase completion claims.
- Clearer PR scope.
- Lower risk of documentation duplication.
- Explicit evidence requirements.
- Baseline snapshots become possible.

### Negative

- Additional metadata must be maintained.
- Existing capabilities require an initial audit.
- Some historical artifacts may remain ambiguous until an ADR resolves ownership.

## Non-goals

This ADR does not:

- approve new cognitive capabilities;
- authorize autonomous agents;
- declare the entire repository production-ready;
- replace security or compliance controls;
- replace human architectural review.

## Approval gate

This ADR remains `proposed` until the framework has been reviewed against the current architecture, governance documents and existing ADR set.
