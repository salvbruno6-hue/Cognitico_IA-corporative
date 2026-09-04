revoke all on function public.elo_establish_authenticated_session() from public;
revoke all on function public.elo_revoke_authenticated_session() from public;
grant execute on function public.elo_establish_authenticated_session() to authenticated;
grant execute on function public.elo_revoke_authenticated_session() to authenticated;
