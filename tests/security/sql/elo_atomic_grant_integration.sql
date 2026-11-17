-- ELO #1172 integration test. Ephemeral PostgreSQL service only.
\set ON_ERROR_STOP on
create role anon nologin;
create role authenticated nologin;
create role service_role nologin;
create table public.elo_identity_registry(identity_id uuid primary key);
create table public.elo_roles(role_id uuid primary key,code text not null,active boolean not null);
create table public.elo_identity_roles(identity_id uuid,role_id uuid);
create table public.elo_identity_sessions(session_id uuid primary key,identity_id uuid,issued_at timestamptz,expires_at timestamptz,revoked_at timestamptz);
create table public.elo_operator_github_bindings(binding_id uuid primary key,identity_id uuid,repository_full_name text,active boolean);
create table public.elo_authorization_grants(
  grant_id uuid primary key default gen_random_uuid(),binding_id uuid not null,
  identity_id uuid not null,session_id uuid,authorization_state text not null,
  operation text not null,repository_full_name text not null,
  issued_by_identity_id uuid,request_id text not null,
  issued_at timestamptz not null default now(),expires_at timestamptz not null,
  revoked_at timestamptz,metadata jsonb not null default '{}'::jsonb,
  constraint elo_authorization_grants_valid_window check (expires_at>issued_at)
);
create table public.elo_authorization_audit(
  audit_id bigint generated always as identity primary key,
  session_id uuid,identity_id uuid,action text not null,resource text,
  scope_key text,decision text not null,reason text,request_id text,
  created_at timestamptz not null default now()
);
insert into public.elo_identity_registry values
('11111111-1111-4111-8111-111111111111'),
('22222222-2222-4222-8222-222222222222');
insert into public.elo_roles values
('33333333-3333-4333-8333-333333333333','CANONICAL_ADMIN',true);
insert into public.elo_identity_roles values
('11111111-1111-4111-8111-111111111111','33333333-3333-4333-8333-333333333333');
insert into public.elo_identity_sessions values
('44444444-4444-4444-8444-444444444444','11111111-1111-4111-8111-111111111111',now()-interval '1 minute',now()+interval '1 day',null),
('55555555-5555-4555-8555-555555555555','22222222-2222-4222-8222-222222222222',now()-interval '1 minute',now()+interval '1 day',null);
insert into public.elo_operator_github_bindings values
('66666666-6666-4666-8666-666666666666','22222222-2222-4222-8222-222222222222','org/repo',true);
grant usage on schema public to service_role;
grant select,insert,update,delete on all tables in schema public to service_role;
grant usage,select on all sequences in schema public to service_role;

-- PSQL resolves \ir relative to this script location, not the working directory.
\ir ../../../supabase/migrations/20261110185000_elo_atomic_grant_audit_rpc.sql

do $access$
begin
  if has_function_privilege('anon','public.elo_atomic_issue_authorization_grant(uuid,uuid,uuid,text,text,text,uuid,uuid,text,timestamptz,jsonb)','EXECUTE')
    or has_function_privilege('authenticated','public.elo_atomic_issue_authorization_grant(uuid,uuid,uuid,text,text,text,uuid,uuid,text,timestamptz,jsonb)','EXECUTE')
    or not has_function_privilege('service_role','public.elo_atomic_issue_authorization_grant(uuid,uuid,uuid,text,text,text,uuid,uuid,text,timestamptz,jsonb)','EXECUTE')
  then raise exception 'public RPC execute permissions are invalid'; end if;
end
$access$;

-- Test-only helper: delegates to the production RPC implementation.
create function public.elo_test_call(
  p_req text,
  p_resource text default 'resource-A',
  p_session uuid default '55555555-5555-4555-8555-555555555555'::uuid,
  p_issuer_session uuid default '44444444-4444-4444-8444-444444444444'::uuid
) returns uuid language sql security invoker as $helper$
  select (public.elo_atomic_issue_authorization_grant(
    '66666666-6666-4666-8666-666666666666'::uuid,
    '22222222-2222-4222-8222-222222222222'::uuid,
    p_session,
    'elo-execution-authorized','execute','org/repo',
    '11111111-1111-4111-8111-111111111111'::uuid,
    p_issuer_session,
    p_req,now()+interval '1 hour',
    jsonb_build_object(
      'issuer_role','CANONICAL_ADMIN',
      'resource_id',p_resource,
      'expires_in_seconds',3600
    )
  )).grant_id
$helper$;

set role service_role;
do $accepted$
declare first_id uuid; replay_id uuid;
begin
  first_id:=public.elo_test_call('req-ok');
  replay_id:=public.elo_test_call('req-ok');
  if first_id is null or first_id<>replay_id then
    raise exception 'idempotent replay did not return original grant';
  end if;
  if (select count(*) from public.elo_authorization_grants where request_id='req-ok')<>1
    or (select count(*) from public.elo_authorization_audit where request_id='req-ok' and decision='ALLOW')<>1
  then raise exception 'exactly one grant and one ALLOW audit required'; end if;
end
$accepted$;

-- The merge consumer (#1177) must observe two different ACTIVE identity
-- sessions: grant.session_id = recipient, audit.session_id = CANONICAL_ADMIN
-- issuer, both bound by the immutable issuance request_id and repository.
do $cross_identity_provenance$
begin
  if not exists (
    select 1
    from public.elo_authorization_grants g
    join public.elo_authorization_audit a
      on a.request_id = g.request_id
     and a.identity_id = g.issued_by_identity_id
     and a.resource = g.repository_full_name
    join public.elo_identity_sessions recipient
      on recipient.session_id = g.session_id
     and recipient.identity_id = g.identity_id
    join public.elo_identity_sessions issuer
      on issuer.session_id = a.session_id
     and issuer.identity_id = g.issued_by_identity_id
    where g.request_id = 'req-ok'
      and g.identity_id = '22222222-2222-4222-8222-222222222222'::uuid
      and g.issued_by_identity_id = '11111111-1111-4111-8111-111111111111'::uuid
      and g.session_id = '55555555-5555-4555-8555-555555555555'::uuid
      and a.session_id = '44444444-4444-4444-8444-444444444444'::uuid
      and a.action = 'issue_authorization_grant'
      and a.decision = 'ALLOW'
      and a.reason = 'canonical_admin_issued_authorization_state'
      and a.created_at >= g.issued_at
      and recipient.revoked_at is null and recipient.expires_at > now()
      and issuer.revoked_at is null and issuer.expires_at > now()
  ) then
    raise exception 'recipient grant session and issuer audit session provenance mismatch';
  end if;
end
$cross_identity_provenance$;

do $invalid_issuer_session$
begin
  perform public.elo_test_call(
    'req-wrong-issuer-session',
    'resource-A',
    '55555555-5555-4555-8555-555555555555'::uuid,
    '55555555-5555-4555-8555-555555555555'::uuid
  );
  raise exception 'recipient session incorrectly accepted as issuer session';
exception when sqlstate '42501' then null;
end
$invalid_issuer_session$;

do $invalid_issuer_no_persist$
begin
  if exists(select 1 from public.elo_authorization_grants where request_id='req-wrong-issuer-session')
    or exists(select 1 from public.elo_authorization_audit where request_id='req-wrong-issuer-session')
  then raise exception 'invalid issuer session persisted authorization evidence'; end if;
end
$invalid_issuer_no_persist$;

do $mismatch$
begin
  perform public.elo_test_call('req-ok','resource-B');
  raise exception 'mismatched replay was incorrectly authorized';
exception when sqlstate '42501' then null;
end
$mismatch$;

do $invalid_session$
begin
  perform public.elo_test_call('req-invalid-session','resource-A',
    '77777777-7777-4777-8777-777777777777'::uuid);
  raise exception 'invalid session was incorrectly authorized';
exception when sqlstate '42501' then null;
end
$invalid_session$;
reset role;

create function public.elo_test_force_audit_failure() returns trigger language plpgsql
as $failure$
begin
  if new.request_id='req-fail-audit' then
    raise exception 'injected audit write failure' using errcode='23514';
  end if;
  return new;
end
$failure$;
create trigger elo_test_force_audit_failure
  before insert on public.elo_authorization_audit
  for each row execute function public.elo_test_force_audit_failure();

set role service_role;
do $force_rollback$
begin
  perform public.elo_test_call('req-fail-audit');
  raise exception 'forced audit error did not propagate';
exception when sqlstate '23514' then null;
end
$force_rollback$;

do $verify_rollback$
begin
  if exists(select 1 from public.elo_authorization_grants where request_id='req-fail-audit')
    or exists(select 1 from public.elo_authorization_audit where request_id='req-fail-audit')
  then raise exception 'audit error left grant or ALLOW persisted'; end if;
end
$verify_rollback$;

update public.elo_authorization_grants set revoked_at=now() where request_id='req-ok';
do $revoke$
begin
  perform public.elo_test_call('req-ok');
  raise exception 'revoked request_id was incorrectly renewed';
exception when sqlstate '42501' then null;
end
$revoke$;
reset role;
select 'ELO #1172 PostgreSQL atomic grant+audit PASS' as result;
