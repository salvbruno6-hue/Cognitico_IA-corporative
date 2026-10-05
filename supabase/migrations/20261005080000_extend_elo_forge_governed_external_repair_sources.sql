-- Extend the canonical Forge source catalog for conversational retrieval.
-- No new authority is created. These are existing operational tables and
-- relational bridge tables used only through the governed Forge read path.

insert into public.elo_aprendizado_fontes
(schema_name, table_name, dominio_codigo, prioridade, extracao_ativa, regra_extracao, enabled, extraction_mode)
values
('public','dimensoes','produtos',55,true,'{"tipo":"dimensao","preservar_proveniencia":true}',true,'registro_para_experiencia'),
('public','estrutura_modular','produtos',56,true,'{"tipo":"estrutura_modular","preservar_proveniencia":true}',true,'registro_para_experiencia'),
('public','estrutura_modular_itens','produtos',57,true,'{"tipo":"estrutura_modular_item","preservar_proveniencia":true}',true,'registro_para_experiencia'),
('public','mt_pedidos_venda_itens','operacoes_externas',82,true,'{"tipo":"ponte_pedido_modelo","preservar_proveniencia":true}',true,'registro_para_experiencia'),
('public','mt_ordens_montagem_externa','operacoes_externas',83,true,'{"tipo":"ordem_montagem_externa","preservar_proveniencia":true}',true,'registro_para_experiencia'),
('public','mt_equipe_montagem_externa','operacoes_externas',84,true,'{"tipo":"equipe_montagem_externa","preservar_proveniencia":true}',true,'registro_para_experiencia'),
('public','mt_funcoes_montagem','operacoes_externas',85,true,'{"tipo":"funcao_montagem_externa","preservar_proveniencia":true}',true,'registro_para_experiencia'),
('public','mt_unidades_modulares','reparos_modulares',103,true,'{"tipo":"unidade_modular","preservar_proveniencia":true}',true,'registro_para_experiencia'),
('public','mt_ordens_reparo','reparos_modulares',104,true,'{"tipo":"ordem_reparo_modular","preservar_proveniencia":true}',true,'registro_para_experiencia')
on conflict (schema_name, table_name) do update set
  dominio_codigo=excluded.dominio_codigo,
  prioridade=excluded.prioridade,
  extracao_ativa=true,
  regra_extracao=excluded.regra_extracao,
  enabled=true,
  extraction_mode=excluded.extraction_mode,
  updated_at=now();
