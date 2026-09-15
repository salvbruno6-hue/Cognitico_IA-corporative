# ELO — Hermes Capability Evolution Loops

## Purpose

This design converts useful Hermes mechanisms into capabilities that belong to ELO itself. Hermes remains a read-only reference authority. No Hermes code is imported as a runtime dependency by these loops.

## Three governed loops

### 1. Discovery/Test Loop

`evidence → consistency evaluation → controlled test → adjustment → retest`

Rules:
- bounded iterations;
- source and revision provenance are immutable;
- mechanism identity is immutable;
- no business operation is executed;
- failure reasons are retained;
- a failed or exhausted candidate remains a candidate.

### 2. Transformation Loop

`validated evidence → native ELO design → function | structure | skill → native contract test → variant → retest`

The transformation must produce an ELO-native capability rather than a hidden Hermes dependency. The capability retains source/revision/evidence references for traceability.

### 3. Approval-Readiness Loop

`native candidate → implementation check + consistency + provenance + governance metadata + Evolution Gate → ready/not ready`

This loop does **not** approve, merge, or promote. It only determines whether the candidate is complete enough to enter the Evolution Gate decision.

## Capability destinations

| Hermes mechanism | Preferred ELO destination |
|---|---|
| Memory | cognitive memory structure + functions |
| Skills | native ELO Skills |
| Toolsets | capability/tool registry + orchestration functions |
| Hierarchical Context | context engine functions + context structures |
| Delegation/Subagents | governed ELO worker/delegation functions |
| Automations/Cron | scheduler/watch functions |
| MCP/Plugins | external capability gateway functions + registry |
| Checkpoints/Execution | execution state/checkpoint structures + recovery functions |

## State model

`DISCOVERED → TESTING → INCONSISTENT → TRANSFORMING → TRANSFORMED → READY_FOR_APPROVAL`

`CANDIDATE` is the safe holding state whenever a loop fails, exhausts its bound, or lacks a required gate.

## Green criterion

A capability is green only when the ELO-native implementation has passed its controlled functional test, consistency is established, provenance is intact, governance metadata is complete, and the Evolution Gate is explicitly approved. Git merge remains separate from cognitive promotion.
