# ELO Issue Registry — Current State

## Purpose

This document records the current governed execution order for **open** ELO work. It is a coordination artifact; it does not create a second authority, Core, memory, scenario engine or execution layer.

## Current open work — 2026-08-18

Only the following repository issues remain open in the canonical ELO repository at this audit point:

1. **#92 — Consolidation, Observability, Integration and Baseline Evidence**
   - Finalize the reproducible architectural evidence package.
   - Keep Baseline v1.0 gated until critical scenarios are evidenced.
2. **#156 — Architecture-to-Operation Validation**
   - Validate the full Cognitive/Core/Forge/Application/Infrastructure boundary and remaining end-to-end/adversarial cases.
3. **#72 — Issue Registry, Dependency and Test Readiness**
   - Maintain this registry as the dependency/governance index and prevent stale dependency claims.
4. **#137 — MT-001 specialist feedback**
   - Remains blocked on external/specialist evidence that is not available to the repository automation.
5. **#125 — Open-source AI architecture benchmark**
   - Governed comparative research only; no canonical replacement is implied.

## Recently completed dependencies

The following dependencies previously listed as active are now implemented and closed. They must not be described as current blockers:

- **#36 — Source Resolver Adapters:** canonical SourceResolver/authorized-adapter boundary and budgeting evidence path are implemented and validated.
- **#56 — Diagnostic Scenario Engine:** canonical scenario ownership was consolidated and adversarial regression protection is present.
- **#39 — Local AI Capability Discovery:** optional runtime capability probing is implemented.
- **#40 — Hybrid Cognitive Bridge/Maturity:** provider degradation and evidence-based maturity are implemented.
- **#41 — Canonical Evolution Gate:** executable classification, duplicate detection, alternative preservation and canonical non-mutation are implemented.
- **#45 — Intent-Driven Source Discovery/GPT Handoff:** consultative handoff is implemented with canonical context and authority boundaries.
- **#99 — Corporate Systemic Model:** derived cross-domain view is implemented without a parallel source of truth.
- **#103 / #105 — Closed-loop orchestration foundations:** governed orchestration and digital-company state-cycle foundations are implemented; broader end-to-end validation remains under #156.
- **#154 — Forge Specialist Skill Registry:** governed HR/PCP/Calculation skill pack is implemented using shared Core faculty.
- **#200–#211:** source, evolution, hybrid, adversarial, runtime, consultative, Forge, specialist-feedback, capability and budgeting integration closure wave is merged.
- **#216:** governed execution boundary and Baseline closure criteria are implemented in `main`.

## Canonical execution order

```text
Baseline evidence (#92)
        ↓
Architecture-to-operation validation (#156)
        ↓
Issue/dependency registry maintenance (#72)
        ↓
External/specialist evidence where genuinely required (#137)
        ↓
Governed external architecture benchmark (#125)
```

The order does **not** mean every item blocks every other item. #137 and #125 are evidence/research tracks and must not be used as artificial blockers for already-implemented core governance contracts.

## Mandatory gates

Every implementation remains subject to **#41 — Canonical Evolution Gate**, even though #41 itself is closed because its executable mechanism is already canonical.

Baseline v1.0 is not declared while critical architectural scenarios remain only `DEFINED`. Documentation is not equivalent to executable evidence.

## Evidence boundary

The current repository state supports the following claims:

- governed source-adapter → evidence integration exists;
- scenario readiness and conflicting-evidence blocking are executable;
- provider degradation is explicit;
- consultative GPT handoff does not acquire canonical authority;
- Forge specialists do not directly promote knowledge into Core;
- governed execution blocks when mandatory authorization/evidence/correlation controls are missing;
- adversarial validation exists for the implemented boundaries.

The repository does **not** automatically prove:

- production deployment readiness;
- live external-provider availability;
- unrestricted autonomous enterprise operation;
- specialist feedback that has not actually been supplied;
- production-scale resilience or SLO compliance.

## Superseded or historical work

Issues whose implementation has already been consolidated into later PRs must remain closed with historical/superseded reasoning. Historical evidence remains in issue/PR lineage. New implementation must first search for an existing canonical owner and classify the proposal as `REUSE | EXTEND | REFERENCE | CONSOLIDATE | NEW`.

## Architectural interpretation

The repository already contains the canonical ELO Cognitivo / Core / Forge separation. The intended system path remains:

`Cognitivo → Context → Source Discovery → Evidence → Forge Specialists → Core Faculty → Scenario/Systemic Analysis → Decision → Authorized Execution → Monitoring → Outcome Feedback → Governed Learning → Evolution Gate`

## Non-negotiables

- no second Cognitive Core;
- no parallel canonical memory;
- no parallel decision authority;
- no contextual enterprise experience promoted directly to Core;
- no invented evidence or silent conflict resolution;
- no irreversible execution without explicit authority;
- no merge without tests/evidence and the applicable governance gates.
