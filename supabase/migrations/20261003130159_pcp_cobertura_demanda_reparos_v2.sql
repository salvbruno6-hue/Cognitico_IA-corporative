create or replace view public.v_elo_pcp_cobertura_demanda_externa
with (security_invoker = true)
as
with demanda as (
  select tenant_id, modelo_id, natureza_demanda, chave_comparabilidade,
         sum(coalesce(quantidade_prevista,0)) as demanda_prevista
  from public.mt_previsoes_demanda
  where periodo_inicio >= date '2026-09-01' and periodo_fim <= date '2027-02-28'
  group by tenant_id, modelo_id, natureza_demanda, chave_comparabilidade
),
estoque as (
  select l.tenant_id, m.id as modelo_id,
         sum(coalesce(l.quantidade_disponivel,0)) as estoque_disponivel
  from public.mt_lotes_estoque l
  join public.lista_mae lm on lm.id = l.lista_mae_id
  join public.modelos m on lm.modelos_aplicaveis ilike '%' || m.codigo || '%'
  where coalesce(l.status,'') not in ('CANCELADO','INATIVO')
  group by l.tenant_id,m.id
),
reparos as (
  select r.tenant_id, um.modelo_id,
         count(*) filter (
           where coalesce(r.status,'') not in ('CANCELADO','CONCLUIDO')
             and coalesce(r.data_final_reparo, date '2999-12-31') <= date '2027-02-28'
         )::numeric as unidades_em_reparo_recuperaveis
  from public.mt_ordens_reparo r
  join public.mt_unidades_modulares um on um.id = r.unidade_modular_id
  group by r.tenant_id,um.modelo_id
),
producao as (
  select tenant_id, modelo_id,
         sum(greatest(coalesce(quantidade_planejada,0)-coalesce(quantidade_produzida,0),0)) as producao_programada
  from public.mt_ordens_producao
  where inicio_planejado >= date '2026-09-01' and inicio_planejado <= date '2027-02-28'
    and coalesce(status,'') not in ('CANCELADA','CANCELADO')
  group by tenant_id,modelo_id
)
select d.tenant_id,d.modelo_id,m.codigo as modelo_codigo,m.nome as modelo_nome,t.tipo as taxonomia_tipo,
       d.natureza_demanda,d.chave_comparabilidade,d.demanda_prevista,
       coalesce(e.estoque_disponivel,0) as estoque_disponivel,
       coalesce(r.unidades_em_reparo_recuperaveis,0) as unidades_em_reparo_recuperaveis,
       coalesce(p.producao_programada,0) as producao_programada,
       greatest(d.demanda_prevista-coalesce(e.estoque_disponivel,0)-coalesce(r.unidades_em_reparo_recuperaveis,0)-coalesce(p.producao_programada,0),0) as necessidade_adicional_fabricacao,
       case when d.demanda_prevista <= coalesce(e.estoque_disponivel,0)+coalesce(r.unidades_em_reparo_recuperaveis,0)+coalesce(p.producao_programada,0)
            then 'COBERTA' else 'DEFICIT_FABRICACAO' end as estado_cobertura
from demanda d join public.modelos m on m.id=d.modelo_id
left join public.taxonomia t on t.id=m.taxonomia_id
left join estoque e on e.tenant_id=d.tenant_id and e.modelo_id=d.modelo_id
left join reparos r on r.tenant_id=d.tenant_id and r.modelo_id=d.modelo_id
left join producao p on p.tenant_id=d.tenant_id and p.modelo_id=d.modelo_id;