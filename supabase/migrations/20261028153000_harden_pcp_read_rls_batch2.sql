-- ELO PCP read RLS hardening — batch 2
-- Scope: SELECT only on mt_linhas_plano_pcp.
-- Child visibility is derived from the governed tenant of the parent PCP plan.

create or replace function elo_private.can_read_pcp_plan(p_plan_id uuid)
returns boolean
language sql
stable
security definer
set search_path = pg_catalog, public
as $$
select exists (
  select 1
  from public.mt_planos_pcp p
  where p.id = p_plan_id
    and elo_private.can_read_pcp_tenant(p.tenant_id)
);
$$;

revoke all on function elo_private.can_read_pcp_plan(uuid) from public;
grant execute on function elo_private.can_read_pcp_plan(uuid) to authenticated;

comment on function elo_private.can_read_pcp_plan(uuid) is
'Fail-closed PCP child-read predicate. Delegates identity, active role, PCP_READ capability, enterprise and domain checks to elo_private.can_read_pcp_tenant using the parent plan tenant.';

drop policy if exists p_mt_linhas_plano_pcp_read on public.mt_linhas_plano_pcp;
create policy p_mt_linhas_plano_pcp_read
on public.mt_linhas_plano_pcp
for select
to authenticated
using (elo_private.can_read_pcp_plan(plano_pcp_id));
