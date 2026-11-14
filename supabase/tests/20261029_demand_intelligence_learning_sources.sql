-- Contract checks for ELO Demand Intelligence source integration.
-- The test is read-only and must fail when the governed associations are missing.

do $$
declare
  missing_count integer;
  demand_count integer;
begin
  select count(*) into missing_count
  from (values
    ('public','mt_pedidos_venda'),
    ('public','mt_demanda_historico'),
    ('public','mt_previsoes_demanda'),
    ('public','mt_balanco_demanda'),
    ('public','v_elo_diretoria_comercial_estoque'),
    ('public','v_elo_pcp_demanda_fluxo_patio'),
    ('public','mt_devolucoes'),
    ('public','mt_devolucao_itens'),
    ('public','mt_planos_pcp'),
    ('public','mt_linhas_plano_pcp'),
    ('public','mt_ordens_producao'),
    ('public','mt_capacidade_diaria')
  ) as required(schema_name, table_name)
  where not exists (
    select 1
    from public.elo_aprendizado_fontes f
    where f.schema_name = required.schema_name
      and f.table_name = required.table_name
      and f.enabled = true
      and f.extracao_ativa = true
  );

  if missing_count <> 0 then
    raise exception 'Demand Intelligence source integration incomplete: % source(s) missing', missing_count;
  end if;

  select count(*) into demand_count
  from public.elo_aprendizado_demanda
  where metodo = 'ORDEM_COGNITIVA_DEMANDA_INTELIGENTE_V1'
    and status = 'CANDIDATO'
    and premissas @> '{"retorno_nao_e_disponibilidade": true, "previsao_nao_e_fato": true, "previsto_realizado_fecha_aprendizado": true}'::jsonb
    and sinais_demanda ? 'cadeia_integrada'
    and sinais_demanda ? 'classes_epistemicas';

  if demand_count <> 1 then
    raise exception 'Existing Demand Intelligence learning candidate was not enriched exactly once';
  end if;
end $$;
