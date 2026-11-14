-- ELO Demand Intelligence — governed source integration
-- Classification: DATA/MIGRATION
-- Purpose: reuse the existing learning source registry and connect the
-- operational demand chain to the already-implemented cognitive sequencer.
-- No KPI, learning rule, or canonical knowledge is promoted by this migration.

begin;

-- Register only existing operational authorities/read-models. The registry is
-- consultative: it does not turn source rows into validated learning.
insert into public.elo_aprendizado_fontes (
  schema_name,
  table_name,
  dominio_codigo,
  prioridade,
  extracao_ativa,
  regra_extracao,
  enabled,
  extraction_mode
)
select *
from (values
  ('public','mt_pedidos_venda','comercial_licitacoes',120,true,
    jsonb_build_object('tipo','demanda_comercial_cabecalho','somente_leitura',true,'preservar_proveniencia',true,'nao_promover_aprendizado',true),
    true,'registro_para_experiencia'),
  ('public','mt_demanda_historico','planejamento_demanda',121,true,
    jsonb_build_object('tipo','demanda_historica_real','somente_leitura',true,'preservar_proveniencia',true,'preservar_natureza_demanda',true,'preservar_chave_comparabilidade',true,'nao_promover_aprendizado',true),
    true,'registro_para_experiencia'),
  ('public','mt_previsoes_demanda','planejamento_demanda',122,true,
    jsonb_build_object('tipo','previsao_demanda','somente_leitura',true,'preservar_proveniencia',true,'classificacao_epistemica','PREVISAO','nao_tratar_como_fato',true,'nao_promover_aprendizado',true),
    true,'registro_para_experiencia'),
  ('public','mt_balanco_demanda','planejamento_demanda',123,true,
    jsonb_build_object('tipo','balanco_demanda_estoque_producao','somente_leitura',true,'preservar_proveniencia',true,'classificacao_epistemica','DERIVADO','nao_promover_aprendizado',true),
    true,'registro_para_experiencia'),
  ('public','v_elo_diretoria_comercial_estoque','planejamento_demanda',124,true,
    jsonb_build_object('tipo','read_model_comercial_demanda_retorno_estoque','somente_leitura',true,'preservar_proveniencia',true,'respeitar_unidade_medida',true,'gap_nao_e_zero',true,'retorno_previsto_nao_e_estoque_livre',true,'nao_promover_aprendizado',true),
    true,'registro_para_experiencia'),
  ('public','v_elo_pcp_demanda_fluxo_patio','planejamento_pcp',125,true,
    jsonb_build_object('tipo','read_model_demanda_fluxo_patio','somente_leitura',true,'preservar_proveniencia',true,'exigir_unidade_fisica_para_cobertura',true,'gap_nao_e_zero',true,'nao_promover_aprendizado',true),
    true,'registro_para_experiencia'),
  ('public','mt_devolucoes','estoque',126,true,
    jsonb_build_object('tipo','retorno_real_locacao','somente_leitura',true,'preservar_proveniencia',true,'retorno_nao_e_disponibilidade',true,'nao_promover_aprendizado',true),
    true,'registro_para_experiencia'),
  ('public','mt_devolucao_itens','estoque',127,true,
    jsonb_build_object('tipo','retorno_real_unidade_modular','somente_leitura',true,'preservar_proveniencia',true,'exigir_inspecao_liberacao',true,'nao_promover_aprendizado',true),
    true,'registro_para_experiencia'),
  ('public','mt_planos_pcp','planejamento_pcp',128,true,
    jsonb_build_object('tipo','plano_pcp','somente_leitura',true,'preservar_proveniencia',true,'nao_promover_aprendizado',true),
    true,'registro_para_experiencia'),
  ('public','mt_linhas_plano_pcp','planejamento_pcp',129,true,
    jsonb_build_object('tipo','linha_plano_pcp','somente_leitura',true,'preservar_proveniencia',true,'nao_promover_aprendizado',true),
    true,'registro_para_experiencia'),
  ('public','mt_ordens_producao','producao_fluxo_modular',130,true,
    jsonb_build_object('tipo','ordem_producao','somente_leitura',true,'preservar_proveniencia',true,'separar_planejado_realizado',true,'nao_promover_aprendizado',true),
    true,'registro_para_experiencia'),
  ('public','mt_capacidade_diaria','planejamento_pcp',131,true,
    jsonb_build_object('tipo','capacidade_diaria','somente_leitura',true,'preservar_proveniencia',true,'nao_promover_aprendizado',true),
    true,'registro_para_experiencia')
) as v(schema_name,table_name,dominio_codigo,prioridade,extracao_ativa,regra_extracao,enabled,extraction_mode)
where not exists (
  select 1
  from public.elo_aprendizado_fontes f
  where f.schema_name = v.schema_name
    and f.table_name = v.table_name
);

-- Enrich the existing demand-learning candidate rather than creating a second
-- concept or a competing reasoning pattern.
update public.elo_aprendizado_demanda d
set
  sinais_demanda = coalesce(d.sinais_demanda, '{}'::jsonb) || jsonb_build_object(
    'cadeia_integrada', jsonb_build_array(
      'COMERCIAL','DEMANDA_HISTORICA','PREVISAO','RETORNO','INSPECAO_REPARO',
      'ESTOQUE_OK_LIVRE','PCP','CAPACIDADE','PRODUCAO','DISPONIBILIDADE_PROJETADA',
      'COBERTURA_RISCO','DECISAO','REALIZADO','ERRO','APRENDIZADO'
    ),
    'classes_epistemicas', jsonb_build_array(
      'FATO','DERIVADO','INDICIO','HIPOTESE','PREVISAO','RECOMENDACAO','DECISAO','APRENDIZADO_VALIDADO'
    )
  ),
  premissas = coalesce(d.premissas, '{}'::jsonb) || jsonb_build_object(
    'estoque_fisico_nao_e_estoque_livre', true,
    'retorno_nao_e_disponibilidade', true,
    'previsao_nao_e_fato', true,
    'decisao_requer_evidencia', true,
    'previsto_realizado_fecha_aprendizado', true
  ),
  verificacoes = coalesce(d.verificacoes, '{}'::jsonb) || jsonb_build_object(
    'integracao_fontes_v2', jsonb_build_array(
      'classificar_fonte_e_unidade',
      'preservar_spot_evento_sazonalidade',
      'separar_confirmado_previsto',
      'validar_retorno_inspecao_reparo_antes_disponibilidade',
      'confrontar_estoque_pcp_capacidade_producao',
      'calcular_risco_sem_converter_gap_em_zero',
      'confrontar_previsto_realizado',
      'promover_aprendizado_somente_apos_gate'
    )
  ),
  evidencias = coalesce(d.evidencias, '[]'::jsonb) || jsonb_build_array(
    jsonb_build_object(
      'data','2026-10-29',
      'tipo','integracao_governada_fontes_demanda_inteligente',
      'origem','GitHub main + Supabase Elo-forge',
      'estado','CANDIDATO',
      'observacao','Reuso do motor e dos KPIs existentes; sem promocao automatica de conhecimento.'
    )
  ),
  updated_at = now()
where d.metodo = 'ORDEM_COGNITIVA_DEMANDA_INTELIGENTE_V1';

commit;
