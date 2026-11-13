# PERF-01 — CI evidence reuse: first governed reduction

Status: **Phase A candidate / current-head revalidation required after concurrency refinement**  
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

## Phase A follow-up — avoid obsolete PR check work (13 Nov 2026)

The existing `ELO PR1 Validation` and `ELO Behavioral Validation`
workflows now use per-workflow/per-PR GitHub Actions concurrency with
`cancel-in-progress` **only for `pull_request`** events. A new PR revision
supersedes an in-flight run of that same workflow for the same PR. Main/feature
push checks keep `cancel-in-progress=false` and use the commit SHA as their
group identity; independent workflow names remain distinct.

This **does not** reuse, alter, or approve an old run; cancellation is
explicitly non-success. The current head still needs all required CI, two
full-suite gates, and the original ELO Evolution/Governance/authorization
checks. No cancel policy is added to the Evolution Gate, Agent Loop,
Maintenance, or Merge Coordinator, which may publish governed evidence.

### Measured GitHub workflow timing — baseline samples only

Using real GitHub Actions metadata
(`updated_at - run_started_at`, approximate workflow wall-clock elapsed,
**not** billable runner minutes or Python test time):

| Head | PR1 | Behavioral | Evolution | Maintenance |
|---|---:|---:|---:|---:|
| PR #1210 `a3a78b1e` | 27 s | 26 s | 65 s | 18 s (later label run) |
| PR #1177 `c5262e99` | 35 s | 34 s | 80 s | Not a comparable PR-head run |

These are **two observational snapshots across different changes**, so
neither percent improvements nor causal speedups are claimed. The longest
measured required workflow was Evolution, which must keep full-suite,
Symbiont, Hermes, security and handoff gates intact. The new concurrency
change targets wasted runner/queue work on superseded PR commits; it does
not claim to shorten an individual latest-head run. Track at least three
comparable revisions including canceled/queued runs before claiming gains.
