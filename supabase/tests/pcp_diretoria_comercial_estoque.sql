-- Contract test: executive Commercial/PCP stock view.

do $$
declare
  missing_cols integer;
begin
  select count(*) into missing_cols
  from (
    values
      ('nivel_analise'),
      ('familia_produto'),
      ('periodo_mes'),
      ('demanda_spot'),
      ('demanda_evento'),
      ('indice_sazonalidade_pct'),
      ('crescimento_yoy_pct'),
      ('retornos_previstos'),
      ('estoque_minimo_spot'),
      ('estoque_seguranca_spot'),
      ('estoque_alvo_spot'),
      ('reserva_evento_referencia'),
      ('estoque_protecao_comercial_referencia'),
      ('estado_estoque'),
      ('nivel_alerta_elo'),
      ('orientacao_cognitiva_elo'),
      ('ferramenta_qualidade_recomendada')
  ) expected(column_name)
  where not exists (
    select 1
    from information_schema.columns c
    where c.table_schema='public'
      and c.table_name='v_elo_diretoria_comercial_estoque'
      and c.column_name=expected.column_name
  );

  if missing_cols > 0 then
    raise exception 'v_elo_diretoria_comercial_estoque missing % expected columns', missing_cols;
  end if;

  if exists (
    select 1
    from elo_private.pcp_diretoria_comercial_mensal
    where familia_produto not in ('MODULO','CONTEINER')
       or nivel_analise not in ('FAMILIA','MODELO')
       or tipo_registro not in ('HISTORICO','PREVISAO_BASE')
  ) then
    raise exception 'invalid executive baseline domain values';
  end if;

  if exists (
    select 1
    from public.v_elo_diretoria_comercial_estoque
    where unidade_medida='REGISTRO_EQUIVALENTE'
      and (saldo_vs_estoque_minimo is not null or saldo_vs_protecao_comercial is not null)
  ) then
    raise exception 'physical stock balance must stay null for registro-equivalente baseline';
  end if;
end $$;