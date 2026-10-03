-- ELO PCP: gatilho e cockpit de decisão para operações externas.
-- A view é dinâmica: a inserção/alteração dos dados não materializa números.
-- O trigger apenas registra que uma nova leitura decisória deve ser validada.
-- Nenhuma decisão de contratação, disponibilidade ou quadro de RH é inferida aqui.

create or replace view public.v_elo_pcp_decisao_externa_detalhe
with (security_invoker = true)
as
with comercial as (
  select
    d.tenant_id,
    d.modelo_id,
    d.natureza_demanda,
    d.chave_comparabilidade,
    sum(d.quantidade) as quantidade_comercial_atual,
    count(distinct d.pedido_venda_id) as pedidos_comerciais,
    count(distinct d.pedido_venda_item_id) as itens_comerciais
  from public.v_elo_pcp_demanda_comercial d
  group by d.tenant_id, d.modelo_id, d.natureza_demanda, d.chave_comparabilidade
),
fator as (
  select
    f.tenant_id,
    f.modelo_id,
    f.modelo_codigo,
    f.modelo_nome,
    f.taxonomia_tipo,
    f.natureza_demanda,
    f.chave_comparabilidade,
    f.quantidade_historica,
    f.quantidade_prevista,
    f.fator_demanda,
    f.variacao_percentual,
    f.estado_comparabilidade,
    f.estado_fator
  from public.v_elo_pcp_referencia_demanda_comparavel f
),
humana as (
  select
    h.tenant_id,
    h.modelo_id,
    h.natureza_demanda,
    h.chave_comparabilidade,
    h.funcao_montagem_id,
    h.funcao_codigo,
    h.funcao_nome,
    h.demanda_colaboradores_media_dia,
    h.demanda_colaboradores_pico_dia,
    h.colaboradores_dia_acumulados,
    h.horas_demanda_acumuladas
  from public.v_elo_pcp_demanda_humana_historica_externa h
),
projecao as (
  select
    p.tenant_id,
    p.modelo_id,
    p.natureza_demanda,
    p.chave_comparabilidade,
    p.funcao_montagem_id,
    p.funcao_codigo,
    p.funcao_nome,
    p.demanda_humana_historica_media_dia,
    p.quantidade_historica,
    p.quantidade_prevista,
    p.fator_demanda,
    p.variacao_percentual,
    p.demanda_humana_projetada_media_dia,
    p.estado_projecao
  from public.v_elo_pcp_demanda_humana_projetada_externa p
),
composicao_gap as (
  select
    g.tenant_id,
    g.modelo_id,
    count(*) as gaps_composicao
  from public.v_elo_pcp_gap_composicao_humana_externa g
  group by g.tenant_id, g.modelo_id
)
select
  coalesce(f.tenant_id, c.tenant_id, h.tenant_id, p.tenant_id) as tenant_id,
  coalesce(f.modelo_id, c.modelo_id, h.modelo_id, p.modelo_id) as modelo_id,
  coalesce(f.modelo_codigo, m.codigo) as modelo_codigo,
  coalesce(f.modelo_nome, m.nome) as modelo_nome,
  coalesce(f.taxonomia_tipo, t.tipo) as taxonomia_tipo,
  coalesce(f.natureza_demanda, c.natureza_demanda, h.natureza_demanda, p.natureza_demanda) as natureza_demanda,
  coalesce(f.chave_comparabilidade, c.chave_comparabilidade, h.chave_comparabilidade, p.chave_comparabilidade) as chave_comparabilidade,

  c.quantidade_comercial_atual,
  c.pedidos_comerciais,
  c.itens_comerciais,

  f.quantidade_historica,
  f.quantidade_prevista,
  f.fator_demanda,
  f.variacao_percentual,
  f.estado_comparabilidade,
  f.estado_fator,

  p.funcao_montagem_id,
  coalesce(p.funcao_codigo, h.funcao_codigo) as funcao_codigo,
  coalesce(p.funcao_nome, h.funcao_nome) as funcao_nome,
  coalesce(p.demanda_humana_historica_media_dia, h.demanda_colaboradores_media_dia) as demanda_humana_historica_media_dia,
  h.demanda_colaboradores_pico_dia,
  h.colaboradores_dia_acumulados,
  h.horas_demanda_acumuladas,
  p.demanda_humana_projetada_media_dia,
  p.estado_projecao,

  coalesce(g.gaps_composicao, 0) as gaps_composicao,

  case
    when coalesce(f.estado_comparabilidade, '') in ('SEM_HISTORICO','SEM_PREVISAO','SEM_NATUREZA','SEM_CHAVE_COMPARABILIDADE')
      then 'DADO_COMERCIAL_NAO_COMPARAVEL'
    when f.estado_fator = 'HISTORICO_ZERO'
      then 'HISTORICO_ZERO_SEM_FATOR'
    when f.estado_fator = 'FATOR_CALCULADO' and coalesce(f.variacao_percentual, 0) > 0
      then 'AUMENTO_DEMANDA_COMPARAVEL'
    when f.estado_fator = 'FATOR_CALCULADO' and coalesce(f.variacao_percentual, 0) < 0
      then 'REDUCAO_DEMANDA_COMPARAVEL'
    when f.estado_fator = 'FATOR_CALCULADO'
      then 'DEMANDA_ESTAVEL'
    when h.modelo_id is null and f.estado_fator = 'FATOR_CALCULADO'
      then 'SEM_HISTORICO_HUMANO'
    else 'AGUARDANDO_VALIDACAO'
  end as motivo_analitico,

  case
    when coalesce(g.gaps_composicao, 0) > 0
      then 'VALIDAR_COMPOSICAO_DA_ORDEM'
    when f.estado_fator = 'FATOR_CALCULADO' and h.modelo_id is null
      then 'INFORMAR_HISTORICO_HUMANO_POR_FUNCAO'
    when f.estado_fator = 'FATOR_CALCULADO' and p.demanda_humana_projetada_media_dia is not null
      then 'VALIDAR_IMPACTO_PROJETADO_COM_OPERACAO_E_RH'
    when f.estado_comparabilidade = 'SEM_CHAVE_COMPARABILIDADE'
      then 'INFORMAR_CHAVE_DE_COMPARABILIDADE'
    when f.estado_fator = 'SEM_PREVISAO'
      then 'INFORMAR_PREVISAO_DO_HORIZONTE'
    when f.estado_fator = 'SEM_HISTORICO'
      then 'INFORMAR_HISTORICO_COMPARAVEL'
    else 'VALIDAR_DADOS_DE_ORIGEM'
  end as proxima_informacao_decisoria

from fator f
full join comercial c
  on c.tenant_id = f.tenant_id
 and c.modelo_id = f.modelo_id
 and c.natureza_demanda is not distinct from f.natureza_demanda
 and c.chave_comparabilidade is not distinct from f.chave_comparabilidade
full join humana h
  on h.tenant_id = coalesce(f.tenant_id, c.tenant_id)
 and h.modelo_id = coalesce(f.modelo_id, c.modelo_id)
 and h.natureza_demanda is not distinct from coalesce(f.natureza_demanda, c.natureza_demanda)
 and h.chave_comparabilidade is not distinct from coalesce(f.chave_comparabilidade, c.chave_comparabilidade)
full join projecao p
  on p.tenant_id = coalesce(f.tenant_id, c.tenant_id, h.tenant_id)
 and p.modelo_id = coalesce(f.modelo_id, c.modelo_id, h.modelo_id)
 and p.natureza_demanda is not distinct from coalesce(f.natureza_demanda, c.natureza_demanda, h.natureza_demanda)
 and p.chave_comparabilidade is not distinct from coalesce(f.chave_comparabilidade, c.chave_comparabilidade, h.chave_comparabilidade)
 and p.funcao_montagem_id is not distinct from h.funcao_montagem_id
left join composicao_gap g
  on g.tenant_id = coalesce(f.tenant_id, c.tenant_id, h.tenant_id, p.tenant_id)
 and g.modelo_id = coalesce(f.modelo_id, c.modelo_id, h.modelo_id, p.modelo_id)
left join public.modelos m
  on m.id = coalesce(f.modelo_id, c.modelo_id, h.modelo_id, p.modelo_id)
left join public.taxonomia t
  on t.id = m.taxonomia_id;

comment on view public.v_elo_pcp_decisao_externa_detalhe is
'Camada analitica de decisao do PCP para operacoes externas. Consolida demanda comercial, referencia historica, fator, demanda humana historica/projetada e gaps. Nao calcula quadro de RH nem recomenda contratacao.';

create or replace view public.v_elo_pcp_decisao_externa_resumo
with (security_invoker = true)
as
with d as (
  select * from public.v_elo_pcp_decisao_externa_detalhe
),
comercial as (
  select
    count(distinct pedido_venda_id) as pedidos_comerciais,
    coalesce(sum(quantidade),0) as unidades_comerciais
  from public.v_elo_pcp_demanda_comercial
),
operacao as (
  select
    count(*) filter (where coalesce(status,'PLANEJADO') not in ('CANCELADO','CANCELADA')) as ordens_externas,
    coalesce(sum(horas_planejadas) filter (where coalesce(status,'PLANEJADO') not in ('CANCELADO','CANCELADA')),0) as horas_planejadas_externas
  from public.mt_ordens_montagem_externa
),
fatores as (
  select
    count(*) filter (where estado_fator='FATOR_CALCULADO') as fatores_calculados,
    count(*) filter (where estado_fator='FATOR_CALCULADO' and variacao_percentual > 0) as fatores_crescimento,
    count(*) filter (where estado_fator='FATOR_CALCULADO' and variacao_percentual < 0) as fatores_reducao,
    count(*) filter (where estado_comparabilidade='COMPARAVEL_POTENCIAL') as comparaveis_potenciais
  from d
),
gaps as (
  select
    count(*) filter (where gaps_composicao > 0) as linhas_com_gap_composicao,
    count(*) filter (where proxima_informacao_decisoria <> 'VALIDAR_IMPACTO_PROJETADO_COM_OPERACAO_E_RH') as linhas_com_informacao_pendente
  from d
),
fonte_demanda as (
  select
    count(*) as historico_registros,
    coalesce(sum(quantidade_historica),0) as historico_unidades,
    coalesce(sum(quantidade_prevista),0) as previsao_unidades
  from (
    select distinct
      tenant_id, modelo_id, natureza_demanda, chave_comparabilidade,
      quantidade_historica, quantidade_prevista
    from public.v_elo_pcp_referencia_demanda_comparavel
  ) x
)
select
  now() as atualizado_em,
  case
    when fd.historico_registros = 0 then 'AGUARDANDO_HISTORICO'
    when fd.previsao_unidades = 0 then 'AGUARDANDO_PREVISAO'
    when ft.fatores_calculados = 0 then 'AGUARDANDO_VALIDACAO_DE_COMPARABILIDADE'
    when gg.linhas_com_gap_composicao > 0 then 'AGUARDANDO_COMPOSICAO_OPERACIONAL'
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

  coalesce(sum(d.demanda_humana_historica_media_dia) filter (where d.demanda_humana_historica_media_dia is not null),0) as demanda_humana_historica_media_total_dia,
  coalesce(sum(d.demanda_humana_projetada_media_dia) filter (where d.demanda_humana_projetada_media_dia is not null),0) as demanda_humana_projetada_media_total_dia,

  gg.linhas_com_gap_composicao,
  gg.linhas_com_informacao_pendente,

  jsonb_build_object(
    'impactos_a_observar', jsonb_build_array(
      'volume_comercial',
      'variacao_da_demanda_comparavel',
      'horas_planejadas_de_operacao_externa',
      'demanda_humana_historica_por_funcao',
      'demanda_humana_projetada_por_funcao',
      'gaps_de_composicao'
    ),
    'informacoes_que_aumentam_precisao', jsonb_build_array(
      'chave_de_comparabilidade_validada',
      'previsao_por_modelo_e_natureza',
      'historico_real_por_modelo_e_natureza',
      'ordens_externas_com_inicio_fim_e_horas_planejadas',
      'composicao_funcional_validada',
      'historico_humano_por_funcao',
      'confiabilidade_da_previsao',
      'origem_comercial_rastreavel'
    ),
    'regra', 'Nao transformar crescimento de demanda em crescimento de quadro de RH sem produtividade, composicao e validacao operacional.'
  ) as guia_decisao
from d
cross join comercial c
cross join operacao o
cross join fatores ft
cross join gaps gg
cross join fonte_demanda fd
group by
  c.pedidos_comerciais, c.unidades_comerciais,
  fd.historico_registros, fd.historico_unidades, fd.previsao_unidades,
  ft.comparaveis_potenciais, ft.fatores_calculados, ft.fatores_crescimento, ft.fatores_reducao,
  o.ordens_externas, o.horas_planejadas_externas,
  gg.linhas_com_gap_composicao, gg.linhas_com_informacao_pendente;

comment on view public.v_elo_pcp_decisao_externa_resumo is
'Resumo executivo do PCP externo: estado, impactos, indicadores, gaps e informacoes que aumentam a precisao. Descritivo, sem recomendacao automatica de quadro de RH.';

insert into public.elo_automation_registry
  (code,name,purpose,trigger_type,source_table,target_action,enabled,requires_validation)
values
  ('elo_pcp_decisao_externa','PCP decisao externa','Registrar alteracoes em demanda comercial, demanda historica/previsao e operacao externa para atualizar a leitura decisoria governada.','EVENT','PCP_EXTERNO','ASK_PCP_DECISAO_EXTERNA',true,true)
on conflict (code) do update set
  name=excluded.name,
  purpose=excluded.purpose,
  trigger_type=excluded.trigger_type,
  source_table=excluded.source_table,
  target_action=excluded.target_action,
  enabled=excluded.enabled,
  requires_validation=excluded.requires_validation,
  updated_at=now();

create or replace function public.elo_pcp_disparar_decisao_externa()
returns trigger
language plpgsql
security definer
set search_path = ''
as $function$
declare
  v_automation_id uuid;
begin
  perform pg_advisory_xact_lock(hashtextextended('elo_pcp_decisao_externa',0));

  select id
    into v_automation_id
  from public.elo_automation_registry
  where code='elo_pcp_decisao_externa'
    and enabled=true
  limit 1;

  if v_automation_id is null then
    return null;
  end if;

  if exists (
    select 1
    from public.elo_automation_runs r
    where r.automation_id=v_automation_id
      and r.status in ('PENDING_INPUT','RUNNING')
      and coalesce(r.details->>'intent','')='PCP_DECISAO_EXTERNA'
  ) then
    return null;
  end if;

  insert into public.elo_automation_runs
    (automation_id,started_at,status,rows_affected,details)
  values
    (v_automation_id,now(),'PENDING_INPUT',1,jsonb_build_object(
      'intent','PCP_DECISAO_EXTERNA',
      'source_table',tg_table_name,
      'next_question','Os dados do PCP externo foram alterados. Posso consolidar os impactos, indicadores, gaps e informacoes faltantes para validacao da decisao?',
      'rule','A view e analitica e descritiva; nenhuma contratacao, dimensionamento de quadro ou disponibilidade de RH deve ser inferida sem produtividade, composicao e validacao.'
    ));

  return null;
end;
$function$;

revoke all on function public.elo_pcp_disparar_decisao_externa() from public, anon, authenticated;

drop trigger if exists trg_elo_pcp_decisao_comercial on public.mt_pedidos_venda;
create trigger trg_elo_pcp_decisao_comercial
after insert or update on public.mt_pedidos_venda
for each statement execute function public.elo_pcp_disparar_decisao_externa();

drop trigger if exists trg_elo_pcp_decisao_comercial_itens on public.mt_pedidos_venda_itens;
create trigger trg_elo_pcp_decisao_comercial_itens
after insert or update on public.mt_pedidos_venda_itens
for each statement execute function public.elo_pcp_disparar_decisao_externa();

drop trigger if exists trg_elo_pcp_decisao_historico on public.mt_demanda_historico;
create trigger trg_elo_pcp_decisao_historico
after insert or update on public.mt_demanda_historico
for each statement execute function public.elo_pcp_disparar_decisao_externa();

drop trigger if exists trg_elo_pcp_decisao_previsao on public.mt_previsoes_demanda;
create trigger trg_elo_pcp_decisao_previsao
after insert or update on public.mt_previsoes_demanda
for each statement execute function public.elo_pcp_disparar_decisao_externa();

drop trigger if exists trg_elo_pcp_decisao_ordem_externa on public.mt_ordens_montagem_externa;
create trigger trg_elo_pcp_decisao_ordem_externa
after insert or update on public.mt_ordens_montagem_externa
for each statement execute function public.elo_pcp_disparar_decisao_externa();

drop trigger if exists trg_elo_pcp_decisao_equipe_externa on public.mt_equipe_montagem_externa;
create trigger trg_elo_pcp_decisao_equipe_externa
after insert or update on public.mt_equipe_montagem_externa
for each statement execute function public.elo_pcp_disparar_decisao_externa();

comment on function public.elo_pcp_disparar_decisao_externa() is
'Gatilho de governanca para consolidacao decisoria do PCP externo. Registra PENDING_INPUT; nao executa dimensionamento de RH nem altera dados operacionais.';
