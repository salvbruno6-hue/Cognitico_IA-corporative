create or replace view public.v_elo_pcp_demanda_fluxo_patio
with (security_invoker = true)
as
with modelo_familia as (
  select
    m.id as modelo_id,
    case
      when upper(trim(coalesce(nullif(m.familia, ''), nullif(t.tipo, ''), ''))) in ('MODULO', 'MÓDULO') then 'MODULO'
      when upper(trim(coalesce(nullif(m.familia, ''), nullif(t.tipo, ''), ''))) in ('CONTEINER', 'CONTÊINER', 'CONTAINER') then 'CONTEINER'
      else 'OUTRO'
    end as familia_produto
  from public.modelos m
  left join public.taxonomia t on t.id = m.taxonomia_id
),
baseline as (
  select
    tenant_id,
    periodo_mes,
    familia_produto,
    unidade_medida,
    demanda_total as demanda_referencia,
    demanda_evento as demanda_evento_referencia,
    retornos_previstos as retornos_referencia,
    estoque_protecao_comercial_referencia as protecao_comercial_referencia,
    gap_quantidade_fisica,
    gap_modelo_canonico,
    gap_tenant
  from elo_private.pcp_diretoria_comercial_mensal
  where nivel_analise = 'FAMILIA'
    and tipo_registro = 'PREVISAO_BASE'
    and periodo_mes >= date_trunc('month', current_date)::date
),
pedidos as (
  select
    p.tenant_id,
    date_trunc('month', coalesce(i.data_solicitada, p.data_entrega_solicitada))::date as periodo_mes,
    mf.familia_produto,
    sum(coalesce(i.quantidade, 0)) as demanda_fisica_confirmada,
    sum(coalesce(i.quantidade, 0)) filter (
      where upper(coalesce(p.natureza_demanda, '')) = 'EVENTO'
    ) as demanda_evento_fisica_confirmada
  from public.mt_pedidos_venda p
  join public.mt_pedidos_venda_itens i on i.pedido_venda_id = p.id
  join modelo_familia mf on mf.modelo_id = i.modelo_id
  where coalesce(i.data_solicitada, p.data_entrega_solicitada) is not null
    and coalesce(i.data_solicitada, p.data_entrega_solicitada) >= date_trunc('month', current_date)::date
    and upper(coalesce(p.status, '')) not in ('CANCELADO', 'CANCELADA')
  group by
    p.tenant_id,
    date_trunc('month', coalesce(i.data_solicitada, p.data_entrega_solicitada))::date,
    mf.familia_produto
),
producao as (
  select
    o.tenant_id,
    date_trunc('month', coalesce(o.fim_planejado, o.inicio_planejado))::date as periodo_mes,
    mf.familia_produto,
    count(*)::bigint as ordens_producao,
    sum(coalesce(o.quantidade_planejada, 0)) as producao_planejada,
    sum(coalesce(o.quantidade_produzida, 0)) as producao_produzida,
    sum(greatest(coalesce(o.quantidade_planejada, 0) - coalesce(o.quantidade_produzida, 0), 0)) as producao_em_aberto,
    count(*) filter (where o.fim_planejado is null)::bigint as ordens_sem_fim_planejado
  from public.mt_ordens_producao o
  join modelo_familia mf on mf.modelo_id = o.modelo_id
  where coalesce(o.fim_planejado, o.inicio_planejado) is not null
    and coalesce(o.fim_planejado, o.inicio_planejado) >= date_trunc('month', current_date)::date
    and upper(coalesce(o.status, '')) not in ('CANCELADO', 'CANCELADA')
  group by
    o.tenant_id,
    date_trunc('month', coalesce(o.fim_planejado, o.inicio_planejado))::date,
    mf.familia_produto
),
operacoes as (
  select
    o.tenant_id,
    date_trunc('month', coalesce(o.fim_planejado, o.inicio_planejado))::date as periodo_mes,
    mf.familia_produto,
    count(op.id)::bigint as operacoes_registradas,
    count(op.id) filter (where op.fim_real is not null)::bigint as operacoes_concluidas
  from public.mt_ordens_producao o
  join modelo_familia mf on mf.modelo_id = o.modelo_id
  left join public.mt_operacoes_ordem_producao op on op.ordem_producao_id = o.id
  where coalesce(o.fim_planejado, o.inicio_planejado) is not null
    and coalesce(o.fim_planejado, o.inicio_planejado) >= date_trunc('month', current_date)::date
    and upper(coalesce(o.status, '')) not in ('CANCELADO', 'CANCELADA')
  group by
    o.tenant_id,
    date_trunc('month', coalesce(o.fim_planejado, o.inicio_planejado))::date,
    mf.familia_produto
),
estoque as (
  select
    u.tenant_id,
    mf.familia_produto,
    count(*)::numeric as unidades_cadastradas,
    count(*) filter (
      where coalesce(u.disponivel_expedicao, false) = true
        and upper(coalesce(u.status_qualidade, '')) not in ('REPROVADO', 'BLOQUEADO')
    )::numeric as unidades_disponiveis_expedicao,
    count(*) filter (
      where coalesce(u.disponivel_expedicao, false) = true
        and upper(coalesce(u.status_qualidade, '')) not in ('REPROVADO', 'BLOQUEADO')
        and upper(coalesce(l.tipo_local, '')) = 'PATIO'
    )::numeric as unidades_patio_confirmadas,
    count(*) filter (
      where coalesce(u.disponivel_expedicao, false) = true
        and upper(coalesce(u.status_qualidade, '')) not in ('REPROVADO', 'BLOQUEADO')
        and u.local_atual_id is null
    )::numeric as unidades_disponiveis_sem_local
  from public.mt_unidades_modulares u
  join modelo_familia mf on mf.modelo_id = u.modelo_id
  left join public.mt_locais l on l.id = u.local_atual_id
  group by u.tenant_id, mf.familia_produto
),
expedicoes as (
  select
    e.tenant_id,
    date_trunc('month', e.data_planejada)::date as periodo_mes,
    mf.familia_produto,
    sum(coalesce(ei.quantidade, case when ei.unidade_modular_id is not null then 1 else 0 end)) as expedicoes_planejadas
  from public.mt_expedicoes e
  join public.mt_expedicao_itens ei on ei.expedicao_id = e.id
  join public.mt_unidades_modulares u on u.id = ei.unidade_modular_id
  join modelo_familia mf on mf.modelo_id = u.modelo_id
  where e.data_planejada is not null
    and e.data_planejada >= date_trunc('month', current_date)::date
    and upper(coalesce(e.status, '')) not in ('CANCELADO', 'CANCELADA')
  group by e.tenant_id, date_trunc('month', e.data_planejada)::date, mf.familia_produto
),
retornos as (
  select
    c.tenant_id,
    date_trunc('month', c.fim)::date as periodo_mes,
    mf.familia_produto,
    sum(coalesce(i.quantidade, 0)) as retornos_contratuais_previstos
  from public.mt_contratos_locacao c
  join public.mt_pedidos_venda p on p.id = c.pedido_venda_id
  join public.mt_pedidos_venda_itens i on i.pedido_venda_id = p.id
  join modelo_familia mf on mf.modelo_id = i.modelo_id
  where c.fim is not null
    and c.fim >= date_trunc('month', current_date)::date
    and upper(coalesce(c.status, '')) not in ('CANCELADO', 'CANCELADA')
  group by c.tenant_id, date_trunc('month', c.fim)::date, mf.familia_produto
),
reparos as (
  select
    r.tenant_id,
    date_trunc('month', r.data_final_reparo)::date as periodo_mes,
    mf.familia_produto,
    count(distinct r.unidade_modular_id)::numeric as reparos_previstos_conclusao
  from public.mt_ordens_reparo r
  join public.mt_unidades_modulares u on u.id = r.unidade_modular_id
  join modelo_familia mf on mf.modelo_id = u.modelo_id
  where r.data_final_reparo is not null
    and r.data_final_reparo >= date_trunc('month', current_date)::date
    and upper(coalesce(r.status, '')) not in ('CANCELADO', 'CANCELADA', 'CONCLUIDO', 'CONCLUIDA')
  group by r.tenant_id, date_trunc('month', r.data_final_reparo)::date, mf.familia_produto
),
reparo_gaps as (
  select
    tenant_id,
    count(*) filter (
      where unidade_modular_id is null
        and upper(coalesce(status, '')) not in ('CANCELADO', 'CANCELADA', 'CONCLUIDO', 'CONCLUIDA')
    )::bigint as reparos_abertos_sem_unidade,
    count(*) filter (
      where unidade_modular_id is not null
        and data_final_reparo is null
        and upper(coalesce(status, '')) not in ('CANCELADO', 'CANCELADA', 'CONCLUIDO', 'CONCLUIDA')
    )::bigint as reparos_abertos_sem_data
  from public.mt_ordens_reparo
  group by tenant_id
),
fluxo_readiness as (
  select
    (select count(*)::bigint from public.fluxo_produtivo_modular_etapas where upper(coalesce(status, '')) = 'ATIVO') as etapas_fluxo_referencia,
    (select count(*)::bigint from public.fluxo_produtivo_modular_etapas where upper(coalesce(status, '')) = 'ATIVO' and tempo_unitario_min is not null) as etapas_com_tempo,
    (select count(*)::bigint from public.fluxo_produtivo_modular_etapas where upper(coalesce(status, '')) = 'ATIVO' and capacidade is not null) as etapas_com_capacidade,
    (select max(lead_time_dias) from public.fluxo_produtivo_modular where ativo = true) as lead_time_fluxo_dias,
    (select max(capacidade_referencia) from public.fluxo_produtivo_modular where ativo = true) as capacidade_fluxo_referencia,
    (select count(*)::bigint from public.mt_operacoes_roteiro) as operacoes_roteiro_cadastradas,
    (select count(*)::bigint from public.mt_tempo_fabricacao_estrutura_modular where ativo = true) as evidencias_tempo_estrutura_20_pes,
    (select sum(coalesce(tempo_operacao_min, 0)) from public.mt_tempo_fabricacao_estrutura_modular where ativo = true) as tempo_estrutura_20_pes_min
),
chaves as (
  select tenant_id, periodo_mes, familia_produto from baseline
  union
  select tenant_id, periodo_mes, familia_produto from pedidos
  union
  select tenant_id, periodo_mes, familia_produto from producao
  union
  select tenant_id, periodo_mes, familia_produto from expedicoes
  union
  select tenant_id, periodo_mes, familia_produto from retornos
  union
  select tenant_id, periodo_mes, familia_produto from reparos
),
base as (
  select
    k.tenant_id,
    k.periodo_mes,
    k.familia_produto,
    b.unidade_medida,
    b.demanda_referencia,
    b.demanda_evento_referencia,
    b.retornos_referencia,
    b.protecao_comercial_referencia,
    p.demanda_fisica_confirmada,
    p.demanda_evento_fisica_confirmada,
    pr.ordens_producao,
    pr.producao_planejada,
    pr.producao_produzida,
    pr.producao_em_aberto,
    pr.ordens_sem_fim_planejado,
    op.operacoes_registradas,
    op.operacoes_concluidas,
    e.unidades_cadastradas,
    e.unidades_disponiveis_expedicao,
    e.unidades_patio_confirmadas,
    e.unidades_disponiveis_sem_local,
    ex.expedicoes_planejadas,
    r.retornos_contratuais_previstos,
    rp.reparos_previstos_conclusao,
    rg.reparos_abertos_sem_unidade,
    rg.reparos_abertos_sem_data,
    b.gap_quantidade_fisica,
    b.gap_modelo_canonico,
    b.gap_tenant,
    fr.etapas_fluxo_referencia,
    fr.etapas_com_tempo,
    fr.etapas_com_capacidade,
    fr.lead_time_fluxo_dias,
    fr.capacidade_fluxo_referencia,
    fr.operacoes_roteiro_cadastradas,
    fr.evidencias_tempo_estrutura_20_pes,
    fr.tempo_estrutura_20_pes_min
  from chaves k
  left join baseline b
    on b.tenant_id is not distinct from k.tenant_id
   and b.periodo_mes = k.periodo_mes
   and b.familia_produto = k.familia_produto
  left join pedidos p
    on p.tenant_id is not distinct from k.tenant_id
   and p.periodo_mes = k.periodo_mes
   and p.familia_produto = k.familia_produto
  left join producao pr
    on pr.tenant_id is not distinct from k.tenant_id
   and pr.periodo_mes = k.periodo_mes
   and pr.familia_produto = k.familia_produto
  left join operacoes op
    on op.tenant_id is not distinct from k.tenant_id
   and op.periodo_mes = k.periodo_mes
   and op.familia_produto = k.familia_produto
  left join estoque e
    on e.tenant_id is not distinct from k.tenant_id
   and e.familia_produto = k.familia_produto
  left join expedicoes ex
    on ex.tenant_id is not distinct from k.tenant_id
   and ex.periodo_mes = k.periodo_mes
   and ex.familia_produto = k.familia_produto
  left join retornos r
    on r.tenant_id is not distinct from k.tenant_id
   and r.periodo_mes = k.periodo_mes
   and r.familia_produto = k.familia_produto
  left join reparos rp
    on rp.tenant_id is not distinct from k.tenant_id
   and rp.periodo_mes = k.periodo_mes
   and rp.familia_produto = k.familia_produto
  left join reparo_gaps rg
    on rg.tenant_id is not distinct from k.tenant_id
  cross join fluxo_readiness fr
),
calculado as (
  select
    b.*,
    case
      when b.tenant_id is null or b.unidades_patio_confirmadas is null then null
      else b.unidades_patio_confirmadas
        + sum(coalesce(b.producao_em_aberto, 0) - coalesce(b.expedicoes_planejadas, 0)) over (
            partition by b.tenant_id, b.familia_produto
            order by b.periodo_mes
            rows between unbounded preceding and current row
          )
    end as saldo_patio_planejado_condicional
  from base b
)
select
  tenant_id,
  periodo_mes,
  familia_produto,
  unidade_medida as unidade_demanda_referencia,
  demanda_referencia,
  demanda_evento_referencia,
  demanda_fisica_confirmada,
  demanda_evento_fisica_confirmada,
  retornos_referencia,
  protecao_comercial_referencia,
  ordens_producao,
  producao_planejada,
  producao_produzida,
  producao_em_aberto,
  ordens_sem_fim_planejado,
  operacoes_registradas,
  operacoes_concluidas,
  unidades_cadastradas,
  unidades_disponiveis_expedicao,
  unidades_patio_confirmadas,
  unidades_disponiveis_sem_local,
  expedicoes_planejadas,
  retornos_contratuais_previstos,
  reparos_previstos_conclusao,
  reparos_abertos_sem_unidade,
  reparos_abertos_sem_data,
  saldo_patio_planejado_condicional,
  etapas_fluxo_referencia,
  etapas_com_tempo,
  etapas_com_capacidade,
  lead_time_fluxo_dias,
  capacidade_fluxo_referencia,
  operacoes_roteiro_cadastradas,
  evidencias_tempo_estrutura_20_pes,
  tempo_estrutura_20_pes_min,
  coalesce(gap_quantidade_fisica, false) as gap_quantidade_fisica,
  coalesce(gap_modelo_canonico, false) as gap_modelo_canonico,
  coalesce(gap_tenant, tenant_id is null) as gap_tenant,
  (tenant_id is null or unidades_cadastradas is null) as gap_unidades_modulares,
  (coalesce(unidades_disponiveis_expedicao, 0) > 0 and coalesce(unidades_patio_confirmadas, 0) = 0) as gap_local_patio,
  (coalesce(ordens_producao, 0) > 0 and coalesce(operacoes_registradas, 0) = 0) as gap_execucao_fluxo,
  (coalesce(operacoes_roteiro_cadastradas, 0) = 0) as gap_roteiro_produtivo,
  (coalesce(etapas_com_tempo, 0) < coalesce(etapas_fluxo_referencia, 0) or lead_time_fluxo_dias is null) as gap_tempo_fluxo,
  (coalesce(etapas_com_capacidade, 0) < coalesce(etapas_fluxo_referencia, 0) or capacidade_fluxo_referencia is null) as gap_capacidade_fluxo,
  (coalesce(reparos_abertos_sem_unidade, 0) > 0) as gap_reparo_sem_unidade,
  case
    when demanda_fisica_confirmada is not null then 'DEMANDA_FISICA_CONFIRMADA'
    when demanda_referencia is not null and unidade_medida = 'REGISTRO_EQUIVALENTE' then 'REFERENCIA_NAO_FISICA'
    when demanda_referencia is not null then 'REFERENCIA_ANALITICA'
    else 'SEM_DEMANDA_REGISTRADA'
  end as estado_demanda,
  case
    when tenant_id is null then 'GAP_TENANT'
    when unidades_cadastradas is null then 'GAP_UNIDADES_MODULARES'
    when coalesce(unidades_disponiveis_expedicao, 0) > 0 and coalesce(unidades_patio_confirmadas, 0) = 0 then 'GAP_LOCAL_PATIO'
    else 'PATIO_FISICO_RASTREAVEL'
  end as estado_disponibilidade_patio,
  case
    when coalesce(operacoes_roteiro_cadastradas, 0) = 0 then 'GAP_ROTEIRO_PRODUTIVO'
    when coalesce(etapas_com_tempo, 0) < coalesce(etapas_fluxo_referencia, 0) or lead_time_fluxo_dias is null then 'GAP_TEMPO_FLUXO'
    when coalesce(etapas_com_capacidade, 0) < coalesce(etapas_fluxo_referencia, 0) or capacidade_fluxo_referencia is null then 'GAP_CAPACIDADE_FLUXO'
    when coalesce(ordens_producao, 0) > 0 and coalesce(operacoes_registradas, 0) = 0 then 'GAP_EXECUCAO_FLUXO'
    else 'FLUXO_RASTREAVEL'
  end as estado_fluxo_produtivo,
  case
    when tenant_id is null then 'Estabelecer tenant operacional antes de cruzar demanda com ativos, ordens e patio.'
    when unidades_cadastradas is null then 'Carregar e reconciliar unidades modulares fisicas por modelo e local atual.'
    when coalesce(operacoes_roteiro_cadastradas, 0) = 0 then 'Cadastrar roteiro operacional por modelo e relacionar as operacoes das ordens ao fluxo modular.'
    when coalesce(etapas_com_tempo, 0) < coalesce(etapas_fluxo_referencia, 0) or lead_time_fluxo_dias is null then 'Completar tempos/lead time do fluxo com evidencia operacional validada; a evidencia de estrutura 20 pes permanece parcial.'
    when coalesce(etapas_com_capacidade, 0) < coalesce(etapas_fluxo_referencia, 0) or capacidade_fluxo_referencia is null then 'Completar capacidades do fluxo antes de afirmar capacidade de atendimento ate o horizonte.'
    when coalesce(reparos_abertos_sem_unidade, 0) > 0 then 'Reconciliar reparos com unidades fisicas; retorno/reparo previsto nao equivale a estoque livre.'
    else 'Cruzar demanda confirmada, OPs, expedicoes, retornos e disponibilidade fisica para o horizonte solicitado.'
  end as orientacao_elo
from calculado;

comment on view public.v_elo_pcp_demanda_fluxo_patio is
'Read-model PCP que relaciona demanda comercial/eventos, pedidos fisicos, ordens e execucao produtiva, disponibilidade fisica de patio, expedicoes, retornos e reparos. A baseline REGISTRO_EQUIVALENTE e apenas contexto; saldo fisico so e calculado quando houver tenant e unidades fisicas reconciliadas. Retornos e reparos previstos permanecem separados do estoque livre.';