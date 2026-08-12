# ELO-002 — Context + Knowledge + Evidence + Memory

**Status:** Implementation specification / first vertical slice
**Target:** `main`
**Purpose:** evolve the canonical ELO interface so information received from sectors, systems and specialist agents becomes contextualized, traceable knowledge without creating a second cognitive core.

## 1. Objective

Implement the smallest complete vertical slice for:

```text
Agent / Sector / System
        ↓
CognitiveRequest
        ↓
Context Resolution
        ↓
Knowledge Intake
        ↓
Evidence Registration
        ↓
Memory Record
        ↓
Cognitive Core
        ↓
CognitiveResponse
```

ELO-002 must preserve the existing ELO-001 contracts and add governed context, knowledge, evidence and memory capabilities through explicit interfaces.

## 2. Scope

### In scope

- request context resolution;
- canonical knowledge item contract;
- evidence contract;
- memory contract;
- provenance for every stored item;
- tenant/domain/principal/session isolation;
- ingestion of observations from agents/sectors;
- distinction between fact, observation, hypothesis, recommendation and decision;
- traceability from response to evidence and memory;
- in-memory adapters suitable for tests;
- deterministic tests;
- documentation and CI validation.

### Explicitly out of scope for ELO-002

- autonomous agents;
- persistent production database;
- production vector database;
- advanced RAG;
- autonomous decision execution;
- unrestricted learning;
- model training;
- causal claims without evidence;
- cross-tenant knowledge sharing.

These remain future capabilities and must be implemented behind the contracts created here.

## 3. Architectural rules

1. `src/elo/` remains the only executable cognitive core.
2. ELO-002 must extend existing contracts rather than duplicate them.
3. `tenant_id` is mandatory for persisted or memory-bearing information.
4. `domain` is mandatory for sector-originated knowledge unless explicitly classified as cross-domain by policy.
5. Every evidence item must have provenance.
6. Memory is not automatically truth.
7. Knowledge is not automatically evidence.
8. An agent conclusion is an observation/inference until validated.
9. Recommendations are not decisions.
10. No cross-tenant retrieval.
11. No silent mutation of existing memory records.
12. Version changes to knowledge and evidence must be traceable.

## 4. Canonical concepts

### Context

The contextual envelope required to interpret a request or observation.

Minimum fields:

```yaml
tenant_id:
domain:
principal_id:
user_id:
session_id:
request_id:
correlation_id:
```

### KnowledgeItem

A structured representation of a potentially reusable organizational or external knowledge statement.

```yaml
knowledge_id:
tenant_id:
domain:
title:
content:
knowledge_type:
source_refs:
evidence_refs:
confidence:
status:
created_at:
updated_at:
provenance:
```

`knowledge_type` should distinguish at minimum:

```text
FACT
OBSERVATION
EXPERT_KNOWLEDGE
SCIENTIFIC_REFERENCE
ORGANIZATIONAL_KNOWLEDGE
HYPOTHESIS
LESSON_LEARNED
```

### Evidence

An item that supports or contradicts an observation, hypothesis, recommendation or decision.

```yaml
evidence_id:
tenant_id:
domain:
source_type:
source_id:
claim:
content_ref:
observed_at:
quality:
relevance:
provenance:
```

Quality states:

```text
VERIFIED
SUPPORTED
UNVERIFIED
CONTRADICTORY
STALE
INVALID
```

### Memory

Contextual historical state used to preserve interaction and organizational experience.

```yaml
memory_id:
tenant_id:
domain:
session_id:
principal_id:
memory_type:
content:
source_refs:
evidence_refs:
created_at:
expires_at:
provenance:
```

Memory types:

```text
SESSION
OBSERVATION
EXPERIENCE
DECISION
OUTCOME
LESSON
CONTEXT
```

## 5. Agent/Sector intake

The ELO must accept a governed report from a specialist agent or sector.

```yaml
observation_id:
tenant_id:
domain:
agent_id:
principal_id:
subject:
observation:
entities:
evidence_refs:
confidence:
questions:
provenance:
```

Processing:

```text
Incoming observation
        ↓
validate identity
        ↓
validate tenant/domain
        ↓
resolve context
        ↓
register evidence
        ↓
classify observation
        ↓
create/update knowledge candidate
        ↓
record memory
        ↓
make available to Cognitive Core
```

The intake must not automatically promote an agent statement to verified knowledge.

## 6. Provenance

All knowledge, evidence and memory records must be traceable to their origin.

Minimum provenance:

```yaml
request_id:
correlation_id:
source_type:
source_id:
agent_id:
provider:
model:
created_at:
validation_status:
metadata:
```

The system must be able to answer:

- who supplied the information;
- from which source;
- when it was obtained;
- under which tenant/domain;
- which request produced it;
- what evidence supports it;
- whether it has been validated.

## 7. Context resolution

The resolver must build context from the existing `CognitiveRequest` without replacing the canonical request.

Resolution order:

```text
explicit request context
        ↓
validated session context
        ↓
tenant/domain policy
        ↓
principal identity
        ↓
source metadata
```

Conflicts must fail closed rather than silently selecting an arbitrary context.

## 8. Retrieval boundary

ELO-002 may provide a simple deterministic repository adapter for retrieving knowledge/evidence/memory.

The adapter must expose semantic intent such as:

```text
find_relevant_knowledge(context, query)
find_evidence(context, refs)
find_memory(context, query)
```

It must not pretend that lexical matching is production RAG.

Production retrieval/vector infrastructure remains a future adapter.

## 9. Cognitive Core integration

The Core receives typed contextual information.

Conceptual flow:

```text
CognitiveRequest
      ↓
ContextResolver
      ↓
KnowledgeRepository
      ↓
EvidenceRepository
      ↓
MemoryRepository
      ↓
CognitiveCore
      ↓
CognitiveResponse
```

The Core remains responsible for orchestration. Storage/retrieval adapters remain outside the Core.

## 10. Response requirements

A successful ELO-002 response should be able to expose, through the existing canonical response/provenance mechanisms:

- request_id;
- session_id;
- domain;
- response;
- evidence references;
- provenance;
- processing_time_ms.

No new incompatible response envelope should be introduced.

## 11. Error contract

The existing error contract remains canonical.

Expected errors include:

```text
INVALID_CONTEXT
TENANT_REQUIRED
DOMAIN_REQUIRED
UNAUTHORIZED_SOURCE
EVIDENCE_NOT_FOUND
MEMORY_ACCESS_DENIED
KNOWLEDGE_ACCESS_DENIED
CONTEXT_CONFLICT
```

Errors must not leak data from another tenant or domain.

## 12. Security and isolation

Tests must prove:

```text
Tenant A cannot retrieve Tenant B knowledge.
Tenant A cannot retrieve Tenant B memory.
Tenant A cannot retrieve Tenant B evidence.
Domain A cannot access restricted Domain B information without policy.
Agent A cannot impersonate Agent B.
```

## 13. Quality rules

A knowledge item must not be marked `VERIFIED` solely because:

- an LLM generated it;
- an agent reported it;
- it appeared frequently;
- it exists in memory.

Verification requires explicit evidence or a governed validation process.

## 14. Tests required

### Context

- valid context accepted;
- tenant required;
- conflicting tenant rejected;
- session context preserved;
- domain preserved.

### Knowledge

- knowledge item created;
- source retained;
- tenant isolation enforced;
- version/provenance retained.

### Evidence

- evidence created;
- evidence linked to knowledge;
- contradictory evidence supported;
- missing evidence handled consistently.

### Memory

- memory created;
- session memory retrievable;
- tenant isolation enforced;
- memory provenance preserved;
- memory does not automatically become verified knowledge.

### Agent intake

- valid agent observation accepted;
- invalid agent identity rejected;
- agent observation becomes traceable candidate knowledge;
- evidence references preserved.

### Integration

- ELO-001 happy path remains working;
- ELO-002 does not break existing CognitiveRequest/CognitiveResponse;
- errors use canonical ErrorContract;
- processing time remains measured.

## 15. Definition of Done

ELO-002 is complete only when all are true:

- [ ] ContextResolver exists and is tested.
- [ ] Knowledge contract exists and is tested.
- [ ] Evidence contract exists and is tested.
- [ ] Memory contract exists and is tested.
- [ ] Agent/Sector intake exists and is tested.
- [ ] Provenance exists on all three stores.
- [ ] Tenant isolation tests pass.
- [ ] Domain/policy isolation tests pass where applicable.
- [ ] Existing ELO-001 tests remain green.
- [ ] New ELO-002 tests pass.
- [ ] CI validates the vertical slice.
- [ ] No duplicate Cognitive Core exists.
- [ ] No persistent production infrastructure is falsely claimed.
- [ ] Documentation reflects actual implementation.
- [ ] Capability maturity is updated only with evidence.

## 16. Maturity target

The target is not automatically maturity 7.

Expected target after implementation:

```text
Context        → 5 TESTED
Knowledge      → 5 TESTED
Evidence       → 5 TESTED
Memory         → 5 TESTED
Agent Intake   → 5 TESTED
Integration    → 5 TESTED
```

Verification and operational evidence require subsequent gates.

## 17. Example — Financial sector

A finance agent reports:

> A transaction used a resource allocation that later caused a discrepancy identified by HR.

ELO-002 should create:

```text
Observation
   ↓
Evidence
   ↓
Context
   ↓
Memory
   ↓
Knowledge Candidate
```

It should not immediately conclude:

> Finance made an error intentionally.

The statement remains an observation until evidence and reasoning establish a stronger conclusion.

## 18. Example — Operations / forklifts

An operations agent reports:

```text
maintenance_cost ↑
impact_events ↑
floor_irregularity = observed
forklift_route = high_frequency
```

ELO-002 stores these as contextualized observations and evidence.

Later ELO reasoning can compare them with historical experiences and evaluate possible interventions.

ELO-002 itself does not decide that a dedicated rail or gantry is the correct solution.

## 19. Future evolution

ELO-002 creates the foundation for:

```text
ELO-003 Reasoning + Critique
ELO-004 Agent Orchestration
ELO-005 Decision + Human Dialogue
ELO-006 Learning + Experience
ELO-007 IoT Intelligence
ELO-008 Enterprise Graph / Digital Twin
```

The exact numbering may be revised by the project registry; the contracts and architectural principles must remain consistent.

## 20. Implementation rule

Every implementation change must follow:

```text
Requirement
 ↓
Capability
 ↓
Contract
 ↓
Implementation
 ↓
Test
 ↓
Evidence
 ↓
Maturity
```

If an implementation conflicts with an existing canonical contract, adapt the implementation to the canonical architecture unless an explicit ADR approves a contract change.

## 21. Final objective

The purpose of ELO-002 is not simply to add storage.

It establishes the first trustworthy bridge between:

```text
SETORES
AGENTES
SISTEMAS
DOCUMENTOS
EVENTOS
OBSERVAÇÕES
        ↓
       ELO
        ↓
CONTEXTO
CONHECIMENTO
EVIDÊNCIA
MEMÓRIA
```

so that future reasoning can be based on traceable organizational experience rather than isolated conversations or unsupported model output.
