# EXT-TOOL-SEARCH-HERMES — Controlled Observation

## Purpose

This stage exercises the already-authorized EXT-TOOL-SEARCH-HERMES
implementation through the existing ExecutionRouter authority and records
runtime-shaped observations without executing a selected tool.

## Boundary

- candidate: EXT-TOOL-SEARCH-HERMES
- owner: ELO Model/Tool Routing
- authority reused: ExecutionRouter
- observation adapter: src/elo/agent_intake/hermes_tool_search_observation.py
- canonical mutation: false
- tool execution: false
- automatic Core promotion: false
- environment: CONTROLLED_OBSERVATION

No new router, registry, memory authority, Evolution Gate, or promotion
authority is introduced.

## Evidence captured

Each observation records:

1. selected tools;
2. disclosed schema count;
3. representation footprint;
4. bounded selection;
5. non-executing status;
6. canonical-mutation status;
7. environment classification.

The observation is deliberately distinguishable from production evidence.
production_evidence remains false unless an explicitly governed production
deployment records a production observation.

## Governance interpretation

This stage closes the instrumentation gap between implementation and an
operational observation contract. It does not raise ELO-CAP-COG-018 to
maturity level 7 and does not authorize Core promotion.

The next valid evidence transition is:

IMPLEMENTED → VALIDATED → OBSERVING → PRODUCTION EVIDENCE → EVOLUTION GATE

Production evidence must come from a governed deployed runtime, not from this
controlled test.
