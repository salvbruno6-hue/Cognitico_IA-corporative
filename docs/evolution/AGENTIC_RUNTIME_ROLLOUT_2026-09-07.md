# ELO Agentic Runtime Rollout — 2026-09-07

## Status

Experimental implementation remains isolated from `main` on branch
`feat/elo-agentic-knowledge-orchestrator-20260907`.

## Runtime boundary

LangGraph/LangChain are optional orchestration dependencies. Canonical ELO
contracts remain framework-neutral. The runtime only consumes read-oriented
ELO capabilities and returns a bounded `KnowledgeContext`.

## Canonical pipeline

```text
Specialist request
  -> GPT intent interpretation
  -> IntentSpec
  -> KnowledgeNeedPlanner
  -> ELO ContextResolution
  -> ELO SourceDiscovery
  -> ELO SourceResolver
  -> applicability / authority / provenance curation
  -> gaps / conflicts
  -> grounded KnowledgeContext
  -> GPT specialist-facing response
```

## Hard boundaries

The agentic runtime MUST NOT:

- mutate Soul, Core or Forge;
- promote canonical knowledge;
- perform learning promotion;
- make authorization decisions;
- write canonical Supabase state;
- depend on provider-specific retrieval APIs from canonical modules.

## Safety constraints

- read-only runtime policy is enforced at graph construction;
- graph state is typed and bounded;
- maximum graph steps are configurable and must be positive;
- optional framework imports stay outside framework-neutral contracts;
- current-context evidence has precedence over historical/reference evidence;
- missing required information remains a gap;
- conflicting evidence remains a conflict;
- provenance is retained.

## Database policy

No new Supabase schema object is required for this rollout stage. Production
Supabase remains unchanged while the agentic runtime is validated in GitHub.

## Exit criteria for main

1. Full agentic test suite passes.
2. Existing ELO regression suite passes.
3. No canonical-module imports of LangGraph/LangChain.
4. No writes to Supabase from the agentic runtime.
5. Contextuality and cross-SO contamination tests pass.
6. Provenance/gap/conflict behavior is deterministic.
7. A reviewed PR explicitly confirms the frozen-boundary contract.
