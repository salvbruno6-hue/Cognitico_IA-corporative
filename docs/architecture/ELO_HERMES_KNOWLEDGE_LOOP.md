# ELO — Hermes Knowledge Learning Loop

```yaml
id: ELO-HERMES-LOOP-001
name: Governed Hermes Knowledge Learning Loop
type: implementation
layer: cognitive
owner: ELO cognitive orchestrator
status: implemented
authority: implementation
version: 0.1
related:
  - docs/architecture/ELO_HERMES_CAPABILITY_SCAN_20260912.md
  - 06-knowledge-engineering/hermes/MEMORY.md
  - src/elo/agent_intake/hermes_knowledge_loop.py
depends_on:
  - read-only Hermes evidence
  - ELO Evolution Gate
```

## Objective

Create a controlled path for ELO to recover knowledge about Hermes mechanisms without changing Hermes and without executing business operations.

## Operating loop

```text
HERMES READ-ONLY EVIDENCE
        ↓
SNAPSHOT
        ↓
DISCOVER MECHANISMS
        ↓
NORMALIZE METADATA / DEPENDENCIES / RELATIONS
        ↓
CREATE LEARNING CANDIDATE
        ↓
PRESERVE PROVENANCE
        ↓
IMPLEMENTATION TEST
        ↓
PROVENANCE TEST
        ↓
ELO EVOLUTION GATE
        ↓
VALIDATED LEARNING
        ↓
COGNITIVE MERGE
```

Git commit/PR/merge is a separate software-delivery path and never substitutes for Cognitive Merge.

## Current Hermes intake scope

The first governed catalogue covers:

1. toolsets and capability eligibility;
2. Skills;
3. persistent memory and session search;
4. hierarchical context files;
5. delegation/subagents;
6. cron/automations;
7. MCP/plugins;
8. execution/checkpoints.

These are candidates derived from the Hermes evidence scan. They are not ELO rules merely because Hermes implements them.

## Safety boundaries

- The loop accepts an explicitly supplied Hermes snapshot/evidence source.
- The loop does not invoke Hermes.
- The loop does not modify Hermes.
- The loop does not execute business operations.
- External mechanisms remain reference evidence until the ELO gates pass.
- Provenance is mandatory for promotion.
- Failed gates retain `candidate` status.
- Only candidates already marked `validated` can be returned by `promote()`.

## Memory boundary

`06-knowledge-engineering/hermes/MEMORY.md` is reference memory for the intake process. It records what was recovered, where it came from and its validation state. It is not the canonical ELO knowledge store.

## Re-entry behavior

When Hermes changes, ELO should repeat the loop from the beginning with a new source revision. A changed revision creates new evidence; it does not silently overwrite previously validated knowledge.

## Stop conditions

Stop before promotion when:

- source or revision provenance is missing;
- mechanism identifiers are duplicated;
- implementation tests fail;
- provenance tests fail;
- Evolution Gate is not approved;
- a conflict with a higher-authority ELO contract is detected;
- the proposed change requires a new persistent model without an approved contract.
