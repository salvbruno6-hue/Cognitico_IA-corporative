-- Durable Objective Continuity checkpoint store for the canonical ELO Web runtime.
-- Cognitive decisions remain in ELO Web; this table is persistence only.
-- Authorization remains exclusively owned by elo-authz / elo_authorization_grants.

create table if not exists public.elo_objective_continuity_checkpoints (
  tenant_id text not null,
  objective_id text not null,
  workstream_id text not null,
  objective_title text not null,
  status text not null default 'ACTIVE' check (status in ('ACTIVE','COMPLETED','HUMAN_APPROVAL_REQUIRED','BLOCKED','FAILED')),
  stage text not null default 'OBJECTIVE_CONTINUITY',
  next_action text not null,
  iteration integer not null default 1 check (iteration >= 1),
  state_version integer not null default 1 check (state_version >= 1),
  last_progress_token text not null,
  no_progress_streak integer not null default 0 check (no_progress_streak >= 0),
  last_decision text not null check (last_decision in ('CONTINUE','CORRECT','REPLAN','ESCALATE','COMPLETE')),
  evidence_refs jsonb not null default '[]'::jsonb check (jsonb_typeof(evidence_refs) = 'array'),
  authorization_evidence_ref text not null,
  authorization_identity_id text not null,
  human_required boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (tenant_id, objective_id, workstream_id)
);

create index if not exists idx_elo_objective_continuity_updated_at
  on public.elo_objective_continuity_checkpoints (updated_at desc);

alter table public.elo_objective_continuity_checkpoints enable row level security;

-- The browser/user roles never access this persistence table directly. The ELO Web
-- server writes only after elo-authz has verified an explicit, unexpired objective
-- continuation grant for operation continue_objective:<objective_id>.
revoke all on table public.elo_objective_continuity_checkpoints from anon, authenticated;
grant select, insert, update, delete on table public.elo_objective_continuity_checkpoints to service_role;
