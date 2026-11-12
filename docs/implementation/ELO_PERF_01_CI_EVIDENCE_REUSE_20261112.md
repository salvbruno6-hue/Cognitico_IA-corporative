# PERF-01 — CI evidence reuse: first governed reduction

Status: **candidate / awaiting current-head CI and Evolution Gate**  
Canonical owner: existing GitHub Actions CI workflows; no new approval authority.

## Confirmed redundancy

On `main` before this change, `elo-pr1-validation.yml`,
`elo-behavioral-validation.yml`, and the `validation` job of
`elo-evolution-gate.yml` each independently execute the entire Python
pytest suite after installing the same `[test,agentic]` extras and compiling
the same `src` tree. These executions remain separately checkable and are
not incorrectly collapsed into one claim of successful execution.

## Phase A — safe scope reduction (this change)

- Keep the **full pytest suite** in both ELO PR1 Validation and ELO
  Evolution Gate. Do not remove existing check names or weaken the external
  access, Hermes, Symbiont, Baseline or RUN-01 tests.
- Run explicitly selected behavioral Python tests in ELO Behavioral
  Validation, alongside its existing ELO Web OAuth regression.
- Preserve the behavioral `pytest.log` and `pytest.exit`, but publish under
  `elo-behavioral-test-evidence` to avoid implying full-suite coverage.
- Add `pytest-scope.json` with actual tested checkout SHA, PR head SHA,
  run id/attempt and scope. It explicitly sets
  `gate_authority=false` and `reusable_as_full_suite=false`.
- No source/runtime, Supabase schema, secret, authorization or merge semantics
  change. Old head/failed/pending checks must never be accepted as success.

## Expected effect and measurement

The redundant full-suite executions in these three workflows decrease
from **three to two** for each applicable trigger, while preserving both
full-suite gates. This is a *structural* count, not a claimed wall-clock,
runtime, cost or production latency improvement. Record at least 3 comparable
before/after PR runs on the same runner class and Python version. Compare
behavioral job median/p95 durations and the full set of required checks,
including failed/queued outcomes; no performance claim without actual timing.

## Phase B — true evidence reuse, deferred behind evidence and governance

Only after Phase A passes and the current Agent Loop/bootstrap contracts
are settled, assess a single canonical full-suite producer with consumers
that verify actual GitHub Actions provenance. Minimum proof:

`repository + tested checkout SHA + PR head SHA + test contract version +
dependency/environment digest + run ID + run attempt + job conclusion`.

The consumer must re-read the trusted GitHub run/artifact, match all fields
and fail closed for absent, pending, failed, expired or stale evidence. A
comment or arbitrary user-supplied artifact is not proof. No new authority,
parallel registry, broad reusable cache for identity/authorization, or direct
merge. Preserve required named checks and the Evolution Gate.

## Rollback

Revert this PR; all three original full-suite invocations remain available
in `main`. No database migration or stored authority requires rollback.
