-- Reconcile live Supabase migration history into version control.
-- Idempotent index cleanup only; no application data changes.

DROP INDEX IF EXISTS public.idx_elo_calculos_aprendidos_so_conceito;
