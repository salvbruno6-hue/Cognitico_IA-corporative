-- Bounded FK performance improvement for active relations only.
-- No application data, RLS, grants, roles, tenant membership or authorization changes.

CREATE INDEX IF NOT EXISTS idx_elo_orcamento_memoria_orcamento_id
  ON public.elo_orcamento_memoria (orcamento_id);

CREATE INDEX IF NOT EXISTS idx_mt_ordens_reparo_unidade_modular_id
  ON public.mt_ordens_reparo (unidade_modular_id);

CREATE INDEX IF NOT EXISTS idx_mt_ordens_reparo_tenant_id
  ON public.mt_ordens_reparo (tenant_id);

CREATE INDEX IF NOT EXISTS idx_mt_ordens_reparo_nao_conformidade_id
  ON public.mt_ordens_reparo (nao_conformidade_id);

CREATE INDEX IF NOT EXISTS idx_mt_ordens_reparo_aprovado_por
  ON public.mt_ordens_reparo (aprovado_por);
