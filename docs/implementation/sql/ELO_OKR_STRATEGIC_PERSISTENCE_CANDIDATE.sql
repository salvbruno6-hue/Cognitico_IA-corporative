-- ELO strategic OKR persistence candidate.
-- APPROVED SCOPE: prepare migration only. DO NOT APPLY TO LIVE SUPABASE.
-- Owner: strategic-objective-domain
-- Access mode: backend-only/service-bound until a canonical tenant membership model exists.
-- Measurement persistence is intentionally out of scope.

create table if not exists public.elo_strategic_objectives (
  tenant_id text not null,
  objective_id text not null,
  title text not null,
  strategy_ref text,
  owner_ref text,
  evidence_refs text[] not null default '{}'::text[],
  authorization_ref text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  constraint elo_strategic_objectives_pkey
    primary key (tenant_id, objective_id),
  constraint elo_strategic_objectives_tenant_required
    check (btrim(tenant_id) <> ''),
  constraint elo_strategic_objectives_id_required
    check (btrim(objective_id) <> ''),
  constraint elo_strategic_objectives_title_required
    check (btrim(title) <> ''),
  constraint elo_strategic_objectives_authorization_required
    check (btrim(authorization_ref) <> '')
);

create table if not exists public.elo_strategic_key_results (
  tenant_id text not null,
  key_result_id text not null,
  objective_id text not null,
  title text not null,
  metric_code text not null,
  direction text not null,
  baseline numeric,
  target numeric,
  deadline date,
  weight numeric not null default 1,
  baseline_evidence_refs text[] not null default '{}'::text[],
  target_evidence_refs text[] not null default '{}'::text[],
  target_approval_state text not null default 'DRAFT',
  target_approval_ref text,
  authorization_ref text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  constraint elo_strategic_key_results_pkey
    primary key (tenant_id, key_result_id),
  constraint elo_strategic_key_results_objective_fkey
    foreign key (tenant_id, objective_id)
    references public.elo_strategic_objectives (tenant_id, objective_id)
    on delete cascade,
  constraint elo_strategic_key_results_metric_fkey
    foreign key (metric_code)
    references public.mt_definicoes_kpi (codigo_kpi),
  constraint elo_strategic_key_results_tenant_required
    check (btrim(tenant_id) <> ''),
  constraint elo_strategic_key_results_id_required
    check (btrim(key_result_id) <> ''),
  constraint elo_strategic_key_results_objective_required
    check (btrim(objective_id) <> ''),
  constraint elo_strategic_key_results_title_required
    check (btrim(title) <> ''),
  constraint elo_strategic_key_results_metric_required
    check (btrim(metric_code) <> ''),
  constraint elo_strategic_key_results_direction_valid
    check (direction in ('INCREASE', 'DECREASE', 'MAINTAIN')),
  constraint elo_strategic_key_results_weight_positive
    check (weight > 0),
  constraint elo_strategic_key_results_baseline_evidence_required
    check (baseline is null or cardinality(baseline_evidence_refs) > 0),
  constraint elo_strategic_key_results_target_evidence_required
    check (target is null or cardinality(target_evidence_refs) > 0),
  constraint elo_strategic_key_results_target_approval_state_valid
    check (target_approval_state in ('DRAFT', 'APPROVED')),
  constraint elo_strategic_key_results_approved_target_has_ref
    check (
      target_approval_state <> 'APPROVED'
      or nullif(btrim(target_approval_ref), '') is not null
    ),
  constraint elo_strategic_key_results_authorization_required
    check (btrim(authorization_ref) <> '')
);

create index if not exists idx_elo_strategic_objectives_tenant
  on public.elo_strategic_objectives (tenant_id);

create index if not exists idx_elo_strategic_key_results_objective
  on public.elo_strategic_key_results (tenant_id, objective_id);

create index if not exists idx_elo_strategic_key_results_metric
  on public.elo_strategic_key_results (metric_code);

-- Reuse the existing canonical ELO updated_at owner. Do not create a parallel function.
drop trigger if exists trg_elo_strategic_objectives_updated_at on public.elo_strategic_objectives;
create trigger trg_elo_strategic_objectives_updated_at
before update on public.elo_strategic_objectives
for each row execute function public.elo_cognitive_set_updated_at();

drop trigger if exists trg_elo_strategic_key_results_updated_at on public.elo_strategic_key_results;
create trigger trg_elo_strategic_key_results_updated_at
before update on public.elo_strategic_key_results
for each row execute function public.elo_cognitive_set_updated_at();

alter table public.elo_strategic_objectives enable row level security;
alter table public.elo_strategic_key_results enable row level security;

-- Fail closed at the Data API boundary. No authenticated client policy is created.
revoke all on table public.elo_strategic_objectives from anon, authenticated;
revoke all on table public.elo_strategic_key_results from anon, authenticated;

-- Explicit backend access. Tenant authorization remains an application/authz responsibility.
grant select, insert, update, delete on table public.elo_strategic_objectives to service_role;
grant select, insert, update, delete on table public.elo_strategic_key_results to service_role;

comment on table public.elo_strategic_objectives is
  'Tenant-scoped strategic Objective owner for ELO strategic_okr capability. Backend-only; authorization_ref preserves elo-authz provenance; no orchestration, evidence, decision or learning authority.';

comment on table public.elo_strategic_key_results is
  'Tenant-scoped KeyResult owner linked to the existing formal KPI registry. Backend-only; authorization_ref preserves elo-authz provenance; Measurement persistence remains separate.';
