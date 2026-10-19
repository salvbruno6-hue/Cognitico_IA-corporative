-- Remove two legacy duplicate indexes from elo_orcamento_calculos_aprendidos.
--
-- Provenance:
-- - idx_elo_calc_aprendidos_hash was introduced in 20260828124859
--   (elo_aprender_calculation_sweep_schema).
-- - idx_elo_calculos_aprendidos_memoria was introduced in 20260828155412
--   (elo_aprender_calculo_dedup_indexes).
-- - the later relational integration migration 20260912221359
--   (elo_modular_producao_compras_aprendizado_relacoes) declared the canonical
--   idx_calculos_aprendidos_hash and idx_calculos_aprendidos_memoria indexes.
--
-- Live pg_index semantics are identical within each pair. This migration keeps
-- the later canonical names and drops only the older duplicates. No table data,
-- constraints, RLS, grants or authorization semantics are changed.

DROP INDEX IF EXISTS public.idx_elo_calc_aprendidos_hash;
DROP INDEX IF EXISTS public.idx_elo_calculos_aprendidos_memoria;
