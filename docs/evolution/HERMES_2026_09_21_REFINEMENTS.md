# Hermes 0.21.4 → ELO refinement candidates

## Source evidence

Hermes Agent `v0.21.4` was released on 2026-09-21 at tag `d337b73`. The release notes expose, among other changes, `skills.auto_load` pinning skills into new sessions and `session_search` after/before bounds plus an OR-relaxed recall retry. This document records only ELO-side observation contracts; it does not modify Hermes.

## Candidate 1 — EXT-SKILL-AUTOLOAD-HERMES

**Existing owner:** ELO Skills / governed skill approval loop.

**Observation:** Hermes can pin configured skills into every new session prompt.

**ELO introduction:** capture the metadata as candidate evidence and evaluate whether deterministic skill-context continuity improves a measurable ELO workflow without bypassing approval, capability selection or context governance.

**Boundary:** no skill is activated by the intake contract; no skill registry or second approval authority is created; canonical mutation remains false.

**Acceptance:** implementation tests pass, provenance is intact, measurable integration gain is demonstrated, and Evolution Gate approval exists.

## Candidate 2 — EXT-SESSION-SEARCH-BOUNDS-HERMES

**Existing owner:** ELO context/memory retrieval boundary.

**Observation:** Hermes session search exposes temporal `after`/`before` bounds and an OR-relaxed recall retry.

**ELO introduction:** represent these controls as bounded retrieval evidence. The ELO adapter must preserve query and temporal bounds and treat relaxed recall as an explicit retry mode, never as an unbounded search or memory mutation.

**Boundary:** no direct Hermes call, no canonical memory write, no second retrieval authority.

**Acceptance:** implementation tests pass, bounds are validated, provenance remains intact, and measurable retrieval-quality or latency gain is demonstrated before any promotion review.

## Related release surfaces deliberately not promoted

- gateway singleton lock: infrastructure reliability, not a cognitive capability;
- `stream-json`: transport/output format;
- MCP discovery concurrency cap: infrastructure control;
- unauthorized-DM `decline`: security/runtime behavior;
- connector setup card: UI/runtime integration;
- Desktop font/update/plugin UI: presentation/operations;
- LTX/Kling catalogs: provider catalog expansion.

These may be revisited only if an ELO owner and measurable cognitive/operational gain are identified.

## Governance

`DISCOVERY → CANDIDATE → CONTROLLED TEST → MEASURED GAIN → REPEATABLE → EVOLUTION GATE → ELO REVIEW → IMPLEMENTATION DECISION`.

No observation is promoted to Core from this document. Git merge is separate from cognitive promotion. Hermes remains unchanged. SO 001.26 is not an architectural reference.
