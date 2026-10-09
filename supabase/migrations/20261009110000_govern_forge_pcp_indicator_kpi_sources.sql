-- Govern existing PCP indicator read-models and formal KPI registries for Forge/MCP retrieval.
-- This migration adds no new calculation authority and performs no operational writes.
-- Indicators remain indicators unless a formal definition exists in mt_definicoes_kpi.

insert into public.elo_aprendizado_fontes
(schema_name, table_name, dominio_codigo, prioridade, extracao_ativa, regra_extracao, enabled, extraction_mode)
values
(
  'public',
  'v_elo_pcp_carga_capacidade_periodo',
  'planejamento_pcp',
  116,
  true,
  '{"tipo":"read_model_indicador_capacidade","escopo":"global","preservar_proveniencia":true,"somente_leitura":true,"nao_promover_a_kpi":true}',
  true,
  'registro_para_experiencia'
),
(
  'public',
  'v_elo_pcp_indicadores_montagem_externa',
  'operacoes_externas',
  117,
  true,
  '{"tipo":"read_model_indicadores_montagem_externa","escopo":"global","preservar_proveniencia":true,"somente_leitura":true,"nao_promover_a_kpi":true}',
  true,
  'registro_para_experiencia'
),
(
  'public',
  'mt_definicoes_kpi',
  'gestao_indicadores',
  118,
  true,
  '{"tipo":"kpi_definition_registry","escopo":"global","preservar_proveniencia":true,"somente_leitura":true,"autoridade_kpi_formal":true,"nao_criar_kpi":true}',
  true,
  'registro_para_experiencia'
),
(
  'public',
  'mt_snapshots_kpi',
  'gestao_indicadores',
  119,
  true,
  '{"tipo":"kpi_snapshot_registry","escopo":"global","preservar_proveniencia":true,"somente_leitura":true,"depende_definicao_kpi":true,"nao_criar_kpi":true}',
  true,
  'registro_para_experiencia'
)
on conflict (schema_name, table_name) do update set
  dominio_codigo = excluded.dominio_codigo,
  prioridade = excluded.prioridade,
  extracao_ativa = true,
  regra_extracao = excluded.regra_extracao,
  enabled = true,
  extraction_mode = excluded.extraction_mode,
  updated_at = now();
