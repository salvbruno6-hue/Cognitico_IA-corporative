-- Governed external data-source registry.
-- Secrets are never stored here. Runtime resolves credential_ref/connection_ref
-- through the connector boundary after elo-authz approval.

create table if not exists public.elo_data_sources (
  data_source_id uuid primary key default gen_random_uuid(),
  source_key text not null unique,
  display_name text not null,
  source_kind text not null check (source_kind in ('ELO_CANONICAL','ENTERPRISE_EXTERNAL','USER_EXTERNAL','INTEGRATION')),
  connector_kind text not null,
  scope_id uuid not null references public.elo_scopes(scope_id),
  credential_ref text not null,
  connection_ref text,
  status text not null default 'ACTIVE' check (status in ('ACTIVE','SUSPENDED','REVOKED')),
  metadata jsonb not null default '{}'::jsonb,
  created_by_identity_id uuid references public.elo_identity_registry(identity_id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.elo_identity_data_source_access (
  identity_id uuid not null references public.elo_identity_registry(identity_id) on delete cascade,
  data_source_id uuid not null references public.elo_data_sources(data_source_id) on delete cascade,
  allowed_operations text[] not null default array['metadata_read','read','query'],
  active boolean not null default true,
  granted_by_identity_id uuid references public.elo_identity_registry(identity_id),
  granted_at timestamptz not null default now(),
  primary key (identity_id, data_source_id),
  check (
    allowed_operations <@ array['metadata_read','read','query','write','schema_change']::text[]
  )
);

create index if not exists idx_elo_data_sources_scope
  on public.elo_data_sources(scope_id);

create index if not exists idx_elo_identity_data_source_access_source
  on public.elo_identity_data_source_access(data_source_id);

alter table public.elo_data_sources enable row level security;
alter table public.elo_identity_data_source_access enable row level security;

-- Runtime connector access uses a server-side privileged client after
-- elo-authz has authorized the request. Direct browser/Data API access is denied.
create policy "elo_data_sources_api_deny_all"
  on public.elo_data_sources
  for all
  to anon, authenticated
  using (false)
  with check (false);

create policy "elo_identity_data_source_access_api_deny_all"
  on public.elo_identity_data_source_access
  for all
  to anon, authenticated
  using (false)
  with check (false);

revoke all on table public.elo_data_sources from anon, authenticated;
revoke all on table public.elo_identity_data_source_access from anon, authenticated;
grant select, insert, update, delete on table public.elo_data_sources to service_role;
grant select, insert, update, delete on table public.elo_identity_data_source_access to service_role;
