# ELO — Canonical Soul and Evolution Memory

**Status:** Canonical architecture direction
**Scope:** Core governance, identity, evolution, knowledge admission and memory boundaries
**Applies to:** ELO architecture and all future model/provider connectors

## 1. Purpose

This document establishes the canonical separation between the ELO's stable identity/architecture and its continuously growing experiential knowledge.

The ELO may receive authorized information from GPT, Claude, Gemini, specialist agents, sectors, systems, documents, GitHub and other approved sources. Receiving information does not by itself change the ELO's canonical identity, contracts or architecture.

The ELO grows through governed admission, evidence, decisions, outcomes and lessons learned.

## 2. Canonical principle

> The ELO may grow in knowledge and experience without automatically changing its canonical structure.

The architecture therefore separates:

1. **ELO Soul / Canonical Identity** — who the ELO is and how its canonical architecture is defined.
2. **Organizational Memory** — what the organization has deliberately retained as reusable knowledge, decisions, experiences and outcomes.
3. **Evolution Memory** — authorized information encountered during analysis, experimentation and external consultation that remains retrievable without becoming canonical knowledge or architecture.

## 3. ELO Soul

The ELO Soul is not ordinary conversational memory. It is the protected canonical identity layer.

It defines, subject to explicit architectural governance:

- identity and purpose;
- canonical architectural boundaries;
- Cognitive Core boundary;
- canonical contracts;
- Context, Knowledge, Evidence and Memory semantics;
- Provenance requirements;
- governance and security principles;
- model/provider independence;
- rules for knowledge admission and promotion;
- rules for architectural change;
- canonical terminology;
- current verified state.

External information, including model-generated proposals, cannot silently modify the Soul.

## 4. Organizational Memory

Organizational Memory contains information deliberately retained because it has ongoing organizational value.

Examples:

- validated knowledge;
- approved decisions;
- policies;
- lessons learned;
- verified outcomes;
- durable organizational context;
- reusable domain knowledge.

Memory must preserve provenance, scope, tenant/domain identity and relevant evidence.

Memory is not automatically truth. Every memory-bearing record has a status and provenance.

## 5. Evolution Memory

Evolution Memory is a governed historical layer for authorized information that may be useful later but is not part of the canonical ELO structure or consolidated organizational knowledge.

It may contain:

- hypotheses;
- rejected alternatives;
- exploratory analyses;
- model suggestions;
- competing interpretations;
- discarded recommendations;
- research trails;
- experimental observations;
- architectural proposals not adopted;
- conversation-derived insights that were explicitly authorized for retention;
- historical context needed to understand why a decision was made.

Evolution Memory is **consultable but non-canonical by default**.

Its existence must never be interpreted as proof that the ELO believes, endorses or implements its contents.

## 6. Knowledge Admission Gate

All external information intended for retention must pass a Knowledge/Memory Admission process.

The admission process evaluates:

- authorization;
- relevance;
- persistence requirement;
- provenance;
- source reliability;
- confidence;
- evidence;
- scope;
- tenant/domain isolation;
- sensitivity and policy;
- reuse potential;
- contradiction with existing knowledge;
- freshness and expiry;
- impact on decisions;
- whether it is suitable for canonical promotion.

Possible outcomes:

```text
REJECT
ARCHIVE
OBSERVATION
EVIDENCE
KNOWLEDGE_CANDIDATE
KNOWLEDGE
DECISION
POLICY
LESSON_LEARNED
ARCHITECTURAL_PROPOSAL
```

No adapter may bypass this gate.

## 7. Promotion model

Information can move between layers only through explicit promotion rules:

```text
External Source
      ↓
Observation / Consultation
      ↓
Evolution Memory or Evidence Archive
      ↓
Validation / Decision / Governance Gate
      ↓
Knowledge / Decision / Policy / Lesson
      ↓
Organizational Memory
      ↓
[only when explicitly approved]
Canonical Architecture / ELO Soul
```

Promotion to the Soul is the highest-impact operation and requires architectural governance. It must never happen merely because a model generated a persuasive proposal.

## 8. Connector rule

GPT, Claude, Gemini and other AI providers are external cognitive providers/connectors. They are not additional Cognitive Cores.

Connectors may:

- submit observations;
- provide analysis;
- provide candidate knowledge;
- provide evidence references;
- propose architectural changes;
- retrieve authorized ELO context.

Connectors may not:

- directly mutate canonical identity;
- directly write canonical architecture;
- bypass provenance;
- bypass tenant/domain/policy controls;
- promote their own output to verified knowledge;
- create a competing Cognitive Core.

## 9. Decision example

A conversation about contracting an autonomous professional rather than an employment relationship may consult legislation, case law, market practice and multiple AI providers.

The complete conversation is not automatically stored as organizational memory.

The ELO may retain:

- relevant evidence;
- the final decision;
- its rationale;
- applicable scope;
- responsible party;
- date/version;
- provenance;
- resulting outcome.

Exploratory discussion, rejected alternatives and intermediate suggestions may remain in Evolution Memory if retention was authorized.

## 10. Identity example

When asked "Who is the ELO?", the system should prefer:

1. ELO Soul / canonical identity;
2. current verified implementation state;
3. canonical contracts;
4. verified evidence;
5. current roadmap;
6. Evolution Memory only to explain historical alternatives or changes.

Evolution Memory must not redefine identity by itself.

## 11. Contradiction handling

If providers or sources disagree, the ELO must preserve the disagreement instead of silently selecting a winner.

Example:

```text
CLAIM A — source set A
CLAIM B — source set B
STATUS — CONTRADICTORY / UNRESOLVED
```

Resolution requires evidence, policy or an authorized decision.

## 12. Maturity model

ELO maturity is not measured by the volume of retained information.

Maturity increases through:

- stronger canonical contracts;
- verified capabilities;
- higher evidence quality;
- better provenance;
- successful isolation and governance;
- validated decisions;
- measured outcomes;
- reusable lessons;
- controlled promotion from experience to knowledge;
- architectural changes that pass explicit gates.

## 13. Canonical invariant

The following invariant applies:

> **Experience can expand the ELO without redefining the ELO.**

A change to the ELO's canonical identity or architecture is a governed architectural change, not an incidental consequence of conversation, retrieval or model output.

## 14. Relationship to ELO-002

This direction extends ELO-002 rather than replacing it. ELO-002 already establishes Context, Knowledge, Evidence, Memory, provenance, tenant/domain/principal/session isolation, distinction between knowledge and evidence, and the rule that memory is not automatically truth.

The present document adds the canonical boundary between Soul, Organizational Memory and Evolution Memory and defines the admission/promotion mechanism needed for future connectors and cognitive providers.

## 15. Required future implementation

Future implementation should introduce explicit contracts/interfaces for:

- `EloCanonicalIdentity`;
- `EvolutionMemory`;
- `KnowledgeAdmission`;
- `PromotionDecision`;
- `ConnectorObservation`;
- `EvolutionRecord`;
- `KnowledgeCandidate`;
- `DecisionRecord`;
- `ArchitecturalChangeProposal`.

These contracts must be integrated with the existing canonical contracts rather than creating parallel cognitive engines.
