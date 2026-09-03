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

  insert into public.elo_identity_sessions
    (session_id, identity_id, issued_at, expires_at, revoked_at, last_seen_at)
  values
    (gen_random_uuid(), v_identity_id, now(), now() + interval '8 hours', null, now())
  returning session_id into v_session_id;

  return v_session_id;
end;
$$;

create or replace function public.elo_revoke_authenticated_session()
returns boolean
language plpgsql
security definer
set search_path = public, auth
as $$
declare
  v_uid uuid := auth.uid();
  v_count integer;
begin
  if v_uid is null then
    raise exception 'AUTH_REQUIRED';
  end if;

  update public.elo_identity_sessions s
     set revoked_at = coalesce(revoked_at, now()),
         last_seen_at = now()
   where s.identity_id in (
     select r.identity_id
       from public.elo_identity_registry r
      where r.auth_user_id = v_uid
   )
     and s.revoked_at is null;

  get diagnostics v_count = row_count;
  return v_count >= 0;
end;
$$;
