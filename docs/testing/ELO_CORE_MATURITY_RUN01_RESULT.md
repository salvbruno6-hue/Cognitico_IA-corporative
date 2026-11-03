# ELO Core Maturity — RUN-01 Result

## Test

**RUN-01 — Intent → Context → Evidence → Reasoning → Decision → Next Action**

## Scope

This test validates the existing canonical `CoreLoopEngine` using the existing Context Resolution and Diagnostic Scenario contracts. It does not introduce a second reasoning engine or execution authority.

## Evidence fixture

Tenant: `tenant-mt`
Domain: `PCP`
Sources: `src-demand`, `src-capacity`

The fixture contains explicit provenance, tenant and domain for both evidence records.

## Cases

### RUN01-HAPPY

Expected:
- recommendation produced;
- evidence IDs preserved;
- diagnostic lenses preserved;
- confidence threshold satisfied;
- `can_execute == false`.

### RUN01-GAP

Expected:
- no observations → `BLOCKED`;
- explicit GAP;
- handoff required;
- no fabricated decision;
- `can_execute == false`.

### RUN01-CONFLICT

Expected:
- conflicting evidence → `HANDOFF`;
- conflict remains explicit;
- recommendation is absent;
- execution remains impossible.

## Operational execution

GitHub Actions is the evidence authority for this repository-local maturity criterion. The canonical Baseline Evidence Gate executes `tests/integration/test_core_critical_run01.py` and canonical boundary tests on the checked-out commit.

The dedicated evidence cycle was executed by PR #517 on head commit `e11f0959b3fa7d4469ba6e20a60c4c31c5d8d8a1`.

Reproducible evidence:

- environment: GitHub Actions / `ubuntu-latest`;
- workflow: **ELO Baseline Evidence Gate**;
- workflow run: `34916707206`;
- job: `104215791138` — **Reproducible baseline evidence**;
- tested SHA: `e11f0959b3fa7d4469ba6e20a60c4c31c5d8d8a1`;
- step `Run baseline evidence gate`: `success`;
- step `Run RUN-01 critical path evidence`: `success`;
- step `Run canonical boundary tests`: `success`;
- step `Publish gate summary`: `success`;
- PR #517 merged through commit `e3b594aaf6fcfa5668b068c958b0bb70b421bce9`.

The gate summary explicitly records that executable RUN-01 critical-path evidence and canonical boundary tests passed.

## Result classification

Current state: **PASS — reproducible GitHub Actions evidence recorded**.

RUN-01 satisfies the matrix evidence rule because executable evidence is tied to a concrete commit and workflow run. The three governed cases remain covered by the canonical integration test, and later Baseline Evidence Gate executions retain RUN-01 as regression coverage.

## Maturity impact

RUN-01 changes from `DEFINED` to `PASS` in the critical matrix.

This does **not** declare Baseline v1.0, production readiness, live provider behavior, or execution authority. Operational/external-provider maturity remains governed by the other critical matrix rows, including RUN-06 and OPS-02/OPS-03.

## Evidence record

- evidence-introduction PR: #265;
- canonical-gate integration PR: #450;
- dedicated evidence publication PR: #517;
- tested commit SHA: `e11f0959b3fa7d4469ba6e20a60c4c31c5d8d8a1`;
- merge commit carrying the evidence cycle: `e3b594aaf6fcfa5668b068c958b0bb70b421bce9`;
- environment: GitHub Actions / `ubuntu-latest`;
- command surface: canonical Baseline Evidence Gate including `python -m pytest -q tests/integration/test_core_critical_run01.py`;
- workflow/run identifier: `ELO Baseline Evidence Gate` / `34916707206`;
- job identifier: `104215791138`;
- observed result: `success`;
- residual risk: end-to-end production/external-provider behavior remains separate from this repository-local RUN-01 evidence.