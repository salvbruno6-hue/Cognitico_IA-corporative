# ELO Context Engineering Contract

**Status:** PROPOSED FOR VALIDATION

## 1. Purpose

Define one common context-engineering model for ELO without creating a new architectural authority or replacing existing Memory, Routing, Learning, Core, Forge, Evidence, or Evolution Gate contracts.

Context Engineering is the discipline that keeps the right context available across executions, experiments, decisions, and learning cycles.

It is not a new database, memory engine, router, or Core.

## 2. Two complementary loops

The agent/execution loop answers: **what must be done now?**

```text
OBSERVE → LOAD CONTEXT → INTERPRET → DECIDE → ROUTE → EXECUTE → EVIDENCE
```

The context/learning loop answers: **what should remain useful for the next decision?**

```text
OBSERVE
  ↓
LOAD CONTEXT
  ↓
RELATE
  ↓
IDENTIFY GAP
  ↓
HYPOTHESIZE
  ↓
EXPERIMENT / ACT
  ↓
MEASURE
  ↓
COMPARE
  ↓
SELF-CORRECT
  ↓
RECORD
  ↓
GENERALIZE
  ↓
GOVERN
  ↓
RETAIN / PROMOTE / REJECT
```

The second loop must never bypass governance. A successful execution is evidence, not generalized learning.

## 3. Context classes

ELO shall distinguish at least five forms of context:

| Context | Owner | Purpose | Canonical by default? |
|---|---|---|---|
| Operational context | Domain/operational layer | Compact rules and instructions that change current decisions | No |
| Accumulated context | Domain context | History, relationships, hypotheses, gaps and outcomes | No |
| Structured learning | Banco de Aprendizados | Queryable learning with provenance, evidence and validation state | Only after governance |
| Procedural context | Skills / Forge | Reusable validated procedures | No; promotion governed |
| Canonical knowledge | Core | Institutional truth, contracts, rules and validated knowledge | Yes, after promotion |

A markdown context file is therefore a context carrier, not automatically a memory authority or canonical source.

## 4. Layer ownership

### Forge

Owns controlled construction, experimentation, adaptation, comparison and testing. Forge receives accumulated experience and produces evidence-backed candidates. It does not promote directly to Core.

Existing constructor boundary remains authoritative: `OBJECTIVE → READ CANONICAL CONSTRAINTS → PLAN → BUILD → TEST → COMPARE → ADJUST → VALIDATE → PROMOTE`.

### Banco de Aprendizados

Owns structured learning records. A learning record should preserve at least provenance, scope, context, evidence, baseline, hypothesis, experiment, outcome, metrics, regression/generalization status and governance state.

The database is the structured memory of validated experience; it is not a replacement for Core.

### Orçamento

Owns economic/commercial context for estimates and decisions: scope, modality, quantities, composition, materials, labor, logistics, production implications, historical deviations, actual-vs-estimated results and their causes.

Budget learning must remain traceable to the originating solicitation/project/version and must not become a universal pricing rule without governed validation.

### Cognitivo

Owns interpretation and synthesis for corporate decisions. It consumes canonical knowledge plus scoped context, evidence and governed learning. It should explain the chain `FATO → EVIDÊNCIA → HIPÓTESE → ANÁLISE → RECOMENDAÇÃO → DECISÃO` and preserve uncertainty where evidence is insufficient.

Cognitivo is not the permanent knowledge store.

### Core

Owns canonical institutional knowledge, non-negotiable contracts, principles and validated rules. Core must remain independent from Forge, external providers and operational source systems.

### Simbionte

Acts transversally as the relation/adaptation faculty: associates experience with existing ELO capabilities, identifies gaps and patterns, proposes adaptations, measures results and prepares candidates for governed learning. It does not become an architectural authority.

### Evidence

Owns immutable execution/test evidence used to support decisions and learning. Evidence must retain source, revision, scope and outcome where applicable.

### Hermes / external runtimes

Provide execution experience and operational capabilities. They are not ELO learning or canonical authorities.

### ELO Web

Provides the human interaction and orchestration surface; it does not redefine ownership of context or knowledge.

## 5. Context record contract

Where structured context is required, the logical record should support:

- `context_id`
- `domain`
- `tenant_scope`
- `source`
- `source_revision`
- `objective`
- `state`
- `observations`
- `relations`
- `information_gaps`
- `hypotheses`
- `baseline`
- `experiment`
- `outcome`
- `metrics`
- `regression_status`
- `generalization_status`
- `provenance`
- `governance_state`
- `linked_capabilities`
- `linked_decisions`
- `evidence_refs`
- `created_at`
- `updated_at`

This is a logical contract, not an instruction to create a new table before existing schemas are inspected.

## 6. Context assembly policy

Before a consequential decision, ELO should assemble context in this order:

1. applicable Soul/Core invariants;
2. domain-specific canonical rules;
3. scoped operational context;
4. relevant structured learning;
5. relevant prior decisions and evidence;
6. current request and objective;
7. available execution capabilities;
8. unresolved information gaps.

More context is not automatically better. Context should be relevant, scoped, versioned and sufficient for the decision.

## 7. Self-correction

Self-correction is allowed inside a bounded cycle when it is based on measured divergence or failure.

```text
EXPECTED → OBSERVED → DELTA → DIAGNOSE → ADJUST → RETEST
```

Self-correction may modify an experiment, procedure, context overlay or candidate implementation inside its authority boundary. It must not silently modify Core, canonical routing, authorization, or governed learning.

## 8. User corrections

A direct user correction is high-value evidence about intended operational context, but it must be captured with provenance and scope. It may update an operational/context candidate immediately where the owning layer permits it; promotion into structured learning or Core remains governed.

This preserves responsiveness without converting every conversation correction into canonical truth.

## 9. Idempotence and history

The context system must be idempotent:

- repeated observation does not create duplicate candidates;
- the same evidence is referenced rather than copied;
- historical evidence remains immutable;
- refinements are append-only or versioned;
- supersession is explicit;
- failed experiments remain traceable;
- tenant/domain boundaries are preserved.

## 10. Promotion boundary

The minimum promotion path is:

```text
EXPERIENCE
  ↓
EVIDENCE
  ↓
ASSOCIATION
  ↓
HYPOTHESIS
  ↓
CONTROLLED TEST
  ↓
MEASURE
  ↓
RETEST / REGRESSION
  ↓
GOVERNED LEARNING
  ↓
EVOLUTION GATE
  ↓
VALIDATED LEARNING / CORE PROMOTION
```

No direct `Hermes → Core`, `Forge → Core`, `chat → Core`, or `execution → generalized learning` path is valid.

## 11. Proposed corporate application

The initial implementation should use the existing architecture rather than create parallel subsystems:

```text
                    ┌──────────── CORE ────────────┐
                    │ canonical knowledge/rules   │
                    └──────────────┬──────────────┘
                                   │
        ┌──────────────────────────▼──────────────────────────┐
        │                 COGNITIVO                           │
        │ context + evidence + learning → corporate decision │
        └───────────────┬───────────────────┬────────────────┘
                        │                   │
                 ORÇAMENTO            BANCO DE
                 economic context      APRENDIZADOS
                        │                   │
                        └─────────┬─────────┘
                                  │
                              SIMBIONTE
                         relation/adaptation
                                  │
                               FORGE
                      experiment/build/test
                                  │
                               EVIDENCE
                                  │
                               HERMES
                              execution
```

The arrows represent governed information/evidence flow, not ownership transfer.

## 12. Validation plan

Before implementation is considered complete, tests must prove:

1. existing ELO capabilities are reused instead of duplicated;
2. context assembly is deterministic for identical inputs;
3. tenant and domain scope are preserved;
4. unknown information is not fabricated to fill gaps;
5. failed/insufficient evidence cannot become learning automatically;
6. repeated observations are idempotent;
7. evidence remains immutable;
8. Forge experiments cannot mutate Core directly;
9. Hermes/external mechanisms remain non-authoritative;
10. promotion requires the Evolution Gate;
11. detaching a source context does not corrupt promoted canonical knowledge;
12. budget-specific context remains traceable to its source and version;
13. decision synthesis preserves the distinction between fact, evidence, hypothesis, analysis, recommendation and decision.

## 13. Implementation order

Do not begin by creating a new universal memory database.

Phase 1 — Contract and mapping: establish this contract and map existing modules, registries, labs and governance paths.

Phase 2 — Context adapters: create thin adapters over existing Forge, learning, budget, cognitive and Core structures.

Phase 3 — Controlled context tests: validate assembly, idempotence, isolation, provenance and detach behavior.

Phase 4 — Corporate pilots: Orçamento and one additional operational domain, using real structures only after schema inspection and with no automatic canonical promotion.

Phase 5 — Governed promotion: connect validated learning to the existing Evolution Gate.

## 14. Non-goals

This contract does not create:

- a second Core;
- a second Memory Engine;
- a second Router;
- a universal context database;
- an autonomous authorization system;
- an automatic learning promoter;
- a new architectural authority for Hermes, Forge or Simbionte.
