# Hermes → ELO Discovery — 2026-09-25

## Scope

Discovery was limited to mechanisms already exposed/documented to ELO as Hermes extensions. No Hermes repository or runtime was modified and no business operation was executed. SO 001.26 was not used as an architectural reference.

## Current documented mechanisms

The ELO candidate registry exposes 15 Hermes mechanisms:

- EXT-CONTEXTREF-HERMES — context references — ELO Context
- EXT-CHECKPOINT-HERMES — checkpoints — ELO State Recovery
- EXT-HOOK-HERMES — event hooks — ELO Workflow/Automation
- EXT-ROUTE-HERMES — provider routing/fallback/credential pools — ELO Model/Tool Routing
- EXT-PROFILE-HERMES — profiles/Bot Mode — ELO Agent Context & Delegation
- EXT-BATCH-HERMES — batch processing — ELO Evaluation & Learning
- EXT-MEMPROVIDER-HERMES — external memory providers — ELO Memory
- EXT-LEARN-HERMES — skill learning / /learn — ELO Knowledge & Skills
- EXT-LEARNING-GRAPH-HERMES — learning graph / curator — ELO Evolution Memory
- EXT-CONTEXT-PLUGIN-HERMES — context engine plugins — ELO Context
- EXT-WORKTREE-HERMES — isolated git worktrees — ELO Forge
- EXT-MULTIAGENT-HERMES — subagent delegation / parallel workstreams — ELO Agent Delegation
- EXT-CRON-HERMES — scheduled agent tasks — ELO Workflow/Automation
- EXT-MCP-HERMES — external MCP capabilities — ELO External Capability Gateway
- EXT-TOOL-SEARCH-HERMES — progressive tool-schema disclosure / tool_search — ELO Model/Tool Routing

## Findings

The mechanisms fall into six families: state/recovery; routing/integration; agent execution; learning; memory/context; and automation.

The architectural signal is composability behind existing ELO owners, not creation of parallel authorities.

## Validated introduction

EXT-TOOL-SEARCH-HERMES has controlled evidence for task quality, repeatability (3/3), zero controlled regressions, and progressive schema representation reduction from 300 to 30 characters. It uses the existing ELO Model/Tool Routing owner and existing governance.

The 90% representation reduction is not treated as production token savings. Production maturity remains pending because the recorded ELO review requires a governed production runtime and real observation.

## Additional validated ELO evolution

The discovery process identified a generic execution requirement: an external Gate must not terminate the Symbiont loop.

Validated sequence:

WAITING_FOR_EXTERNAL_GATE -> PERCEIVE -> RECONCILE -> RESUME

Implementation sequence merged:

- #752 CRL checkpoint adapter
- #754 external Gate perception
- #755 resume existing loop after Gate perception
- #756 external Gate observation adapter
- #757 event-driven Gate perception

These changes reuse the existing Symbiont execution authority and add no scheduler, supervisor, memory authority, router, production authorization, promotion, or canonical mutation.

## Not promoted

The remaining Hermes mechanisms remain candidates pending their own evidence contracts. No observation was promoted automatically to Core, canonical knowledge, production maturity, or authority ownership.

## Evidence boundary

This is an ELO-side exposure registry, not a direct live inspection of a Hermes runtime. Therefore it does not claim that every listed mechanism is currently enabled or unchanged in Hermes.

A direct Hermes runtime/API inventory is still required to establish live availability, exact interfaces, metadata, versions, dependencies and current surfaces.

## Test and gate result

The event-driven Symbiont capability was covered by controlled tests. PR #757 passed ELO Maintenance Coordinator, Behavioral Validation, PR1 Validation, Baseline Evidence Gate, GitHub Pages and Evolution Gate. The Vercel status remained the known external deployment rate-limit failure and was not treated as a code/test failure.

## Pending review

1. Direct live Hermes inventory.
2. Candidate-specific evidence for the remaining mechanisms.
3. Production runtime evidence for EXT-TOOL-SEARCH-HERMES before maturity-7 promotion.
4. Any Core or promotion decision remains subject to Evolution Gate and human governance.
