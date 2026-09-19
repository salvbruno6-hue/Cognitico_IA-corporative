# ELO — Hermes Current Mechanisms Discovery 2026-09-19

**Status:** EVOLUTION LAB / CANDIDATE-ONLY  
**Source:** Hermes Agent public documentation, observed 2026-09-19  
**Authority:** ELO Cognitivo / Evolution_Gate  
**Constraint:** discovery only; no Hermes modification and no business operation.

## Purpose

Record newly exposed Hermes mechanisms that are not yet represented as validated ELO extensions. Each candidate must extend an existing ELO owner; none may create a parallel authority.

## Validated source observations

Hermes currently documents context references, checkpoints, event hooks, programmatic code execution, provider routing/fallback, credential pools, prompt caching, profiles/bot mode, batch processing and pluggable external memory providers. These observations come from Hermes documentation and are treated as source evidence, not ELO authority.

## Candidate introductions

| ID | Hermes mechanism | Existing ELO owner | Candidate introduction | Validation state |
|---|---|---|---|---|
| `EXT-CONTEXTREF-HERMES` | `@` context references for files/folders/diffs/URLs | ELO Context | governed context-reference resolution with provenance and size/policy bounds | CANDIDATE-ONLY |
| `EXT-CHECKPOINT-HERMES` | working-directory checkpoints and rollback | ELO State Recovery | pre-mutation checkpoint contract for controlled technical changes | CANDIDATE-ONLY |
| `EXT-HOOK-HERMES` | lifecycle gateway/plugin hooks | ELO Workflow/Automation | provider-neutral lifecycle interception for evidence, metrics and guardrails | CANDIDATE-ONLY |
| `EXT-ROUTE-HERMES` | provider routing, fallback and credential pools | ELO Model/Tool Routing | policy-based provider selection and bounded failover without changing authority | CANDIDATE-ONLY |
| `EXT-PROFILE-HERMES` | isolated profiles / Bot Mode | ELO Agent Context & Delegation | isolated agent-context profiles with explicit identity, memory and skill scope | CANDIDATE-ONLY |
| `EXT-BATCH-HERMES` | batch processing / trajectory generation | ELO Evaluation & Learning | bounded batch evaluation intake with provenance and no automatic promotion | CANDIDATE-ONLY |
| `EXT-MEMPROVIDER-HERMES` | pluggable external memory providers | ELO Memory | provider adapter contract only; Supabase remains the cognitive persistence authority | CANDIDATE-ONLY |

## Acceptance contract

A candidate can become valid only after:

`source evidence → existing owner mapping → bounded adaptation → controlled test → measured gain → no regression → repeatability → Evolution_Gate`

The source mechanism itself is never sufficient evidence of promotion.

## Explicit exclusions

- No new Core, Memory Authority, Skill Registry, Tool Registry, Context Engine, Scheduler, MCP Authority, or State Authority.
- No direct Hermes mutation.
- No business execution.
- No use of SO 001.26 as architectural reference.
- External memory providers are adapters only; they cannot become ELO cognitive authority.

## Source evidence

- Hermes Features Overview: https://hermes-agent.nousresearch.com/docs/user-guide/features/overview
- Hermes Tools & Toolsets: https://hermes-agent.nousresearch.com/docs/user-guide/features/tools
- Hermes documentation index: https://hermes-agent.nousresearch.com/docs/

## Decision

The mechanisms above are **new discovery candidates**, not validated ELO capabilities. This run does not promote them. Existing Hermes/OpenClaw extensions remain governed by `ELO_EXTENDED_CAPABILITIES_HERMES_OPENCLAW.md` and its Evolution Gate.
