# ELO Health — Post-production reconciliation — 2026-10-28

## Production migration

- Supabase project: `Elo-forge`
- migration name: `elo_health_hot_fk_batch2`
- version recorded by Supabase: `20261028035933`
- source approval: PR #1085 / main `0bfaa50e3f63a777d68866d13b8170c885e03601`

## Applied scope

Exactly five evidence-ranked covering indexes were applied:

1. `mt_unidades_modulares(ordem_producao_id)`
2. `mt_unidades_modulares(modelo_id)`
3. `mt_unidades_modulares(pedido_venda_item_id)`
4. `mt_unidades_modulares(local_atual_id)`
5. `elo_automation_runs(automation_id)`

No application data, RLS policy, grant, role, tenant mapping or ELO authority was changed.

## Verification

Immediately after deployment:

- all five indexes exist in the live catalog with the expected btree definitions;
- total unindexed FK paths decreased from **145 to 140**;
- evidence-ranked hot unindexed paths decreased from **10 to 5**;
- `DATABASE_RLS` remains `HEALTHY` with 174/174 public tables using RLS and zero effectively exposed RLS/no-policy tables;
- `CAPABILITIES` remains `HEALTHY` with 15/15 active;
- `OBJECTIVE_CONTINUITY` remains `READY_IDLE` after its bounded persistence proof and cleanup;
- `MT_AUTHORIZATION` remains `GAP_HIGH` (71 tables / 168 literal-true policy objects) and was not expanded;
- `COGNITIVE_EXPERIENCE_MODEL` remains `CONFLICT` with four threshold mismatches;
- exact permissive-policy duplication remains `REVIEW` with 10 groups;
- cognitive relations remain `PARTIAL` (36 knowledge items, zero generic links/relations).

## Interpretation

This batch is successful because it removed the currently highest-evidence FK performance debt without changing authorization or data semantics. The remaining advisor count is not a target by itself. The next performance batch, if any, must be re-ranked from fresh workload evidence.
