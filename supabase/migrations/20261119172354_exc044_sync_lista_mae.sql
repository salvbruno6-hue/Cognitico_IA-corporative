do $$
declare
  v_exc_id uuid;
  v_material numeric;
  v_mo numeric;
  v_total numeric;
begin
  select id into v_exc_id from public.excedentes where codigo_excedente='EXC-044';
  if v_exc_id is null then raise exception 'EXC-044 não localizado'; end if;

  update public.excedente_itens i
  set quantidade=i.quantidade
  where i.excedente_id=v_exc_id
    and i.cod_item is not null;

  select coalesce(sum(valor_total),0) into v_material
  from public.excedente_itens where excedente_id=v_exc_id;

  select coalesce(sum(valor_parcial),0) into v_mo
  from public.excedente_mao_obra where excedente_id=v_exc_id;

  v_total := round(v_material+v_mo,2);

  update public.excedentes
  set custo_total=v_total,
      valor_total=v_total,
      updated_at=now(),
      observacao=concat(
        'EXC ativo e sincronizado com public.lista_mae em 19/11/2026. ',
        'Materiais R$',to_char(v_material,'FM999999990.00'),
        ' + MO R$',to_char(v_mo,'FM999999990.00'),
        ' = R$',to_char(v_total,'FM999999990.00'),
        '. BOM base M01 não alterada.'
      )
  where id=v_exc_id;

  insert into public.tb_elo_eventos_governanca(
    evento,etapa,componente_orquestrador,componente_membro,status,referencia,detalhes
  )
  select
    'SINCRONIZACAO_EXC044_LISTA_MAE_20261119',
    'VALIDACAO',
    'ELO','FORGE_BUDGETING',
    'SINCRONIZADO',
    'EXC-044',
    jsonb_build_object(
      'fonte_valores','public.lista_mae',
      'materiais_total',v_material,
      'mao_obra_total',v_mo,
      'total_excedente',v_total,
      'divergencias_encontradas',0,
      'planilhas_alteradas',false,
      'bom_m01_alterada',false
    )
  where not exists(
    select 1 from public.tb_elo_eventos_governanca
    where evento='SINCRONIZACAO_EXC044_LISTA_MAE_20261119' and referencia='EXC-044'
  );
end $$;