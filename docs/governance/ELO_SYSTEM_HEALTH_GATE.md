# ELO — System Health Gate

## Authority

- GitHub is the canonical operational authority for code, contracts, migrations, tests and governance.
- Supabase is the persistent/cognitive authority for current state, evidence, experience and operational data.
- GPT/Symbiont diagnoses and orchestrates; it does not become a third authority.

The gate reconciles GitHub intent with Supabase evidence. A conflict is a GAP to investigate, not permission to invent a new registry or rewrite an authority boundary.

This gate **operationalizes, and does not replace**, the existing RLS evidence chain in `docs/evolution/RLS_AUTHORIZATION_AUDIT_2026-10-08.md`, `docs/evolution/RLS_NO_POLICY_AUDIT_2026-10-08.json` and `tests/security/test_rls_no_policy_inventory.py`. Those artifacts remain the classified evidence/contract snapshot; the SQL here is a reusable live regression probe.

## Execution order

`diagnose -> evidence -> analyze -> correct -> test -> validate -> Evolution Gate -> merge -> production reconciliation -> learn`

## Security invariant: RLS without policy

`RLS enabled + no policy` is not automatically a vulnerability.

Classification:

| Condition | Status | Action |
|---|---|---|
| RLS enabled, no policy, `anon=0`, `authenticated=0` privileges | PASS / fail-closed | Preserve unless a real client contract requires access |
| RLS enabled, no policy, client role has privileges | BLOCK | Investigate grants and intended access before promotion |
| RLS enabled with policies | REVIEW | Validate ownership/tenant/capability predicates and avoid authorization by role alone |

Do not create permissive policies merely to silence an advisor. Access must follow the real application contract. The richer A/B/C classification and per-table provenance remain in the existing RLS audit; this gate only detects live regression of the client exposure boundary.

## Performance invariant: duplicate indexes

An exact duplicate index is a `REVIEW` finding until provenance determines which name is canonical.

Removal is allowed only when:

1. the two definitions are equivalent;
2. the retained index is evidenced by the canonical GitHub migration/contract, or another explicit authority;
3. no constraint depends on the index being removed;
4. the cleanup is idempotent and deletes no application data;
5. post-deployment advisors confirm the duplicate finding disappeared.

Unknown provenance remains a GAP; do not choose a winner by naming preference.

## Current reconciliation — 2026-10-18

Evidence from production Supabase:

- the live client-exposure probe returns zero custom ELO tables with RLS/no-policy plus `anon` or `authenticated` privileges; this confirms the fail-closed boundary already classified by the 2026-10-08 audit rather than creating a new classification;
- five exact duplicate-index pairs are present;
- three duplicate pairs in `elo_orcamento_associacoes` / `elo_orcamento_decisoes` have canonical `ix_*` counterparts declared by `20260912100000_align_elo_orcamento_forge_governance.sql` and are safe cleanup candidates;
- two pairs in `elo_orcamento_calculos_aprendidos` remain GAPs because the canonical index name/provenance is not yet established in GitHub.

## Reusable evidence query

Run `supabase/health/elo_system_health_gate.sql` against the target environment. The script is read-only and reports findings; it does not mutate production.

Promotion is blocked by `BLOCK` findings. `REVIEW` findings require evidence and a governed disposition. A clean query does not replace the existing classified audit, functional/regression tests or post-merge validation.
