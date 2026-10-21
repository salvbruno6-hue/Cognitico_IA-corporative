-- ELO PCP / Diretoria: baseline analitica mensal Comercial -> Estoque.
-- Esta tabela e derivada e nao substitui mt_demanda_historico, mt_previsoes_demanda,
-- mt_unidades_modulares, mt_ordens_reparo ou demais autoridades operacionais.

create schema if not exists elo_private;

create table if not exists elo_private.pcp_diretoria_comercial_mensal (
  id uuid primary key default gen_random_uuid(),
  fonte_id uuid references public.mt_referencias_fontes(id),
  tenant_id uuid references public.mt_tenants(id),
  nivel_analise text not null check (nivel_analise in ('FAMILIA','MODELO')),
  familia_produto text not null check (familia_produto in ('MODULO','CONTEINER')),
  modelo_id uuid references public.modelos(id),
  modelo_chave_normalizada text,
  modelo_exibicao text,
  periodo_mes date not null,
  tipo_registro text not null check (tipo_registro in ('HISTORICO','PREVISAO_BASE')),
  unidade_medida text not null default 'REGISTRO_EQUIVALENTE'
    check (unidade_medida in ('REGISTRO_EQUIVALENTE','UNIDADE_FISICA')),

  demanda_total numeric,
  demanda_spot numeric,
  demanda_evento numeric,
  demanda_venda numeric,
  transferencias numeric,

  participacao_spot_pct numeric,
  participacao_evento_pct numeric,
  participacao_venda_pct numeric,
  participacao_mes_ano_pct numeric,
  indice_sazonalidade_pct numeric,
  classificacao_sazonalidade text,
  natureza_dominante text,

  crescimento_mom_pct numeric,
  crescimento_yoy_pct numeric,
  crescimento_spot_yoy_pct numeric,
  crescimento_evento_yoy_pct numeric,
  tendencia_yoy text,
  tendencia_base_pct numeric,
  metodo_previsao text,

  retornos_previstos numeric,
  cobertura_retorno_pct numeric,

  estoque_minimo_spot numeric,
  estoque_seguranca_spot numeric,
  estoque_alvo_spot numeric,
  reserva_evento_referencia numeric,
  pressao_venda_referencia numeric,
  estoque_protecao_comercial_referencia numeric,
  necessidade_comercial_total_referencia numeric,
  anos_base_estoque integer,
  confianca_politica text,

  qualidade_data_proposta_pct numeric,
  gap_quantidade_fisica boolean not null default true,
  gap_modelo_canonico boolean not null default true,
  gap_tenant boolean not null default true,
  gap_retorno boolean not null default true,

  source_sha256 text not null,
  regra_versao text not null,
  status_governanca text not null default 'BASELINE_ANALITICA_CSV',
  criado_em timestamptz not null default now(),

  check (
    (nivel_analise = 'FAMILIA' and modelo_chave_normalizada is null)
    or
    (nivel_analise = 'MODELO' and modelo_chave_normalizada is not null)
  )
);

alter table elo_private.pcp_diretoria_comercial_mensal enable row level security;

create policy "service_role_pcp_diretoria_comercial_mensal"
on elo_private.pcp_diretoria_comercial_mensal
for all
to service_role
using (true)
with check (true);

create index if not exists idx_pcp_dir_comercial_periodo
  on elo_private.pcp_diretoria_comercial_mensal (periodo_mes, familia_produto, nivel_analise);

create index if not exists idx_pcp_dir_comercial_modelo
  on elo_private.pcp_diretoria_comercial_mensal (modelo_id, periodo_mes);

create index if not exists idx_pcp_dir_comercial_source
  on elo_private.pcp_diretoria_comercial_mensal (source_sha256, regra_versao);

create unique index if not exists ux_pcp_dir_comercial_linha
  on elo_private.pcp_diretoria_comercial_mensal (
    source_sha256,
    regra_versao,
    nivel_analise,
    familia_produto,
    coalesce(modelo_chave_normalizada, '__FAMILIA__'),
    periodo_mes,
    tipo_registro
  );

comment on table elo_private.pcp_diretoria_comercial_mensal is
'Baseline analitica mensal para apresentacao diretiva Comercial/PCP. Consolida historico e previsao-base por familia/modelo, indicadores SPOT/EVENTO, sazonalidade, crescimento, retorno previsto e politica estatistica de estoque. Nao e autoridade operacional e nao converte registro comercial em unidade fisica sem evidencia.';

comment on column elo_private.pcp_diretoria_comercial_mensal.estoque_minimo_spot is
'Referencia estatistica mensal: teto do P75 historico da demanda SPOT para o mesmo mes-calendario.';

comment on column elo_private.pcp_diretoria_comercial_mensal.estoque_seguranca_spot is
'Diferenca entre teto do P90 e teto do P75 da demanda SPOT do mesmo mes-calendario. E uma reserva empirica, nao substitui calculo classico por lead time/nivel de servico quando esses dados existirem.';

comment on column elo_private.pcp_diretoria_comercial_mensal.reserva_evento_referencia is
'Teto do P75 historico de EVENTO no mesmo mes-calendario. Mantido separado do estoque permanente porque EVENTO nao equivale automaticamente a sazonalidade confirmada futura.';

create or replace view public.v_elo_diretoria_comercial_estoque
with (security_invoker = true)
as
with cobertura_modelo as (
  select
    tenant_id,
    modelo_id,
    familia_produto,
    demanda_prevista,
    estoque_disponivel,
    unidades_em_reparo_recuperaveis,
    producao_programada,
    necessidade_adicional_fabricacao,
    estado_cobertura
  from public.v_elo_pcp_cobertura_demanda_externa
),
cobertura_familia as (
  select
    tenant_id,
    familia_produto,
    sum(demanda_prevista) as demanda_prevista,
    sum(estoque_disponivel) as estoque_disponivel,
    sum(unidades_em_reparo_recuperaveis) as unidades_em_reparo_recuperaveis,
    sum(producao_programada) as producao_programada,
    sum(necessidade_adicional_fabricacao) as necessidade_adicional_fabricacao,
    case
      when count(*) filter (where estado_cobertura like 'GAP_%') > 0 then 'GAP_OPERACIONAL'
      when count(*) filter (where estado_cobertura = 'DEFICIT_FABRICACAO') > 0 then 'DEFICIT_FABRICACAO'
      when count(*) > 0 then 'COBERTA'
      else 'SEM_PREVISAO'
    end as estado_cobertura
  from public.v_elo_pcp_cobertura_demanda_externa
  group by tenant_id, familia_produto
),
base as (
  select
    b.*,
    extract(year from b.periodo_mes)::integer as ano,
    extract(month from b.periodo_mes)::integer as mes_num,
    case extract(month from b.periodo_mes)::integer
      when 1 then 'JAN' when 2 then 'FEV' when 3 then 'MAR' when 4 then 'ABR'
      when 5 then 'MAI' when 6 then 'JUN' when 7 then 'JUL' when 8 then 'AGO'
      when 9 then 'SET' when 10 then 'OUT' when 11 then 'NOV' when 12 then 'DEZ'
    end as mes_nome
  from elo_private.pcp_diretoria_comercial_mensal b
),
integrada as (
  select
    b.*,
    coalesce(m.codigo, null) as modelo_codigo_canonico,
    coalesce(m.nome, b.modelo_exibicao) as modelo_nome_apresentacao,
    case when b.nivel_analise='MODELO' then cm.demanda_prevista else cf.demanda_prevista end as demanda_prevista_operacional,
    case when b.nivel_analise='MODELO' then cm.estoque_disponivel else cf.estoque_disponivel end as estoque_disponivel_operacional,
    case when b.nivel_analise='MODELO' then cm.unidades_em_reparo_recuperaveis else cf.unidades_em_reparo_recuperaveis end as reparos_recuperaveis_operacional,
    case when b.nivel_analise='MODELO' then cm.producao_programada else cf.producao_programada end as producao_programada_operacional,
    case when b.nivel_analise='MODELO' then cm.necessidade_adicional_fabricacao else cf.necessidade_adicional_fabricacao end as necessidade_adicional_fabricacao_operacional,
    case when b.nivel_analise='MODELO' then cm.estado_cobertura else cf.estado_cobertura end as estado_cobertura_operacional
  from base b
  left join public.modelos m on m.id=b.modelo_id
  left join cobertura_modelo cm
    on b.nivel_analise='MODELO'
   and cm.tenant_id=b.tenant_id
   and cm.modelo_id=b.modelo_id
  left join cobertura_familia cf
    on b.nivel_analise='FAMILIA'
   and cf.tenant_id=b.tenant_id
   and cf.familia_produto=b.familia_produto
)
select
  i.id,
  i.fonte_id,
  i.tenant_id,
  i.nivel_analise,
  i.familia_produto,
  i.modelo_id,
  i.modelo_codigo_canonico,
  i.modelo_chave_normalizada,
  i.modelo_nome_apresentacao,
  i.periodo_mes,
  i.ano,
  i.mes_num,
  i.mes_nome,
  i.tipo_registro,
  i.unidade_medida,

  i.demanda_total,
  i.demanda_spot,
  i.demanda_evento,
  i.demanda_venda,
  i.transferencias,
  i.participacao_spot_pct,
  i.participacao_evento_pct,
  i.participacao_venda_pct,
  i.participacao_mes_ano_pct,
  i.indice_sazonalidade_pct,
  i.classificacao_sazonalidade,
  i.natureza_dominante,

  i.crescimento_mom_pct,
  i.crescimento_yoy_pct,
  i.crescimento_spot_yoy_pct,
  i.crescimento_evento_yoy_pct,
  i.tendencia_yoy,
  i.tendencia_base_pct,
  i.metodo_previsao,

  i.retornos_previstos,
  i.cobertura_retorno_pct,

  i.estoque_minimo_spot,
  i.estoque_seguranca_spot,
  i.estoque_alvo_spot,
  i.reserva_evento_referencia,
  i.pressao_venda_referencia,
  i.estoque_protecao_comercial_referencia,
  i.necessidade_comercial_total_referencia,
  i.anos_base_estoque,
  i.confianca_politica,

  i.demanda_prevista_operacional,
  i.estoque_disponivel_operacional,
  i.reparos_recuperaveis_operacional,
  i.producao_programada_operacional,
  i.necessidade_adicional_fabricacao_operacional,
  i.estado_cobertura_operacional,

  case
    when i.unidade_medida <> 'UNIDADE_FISICA' then null
    when i.estoque_disponivel_operacional is null then null
    else i.estoque_disponivel_operacional - i.estoque_minimo_spot
  end as saldo_vs_estoque_minimo,

  case
    when i.unidade_medida <> 'UNIDADE_FISICA' then null
    when i.estoque_disponivel_operacional is null then null
    else
      i.estoque_disponivel_operacional
      + coalesce(i.reparos_recuperaveis_operacional,0)
      + coalesce(i.producao_programada_operacional,0)
      - i.estoque_protecao_comercial_referencia
  end as saldo_vs_protecao_comercial,

  case
    when i.unidade_medida <> 'UNIDADE_FISICA' then 'GAP_QUANTIDADE_FISICA'
    when i.estoque_disponivel_operacional is null then 'AGUARDANDO_ESTOQUE_OPERACIONAL'
    when i.estoque_disponivel_operacional < i.estoque_minimo_spot then 'ABAIXO_MINIMO'
    when i.estoque_disponivel_operacional < i.estoque_alvo_spot then 'ENTRE_MINIMO_E_ALVO'
    else 'ACIMA_ALVO_SPOT'
  end as estado_estoque,

  case
    when i.crescimento_yoy_pct is null then 'SEM_BASE_COMPARAVEL'
    when i.crescimento_yoy_pct > 0 then 'ALTA_DEMANDA'
    when i.crescimento_yoy_pct < 0 then 'QUEDA_DEMANDA'
    else 'DEMANDA_ESTAVEL'
  end as sinal_demanda,

  case
    when i.gap_quantidade_fisica or i.gap_tenant or (i.nivel_analise='MODELO' and i.gap_modelo_canonico)
      then 'GAP_DADOS'
    when i.estado_cobertura_operacional='DEFICIT_FABRICACAO'
      then 'CRITICO'
    when i.crescimento_yoy_pct is not null and i.crescimento_yoy_pct <> 0
      then 'ATENCAO'
    else 'INFORMATIVO'
  end as nivel_alerta_elo,

  case
    when i.crescimento_yoy_pct > 0 then
      'Validar causas externas da alta antes de ampliar estoque/producao: contratos e renovacoes, campanhas comerciais, eventos confirmados, concorrencia, preco e mercado.'
    when i.crescimento_yoy_pct < 0 then
      'Validar causas externas da queda antes de reduzir estoque/producao: perdas de contrato, renovacoes frageis, cancelamentos, concorrencia, preco e mercado.'
    else
      'Monitorar carteira, renovacoes, campanhas, eventos e concorrencia; ausencia de variacao nao elimina risco externo.'
  end as orientacao_cognitiva_elo,

  case
    when i.crescimento_yoy_pct is not null and i.crescimento_yoy_pct <> 0
      then 'SWOT + 5W2H'
    else 'MONITORAMENTO'
  end as ferramenta_qualidade_recomendada,

  jsonb_build_array(
    'perdas_de_contrato',
    'renovacoes_frageis_ou_confirmadas',
    'campanhas_de_novos_clientes',
    'eventos_confirmados_ou_cancelados',
    'aumento_ou_reducao_da_concorrencia',
    'alteracao_de_preco',
    'mudanca_de_mercado'
  ) as checklist_contexto_externo,

  i.qualidade_data_proposta_pct,
  i.gap_quantidade_fisica,
  i.gap_modelo_canonico,
  i.gap_tenant,
  i.gap_retorno,
  i.source_sha256,
  i.regra_versao,
  i.status_governanca,
  i.criado_em
from integrada i;

comment on view public.v_elo_diretoria_comercial_estoque is
'Visao executiva Comercial/PCP por familia e modelo, ano/mes. Mostra SPOT, EVENTO, sazonalidade, crescimento, previsao-base, retornos e politica de estoque; integra estoque/reparo/producao somente quando tenant, modelo e unidade fisica estiverem reconciliados. Sinais externos sao perguntas de validacao, nunca causas presumidas.';