# ELO-007 / ELO-008 — Persistent Knowledge, RAG, Learning and MLOps

## Architectural decision

Stages 7 and 8 extend existing ELO-002 Memory/Knowledge/Evidence and ELO-003 agent governance. They do not create a second Cognitive Core.

## ELO-007 — Persistent Memory + Knowledge + RAG

The reference implementation uses `PersistentMemoryStore` with SQLite. It is an adapter, not a new canonical memory authority and not a claim that SQLite is the final enterprise vector store.

Every admitted record requires:

- `tenant_id`;
- `domain`;
- `principal_id`;
- `source_id`;
- provenance;
- creation time;
- optional expiry;
- governed kind/tags.

Retrieval is deterministic lexical ranking. This is intentionally a baseline retrieval capability. A future vector database can implement the same boundary without changing the ELO cognitive contracts.

`GovernedRetriever` produces a bounded `RAGContext` containing only scoped `RetrievedEvidence` and citation identifiers. It does not generate claims and does not promote retrieved content to canonical truth.

### Lifecycle

`Source → Temporal Memory → Admission → Persistent Memory → Retrieval → Evidence/RAG Context → Reasoning → Recommendation/Decision`

Empty retrieval is represented explicitly as `NO_VERIFIED_EVIDENCE_AVAILABLE`.

## ELO-008 — Learning + Experience + MLOps

Learning begins from observed outcomes, not from uncontrolled self-modification.

`Decision → Expected Outcome → Observed Outcome → Experience → Learning Candidate → Dataset Version → Evaluation → Human Approval → Promotion`

A candidate cannot be promoted when:

- evaluation is below threshold;
- evaluator metadata is absent;
- dataset lineage is absent;
- human approval is absent.

The implementation records experience through the existing persistent memory adapter and keeps candidate/evaluation lifecycle governed in the learning service.

### Explicit non-goals

- no autonomous production model training;
- no silent model/provider replacement;
- no self-modifying Core;
- no autonomous financial, HR, legal or safety decision;
- no mandatory vector database;
- no provider treated as canonical authority.

## Tenant and domain isolation

Persistence and retrieval always require the caller's tenant and domain. A record from another tenant or domain is not returned even if its identifier or query matches.

## MLOps boundary

Dataset version, evaluator, metric, threshold, evaluation timestamp and promotion state form the minimum reproducibility metadata. A future model registry/training platform can be connected as an authorized adapter.

## Evolution Gate

Changes remain subordinate to ELO-GOV-001. Compatible implementation may be absorbed after tests. Architectural conflicts must be classified and preserved as alternatives rather than silently changing the canonical architecture.
