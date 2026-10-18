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
- the Supabase performance advisor reports `duplicate_index=2` and `unused_index=86` after the governed cleanup.

## Performance invariant: RLS initialization plan

Row-independent authentication helpers inside RLS predicates should not be needlessly re-evaluated for every row. This is a performance concern, not an authorization redesign opportunity.

The live Health Gate finding `PERF_RLS_AUTH_JWT_PER_ROW` identifies policies that still contain direct `auth.jwt()` calls. A remediation is valid only when it preserves the existing authorization predicate and changes only the evaluation shape. In particular, the presence of this finding is **not** permission to remove `PCP_ADMIN`, change role semantics, add tenant membership, or broaden/narrow access as a side effect.

### Live reconciliation — 2026-10-18

Production currently contains **9** policies with direct `auth.jwt()` evaluation, matching the Supabase `auth_rls_initplan` advisor count. They are the seven `p_pcp_*_admin_write` policies on `lista_mae`, `modelos`, `dimensoes`, `kits`, `kit_itens`, `fluxo_produtivo_modular` and `fluxo_produtivo_modular_etapas`, plus the DELETE policies `p_pcp_reparo_delete_admin` and `p_pcp_lotes_delete_admin`.

The seven `*_admin_write` policies use `FOR ALL`, so they also overlap SELECT policies and contribute to part of the separate `multiple_permissive_policies` advisor surface. That overlap must be analyzed independently before splitting policy commands; the initplan optimization itself must not silently change authorization semantics.

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

## Reusable evidence query

Run `supabase/health/elo_system_health_gate.sql` against the target environment. The script is read-only and reports findings; it does not mutate production.

`BLOCK` findings stop promotion. `GAP_HIGH` findings prohibit expansion/normalization of the known gap and require a bounded remediation path. `REVIEW` findings require evidence and governed disposition. A clean query does not replace the existing classified audit, functional/regression tests or post-merge validation.
