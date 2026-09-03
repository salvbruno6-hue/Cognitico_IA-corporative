-- ELO canonical identity binding: allow the authenticated OAuth callback
-- to invoke the existing SECURITY DEFINER binding function.
-- No new identity/authentication authority is introduced.

grant execute on function public.elo_bind_authenticated_identity() to authenticated;
revoke execute on function public.elo_bind_authenticated_identity() from anon;
