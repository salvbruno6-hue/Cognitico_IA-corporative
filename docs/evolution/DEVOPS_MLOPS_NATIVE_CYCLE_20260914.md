# ELO — DevOps + MLOps Native Cycle

## Decision

The current main already contains operational and MLOps concepts. This cycle therefore adds only the missing executable, provider-neutral boundaries rather than creating new infrastructure authorities.

## DevOps relation

`Core → NativeDevOpsOperation → observability/infrastructure adapters → Governance/Evolution Gate`

The boundary records change identity, evidence, provenance, health and rollback readiness. It does not deploy, scale, monitor, or own infrastructure.

## MLOps relation

`Cognitive learning/evaluation → NativeMLOpsEvaluation → Evidence/Learning → Governance/Evolution Gate`

The boundary records model, dataset version, evaluator, metric, threshold, score, evidence and provenance. It produces only `CANDIDATE` or `REJECTED`; it does not create a model registry, train models, or promote a model canonically.

## Ecosystem health method

Every implementation is assessed as:

`Relations → Code → Instructions → Contracts → Evidence → Governance → Tests → Merge → ON_MAIN → Post-merge Regression → Learning`

## Required invariants

- ELO remains the authority; infrastructure/model providers are adapters.
- Evidence and provenance are mandatory.
- Secret-bearing metadata is rejected.
- Failed health or unverified rollback blocks operational promotion.
- A model below threshold is rejected; a passing model remains candidate-only.
- No parallel registry, deployment authority, evaluation authority, or gate is created.
- Existing observability, experience evaluation, Evolution Gate and repository workflows remain canonical.

## Potencialização para o ELO

- **DevOps:** transforms operational readiness, health and recovery into explicit evidence that Core/Governance can reason over, improving safe evolution and recovery decisions.
- **MLOps:** turns model evaluation into reproducible cognitive evidence, allowing ELO to compare model experiences without delegating canonical judgment to an external platform.
