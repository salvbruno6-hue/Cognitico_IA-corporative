-- ELO operator/GitHub binding and explicit authorization-state evidence.
-- Structural change: bindings are persistent evidence; authorization states are
-- consumed by execution layers and are never generated from Codex output.

create table if not exists public.elo_operator_github_bindings (
  binding_id uuid primary key default gen_random_uuid(),
  identity_id uuid not null references public.elo_identity_registry(identity_id) on delete cascade,
  github_user_id bigint not null,
  github_login text not null,
  repository_full_name text not null,
  operation_class text not null check (operation_class in ('OPERATIONAL','STRUCTURAL')),
  active boolean not null default true,
  verified_at timestamptz not null default now(),
  verified_by_identity_id uuid references public.elo_identity_registry(identity_id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (identity_id, repository_full_name),
  unique (github_user_id, repository_full_name)
);

create table if not exists public.elo_authorization_grants (
  grant_id uuid primary key default gen_random_uuid(),
  binding_id uuid not null references public.elo_operator_github_bindings(binding_id) on delete cascade,
  identity_id uuid not null references public.elo_identity_registry(identity_id) on delete cascade,
  session_id uuid references public.elo_identity_sessions(session_id) on delete set null,
  authorization_state text not null check (
    authorization_state in (
      'elo-execution-authorized',
      'elo-commit-authorized',
      'elo-merge-authorized'
    )
  ),
  operation text not null,
  repository_full_name text not null,
  issued_by_identity_id uuid references public.elo_identity_registry(identity_id) on delete set null,
  request_id text not null,
  issued_at timestamptz not null default now(),
  expires_at timestamptz not null,
  revoked_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  constraint elo_authorization_grants_valid_window check (expires_at > issued_at)
);

create index if not exists idx_elo_operator_github_bindings_identity
  on public.elo_operator_github_bindings(identity_id, active);

create index if not exists idx_elo_operator_github_bindings_github
  on public.elo_operator_github_bindings(github_user_id, repository_full_name, active);

create index if not exists idx_elo_authorization_grants_lookup
  on public.elo_authorization_grants(
    binding_id, authorization_state, operation, repository_full_name, expires_at
  );

alter table public.elo_operator_github_bindings enable row level security;
alter table public.elo_authorization_grants enable row level security;

revoke all on public.elo_operator_github_bindings from anon, authenticated;
revoke all on public.elo_authorization_grants from anon, authenticated;
