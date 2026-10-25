-- Durable Objective Continuity checkpoint store for the canonical ELO Web runtime.
-- Cognitive decisions remain in ELO Web; this table is persistence only.

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

revoke all on table public.elo_objective_continuity_checkpoints from anon, authenticated;
grant select, insert, update, delete on table public.elo_objective_continuity_checkpoints to service_role;

-- Autonomous objective continuation is an explicit ELO capability. It is granted
-- only to the canonical administrative role at this stage; elo-authz remains the
-- authority that evaluates the authenticated identity on every cycle.
insert into public.elo_capabilities (code, name, description, active)
values (
  'OBJECTIVE_CONTINUE',
  'Continuar objetivo ELO',
  'Permite executar um ciclo governado de Objective Continuity sem nova aprovação conversacional.',
  true
)
on conflict (code) do update
set name = excluded.name,
    description = excluded.description,
    active = true;

insert into public.elo_role_capabilities (role_id, capability_id)
select r.role_id, c.capability_id
from public.elo_roles r
join public.elo_capabilities c on c.code = 'OBJECTIVE_CONTINUE'
where r.code = 'CANONICAL_ADMIN' and r.active = true
on conflict do nothing;
