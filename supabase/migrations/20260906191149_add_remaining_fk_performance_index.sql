-- Reconcile live Supabase migration history into version control.
-- Performance-only index; no application data changes.

CREATE INDEX IF NOT EXISTS idx_excedentes_memoria_calculo_id
  ON public.excedentes (memoria_calculo_id);
