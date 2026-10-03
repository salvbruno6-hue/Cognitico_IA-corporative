-- ELO PCP: fila canônica de dados faltantes para comunicação via GPT.
-- Propósito: transformar GAPs de dados em solicitações objetivas e rastreáveis.
-- Regra: o ELO identifica o dado ausente, a fonte autorizada, os campos e a pergunta.
-- O ELO nunca infere ou inventa o valor ausente.
-- A view usa security_invoker para respeitar as políticas das fontes subjacentes.

create or replace view public.v_elo_pcp_dados_pendentes
with (security_invoker = true)
as
with resumo as (
  select * from public.v_elo_pcp_decisao_externa_resumo limit 1
),
detalhes as (
  select distinct
    d.modelo_id,
    d.modelo_codigo,
    d.modelo_nome,
    d.natureza_demanda,
    d.chave_comparabilidade,
    d.proxima_informacao_decisoria,
    d.estado_comparabilidade,
    d.estado_fator,
    d.gaps_composicao
  from public.v_elo_pcp_decisao_externa_detalhe d
),
solicitacoes as (
  select
    1::integer as prioridade,
    'HISTORICO_COMPARAVEL'::text as codigo,
    'DADO'::text as tipo_solicitacao,
    'REFERENCIA_HISTORICA'::text as gate,
    'mt_demanda_historico'::text as fonte_autorizada,
    'Informe a demanda histórica real de 01/09/2025 a 28/02/2026, por modelo, natureza da demanda e chave de comparabilidade quando aplicável.'::text as pergunta_gpt,
    'Sem histórico comparável o PCP não pode validar o fator de crescimento/redução.'::text as motivo,
    true as bloqueia_execucao,
    jsonb_build_array('modelo_id','periodo_inicio','periodo_fim','quantidade_real','natureza_demanda','chave_comparabilidade') as campos_obrigatorios
  from resumo r
  where r.estado_decisao = 'AGUARDANDO_HISTORICO'

  union all

  select
    2,
    'PREVISAO_HORIZONTE',
    'DADO',
    'REFERENCIA_FUTURA',
    'mt_previsoes_demanda',
    'Informe a previsão de demanda de 01/09/2026 a 28/02/2027, por modelo, natureza da demanda e chave de comparabilidade quando aplicável.',
    'Sem previsão futura o PCP não consegue comparar o horizonte futuro com a referência histórica.',
    true,
    jsonb_build_array('modelo_id','periodo_inicio','periodo_fim','quantidade_prevista','natureza_demanda','chave_comparabilidade')
  from resumo r
  where r.estado_decisao = 'AGUARDANDO_PREVISAO'

  union all

  select
    3,
    'COMPARABILIDADE',
    'DADO',
    'VALIDACAO_DE_COMPARABILIDADE',
    'PCP_DEMANDA_CRESCIMENTO_REFERENCIA_COMPARAVEL',
    'Informe ou valide a natureza da demanda e a chave de comparabilidade dos registros que ainda não podem ser considerados equivalentes. O ELO não deve inferir essa chave.',
    'Sem comparabilidade validada o fator não pode ser calculado.',
    true,
    jsonb_build_array('modelo_id','natureza_demanda','chave_comparabilidade')
  from resumo r
  where r.estado_decisao = 'AGUARDANDO_VALIDACAO_DE_COMPARABILIDADE'

  union all

  select
    4,
    'COMPOSICAO_FUNCIONAL',
    'DADO',
    'DEMANDA_HUMANA',
    'evidencia_operacional_validada',
    'Informe ou valide a composição funcional real necessária para os modelos/ordens indicados, incluindo as funções envolvidas e a evidência operacional que sustenta essa composição.',
    'Sem composição funcional validada o crescimento de demanda não pode ser convertido em demanda humana por função.',
    true,
    jsonb_build_array('modelo_id','funcao','evidencia_origem')
  from resumo r
  where r.estado_decisao = 'AGUARDANDO_COMPOSICAO_OPERACIONAL'

  union all

  select
    5,
    'HISTORICO_HUMANO_POR_FUNCAO',
    'DADO',
    'DEMANDA_HUMANA',
    'v_elo_pcp_demanda_humana_historica_externa',
    'Informe ou valide o histórico de demanda humana por função para o modelo/natureza indicados. Não informe quadro de RH; informe demanda operacional observada.',
    'Sem histórico humano por função o fator não pode ser aplicado à demanda humana correspondente.',
    true,
    jsonb_build_array('modelo_id','natureza_demanda','funcao_codigo','demanda_colaboradores_media_dia','horas_demanda_acumuladas')
  from detalhes d
  where d.proxima_informacao_decisoria = 'INFORMAR_HISTORICO_HUMANO_POR_FUNCAO'

  union all

  select
    6,
    'CHAVE_COMPARABILIDADE',
    'DADO',
    'REFERENCIA_HISTORICA',
    'PCP_DEMANDA_CRESCIMENTO_REFERENCIA_COMPARAVEL',
    'Informe a chave de comparabilidade do registro indicado. Se não houver correspondência real, informe explicitamente que o registro não é comparável.',
    'A ausência de chave impede o ELO de afirmar equivalência entre demandas.',
    true,
    jsonb_build_array('modelo_id','natureza_demanda','chave_comparabilidade')
  from detalhes d
  where d.proxima_informacao_decisoria = 'INFORMAR_CHAVE_DE_COMPARABILIDADE'

  union all

  select
    7,
    'DADO_ORIGEM',
    'DADO',
    'VALIDACAO',
    'fonte_operacional_canonica',
    'Informe qual é a fonte operacional autorizada para o dado faltante indicado pelo ELO e forneça o registro correspondente. O ELO não substituirá a ausência por estimativa.',
    'O dado de origem não está suficientemente identificado para sustentar a decisão.',
    true,
    jsonb_build_array('fonte','identificador_registro','periodo','valor')
  from detalhes d
  where d.proxima_informacao_decisoria = 'VALIDAR_DADOS_DE_ORIGEM'
)
select
  prioridade,
  codigo,
  tipo_solicitacao,
  gate,
  fonte_autorizada,
  pergunta_gpt,
  motivo,
  bloqueia_execucao,
  campos_obrigatorios,
  now() as atualizado_em
from solicitacoes
order by prioridade, codigo;

comment on view public.v_elo_pcp_dados_pendentes is
'Fila canônica de dados faltantes para comunicação do ELO via GPT. Determina o próximo dado necessário por gate, sem inferir valores. O GPT deve formular a pergunta usando pergunta_gpt e bloquear o cálculo quando bloqueia_execucao=true.';
