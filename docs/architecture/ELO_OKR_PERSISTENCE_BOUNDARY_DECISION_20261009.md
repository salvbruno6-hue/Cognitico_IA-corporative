---
id: ELO-DATA-OKR-PERSIST-001
name: Strategic Objective Persistence Boundary
type: contract
layer: data
owner: strategic-objective-domain
status: normative
authority: contract
version: 1.0
related:
  - strategic_okr
  - OkrReadRepository
  - mt_definicoes_kpi
  - mt_snapshots_kpi
  - elo_cognitive_relations
  - EvidenceRepository
  - GovernedOrchestrator
---

# ELO — Strategic Objective Persistence Boundary

## 1. Decision status

**APPROVED FOR MIGRATION PREPARATION on 2026-10-09.**

Explicit human authorization approved **Option A**: define the smallest tenant-scoped persistent owner for `Objective` and `KeyResult` and prepare the migration, without applying DDL to Supabase live and without merging PR #961.

The repository rule `INSPECT → REUSE → EXTEND → RELATE → REFACTOR/MIGRATE → CREATE ONLY IF INDISPENSABLE` was applied before this decision.

## 2. Proven facts

Read-only inspection of the canonical repository and live Supabase project established that:

1. no existing `Objective`, `KeyResult`, `OKR`, `Objetivo` or `Resultado-Chave` persistent entity owner was found in `public` or `elo_core`;
2. `elo_cognitive_relations` is a generic relation owner, not an entity-state owner, has no `tenant_id`, and is currently service-role-only;
3. `elo_conhecimento_itens` / `elo_conhecimento_vinculos` are knowledge owners, not strategic entity stores;
4. `mt_definicoes_kpi` remains the existing formal KPI-definition registry and must not be duplicated;
5. `mt_snapshots_kpi` remains the existing KPI snapshot owner but currently has no `tenant_id` or `key_result_id` binding;
6. the canonical authorization baseline owns identity, role, capability and scope but does not establish a general tenant-membership table/FK suitable for direct client-side tenant RLS;
7. the application contract already requires `tenant_id` on `Objective`, `KeyResult` and `Measurement` and fails closed on cross-tenant reads.

## 3. Canonical ownership boundaries

| Concept | Canonical owner | Rule |
|---|---|---|
| Cognitive orchestration | `GovernedOrchestrator` | OKR remains subordinate capability |
| Objective/KR semantics | `strategic-objective-domain` | owns only strategic entity semantics |
| Objective/KR persistence | `public.elo_strategic_objectives` / `public.elo_strategic_key_results` | approved new minimal persistent owner |
| KPI definition | `mt_definicoes_kpi` | reuse; no second KPI registry |
| KPI snapshot/observation | `mt_snapshots_kpi` | unchanged by this decision |
| Evidence | `EvidenceRepository` | persistence stores references only, never evidence content |
| Decision/Action/Outcome | canonical `DecisionLifecycle` / outcome owners | no OKR lifecycle copy |
| Learning | canonical Symbiont / learning governance | no automatic OKR learning |
| Generic cognitive relations | `elo_cognitive_relations` | relation only; not Objective/KR entity storage |
| Authorization | `elo-authz` / canonical authorization schema | persistence does not self-authorize |

## 4. Approved persistent owner

### 4.1 `public.elo_strategic_objectives`

Minimum persistent state:

- `tenant_id` — required tenant identity;
- `objective_id` — stable Objective identity inside the tenant;
- `title` — required human-readable objective;
- `strategy_ref` — optional reference to an external/canonical strategy identity;
- `owner_ref` — optional owner identity/reference;
- `evidence_refs` — identities only; no evidence payload;
- `created_at`, `updated_at` — temporal metadata.

Primary identity is composite:

`(tenant_id, objective_id)`.

### 4.2 `public.elo_strategic_key_results`

Minimum persistent state:

- `tenant_id`;
- `key_result_id`;
- `objective_id`;
- `title`;
- `metric_code` — reference to the existing formal KPI registry;
- `direction` — `INCREASE`, `DECREASE` or `MAINTAIN`;
- `baseline` + `baseline_evidence_refs`;
- `target` + `target_evidence_refs`;
- `target_approval_state` — `DRAFT` or `APPROVED`;
- `target_approval_ref`;
- `deadline`;
- `weight`;
- `created_at`, `updated_at`.

Primary identity is composite:

`(tenant_id, key_result_id)`.

The Objective relation is also composite:

`(tenant_id, objective_id) → elo_strategic_objectives(tenant_id, objective_id)`.

This prevents a KR from binding to an Objective belonging to another tenant at the database constraint layer.

## 5. KPI boundary

`KeyResult.metric_code` references `mt_definicoes_kpi.codigo_kpi`.

This reuses the current formal KPI identity and does not create a second KPI registry. The migration prepared under this decision does **not** modify `mt_definicoes_kpi` or `mt_snapshots_kpi`.

The corporate/global versus tenant-aware semantic scope of KPI definitions remains a separate governance question; this decision only reuses the registry that exists today.

## 6. Evidence representation

To minimize new authority, Objective/KR persistence stores only evidence identities as `text[]` references:

- Objective: `evidence_refs`;
- KR baseline: `baseline_evidence_refs`;
- KR target: `target_evidence_refs`.

No evidence body, confidence model, provenance calculation or evidence lifecycle is copied into these tables. `EvidenceRepository` remains the evidence authority.

Database checks preserve the application contract:

- a non-null `baseline` requires at least one baseline evidence reference;
- a non-null `target` requires at least one target evidence reference;
- `APPROVED` target state requires a non-empty `target_approval_ref`;
- `weight > 0`.

## 7. Tenant isolation / access mode

Because no canonical tenant-membership table suitable for client-side RLS is proven, the prepared migration uses the safest compatible mode:

**BACKEND-ONLY / SERVICE-BOUND.**

Rules:

1. RLS is enabled on both tables because they live in `public`;
2. all privileges are revoked from `anon` and `authenticated`;
3. no permissive client RLS policy is created;
4. `service_role` receives explicit table privileges for the authorized backend path;
5. tenant authorization must be validated by the existing ELO authorization boundary before repository access;
6. sector/department is never treated as tenant identity;
7. user-editable JWT metadata is never used as tenant authority.

A future migration may expose authenticated access only after a canonical tenant membership/source is approved. This decision does not pre-authorize that future exposure.

## 8. Measurement remains separate

This approval does **not** select M1/M2/M3 for persistent Measurement binding.

Current state remains:

- KPI definition: existing registry reused;
- KPI snapshots: existing owner preserved;
- `Measurement ↔ KeyResult ↔ tenant` persistence: **BLOCKED BY A SEPARATE GOVERNANCE DECISION**.

No new measurement table is authorized by this decision.

## 9. Migration preparation requirements

The migration candidate must:

- create only the two approved strategic entity tables;
- include tenant-safe composite keys/FK;
- reference the existing KPI registry;
- enable RLS;
- revoke `anon` and `authenticated` access;
- avoid client policies until tenant membership is governed;
- avoid `SECURITY DEFINER` helpers;
- avoid automatic learning, decisions or target approval;
- perform no data backfill;
- remain unapplied to live Supabase until a separate explicit authorization.

The official migration filename must be generated by the Supabase migration workflow. If the CLI is unavailable, the SQL may be prepared as a candidate artifact but must not be committed under an invented migration timestamp.

## 10. Non-goals

This decision does NOT authorize:

- `OkrOrchestrator` or OKR router;
- second KPI registry;
- OKR evidence repository;
- OKR decision lifecycle;
- OKR learning engine;
- automatic target approval;
- automatic learning;
- Measurement persistence changes;
- Supabase live DDL;
- PR #961 merge.

## 11. Current authorization boundary

Authorized now:

`Option A → define owner → prepare migration SQL → validate repository gates`.

Not authorized now:

`apply live → deploy → merge → Measurement schema mutation`.
