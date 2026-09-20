# ELO — Hermes Current Mechanisms Discovery 2026-09-20

**Status:** EVOLUTION LAB / CANDIDATE-ONLY  
**Source:** Hermes Agent public documentation, observed 2026-09-20  
**Authority:** ELO Cognitivo / Evolution_Gate  
**Constraint:** discovery and candidate registration only; no Hermes modification and no business operation.

## Purpose

Expand the Hermes-to-ELO candidate registry with mechanisms currently exposed by Hermes that are not yet validated as ELO capabilities. Every candidate must map to an existing ELO owner and remain non-authoritative until controlled validation.

## Newly observed mechanisms

Current Hermes documentation exposes or documents:

- context references and extensible context-reference providers;
- filesystem checkpoints and rollback;
- lifecycle hooks;
- provider/model routing and credential pools;
- isolated profiles/Bot Mode;
- batch trajectory generation;
- external memory providers;
- `/learn` skill learning and curator/learning-graph concepts;
- pluggable context engines;
- git worktree isolation;
- subagent delegation and parallel workstreams;
- cron/scheduled agent tasks.

These are source observations, not ELO authority. Hermes remains unmodified.

## Candidate introductions

| ID | Hermes mechanism | Existing ELO owner | Candidate introduction | State |
|---|---|---|---|---|
| EXT-CONTEXTREF-HERMES | context references | ELO Context | provenance-bounded reference resolution | CANDIDATE-ONLY |
| EXT-CHECKPOINT-HERMES | checkpoints/rollback | ELO State Recovery | pre-mutation checkpoint contract | CANDIDATE-ONLY |
| EXT-HOOK-HERMES | lifecycle hooks | ELO Workflow/Automation | evidence/metric/guardrail lifecycle hooks | CANDIDATE-ONLY |
| EXT-ROUTE-HERMES | routing/fallback/credential pools | ELO Model/Tool Routing | policy-bounded failover | CANDIDATE-ONLY |
| EXT-PROFILE-HERMES | profiles/Bot Mode | ELO Agent Context & Delegation | isolated agent-context profiles | CANDIDATE-ONLY |
| EXT-BATCH-HERMES | batch processing | ELO Evaluation & Learning | bounded evaluation intake | CANDIDATE-ONLY |
| EXT-MEMPROVIDER-HERMES | external memory providers | ELO Memory | adapter-only memory providers | CANDIDATE-ONLY |
| EXT-LEARN-HERMES | /learn / skill learning | ELO Knowledge & Skills | governed skill synthesis/admission | CANDIDATE-ONLY |
| EXT-LEARNING-GRAPH-HERMES | learning graph/curator | ELO Evolution Memory | evidence-linked learning relations | CANDIDATE-ONLY |
| EXT-CONTEXT-PLUGIN-HERMES | context engine plugins | ELO Context | bounded context-engine adapter | CANDIDATE-ONLY |
| EXT-WORKTREE-HERMES | isolated git worktrees | ELO Forge | isolated technical workspace | CANDIDATE-ONLY |
| EXT-MULTIAGENT-HERMES | subagent delegation | ELO Agent Delegation | bounded parallel/delegated execution | CANDIDATE-ONLY |
| EXT-CRON-HERMES | scheduled agent tasks | ELO Workflow/Automation | governed deterministic scheduling | CANDIDATE-ONLY |

## Validation boundary

A candidate becomes valid only after:

`source evidence → owner mapping → bounded adaptation → controlled test → measured gain → no regression → repeatability → Evolution Gate`

Registration in this file is not validation and does not activate a runtime capability.

## Governance

- No Hermes source is modified.
- No business operation is executed.
- No SO 001.26 is used as architectural evidence.
- No candidate creates a second Core, Memory authority, Context authority, Tool registry, Scheduler authority, or Forge authority.
- External memory providers remain adapters; Supabase remains the cognitive persistence member.
- Git worktrees remain Forge isolation mechanisms and do not become an independent merge authority.
- Cron remains an execution adapter; scheduling cannot bypass ELO governance.
- Multi-agent execution cannot transfer cognitive or merge authority.

## Source evidence

- Hermes Features Overview: https://hermes-agent.nousresearch.com/docs/user-guide/features/overview
- Hermes Plugins: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
- Hermes Memory Providers: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
- Hermes Memory Provider Plugin contract: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/memory-provider-plugin.md
- Hermes Gateway Internals: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/gateway-internals.md
- Hermes Cron Internals: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/cron-internals.md

## Decision

All thirteen mechanisms remain CANDIDATE-ONLY. The registry is evidence capture and experiment planning; it is not a promotion event.
