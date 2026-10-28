# MT RLS duplicate-policy canonicalization — 2026-10-28

## Decision

For the four PCP tables covered by the 10 exact `multiple_permissive_policies` findings, the `p_pcp_*` policy family is the canonical surviving family.

Scope:

- `mt_eventos_reparo`
- `mt_lotes_estoque`
- `mt_movimentacoes_estoque`
- `mt_ordens_reparo`

This decision is intentionally narrow. It does not declare every `p_pcp_*` policy canonical across the database and does not authorize broad RLS rewrites.

## Evidence

A prior provenance audit proved that all 10 pairs are exact semantic duplicates but could not establish ownership from historical provenance.

Since then, the governed authorization boundary has advanced: a verified Google operator identity is bound to `ENTERPRISE/MULTITEINER`, the PCP domain and `PCP_READ`. The operator explicitly authorized duplicate-policy reconciliation.

A live transactional rehearsal in `Elo-forge` dropped only the 10 `p_mt_*` duplicates and then rolled back. During the rehearsal:

- every affected SELECT/INSERT/UPDATE action retained exactly one `p_pcp_*` policy;
- every surviving predicate remained literal `TRUE`, identical to the effective pre-change authorization semantics;
- duplicate groups for these actions fell from 10 to 0;
- no table data, grants, tenant mapping, capability mapping or DELETE policy changed.

## Boundary

This migration fixes performance/maintainability duplication only.

It does **not** close the broader `AUTHZ_MT_PERMISSIVE_TRUE` gap. Replacing literal-TRUE policies with identity + tenant + capability authorization is a separate governed phase requiring explicit ALLOW/DENY validation per action.

## Canonical survivors

- `p_pcp_eventos_insert`
- `p_pcp_eventos_select`
- `p_pcp_lotes_insert`
- `p_pcp_lotes_select`
- `p_pcp_lotes_update`
- `p_pcp_mov_insert`
- `p_pcp_mov_select`
- `p_pcp_reparo_insert`
- `p_pcp_reparo_select`
- `p_pcp_reparo_update`

The admin DELETE policies remain unchanged.
