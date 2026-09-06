-- Reconcile live Supabase migration history into version control.
-- Performance-only indexes for identity/session foreign-key access paths.

CREATE INDEX IF NOT EXISTS idx_elo_identity_registry_provider_subject
  ON public.elo_identity_registry (provider, provider_subject);
CREATE INDEX IF NOT EXISTS idx_elo_identity_sessions_identity
  ON public.elo_identity_sessions (identity_id);
