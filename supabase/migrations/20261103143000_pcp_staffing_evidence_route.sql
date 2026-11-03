-- Governed PCP staffing-evidence route.
-- Extends the existing critical-gap reasoning candidate; it does not create
-- an HR registry or reuse external-mounting tables as internal shop-floor truth.

update public.elo_aprendizado_conceitos
set conteudo = conteudo || jsonb_build_object(
  'roteiro_coleta_capacidade_montagem', jsonb_build_object(
    'objetivo', 'caracterizar a capacidade observada e separar restrição de mão de obra de restrições externas antes de qualquer cálculo de contratação',
    'ordem', jsonb_build_array(
      'PERIODO_OBSERVADO',
      'EQUIPE_POR_SETOR_FUNCAO',
      'TURNOS_JORNADA',
      'HORAS_EXTRAS_ABSENTEISMO',
      'MIX_MODELOS',
      'EL_E_MATERIAIS',
      'RETRABALHO_E_ESPERAS',
      'WIP_E_EQUIPAMENTOS',
      'PRODUCAO_REALIZADA',
      'CAUSA_RESTRICAO',
      'PRODUTIVIDADE_MARGINAL_POR_COLABORADOR'
    ),
    'gate_contratacao', 'somente quando CAUSA_RESTRICAO=MAO_DE_OBRA e PRODUTIVIDADE_MARGINAL_POR_COLABORADOR estiver comprovada',
    'estado_persistencia_interna', 'GAP_OWNER_NAO_LOCALIZADO',
    'observacao_persistencia', 'mt_equipe_montagem_externa e mt_funcoes_montagem modelam montagem externa e não devem ser reutilizadas silenciosamente para a oficina interna',
    'superficies_existentes_consultivas', jsonb_build_array(
      'v_elo_pcp_capacidade_rh_montagem',
      'v_elo_pcp_capacidade_montagem_externa',
      'v_elo_pcp_dados_pendentes',
      'v_elo_pcp_dialogo_regras'
    )
  ),
  'estado_dado_montagem_6_dia', jsonb_build_object(
    'classificacao', 'EVIDENCIA_HISTORICA_A_CARACTERIZAR',
    'valor', 6,
    'unidade', 'MODULOS_DIA',
    'nao_promover_como', 'CAPACIDADE_CANONICA_VIGENTE'
  )
),
updated_at = now()
where codigo = 'ORCH.CRITICAL.GAP.REASONING.PCP.CASE';

update public.elo_aprendizado_pcp_planejamento p
set criterios_decisao = p.criterios_decisao || jsonb_build_array(
  'contexto completo de equipe não prova por si só que mão de obra é a causa do gargalo',
  'se a causa comprovada não for mão de obra, bloquear cálculo de contratação',
  'se a causa for mão de obra, exigir produtividade marginal por colaborador antes de calcular headcount adicional'
),
excecoes = p.excecoes || jsonb_build_array(
  'OWNER_PERSISTENCIA_EQUIPE_INTERNA_NAO_LOCALIZADO',
  'RESTRICAO_NAO_MAO_DE_OBRA',
  'PRODUTIVIDADE_MARGINAL_NAO_MEDIDA'
),
updated_at = now()
from public.elo_aprendizado_conceitos c
where p.conceito_id = c.id
  and c.codigo = 'ORCH.CRITICAL.GAP.REASONING.PCP.CASE';
