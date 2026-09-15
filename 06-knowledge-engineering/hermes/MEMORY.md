# ELO — Hermes Knowledge Memory

```yaml
id: ELO-HERMES-MEMORY-001
name: Hermes Knowledge Intake Memory
type: reference
layer: knowledge
owner: ELO cognitive orchestrator
status: draft
authority: reference
version: 0.1
related:
  - docs/architecture/ELO_HERMES_CAPABILITY_SCAN_20260912.md
  - src/elo/agent_intake/hermes_knowledge_loop.py
depends_on:
  - ELO Evolution Gate
  - read-only Hermes capability evidence
```

## Purpose

This file is the persistent human-readable memory boundary for knowledge recovered from Hermes. It records mechanisms, provenance and validation state without granting Hermes authority over ELO.

## Current knowledge candidates

- **Tools/toolsets/elegibility** — candidate for an ELO capability-eligibility graph.
- **Skills** — candidate for governed procedural knowledge intake.
- **Memory + session search** — candidate for separating persistent memory from historical evidence.
- **Context files** — candidate for provenance, scope and precedence-aware context.
- **Delegation/subagents** — candidate for governed specialist decomposition.
- **Cron/automations** — candidate for scheduled missions with preconditions.
- **MCP/plugins** — candidate for governed external capability relationships.
- **Execution/checkpoints** — candidate for risk, reversibility and execution gates.

## Admission boundary

These observations remain `CANDIDATE` until the ELO implementation test, provenance test and Evolution Gate all pass. A Git commit or merge does not itself constitute cognitive promotion.

## Read-only discovery contract

The intake loop may consume a Hermes snapshot or other explicitly supplied evidence. It must not modify Hermes, execute business operations, expose provider secrets, or treat an external observation as an ELO rule.

## Learning transition

```text
HERMES EVIDENCE
  → DISCOVERY
  → CANDIDATE
  → IMPLEMENTATION TEST
  → PROVENANCE TEST
  → ELO EVOLUTION GATE
  → VALIDATED LEARNING
  → COGNITIVE MERGE
```

Only the final stages can promote knowledge into the canonical ELO learning system. Until then this file is reference memory, not canonical knowledge.
