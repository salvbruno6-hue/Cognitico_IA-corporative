create schema if not exists elo_private;

create table if not exists elo_private.pcp_requisitos_fisicos_planejamento (
  id uuid primary key default gen_random_uuid(),
  tenant_id uuid null references public.mt_tenants(id),
  modelo_id uuid not null references public.modelos(id),
  natureza_demanda text not null,
  quantidade_objetivo numeric not null check (quantidade_objetivo > 0),
  data_limite date not null,
  quantidade_iniciada numeric not null default 0 check (quantidade_iniciada >= 0),
  quantidade_concluida numeric not null default 0 check (quantidade_concluida >= 0),
  estado_producao text not null default 'NAO_INICIADA',
  distribuicao_mensal_status text not null default 'AGUARDANDO_CAPACIDADE_VALIDADA',
  origem text not null,
  fonte_referencia text,
  confirmado_em timestamptz not null default now(),
  observacoes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint pcp_requisitos_fisicos_natureza_ck check (natureza_demanda in ('EVENTO','SPOT','VENDA','MISTO','OUTRO')),
  constraint pcp_requisitos_fisicos_estado_ck check (estado_producao in ('NAO_INICIADA','EM_PRODUCAO','CONCLUIDA','SUSPENSA')),
  constraint pcp_requisitos_fisicos_quantidades_ck check (quantidade_concluida <= quantidade_iniciada and quantidade_iniciada <= quantidade_objetivo)
);

create unique index if not exists ux_pcp_requisitos_fisicos_planejamento
  on elo_private.pcp_requisitos_fisicos_planejamento (modelo_id, natureza_demanda, data_limite, origem);

alter table elo_private.pcp_requisitos_fisicos_planejamento enable row level security;

drop policy if exists pcp_requisitos_fisicos_service_role on elo_private.pcp_requisitos_fisicos_planejamento;
create policy pcp_requisitos_fisicos_service_role
  on elo_private.pcp_requisitos_fisicos_planejamento
  for all
  to service_role
  using (true)
  with check (true);

insert into elo_private.pcp_requisitos_fisicos_planejamento (
  tenant_id, modelo_id, natureza_demanda, quantidade_objetivo, data_limite,
  quantidade_iniciada, quantidade_concluida, estado_producao,
  distribuicao_mensal_status, origem, fonte_referencia, observacoes
)
select
  null,
  m.id,
  'EVENTO',
  300,
  date '2027-01-31',
  0,
  0,
  'NAO_INICIADA',
  'AGUARDANDO_CAPACIDADE_VALIDADA',
  'CONFIRMACAO_USUARIO_CHAT_2026-10-21',
  'user://planejamento-demanda-fluxo-modular/2026-10-21',
  'Requisito físico confirmado pelo usuário: 300 unidades M01 até o fim de janeiro de 2027. Produção ainda não iniciada e nenhuma unidade concluída. Distribuição mensal deve seguir capacidade validada do fluxo produtivo; não ratear mecanicamente.'
from public.modelos m
where upper(m.codigo) = 'M01'
on conflict (modelo_id, natureza_demanda, data_limite, origem)
do update set
  quantidade_objetivo = excluded.quantidade_objetivo,
  quantidade_iniciada = excluded.quantidade_iniciada,
  quantidade_concluida = excluded.quantidade_concluida,
  estado_producao = excluded.estado_producao,
  distribuicao_mensal_status = excluded.distribuicao_mensal_status,
  fonte_referencia = excluded.fonte_referencia,
  observacoes = excluded.observacoes,
  updated_at = now();

create or replace view public.v_elo_pcp_requisito_fisico_planejamento
with (security_invoker = true)
as
with fluxo as (
  select
    (select count(*)::bigint from public.fluxo_produtivo_modular_etapas where upper(coalesce(status,''))='ATIVO') as etapas_fluxo_referencia,
    (select count(*)::bigint from public.fluxo_produtivo_modular_etapas where upper(coalesce(status,''))='ATIVO' and tempo_unitario_min is not null) as etapas_com_tempo,
    (select count(*)::bigint from public.fluxo_produtivo_modular_etapas where upper(coalesce(status,''))='ATIVO' and capacidade is not null) as etapas_com_capacidade,
    (select max(lead_time_dias) from public.fluxo_produtivo_modular where ativo=true) as lead_time_fluxo_dias,
    (select max(capacidade_referencia) from public.fluxo_produtivo_modular where ativo=true) as capacidade_fluxo_referencia,
    (select count(*)::bigint from public.mt_operacoes_roteiro) as operacoes_roteiro_cadastradas
),
reparo_textual as (
  select
    count(*)::bigint as reparos_textuais_candidatos,
    count(*) filter (where upper(coalesce(status,'')) in ('CONCLUIDO','CONCLUIDA'))::bigint as reparos_textuais_concluidos,
    count(*) filter (where unidade_modular_id is not null)::bigint as reparos_textuais_vinculados_unidade
  from public.mt_ordens_reparo
  where upper(regexp_replace(coalesce(tipo_modulo,''),'[^A-Z0-9]+','','g')) = upper(regexp_replace('Módulo Habitacional 20pés Amplo','[^A-Z0-9]+','','g'))
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
cross join fluxo f
cross join reparo_textual rt;

comment on table elo_private.pcp_requisitos_fisicos_planejamento is
'Requisitos físicos confirmados de planejamento. Não substitui pedido, AF, plano PCP ou OP operacional. Permite ao ELO preservar uma necessidade confirmada pelo usuário enquanto aguarda reconciliação operacional.';

comment on view public.v_elo_pcp_requisito_fisico_planejamento is
'Read-model do requisito físico confirmado por modelo/prazo, incluindo readiness do fluxo produtivo e evidência textual de reparos sem promovê-la a estoque físico. A programação mensal só deve ocorrer após capacidade validada.';

revoke all on public.v_elo_pcp_requisito_fisico_planejamento from anon, authenticated;
