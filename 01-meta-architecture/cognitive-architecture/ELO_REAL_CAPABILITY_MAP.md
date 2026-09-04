# ELO — Real Capability and Identity Map

## Audit purpose

This document distinguishes what the canonical repository establishes as identity, what is implemented as executable capability, what is only a contract/specification, and what remains a gap or consolidation problem.

It is an audit artifact, not a second architecture authority.

## Identity conclusion

The canonical ELO is a governed cognitive enterprise platform whose purpose is to integrate context, knowledge, evidence, reasoning, decision, execution and learning. Its normative authority is ELO Cognitivo. ELO Core materializes canonical capabilities. ELO Forge is the construction/experiment/test plane. Validation/Governance verifies conformity and can block promotion.

## Capability status taxonomy

- **CANONICAL** — architectural authority/identity is established.
- **IMPLEMENTED** — executable capability exists in `main` and has merged evidence.
- **CONTRACT** — behavior is formally specified but implementation evidence is incomplete or indirect.
- **DEFINED** — intended capability documented but not yet reproducibly evidenced.
- **EXPERIMENTAL** — implementation exists but is not canonical/promoted.
- **DUPLICATED** — overlapping implementations require consolidation.
- **BLOCKED** — execution depends on unavailable external/runtime evidence.
- **HISTORICAL** — retained for provenance, not authority.

## Current capability map

| Domain | Current status | Evidence/owner | Assessment |
|---|---|---|---|
| Canonical identity / architecture | CANONICAL | cognitive-architecture contracts | Established |
| Context resolution | IMPLEMENTED | canonical Context/CognitiveRequest path | Reusable foundation |
| Persistent memory / RAG | IMPLEMENTED | ELO-007 / PR #88 | Governed, provenance-aware |
| Source discovery / authorized adapters | IMPLEMENTED | SourceResolver / PR #214/#215 | External availability remains runtime-dependent |
| GPT/provider consultation | IMPLEMENTED/CONTRACT | governed provider handoff | Consultative, never canonical truth by itself |
| Core cognitive loop | IMPLEMENTED | ELO-CORE-001 / PR #186 | Context → Evidence → Diagnosis → Handoff/Recommendation |
| Multi-scenario diagnosis | IMPLEMENTED | ELO-TEST-001 / PR #187 | Canonical scenario gate exists |
| Scenario/diagnostic ownership | DUPLICATED | #56 | Three overlapping executable families require consolidation |
| Systemic/cross-domain reasoning | IMPLEMENTED | #99 and validation waves | Existing canonical capability |
| Governed execution boundary | IMPLEMENTED | #216 / merged evidence | Authorization/provenance/correlation controls |
| Agent ecosystem | IMPLEMENTED | ELO-003 / PR #77 | Governed agents and autonomy levels |
| Cognitive execution supervision | IMPLEMENTED/CONTRACT | ELO-022 | Recoverable state, decisions, budgets, escalation |
| Forge constructor | CANONICAL/IMPLEMENTED | Forge constructor architecture | No independent authority |
| Specialist registry | IMPLEMENTED | #154 | Specialist boundary exists |
| Enterprise/business model | CANONICAL/DEFINED | enterprise manifest + domain model | Strategic layer exists; operational completeness varies |
| Corporate data analysis | CONTRACT/IMPLEMENTED PARTIAL | corporate test protocol | Data-quality/semantic checks are defined |
| Forecast/projection | CONTRACT | systemic/scenario contracts | Must remain hypothesis/condition based |
| Budgeting / quotation | IMPLEMENTED PARTIAL | ELO-024 / #245 | Capability foundation exists; autonomous end-to-end budgeting is not yet fully evidenced |
| Budget calculation memory | CONTRACT | Budget specialist directive | Reusable reasoning model defined |
| Budget scenarios/sensitivity | IMPLEMENTED PARTIAL | ELO-024 + #56 | Must delegate to one canonical scenario owner |
| Cost/pricing source resolution | CONTRACT/PARTIAL | budgeting + source contracts | Cannot fabricate absent/current prices |
| Orçamento × realizado | CONTRACT | ELO-024 | Outcome loop defined; operational evidence still required |
| Learning / Evolution Gate | IMPLEMENTED/CONTRACT | #41 and evolution contracts | Governed promotion exists |
| Baseline v1.0 | BLOCKED/UNDECLARED | #92/#156 | Critical matrix and external/live evidence remain incomplete |
| External ELO-Forge | HISTORICAL | #156 retirement gate | Must not remain an operational authority/dependency |

## What the ELO already knows how to do

At the architectural level the ELO can:

1. preserve tenant/domain/principal/session/request/correlation context;
2. retrieve authorized evidence and preserve provenance;
3. distinguish observation, evidence, knowledge, inference, hypothesis and decision;
4. diagnose through multiple scenarios and lenses;
5. reason across domains and dependencies;
6. consult governed specialists/providers;
7. execute only through governed authorization boundaries;
8. track bounded autonomous execution cycles;
9. correct or replan when evidence requires it;
10. validate changes through tests and governance;
11. preserve historical evidence while learning;
12. promote generalized knowledge only through governed evolution;
13. construct implementations inside Forge without creating a second authority.

## What is specifically needed for autonomous budgeting

The repository already contains a strong budgeting directive. It defines the sequence:

`REQUISITO → SOLUÇÃO → QUANTITATIVO → PREMISSA → COMPOSIÇÃO → CUSTO → MEMÓRIA DE RACIOCÍNIO`

and the complete path:

`SO → DOCUMENTAÇÃO → PTS TÉCNICA → ESPECIALISTA → ORÇAMENTO → PTS PÓS → APRENDIZADO`.

It explicitly separates orchestration, execution, knowledge, calculation, evidence and learning. It also defines the reasoning memory needed to transform a prior calculation into reusable logic rather than copying a historical value.

Therefore the target is not a new budgeting intelligence. The target is **integration of the existing budgeting knowledge with the canonical ELO cognitive loop**.

## Target autonomous budgeting operating model

```text
SO / Pedido
   ↓
Context Resolver
   ↓
Source Resolver
   ↓
Knowledge + Memory
   ↓
Requirement normalization
   ↓
PTS / technical solution
   ↓
Specialist Budgeting capability
   ↓
Model/Base selection
   ↓
Excess / delta identification
   ↓
Quantification
   ↓
Composition
   ↓
Cost / pricing
   ↓
Logistics / indirects / risks
   ↓
Cross-check
   ↓
Scenario / sensitivity
   ↓
PTS Pós
   ↓
ELO decision
   ↓
Recommendation / authorization boundary
   ↓
Execution only when authorized
   ↓
Budget × actual
   ↓
Learning / Evolution Gate
```

## Critical gaps before claiming “orça sozinho”

1. Consolidate the three overlapping scenario engines under #56.
2. Verify the ELO-024 implementation against the existing budgeting directive rather than duplicating the domain knowledge.
3. Wire reproducible budgeting tests into the canonical gates.
4. Prove calculation reproducibility with representative SO fixtures.
5. Prove missing data becomes GAP/follow-up instead of fabricated value.
6. Prove current prices are sourced/validated rather than copied from history.
7. Prove PTS Técnica × Orçamento reconciliation.
8. Prove logistics, labor, indirect costs and responsibility boundaries.
9. Prove scenario/sensitivity calculations use the canonical scenario owner.
10. Prove Budget × Actual and learning without historical mutation.
11. Complete the critical architecture matrix required by #92/#156 before any global autonomy claim.

## Architectural decision

**Do not create a separate Budget Core, Budget Scenario Engine, Budget Memory or Budget Orchestrator.**

The correct evolution is:

```text
existing ELO cognition
        +
existing budgeting knowledge
        +
existing specialist boundary
        +
existing scenario capability
        +
existing governed execution
        =
Autonomous Governed Budgeting
```

## Final identity statement

The ELO is not the budget specialist, not the ERP, not the database, not GPT and not Forge.

The ELO is the **cognitive and governance system that understands the business problem, assembles authorized evidence and capabilities, reasons across them, decides what is justified, orchestrates bounded execution, verifies outcomes and learns under governance**.

The budgeting specialist is one of the capabilities through which that intelligence becomes operational.
