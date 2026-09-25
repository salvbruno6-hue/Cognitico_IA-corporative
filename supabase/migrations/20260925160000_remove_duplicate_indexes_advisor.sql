-- Supabase Postgres best-practice remediation: remove one index from each pair
-- proven identical by the live performance advisor.
-- Scope: performance-only index deduplication. No application data changes.
-- Preserve the first-listed canonical index in each pair.

DROP INDEX IF EXISTS public.ix_elo_orcamento_associacoes_lista_mae;
DROP INDEX IF EXISTS public.idx_elo_calc_aprendidos_hash;
DROP INDEX IF EXISTS public.idx_elo_calculos_aprendidos_memoria;
DROP INDEX IF EXISTS public.ix_elo_orcamento_decisoes_associacao;
DROP INDEX IF EXISTS public.ix_elo_orcamento_decisoes_orcamento;
