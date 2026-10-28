-- Applied to Elo-forge as migration elo_health_hot_fk_batch2.
-- Production version recorded by Supabase: 20261028035933.
-- Scope: performance only; no application data, RLS, grants, roles or authority changes.

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
