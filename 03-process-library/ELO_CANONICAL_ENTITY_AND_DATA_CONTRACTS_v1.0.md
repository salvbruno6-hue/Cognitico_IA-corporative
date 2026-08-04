# ELO Canonical Entity and Data Contracts v1.0

**Status:** Normative
**Scope:** Canonical entities, identifiers, relationships and data ownership for the ELO Enterprise Integration Platform.

## 1. Purpose

This document defines the canonical enterprise data model used by ELO. Its purpose is to prevent parallel vocabularies, duplicated entities and incompatible schemas across cognitive, security, integration and analytics components.

## 2. Normative scope

The canonical model governs:

- entity identity and ownership;
- tenant isolation;
- domain boundaries;
- relationship semantics;
- lifecycle and versioning;
- audit and provenance anchors;
- event compatibility;
- reference stability.

## 3. Canonical entity set

The following entities are considered part of the core enterprise ontology for ELO and may be extended, but not silently redefined:

- `Tenant`
- `Domain`
- `Principal`
- `User`
- `Role`
- `Permission`
- `Policy`
- `Session`
- `Context`
- `Knowledge`
- `Memory`
- `Reasoning`
- `Evidence`
- `Recommendation`
- `Decision`
- `Agent`
- `Capability`
- `Tool`
- `Task`
- `Event`
- `Provenance`
- `AuditEvent`
- `SourceReference`
- `Metric`
- `Hypothesis`
- `Insight`
- `RecommendationAction`
- `Outcome`

## 4. Entity boundary rules

### Tenant
Primary organizational isolation boundary. Every persisted object that belongs to an organization must be traceable to one Tenant.

### Domain
Business context within a Tenant. Domain is used for routing, ownership and authorization boundaries. `department` may exist as a legacy or adapter field, but it is not the canonical boundary.

### Principal
Authenticated actor, human or machine. Principal is the authorization subject for access and execution decisions.

### Session
Time-bounded interaction or execution container. Session holds references to Context and temporary working state. It must not become a permanent store for corporate knowledge.

### Context
Current situational information required for interpretation. Context is transient by design and may reference source facts, session state, task inputs and domain constraints.

### Knowledge
Persisted, governed and recoverable organizational knowledge derived from validated sources.

### Memory
Cognitive persistence derived from events, interactions or results. Memory may reference Context and Knowledge. It does not redefine them.

### Reasoning
Structured intermediate cognitive output. Reasoning consumes Context, Knowledge, Memory, Policies and Evidence and produces traceable analytical artifacts.

### Evidence
Verifiable supporting artifact. Evidence always requires a source anchor and may be used by Reasoning or Decision components.

### Recommendation
Candidate action or conclusion produced by reasoning. It is not equivalent to approval or execution.

### Decision
Governed selection or approval, attached to context, evidence, responsible principal, applicable policy and outcome reference.

### Agent
Goal-oriented executable unit. Agent identity must include version, capability scope, tool scope and autonomy limits.

### Capability
Declared ability of an Agent or service. Capability is explicit and permissioned.

### Tool
External callable action or integration endpoint. Tools must be whitelisted and policy-gated.

### Task
Discrete work unit assigned to a Principal or Agent. Tasks may reference Sessions, Events, Decisions or Recommendations.

### Event
Immutable occurrence used for orchestration, audit, integration or learning.

### Provenance
Record of origin, transformation and chain of custody of data, knowledge, reasoning and decisions.

### AuditEvent
Security and governance record produced by a relevant operation.

### SourceReference
Pointer to a document, record, message, API response or other source artifact.

### Metric
Measured value used by analytics, evaluation or monitoring.

### Hypothesis
Testable analytical statement.

### Insight
Validated interpretation of data or events.

### RecommendationAction
Actionable interpretation of a recommendation, usually tied to workflow or execution.

### Outcome
Observed result after a decision, action or recommendation is evaluated.

## 5. Required identifiers and ownership fields

Every canonical entity that is persisted should expose, when applicable:

- `id`
- `tenant_id`
- `domain`
- `status`
- `version`
- `created_at`
- `updated_at`
- `created_by`
- `owner_id`
- `policy_id`
- `provenance_id`
- `classification`
- `retention_class`

Legacy identifiers may coexist in adapters, but the canonical model must not depend on them.

## 6. Relationship rules

The canonical model follows these rules:

1. A Tenant owns many Domains.
2. A Domain belongs to exactly one Tenant.
3. A Principal may access one or more Tenants only through explicit authorization.
4. A Session belongs to one Principal and one Tenant, and may reference one or more Domains.
5. Context belongs to a Session or Task, not to long-term storage by default.
6. Knowledge is derived from validated sources and may be referenced by Memory.
7. Memory may reference Context and Knowledge, but is not a substitute for either.
8. Reasoning produces Evidence-backed intermediate artifacts.
9. Recommendation may lead to Decision, but is not a Decision.
10. Decision may lead to Outcome, but is not automatically execution.
11. Agent uses Capabilities and Tools under Policy.
12. Event may trigger Context refresh, Memory capture, Reasoning, Recommendation or Decision workflows.
13. Provenance and AuditEvent must be attached wherever transformation or governance requires traceability.

## 7. Compatibility rules

Any new schema or document is compatible only if it:

- preserves tenant isolation;
- preserves domain ownership;
- avoids redefining canonical entities under alternate names;
- makes provenance explicit where relevant;
- respects session vs knowledge boundaries;
- respects recommendation vs decision boundaries;
- declares policy and authorization dependencies;
- declares event and audit dependencies.

## 8. Data contract principles

The ELO data model must remain:

- explicit;
- versioned;
- traceable;
- policy-aware;
- auditable;
- compatible with adapters for legacy systems;
- suitable for both operational and analytical use.

## 9. Duplicity and conflict policy

When another document introduces a field, entity or relationship already represented here, the new material must be merged or mapped to this canonical model. It must not create a second source of truth.

## 10. Next subordinate specifications

This document is expected to be detailed, without redefining the core, by:

- Security, Tenant and Policy Enforcement;
- Context, Knowledge and Memory;
- Reasoning and Verification;
- Decision Intelligence;
- Agent Lifecycle and Autonomy;
- Provenance, Evidence and Audit;
- Analytical Intelligence;
- Integration Contracts and Events.

---

**Version:** v1.0
**Classification:** normative