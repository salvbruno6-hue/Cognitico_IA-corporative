# MT RLS duplicate-policy provenance audit — 2026-10-19

## Objective

Classify the 10 remaining `multiple_permissive_policies` findings in the Multiteiner tables without changing authorization semantics or choosing a surviving policy family by name alone.

## Live evidence

The remaining advisor findings are 10 exact semantic duplicates across four tables:

| Table | Action | Policy A | Policy B | Predicate equivalence |
|---|---|---|---|---|
| `mt_eventos_reparo` | INSERT | `p_mt_eventos_reparo_append` | `p_pcp_eventos_insert` | exact (`WITH CHECK true`) |
| `mt_eventos_reparo` | SELECT | `p_mt_eventos_reparo_read` | `p_pcp_eventos_select` | exact (`USING true`) |
| `mt_lotes_estoque` | INSERT | `p_mt_lotes_estoque_insert` | `p_pcp_lotes_insert` | exact (`WITH CHECK true`) |
| `mt_lotes_estoque` | SELECT | `p_mt_lotes_estoque_read` | `p_pcp_lotes_select` | exact (`USING true`) |
| `mt_lotes_estoque` | UPDATE | `p_mt_lotes_estoque_update` | `p_pcp_lotes_update` | exact (`USING true`, `WITH CHECK true`) |
| `mt_movimentacoes_estoque` | INSERT | `p_mt_movimentacoes_estoque_append` | `p_pcp_mov_insert` | exact (`WITH CHECK true`) |
| `mt_movimentacoes_estoque` | SELECT | `p_mt_movimentacoes_estoque_read` | `p_pcp_mov_select` | exact (`USING true`) |
| `mt_ordens_reparo` | INSERT | `p_mt_ordens_reparo_insert` | `p_pcp_reparo_insert` | exact (`WITH CHECK true`) |
| `mt_ordens_reparo` | SELECT | `p_mt_ordens_reparo_read` | `p_pcp_reparo_select` | exact (`USING true`) |
| `mt_ordens_reparo` | UPDATE | `p_mt_ordens_reparo_update` | `p_pcp_reparo_update` | exact (`USING true`, `WITH CHECK true`) |

These findings are therefore `EXACT_DUPLICATE`, not merely overlapping permissive policies.

## Provenance result

Searches against both the canonical GitHub repository and `supabase_migrations.schema_migrations` did not recover the creation authority for either policy family (`p_mt_*` versus `p_pcp_*`). The tracked migration history only contains later optimization references to selected `p_pcp_*` delete policies; it does not establish which duplicate read/insert/update family is canonical.

This means the live policies are authorization state with incomplete provenance.

## Governance conclusion

Do **not** drop one family solely because the predicates are currently identical or because one naming convention appears newer/cleaner.

A safe consolidation requires one of the following to become true:

1. a canonical migration/ADR/contract is recovered that names the surviving family; or
2. a governed authorization migration explicitly declares the canonical policy family and proves no access drift under the future MT identity/tenant contract.

Until then:

- severity remains `REVIEW` for performance duplication;
- the broader `AUTHZ_MT_PERMISSIVE_TRUE` condition remains `GAP_HIGH`;
- no policy removal is authorized by this audit;
- no tenant, identity, capability or scope mapping may be inferred from these names.

## Current production boundary

At the time of this audit:

- MT literal-true policies: 168 policy objects across 71 tables;
- remaining multiple-permissive findings: 10;
- all 10 findings above are exact semantic duplicates;
- no tracked source proves which duplicate policy family is authoritative.

This document is evidence for future reconciliation, not authorization to mutate production.
