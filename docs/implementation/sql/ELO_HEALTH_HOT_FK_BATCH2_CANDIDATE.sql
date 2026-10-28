-- ELO Health consolidation — hot FK batch 2 candidate.
-- Evidence source: live ELO System Health Gate ranking on 2026-10-28.
-- This is a reviewed candidate, not a production migration by itself.
-- Scope is performance only: no data, RLS, grants, roles or authority changes.

CREATE INDEX IF NOT EXISTS idx_mt_unidades_modulares_ordem_producao_id
  ON public.mt_unidades_modulares (ordem_producao_id);

CREATE INDEX IF NOT EXISTS idx_mt_unidades_modulares_modelo_id
  ON public.mt_unidades_modulares (modelo_id);

CREATE INDEX IF NOT EXISTS idx_mt_unidades_modulares_pedido_venda_item_id
  ON public.mt_unidades_modulares (pedido_venda_item_id);

CREATE INDEX IF NOT EXISTS idx_mt_unidades_modulares_local_atual_id
  ON public.mt_unidades_modulares (local_atual_id);

CREATE INDEX IF NOT EXISTS idx_elo_automation_runs_automation_id
  ON public.elo_automation_runs (automation_id);
