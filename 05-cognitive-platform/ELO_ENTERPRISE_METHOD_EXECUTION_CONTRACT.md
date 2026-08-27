# ELO Enterprise Method Execution Contract

## Purpose

Define the execution boundary between ELO cognitive capabilities and the tenant's actual operating methodology.

## Mandatory sequence

```text
INPUT
  -> DISCOVER CONTEXT
  -> LOAD TENANT METHOD
  -> DECOMPOSE TASK
  -> MATCH CAPABILITIES
  -> SELECT MODEL / TOOL / ALGORITHM
  -> EXECUTE
  -> VERIFY AGAINST TENANT METHOD
  -> RECORD EXPERIENCE
  -> PROPOSE IMPROVEMENT
```

## Authority order

1. Safety, security and ELO Core invariants.
2. Explicit tenant rules and approved methodology.
3. Evidenced tenant practice.
4. Tenant-specific learned experience.
5. Governed improvement proposals.
6. External knowledge and experiments.

External knowledge cannot silently override an approved tenant rule.

## Unknown methodology

When a required method element is unknown, ELO must mark it as unknown or request evidence. It must not manufacture a parameter merely because a generic industry pattern exists.

## Artifacts

Every material decision should retain provenance for:

- source;
- method version;
- tenant scope;
- capability/executor;
- model version where applicable;
- inputs and assumptions;
- result;
- verification outcome;
- confidence;
- experience reference.

## Generalization boundary

A tenant-specific observation remains tenant-scoped. Repetition may strengthen evidence for that tenant but does not make the information portable. A candidate for Canon requires privacy screening, independent evidence, explicit generalization, regression testing and governance approval.
