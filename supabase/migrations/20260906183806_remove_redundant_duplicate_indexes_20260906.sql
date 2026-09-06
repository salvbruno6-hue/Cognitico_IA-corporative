-- Reconcile live Supabase migration history into version control.
-- This migration is intentionally idempotent and limited to schema/index cleanup.
-- No application data is inserted, updated, or deleted.

DROP INDEX IF EXISTS public.idx_elo_conhecimento_vinculos_origem;
DROP INDEX IF EXISTS public.idx_elo_conhecimento_vinculos_destino;
