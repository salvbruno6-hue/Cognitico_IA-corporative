-- ELO OKR Measurement binding candidate (M2).
-- PREPARED ONLY. DO NOT APPLY TO LIVE SUPABASE WITHOUT EXPLICIT AUTHORIZATION.
-- Owners preserved:
--   mt_definicoes_kpi     = formal KPI registry
--   mt_snapshots_kpi      = KPI snapshot values
--   elo_strategic_key_results = tenant-scoped KR
-- This table owns only KR <-> existing snapshot attribution plus evidence refs.

create table if not exists public.elo_strategic_kr_snapshot_bindings (
  binding_id uuid primary key default gen_random_uuid(),
  tenant_id text not null,
  key_result_id text not null,
  snapshot_id uuid not null,
  evidence_refs text[] not null,
  authorization_ref text not null,
  created_at timestamptz not null default now(),

  constraint elo_strategic_kr_snapshot_bindings_kr_fkey
    foreign key (tenant_id, key_result_id)
    references public.elo_strategic_key_results (tenant_id, key_result_id)
    on delete cascade,

  constraint elo_strategic_kr_snapshot_bindings_snapshot_fkey
    foreign key (snapshot_id)
    references public.mt_snapshots_kpi (id)
    on delete restrict,

  constraint elo_strategic_kr_snapshot_bindings_unique
    unique (tenant_id, key_result_id, snapshot_id),

  constraint elo_strategic_kr_snapshot_bindings_tenant_required
    check (btrim(tenant_id) <> ''),

  constraint elo_strategic_kr_snapshot_bindings_kr_required
    check (btrim(key_result_id) <> ''),

  constraint elo_strategic_kr_snapshot_bindings_evidence_required
    check (cardinality(evidence_refs) > 0),

  constraint elo_strategic_kr_snapshot_bindings_authorization_required
    check (btrim(authorization_ref) <> '')
);

create index if not exists idx_elo_strategic_kr_snapshot_bindings_kr
  on public.elo_strategic_kr_snapshot_bindings (tenant_id, key_result_id);

create index if not exists idx_elo_strategic_kr_snapshot_bindings_snapshot
  on public.elo_strategic_kr_snapshot_bindings (snapshot_id);

alter table public.elo_strategic_kr_snapshot_bindings enable row level security;

-- Fail closed at the Data API boundary.
revoke all on table public.elo_strategic_kr_snapshot_bindings from anon, authenticated;

-- Explicit backend access. Tenant authorization remains an application/authz responsibility.
grant select, insert, update, delete on table public.elo_strategic_kr_snapshot_bindings to service_role;

comment on table public.elo_strategic_kr_snapshot_bindings is
  'Tenant-scoped binding between an ELO strategic KR and an existing KPI snapshot. Owns attribution/evidence refs plus elo-authz authorization_ref only; does not own KPI definition or snapshot value.';
