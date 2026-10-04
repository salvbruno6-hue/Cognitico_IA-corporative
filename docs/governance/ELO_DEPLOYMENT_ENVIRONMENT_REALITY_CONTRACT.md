# ELO — Deployment Environment Reality Contract

## Purpose

Prevent the ELO from treating a declared, simulated or partially validated
deployment environment as a real deployed environment.

This contract is a **fail-closed evidence boundary**. It does not create a
deployment authority, runtime authority, provider adapter, or Evolution Gate.

## Reality levels

`NOT_DECLARED` → no environment identity is established.

`DECLARED_ONLY` → environment/configuration is named, but deployment is not
independently proven.

`ARTIFACT_VERIFIED` → deployment identity, source commit, artifact and
independent evidence reference exist. This proves an artifact/deployment
boundary, not runtime execution.

`RUNTIME_VERIFIED` → an observed runtime endpoint and healthcheck evidence
exist. This proves runtime observation, not production outcome.

`OPERATIONALLY_VERIFIED` → runtime operation was observed. This still does
not prove production outcome or authorize promotion.

`PRODUCTION_PROVEN` → production outcome was explicitly observed and explicit
governance approval evidence exists.

## Non-evidence

The following MUST NOT be converted into deployment proof by themselves:

- source code presence;
- deployment configuration files;
- environment variable declarations;
- successful unit/integration tests;
- CI success;
- mocked HTTP responses;
- local execution;
- a Vercel/Supabase project reference without a deployment observation;
- a URL written in documentation without an observed healthcheck;
- a runtime adapter existing in the repository.

## Required evidence chain

```
TARGET ENVIRONMENT
    ↓
DEPLOYMENT ID
    ↓
SOURCE COMMIT
    ↓
ARTIFACT
    ↓
INDEPENDENT DEPLOYMENT EVIDENCE
    ↓
OBSERVED RUNTIME ENDPOINT
    ↓
HEALTHCHECK EVIDENCE
    ↓
OPERATIONAL OBSERVATION
    ↓
PRODUCTION OUTCOME
    ↓
EXPLICIT GOVERNANCE APPROVAL
```

Each transition is independent. Missing evidence stops classification at the
highest verified level.

## Governance rules

1. Never infer deployment from configuration.
2. Never infer runtime from code existence.
3. Never infer production from CI.
4. Never infer production from a successful healthcheck alone.
5. Never let this contract authorize deployment, promotion or merge.
6. Preserve provenance for every positive classification.
7. Keep `deployment_proven`, `runtime_proven` and `production_proven`
   separate.
8. A failed or absent observation is a gap, not a negative claim about the
   external environment.

## Scope

This contract is reusable by Vercel, Supabase, GitHub Actions or another
authorized deployment provider. Provider-specific verification remains owned by
the existing provider/deployment boundary.

## Current implementation state

The contract establishes a deterministic classification boundary and tests the
most important false-positive cases. It does not claim that any current ELO
environment is production-proven.
