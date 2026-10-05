-- Govern canonical PCP read-models for conversational Forge retrieval.
-- These are existing read-only views; no new authority is created.

insert into public.elo_aprendizado_fontes
(schema_name, table_name, dominio_codigo, prioridade, extracao_ativa, regra_extracao, enabled, extraction_mode)
values
('public','v_elo_pcp_cobertura_demanda_externa','planejamento_pcp',112,true,'{"tipo":"read_model_cobertura_demanda","preservar_proveniencia":true,"somente_leitura":true}',true,'registro_para_experiencia'),
('public','v_elo_pcp_decisao_externa_detalhe','operacoes_externas',113,true,'{"tipo":"read_model_decisao_externa_detalhe","preservar_proveniencia":true,"somente_leitura":true}',true,'registro_para_experiencia'),
('public','v_elo_pcp_decisao_externa_resumo','operacoes_externas',114,true,'{"tipo":"read_model_decisao_externa_resumo","escopo":"global","preservar_proveniencia":true,"somente_leitura":true}',true,'registro_para_experiencia'),
('public','v_elo_pcp_dialogo_regras','planejamento_pcp',115,true,'{"tipo":"read_model_regras_dialogo","escopo":"global","preservar_proveniencia":true,"somente_leitura":true}',true,'registro_para_experiencia')
on conflict (schema_name, table_name) do update set
  dominio_codigo=excluded.dominio_codigo,
  prioridade=excluded.prioridade,
  extracao_ativa=true,
  regra_extracao=excluded.regra_extracao,
  enabled=true,
  extraction_mode=excluded.extraction_mode,
  updated_at=now();
