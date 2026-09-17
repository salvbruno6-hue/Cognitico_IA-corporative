# ELO Supabase Learning Memory Foundation

**Status:** PROPOSED FOR IMPLEMENTATION AFTER HERMES CANDIDATE CLOSURE

## 1. Purpose

Establish the first implementation boundary for ELO's persistent learning memory using the existing Supabase schema.

This document does **not** create a new universal memory table. Supabase is the persistence layer for the existing distributed ELO memory model, while ELO Cognitive remains responsible for interpretation, association, governance and decision synthesis.

## 2. Architectural principle

The ELO learning memory is distributed by function and domain:

```text
EXPERIENCE
  -> PATTERN
  -> REASONING PATTERN
  -> CORPORATE LEARNING
  -> ARBITRATION / GOVERNANCE
  -> CANONICAL KNOWLEDGE
```

Domain-specific memories remain owned by their domains. Corporate learning does not replace operational memory, budget memory, PCP memory or quality memory.

## 3. Memory layers

| Layer | Existing structure | Responsibility |
|---|---|---|
| Experience | `elo_experience_record` | Preserve what happened, context, decisions, verification, errors, corrections and outcomes. |
| Experience pattern | `elo_experience_pattern` | Preserve reusable patterns extracted from repeated or comparable experiences. |
| Reasoning pattern | `elo_reasoning_pattern` | Preserve reusable cognitive approaches, heuristics and decision patterns. |
| Corporate learning | `elo_corporate_learning` | Consolidate explicit learning supported by evidence, provenance, scope and governance state. |
| Specialization | `elo_specialization_profile` | Preserve scoped specialized knowledge and context. |
| Assessment | `elo_corporate_assessment` | Preserve corporate assessments that inform learning and decisions. |
| Advisory | `elo_corporate_advisory` | Preserve diagnoses and recommendations linked to evidence and learning. |
| Arbitration | `elo_pts_pos` | Preserve governed positions and arbitration states before canonical incorporation. |
| Budget memory | `elo_orcament_calculation_memory` | Preserve reusable budget calculation premises, formulas, results and reuse conditions. |
| Budget execution | `elo_orcament_run` | Preserve concrete budget runs, inputs, outputs and decision traces. |
| Budget relations | `elo_orcament_association` | Preserve relationships among budget entities. |
| Quality | `elo_quality_*` | Preserve inspections, nonconformities and quality evidence. |
| PCP / production | Existing `elo_pcp_*` / production structures | Preserve operational planning, capacity, demand, execution and deviation context. |

## 4. Ownership

### Supabase

Supabase is the persistent structured storage layer. It preserves records, relationships, provenance and historical state.

### ELO Cognitive

ELO Cognitive interprets records, assembles scoped context, compares evidence, identifies patterns, evaluates applicability and synthesizes corporate decisions.

### Simbiont

The Simbiont is the transversal relation and adaptation faculty. It connects experience with existing capabilities and domain memories, proposes hypotheses and adaptations, and prepares evidence-backed learning candidates.

### Forge

Forge executes controlled construction and experimentation when a hypothesis requires testing. Forge must not write canonical knowledge directly.

### Core

Core remains the canonical institutional knowledge authority. Supabase learning records do not become Core merely because they are stored or repeated.

## 5. Learning lifecycle

```text
1. EXPERIENCE
   elo_experience_record

2. ASSOCIATION
   relate experience to domain records, prior decisions and evidence

3. PATTERN
   elo_experience_pattern

4. REASONING
   elo_reasoning_pattern

5. LEARNING CANDIDATE
   elo_corporate_learning

6. GOVERNANCE
   elo_pts_pos / applicable governance path

7. EVOLUTION GATE

8. VALIDATED LEARNING

9. CORE PROMOTION, only when canonical promotion is justified
```

Not every experience must reach every stage. Promotion must be evidence-driven and governed.

## 6. Domain memory integration

### Orçamento

Budget memory remains specialized:

```text
solicitação / projeto
       ↓
elo_orcament_run
       ↓
elo_orcament_calculation_memory
       ↓
association with experience / evidence / learning
       ↓
elo_corporate_learning when the lesson is corporate
```

A calculation premise is not automatically a corporate rule.

### PCP / Produção

Operational planning and execution records remain in their existing structures. Deviations, causes and validated recurring patterns can feed experience and corporate learning without duplicating the source records.

### Qualidade

Inspection and nonconformity records remain quality-owned. Repeated causes, successful corrections and validated prevention patterns can generate learning candidates with provenance back to the quality records.

## 7. Context assembly

For a consequential corporate decision, the Cognitive layer should assemble context from:

1. Soul/Core invariants;
2. applicable canonical domain rules;
3. current operational records;
4. specialized domain memory;
5. relevant experience records;
6. relevant experience and reasoning patterns;
7. governed corporate learning;
8. prior decisions and arbitration;
9. supporting evidence;
10. current objective and information gaps.

The order is a governance policy, not a requirement to copy all records into one context object.

## 8. Provenance and deduplication

The memory fabric must preserve:

- source record and source revision where applicable;
- tenant/domain scope;
- original context;
- relationship to the originating decision or operation;
- evidence references;
- learning state;
- supersession history;
- failed experiments and negative evidence;
- versioned refinements.

Repeated observations should reference existing records rather than create duplicate learning identities.

## 9. What must not happen

- Do not create a second universal learning database.
- Do not duplicate budget, PCP or quality operational records inside corporate learning.
- Do not treat Supabase persistence as authorization to promote learning.
- Do not promote a single successful execution into generalized knowledge.
- Do not allow Hermes or another external runtime to become the learning authority.
- Do not allow Forge to bypass governance and write Core.
- Do not silently overwrite historical experience.
- Do not mix tenant or domain scopes.

## 10. Implementation sequence

This foundation starts **after closure of the current Hermes/OpenClaw candidate evaluation sequence**.

### Phase A — Schema mapping

Create a read-only inventory of the existing Supabase learning, experience, domain, decision, evidence and governance tables and their relationships.

### Phase B — Context adapters

Implement thin, deterministic adapters over existing tables. Adapters resolve references; they do not duplicate the underlying memory.

### Phase C — Context assembly tests

Test deterministic assembly, provenance, scope isolation, missing information, duplicate prevention and historical immutability.

### Phase D — Domain pilots

Start with Orçamento and one operational domain such as Qualidade or PCP. Use existing records and no automatic canonical promotion.

### Phase E — Governed learning

Connect qualified candidates to the existing governance and Evolution Gate flow.

## 11. Initial acceptance criteria

The foundation is accepted only when tests demonstrate:

1. existing memory structures are reused;
2. no parallel memory authority is created;
3. records remain traceable to their source;
4. identical observations are idempotent;
5. tenant and domain boundaries are preserved;
6. failed or insufficient evidence remains non-canonical;
7. domain-specific memory remains domain-specific;
8. corporate learning can reference, rather than duplicate, source records;
9. Cognitive decisions can distinguish facts, evidence, hypotheses, analysis, recommendations and decisions;
10. Core promotion still requires the existing governance/Evolution Gate path.

## 12. First implementation artifact

The first code artifact after candidate closure should be a **read-only Supabase schema/context adapter**, not a new learning table.

Its first responsibility is to answer:

```text
WHAT MEMORY EXISTS?
WHERE IS IT?
WHO OWNS IT?
WHAT DOES IT RELATE TO?
WHAT EVIDENCE SUPPORTS IT?
WHAT IS ITS GOVERNANCE STATE?
CAN IT BE USED IN THIS CONTEXT?
```

Only after those answers are deterministic should ELO begin changing runtime behavior based on the distributed learning memory.
