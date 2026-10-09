---
id: ELO-DATA-OKR-PERSIST-001
name: Strategic Objective Persistence Boundary
type: contract
layer: data
owner: strategic-objective-domain
status: draft
authority: proposal
version: 0.1
related:
  - strategic_okr
  - OkrReadRepository
  - mt_definicoes_kpi
  - mt_snapshots_kpi
  - elo_cognitive_relations
  - EvidenceRepository
  - GovernedOrchestrator
depends_on:
  - explicit architectural approval for the persistent owner
  - explicit tenant isolation model for strategic data
---

# ELO — Strategic Objective Persistence Boundary

## 1. Decision status

This document is a **DRAFT architecture/data contract proposal**. It does not authorize schema creation, migration execution, production data writes, or merge.

The repository rule `INSPECT → REUSE → EXTEND → RELATE → REFACTOR/MIGRATE → CREATE ONLY IF INDISPENSABLE` was applied before this proposal.

## 2. Proven facts

Read-only inspection of the canonical repository and live Supabase project established that:

1. no existing `Objective`, `KeyResult`, `OKR`, `Objetivo` or `Resultado-Chave` persistent entity owner was found in `public` or `elo_core`;
2. `elo_cognitive_relations` is a generic **relation** owner with `source_type/source_id → relation_type → target_type/target_id`, but it has no `tenant_id` and is currently service-role-only;
3. `elo_conhecimento_itens` / `elo_conhecimento_vinculos` are knowledge owners, not strategic entity stores, and also do not represent a tenant-scoped Objective/KR lifecycle;
4. `mt_definicoes_kpi` is the existing formal KPI-definition registry and must not be duplicated;
5. `mt_snapshots_kpi` is the existing KPI observation/snapshot owner, but its current schema has no `tenant_id` and no `key_result_id` binding;
6. `mt_definicoes_kpi` and `mt_snapshots_kpi` currently have RLS enabled, but their authenticated policies are not tenant filters: definitions are readable by authenticated clients and snapshots are readable/appendable by authenticated clients;
7. the canonical authorization baseline owns identity, role, capability and scope, but it does not establish a general tenant table/FK that can be assumed for new strategic persistence;
8. the application contract already requires `tenant_id` on `Objective`, `KeyResult` and `Measurement` and fails closed on cross-tenant reads.

## 3. Canonical ownership boundaries

The persistence design MUST preserve these owners:

| Concept | Existing owner | Rule |
|---|---|---|
| Cognitive orchestration | `GovernedOrchestrator` | OKR remains subordinate capability |
| Objective/KR semantics | `strategic-objective-domain` | persistence may implement the port; it must not become an orchestrator |
| KPI definition | `mt_definicoes_kpi` | reuse; no second KPI registry |
| KPI snapshot/observation | `mt_snapshots_kpi` | reuse or strengthen only after tenant/binding decision |
| Evidence | `EvidenceRepository` | references only from OKR entities; no OKR evidence store |
| Decision/Action/Outcome | canonical `DecisionLifecycle` / outcome owners | no OKR lifecycle copy |
| Learning | canonical Symbiont / learning governance | no automatic OKR learning |
| Generic cognitive relations | `elo_cognitive_relations` | relation only; not Objective/KR entity storage |
| Authorization | `elo-authz` / canonical authorization schema | persistence does not self-authorize |

## 4. Why existing generic tables are insufficient as the Objective/KR entity owner

### 4.1 `elo_cognitive_relations`

It can potentially represent links such as:

`operational-event → KPI → KR → Objective → strategy`

but it cannot safely own the Objective or KR entity itself because:

- it models edges rather than entity state;
- it has no `tenant_id` column;
- its live policy is service-role-only;
- it has no Objective/KR lifecycle fields;
- overloading `context` JSONB with the entire strategic entity would hide schema, constraints and ownership.

Result: **REUSE FOR RELATIONS ONLY, subject to a later tenant-isolation decision.**

### 4.2 Knowledge tables

`elo_conhecimento_itens` and `elo_conhecimento_vinculos` own governed knowledge, not operational strategic commitments with approved targets, deadlines and current measurements.

Result: **DO NOT REUSE AS THE OKR ENTITY STORE.**

## 5. KPI definition versus tenant-scoped measurement

The current design must distinguish two scopes:

### 5.1 KPI definition identity

`mt_definicoes_kpi` may remain a corporate/global definition registry if that scope is explicitly confirmed. A KPI code, formula, domain and unit can be global without making every measurement global.

This proposal therefore preserves:

`KeyResult.metric_code → mt_definicoes_kpi.codigo_kpi`

### 5.2 Measurement context

The OKR contract requires:

`Measurement(tenant_id, measurement_id, key_result_id, metric_code, value, measured_at, evidence_refs, source_ref)`

The current `mt_snapshots_kpi` table contains KPI/date/value context but does not represent `tenant_id` or `key_result_id`. Therefore it must **not** be claimed as a complete tenant-safe implementation of `Measurement` yet.

Current classification:

- KPI definition registry: `REUSE / GLOBAL SCOPE TO BE CONFIRMED`;
- KPI snapshots: `REUSE CANDIDATE / TENANT+SUBJECT BINDING NOT PROVEN`;
- OKR Measurement persistence: `PARCIAL / BLOCKED BY BINDING MODEL`.

## 6. Minimum persistent domain that appears indispensable

Because no equivalent Objective/KR entity owner was found, a dedicated tenant-scoped strategic entity owner is the leading architecture candidate. This is a **proposal, not authorized DDL**.

Minimum semantics required by the already-implemented contract:

### Objective entity

- tenant identity;
- objective identity;
- title;
- optional strategy reference;
- optional owner reference;
- evidence/provenance linkage;
- temporal/audit metadata.

### KeyResult entity

- tenant identity;
- KR identity;
- Objective identity;
- title;
- formal KPI identity (`metric_code`), not a duplicate KPI definition;
- direction;
- baseline + baseline evidence;
- target + target evidence;
- target approval state + approval reference;
- deadline;
- weight;
- temporal/audit metadata.

The storage representation of evidence references (array, normalized relation, or canonical evidence association) remains a separate implementation decision and must not be silently embedded in JSON merely for convenience.

## 7. Candidate architectures

### Option A — Dedicated tenant-scoped Objective/KR persistence — RECOMMENDED FOR APPROVAL

Create the smallest persistent owner for Objective and KeyResult only, implementing `OkrReadRepository` and preserving all existing owners.

Properties:

- explicit `tenant_id` on strategic entities;
- FK/constraint that prevents KR from binding to an Objective of another tenant;
- RLS or backend-only access aligned with canonical ELO authorization;
- no duplicate KPI definition/snapshot registry;
- no learning/decision/evidence authority inside the tables;
- relation to `elo_cognitive_relations` remains optional/read-side until tenant semantics for that table are governed.

This option best matches the current domain contract while minimizing new authority.

### Option B — Extend a future proven generic strategic-entity owner

If a canonical tenant-scoped generic entity owner is later found or approved, adapt Objective/KR to it instead of creating dedicated tables.

Current state: **BLOCKED — no such owner is proven today.**

### Option C — External system remains persistent owner

Keep `OkrReadRepository` as an adapter over an external OKR/strategy system if such a system becomes the corporate source of truth.

Current state: **BLOCKED — no external owner/source was identified in the current scope.**

## 8. Tenant isolation requirements before any DDL

Any approved persistence MUST define the tenant security source explicitly. It must not infer tenant from department/sector and must not trust user-editable metadata.

Before migration creation, one of these must be proven and approved:

1. canonical tenant membership table / scope binding used by RLS; or
2. backend-only/service-bound access where tenant authorization is validated by `elo-authz` before storage access; or
3. another existing canonical tenant boundary with equivalent evidence.

A policy equivalent to `TO authenticated USING (true)` is insufficient for Objective/KR strategic data.

## 9. Measurement binding decision required

Before claiming full persistence E2E, choose one governed approach:

### M1 — Strengthen `mt_snapshots_kpi`

Add tenant/subject binding to the existing snapshot owner if this does not break its intended corporate/global semantics.

### M2 — Add a tenant-scoped KR↔snapshot association

Keep snapshot values in the existing owner and persist only the tenant/KR association with provenance. This avoids creating a second KPI snapshot registry.

### M3 — Prove snapshots are intentionally global and source measurements elsewhere

If `mt_snapshots_kpi` is intentionally global and cannot carry tenant context, a different canonical measurement source must be proved; do not duplicate snapshot authority merely for OKR.

No option is selected by this draft.

## 10. Implementation gate

The next implementation step is authorized only after an explicit architecture decision confirms:

- persistent owner for Objective/KR;
- tenant-isolation authority;
- KPI-definition scope (global vs tenant-aware);
- Measurement ↔ KR binding model;
- access mode (backend-only vs authenticated RLS surface).

Only then should a migration be generated through the repository's official Supabase migration flow, followed by adapter implementation, tests, advisors and live validation.

## 11. Non-goals

This proposal does NOT authorize:

- new `OkrOrchestrator` or router;
- new KPI registry;
- new evidence repository;
- new decision lifecycle;
- new learning engine;
- automatic target approval;
- automatic learning;
- live Supabase DDL;
- merge of PR #961.

## 12. Proposed decision

**Recommended architecture:** approve Option A for Objective/KeyResult entity ownership, while keeping KPI definition in `mt_definicoes_kpi`; separately choose the Measurement binding strategy before implementation.

Until that decision exists, the current `OkrReadRepository` remains the correct storage-neutral boundary and the persistence gap remains fail-closed rather than being filled by an invented schema.
