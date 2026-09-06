-- Reconcile live Supabase migration history into version control.
-- Keep FK index coverage explicit and idempotent.

CREATE INDEX IF NOT EXISTS idx_excedente_itens_excedente_id
  ON public.excedente_itens (excedente_id);
CREATE INDEX IF NOT EXISTS idx_excedente_mao_obra_excedente_id
  ON public.excedente_mao_obra (excedente_id);
