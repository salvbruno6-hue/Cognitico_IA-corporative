-- Reconcile live Supabase migration history into version control.
-- Performance-only indexes for orçamento foreign-key access paths.

CREATE INDEX IF NOT EXISTS idx_elo_orcamento_decisoes_lista_mae_id
  ON public.elo_orcamento_decisoes (lista_mae_id);
CREATE INDEX IF NOT EXISTS idx_elo_orcamento_memoria_lista_mae_id
  ON public.elo_orcamento_memoria (lista_mae_id);
CREATE INDEX IF NOT EXISTS idx_elo_calc_varreduras_learning
  ON public.elo_orcamento_calculo_varreduras (learning_id);
CREATE INDEX IF NOT EXISTS idx_elo_calc_evidencias_calculo
  ON public.elo_orcamento_calculo_evidencias (calculo_id);
