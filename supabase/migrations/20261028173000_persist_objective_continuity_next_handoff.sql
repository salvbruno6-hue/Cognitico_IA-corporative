-- Persist the next governed GPT -> ELO handoff alongside the canonical checkpoint.
-- This does not add a second store: the handoff is derived state owned by the
-- same Objective Continuity checkpoint and version.

alter table public.elo_objective_continuity_checkpoints
  add column if not exists next_trigger jsonb null,
  add column if not exists next_elo_prompt text null;

do $$
begin
  if not exists (
    select 1
    from pg_constraint
    where conname = 'elo_objective_continuity_next_trigger_object_chk'
      and conrelid = 'public.elo_objective_continuity_checkpoints'::regclass
  ) then
    alter table public.elo_objective_continuity_checkpoints
      add constraint elo_objective_continuity_next_trigger_object_chk
      check (next_trigger is null or jsonb_typeof(next_trigger) = 'object');
  end if;
end
$$;

comment on column public.elo_objective_continuity_checkpoints.next_trigger is
'Persisted next GPT->ELO trigger derived from the same checkpoint version; null for terminal/human-required states.';

comment on column public.elo_objective_continuity_checkpoints.next_elo_prompt is
'Persisted complete NEXT_ELO_PROMPT derived from the checkpoint; never an independent authority or substitute checkpoint.';
