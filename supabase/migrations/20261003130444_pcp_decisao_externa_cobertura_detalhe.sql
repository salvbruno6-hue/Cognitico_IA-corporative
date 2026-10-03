create or replace view public.v_elo_pcp_decisao_externa_detalhe
with (security_invoker = true)
as
with comercial as (
  select d.tenant_id,d.modelo_id,d.natureza_demanda,d.chave_comparabilidade,sum(d.quantidade) as quantidade_comercial_atual,
         count(distinct d.pedido_venda_id) as pedidos_comerciais,count(distinct d.pedido_venda_item_id) as itens_comerciais
  from public.v_elo_pcp_demanda_comercial d
  group by d.tenant_id,d.modelo_id,d.natureza_demanda,d.chave_comparabilidade
),
fator as (
  select tenant_id,modelo_id,modelo_codigo,modelo_nome,taxonomia_tipo,natureza_demanda,chave_comparabilidade,quantidade_historica,
         quantidade_prevista,fator_demanda,variacao_percentual,estado_comparabilidade,estado_fator
  from public.v_elo_pcp_referencia_demanda_comparavel
),
humana as (
  select tenant_id,modelo_id,natureza_demanda,chave_comparabilidade,funcao_montagem_id,funcao_codigo,funcao_nome,demanda_colaboradores_media_dia,
         demanda_colaboradores_pico_dia,colaboradores_dia_acumulados,horas_demanda_acumuladas
  from public.v_elo_pcp_demanda_humana_historica_externa
),
projecao as (
  select tenant_id,modelo_id,natureza_demanda,chave_comparabilidade,funcao_montagem_id,funcao_codigo,funcao_nome,demanda_humana_historica_media_dia,
         quantidade_historica,quantidade_prevista,fator_demanda,variacao_percentual,demanda_humana_projetada_media_dia,estado_projecao
  from public.v_elo_pcp_demanda_humana_projetada_externa
),
composicao_gap as (
  select g.tenant_id,u.modelo_id,count(*) as gaps_composicao
  from public.v_elo_pcp_gap_composicao_humana_externa g cross join lateral unnest(g.modelos_ids) as u(modelo_id)
  group by g.tenant_id,u.modelo_id
),
cobertura as (select * from public.v_elo_pcp_cobertura_demanda_externa)
select
  coalesce(f.tenant_id,c.tenant_id,h.tenant_id,p.tenant_id) as tenant_id,
  coalesce(f.modelo_id,c.modelo_id,h.modelo_id,p.modelo_id) as modelo_id,
  coalesce(f.modelo_codigo,m.codigo) as modelo_codigo,coalesce(f.modelo_nome,m.nome) as modelo_nome,
  coalesce(f.taxonomia_tipo,t.tipo) as taxonomia_tipo,
  coalesce(f.natureza_demanda,c.natureza_demanda,h.natureza_demanda,p.natureza_demanda) as natureza_demanda,
  coalesce(f.chave_comparabilidade,c.chave_comparabilidade,h.chave_comparabilidade,p.chave_comparabilidade) as chave_comparabilidade,
  c.quantidade_comercial_atual,c.pedidos_comerciais,c.itens_comerciais,f.quantidade_historica,f.quantidade_prevista,f.fator_demanda,
  f.variacao_percentual,f.estado_comparabilidade,f.estado_fator,p.funcao_montagem_id,coalesce(p.funcao_codigo,h.funcao_codigo) as funcao_codigo,
  coalesce(p.funcao_nome,h.funcao_nome) as funcao_nome,coalesce(p.demanda_humana_historica_media_dia,h.demanda_colaboradores_media_dia) as demanda_humana_historica_media_dia,
  h.demanda_colaboradores_pico_dia,h.colaboradores_dia_acumulados,h.horas_demanda_acumuladas,p.demanda_humana_projetada_media_dia,p.estado_projecao,
  coalesce(g.gaps_composicao,0) as gaps_composicao,
  case
    when coalesce(f.estado_comparabilidade,'') in ('SEM_HISTORICO','SEM_PREVISAO','SEM_NATUREZA','SEM_CHAVE_COMPARABILIDADE') then 'DADO_COMERCIAL_NAO_COMPARAVEL'
    when f.estado_fator='HISTORICO_ZERO' then 'HISTORICO_ZERO_SEM_FATOR'
    when f.estado_fator='FATOR_CALCULADO' and coalesce(f.variacao_percentual,0)>0 then 'AUMENTO_DEMANDA_COMPARAVEL'
    when f.estado_fator='FATOR_CALCULADO' and coalesce(f.variacao_percentual,0)<0 then 'REDUCAO_DEMANDA_COMPARAVEL'
    when f.estado_fator='FATOR_CALCULADO' then 'DEMANDA_ESTAVEL'
    when h.modelo_id is null and f.estado_fator='FATOR_CALCULADO' then 'SEM_HISTORICO_HUMANO'
    else 'AGUARDANDO_VALIDACAO' end as motivo_analitico,
  case
    when coalesce(g.gaps_composicao,0)>0 then 'VALIDAR_COMPOSICAO_DA_ORDEM'
    when f.estado_fator='FATOR_CALCULADO' and h.modelo_id is null then 'INFORMAR_HISTORICO_HUMANO_POR_FUNCAO'
    when f.estado_fator='FATOR_CALCULADO' and p.demanda_humana_projetada_media_dia is not null then 'VALIDAR_IMPACTO_PROJETADO_COM_OPERACAO_E_RH'
    when f.estado_comparabilidade='SEM_CHAVE_COMPARABILIDADE' then 'INFORMAR_CHAVE_DE_COMPARABILIDADE'
    when f.estado_fator='SEM_PREVISAO' then 'INFORMAR_PREVISAO_DO_HORIZONTE'
    when f.estado_fator='SEM_HISTORICO' then 'INFORMAR_HISTORICO_COMPARAVEL'
    else 'VALIDAR_DADOS_DE_ORIGEM' end as proxima_informacao_decisoria,
  coalesce(cb.demanda_prevista,0) as cobertura_demanda_prevista_modelo,coalesce(cb.estoque_disponivel,0) as cobertura_estoque_disponivel,
  coalesce(cb.unidades_em_reparo_recuperaveis,0) as cobertura_reparos_recuperaveis,coalesce(cb.producao_programada,0) as cobertura_producao_programada,
  coalesce(cb.necessidade_adicional_fabricacao,0) as necessidade_adicional_fabricacao,coalesce(cb.estado_cobertura,'SEM_PREVISAO') as estado_cobertura,
  coalesce(cb.reparos_sem_unidade,0) as reparos_sem_unidade,coalesce(cb.reparos_sem_data_conclusao,0) as reparos_sem_data_conclusao
from fator f
full join comercial c on c.tenant_id=f.tenant_id and c.modelo_id=f.modelo_id and c.natureza_demanda is not distinct from f.natureza_demanda and c.chave_comparabilidade is not distinct from f.chave_comparabilidade
full join humana h on h.tenant_id=coalesce(f.tenant_id,c.tenant_id) and h.modelo_id=coalesce(f.modelo_id,c.modelo_id) and h.natureza_demanda is not distinct from coalesce(f.natureza_demanda,c.natureza_demanda) and h.chave_comparabilidade is not distinct from coalesce(f.chave_comparabilidade,c.chave_comparabilidade)
full join projecao p on p.tenant_id=coalesce(f.tenant_id,c.tenant_id,h.tenant_id) and p.modelo_id=coalesce(f.modelo_id,c.modelo_id,h.modelo_id) and p.natureza_demanda is not distinct from coalesce(f.natureza_demanda,c.natureza_demanda,h.natureza_demanda) and p.chave_comparabilidade is not distinct from coalesce(f.chave_comparabilidade,c.chave_comparabilidade,h.chave_comparabilidade) and p.funcao_montagem_id is not distinct from h.funcao_montagem_id
left join composicao_gap g on g.tenant_id=coalesce(f.tenant_id,c.tenant_id,h.tenant_id,p.tenant_id) and g.modelo_id=coalesce(f.modelo_id,c.modelo_id,h.modelo_id,p.modelo_id)
left join cobertura cb on cb.tenant_id=coalesce(f.tenant_id,c.tenant_id,h.tenant_id,p.tenant_id) and cb.modelo_id=coalesce(f.modelo_id,c.modelo_id,h.modelo_id,p.modelo_id)
left join public.modelos m on m.id=coalesce(f.modelo_id,c.modelo_id,h.modelo_id,p.modelo_id)
left join public.taxonomia t on t.id=m.taxonomia_id;