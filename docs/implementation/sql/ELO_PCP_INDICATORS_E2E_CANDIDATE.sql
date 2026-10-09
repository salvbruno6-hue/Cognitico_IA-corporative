-- ELO PCP/KPI E2E — SQL CANDIDATO DE IMPLEMENTAÇÃO
--
-- NÃO É MIGRATION CANÔNICA e NÃO deve ser aplicado diretamente em produção.
-- O arquivo final deve ser criado por `supabase migration new <nome>` no ambiente
-- de implementação e então receber somente o SQL validado deste candidato.
--
-- Objetivo: governar read-models de indicadores e registros formais de KPI já
-- existentes sem criar nova autoridade, sem promover indicador a KPI e sem
-- escrever dados operacionais.

begin;

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

commit;

-- Validações obrigatórias pós-migration:
-- 1. as quatro fontes aparecem em elo_aprendizado_fontes com enabled/extracao_ativa=true;
-- 2. nenhuma escrita ocorre nas views ou tabelas operacionais/KPI de origem;
-- 3. ausência de linhas nas views retorna ausência de evidência, não KPI=0;
-- 4. mt_definicoes_kpi continua sendo a autoridade para existência de KPI formal;
-- 5. mt_snapshots_kpi só é interpretada em relação a uma definição de KPI existente;
-- 6. o runtime expõe provenance/source_table/source_fields para cada indicador lido;
-- 7. nenhum read-model é promovido automaticamente a KPI.
