create or replace view public.v_elo_pcp_comunicacao_melhoria
with (security_invoker = true)
as
select
  prioridade,
  codigo,
  gate,
  fonte_autorizada,
  pergunta_gpt as ponto_a_inserir_ou_melhorar,
  motivo,
  bloqueia_execucao,
  campos_obrigatorios,
  case
    when bloqueia_execucao then 'COMUNICAR_E_SOLICITAR_DADO'
    else 'APONTAR_MELHORIA'
  end as acao_elo,
  'ELO_AUTONOMO_COMUNICACAO'::text as autoridade_comunicacao
from public.v_elo_pcp_dados_pendentes
order by prioridade,codigo;

comment on view public.v_elo_pcp_comunicacao_melhoria is
'Projeção governada para comunicação autônoma do ELO. Permite apontar dados faltantes, itens a inserir e melhorias. Não concede autoridade para alterar dados/regras nem liberar gates.';