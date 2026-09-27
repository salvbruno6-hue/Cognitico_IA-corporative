-- ELO read-only RLS state reader.
-- Reads pg_class.relrowsecurity and pg_policies for a given set
-- of tables in the public schema.
-- Read-only. Never executes DDL. Never mutates state.
--
-- Pattern: logic in elo_private (internal schema, not exposed);
-- public wrapper grants EXECUTE only to service_role.

create or replace function elo_private.read_rls_state(
  p_tables text[]
)
returns jsonb
language plpgsql
stable
security definer
set search_path = pg_catalog, public
as $$
declare
  v_result jsonb := '[]'::jsonb;
  v_table text;
  v_rls boolean;
  v_policies text[];
begin
  if p_tables is null or array_length(p_tables, 1) is null then
    return '[]'::jsonb;
  end if;

  foreach v_table in array p_tables loop
    select c.relrowsecurity
      into v_rls
      from pg_class c
      join pg_namespace n on n.oid = c.relnamespace
     where n.nspname = 'public'
       and c.relname = v_table
       and c.relkind = 'r';

    if not found then
      v_result := v_result || jsonb_build_object(
        'table', v_table,
        'rls_enabled', null,
        'policies', '[]'::jsonb,
        'error', 'table_not_found'
      );
      continue;
    end if;

    select coalesce(
             array_agg(p.policyname order by p.policyname),
             array[]::text[]
           )
      into v_policies
      from pg_policies p
     where p.schemaname = 'public'
       and p.tablename = v_table;

    v_result := v_result || jsonb_build_object(
      'table', v_table,
      'rls_enabled', v_rls,
      'policies', to_jsonb(v_policies)
    );
  end loop;

  return v_result;
end;
$$;

revoke all on function elo_private.read_rls_state(text[])
  from public, anon, authenticated;
grant execute on function elo_private.read_rls_state(text[])
  to service_role;

comment on function elo_private.read_rls_state(text[])
is 'Read-only RLS state reader. Returns JSONB array of {table, rls_enabled, policies} for the given public tables. Never executes DDL.';

create or replace function public.elo_read_rls_state(
  p_tables text[]
)
returns jsonb
language sql
stable
security definer
set search_path = pg_catalog, public
as $$
  select elo_private.read_rls_state(p_tables)
$$;

revoke all on function public.elo_read_rls_state(text[])
  from public, anon, authenticated;
grant execute on function public.elo_read_rls_state(text[])
  to service_role;

comment on function public.elo_read_rls_state(text[])
is 'Public wrapper for elo_private.read_rls_state. Executable only by service_role.';
