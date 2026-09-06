-- ELO-410: tighten public RPC exposure for privileged identity/session helpers.
-- Keep the existing SECURITY DEFINER implementation and canonical ownership;
-- remove Data API execution from generic caller roles. The legitimate ELO web
-- client currently invokes these RPCs as authenticated, so this migration is
-- intentionally a review artifact: no replacement grant is introduced here.
-- A follow-up runtime path must use a server-side privileged boundary before
-- restoring execution for any caller role.

revoke all on function public.elo_bind_authenticated_identity() from public;
revoke all on function public.elo_bind_authenticated_identity() from anon;
revoke all on function public.elo_bind_authenticated_identity() from authenticated;

revoke all on function public.elo_establish_authenticated_session() from public;
revoke all on function public.elo_establish_authenticated_session() from anon;
revoke all on function public.elo_establish_authenticated_session() from authenticated;

revoke all on function public.elo_revoke_authenticated_session() from public;
revoke all on function public.elo_revoke_authenticated_session() from anon;
revoke all on function public.elo_revoke_authenticated_session() from authenticated;
