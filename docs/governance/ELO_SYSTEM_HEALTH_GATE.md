# ELO — System Health Gate

## Authority

- GitHub is the canonical operational authority for code, contracts, migrations, tests and governance.
- Supabase is the persistent/cognitive authority for current state, evidence, experience and operational data.
- GPT/Symbiont diagnoses and orchestrates; it does not become a third authority.

The gate reconciles GitHub intent with Supabase evidence. A conflict is a GAP to investigate, not permission to invent a new registry or rewrite an authority boundary.

This gate **operationalizes, and does not replace**, the existing RLS evidence chain in `docs/evolution/RLS_AUTHORIZATION_AUDIT_2026-10-08.md`, `docs/evolution/RLS_NO_POLICY_AUDIT_2026-10-08.json` and `tests/security/test_rls_no_policy_inventory.py`. Those artifacts remain the classified evidence/contract snapshot; the SQL here is a reusable live regression probe.

## Execution order

`diagnose -> evidence -> analyze -> correct -> test -> validate -> Evolution Gate -> merge -> production reconciliation -> learn`

## Finding states

| State | Meaning | Promotion rule |
|---|---|---|
| `BLOCK` | A demonstrated unsafe regression in the governed boundary | Do not promote until corrected or explicitly reclassified by canonical evidence |
| `GAP_HIGH` | A known high-priority authorization/architecture gap whose safe replacement contract is not live yet | Do not expand or normalize the pattern; unrelated work may proceed only without increasing the gap |
| `REVIEW` | A finding requiring provenance and governed disposition | No automatic mutation |
| PASS / no row | The specific regression probe did not find a violation | Does not replace functional/security tests |

## Security invariant: RLS without policy

`RLS enabled + no policy` is not automatically a vulnerability.

Classification:

| Condition | Status | Action |
|---|---|---|
| RLS enabled, no policy, no effective client DML privileges | PASS / fail-closed | Preserve unless a real client contract requires access |
| RLS enabled, no policy, client role has effective DML privileges | BLOCK | Investigate grants and intended access before promotion |
| RLS enabled with policies | REVIEW | Validate ownership/tenant/capability predicates and avoid authorization by role alone |

The live probe uses `has_table_privilege`, so inherited grants through role membership or `PUBLIC` are included. Do not create permissive policies merely to silence an advisor. Access must follow the real application contract. The richer A/B/C classification and per-table provenance remain in the existing RLS audit.

## Authorization invariant: MT permissive policies

The 2026-10-08 RLS audit identified legacy `mt_*` policies where an authenticated predicate reduces to literal `true`. Those policies are **not a canonical tenant-authorization contract**.

The later `ELO_OKR_ENTERPRISE_TENANT_SCOPE_DECISION_20261009.md` establishes `ENTERPRISE/MULTITEINER` only as a prepared candidate boundary and explicitly marks it **NOT LIVE**. It requires `elo-authz` to prove canonical Google-bound identity, active session, active `ENTERPRISE` scope membership, capability, tenant, action and resource before strategic write authorization. That decision must not be generalized silently to every MT table.

Therefore:

1. existing literal-true MT policies remain `GAP_HIGH` until their real consumers and authorization contracts are traced;
2. the gap must not be expanded by new permissive policies or treated as evidence that all authenticated users are authorized;
3. no bulk revoke/rewrite is allowed without proving required application/admin workflows;
4. no new tenant table, role, capability or parallel authorization service may be invented;
5. remediation must reuse canonical `elo-authz`, `elo_identity_registry`, `elo_identity_scopes`, `elo_scopes` and existing capabilities where applicable.

### Live reconciliation — 2026-10-18

The current Supabase probe finds:

- **168** literal-true policy objects across **71** `mt_*` tables;
- **71/71** tables have effective authenticated SELECT access;
- **71/71** tables have effective authenticated write access (INSERT/UPDATE/DELETE, at least one);
- **30/71** tables carry a direct `tenant_id` column;
- the prior 2026-10-08 audit recorded 164 policy objects across 68 tables, so the gap has expanded and must remain visible as drift.

This evidence does **not** prove that all 71 tables leak cross-tenant data in every runtime path; it proves that tenant isolation and ordinary-user authorization cannot be certified from the current policies alone.

PR #978 adds a repository regression guard so new migrations cannot introduce additional literal-true MT policies applicable to `authenticated` or `PUBLIC` while this tenant contract remains unresolved. The guard uses an explicit checked-in legacy-file baseline rather than a timestamp cutoff.

## Performance invariant: duplicate indexes

An exact duplicate index is a `REVIEW` finding until provenance determines which name is canonical.

Removal is allowed only when:

1. the two definitions are equivalent across material `pg_index` semantics;
2. the retained index is evidenced by the canonical GitHub migration/contract, or another explicit authority;
3. no constraint depends on the index being removed;
4. the cleanup is idempotent and deletes no application data;
5. post-deployment advisors confirm the duplicate finding disappeared.

Unknown provenance remains a GAP; do not choose a winner by naming preference.

### Duplicate-index reconciliation — 2026-10-18

Evidence from production Supabase after PR #976 and production migration `20261018200439_reconcile_canonical_orcamento_duplicate_indexes`:

- the effective client-exposure probe returns zero custom ELO tables with RLS/no-policy plus `anon` or `authenticated` DML privileges;
- exact duplicate-index findings fell from five pairs to two;
- the two remaining pairs are both in `elo_orcamento_calculos_aprendidos` and remain `REVIEW` because canonical name/provenance is not established in GitHub;
- live catalog inspection confirms all four indexes are valid ordinary non-constraint indexes; observed scans differ, but usage statistics do not establish canonical authority;
- the Supabase performance advisor reported `duplicate_index=2` after the governed cleanup.

## Performance invariant: RLS initialization plan

Row-independent authentication helpers inside RLS predicates should not be needlessly re-evaluated for every row. This is a performance concern, not an authorization redesign opportunity.

The live Health Gate finding `PERF_RLS_AUTH_JWT_PER_ROW` identifies policies that still contain direct `auth.jwt()` calls after valid scalar-`SELECT` wrappers are removed from the diagnostic expression. A remediation is valid only when it preserves the existing authorization predicate and changes only the evaluation shape.

### Live reconciliation — 2026-10-18

PR #981 and production migration `optimize_rls_auth_jwt_initplan` converted the nine direct `auth.jwt()` policy evaluations to scalar `SELECT` form while preserving policy names, commands, roles, `app_metadata.role = admin`, `PCP_ADMIN`, tenant behavior and grants.

Post-production evidence:

- Supabase `auth_rls_initplan` advisor: **9 -> 0**;
- Health Gate `PERF_RLS_AUTH_JWT_PER_ROW`: **9 -> 0**;
- MT literal-true policy count remains **168**;
- permissive-policy overlaps remain **17**;
- duplicate-index groups remain **2**.

Therefore the initPlan debt is closed without authorization drift.

## Performance invariant: permissive-policy overlap

Multiple permissive policies for the same role/action are not one homogeneous problem. The Health Gate classifies `PERF_RLS_PERMISSIVE_OVERLAP` findings as:

- `ALL_PLUS_SPECIFIC`: a `FOR ALL` policy overlaps a command-specific policy. Correcting this can change authorization semantics and therefore requires behavioral allow/deny tests before policy restructuring.
- `EXACT_DUPLICATE`: command-specific policies have the same effective row predicates. They are candidates for consolidation only after GitHub provenance establishes which policy name/owner is canonical.
- `MULTIPLE_DISTINCT`: multiple permissive policies intentionally or historically express different predicates. They must not be collapsed as duplicates.

### Live reconciliation — 2026-10-18

The current 17 advisor findings split into:

- **7 `ALL_PLUS_SPECIFIC`** SELECT overlaps on `dimensoes`, `fluxo_produtivo_modular`, `fluxo_produtivo_modular_etapas`, `kit_itens`, `kits`, `lista_mae` and `modelos`;
- **10 `EXACT_DUPLICATE`** action overlaps across `mt_eventos_reparo`, `mt_lotes_estoque`, `mt_movimentacoes_estoque` and `mt_ordens_reparo`.

The 10 MT pairs are semantically identical in the live catalog (`authenticated`, same command, same `true` predicates), but their canonical policy-name provenance is not established in GitHub. Therefore they remain `REVIEW`; equivalence is evidence for possible cleanup, not authority to choose which policy survives.

## Performance invariant: foreign-key indexing

An advisor finding for an unindexed foreign key is **not** an instruction to index every FK. Each additional index has storage/write cost and newly created indexes will initially appear as unused until workload exercises them.

The Health Gate finding `PERF_UNINDEXED_FK_PRIORITY` ranks remaining FK paths using current `pg_stat_user_tables` evidence:

- estimated live rows;
- sequential scans;
- index scans on the table;
- insert/update/delete activity.

These statistics are cumulative and can reset, so they are prioritization evidence rather than a permanent importance score. Index creation remains bounded, versioned and separately validated.

### Live reconciliation — 2026-10-18

PR #982 and production migration `add_hot_fk_performance_indexes` added five covering indexes to the highest-evidence current FK paths:

- `elo_orcamento_memoria(orcamento_id)`;
- `mt_ordens_reparo(unidade_modular_id)`;
- `mt_ordens_reparo(tenant_id)`;
- `mt_ordens_reparo(nao_conformidade_id)`;
- `mt_ordens_reparo(aprovado_por)`.

Post-production evidence:

- `unindexed_foreign_keys`: **150 -> 145**;
- `auth_rls_initplan`: remains **0**;
- `multiple_permissive_policies`: remains **17**;
- `duplicate_index`: remains **2**;
- security advisor: unchanged at 34 informational RLS/no-policy findings plus the separate leaked-password-protection warning;
- `unused_index`: **86 -> 91** immediately after deployment because all five new indexes had no post-creation scans yet. This is expected initialization evidence, not a reason for immediate removal.

After this first batch, the remaining populated candidates drop sharply in scale: the largest currently observed unindexed-FK table has 37 estimated rows. The process should therefore re-rank live evidence before any further batch instead of chasing the advisor count toward zero.

## Reusable evidence query

Run `supabase/health/elo_system_health_gate.sql` against the target environment. The script is read-only and reports findings; it does not mutate production.

`BLOCK` findings stop promotion. `GAP_HIGH` findings prohibit expansion/normalization of the known gap and require a bounded remediation path. `REVIEW` findings require evidence and governed disposition. A clean query does not replace the existing classified audit, functional/regression tests or post-merge validation.
