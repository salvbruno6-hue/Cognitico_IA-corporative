-- ELO-LEARN-001 / #532
-- Persistent GitHub operator binding and explicit governed authorization states.
-- Extends the canonical elo-authz authority; it does not create a parallel authority.

create table if not exists public.elo_operator_github_bindings (
  binding_id uuid primary key default gen_random_uuid(),
  identity_id uuid not null references public.elo_identity_registry(identity_id) on delete cascade,
  github_user_id bigint not null,
  github_login text not null,
  authentication_binding_method text not null,
  active boolean not null default true,
  established_at timestamptz not null default now(),
  revoked_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  constraint elo_operator_github_bindings_login_nonempty check (length(trim(github_login)) > 0),
  constraint elo_operator_github_bindings_revoked_after_established check (revoked_at is null or revoked_at >= established_at),
  unique (identity_id, github_user_id)
);

create table if not exists public.elo_operator_authorization_states (
  authorization_state_id uuid primary key default gen_random_uuid(),
  binding_id uuid not null references public.elo_operator_github_bindings(binding_id) on delete cascade,
  identity_id uuid not null references public.elo_identity_registry(identity_id) on delete cascade,
  session_id uuid not null references public.elo_identity_sessions(session_id) on delete cascade,
  repository text not null,
  operation_class text not null check (operation_class in ('OPERATIONAL','STRUCTURAL')),
  state text not null check (state in ('elo-execution-authorized','elo-commit-authorized','elo-merge-authorized')),
  issued_by text not null check (issued_by = 'elo-authz'),
  request_id text not null,
  issued_at timestamptz not null default now(),
  expires_at timestamptz not null,
  revoked_at timestamptz,
  evidence jsonb not null default '{}'::jsonb,
  constraint elo_operator_authorization_states_repo_nonempty check (length(trim(repository)) > 0),
  constraint elo_operator_authorization_states_valid_window check (expires_at > issued_at),
  constraint elo_operator_authorization_states_revoked_after_issue check (revoked_at is null or revoked_at >= issued_at)
);

create unique index if not exists uq_elo_operator_github_binding_active_identity
  on public.elo_operator_github_bindings(identity_id) where active = true and revoked_at is null;
create unique index if not exists uq_elo_operator_github_binding_active_github
  on public.elo_operator_github_bindings(github_user_id) where active = true and revoked_at is null;
create index if not exists idx_elo_operator_auth_state_lookup
  on public.elo_operator_authorization_states(identity_id, repository, state, expires_at desc);

alter table public.elo_operator_github_bindings enable row level security;
alter table public.elo_operator_authorization_states enable row level security;
revoke all on public.elo_operator_github_bindings from anon, authenticated;
revoke all on public.elo_operator_authorization_states from anon, authenticated;

insert into public.elo_capabilities (code, description) values
  ('EXECUTE', 'Autoriza execução governada em repositório vinculado'),
  ('COMMIT', 'Autoriza commit governado em repositório vinculado'),
  ('MERGE_OPERATIONAL', 'Autoriza merge operacional após gates governados')
on conflict (code) do nothing;

-- No role receives these capabilities automatically here.
-- Assignment remains an explicit canonical governance operation.
