-- Performance-only foreign-key indexes for the ELO authorization boundary.
-- No data, RLS, grants, roles, policies, capabilities or authority changes.
-- Selected from Supabase Advisor findings observed on 2026-10-29.

CREATE INDEX IF NOT EXISTS idx_elo_authorization_grants_identity_id
  ON public.elo_authorization_grants (identity_id);

CREATE INDEX IF NOT EXISTS idx_elo_authorization_grants_session_id
  ON public.elo_authorization_grants (session_id);

CREATE INDEX IF NOT EXISTS idx_elo_authorization_grants_issued_by_identity_id
  ON public.elo_authorization_grants (issued_by_identity_id);

CREATE INDEX IF NOT EXISTS idx_elo_operator_github_bindings_verified_by_identity_id
  ON public.elo_operator_github_bindings (verified_by_identity_id);
