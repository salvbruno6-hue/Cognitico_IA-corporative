-- ELO PCP read RLS hardening — batch 1
-- Scope: SELECT only, on tenant-bearing PCP tables.
-- No write capability is granted or modified here.

create or replace function elo_private.can_read_pcp_tenant(p_tenant_id uuid)
returns boolean
language sql
stable
security definer
set search_path = pg_catalog, public
as $$
select
  p_tenant_id is not null
  and exists (
    select 1
    from public.mt_tenants t
    where t.id = p_tenant_id
      and t.ativo
  )
  and exists (
    select 1
    from public.elo_identity_registry i
    join public.elo_identity_roles ir
      on ir.identity_id = i.identity_id
    join public.elo_role_capabilities rc
      on rc.role_id = ir.role_id
    join public.elo_capabilities c
      on c.capability_id = rc.capability_id
     and c.active
    where i.auth_user_id = auth.uid()
      and i.active
      and c.code = 'PCP_READ'
  )
  and exists (
    select 1
    from public.elo_identity_registry i
    join public.elo_identity_scopes eis
      on eis.identity_id = i.identity_id
    join public.elo_scopes s
      on s.scope_id = eis.scope_id
     and s.active
    join public.mt_tenants t
      on t.id = p_tenant_id
     and t.ativo
    where i.auth_user_id = auth.uid()
      and i.active
      and s.scope_type = 'ENTERPRISE'
      and s.scope_key = t.codigo
  )
  and exists (
    select 1
    from public.elo_identity_registry i
    join public.elo_identity_scopes eis
      on eis.identity_id = i.identity_id
    join public.elo_scopes s
      on s.scope_id = eis.scope_id
     and s.active
    where i.auth_user_id = auth.uid()
      and i.active
      and s.scope_type = 'DOMAIN'
      and s.scope_key = 'PCP-LISTA-MAE'
  );
$$;

revoke all on function elo_private.can_read_pcp_tenant(uuid) from public;
grant execute on function elo_private.can_read_pcp_tenant(uuid) to authenticated;

comment on function elo_private.can_read_pcp_tenant(uuid) is
'Fail-closed PCP read predicate: active identity + explicit PCP_READ capability + enterprise scope matching tenant code + DOMAIN/PCP-LISTA-MAE. No write authority.';

drop policy if exists p_mt_planos_pcp_read on public.mt_planos_pcp;
create policy p_mt_planos_pcp_read
on public.mt_planos_pcp
for select
to authenticated
using (elo_private.can_read_pcp_tenant(tenant_id));

drop policy if exists p_mt_ordens_producao_read on public.mt_ordens_producao;
create policy p_mt_ordens_producao_read
on public.mt_ordens_producao
for select
to authenticated
using (elo_private.can_read_pcp_tenant(tenant_id));
