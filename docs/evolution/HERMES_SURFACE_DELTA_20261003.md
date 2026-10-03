# Hermes Surface Delta → ELO — 2026-10-03

## Scope

This document records current Hermes mechanisms observed from its public surface and maps them to existing ELO owners. It is a discovery artifact, not an authorization or production-integration record.

Hermes is not modified by this change. No business operation, external connector, MCP server, memory provider, scheduler, webhook, or agent execution is invoked.

## Candidate introductions

| Mechanism | ELO owner | Candidate introduction |
|---|---|---|
| Webhook guard | ELO Workflow/Automation | Authenticated event intake with filters, idempotency and bounded toolsets; authenticated payload remains untrusted business content. |
| Tool-loop guardrails | ELO Model/Tool Routing | Detect repeated failed/non-progressing tool calls and expose a bounded safety signal. |
| Code kernel | ELO Model/Tool Routing | Treat session-scoped programmatic execution as a bounded runtime contract with idle/LRU and per-cell authority constraints. |
| Dynamic MCP discovery | ELO External Capability Gateway | Detect runtime capability changes without treating newly registered tools as authorized. |
| MCP sampling | ELO External Capability Gateway | Treat server-requested inference as bounded external delegation with model/token/time/rate/tool-round controls. |
| Delegation controls | ELO Agent Delegation | Preserve explicit concurrency, depth, isolation and heartbeat metadata for delegated work. |
| Webhook coalescing | ELO Workflow/Automation | Convert event bursts into bounded scheduling signals while preserving idempotency and at-most-once semantics. |
| Skill lifecycle | ELO Knowledge & Skills | Preserve source, update and snapshot provenance before governed skill admission. |
| Session lineage | ELO Context | Treat session lineage and historical search as provenance/context, not learning or canonical memory. |
| Profile isolation | ELO Agent Context & Delegation | Preserve configuration/credential/memory/session/skill/cron isolation without authority transfer. |

## Validation classification

All ten entries are CANDIDATE_ONLY.

They are not:

- production outcomes;
- implementation authorization;
- canonical memory;
- new authority;
- a new Evolution Gate;
- autonomous promotion;
- business execution.

## Existing ELO integrations confirmed separately

The current main already contains governed runtime bridges for:

- EXT-CRON-HERMES via the canonical workflow runtime;
- EXT-PROFILE-HERMES via the canonical AgentOrchestrator;
- EXT-CONTEXT-PLUGIN-HERMES via the canonical ExecutionBoundary;
- EXT-WORKTREE-HERMES via the canonical ExecutionBoundary;
- EXT-MULTIAGENT-HERMES through the existing AgentOrchestrator delegation path;
- EXT-TOOL-SEARCH-HERMES through the existing ExecutionRouter runtime-evidence path.

These are existing implementation surfaces. This discovery does not recreate them.

## Controlled validation

The accompanying test module validates registry completeness, uniqueness, candidate-only state, owner reuse and authority boundaries. It does not invoke Hermes or any external business system.

Passing these tests validates the ELO-side discovery representation only. It does not prove runtime or production behavior.

## Sources

The current Hermes public surface documents tool-search progressive disclosure, dynamic MCP registration/sampling, webhook authentication/filtering/idempotency/rate limits, delegated execution controls, persistent code-execution kernels, skills lifecycle and isolated profiles. These observations were used only to construct candidate introductions; they were not treated as ELO architectural authority.