-- Consolidate exact duplicate permissive PCP/MT RLS policies.
-- Scope is intentionally limited to the 10 advisor findings proven equivalent.
-- The p_pcp_* family is declared canonical for these four PCP tables.
-- This migration does NOT tighten the broader literal-TRUE authorization model;
-- that remains a separate governed RLS-hardening phase.

-- mt_eventos_reparo
DROP POLICY IF EXISTS p_mt_eventos_reparo_append ON public.mt_eventos_reparo;
DROP POLICY IF EXISTS p_mt_eventos_reparo_read ON public.mt_eventos_reparo;

-- mt_lotes_estoque
DROP POLICY IF EXISTS p_mt_lotes_estoque_insert ON public.mt_lotes_estoque;
DROP POLICY IF EXISTS p_mt_lotes_estoque_read ON public.mt_lotes_estoque;
DROP POLICY IF EXISTS p_mt_lotes_estoque_update ON public.mt_lotes_estoque;

-- mt_movimentacoes_estoque
DROP POLICY IF EXISTS p_mt_movimentacoes_estoque_append ON public.mt_movimentacoes_estoque;
DROP POLICY IF EXISTS p_mt_movimentacoes_estoque_read ON public.mt_movimentacoes_estoque;

-- mt_ordens_reparo
DROP POLICY IF EXISTS p_mt_ordens_reparo_insert ON public.mt_ordens_reparo;
DROP POLICY IF EXISTS p_mt_ordens_reparo_read ON public.mt_ordens_reparo;
DROP POLICY IF EXISTS p_mt_ordens_reparo_update ON public.mt_ordens_reparo;

-- Canonical survivors intentionally preserved:
-- p_pcp_eventos_insert / p_pcp_eventos_select
-- p_pcp_lotes_insert / p_pcp_lotes_select / p_pcp_lotes_update
-- p_pcp_mov_insert / p_pcp_mov_select
-- p_pcp_reparo_insert / p_pcp_reparo_select / p_pcp_reparo_update
