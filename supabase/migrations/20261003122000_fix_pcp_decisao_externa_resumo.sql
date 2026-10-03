-- Corrige o resumo decisorio para retornar uma linha mesmo quando ainda nao existem dados operacionais.
create or replace view public.v_elo_pcp_decisao_externa_resumo
with (security_invoker=true)
as
with d as (
  select * from public.v_elo_pcp_decisao_externa_detalhe
),
comercial as (
  select count(distinct pedido_venda_id) as pedidos_comerciais,
         coalesce(sum(quantidade),0) as unidades_comerciais
  from public.v_elo_pcp_demanda_comercial
),
operacao as (
  select count(*) filter (where coalesce(status,'PLANEJADO') not in ('CANCELADO','CANCELADA')) as ordens_externas,
         coalesce(sum(horas_planejadas) filter (where coalesce(status,'PLANEJADO') not in ('CANCELADO','CANCELADA')),0) as horas_planejadas_externas
  from public.mt_ordens_montagem_externa
),
fatores as (
  select count(*) filter (where estado_fator='FATOR_CALCULADO') as fatores_calculados,
         count(*) filter (where estado_fator='FATOR_CALCULADO' and variacao_percentual>0) as fatores_crescimento,
         count(*) filter (where estado_fator='FATOR_CALCULADO' and variacao_percentual<0) as fatores_reducao,
         count(*) filter (where estado_comparabilidade='COMPARAVEL_POTENCIAL') as comparaveis_potenciais
  from d
),
gaps as (
  select count(*) filter (where gaps_composicao>0) as linhas_com_gap_composicao,
         count(*) filter (where proxima_informacao_decisoria<>'VALIDAR_IMPACTO_PROJETADO_COM_OPERACAO_E_RH') as linhas_com_informacao_pendente
  from d
),
fonte_demanda as (
  select count(*) as historico_registros,
         coalesce(sum(quantidade_historica),0) as historico_unidades,
         coalesce(sum(quantidade_prevista),0) as previsao_unidades
  from (
    select distinct tenant_id,modelo_id,natureza_demanda,chave_comparabilidade,quantidade_historica,quantidade_prevista
    from public.v_elo_pcp_referencia_demanda_comparavel
  ) x
)
select
  now() as atualizado_em,
  case
    when fd.historico_registros=0 then 'AGUARDANDO_HISTORICO'
    when fd.previsao_unidades=0 then 'AGUARDANDO_PREVISAO'
    when ft.fatores_calculados=0 then 'AGUARDANDO_VALIDACAO_DE_COMPARABILIDADE'
    when gg.linhas_com_gap_composicao>0 then 'AGUARDANDO_COMPOSICAO_OPERACIONAL'
    else 'ANALISE_DISPONIVEL_PARA_VALIDACAO'
  end as estado_decisao,
  c.pedidos_comerciais,
  c.unidades_comerciais,
  fd.historico_registros,
  fd.historico_unidades,
  fd.previsao_unidades,
  ft.comparaveis_potenciais,
  ft.fatores_calculados,
  ft.fatores_crescimento,
  ft.fatores_reducao,
  o.ordens_externas,
  o.horas_planejadas_externas,
  coalesce((select sum(x.demanda_humana_historica_media_dia) from d x where x.demanda_humana_historica_media_dia is not null),0) as demanda_humana_historica_media_total_dia,
  coalesce((select sum(x.demanda_humana_projetada_media_dia) from d x where x.demanda_humana_projetada_media_dia is not null),0) as demanda_humana_projetada_media_total_dia,
  gg.linhas_com_gap_composicao,
  gg.linhas_com_informacao_pendente,
  jsonb_build_object(
    'impactos_a_observar',jsonb_build_array(
      'volume_comercial','variacao_da_demanda_comparavel','horas_planejadas_de_operacao_externa',
      'demanda_humana_historica_por_funcao','demanda_humana_projetada_por_funcao','gaps_de_composicao'
    ),
    'informacoes_que_aumentam_precisao',jsonb_build_array(
      'chave_de_comparabilidade_validada','previsao_por_modelo_e_natureza','historico_real_por_modelo_e_natureza',
      'ordens_externas_com_inicio_fim_e_horas_planejadas','composicao_funcional_validada','historico_humano_por_funcao',
      'confiabilidade_da_previsao','origem_comercial_rastreavel'
    ),
    'regra','Nao transformar crescimento de demanda em crescimento de quadro de RH sem produtividade, composicao e validacao operacional.'
  ) as guia_decisao
from comercial c
cross join operacao o
cross join fatores ft
cross join gaps gg
cross join fonte_demanda fd;