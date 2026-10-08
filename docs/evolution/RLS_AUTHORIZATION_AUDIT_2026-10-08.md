---
id: ELO-AUDIT-RLS-20261008
name: RLS authorization live reconciliation
type: reference
layer: governance
owner: ELO canonical authorization
status: draft
authority: reference
related: [ELO_AI_AGENT_WORKING_RULES.md, AGENTS.md]
---

# Scope and authority

Base main: `46cfd427d2c0b40230c17145ad09f9e9a6205394` after PR #952.
Supabase project: `fxbpevjrkwhbicpmecow`. Observations: 2026-10-08.
This audit is runtime evidence, not a new authorization contract or a claim that Stage 1 is complete.
The earlier SECURITY DEFINER correction is reconciled in GitHub; live checks confirm no public SECURITY DEFINER function is executable by anon/authenticated. No migration was reapplied.

# mt_gates investigation

| Question | Evidence and result |
|---|---|
| Creation | Persisted migration `20260913010826`, `v6_multiteiner_complementar_gaps`, creates the table. Owner is postgres; the individual author is not recorded by the inspected catalog. |
| Purpose | Schema stores gate code/name/domain/status/reason/evaluation time/evaluator per tenant. The migration also defines PCP approval and operational decision rules; a runtime consumer for this table is not established. |
| Origin of authenticated grants | `20260913011100`, `v6_rls_multiteiner_por_natureza`, block 8 grants SELECT/INSERT/UPDATE to every public table matching `mt_%`. |
| Planned policy | Same migration enables RLS for all MT tables but omits mt_gates from every policy list. No subsequent literal reference or policy was found. Omission does not prove an intended permissive policy. |
| Consumers | Full local repository/history search has no mt_gates reference. Live elo-authz v14, elo-data-gateway v3 and elo-mcp v9 have no literal reference. No non-system SQL function, noninternal trigger or view dependency references it. Dynamic/external unregistered consumers cannot be ruled out. |
| Frontend direct access | No reference found. Table has zero rows. RLS currently blocks client reads/writes regardless of its legacy grants. |
| Governed boundary | Privileged operations must reuse elo-authz; the gateway table allowlist does not expose mt_gates. No new RPC or admin bypass is warranted. |
| Capability/role | No mt_gates-specific capability or tenant membership contract found. ADMIN, PCP_READ and PCP_UPDATE exist, but assigning one to this table would invent an unproven contract. |
| Legacy grant | Confirmed unmatched wildcard grant; ineffective under current RLS. |
| Tenant contract | tenant_id is NOT NULL, references mt_tenants(id); UNIQUE(tenant_id,codigo_gate). avaliado_por references mt_pessoas(id), without a composite same-tenant constraint. |
| Cross-tenant risk | Current client denial prevents direct access. Backend bypasses RLS and must enforce tenant scope if a consumer is admitted. A future permissive policy would activate latent grants. |
| ADM/developer direct operation | No demonstrated direct authenticated admin consumer. Existing postgres/service_role table grants remain unchanged; user authentication alone is not an admin role. This is not proof of every admin workflow. |
| service_role runtime | Has SELECT/INSERT/UPDATE/DELETE and BYPASSRLS. Sufficient for the existing server access boundary, not proof of an operational mt_gates feature. |
| Decision | CORRECT unmatched client grants; preserve deny-all state, schema, rows, owner and server authority. No client policy is created. Class A describes the preserved boundary, not a claim about the original author's intent. |

# Classification of no-policy tables

`RLS_NO_POLICY_AUDIT_2026-10-08.json` records each of 34 tables with source, source_type, source_fields, observed_state, expected_state, gap, confidence, canonical_owner, risk, proposed_action, validation, consumer and ACL.
29 are public tables; five are elo_core tables. The previous 29-versus-34 discrepancy was a query-scope error, not a database change.
The five Core tables are explicitly internal/fail-closed in the existing `AUDIT_SOLIDIFICATION_GATE_2026-09-07.md`; service_role does not have SELECT on them, so its BYPASSRLS must not be confused with object grants.
Learning tables are backend-governed; dedicated writer grants do not themselves bypass RLS. Bindings/grants are elo-authz server-only. Supplier quotations use the existing restricted RPC; Lista-Mãe changes are recorded by the existing owner-executed trigger. No warning-only policy is added.

# Remaining Stage 1 GAP

The same historical MT migration contains USING(true)/WITH CHECK(true) policies for authenticated. Live sample checks confirm this on mt_clientes, mt_planos_pcp, mt_pessoas and mt_tenants; the catalog has 164 MT policies containing true across 68 MT tables.
This count refers to policy objects, not 164 tables or verified data leaks.
The canonical helper elo_private.has_capability checks persisted identity/roles/capabilities but does not resolve tenant membership. Observed scope types are DOMAIN, ENTERPRISE, REPOSITORY and SYSTEM; no tenant membership join was found in the inspected identity/tenant tables.
Consequently tenant isolation and ordinary-user operational permissions are not certified. Do not introduce a tenant authority, grant ordinary users administration, or silently remove required admin workflows.

Required next reconciliation: trace all MT consumers, reuse the canonical identity/scope authorization model, establish which tenant keys belong to each principal, then test ordinary user denial, authorized tenant access and ADM access with the actual contract. If that contract is absent, the architecture owner must decide it before a policy implementation.

# Stage 2 preliminary evidence (not started)

postgres has schema-public function default ACL `{postgres=X/postgres,service_role=X/postgres}` but no global function default ACL. PostgreSQL's acldefault for functions is `{=X/postgres,postgres=X/postgres}`. Therefore absence of PUBLIC in the schema-specific ACL is not proof that future functions are fail-closed: the implicit global PUBLIC execute requires a global default-privilege correction. Confirm with a rolled-back newly created function before implementation. Managed platform roles and schemas must not be broadly rewritten.

# Validation and state

The bounded mt_gates migration has an executable SQL regression with role probes for anon/authenticated/service_role and checks preserving postgres/service_role privileges, RLS and tenant_id. It writes no operational rows and rolls back the probes.
Python checks collect the inventory and prevent expanding the bounded migration into policy/admin mutation.
Pre-change live regression failed with `authenticated unexpectedly has SELECT on mt_gates`.
Applying the migration twice in a BEGIN/ROLLBACK probe passed both denial probes and the service_role read. A subsequent read confirmed the original grants were restored and row count remained zero. Thus the pre-merge experiment did not persist a permission change.
The 13 targeted Python tests passed; the full local suite passed under Python 3.12 and canonical Python 3.14.8. The Hermes 13 governed implementation loop also passed (evidence-only, no candidate promotion or production execution). CI, migration application and post-change runtime evidence must be recorded in the PR before reporting this correction complete.

| Stage | State |
|---|---|
| 1 RLS / authorization | EM EXECUCAO — MT tenant authorization remains unverified |
| 2 Structural privileges | PENDENTE — preliminary global PUBLIC default identified |
| 3 Backlog / duplication | PENDENTE |
| 4 Core / Forge | PENDENTE |
| 5 Cognitive orchestrator | PENDENTE |
| 6 Memory / learning | PENDENTE |
| 7 Runtime / production / performance | PENDENTE — earlier OAuth validation is separate evidence |
| 8 Governed operational autonomy | PENDENTE |
