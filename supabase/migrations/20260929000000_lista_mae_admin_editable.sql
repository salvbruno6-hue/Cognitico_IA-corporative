-- ELO governance: allow admin to edit Lista-Mãe.
--
-- Context:
-- - lista_mae is a Multiteiner corporate table linked to PCP
-- - Current trigger requires app.lista_mae_aprovada = 'SIM'
--   for any INSERT/UPDATE/DELETE
-- - The gateway does not set this GUC, blocking all writes
-- - Admin human must be able to edit directly
--
-- Decision (ADR-0017):
-- - Trigger accepts three authorization sources:
--   1. GUC app.lista_mae_aprovada = 'SIM' (gateway authorized)
--   2. elo_private.has_capability('PCP_ADMIN')
--   3. auth.jwt() -> 'app_metadata' ->> 'role' = 'admin'
-- - Audit trail preserved (lista_mae_alteracoes)
-- - RLS unchanged (p_pcp_* stay active)

create or replace function public.lista_mae_guard()
returns trigger
language plpgsql
security definer
set search_path = pg_catalog, public
as $function$
declare
  v_aprovado text;
  v_tem_cap boolean;
  v_jwt_role text;
begin
  -- Fonte 1: GUC de sessão (fluxo gateway autorizado)
  v_aprovado := current_setting('app.lista_mae_aprovada', true);

  -- Fonte 2: capability PCP_ADMIN
  begin
    v_tem_cap := elo_private.has_capability('PCP_ADMIN');
  exception when others then
    v_tem_cap := false;
  end;

  -- Fonte 3: app_metadata.role = 'admin' (JWT Supabase Auth)
  begin
    v_jwt_role := auth.jwt() -> 'app_metadata' ->> 'role';
  exception when others then
    v_jwt_role := null;
  end;

  if coalesce(v_aprovado, '') <> 'SIM'
     and coalesce(v_tem_cap, false) = false
     and coalesce(v_jwt_role, '') <> 'admin' then
    raise exception
      'ALTERAÇÃO BLOQUEADA: a Lista-Mãe exige aprovação explícita ou capability administrativa.';
  end if;

  insert into public.lista_mae_alteracoes (
    operacao,
    cod_produt,
    dados_antes,
    dados_depois,
    aprovado,
    aprovado_em
  ) values (
    tg_op,
    coalesce(new.cod_produt, old.cod_produt),
    case when tg_op in ('UPDATE', 'DELETE') then to_jsonb(old) else null end,
    case when tg_op in ('INSERT', 'UPDATE') then to_jsonb(new) else null end,
    true,
    now()
  );

  return coalesce(new, old);
end;
$function$;

comment on function public.lista_mae_guard()
is 'Lista-Mãe guard. Allows INSERT/UPDATE/DELETE when: (1) GUC app.lista_mae_aprovada=SIM, (2) capability PCP_ADMIN, or (3) JWT app_metadata.role=admin. Always writes to lista_mae_alteracoes. Per ADR-0017.';
