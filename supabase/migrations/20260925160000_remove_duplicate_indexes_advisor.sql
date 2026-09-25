-- Supabase Postgres best-practice remediation: remove indexes proven identical by the live advisor.
-- Scope: performance-only index deduplication. No application data changes.
-- Idempotent: safe to replay against an already-reconciled schema.

DROP INDEX IF EXISTS public.idx_elo_orc_lista_mae;
DROP INDEX IF EXISTS public.idx_calculos_aprendidos_hash;
DROP INDEX IF EXISTS public.idx_calculos_aprendidos_memoria;
DROP INDEX IF EXISTS public.idx_elo_orc_dec_associacao;
DROP INDEX IF EXISTS public.idx_elo_orc_dec_orcamento;

DROP INDEX IF EXISTS public.idx_elo_calc_aprendidos_hash;
DROP INDEX IF EXISTS public.idx_elo_calculos_aprendidos_memoria;
DROP INDEX IF EXISTS public.ix_elo_orcamento_associacoes_lista_mae;
DROP INDEX IF EXISTS public.ix_elo_orcamento_decisoes_associacao;
DROP INDEX IF EXISTS public.ix_elo_orcamento_decisoes_orcamento;
