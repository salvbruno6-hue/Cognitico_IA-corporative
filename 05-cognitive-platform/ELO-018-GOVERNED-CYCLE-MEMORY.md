# ELO-018 — Governed Cycle Memory

## Purpose
Define the governed memory contract for sequential Multiteiner operational cycles without creating a second Core, memory engine, or Orchestrator.

## Memory planes

1. **Cycle Memory** — immutable operational history: cycle id, correlation, prior state, observations, evidence, provenance, specialists, decisions, authority, actions, resulting state and outcomes.
2. **Context Memory** — derived operational state required by the next cycle. It is a projection, not a replacement for historical records.
3. **Experience / Learning Candidates** — observations and outcomes awaiting validation; they are not canonical knowledge.
4. **Faculty** — validated, reusable mechanics that have evidence of generality.
5. **Overlay** — contextual or tenant-specific mechanics that can be removed without changing the faculty.
6. **Gap** — insufficient evidence or missing knowledge.
7. **Conflict** — incompatible knowledge or evidence requiring resolution.

## Governance invariants

- Historical cycle records are not silently rewritten when knowledge evolves.
- Context is derived from governed history and must retain correlation to its source cycles.
- A single cycle cannot promote a hypothesis directly to canonical faculty.
- Provenance, tenant, principal, authority and correlation remain attached to promoted knowledge.
- Removing a specialist does not remove already validated ELO knowledge.
- Removing or invalidating an overlay cannot corrupt historical cycle memory or canonical faculty.
- Conflict remains explicit until resolved; it is never silently overwritten.
- Memory writes occur through the existing ELO orchestration/governance contracts.
- No new Core, parallel memory authority, parallel Orchestrator, or organizational seed is introduced.

## Sequential contract

```text
C1 → outcome → governed memory
              ↓
          relevant context
              ↓
C2 → compare(C1,C2) → decision → outcome
              ↓
C3 → causal comparison → learning candidate
              ↓
       faculty / overlay / gap / conflict
```

## Required evidence

Each cycle record must preserve: `cycle_id`, `correlation_id`, `tenant_id`, `state_before`, `observations`, `evidence`, `provenance`, `specialists`, `decision`, `authority`, `action`, `state_after`, `outcome`, and `learning_status`.

## Promotion rule

Operational memory is retained first. Learning is evaluated separately. Only validated learning may become faculty; context-specific learning becomes overlay; insufficient evidence remains gap; incompatible evidence remains conflict.
