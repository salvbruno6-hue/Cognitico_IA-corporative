# ELO-003 — Governed Agent Ecosystem — Final Baseline

## Purpose

ELO-003 establishes the governed agent layer around the existing ELO Cognitive Core. Agents are specialists, not replacement cores.

## Canonical flow

```text
ELO
 ↓
AgentTask
 ↓
AgentRegistry
 ↓
Capability + Policy
 ↓
ToolRegistry
 ↓
Autonomy Gate
 ↓
Execution Boundary
 ↓
AgentObservation
 ↓
Evidence / Knowledge / Memory
 ↓
ELO Cognitive Core
```

## Contracts

### Agent

- identity and version;
- tenant scope;
- domain;
- capabilities;
- tools;
- policy profile;
- autonomy level;
- status;
- provenance.

### Task

- task identity;
- agent identity;
- tenant/domain;
- objective;
- context/evidence references;
- constraints;
- allowed tools;
- required output;
- time budget;
- policy.

### Observation

- observation identity;
- agent identity;
- tenant/domain;
- subject;
- observation;
- evidence references;
- confidence;
- questions;
- provenance.

## Autonomy

| Level | Capability | Default execution rule |
|---|---|---|
| L0 | Observe | no action |
| L1 | Analyze | no action |
| L2 | Recommend | no action |
| L3 | Approval | requires approval |
| L4 | Policy-bounded | only explicitly permitted actions |
| L5 | Governed autonomy | autonomous only inside explicit policy |

Autonomy is never inferred from the agent name, prompt or model output.

## Tool governance

A tool must have:

- unique ID;
- capability;
- domain;
- tenant scope;
- enabled status;
- explicit authorization.

The orchestrator must reject:

- unknown tools;
- disabled tools;
- capability mismatch;
- domain mismatch;
- tenant mismatch;
- execution beyond autonomy level.

## Isolation

The following are mandatory boundaries:

```text
Tenant A ≠ Tenant B
Domain A ≠ Domain B unless policy permits
Agent A ≠ Agent B
Observation identity must match task identity
```

## Evidence rule

An agent observation is not automatically verified knowledge.

```text
Agent output
 ↓
Observation
 ↓
Evidence
 ↓
Validation
 ↓
Knowledge status
```

## Legacy reconciliation

Historical agents under the old `ELO/agents/` tree are requirements and domain experience. They are not copied into the canonical runtime as a second agent framework.

## Future capabilities

The contracts intentionally support later additions:

- persistent agent state;
- production tool adapters;
- advanced RAG;
- governed autonomous execution;
- agent-to-agent collaboration;
- learning from outcomes;
- model lifecycle/MLOps.

These must remain behind the canonical governance boundaries.

## Definition of Done

- [x] agent contract;
- [x] task contract;
- [x] observation contract;
- [x] autonomy levels;
- [x] tenant-scoped registry;
- [x] capability authorization;
- [x] tool authorization;
- [x] orchestration boundary;
- [x] identity/domain checks;
- [x] deterministic authorization tests;
- [x] no second Cognitive Core;
- [x] documented merge gate.

Runtime CI must be green before merge; file creation alone is not evidence of test execution.
