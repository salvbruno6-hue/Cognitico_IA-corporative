# Hermes Tool Search → ELO refinement candidate

## Source evidence

Hermes currently exposes an opt-in progressive-disclosure layer for MCP/plugin tools and selected deferred built-ins. Instead of placing every deferred tool schema in the model-visible tool array, Hermes can expose a bounded catalog/bridge and load an individual schema on demand. Current documentation exposes controls for enablement, listing budget, default/max search limits, catalog listing, and a curated defer list.

## Candidate

`EXT-TOOL-SEARCH-HERMES`

**Existing ELO owner:** `ELO Model/Tool Routing`.

**Proposed introduction:** represent progressive tool-schema disclosure as candidate evidence for reducing context/schema overhead while preserving explicit tool discovery boundaries.

## Why this is not a new authority

- no Hermes tool is invoked by the adapter;
- no tool is enabled or disabled by the adapter;
- no MCP/plugin registry is copied into ELO;
- no second router or policy engine is created;
- no memory or Core mutation occurs;
- `candidate_only=true` and `canonical_mutation=false` remain mandatory.

## Controlled acceptance criteria

1. metadata normalization is deterministic;
2. duplicate deferred tools are rejected;
3. invalid search limits are rejected;
4. provenance/source revision is preserved;
5. the candidate reuses the existing routing owner;
6. controlled measurement demonstrates a repeatable reduction in schema/context overhead without task-quality regression;
7. Evolution Gate approval is obtained before any production introduction.

The implementation establishes the candidate boundary and deterministic tests only. It does not claim measured gain or production validity.

## Deliberately not introduced

Hermes Codex App-Server Runtime remains outside this candidate because ELO already has governed runtime/MCP boundaries. It should only be introduced if a distinct measurable ELO gain is demonstrated that cannot be expressed as a refinement of the existing runtime boundary.

## Governance state

`CANDIDATE → CONTROLLED TEST → MEASURED GAIN → REPEATABLE → EVOLUTION GATE → ELO REVIEW → IMPLEMENTATION`

GitHub remains the operational authority. Cognitive promotion remains separate from code merge.
