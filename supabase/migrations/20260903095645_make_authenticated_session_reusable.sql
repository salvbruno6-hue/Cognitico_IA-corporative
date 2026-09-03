create or replace function public.elo_establish_authenticated_session()
returns uuid
language plpgsql
security definer
set search_path = public, auth
as $$
declare
  v_uid uuid := auth.uid();
  v_identity_id uuid;
  v_session_id uuid;
begin
  if v_uid is null then
    raise exception 'AUTH_REQUIRED';
  end if;

  select identity_id
    into v_identity_id
  from public.elo_identity_registry
  where auth_user_id = v_uid
    and active = true
  order by updated_at desc
  limit 1;

  if v_identity_id is null then
    raise exception 'ELO_IDENTITY_REQUIRED';
  end if;

  select session_id
    into v_session_id
  from public.elo_identity_sessions
  where identity_id = v_identity_id
    and revoked_at is null
    and (expires_at is null or expires_at > now())
  order by last_seen_at desc
  limit 1;

  if v_session_id is not null then
    update public.elo_identity_sessions
       set last_seen_at = now()
     where session_id = v_session_id;
    return v_session_id;
  end if;

  insert into public.elo_identity_sessions
    (session_id, identity_id, issued_at, expires_at, revoked_at, last_seen_at)
  values
    (gen_random_uuid(), v_identity_id, now(), now() + interval '8 hours', null, now())
  returning session_id into v_session_id;

  return v_session_id;
end;
$$;

revoke execute on function public.elo_establish_authenticated_session() from anon;
revoke execute on function public.elo_revoke_authenticated_session() from anon;
grant execute on function public.elo_establish_authenticated_session() to authenticated;
grant execute on function public.elo_revoke_authenticated_session() to authenticated;
