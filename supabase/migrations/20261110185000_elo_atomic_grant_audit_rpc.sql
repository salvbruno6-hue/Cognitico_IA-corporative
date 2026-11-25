-- ELO #1172: atomic grant+audit persistence for the canonical elo-authz issuer.
-- This is a persistence adapter, not a second authorization authority.
-- Migration requires governed ELO gates, never direct execution on production.
begin;

do $preflight$
begin
  if exists (
    select 1 from public.elo_authorization_grants
    where issued_by_identity_id is not null
    group by issued_by_identity_id, request_id having count(*) > 1
  ) then
    raise exception 'elo_authz_issue_request_duplicates_require_reconciliation'
      using errcode = '23505';
  end if;
end
$preflight$;

create unique index if not exists uq_elo_authz_grant_issuer_request
  on public.elo_authorization_grants (issued_by_identity_id, request_id);

create or replace function public.elo_atomic_issue_authorization_grant(
  p_binding_id uuid,
  p_identity_id uuid,
  p_session_id uuid,
  p_authorization_state text,
  p_operation text,
  p_repository_full_name text,
  p_issued_by_identity_id uuid,
  p_issuer_session_id uuid,
  p_request_id text,
  p_expires_at timestamptz,
  p_metadata jsonb
)
returns public.elo_authorization_grants
language plpgsql
security invoker
set search_path = ''
as $elo_atomic$
declare
  v_now timestamptz := transaction_timestamp();
  v_grant public.elo_authorization_grants%rowtype;
begin
  if p_binding_id is null or p_identity_id is null or p_session_id is null
     or p_issued_by_identity_id is null or p_issuer_session_id is null
     or nullif(btrim(p_operation), '') is null
     or nullif(btrim(p_repository_full_name), '') is null
     or nullif(btrim(p_request_id), '') is null
     or p_authorization_state not in (
       'elo-execution-authorized', 'elo-commit-authorized', 'elo-merge-authorized'
     ) or p_authorization_state is null
     or p_metadata is null or jsonb_typeof(p_metadata) <> 'object'
     or p_metadata->>'issuer_role' is distinct from 'CANONICAL_ADMIN'
     or nullif(btrim(p_metadata->>'resource_id'), '') is null
     or coalesce(p_metadata->>'expires_in_seconds', '') !~ '^[0-9]+$'
  then
    raise exception 'elo_authz_atomic_grant_invalid_arguments' using errcode = '22023';
  end if;

  if (p_metadata->>'expires_in_seconds')::integer < 60
     or (p_metadata->>'expires_in_seconds')::integer > 86400
     or p_expires_at is null or p_expires_at <= v_now
     or p_expires_at > v_now + interval '24 hours 15 seconds'
  then
    raise exception 'elo_authz_atomic_grant_expiry_invalid' using errcode = '22023';
  end if;

  if p_operation like 'continue_objective:%' and (
     p_authorization_state <> 'elo-execution-authorized'
     or p_metadata->>'resource_id' is distinct from substring(p_operation from 20)
     or nullif(btrim(p_metadata->>'tenant_id'), '') is null
  ) then
    raise exception 'elo_authz_atomic_objective_binding_invalid' using errcode = '22023';
  end if;

  -- These are relational integrity checks; elo-authz owns actual authorization.
  if not exists (
    select 1 from public.elo_operator_github_bindings b
    where b.binding_id = p_binding_id and b.identity_id = p_identity_id
      and b.repository_full_name = p_repository_full_name and b.active
  ) or not exists (
    select 1 from public.elo_identity_roles ir
    join public.elo_roles r on r.role_id = ir.role_id
    where ir.identity_id = p_issued_by_identity_id
      and r.code = 'CANONICAL_ADMIN' and r.active
  ) or not exists (
    select 1 from public.elo_identity_sessions s
    where s.session_id = p_issuer_session_id
      and s.identity_id = p_issued_by_identity_id
      and s.revoked_at is null and s.issued_at <= v_now and s.expires_at > v_now
  ) or not exists (
    select 1 from public.elo_identity_sessions s
    where s.session_id = p_session_id and s.identity_id = p_identity_id
      and s.revoked_at is null and s.issued_at <= v_now and s.expires_at > v_now
  ) then
    raise exception 'elo_authz_atomic_grant_identity_session_or_binding_invalid'
      using errcode = '42501';
  end if;

  insert into public.elo_authorization_grants (
    binding_id, identity_id, session_id, authorization_state,
    operation, repository_full_name, issued_by_identity_id,
    request_id, issued_at, expires_at, revoked_at, metadata
  ) values (
    p_binding_id, p_identity_id, p_session_id, p_authorization_state,
    p_operation, p_repository_full_name, p_issued_by_identity_id,
    p_request_id, v_now, p_expires_at, null, p_metadata
  )
  on conflict (issued_by_identity_id, request_id) do nothing
  returning * into v_grant;

  if not found then
    -- A retry returns the original grant, never extends its expiry.
    select * into v_grant from public.elo_authorization_grants g
    where g.issued_by_identity_id = p_issued_by_identity_id
      and g.request_id = p_request_id;
    if not found or v_grant.binding_id is distinct from p_binding_id
       or v_grant.identity_id is distinct from p_identity_id
       or v_grant.session_id is distinct from p_session_id
       or v_grant.authorization_state is distinct from p_authorization_state
       or v_grant.operation is distinct from p_operation
       or v_grant.repository_full_name is distinct from p_repository_full_name
       or v_grant.metadata is distinct from p_metadata
       or v_grant.revoked_at is not null or v_grant.expires_at <= v_now
       or not exists (
         select 1 from public.elo_authorization_audit a
         where a.request_id = p_request_id
           and a.identity_id = p_issued_by_identity_id
           and a.session_id = p_issuer_session_id
           and a.action = 'issue_authorization_grant'
           and a.resource = p_repository_full_name
           and a.decision = 'ALLOW'
           and a.reason = 'canonical_admin_issued_authorization_state'
           and a.created_at >= v_grant.issued_at
       )
    then
      raise exception 'elo_authz_atomic_grant_request_replay_mismatch'
        using errcode = '42501';
    end if;
    return v_grant;
  end if;

  -- An error here rolls back the grant INSERT in the same RPC transaction.
  insert into public.elo_authorization_audit (
    identity_id, session_id, action, resource, decision, reason, request_id
  ) values (
    p_issued_by_identity_id, p_issuer_session_id,
    'issue_authorization_grant', p_repository_full_name,
    'ALLOW', 'canonical_admin_issued_authorization_state', p_request_id
  );
  return v_grant;
end
$elo_atomic$;

-- public is exposed to PostgREST. This function is service_role-only.
revoke all on function public.elo_atomic_issue_authorization_grant(
  uuid, uuid, uuid, text, text, text, uuid, uuid, text, timestamptz, jsonb
) from public, anon, authenticated;
grant execute on function public.elo_atomic_issue_authorization_grant(
  uuid, uuid, uuid, text, text, text, uuid, uuid, text, timestamptz, jsonb
) to service_role;
comment on function public.elo_atomic_issue_authorization_grant(
  uuid, uuid, uuid, text, text, text, uuid, uuid, text, timestamptz, jsonb
) is 'ELO #1172: transactional grant+audit persistence adapter for elo-authz; service_role only.';
commit;
