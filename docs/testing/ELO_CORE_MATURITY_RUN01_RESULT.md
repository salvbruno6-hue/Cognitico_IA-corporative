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

## Result classification

The repository contains executable tests for all three cases. Final PASS is only recorded after the corresponding CI workflow execution is successful and tied to the commit containing this test.

## Maturity impact

If CI passes, RUN-01 changes from `DEFINED` to `PASS` in the critical matrix. It does not by itself establish Baseline v1.0.

## Required evidence record

- commit SHA: recorded by PR/CI;
- environment: GitHub Actions runtime;
- command: `python -m pytest -q tests/integration/test_core_critical_run01.py`;
- workflow/run identifier: to be recorded by CI;
- observed result: to be recorded only from CI;
- residual risk: end-to-end production/external-provider behavior remains separate from this repository-local test.
