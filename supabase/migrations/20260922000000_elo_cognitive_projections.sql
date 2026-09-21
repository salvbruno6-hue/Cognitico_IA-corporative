-- Migration: cognitive read-only projections
-- Adds three projection tables for cognitive state exposed via MCP.
-- Populated by external jobs from canonical sources in the repository
-- (memory/). They do NOT replace the canonical source.
-- Read-only for authenticated; no write policies (fail-closed).

-- ---------------------------------------------------------------------------
-- elo_dol_projection — Decision Outcome Loop projection
-- ---------------------------------------------------------------------------
create table if not exists public.elo_dol_projection (
  decision_id text primary key,
  state text not null check (state in (
    'proposed','approved','executed','observing','evaluated',
    'attributed','learned','closed','escalated','reverted'
  )),
  sector text,
  decision_type text,
  confidence_declared numeric,
  confidence_calibrated numeric,
  outcome text,
  attribution text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_elo_dol_projection_state
  on public.elo_dol_projection (state);
create index if not exists idx_elo_dol_projection_sector
  on public.elo_dol_projection (sector);
create index if not exists idx_elo_dol_projection_decision_type
  on public.elo_dol_projection (decision_type);

alter table public.elo_dol_projection enable row level security;
drop policy if exists "read_dol_projection_authenticated" on public.elo_dol_projection;
create policy "read_dol_projection_authenticated"
  on public.elo_dol_projection for select
  to authenticated using (true);

-- ---------------------------------------------------------------------------
-- elo_calibration_model — confidence calibration projection
-- ---------------------------------------------------------------------------
create table if not exists public.elo_calibration_model (
  model_id text primary key,
  model jsonb not null,
  updated_at timestamptz not null default now()
);

alter table public.elo_calibration_model enable row level security;
drop policy if exists "read_calibration_model_authenticated" on public.elo_calibration_model;
create policy "read_calibration_model_authenticated"
  on public.elo_calibration_model for select
  to authenticated using (true);

-- ---------------------------------------------------------------------------
-- elo_precedent_index — decision precedent projection
-- ---------------------------------------------------------------------------
create table if not exists public.elo_precedent_index (
  precedent_id text primary key,
  decision_id text not null,
  sector text,
  decision_type text,
  confidence_band text,
  outcome text,
  created_at timestamptz not null default now()
);

create index if not exists idx_elo_precedent_index_sector
  on public.elo_precedent_index (sector);
create index if not exists idx_elo_precedent_index_decision_type
  on public.elo_precedent_index (decision_type);
create index if not exists idx_elo_precedent_index_confidence_band
  on public.elo_precedent_index (confidence_band);

alter table public.elo_precedent_index enable row level security;
drop policy if exists "read_precedent_index_authenticated" on public.elo_precedent_index;
create policy "read_precedent_index_authenticated"
  on public.elo_precedent_index for select
  to authenticated using (true);