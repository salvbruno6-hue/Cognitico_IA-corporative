-- Layer: tenant / Multiteiner
-- Governed decision: create the operational MULTITEINER tenant and bind only
-- the explicitly confirmed 300-unit M01 requirement. Do not backfill repairs.
-- GitHub remains implementation/governance authority; Supabase remains
-- persistent operational authority.

begin;

insert into public.mt_tenants (codigo, nome, ativo)
values ('MULTITEINER', 'Multiteiner', true)
on conflict (codigo) do nothing;

do $$
declare
  v_tenant_id uuid;
  v_tenant_nome text;
  v_tenant_ativo boolean;
  v_requirement_count integer;
begin
  select id, nome, ativo
    into v_tenant_id, v_tenant_nome, v_tenant_ativo
  from public.mt_tenants
  where codigo = 'MULTITEINER';

  if v_tenant_id is null then
    raise exception 'MULTITEINER tenant was not created/resolved';
  end if;

  if v_tenant_nome <> 'Multiteiner' or v_tenant_ativo is not true then
    raise exception 'Existing MULTITEINER tenant conflicts with governed identity: nome=%, ativo=%', v_tenant_nome, v_tenant_ativo;
  end if;

  select count(*)
    into v_requirement_count
  from elo_private.pcp_requisitos_fisicos_planejamento r
  join public.modelos m on m.id = r.modelo_id
  where m.codigo = 'M01'
    and r.quantidade_objetivo = 300
    and r.data_limite = date '2027-01-31'
    and r.origem = 'CONFIRMACAO_USUARIO_CHAT_2026-10-21'
    and r.fonte_referencia = 'user://planejamento-demanda-fluxo-modular/2026-10-21';

  if v_requirement_count <> 1 then
    raise exception 'Expected exactly one governed 300-unit M01 requirement, found %', v_requirement_count;
  end if;

  update elo_private.pcp_requisitos_fisicos_planejamento r
  set tenant_id = v_tenant_id
  from public.modelos m
  where m.id = r.modelo_id
    and m.codigo = 'M01'
    and r.quantidade_objetivo = 300
    and r.data_limite = date '2027-01-31'
    and r.origem = 'CONFIRMACAO_USUARIO_CHAT_2026-10-21'
    and r.fonte_referencia = 'user://planejamento-demanda-fluxo-modular/2026-10-21'
    and (r.tenant_id is null or r.tenant_id = v_tenant_id);
end
$$;

commit;

-- Explicit non-actions:
-- * no UPDATE to public.mt_ordens_reparo;
-- * no backfill of legacy repair tenant_id;
-- * no elo_identity_scopes mutation;
-- * no RLS/policy expansion.
