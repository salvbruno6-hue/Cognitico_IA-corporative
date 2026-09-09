# ELO Agentic Knowledge Orchestrator — Boundary Contract

## Purpose

Provide a natural-language bridge between specialist requests and governed ELO knowledge retrieval without requiring the specialist to know ELO internal tables, identifiers, paths or retrieval mechanics.

## Canonical flow

```text
SPECIALIST
  -> GPT interpretation
  -> IntentSpec
  -> KnowledgeNeedPlanner
  -> existing ELO context/source resolution
  -> governed retrieval
  -> applicability/authority/context curation
  -> gaps/conflicts
  -> grounded KnowledgeContext
  -> GPT response
  -> SPECIALIST
```

## Frozen ELO boundary

This layer is an adapter/orchestrator only. It MUST NOT become an authority for:

- Soul or identity;
- Core canonical governance;
- Forge canonical ownership;
- canonical knowledge promotion;
- learning promotion;
- persistence of canonical knowledge;
- authorization decisions;
- direct Supabase schema mutation.

The existing ELO `ContextResolutionEngine`, `SourceDiscoveryEngine`, `SourceResolver`, Knowledge Engineering and governed authorization boundaries remain authoritative.

## Framework isolation

LangGraph/LangChain MAY be introduced as runtime orchestration dependencies, but canonical ELO contracts MUST remain framework-neutral. No canonical ELO module may depend on LangGraph/LangChain solely to preserve portability.

## Retrieval policy

The orchestrator must prioritize current-context evidence before historical/reference evidence. Similarity alone does not establish applicability. Missing required information creates a gap; conflicting evidence creates a conflict; neither may be silently converted into fact.

## Read-only first

The initial implementation uses existing ELO sources as read/query capabilities. No new Supabase table is required by this contract.

## Acceptance gates

1. Specialist can ask in natural language without ELO identifiers.
2. Active SO/project context is carried into retrieval.
3. Internal source structure is hidden from the specialist.
4. Provenance is preserved.
5. Historical/reference material cannot silently replace current-context evidence.
6. Gaps and conflicts are explicit.
7. Agentic runtime can be removed without changing canonical ELO contracts.
8. No Core/Soul/Forge mutation occurs.
9. Supabase schema remains unchanged unless a later, separately approved migration proves necessary.
