# ELO — Hermes Discovery Audit — 2026-09-16

## Scope

This audit inspects the current Hermes reference surface without modifying Hermes and without executing business operations. The architectural reference snapshot is Hermes commit `45ac26a217cc93603d19db8e4b9b064ca57d6806`, plus the current Hermes `main` state at the audit date.

`SO 001.26` is not used as an architectural reference.

## Discovery results

### 1. Architectural evolution scanner

Hermes now exposes an architectural evolution pipeline that separates read-only host scanning from artifact generation and validation. The scanner records mechanisms, interfaces, metadata and declared relations; the planner builds an ELO-owned projection; generated documentation/code/tests remain reviewable artifacts and are not silently written to the repository.

**ELO disposition:** reuse the concept inside Forge/Symbiont governance, not as a new authority. The ELO implementation must remain the canonical owner of its architecture model.

**State:** candidate refinement; not promoted from Hermes.

### 2. Micro-compaction / rolling context retention

Hermes exposes rolling per-exchange context compaction with cursor recovery, summary rehydration, defragmentation, failure tracking, telemetry and database synchronization. The implementation explicitly protects user turns and avoids absorbing incomplete turns. It also treats failed summarization as retryable rather than accepting partial summaries.

**ELO disposition:** this is an enhancement of the existing `HERMES-CONTEXT` / `HERMES-MEMORY` candidates, not a ninth capability. ELO already contains a deterministic retention laboratory that evaluates continuity, repeatability, regression and tenant scope without persistence or promotion.

**State:** controlled ELO refinement validated; production semantic summarization not introduced.

### 3. Explicit learning and Symbiont evolution pipeline

Hermes contains an explicit ELO Symbiont evolution path that scans host mechanisms, associates them with ELO-owned capabilities, and keeps architectural observations separate from learning promotion. The recent implementation also records architecture artifacts and validation without granting host mutation authority.

**ELO disposition:** confirms the existing ELO Symbiont contract and reinforces the rule that external mechanisms are experience/reference surfaces. No competing Memory, Router, Evolution Gate or Core authority is introduced.

**State:** validated as architectural reference; no new ELO authority created.

### 4. Frontend lab changes

Recent Hermes commits created and then reverted a temporary frontend lab marker. No persistent architectural capability was established by those changes.

**ELO disposition:** no candidate.

## Candidate map

| Mechanism | ELO owner | Classification | Controlled proof | Promotion |
|---|---|---|---|---|
| Memory | ELO Cognitive Memory | Existing candidate `HERMES-MEMORY` | Passed native deterministic probe | Candidate-only |
| Skills | ELO Native Skills Registry | Existing candidate `HERMES-SKILLS` | Passed native deterministic probe | Candidate-only |
| Toolsets | ELO Capability/Tool Registry | Existing candidate `HERMES-TOOLSETS` | Passed native deterministic probe | Candidate-only |
| Hierarchical Context | ELO Context Engine | Existing candidate `HERMES-CONTEXT` | Native probe + retention lab passed; context assembly CI passed | Candidate-only / review pending |
| Delegation/Subagents | ELO Worker/Delegation Engine | Existing candidate `HERMES-DELEGATION` | Passed native deterministic probe | Candidate-only |
| Automations/Cron | ELO Scheduler/Watchers | Existing candidate `HERMES-AUTOMATION` | Passed native deterministic probe | Candidate-only |
| MCP/Plugins | ELO External Capability Gateway | Existing candidate `HERMES-MCP` | Passed native deterministic probe | Candidate-only |
| Checkpoints/Execution | ELO State Recovery Engine | Existing candidate `HERMES-CHECKPOINT` | Passed native deterministic probe | Candidate-only |
| Micro-compaction | Context + Memory | Refinement, not new candidate | Deterministic retention laboratory passed | Not promoted to production summarizer |
| Architecture evolution scanner | Forge/Symbiont governance | Refinement, not new authority | Read-only architecture reference | Not promoted |

## Validation evidence

The eight native capability probes are deterministic and side-effect free. They verify successful controlled behavior, evidence production, tenant state isolation and the absence of canonical mutation/promotion. The ELO native test suite asserts all eight complete successfully and remain `candidate_only`.

The Supabase memory adapter initially exposed a scope-test regression on the current context-assembly branch. The test was corrected to enforce explicit scope matching. The subsequent CI run completed successfully with 5 tests passing.

The new Context Assembly workflow then completed successfully for the current branch commit. It executes the context-assembly and Supabase memory adapter test suites together; no external service or business operation is invoked.

The ELO retention laboratory already covers the core safety properties inspired by Hermes micro-compaction: tenant scope, continuity, repeatability, regression detection and candidate-only governance. It intentionally does not claim Hermes-specific LLM summarization or production database synchronization.

## Governance decision

No Hermes code was modified.

No business operation was executed.

No external observation was promoted to Core or canonical learning.

No ninth capability was created for micro-compaction because the mechanism is structurally an improvement to existing Context/Memory ownership.

No new universal learning database was created.

The current Context Assembly implementation is technically validated by CI but remains in a draft PR and therefore is not represented as merged canonical architecture.

## Pending review

1. Review/merge PR #547 only after repository governance review; CI is green but the PR remains draft.
2. Resolve the remaining scope-model gap: records without an explicit scope are currently tolerated by the read-only adapter and require a future uniform scope contract before stronger tenant isolation can be claimed.
3. Validate the first Orçamento context pilot against the real Supabase schema before adding further domain adapters.
4. Evaluate micro-compaction only as a provider-neutral context-retention refinement; do not import Hermes-specific LLM/database behavior blindly.
5. Run Evolution Gate for the eight candidates before any promotion beyond candidate-only state.
6. Treat `public.taxonomia_modulos_reparo` RLS remediation as a separate security task; do not conflate it with cognitive evolution.
