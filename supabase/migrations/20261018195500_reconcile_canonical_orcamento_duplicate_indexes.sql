-- ELO system health reconciliation.
-- GitHub is the canonical operational authority; keep the index names already
-- declared by 20260912100000_align_elo_orcamento_forge_governance.sql.
-- This migration is idempotent and removes only indexes proven identical to
-- canonical counterparts. It does not alter application data.

DROP INDEX IF EXISTS public.idx_elo_orc_lista_mae;
DROP INDEX IF EXISTS public.idx_elo_orc_dec_associacao;
DROP INDEX IF EXISTS public.idx_elo_orc_dec_orcamento;

-- Intentionally NOT removing the two duplicate-index pairs on
-- elo_orcamento_calculos_aprendidos here. Their canonical name is not yet
-- evidenced in GitHub, so they remain a governance GAP until provenance is
-- established.