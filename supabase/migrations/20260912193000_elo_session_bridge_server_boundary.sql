-- ELO Session Bridge: privileged identity/session RPCs remain server-only.
-- The browser must not execute these helpers directly. ELO Web reaches them
-- through the server-side elo-session-bridge boundary, which validates the
-- Supabase user token before using the service-role database path.

REVOKE ALL ON FUNCTION public.elo_bind_authenticated_identity() FROM PUBLIC;
REVOKE ALL ON FUNCTION public.elo_bind_authenticated_identity() FROM anon;
REVOKE ALL ON FUNCTION public.elo_bind_authenticated_identity() FROM authenticated;

REVOKE ALL ON FUNCTION public.elo_establish_authenticated_session() FROM PUBLIC;
REVOKE ALL ON FUNCTION public.elo_establish_authenticated_session() FROM anon;
REVOKE ALL ON FUNCTION public.elo_establish_authenticated_session() FROM authenticated;

REVOKE ALL ON FUNCTION public.elo_revoke_authenticated_session() FROM PUBLIC;
REVOKE ALL ON FUNCTION public.elo_revoke_authenticated_session() FROM anon;
REVOKE ALL ON FUNCTION public.elo_revoke_authenticated_session() FROM authenticated;

CREATE INDEX IF NOT EXISTS idx_elo_identity_registry_auth_user
  ON public.elo_identity_registry (auth_user_id);
