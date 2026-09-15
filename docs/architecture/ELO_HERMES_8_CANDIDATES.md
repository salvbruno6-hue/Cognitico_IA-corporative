# ELO — Hermes → 8 Native Capability Candidates

Status: candidate-only / audit application
Authority: ELO governance
Hermes authority: reference-only

This manifest applies the governed capability-evolution model to the eight identified Hermes mechanisms. It does not claim functional integration or promotion.

## State model

`DISCOVERED → CANDIDATE → EVALUATING → TRANSFORMING → TESTING → READY_FOR_APPROVAL → EVOLUTION_GATE → VALIDATED`

Failure returns to `CANDIDATE` with a new variant. Exhaustion never promotes.

## Candidates

| ID | Hermes mechanism | Native ELO target | Type | Initial state | Required functional proof |
|---|---|---|---|---|---|
| HERMES-MEMORY | Memory | ELO Cognitive Memory | structure + function | candidate | read/write/retrieve semantics, isolation, provenance, bounded context |
| HERMES-SKILLS | Skills | ELO Native Skills Registry | Skill + structure | candidate | discover/load/validate/execute skill contract without Hermes runtime |
| HERMES-TOOLSETS | Toolsets | ELO Capability/Tool Registry | structure + function | candidate | allowlist, capability resolution, policy enforcement, deterministic rejection |
| HERMES-CONTEXT | Hierarchical Context | ELO Context Engine | function + structure | candidate | parent/child scope, precedence, isolation, bounded context assembly |
| HERMES-DELEGATION | Delegation/Subagents | ELO Worker/Delegation Engine | function | candidate | isolated execution contract, identity, resource limits, result/evidence return |
| HERMES-AUTOMATION | Automations/Cron | ELO Scheduler/Watchers | function + Skill | candidate | schedule registration, trigger evaluation, idempotency, safe no-op test |
| HERMES-MCP | MCP/Plugins | ELO External Capability Gateway | structure + function | candidate | trust boundary, allowlist, lifecycle, failure isolation, provenance |
| HERMES-CHECKPOINT | Checkpoints/Execution | ELO State Recovery Engine | structure + function | candidate | snapshot/restore, atomicity, rollback, crash-safe state semantics |

## Readiness rule

A candidate is **READY_FOR_APPROVAL** only when all of these are independently evidenced:

1. Hermes source and revision are recorded.
2. Native ELO contract is defined.
3. Consistency evaluation passes.
4. Controlled functional test passes.
5. Provenance is intact.
6. Governance metadata is complete.
7. No unresolved critical dependency or security boundary exists.
8. ELO Evolution Gate reports approval readiness.

READY_FOR_APPROVAL is not approval and does not promote knowledge.

## Current audit result

All eight are intentionally `CANDIDATE` at this stage. The generic evolution loops are ready to process them, but no candidate is marked green merely because Hermes implements the source mechanism.

### Next execution order

1. Memory
2. Skills
3. Toolsets
4. Hierarchical Context
5. Delegation/Subagents
6. Automations/Cron
7. MCP/Plugins
8. Checkpoints/Execution

Each candidate must produce its own native ELO test evidence before its semaphore can become green.
