-- PCP: corrige drift de produção na seleção do fluxo aplicável por modelo.
-- A migration original foi aplicada antes do ajuste final `NULLS LAST` chegar ao GitHub.
-- Não altera tempos, capacidades, roteiros ou dados operacionais.

create or replace view public.v_elo_pcp_requisito_fisico_planejamento
with (security_invoker = true)
as
with reparo_textual as (
  select
    count(*)::bigint as reparos_textuais_candidatos,
    count(*) filter (where upper(coalesce(status,'')) in ('CONCLUIDO','CONCLUIDA'))::bigint as reparos_textuais_concluidos,
    count(*) filter (where unidade_modular_id is not null)::bigint as reparos_textuais_vinculados_unidade
  from public.mt_ordens_reparo
  where upper(regexp_replace(coalesce(tipo_modulo,''),'[^A-Z0-9]+','','g')) =
        upper(regexp_replace('Módulo Habitacional 20pés Amplo','[^A-Z0-9]+','','g'))
)
select
  r.id,
  r.tenant_id,
  r.modelo_id,
  m.codigo as modelo_codigo,
  m.nome as modelo_nome,
  case
    when upper(trim(coalesce(m.familia,''))) in ('MODULO','MÓDULO') then 'MODULO'
    when upper(trim(coalesce(m.familia,''))) in ('CONTEINER','CONTÊINER','CONTAINER') then 'CONTEINER'
    else upper(trim(coalesce(m.familia,'OUTRO')))
  end as familia_produto,
  r.natureza_demanda,
  r.quantidade_objetivo,
  r.quantidade_iniciada,
  r.quantidade_concluida,
  greatest(r.quantidade_objetivo-r.quantidade_concluida,0) as quantidade_restante,
  r.data_limite,
  r.estado_producao,
  r.distribuicao_mensal_status,
  r.origem,
  r.fonte_referencia,
  r.confirmado_em,
  f.etapas_fluxo_referencia,
  f.etapas_com_tempo,
  f.etapas_com_capacidade,
  f.lead_time_fluxo_dias,
  f.capacidade_fluxo_referencia,
  f.operacoes_roteiro_cadastradas,
  rt.reparos_textuais_candidatos,
  rt.reparos_textuais_concluidos,
  rt.reparos_textuais_vinculados_unidade,
  (r.tenant_id is null) as gap_tenant,
  (coalesce(f.operacoes_roteiro_cadastradas,0)=0) as gap_roteiro_produtivo,
  (coalesce(f.etapas_com_tempo,0)<coalesce(f.etapas_fluxo_referencia,0) or f.lead_time_fluxo_dias is null) as gap_tempo_fluxo,
  (coalesce(f.etapas_com_capacidade,0)<coalesce(f.etapas_fluxo_referencia,0) or f.capacidade_fluxo_referencia is null) as gap_capacidade_fluxo,
  (coalesce(rt.reparos_textuais_candidatos,0)>0 and coalesce(rt.reparos_textuais_vinculados_unidade,0)=0) as gap_reparo_sem_unidade_fisica,
  case
    when r.quantidade_concluida >= r.quantidade_objetivo then 'CONCLUIDO'
    when r.quantidade_iniciada > 0 then 'EM_EXECUCAO'
    else 'NAO_INICIADO'
  end as estado_atendimento,
  case
    when r.tenant_id is null then 'GAP_TENANT'
    when coalesce(f.operacoes_roteiro_cadastradas,0)=0 then 'GAP_ROTEIRO_PRODUTIVO'
    when coalesce(f.etapas_com_tempo,0)<coalesce(f.etapas_fluxo_referencia,0) or f.lead_time_fluxo_dias is null then 'GAP_TEMPO_FLUXO'
    when coalesce(f.etapas_com_capacidade,0)<coalesce(f.etapas_fluxo_referencia,0) or f.capacidade_fluxo_referencia is null then 'GAP_CAPACIDADE_FLUXO'
    else 'CAPACIDADE_APTA_PARA_PROGRAMACAO'
  end as estado_programacao_capacidade,
  case
    when r.tenant_id is null then 'Requisito físico confirmado, mas ainda não associado a tenant operacional.'
    when coalesce(f.operacoes_roteiro_cadastradas,0)=0 then 'Cadastrar roteiro produtivo M01 antes de distribuir as 300 unidades no calendário.'
    when coalesce(f.etapas_com_tempo,0)<coalesce(f.etapas_fluxo_referencia,0) or f.lead_time_fluxo_dias is null then 'Completar tempos e lead time do fluxo M01; não usar apenas tempos parciais da estrutura.'
    when coalesce(f.etapas_com_capacidade,0)<coalesce(f.etapas_fluxo_referencia,0) or f.capacidade_fluxo_referencia is null then 'Completar capacidade por etapa e gargalo; então programar as 300 unidades até 31/01/2027.'
    else 'Distribuir as 300 unidades pelo calendário conforme capacidade validada e gerar plano/OPs governados.'
  end as orientacao_elo
from elo_private.pcp_requisitos_fisicos_planejamento r
join public.modelos m on m.id=r.modelo_id
cross join lateral (
  with fluxo_aplicavel as (
    select fp.*
    from public.fluxo_produtivo_modular fp
    where fp.ativo=true
      and (fp.modelo_id=r.modelo_id or fp.modelo_id is null)
    order by
      (fp.modelo_id=r.modelo_id) desc nulls last,
      fp.versao desc nulls last,
      fp.codigo
    limit 1
  )
  select
    count(e.id) filter (where upper(coalesce(e.status,''))='ATIVO')::bigint as etapas_fluxo_referencia,
    count(e.id) filter (where upper(coalesce(e.status,''))='ATIVO' and e.tempo_unitario_min is not null)::bigint as etapas_com_tempo,
    count(e.id) filter (where upper(coalesce(e.status,''))='ATIVO' and e.capacidade is not null)::bigint as etapas_com_capacidade,
    max(fp.lead_time_dias) as lead_time_fluxo_dias,
    max(fp.capacidade_referencia) as capacidade_fluxo_referencia,
    (select count(*)::bigint from public.mt_operacoes_roteiro) as operacoes_roteiro_cadastradas
  from fluxo_aplicavel fp
  left join public.fluxo_produtivo_modular_etapas e on e.fluxo_id=fp.id
) f
cross join reparo_textual rt;

comment on view public.v_elo_pcp_requisito_fisico_planejamento is
'Read-model do requisito físico confirmado por modelo/prazo. Métricas de fluxo usam o fluxo ativo específico do modelo quando existente, com fallback para o fluxo geral ativo; fluxos específicos de outros modelos não contaminam readiness. Não promove capacidade, tempo, roteiro ou estoque ausente.';

revoke all on public.v_elo_pcp_requisito_fisico_planejamento from anon, authenticated;
